from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
from app.utils.require_auth import require_auth
from datetime import datetime
from app.services.mongo import saveFileRecord, getFileById, getFileByHash
from uuid import uuid4
from bson import ObjectId
import os
from app.utils.hash import generateFileHash
from app.utils.serialize import serialize_file

uploadBP = Blueprint("upload", __name__, url_prefix="/")

ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".pdf", ".webp"}

def allowed_file(filename):
    _, extension = os.path.splitext(filename)
    return extension.lower() in ALLOWED_EXTENSIONS


@uploadBP.route("/upload", methods=["POST"])
@require_auth
def upload_file():
    file = request.files.get("file")
    if not file:
        return jsonify({"success": False, "message": "No file provided"}), 400

    if not allowed_file(file.filename):
        return jsonify({"success": False, "message": "Unsupported file type"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join("uploads", filename)

    # ensure uploads directory exists
    os.makedirs("uploads", exist_ok=True)

    # deduplicate by hash if file already exists
    if os.path.exists(filepath):
        existing_hash = generateFileHash(filepath)
        existing_file = getFileByHash(str(existing_hash))
        if existing_file:
            file_url = f"http://localhost:5000/api/v1/file/{existing_file['_id']}"
            return (
                jsonify(
                    {
                        "success": True,
                        "message": "File already exists",
                        "file_id": str(existing_file["_id"]),
                        "file_url": file_url,
                    }
                ),
                200,
            )

        # rename duplicate file with unique ID
        name, ext = os.path.splitext(filename)
        filename = f"{name}_{uuid4().hex}{ext}"
        filepath = os.path.join("uploads", filename)

    file.save(filepath)

    user_id = request.user.get("user_id")
    if not ObjectId.is_valid(user_id):
        return jsonify({"success": False, "message": "Invalid user ID"}), 400

    file_hash = generateFileHash(filepath)
    file_record = {
        "filename": filename,
        "filepath": filepath,
        "uploaded_at": datetime.now(),
        "uploaded_by": ObjectId(user_id),
        "file_type": file.mimetype,
        "metadata": {},
        "sha-256-hash": str(file_hash),
    }

    file_id = saveFileRecord(file_record)
    file_record["_id"] = file_id
    file_url = f"http://localhost:5000/api/v1/file/{file_id}"

    return (
        jsonify({"success": True, "file_id": file_url, "file_url": file_url}),
        201,
    )


@uploadBP.route("/file/<id>", methods=["GET"])
def get_file(id):
    if not ObjectId.is_valid(id):
        return jsonify({"success": False, "message": "Invalid file ID"}), 400

    file_record = getFileById(id)
    if not file_record:
        return jsonify({"success": False, "message": f"File {id} not found"}), 404

    file_path = os.path.join("..", file_record["filepath"])
    if not os.path.exists(file_path):
        return jsonify({"success": False, "message": "File missing on server"}), 410

    return send_file(
        file_path,
        mimetype=file_record.get("file_type", "application/octet-stream"),
        as_attachment=True,
        download_name=file_record["filename"],
    )
