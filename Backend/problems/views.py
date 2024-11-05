import json
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@csrf_exempt
def userRole(request):
    if request.method == "POST":
        data = json.loads(request.body)
        role = data.get('role', '')
        count = data.get('count', 0)

        # Load the problems from questions.json
        problems_file_path = os.path.join(BASE_DIR, 'compile', 'jsonfiles', 'questions.json')
        with open(problems_file_path, 'r') as file:
            problems_data = json.load(file)
        
        # Filter problems based on the role
        filtered_problems = [problem for problem in problems_data['problems'] if role in problem.get('role')]
        
        # If count is 0 or greater than available problems, return all problems
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

            # Prepare the data to save
            filtered_data = {"problems": selected_problems}
        
        # Define paths to save autoSelected.json in both Frontend and Backend directories
        frontend_path = os.path.join(BASE_DIR, '../Frontend/public/json/autoSelected.json')
        backend_path = os.path.join(BASE_DIR, 'compile', 'jsonfiles', 'autoSelected.json')
        
        # Save the selected problems to autoSelected.json in the Frontend and Backend directories
        with open(frontend_path, 'w') as outfile:
            json.dump(filtered_data, outfile, indent=2)

        with open(backend_path, 'w') as outfile:
            json.dump(filtered_data, outfile, indent=2)
        
        return JsonResponse({"message": "Filtered data saved to Frontend/public/json/autoSelected.json and Backend/compile/jsonfiles/autoSelected.json"})
    
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
