from flask import Blueprint, request, jsonify
from bson import ObjectId
from datetime import datetime
from app.services.mongo import getReports, getReportImages
from app.utils.require_auth import require_auth

reportsBP = Blueprint("reports", __name__)


@reportsBP.route("/getreports", methods=["GET"])
@require_auth 
def get_reports():
    reports = getReports()

    return (
        jsonify({"reports": reports, "message": "Reports fetched", "success": True}),
        200,
    )


@reportsBP.route("/getreportimages/<id>", methods=["GET"])
@require_auth 
def get_report_images(id):
    if not ObjectId.is_valid(id):
        return (
            jsonify({"images": [], "message": "Invalid report ID", "success": False}),
            400,
        )

    images = getReportImages(ObjectId(id))

    if not images:
        return (
            jsonify({"images": [], "message": "Report not found", "success": False}),
            404,
        )

    return (
        jsonify({"images": images, "message": "Images fetched", "success": True}),
        200,
    )
