from flask import Blueprint, jsonify, request
from app.services.mongo import insertReport

reportBP = Blueprint("report", __name__)

@reportBP.route("/", methods=["POST"])
def create_report():
    ## TODO Implement report generation/saving and response logic

    id = insertReport(request.json)

    return jsonify({"id": id, "message": "Report saved"}), 201