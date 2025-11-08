from flask import Blueprint, jsonify, request
from bson import ObjectId
from datetime import datetime
from app.services.mongo import saveReport, getReports, getReport
from app.schemas.templates import ReportTemplate
from app.utils.require_auth import require_auth
from app.utils.serialize import serialize_report

reportBP = Blueprint("report", __name__)

@reportBP.route("/report", methods=["POST"])
@require_auth
def create_report():
    data = request.json or {}
    user = request.user  # Set by require_auth decorator

    report = ReportTemplate()
    report["user_id"] = ObjectId(user["user_id"])
    report["title"] = data.get("title", "Untitled Report")
    report["severity"] = data.get("severity", "low")
    report["description"] = data.get("description", "")
    report["category"] = data.get("category", "general")
    report["status"] = data.get("status", "pending")
    report["ai_analysis"] = data.get("ai_analysis", {})
    report["created_at"] = datetime.now()
    report["updated_at"] = datetime.now()

    if data.get("location"):
        loc = data["location"]
        if isinstance(loc, str) and ObjectId.is_valid(loc):
            report["location"] = ObjectId(loc)
        else:
            report["location"] = loc  # dict with lat/lng/address

    if data.get("images"):
        valid_imgs = [ObjectId(i) for i in data["images"] if ObjectId.is_valid(i)]
        report["images"] = valid_imgs

    # optional project association
    if data.get("project_id") and ObjectId.is_valid(data["project_id"]):
        report["project_id"] = ObjectId(data["project_id"])

    inserted_id = saveReport(report)
    report["_id"] = inserted_id
    return jsonify(serialize_report(report)), 201


@reportBP.route("/report", methods=["GET"])
@require_auth
def get_all_reports():
    reports = getReports()
    return jsonify([serialize_report(r) for r in reports]), 200

@reportBP.route("/report/<id>", methods=["GET"])
@require_auth
def get_report(id):
    if not ObjectId.is_valid(id):
        return jsonify({"error": "Invalid report ID"}), 400

    report = getReport(ObjectId(id))
    if not report:
        return jsonify({"error": "Report not found"}), 404

    return jsonify(serialize_report(report)), 200
