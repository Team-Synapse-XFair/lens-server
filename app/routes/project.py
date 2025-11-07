from flask import Blueprint, jsonify, request
from bson import ObjectId
from datetime import datetime
from app.services.mongo import saveProject, getProjects, updateProject, deleteProject, getProjectById
from app.schemas.templates import ProjectTemplate
from app.utils.require_auth import require_auth

projectBP = Blueprint("project", __name__)

# CREATE
@projectBP.route("/project", methods=["POST"])
@require_auth
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
    return jsonify({"id": str(inserted_id), "message": "Project created", "success": True}), 201


# READ ALL
@projectBP.route("/project", methods=["GET"])
def get_all_projects():
    projects = getProjects()
    for p in projects:
        p["_id"] = str(p["_id"])
        if isinstance(p.get("location"), ObjectId):
            p["location"] = str(p["location"])
        p["reports"] = [str(r) for r in p.get("reports", [])]
    return jsonify({"projects": projects, "success": True}), 200


# READ ONE
@projectBP.route("/project/<project_id>", methods=["GET"])
def get_project(project_id):
    if not ObjectId.is_valid(project_id):
        return jsonify({"error": "Invalid project ID"}), 400
    project = getProjectById(ObjectId(project_id))
    if not project:
        return jsonify({"error": "Project not found"}), 404
    project["_id"] = str(project["_id"])
    project["reports"] = [str(r) for r in project.get("reports", [])]
    if isinstance(project.get("location"), ObjectId):
        project["location"] = str(project["location"])
    return jsonify({"project": project, "success": True}), 200


# UPDATE
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
    return jsonify({"message": "Project updated", "success": True}), 200


# DELETE
@projectBP.route("/project/<project_id>", methods=["DELETE"])
@require_auth
def delete_project(project_id):
    if not ObjectId.is_valid(project_id):
        return jsonify({"error": "Invalid project ID"}), 400
    delete_count = deleteProject(ObjectId(project_id))
    if not delete_count:
        return jsonify({"error": "Project not found"}), 404
    return jsonify({"message": "Project deleted", "success": True}), 200
