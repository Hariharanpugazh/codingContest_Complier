import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient

# Set up MongoDB connection
client = MongoClient("mongodb://localhost:27017/")  # Adjust as necessary
db = client["Coding_Platform"]
contest_collection = db["Contest_Details"]
user_info_collection = db["User_info"]

@csrf_exempt
def saveDetails(request):
    if request.method == "POST":
        # Parse JSON data from the request body
        data = json.loads(request.body)
        contest_name = data.get('contest_name', '')
        start_time = data.get('start_time', '')
        end_time = data.get('end_time', '')
        organization_type = data.get('organization_type', '')
        organization_name = data.get('organization_name', '')
        testType = data.get('ContestType', '')
        contest_id = data.get('contest_id', '')

        # Prepare data for MongoDB
        contest_data = {
            'contest_name': contest_name,
            'start_time': start_time,
            'end_time': end_time,
            'organization_type': organization_type,
            'organization_name': organization_name,
            'testType': testType,
            'contest_id': contest_id,
        }

        # Insert data into MongoDB collection
        try:
            contest_collection.insert_one(contest_data)
            return JsonResponse({"message": "Contest details saved successfully"})
        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)

@csrf_exempt
def saveUserInfo(request):
    if request.method == "POST":
        # Parse JSON data from the request body
        data = json.loads(request.body)
        print("Received data:", data)  # Debugging line
        
        name = data.get('name', '')
        role = data.get('role', '')
        skills = data.get('skills', [])
        contest_id = data.get('contest_id', '')

        # Prepare data for MongoDB
        user_info_data = {
            'name': name,
            'role': role,
            'skills': skills,
            'contest_id': contest_id,
        }

        print("Data to save:", user_info_data)  # Debugging line

        # Insert data into MongoDB collection
        try:
            user_info_collection.insert_one(user_info_data)
            print("Data inserted successfully")  # Debugging line
            return JsonResponse({"message": "User information saved successfully"})
        except Exception as e:
            print("Error inserting data:", e)  # Debugging line
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)