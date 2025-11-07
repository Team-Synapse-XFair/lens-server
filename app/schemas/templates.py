from datetime import datetime
from bson import ObjectId

def FileTemplate() :
    return {
        'filename': '',
        'filepath': '',
        'uploaded_at': datetime.now(),
        'uploaded_by': ObjectId(), ## User who uploaded
        'file_type': '', ## ex: 'image/png', 'application/pdf', etc.
        'metadata': {}, ## any additional metadata
    }

def ImageTemplate() :
    return {
        'file_id': ObjectId(), ## Reference to File document
        'report_id': ObjectId(), ## Report this image is associated with
        'uploaded_at': datetime.now(),
        'description': '',
    }

def CommentTemplate() :
    return {
        'report_id': ObjectId(), ## Report this comment is associated with
        'user_id': ObjectId(), ## User who made the comment
        'content': '',
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
    }

def LocationTemplate() :
    return {
        'latitude': 0.0,
        'longitude': 0.0,
        'address': '',
        'city': '',
        'state': '',
        'postal_code': '',
    }

def UserTemplate() :
    return {
        'username': '',
        'email': '',
        'hashed_password': '',
        'full_name': '',
        'role': '', ## ex: 'admin', 'citizen', 'official'
        'joined_at': datetime.now(),
        'reports_submitted': [], ## list of report ObjectIds
        'profile': {}, ## additional profile info (city, organiztion, verified, etc.) organization only used when role is 'official'
    }

def ProjectTemplate() :
    return {
        'name': '',
        'department': '', ## Under which city department this project falls
        'budget': 0.0,
        'status': '', ## ex: 'planning', 'in_progress', 'completed'
        'progress': 0, ## percentage 0-100
        'ai_summary': {}, ## ai-generated project summary/insights (risk level, accountability, etc.)
        'start_date': datetime.now(),
        'end_date': datetime.now(),
        'location': ObjectId(), ## Location ObjectId
        'reports': [], ## list of associated Report ObjectIds
        'last_updated': datetime.now(),
    }

def ReportTemplate() :
    return {
        'user_id': ObjectId(), ## User who reported
        'title': '',
        'description': '',
        'severity': '', ## ex: 'low', 'medium', 'high'
        'project_id': ObjectId(), ## Associated project (if any)
        'category': '', ## ex: 'road_damage', 'streetlight_outage', 'water_leak' etc.
        'location': ObjectId(), ## latitude/longitude/local address
        'images': [], ## list of image ObjectIds (each image stored separately in 'images' collection)
        'status': '', ## ex: 'pending', 'verified', 'resolved', 'rejected'
        'ai_analysis': {}, ## ai-generated insights (e.g. detected damage, severity, confidence, etc.)
        'created_at': datetime.now(), ## self explanatory
        'updated_at': datetime.now(), ## self explanatory
        'comments': [], ## list of comment ObjectIds (each comment stored in 'comments' collection)
    }

def BuilderTemplate():
    return {
        "_id": ObjectId(),  # unique builder id
        "name": "",
        "estd": datetime.now(),  # or year if you prefer
        "hq_location": "",  # main office / HQ
        "contact": {
            "email": "",
            "phone": "",
            "website": ""
        },
        "projects": [],  # list of associated Project ObjectIds
        "accountability_score": 0,  # numeric 0–100 or similar
        "comments": [],  # list of Comment ObjectIds
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }

def CommentTemplate():
    """Generic comment structure usable across builders, reports, etc."""
    return {
        "_id": ObjectId(),
        "parent_type": "",        # can be "builder", "report", "project"
        "parent_id": ObjectId(),  # links to the entity being commented on
        "user_id": ObjectId(),    # user who made the comment
        "content": "",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }