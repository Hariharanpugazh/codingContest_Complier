from pymongo import MongoClient
from django.conf import settings


class ContestDetails:
    collection_name = "Contest_Details"

    @staticmethod
    def get_collection():
        """
        Get the MongoDB collection.
        """
        client = MongoClient(settings.MONGO_DB_CONFIG['HOST'])
        db = client[settings.MONGO_DB_CONFIG['NAME']]
        return db[ContestDetails.collection_name]

    @staticmethod
    def create_contest(data):
        """
        Create a new contest document.
        """
        collection = ContestDetails.get_collection()
        return collection.insert_one(data).inserted_id

    @staticmethod
    def get_contest_by_id(contest_id):
        """
        Fetch a contest document by its unique contest_id.
        """
        collection = ContestDetails.get_collection()
        return collection.find_one({"contest_id": contest_id})

    @staticmethod
    def update_contest(contest_id, updated_data):
        """
        Update a contest document.
        """
        collection = ContestDetails.get_collection()
        result = collection.update_one({"contest_id": contest_id}, {"$set": updated_data})
        return result.modified_count

    @staticmethod
    def delete_contest(contest_id):
        """
        Delete a contest document by its unique contest_id.
        """
        collection = ContestDetails.get_collection()
        result = collection.delete_one({"contest_id": contest_id})
        return result.deleted_count

    @staticmethod
    def get_all_contests():
        """
        Fetch all contest documents.
        """
        collection = ContestDetails.get_collection()
        return list(collection.find())
