from flask import Blueprint, jsonify, request
from bson import ObjectId
from datetime import datetime
from app.services.mongo import saveProject, getAllProjects, updateProject, getProjectById
from app.schemas.templates import ProjectTemplate
from app.utils.require_auth import require_admin, require_auth
from app.utils.serialize import serialize_project

projectBP = Blueprint("project", __name__)

@projectBP.route("/project", methods=["POST"])
@require_admin
def create_project():
    data = request.json or {}
    project = ProjectTemplate()

    project["name"] = data.get("name", "")
    project["department"] = data.get("department", "")
    project["budget"] = data.get("budget", 0.0)
    project["status"] = data.get("status", "planning")
    project["progress"] = data.get("progress", 0)
    project["ai_summary"] = data.get("ai_summary", {})
    project["start_date"] = data.get("start_date", datetime.now())
    project["end_date"] = data.get("end_date", datetime.now())
    project["last_updated"] = datetime.now()

    # Handle location
    loc = data.get("location")
    if isinstance(loc, str) and ObjectId.is_valid(loc):
        project["location"] = ObjectId(loc)

    # Handle reports list
    if data.get("reports"):
        valid_reports = [ObjectId(r) for r in data["reports"] if ObjectId.is_valid(r)]
        project["reports"] = valid_reports

    inserted_id = saveProject(project)
    project["_id"] = inserted_id  # add inserted id for serialization
    return jsonify(serialize_project(project)), 201


@projectBP.route("/project", methods=["GET"])
def get_all_projects():
    projects = getAllProjects()
    return jsonify([serialize_project(p) for p in projects]), 200


@projectBP.route("/project/<project_id>", methods=["GET"])
def get_project(project_id):
    if not ObjectId.is_valid(project_id):
        return jsonify({"error": "Invalid project ID"}), 400

    project = getProjectById(ObjectId(project_id))
    if not project:
        return jsonify({"error": "Project not found"}), 404

    return jsonify(serialize_project(project)), 200


@projectBP.route("/project/<project_id>", methods=["PUT"])
@require_auth
def update_project(project_id):
    if not ObjectId.is_valid(project_id):
        return jsonify({"error": "Invalid project ID"}), 400

    data = request.json or {}
    data["last_updated"] = datetime.now()

    update_count = updateProject(ObjectId(project_id), data)
    if not update_count:
        return jsonify({"error": "Project not found"}), 404

    updated = getProjectById(ObjectId(project_id))
    return jsonify(serialize_project(updated)), 200
