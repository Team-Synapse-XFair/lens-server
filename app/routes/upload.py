from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
from app.utils.require_auth import require_auth
from datetime import datetime
from app.services.mongo import saveFileRecord, getFileById, getFileByHash
from uuid import uuid4
from bson import ObjectId
import os
from app.utils.hash import generateFileHash

uploadBP = Blueprint("upload", __name__, url_prefix="/")

def allowed_file(filename):
    name, extension = os.path.splitext(filename)
    extension = extension.lower()
    return extension in {'.png', '.jpg', '.jpeg'}

@uploadBP.route("/upload-multiple", methods=["POST"])
@require_auth
def upload_multiple():
    files = request.file.getlist('files')
    uploaded_files = []

    for file in files:
        if not file:
            return jsonify({"success": False, "message": "No file provided"}), 400

        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join('uploads', filename)

            if os.path.exists(filepath):
                existingFileHash = generateFileHash(filepath)

                existingFile = getFileByHash(str(existingFileHash))
                if existingFile:
                    existingFileId = str(existingFile['_id'])
                    existingFileUrl = f"http://localhost:5000/api/v1/file/{existingFileId}"
                    return jsonify({"success": True, "message": "File already exists", "file_id": existingFileId, "file_url": existingFileUrl}), 200

                name, ext = os.path.splitext(filename)
                uniqueID = uuid4().hex
                filename = f"{name}_{uniqueID}{ext}"
                filepath = os.path.join('uploads', filename)

            if not os.path.exists('uploads'):
                os.makedirs('uploads')

            file.save(f'{filepath}')

            user_id = request.user['user_id']

            if not ObjectId.is_valid(user_id):
                return jsonify({"success": False, "message": "Invalid user ID"}), 400
            
            fileHash = generateFileHash(filepath)

            file_record = {'filename': filename, 'filepath': filepath, 'uploaded_at': datetime.now(), 'uploaded_by': ObjectId(user_id), 'file_type': file.mimetype, 'metadata': {}, "sha-256-hash": str(fileHash)}

            file_id = saveFileRecord(file_record)

            file_url = f"http://localhost:5000/api/v1/file/{file_id}"

            return jsonify({"success": True, "file_id": file_id, "file_url": file_url}), 201
        
    return jsonify({"success": False, "message": "No valid files to upload"}), 400

@uploadBP.route("/upload", methods=["POST"])
@require_auth
def upload_file():
    file = request.files['file']

    if not file:
        return jsonify({"success": False, "message": "No file provided"}), 400

    if allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join('uploads', filename)

        if os.path.exists(filepath):
            existingFileHash = generateFileHash(filepath)

            existingFile = getFileByHash(str(existingFileHash))
            if existingFile:
                existingFileId = str(existingFile['_id'])
                existingFileUrl = f"http://localhost:5000/api/v1/file/{existingFileId}"
                return jsonify({"success": True, "message": "File already exists", "file_id": existingFileId, "file_url": existingFileUrl}), 200

            name, ext = os.path.splitext(filename)
            uniqueID = uuid4().hex
            filename = f"{name}_{uniqueID}{ext}"
            filepath = os.path.join('uploads', filename)

        if not os.path.exists('uploads'):
            os.makedirs('uploads')

        file.save(f'{filepath}')

        user_id = request.user['user_id']

        if not ObjectId.is_valid(user_id):
            return jsonify({"success": False, "message": "Invalid user ID"}), 400
        
        fileHash = generateFileHash(filepath)

        file_record = {'filename': filename, 'filepath': filepath, 'uploaded_at': datetime.now(), 'uploaded_by': ObjectId(user_id), 'file_type': file.mimetype, 'metadata': {}, "sha-256-hash": str(fileHash)}

        file_id = saveFileRecord(file_record)

        file_url = f"http://localhost:5000/api/v1/file/{file_id}"

        return jsonify({"success": True, "file_id": file_id, "file_url": file_url}), 201

    return jsonify({"success": False, "message": "File upload failed"}), 500

@uploadBP.route("/file/<id>", methods=["GET"])
def get_file(id):
    if not ObjectId.is_valid(id):
        return jsonify({"success": False, "message": "Invalid file ID"}), 400

    file_record = getFileById(id)
    if not file_record:
        return jsonify({"success": False, "message": f"Failed to find file {id}."}), 404
    
    fileType = file_record.get("file_type", "application/octet-stream")
    
    return send_file(
        f"..\\{file_record["filepath"]}",
        mimetype=fileType, as_attachment=True, download_name=file_record["filename"]), 200