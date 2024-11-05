import json
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@csrf_exempt
def userRole(request):
    if request.method == "POST":
        data = json.loads(request.body)
        role = data.get('role', '')

        print(BASE_DIR)
        # Load the problems from problems.json
        problems_file_path = os.path.join(BASE_DIR, 'compile', 'jsonfiles', 'questions.json')
        with open(problems_file_path, 'r') as file:
            problems_data = json.load(file)
        
        # Filter problems based on the role
        filtered_problems = [problem for problem in problems_data['problems'] if problem.get('role') == role]

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
