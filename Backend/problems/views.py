import json
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .additional import filter
from pymongo import MongoClient

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Initialize MongoDB client (adjust URI and database name accordingly)
client = MongoClient('mongodb://localhost:27017/')
db = client['Coding_Platform']  # Replace with your database name
collection = db['finalQuestions']  # Replace with your collection name

@csrf_exempt
def userRole(request):
    if request.method == "POST":
        role = request.GET.get('role', 'Junior Software Developer')  # Example role
        count = int(request.GET.get('count', 3))  # Example count
        print(f"Role: {role}, Count: {count}")
        document = collection.find_one({"contestId": "b39wyg7xc"}) 
            
        # Filter problems based on the role
        filtered_problems = [problem for problem in document['problems'] if role in problem.get('role')]
        
        response = filter.filteration(filtered_problems, role, count)
        return response
    
    return JsonResponse({"error": "Invalid request method."}, status=405)

'''
def userRole(request):
    if request.method == "POST":
        data = json.loads(request.body)
        role = data.get('role', '')
        count = data.get('count', '')

        print(BASE_DIR)
        # Load the problems from problems.json
        problems_file_path = os.path.join(BASE_DIR, 'compile', 'jsonfiles', 'questions.json')
        with open(problems_file_path, 'r') as file:
            problems_data = json.load(file)
        
        # Filter problems based on the role
        filtered_problems = [problem for problem in problems_data['problems'] if role in problem.get('role')]

        # Prepare the data to save
        filtered_data = {"problems": filtered_problems}
        
        # Define path to save autoSelected.json in the Frontend directory
        frontend_path = os.path.join(BASE_DIR, '../Frontend/public/json/autoSelected.json')
        
        # Ensure the Frontend directory exists (in case it was moved or deleted)
        # os.makedirs('Frontend', exist_ok=True)
        
        # Save the filtered problems to autoSelected.json in Frontend directory
        with open(frontend_path, 'w') as outfile:
            json.dump(filtered_data, outfile, indent=2)
        
        return JsonResponse({"message": "Filtered data saved to Frontend/autoSelected.json"})
    
    return JsonResponse({"error": "Invalid request method."}, status=405)
'''


# def get_filtered_problems(request):
#     # Fetch problems from MongoDB
#     role = request.GET.get('role', 'Junior Software Developer')  # Example role
#     count = int(request.GET.get('count', 3))  # Example count
#     print(f"Role: {role}, Count: {count}")
#     document = collection.find_one({"contestId": "b39wyg7xc"})  # Adjust query as needed

#     # Check if document exists
#     if not document:
#         return JsonResponse({"error": "Document not found"}, status=404)
    
#     # Extract problems from the document
#     filtered_problems = document.get("problems", [])

#     # Call the filteration function to filter and save problems
#     return filteration(filtered_problems, role, count)

    