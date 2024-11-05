import json
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@csrf_exempt
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
        
        # Filter problems based on the role and level
        filtered_problems = [problem for problem in problems_data['problems'] if role in problem.get('role')]
        easy_problems = [problem for problem in filtered_problems if problem.get('level') == 'easy']
        medium_problems = [problem for problem in filtered_problems if problem.get('level') == 'medium']
        hard_problems = [problem for problem in filtered_problems if problem.get('level') == 'hard']

        if role == 'Senior Software Developer':
            easy = 0.4
            medium = 0.3

        if role == 'Junior Software Developer':
            easy = 0.6
            medium = 0.3

        if role == 'AI Developer':
            easy = 0.5
            medium = 0.3

        # Calculate the number of problems to select from each level
        easy_count = round(count * easy)  # 50% for easy
        medium_count = round(count * medium)  # 30% for medium
        hard_count = count - (easy_count + medium_count)  # Remaining 20% for hard

        # Randomly select problems from each level based on the calculated counts
        selected_problems = []
        selected_problems.extend(random.sample(easy_problems, min(easy_count, len(easy_problems))))
        selected_problems.extend(random.sample(medium_problems, min(medium_count, len(medium_problems))))
        selected_problems.extend(random.sample(hard_problems, min(hard_count, len(hard_problems))))

        # Shuffle the selected problems to ensure randomness in order
        random.shuffle(selected_problems)

        # Prepare the data to save
        filtered_data = {"problems": selected_problems}
        
        # Define path to save autoSelected.json in the Frontend directory
        frontend_path = os.path.join(BASE_DIR, '../Frontend/public/json/autoSelected.json')
        
        # Save the selected problems to autoSelected.json in the Frontend directory
        with open(frontend_path, 'w') as outfile:
            json.dump(filtered_data, outfile, indent=2)
        
        return JsonResponse({"message": "Filtered data saved to Frontend/public/json/autoSelected.json"})
    
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
