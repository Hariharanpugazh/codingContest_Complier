
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