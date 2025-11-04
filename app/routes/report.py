from flask import Blueprint, jsonify, request
from bson import ObjectId
from datetime import datetime
from app.services.mongo import insertReport
from app.schemas.templates import ReportTemplate

reportBP = Blueprint("report", __name__)

@reportBP.route("/", methods=["POST"])
def create_report():
    data = request.json or {}
    
    # 1. Start with the base report template
    report = ReportTemplate()

    # 2. Fill in report details from request data
    if data.get("user_id"):
        report["user_id"] = ObjectId(data["user_id"])
    report["title"] = data.get("title", "Untitled Report")
    report["description"] = data.get("description", "")
    report["category"] = data.get("category", "general")
    report["status"] = data.get("status", "pending")
    report["ai_analysis"] = data.get("ai_analysis", {})
    report["created_at"] = datetime.now()
    report["updated_at"] = datetime.now()

    # 3. Handle location (can be objectId or dict)
    if data.get("location"):
        loc = data["location"]
        if isinstance(loc, str) and ObjectId.is_valid(loc):
            report["location"] = ObjectId(loc)
        else:
            report["location"] = loc  # e.g. a dict of lat/lng

    # 4. Handle images — must be ObjectIds if exist
    if data.get("images"):
        valid_imgs = []
        for img in data["images"]:
            if isinstance(img, str) and ObjectId.is_valid(img):
                valid_imgs.append(ObjectId(img))
        report["images"] = valid_imgs

    # 5. Handle comments similarly
    if data.get("comments"):
        valid_comments = []
        for c in data["comments"]:
            if isinstance(c, str) and ObjectId.is_valid(c):
                valid_comments.append(ObjectId(c))
        report["comments"] = valid_comments

    # 6. Save the report to MongoDB
    inserted_id = insertReport(report)

    # 7. Send a response
    return jsonify({"id": inserted_id, "message": "Report saved"}), 201
