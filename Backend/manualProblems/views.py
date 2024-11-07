from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
import traceback

@csrf_exempt
def save_problem(request):
    # Define the full path for the compile/jsonfiles directory
    directory = os.path.join(os.path.dirname(__file__), '..', 'compile', 'jsonfiles')
    file_path = os.path.join(directory, 'manualProblems.json')
    
    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)
    
    # Load existing data if the file exists and is not empty
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, 'r') as json_file:
            try:
                existing_data = json.load(json_file)
            except json.JSONDecodeError:
                existing_data = {"problems": []}  # Reset to default if JSON is invalid
    else:
        existing_data = {"problems": []}  # Initialize with default if file doesn't exist or is empty

    if request.method == 'GET':
        # Return the existing problems data
        return JsonResponse(existing_data, status=200, safe=False)

    elif request.method == 'POST':
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)
            new_problem = data.get("problems", [])[0]

            # Check if the problem already exists (by id) and update it, otherwise add it
            problem_id = new_problem.get("id")
            problem_exists = False

            for index, problem in enumerate(existing_data["problems"]):
                if problem.get("id") == problem_id:
                    # Update existing problem
                    existing_data["problems"][index] = new_problem
                    problem_exists = True
                    break

            if not problem_exists:
                # Add new problem if it does not exist
                existing_data["problems"].append(new_problem)

            # Write the updated data back to the file
            with open(file_path, 'w') as json_file:
                json.dump(existing_data, json_file, indent=4)

            return JsonResponse({'message': 'Problem data saved successfully!'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            print("An error occurred:", str(e))
            traceback.print_exc()  # Print stack trace for debugging
            return JsonResponse({'error': str(e)}, status=500)

    elif request.method == 'DELETE':
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)
            problem_id = data.get("id")

            # Remove the problem with the specified id
            existing_data["problems"] = [
                problem for problem in existing_data["problems"] if problem.get("id") != problem_id
            ]

            # Write the updated data back to the file
            with open(file_path, 'w') as json_file:
                json.dump(existing_data, json_file, indent=4)

            return JsonResponse({'message': 'Problem deleted successfully!'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            print("An error occurred:", str(e))
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=500)

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
