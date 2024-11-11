from django.http import JsonResponse
from pymongo import MongoClient
from bson import ObjectId
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

# Establish a single MongoDB client and database instance
client = MongoClient('mongodb://localhost:27017/')
db = client['Coding_Platform']
questions_collection = db['Questions_Library'] 

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

@csrf_exempt  # This disables CSRF protection for this view
@require_http_methods(["POST"])
def get_question_by_id(request):
    """
    Retrieves a specific problem from the problems array based on the question ID.
    """
    try:
        # Parse JSON data from the POST request
        data = json.loads(request.body)
        question_id = data.get("id")  # Assume the POST request contains {"id": <question_id>}

        # Find the document with a problem matching the provided `id` within the problems array
        document = questions_collection.find_one({"problems.id": question_id})

        # Check if the document was found
        if document:
            # Search for the specific problem within the `problems` array
            problem = next((p for p in document['problems'] if p['id'] == question_id), None)

            if problem:
                return JsonResponse({"status": "success", "problem": problem}, status=200)
            else:
                return JsonResponse({"status": "error", "message": "Problem not found in problems array."}, status=404)
        else:
            return JsonResponse({"status": "error", "message": "Question document not found."}, status=404)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

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

def update_question_by_id(request):
    """
    Updates a specific problem in the questions array based on the question ID.
    """
    try:
        # Parse JSON data from the PUT request
        data = json.loads(request.body)
        question_id = data.get("id")  # Assume the PUT request contains {"id": <question_id>, ...other fields...}
        
        # Find and update the problem with the specified ID in the `problems` array
        result = questions_collection.update_one(
            {"problems.id": question_id},
            {"$set": {"problems.$": data}}  # Replace the specific problem document in the array
        )

        if result.matched_count > 0:
            return JsonResponse({"status": "success", "message": "Problem updated successfully."}, status=200)
        else:
            return JsonResponse({"status": "error", "message": "Problem not found."}, status=404)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_question_by_id(request):
    """
    Deletes a specific problem from the questions array based on the question ID.
    """
    try:
        # Parse JSON data from the DELETE request
        data = json.loads(request.body)
        question_id = data.get("id")  # Assume the DELETE request contains {"id": <question_id>}

        # Remove the specific problem with the given `id` from the `problems` array
        result = questions_collection.update_one(
            {"problems.id": question_id},
            {"$pull": {"problems": {"id": question_id}}}
        )

        if result.modified_count > 0:
            return JsonResponse({"status": "success", "message": "Problem deleted successfully."}, status=200)
        else:
            return JsonResponse({"status": "error", "message": "Problem not found."}, status=404)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


