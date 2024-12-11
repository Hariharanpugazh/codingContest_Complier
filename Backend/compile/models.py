from pymongo import MongoClient
from django.conf import settings


class FileUploadProblems:
    collection_name = "FileUpload"

    @staticmethod
    def get_collection():
        client = MongoClient(settings.MONGO_DB_CONFIG['HOST'])
        db = client[settings.MONGO_DB_CONFIG['NAME']]
        return db[FileUploadProblems.collection_name]

    @staticmethod
    def create_problem(data):
        """
        Create a new problem document.
        """
        collection = FileUploadProblems.get_collection()
        return collection.insert_one(data).inserted_id

    @staticmethod
    def get_problem_by_id(problem_id):
        """
        Fetch a problem document by its ID.
        """
        from bson.objectid import ObjectId
        collection = FileUploadProblems.get_collection()
        return collection.find_one({"_id": ObjectId(problem_id)})

    @staticmethod
    def update_problem(problem_id, updated_data):
        """
        Update a problem document.
        """
        from bson.objectid import ObjectId
        collection = FileUploadProblems.get_collection()
        result = collection.update_one({"_id": ObjectId(problem_id)}, {"$set": updated_data})
        return result.modified_count

    @staticmethod
    def delete_problem(problem_id):
        """
        Delete a problem document by its ID.
        """
        from bson.objectid import ObjectId
        collection = FileUploadProblems.get_collection()
        result = collection.delete_one({"_id": ObjectId(problem_id)})
        return result.deleted_count
    

