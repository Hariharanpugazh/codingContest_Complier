from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
import random
import os
import json

# Initialize MongoDB connection
client = MongoClient('mongodb://localhost:27017/')  # Replace with your connection URI
db = client['Coding_Platform']  # Replace with your database name
collection = db['finalQuestions']  # Replace with your collection name

PROBLEMS_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'Frontend', 'public', 'json', 'questions.json')    
@csrf_exempt
def userRole(request):
    if request.method == "POST":
        try:
            # Parse JSON request body
            data = json.loads(request.body)
            role = data.get('role', '')  # User role
            contest_id = data.get('contest_id', '')  # Contest ID entered by the user
            count = 3  # Default number of questions to fetch

            # Validate inputs
            if not contest_id:
                return JsonResponse({"error": "Contest ID is required."}, status=400)
            if not role:
                return JsonResponse({"error": "Role is required."}, status=400)

            # Fetch the contest data from MongoDB using the contest_id
            document = collection.find_one({"contestId": contest_id})
            if not document:
                return JsonResponse({"error": f"No contest found for contest_id: {contest_id}"}, status=404)

            # Extract problems from the database document
            problems = document.get("problems", [])
            if not problems:
                return JsonResponse({"error": "No problems found for this contest."}, status=404)

            # Debug: Log the total number of problems fetched
            print(f"Total problems fetched for contest ID '{contest_id}': {len(problems)}")

            # Filter and randomize the problems using the filteration function
            filtered_problems = filteration(problems, role, count)

            # Prepare the response format
            response_data = {"problems": filtered_problems}

            # Overwrite the JSON file with the new data
            os.makedirs(os.path.dirname(PROBLEMS_FILE_PATH), exist_ok=True)
            with open(PROBLEMS_FILE_PATH, 'w') as file:
                json.dump(response_data, file, indent=2)

            print(f"Filtered problems saved to {PROBLEMS_FILE_PATH}")

            # Return success response
            return JsonResponse({"message": "Problems filtered and saved successfully!", "path": PROBLEMS_FILE_PATH}, status=200)

        except Exception as e:
            # Handle unexpected errors
            print(f"Error in userRole: {e}")
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)


def filteration(filtered_problems, role, count):
    import random

    # Separate problems by difficulty level
    easy_problems = [p for p in filtered_problems if p.get('level') == 'easy']
    medium_problems = [p for p in filtered_problems if p.get('level') == 'medium']
    hard_problems = [p for p in filtered_problems if p.get('level') == 'hard']

    # Debugging: Log the available problems by difficulty
    print(f"Easy: {len(easy_problems)}, Medium: {len(medium_problems)}, Hard: {len(hard_problems)}")

    # Define proportions based on role
    role_proportions = {
        'Senior Software Developer': (0.4, 0.3),
        'Junior Software Developer': (0.6, 0.3),
        'AI Developer': (0.5, 0.3),
    }
    easy, medium = role_proportions.get(role, (0.5, 0.3))  # Default proportions

    # Calculate the number of problems to select
    easy_count = round(count * easy)
    medium_count = round(count * medium)
    hard_count = count - (easy_count + medium_count)

    # Debugging: Log the required number of problems for each difficulty level
    print(f"Required: Easy={easy_count}, Medium={medium_count}, Hard={hard_count}")

    # Randomly sample problems for each level
    selected_problems = []
    selected_problems.extend(random.sample(easy_problems, min(easy_count, len(easy_problems))))
    selected_problems.extend(random.sample(medium_problems, min(medium_count, len(medium_problems))))
    selected_problems.extend(random.sample(hard_problems, min(hard_count, len(hard_problems))))

    # Shuffle the selected problems to ensure randomness
    random.shuffle(selected_problems)

    # Return the filtered problems
    return selected_problems