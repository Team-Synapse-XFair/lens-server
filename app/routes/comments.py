from flask import Blueprint, request, jsonify
from bson import ObjectId
from datetime import datetime
from app.schemas.templates import CommentTemplate
from app.services.mongo import saveComment, getAllComments
from app.utils.require_auth import require_auth
from app.utils.serialize import serialize_comment
comment_bp = Blueprint("comment_bp", __name__, url_prefix="/comments")

@comment_bp.route("/", methods=["POST"])
@require_auth
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

    result = saveComment(comment)
    return jsonify(serialize_comment(comment)), 201


@comment_bp.route("/", methods=["GET"])
@require_auth
def get_comments():
    comments = getAllComments()
    return jsonify([serialize_comment(c) for c in comments]), 200


@comment_bp.route("/<parent_type>/<parent_id>", methods=["GET"])
@require_auth
def get_comments_for_parent(parent_type, parent_id):
    try:
        comments = getCommentsByParent(parent_type, ObjectId(parent_id))
        return jsonify([serialize_comment(c) for c in comments]), 200
    except:
        return jsonify({"error": "Invalid parent_id"}), 400
