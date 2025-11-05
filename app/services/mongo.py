from pymongo import MongoClient
import os
from datetime import datetime

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)

MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "lens_dev")

def getDB(db_name=MONGO_DB_NAME):
    return client[db_name]

def checkConnection():
    try:
        # The ismaster command is cheap and does not require auth.
        client.admin.command('ismaster')
        return True
    except Exception as e:
        print(f"MongoDB connection error: {e}")
        return False
    
def getUser(email):
    if not checkConnection():
        raise ConnectionError("Unable to connect to MongoDB")

    users = getDB()['users']
    user = users.find_one({'email': email})
    return user

def saveReport(report):
    if not checkConnection():
        raise ConnectionError("Unable to connect to MongoDB")

    reports = getDB()['reports']
    
    result = reports.insert_one(report)
    return str(result.inserted_id)

def saveUser(user):
    if not checkConnection():
        raise ConnectionError("Unable to connect to MongoDB")

    users = getDB()['users']
    
    result = users.insert_one(user)
    return str(result.inserted_id)