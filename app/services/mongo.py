# import os
# from datetime import datetime
# from pymongo import MongoClient

# MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
# client = MongoClient(MONGO_URI)

# MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "lens_dev")
# db = client[MONGO_DB_NAME]

# reports = db['reports']

# def insertReport(data):
#     ## TODO Implement proper shcema logic and user validation

#     ## NOTE Ignore this table structure, check app/schemas/templates.py for intended structure
#     report = {
#         'user_id': data.get('user_id', 'anonymous'),
#         'title': data.get('title', 'Untitled Report'),
#         'description': data.get('description', ''),
#         'category': data.get('category', 'general'),
#         'location': data.get('location', {}),
#         'images': data.get('images', []),
#         'status': data.get('status', 'pending'),
#         'ai_analysis': data.get('ai_analysis', {}),
#         'created_at': data.get('created_at', datetime.now()),
#         'updated_at': data.get('updated_at', datetime.now()),
#         'comments': data.get('comments', []),
#     }
#     result = reports.insert_one(report)
#     return str(result.inserted_id)
from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)

MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "lens_dev")
db = client[MONGO_DB_NAME]

reports = db["reports"]

def insertReport(report):
    result = reports.insert_one(report)
    return str(result.inserted_id)
