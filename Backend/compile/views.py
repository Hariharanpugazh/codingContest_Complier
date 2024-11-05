from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
from .additional import compile, csvtojson, filepath


# PROBLEMS_FILE_PATH = os.path.join('compile/jsonfiles', 'questions.json')

@csrf_exempt
def compileCode(request):
    if request.method == "POST":
        
        PROBLEMS_FILE_PATH = filepath.get_filepath()
        
        print('PROBLEMS_FILE_PATH:',PROBLEMS_FILE_PATH)

        data = json.loads(request.body)
        user_code = data.get('user_code', '')
        language = data.get('language', '')
        problem_id = data.get('problem_id', 0)

        test_case = 'samples'
        response = compile.compilecode(PROBLEMS_FILE_PATH, problem_id, user_code, test_case, language)
        return response

    return JsonResponse({"error": "Invalid request method."}, status=405)

@csrf_exempt
def compileHidden(request):
    if request.method == "POST":

        PROBLEMS_FILE_PATH = filepath.get_filepath()

        print('PROBLEMS_FILE_PATH:',PROBLEMS_FILE_PATH)

        data = json.loads(request.body)
        user_code = data.get('user_code', '')
        language = data.get('language', '')
        problem_id = data.get('problem_id', 0)
        PROBLEMS_FILE_PATH = filepath.get_filepath()

        test_case = 'hidden_samples'
        response = compile.compilecode(PROBLEMS_FILE_PATH, problem_id, user_code, test_case, language)
        return response

    return JsonResponse({"error": "Invalid request method."}, status=405)
    

@csrf_exempt
def userInput(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('file')
        if not csv_file:
            return JsonResponse({'error': 'No file provided'}, status=400)
        

        output_dir = 'compile/jsonfiles'  # Directory to save problems.json
        os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist
        output_json_path = os.path.join(output_dir, 'problems.json')  # Path for problems.json

        response = csvtojson.csv_to_json(csv_file, output_json_path)
        return response


@csrf_exempt
def selectedProblems(request):
    if request.method == "POST":
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)
            selected_ids = data.get('selected', [])

            # Define the directory and file paths
            directory = 'compile/jsonfiles'
            questions_file = os.path.join(directory, 'questions.json')
            selected_file = os.path.join(directory, 'selected.json')

            # Load the questions.json file
            if not os.path.exists(questions_file):
                return JsonResponse({"error": "questions.json not found."}, status=404)

            with open(questions_file, 'r') as f:
                questions_data = json.load(f)

            # Filter the problems based on the selected IDs
            filtered_problems = [
                problem for problem in questions_data.get('problems', [])
                if problem['id'] in selected_ids
            ]

            # Save the filtered problems to selected.json
            with open(selected_file, 'w') as f:
                json.dump({'selected_problems': filtered_problems}, f, indent=4)

            return JsonResponse({"message": "Selected problems saved successfully", "file": selected_file}, status=200)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)
