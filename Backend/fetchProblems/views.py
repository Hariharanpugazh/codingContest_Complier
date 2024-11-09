from django.http import JsonResponse
from pymongo import MongoClient
from bson import ObjectId

# Establish a single MongoDB client and database instance
client = MongoClient('mongodb://localhost:27017/')
db = client['Coding_Platform']

def fetch_AutoSelect_problems(request):
    # Access the AutoSelect collection
    collection = db['AutoSelect']

    # Fetch only the 'problems' field from each document in AutoSelect
    documents = collection.find({}, {'problems': 1, '_id': 0})  # Retrieve only the 'problems' field and exclude '_id'

    # Flatten the problems into a single list to return as JSON
    problems = [problem for document in documents for problem in document.get('problems', [])]

    return JsonResponse({'problems': problems})

def fetch_Questions(request):
    # Access the AutoSelect collection
    collection = db['Questions_Library']

    # Fetch only the 'problems' field from each document in AutoSelect
    documents = collection.find({}, {'problems': 1, '_id': 0})  # Retrieve only the 'problems' field and exclude '_id'

    # Flatten the problems into a single list to return as JSON
    problems = [problem for document in documents for problem in document.get('problems', [])]

    return JsonResponse({'problems': problems})


def fetch_FileUpload_problems(request):
    # Access the FileUpload collection
    collection = db['FileUpload']

    # Fetch all documents from FileUpload collection and convert ObjectId to string
    problems = []
    for document in collection.find({}):
        document['_id'] = str(document['_id'])  # Convert ObjectId to string
        problems.append(document)

    return JsonResponse({'problems': problems}, safe=False)


def fetch_ManualUpload_problems(request):
    # Access the ManualUpload_onebyone collection
    collection = db['ManualUpload_onebyone']

    # Fetch all documents with all fields and convert ObjectId to string
    problems = []
    for document in collection.find({}):
        document['_id'] = str(document['_id'])  # Convert ObjectId to string for JSON serialization
        problems.append(document)

    return JsonResponse({'problems': problems}, safe=False)
