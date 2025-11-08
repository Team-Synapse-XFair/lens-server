from pymongo import MongoClient
import os
from datetime import datetime
from bson import ObjectId

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)

MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "lens_dev")


def getDB(db_name=MONGO_DB_NAME):
    return client[db_name]


def checkConnection():
    try:
        # cheap and does not require auth
        client.admin.command("ismaster")
        return True
    except Exception as e:
        print(f"MongoDB connection error: {e}")
        return False


def getUser(email):
    if not checkConnection():
        raise ConnectionError("Unable to connect to MongoDB")

    users = getDB()["users"]
    user = users.find_one({"email": email})
    return user


def saveReport(report):
    if not checkConnection():
        raise ConnectionError("Unable to connect to MongoDB")

    reports = getDB()["reports"]

    result = reports.insert_one(report)
    return str(result.inserted_id)


def saveUser(user):
    if not checkConnection():
        raise ConnectionError("Unable to connect to MongoDB")

    users = getDB()["users"]

    result = users.insert_one(user)
    return str(result.inserted_id)


def saveFileRecord(file_doc):
    if not checkConnection():
        raise ConnectionError("Unable to connect to MongoDB")

    files = getDB()["files"]

    result = files.insert_one(file_doc)
    return str(result.inserted_id)


def saveImage(image_doc):
    if not checkConnection():
        raise ConnectionError("Unable to connect to MongoDB")

    images = getDB()["images"]

    result = images.insert_one(image_doc)
    return str(result.inserted_id)


def getFileById(file_id):
    if not checkConnection():
        raise ConnectionError("Unable to connect to MongoDB")

    files = getDB()["files"]
    file_doc = files.find_one({"_id": ObjectId(file_id)})
    return file_doc


def getFileByHash(file_hash):
    if not checkConnection():
        raise ConnectionError("Unable to connect to MongoDB")

    files = getDB()["files"]
    file_doc = files.find_one({"sha-256-hash": file_hash})
    return file_doc


def saveImages(images):
    if not checkConnection():
        raise ConnectionError("Unable to connect to MongoDB")

    images = getDB()["images"]

    result = images.insert_many(images)
    ids = []
    for id in result.inserted_ids:
        ids.append(str(id))

    return ids


def getReports():
    if not checkConnection():
        raise ConnectionError("Unable to connect to MongoDB")

    reports = getDB()["reports"]
    report_list = list(reports.find())
    for report in report_list:
        report["id"] = str(report["_id"])
        report.pop("_id", None)
        report["location"] = str(report["location"]) if "location" in report else None
        report["images"] = [str(img_id) for img_id in report.get("images", [])]
        report["user_id"] = str(report["user_id"]) if "user_id" in report else None
        report["created_at"] = (
            report["created_at"].isoformat() if "created_at" in report else None
        )
        report["updated_at"] = (
            report["updated_at"].isoformat() if "updated_at" in report else None
        )
        report["project_id"] = (
            str(report["project_id"]) if "project_id" in report else None
        )
        report["severity"] = report["severity"] if "severity" in report else None
        report["uploaded_by"] = (
            str(report["uploaded_by"]) if "uploaded_by" in report else None
        )

    return report_list


def getReportImages(report_id):
    if not checkConnection():
        raise ConnectionError("Unable to connect to MongoDB")

    reports = getDB()["reports"]
    report = reports.find_one({"_id": ObjectId(report_id)})
    if not report or "images" not in report:
        return []

    images = getDB()["files"]
    image_list = []
    for img_id in report["images"]:
        img_doc = images.find_one({"_id": img_id})
        if img_doc:
            img_doc["id"] = str(img_doc["_id"])
            img_doc["uploaded_by"] = (
                str(img_doc["uploaded_by"]) if "uploaded_by" in img_doc else None
            )
            ## make url
            img_doc["file_url"] = f"http://localhost:5000/api/v1/file/{img_doc['id']}"
            img_doc.pop("_id", None)
            image_list.append(img_doc)

    return image_list

def getReport(report_id):
    if not checkConnection():
        raise ConnectionError("Unable to connect to MongoDB")

    reports = getDB()["reports"]
    report = reports.find_one({"_id": ObjectId(report_id)})
    return report


def getBuilderById(builder_id):
    if not checkConnection():
        raise ConnectionError("Unable to connect to MongoDB")

    builders = getDB()["builders"]
    builder = builders.find_one({"_id": ObjectId(builder_id)})
    return builder

def updateBuilder(builder_id, update_data):
    if not checkConnection():
        raise ConnectionError("Unable to connect to MongoDB")

    builders = getDB()["builders"]
    result = builders.update_one(
        {"_id": ObjectId(builder_id)}, {"$set": update_data}
    )
    return result.modified_count > 0

def createBuilder(builder_data):
    if not checkConnection():
        raise ConnectionError("Unable to connect to MongoDB")

    builders = getDB()["builders"]
    result = builders.insert_one(builder_data)
    return str(result.inserted_id)

