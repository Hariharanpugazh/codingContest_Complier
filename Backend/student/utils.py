# utils/mongo.py
import os
import pymongo
from dotenv import load_dotenv
from pymongo.errors import ConfigurationError, ServerSelectionTimeoutError
import jwt
from pymongo import MongoClient
from datetime import datetime, timedelta

load_dotenv()

class MongoDBConnection:
    _instance = None

    @classmethod
    def get_connection(cls):
        if cls._instance is None:
            try:
                client = pymongo.MongoClient(os.getenv("MONGODB_URI"), serverSelectionTimeoutMS=5000)
                client.admin.command("ping")  # Check connection
                cls._instance = client["test_portal_db"]
            except (ConfigurationError, ServerSelectionTimeoutError) as e:
                raise Exception(f"Database connection error: {e}")
        return cls._instance

    @classmethod
    def get_collection(cls, collection_name):
        return cls.get_connection()[collection_name]

# Collections
# staff_collection = MongoDBConnection.get_collection("staff")
student_collection = MongoDBConnection.get_collection("students")
contest_details_collection = MongoDBConnection.get_collection("Contest_Details")
final_questions_collection = MongoDBConnection.get_collection("finalQuestions")
