from django.http import JsonResponse
from pymongo import MongoClient
from bson import ObjectId
import json
import os
from django.views.decorators.csrf import csrf_exempt

from pymongo import MongoClient

# Update the MongoClient to use the provided connection string
client = MongoClient("mongodb+srv://ihub:ihub@test-portal.lcgyx.mongodb.net/test_portal_db?retryWrites=true&w=majority")
db = client["test_portal_db"]  # Ensure this matches the database name in your connection string
questions_collection = db['finalQuestions'] 

@csrf_exempt
def fetch_Questions(request):
    # Access the finalQuestions collection
    collection = db['finalQuestions']

    # Fetch the document with the contestId, assuming there's only one
    document = collection.find_one({}, {'problems': 1, '_id': 0})  # Retrieve only the 'problems' field and exclude '_id'

    # If no document is found, return an empty problems array
    if not document:
        return JsonResponse({'problems': []})

    # Extract the problems list from the document
    problems = document.get('problems', [])

    # Format the problems as required
    formatted_problems = []
    for problem in problems:
        formatted_problem = {
            "id": problem.get("id"),
            "title": problem.get("title"),
            "level": problem.get("level"),
            "problem_statement": problem.get("problem_statement"),
            "samples": [
                {"input": sample.get("input"), "output": sample.get("output")}
                for sample in problem.get("samples", [])
            ],
            "hidden_samples": [
                {"input": hidden_sample.get("input"), "output": hidden_sample.get("output")}
                for hidden_sample in problem.get("hidden_samples", [])
            ]
        }
        formatted_problems.append(formatted_problem)

    # Return the formatted response
    return JsonResponse({'problems': formatted_problems})



def fetch_and_save_questions(request):
    # Path to the frontend's public/json/questions.json file
    # Adjust the path to your actual frontend directory
    file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'Frontend', 'public', 'json', 'questions.json')

    # Fetch data from MongoDB
    document = questions_collection.find_one({}, {'problems': 1, '_id': 0})
    if not document:
        return JsonResponse({'error': 'No data found in finalQuestions collection'}, status=404)

    # Prepare the data for saving
    data_to_save = {'problems': document.get('problems', [])}

    # Write the fetched data to questions.json
    try:
        with open(file_path, 'w') as file:
            json.dump(data_to_save, file, indent=2)
        print('Data successfully written to questions.json')
    except Exception as e:
        return JsonResponse({'error': f'Failed to save JSON file: {str(e)}'}, status=500)

    # Return the fetched data as a JSON response
    return JsonResponse(data_to_save)