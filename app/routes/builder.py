from flask import Blueprint, request, jsonify
from bson import ObjectId
from datetime import datetime
from app.schemas.templates import BuilderTemplate
from app.services.mongo import createBuilder, getAllBuilders, getBuilderById, updateBuilder
from app.utils.require_auth import require_auth
from app.utils.serialize import serialize_builder
builder_bp = Blueprint("builder_bp", __name__, url_prefix="/builders")

@builder_bp.route("/create", methods=["POST"])
@require_auth
def create_builder():
    data = request.json or {}
    builder = BuilderTemplate()

    builder["name"] = data.get("name", "")
    builder["company"] = data.get("company", "")
    builder["projects"] = [ObjectId(p) for p in data.get("projects", []) if ObjectId.is_valid(p)]
    builder["contact"] = data.get("contact", {})
    builder["created_at"] = datetime.now()
    builder["updated_at"] = datetime.now()
    builder["hq_location"] = data.get("hq_location", {})

    inserted_id = createBuilder(builder)
    builder["_id"] = inserted_id  # add inserted id for serialization
    return jsonify({
            "builder": serialize_builder(builder),
            "success": True
            }), 201


@builder_bp.route("/", methods=["GET"])
def get_builders():
    builders = getAllBuilders()
    return jsonify([serialize_builder(b) for b in builders]), 200


@builder_bp.route("/<id>", methods=["GET"])
def get_builder(id):
    try:
        builder = getBuilderById(ObjectId(id))
        if not builder:
            return jsonify({"error": "Builder not found"}), 404
        return jsonify({
            "builder": serialize_builder(builder),
            "success": True
            }), 200
    except:
        return jsonify({"error": "Invalid ID format"}), 400


@builder_bp.route("/<id>", methods=["PUT"])
def update_builder(id):
    data = request.json or {}
    data["updated_at"] = datetime.now()

    try:
        result = updateBuilder({"_id": ObjectId(id)}, {"$set": data})
        if result.matched_count == 0:
            return jsonify({"error": "Builder not found"}), 404
        return jsonify({"message": "Builder updated successfully"}), 200
    except:
        return jsonify({"error": "Invalid ID format"}), 400