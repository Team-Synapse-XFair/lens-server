from bson import ObjectId

def serialize_objectid(value):
    if isinstance(value, ObjectId):
        return str(value)
    elif isinstance(value, list):
        return [serialize_objectid(v) for v in value]
    elif isinstance(value, dict):
        return {k: serialize_objectid(v) for k, v in value.items()}
    return value


def serialize(data: dict):
    serialized = {}
    for k, v in data.items():
        if isinstance(v, ObjectId):
            serialized[k] = str(v)
        elif isinstance(v, list):
            serialized[k] = [serialize_objectid(i) for i in v]
        elif isinstance(v, dict):
            serialized[k] = serialize_objectid(v)
        elif hasattr(v, "isoformat"):
            serialized[k] = v.isoformat()
        else:
            serialized[k] = v
    return serialized

def serialize_file(file_data):
    return serialize(file_data)


def serialize_image(image_data):
    return serialize(image_data)


def serialize_comment(comment_data):
    return serialize(comment_data)


def serialize_location(location_data):
    return serialize(location_data)


def serialize_user(user_data):
    user = serialize(user_data)
    # Optional: don’t expose hashed password
    user.pop("hashed_password", None)
    return user


def serialize_project(project_data):
    return serialize(project_data)


def serialize_report(report_data):
    return serialize(report_data)


def serialize_builder(builder_data):
    return serialize(builder_data)
