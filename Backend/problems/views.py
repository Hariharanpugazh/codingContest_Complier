import json
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .additional import filter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@csrf_exempt
def userRole(request):
    if request.method == "POST":
        data = json.loads(request.body)
        role = data.get('role', '')
        count = 3

        # Load the problems from questions.json
        problems_file_path = os.path.join(BASE_DIR, 'compile', 'jsonfiles', 'questions.json')
        with open(problems_file_path, 'r') as file:
            problems_data = json.load(file)
        
        # Filter problems based on the role
        filtered_problems = [problem for problem in problems_data['problems'] if role in problem.get('role')]
        
        response = filter.filteration(filtered_problems, role, count, BASE_DIR)
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

import random
import os
import json
from django.http import JsonResponse
from pymongo import MongoClient

# Define the path to the JSON file where problems should be saved
PROBLEMS_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'Frontend', 'public', 'json', 'questions.json')

# Initialize MongoDB client (adjust URI and database name accordingly)
client = MongoClient('mongodb://localhost:27017/')
db = client['Coding_Platform']  # Replace with your database name
collection = db['finalQuestions']  # Replace with your collection name

def filteration(filtered_problems, role, count):
    # If count is 0 or greater than available problems, use all problems
    if count == 0 or count >= len(filtered_problems):
        filtered_data = {"problems": filtered_problems}
    else:
        # Separate problems by level
        easy_problems = [problem for problem in filtered_problems if problem.get('level') == 'easy']
        medium_problems = [problem for problem in filtered_problems if problem.get('level') == 'medium']
        hard_problems = [problem for problem in filtered_problems if problem.get('level') == 'hard']

        # Define proportions based on role
        if role == 'Senior Software Developer':
            easy, medium = 0.4, 0.3
        elif role == 'Junior Software Developer':
            easy, medium = 0.6, 0.3
        elif role == 'AI Developer':
            easy, medium = 0.5, 0.3
        else:
            easy, medium = 0.5, 0.3  # Default proportions if role is unknown

        # Calculate the number of problems to select from each level
        easy_count = round(count * easy)
        medium_count = round(count * medium)
        hard_count = count - (easy_count + medium_count)

        # Randomly select problems from each level based on the calculated counts
        selected_problems = []
        selected_problems.extend(random.sample(easy_problems, min(easy_count, len(easy_problems))))
        selected_problems.extend(random.sample(medium_problems, min(medium_count, len(medium_problems))))
        selected_problems.extend(random.sample(hard_problems, min(hard_count, len(hard_problems))))

        # Shuffle the selected problems to ensure randomness in order
        random.shuffle(selected_problems)

        # Prepare the filtered data
        filtered_data = {"problems": selected_problems}

    # Save the filtered data to the specified JSON file
    with open(PROBLEMS_FILE_PATH, 'w') as outfile:
        json.dump(filtered_data, outfile, indent=2)

    # Return a success message
    return JsonResponse({"message": f"Filtered data saved to {PROBLEMS_FILE_PATH}"})

def get_filtered_problems(request):
    # Fetch problems from MongoDB
    role = request.GET.get('role', 'Junior Software Developer')  # Example role
    count = int(request.GET.get('count', 3))  # Example count
    print(f"Role: {role}, Count: {count}")
    document = collection.find_one({"contestId": "b39wyg7xc"})  # Adjust query as needed

    # Check if document exists
    if not document:
        return JsonResponse({"error": "Document not found"}, status=404)
    
    # Extract problems from the document
    filtered_problems = document.get("problems", [])

    # Call the filteration function to filter and save problems
    return filteration(filtered_problems, role, count)

    