def getAllBuilders():
    if not checkConnection():
        raise ConnectionError("Unable to connect to MongoDB")

    builders = getDB()["builders"]
    builder_list = list(builders.find())
    for builder in builder_list:
        builder["id"] = str(builder["_id"])
        builder.pop("_id", None)
        builder["projects"] = [str(proj_id) for proj_id in builder.get("projects", [])]
        builder["comments"] = [str(comm_id) for comm_id in builder.get("comments", [])]
        builder["created_at"] = (
            builder["created_at"].isoformat() if "created_at" in builder else None
        )
        builder["updated_at"] = (
            builder["updated_at"].isoformat() if "updated_at" in builder else None
        )

    return builder_list

def saveProject(project):
    if not checkConnection():
        raise ConnectionError("Unable to connect to MongoDB")

    projects = getDB()["projects"]

    result = projects.insert_one(project)
    return str(result.inserted_id)

def getProjectById(project_id):
    if not checkConnection():
        raise ConnectionError("Unable to connect to MongoDB")

    projects = getDB()["projects"]
    project = projects.find_one({"_id": ObjectId(project_id)})
    return project

def updateProject(project_id, update_data):
    if not checkConnection():
        raise ConnectionError("Unable to connect to MongoDB")

    projects = getDB()["projects"]
    result = projects.update_one(
        {"_id": ObjectId(project_id)}, {"$set": update_data}
    )
    return result.modified_count > 0

def getAllProjects():
    if not checkConnection():
        raise ConnectionError("Unable to connect to MongoDB")

    projects = getDB()["projects"]
    project_list = list(projects.find())
    for project in project_list:
        project["id"] = str(project["_id"])
        project.pop("_id", None)
        project["location"] = str(project["location"]) if "location" in project else None
        project["reports"] = [str(rep_id) for rep_id in project.get("reports", [])]
        project["start_date"] = (
            project["start_date"].isoformat() if "start_date" in project else None
        )
        project["end_date"] = (
            project["end_date"].isoformat() if "end_date" in project else None
        )
        project["last_updated"] = (
            project["last_updated"].isoformat() if "last_updated" in project else None
        )

    return project_list

def saveComment(comment):
    if not checkConnection():
        raise ConnectionError("Unable to connect to MongoDB")

    comments = getDB()["comments"]

    result = comments.insert_one(comment)
    return str(result.inserted_id)

def getCommentById(comment_id):
    if not checkConnection():
        raise ConnectionError("Unable to connect to MongoDB")

    comments = getDB()["comments"]
    comment = comments.find_one({"_id": ObjectId(comment_id)})
    return comment

def updateComment(comment_id, update_data):
    if not checkConnection():
        raise ConnectionError("Unable to connect to MongoDB")

    comments = getDB()["comments"]
    result = comments.update_one(
        {"_id": ObjectId(comment_id)}, {"$set": update_data}
    )
    return result.modified_count > 0

def getAllComments():
    if not checkConnection():
        raise ConnectionError("Unable to connect to MongoDB")

    comments = getDB()["comments"]
    comment_list = list(comments.find())
    for comment in comment_list:
        comment["id"] = str(comment["_id"])
        comment.pop("_id", None)
        comment["parent_id"] = (
            str(comment["parent_id"]) if "parent_id" in comment else None
        )
        comment["user_id"] = (
            str(comment["user_id"]) if "user_id" in comment else None
        )
        comment["created_at"] = (
            comment["created_at"].isoformat() if "created_at" in comment else None
        )
        comment["updated_at"] = (
            comment["updated_at"].isoformat() if "updated_at" in comment else None
        )

    return comment_list

def getCommentsByParent(parent_type, parent_id):
    if not checkConnection():
        raise ConnectionError("Unable to connect to MongoDB")

    comments = getDB()["comments"]
    comment_list = list(
        comments.find({"parent_type": parent_type, "parent_id": ObjectId(parent_id)})
    )
    for comment in comment_list:
        comment["id"] = str(comment["_id"])
        comment.pop("_id", None)
        comment["parent_id"] = (
            str(comment["parent_id"]) if "parent_id" in comment else None
        )
        comment["user_id"] = (
            str(comment["user_id"]) if "user_id" in comment else None
        )
        comment["created_at"] = (
            comment["created_at"].isoformat() if "created_at" in comment else None
        )
        comment["updated_at"] = (
            comment["updated_at"].isoformat() if "updated_at" in comment else None
        )

    return comment_list

def getAllBuilders():
    if not checkConnection():
        raise ConnectionError("Unable to connect to MongoDB")

    comments = getDB()["comments"]
    comment_list = list(comments.find())
    for comment in comment_list:
        comment["id"] = str(comment["_id"])
        comment.pop("_id", None)
        comment["report_id"] = (
            str(comment["report_id"]) if "report_id" in comment else None
        )
        comment["user_id"] = (
            str(comment["user_id"]) if "user_id" in comment else None
        )
        comment["created_at"] = (
            comment["created_at"].isoformat() if "created_at" in comment else None
        )
        comment["updated_at"] = (
            comment["updated_at"].isoformat() if "updated_at" in comment else None
        )

    return comment_list