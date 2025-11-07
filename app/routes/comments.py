from flask import Blueprint, request, jsonify
from bson import ObjectId
from datetime import datetime
from app import mongo
from app.schemas.templates import CommentTemplate

comment_bp = Blueprint("comment_bp", __name__, url_prefix="/comments")


def serialize_comment(comment):
    comment["_id"] = str(comment["_id"])
    comment["parent_id"] = str(comment["parent_id"])
    comment["user_id"] = str(comment["user_id"])
    return comment


# --- create comment ---
@comment_bp.route("/", methods=["POST"])
def create_comment():
    data = request.json or {}

    required = ["parent_type", "parent_id", "user_id", "content"]
    if not all(f in data for f in required):
        return jsonify({"error": "Missing required fields"}), 400

    comment = CommentTemplate()
    for key, val in data.items():
        if key in comment:
            if key.endswith("_id"):
                comment[key] = ObjectId(val)
            else:
                comment[key] = val

    comment["created_at"] = datetime.now()
    comment["updated_at"] = datetime.now()

    mongo.db.comments.insert_one(comment)
    return jsonify(serialize_comment(comment)), 201


# --- get all comments ---
@comment_bp.route("/", methods=["GET"])
def get_comments():
    comments = list(mongo.db.comments.find())
    return jsonify([serialize_comment(c) for c in comments]), 200


# --- get comments for a specific parent (optional) ---
@comment_bp.route("/<parent_type>/<parent_id>", methods=["GET"])
def get_comments_for_parent(parent_type, parent_id):
    try:
        comments = list(
            mongo.db.comments.find(
                {"parent_type": parent_type, "parent_id": ObjectId(parent_id)}
            )
        )
        return jsonify([serialize_comment(c) for c in comments]), 200
    except:
        return jsonify({"error": "Invalid parent_id"}), 400
