import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient

# Set up MongoDB connection
client = MongoClient("mongodb://localhost:27017/")  # Adjust as necessary
db = client["Coding_Platform"]
contest_collection = db["Contest_Details"]
user_info_collection = db["User_info"]
user_results_collection = db['User_results']

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
        user_id = data.get('user_id', '')

        # Prepare data for MongoDB
        user_info_data = {
            'user_id': user_id,
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


@csrf_exempt
def publish_contest(request):
    if request.method == 'POST':
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)
            user_id = data.get('user_id')  # Get the 'user_id' from the request

            if user_id:
                # Convert user_id to an integer if necessary
                if isinstance(user_id, str):
                    user_id = int(user_id)

                # Query User_info collection for the given user_id
                user_data = user_info_collection.find_one({'user_id': user_id})

                if user_data:
                    # Remove MongoDB ObjectId before saving to the new collection
                    user_data.pop('_id', None)

                    # Save the retrieved data to the User_results collection
                    user_results_collection.insert_one(user_data)

                    print(f"User data for user_id {user_id} saved to User_results.")
                    return JsonResponse({'status': 'success', 'message': 'Data saved successfully'})
                else:
                    print(f"User ID {user_id} not found in User_info.")
                    return JsonResponse({'status': 'error', 'message': 'User ID not found in User_info'}, status=404)
            else:
                return JsonResponse({'status': 'error', 'message': 'No user_id provided'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Invalid user_id format'}, status=400)
        except Exception as e:
            print(f"An error occurred: {e}")
            return JsonResponse({'status': 'error', 'message': 'An internal error occurred'}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

