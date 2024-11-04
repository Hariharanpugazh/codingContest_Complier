import requests
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
        selected_problem_index = data.get('selected_problem_index', 0)

        test_case = 'samples'
        response = compile.compilecode(PROBLEMS_FILE_PATH, selected_problem_index, user_code, test_case, language)
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
        selected_problem_index = data.get('selected_problem_index', 0)
        PROBLEMS_FILE_PATH = filepath.get_filepath()

        test_case = 'hidden_samples'
        response = compile.compilecode(PROBLEMS_FILE_PATH, selected_problem_index, user_code, test_case, language)
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


