from flask import Blueprint, request, jsonify
from bson import ObjectId
from datetime import datetime
from app import mongo
from app.schemas.templates import BuilderTemplate
builder_bp = Blueprint("builder_bp", __name__, url_prefix="/builders")

# --- helpers ---
def serialize_builder(builder):
    builder["_id"] = str(builder["_id"])
    builder["projects"] = [str(p) for p in builder.get("projects", [])]
    builder["comments"] = [str(c) for c in builder.get("comments", [])]
    return builder


# --- create ---
@builder_bp.route("/", methods=["POST"])
def create_builder():
    data = request.json or {}
    builder = BuilderTemplate()

    # Merge provided data into template
    for key, value in data.items():
        if key in builder:
            builder[key] = value
        elif key in builder["contact"]:
            builder["contact"][key] = value

    builder["created_at"] = datetime.now()
    builder["updated_at"] = datetime.now()

    mongo.db.builders.insert_one(builder)
    return jsonify(serialize_builder(builder)), 201


# --- read all ---
@builder_bp.route("/", methods=["GET"])
def get_builders():
    builders = list(mongo.db.builders.find())
    return jsonify([serialize_builder(b) for b in builders]), 200


# --- read single ---
@builder_bp.route("/<id>", methods=["GET"])
def get_builder(id):
    try:
        builder = mongo.db.builders.find_one({"_id": ObjectId(id)})
        if not builder:
            return jsonify({"error": "Builder not found"}), 404
        return jsonify(serialize_builder(builder)), 200
    except:
        return jsonify({"error": "Invalid ID format"}), 400


# --- update ---
@builder_bp.route("/<id>", methods=["PUT"])
def update_builder(id):
    data = request.json or {}
    data["updated_at"] = datetime.now()

    try:
        result = mongo.db.builders.update_one({"_id": ObjectId(id)}, {"$set": data})
        if result.matched_count == 0:
            return jsonify({"error": "Builder not found"}), 404
        return jsonify({"message": "Builder updated successfully"}), 200
    except:
        return jsonify({"error": "Invalid ID format"}), 400


# --- delete ---
@builder_bp.route("/<id>", methods=["DELETE"])
def delete_builder(id):
    try:
        result = mongo.db.builders.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            return jsonify({"error": "Builder not found"}), 404
        return jsonify({"message": "Builder deleted successfully"}), 200
    except:
        return jsonify({"error": "Invalid ID format"}), 400
