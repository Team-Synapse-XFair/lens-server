from flask import Blueprint, jsonify, request
from bson import ObjectId
from datetime import datetime
from app.services.mongo import saveReport
from app.schemas.templates import ReportTemplate
from app.utils.require_auth import require_auth
from app import mongo

reportBP = Blueprint("report", __name__)

@reportBP.route("/report", methods=["POST"])
@require_auth
def create_report():
    data = request.json or {}
    user = request.user  # NOTE Set by require_auth decorator
    
    report = ReportTemplate()

    report["user_id"] = ObjectId(user['user_id'])
    report["title"] = data.get("title", "Untitled Report")
    report ["severity"] = data.get("severity", "low")
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

    return jsonify({"id": inserted_id, "message": "Saved", "success": True}), 201

# --- GET ALL REPORTS ---
@reportBP.route("/report", methods=["GET"])
def get_all_reports():
    reports = list(mongo.db.reports.find())
    for r in reports:
        r["_id"] = str(r["_id"])
        r["user_id"] = str(r["user_id"])
        if isinstance(r.get("location"), ObjectId):
            r["location"] = str(r["location"])
        r["images"] = [str(i) for i in r.get("images", [])]
    return jsonify(reports), 200


# --- GET SINGLE REPORT ---
@reportBP.route("/report/<id>", methods=["GET"])
def get_report(id):
    if not ObjectId.is_valid(id):
        return jsonify({"error": "Invalid report ID"}), 400

    report = mongo.db.reports.find_one({"_id": ObjectId(id)})
    if not report:
        return jsonify({"error": "Report not found"}), 404

    report["_id"] = str(report["_id"])
    report["user_id"] = str(report["user_id"])
    if isinstance(report.get("location"), ObjectId):
        report["location"] = str(report["location"])
    report["images"] = [str(i) for i in report.get("images", [])]

    return jsonify(report), 200