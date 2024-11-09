from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
import traceback
from pymongo import MongoClient

def get_problems():
    """Load existing problem data."""
    # Define the full path for the compile/jsonfiles directory
    directory = os.path.join(os.path.dirname(__file__), '..', 'compile', 'jsonfiles')
    file_path = os.path.join(directory, 'manualProblems.json')

    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)

    return JsonResponse(get_existing_data(file_path), status=200, safe=False)

def save_problem_data(new_problem):
    try:
        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB connection string if different
        db = client['Coding_Platform']  # Replace with your database name
        collection = db['ManualUpload_onebyone']
        
        # Create a properly structured document
        problem_document = {
            "id": new_problem.get('id'),
            "title": new_problem.get('title', ''),
            "role": new_problem.get('role', []),
            "level": new_problem.get('level', ''),
            "problem_statement": new_problem.get('problem_statement', ''),
            "samples": new_problem.get('samples', []),
            "hidden_samples": new_problem.get('hidden_samples', [])
        }
        
        # Remove None values
        problem_document = {k: v for k, v in problem_document.items() if v is not None}
        
        # Check if document with this id already exists
        existing_problem = collection.find_one({'id': problem_document['id']})
        
        if existing_problem:
            # Update existing document
            result = collection.update_one(
                {'id': problem_document['id']},
                {'$set': problem_document}
            )
            message = 'Problem updated successfully!'
        else:
            # Insert new document
            result = collection.insert_one(problem_document)
            message = 'Problem created successfully!'

        # Verify the operation was successful
        if result:
            return JsonResponse({
                'message': message,
                'problem_id': problem_document['id']
            }, status=201)
        else:
            raise Exception("Failed to save the document")

    except Exception as e:
        return JsonResponse({
            'error': f'Error saving problem data: {str(e)}'
        }, status=400)
    
    finally:
        # Close the MongoDB connection
        client.close()

def modify_problem_data(new_problem, file_path):
    """Modify an existing problem based on the given ID."""
    # Define the full path for the compile/jsonfiles directory
    directory = os.path.join(os.path.dirname(__file__), '..', 'compile', 'jsonfiles')
    file_path = os.path.join(directory, 'manualProblems.json')

    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)

    existing_data = get_existing_data(file_path)
    problem_id = str(new_problem.get("id"))
    
    # Remove all instances of problems with the same ID
    existing_data["problems"] = [
        p for p in existing_data["problems"] 
        if str(p.get("id")) != problem_id
    ]
    
    # Add the modified problem
    existing_data["problems"].append(new_problem)
    
    try:
        with open(file_path, 'w') as json_file:
            json.dump(existing_data, json_file, indent=4)
        return JsonResponse({'message': 'Problem modified successfully!'}, status=200)
    except Exception as e:
        print("Error modifying problem:", str(e))
        traceback.print_exc()
        return JsonResponse({'error': 'Failed to modify problem data'}, status=500)

def delete_problem_data(problem_id):
    """Delete a problem based on the given ID."""
    # Define the full path for the compile/jsonfiles directory
    directory = os.path.join(os.path.dirname(__file__), '..', 'compile', 'jsonfiles')
    file_path = os.path.join(directory, 'manualProblems.json')

    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)

    existing_data = get_existing_data(file_path)
    str_problem_id = str(problem_id)
    
    # Remove all instances of the problem with the given ID
    original_length = len(existing_data["problems"])
    existing_data["problems"] = [
        p for p in existing_data["problems"] 
        if str(p.get("id")) != str_problem_id
    ]

    if len(existing_data["problems"]) == original_length:
        return JsonResponse({'error': 'Problem not found for deletion'}, status=404)

    try:
        with open(file_path, 'w') as json_file:
            json.dump(existing_data, json_file, indent=4)
        return JsonResponse({'message': 'Problem deleted successfully!'}, status=200)
    except Exception as e:
        print("Error deleting problem:", str(e))
        traceback.print_exc()
        return JsonResponse({'error': 'Failed to delete problem data'}, status=500)

def get_existing_data(file_path):
    """Helper function to load existing data from file."""
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, 'r') as json_file:
            try:
                data = json.load(json_file)
                # Remove any duplicate IDs that might exist
                seen_ids = set()
                unique_problems = []
                for problem in data["problems"]:
                    problem_id = str(problem.get("id"))
                    if problem_id not in seen_ids:
                        seen_ids.add(problem_id)
                        unique_problems.append(problem)
                data["problems"] = unique_problems
                return data
            except json.JSONDecodeError:
                return {"problems": []}
    return {"problems": []}

@csrf_exempt
def save_problem(request):
    directory = os.path.join(os.path.dirname(__file__), '..', 'compile', 'jsonfiles')
    file_path = os.path.join(directory, 'manualProblems.json')
    """Handle saving, modifying, and deleting problems."""
    if request.method == 'GET':
        return get_problems()

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_problem = data.get("problems", [])[0]
            return save_problem_data(new_problem)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            print("An error occurred:", str(e))
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=500)

    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            new_problem = data.get("problems", [])[0]
            return modify_problem_data(new_problem, file_path)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            print("An error occurred:", str(e))
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=500)

    elif request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            problem_id = data.get("id")
            return delete_problem_data(problem_id)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            print("An error occurred:", str(e))
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=500)

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)