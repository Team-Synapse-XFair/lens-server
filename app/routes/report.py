from flask import Blueprint, jsonify, request
from bson import ObjectId
from datetime import datetime
from app.services.mongo import saveReport
from app.schemas.templates import ReportTemplate
from app.utils.require_auth import require_auth

reportBP = Blueprint("report", __name__)

@reportBP.route("/report", methods=["POST"])
@require_auth
def create_report():
    data = request.json or {}
    user = request.user  # NOTE Set by require_auth decorator
    
    report = ReportTemplate()

    report["user_id"] = ObjectId(user['user_id'])
    report["title"] = data.get("title", "Untitled Report")
    report["description"] = data.get("description", "")
    report["category"] = data.get("category", "general")
    report["status"] = data.get("status", "pending")
    report["ai_analysis"] = data.get("ai_analysis", {})
    report["created_at"] = datetime.now()
    report["updated_at"] = datetime.now()

    # TODO Handle locations from frontend properly
    if data.get("location"):
        loc = data["location"]
        if isinstance(loc, str) and ObjectId.is_valid(loc):
            report["location"] = ObjectId(loc)
        else:
            report["location"] = loc  # e.g. a dict of lat/lng

    # TODO Handle images from frontend properly
    if data.get("images"):
        valid_imgs = []
        for img in data["images"]:
            if isinstance(img, str) and ObjectId.is_valid(img):
                valid_imgs.append(ObjectId(img))
        report["images"] = valid_imgs

    # TODO Implement project association

    inserted_id = saveReport(report)

    return jsonify({"id": inserted_id, "message": "Saved"}), 201
