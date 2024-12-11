import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models_contest import ContestDetails
from datetime import datetime
from bson import ObjectId

# Update the MongoClient to use the provided connection string
client = MongoClient("mongodb+srv://ihub:ihub@test-portal.lcgyx.mongodb.net/test_portal_db?retryWrites=true&w=majority")
db = client["test_portal_db"]  # Ensure this matches the database name in your connection string
contest_collection = db["Contest_Details"]
user_info_collection = db["User_info"]
final_questions_collection = db["finalQuestions"]



def get_contests(request):
    # Fetch all contests from the Contest_Details collection
    contests = list(contest_collection.find({}, {"_id": 0}))  
    return JsonResponse(contests, safe=False)

@csrf_exempt
def delete_contest(request, contest_id):
    if request.method == 'DELETE':
        try:
            # Find the contest by contest_id in the MongoDB collection and delete it
            result = contest_collection.delete_one({'contest_id': contest_id})
            if result.deleted_count == 0:
                return JsonResponse({'error': 'Contest not found'}, status=404)

            # Also delete the corresponding finalQuestions document
            final_questions_result = final_questions_collection.delete_one({'contestId': contest_id})
            if final_questions_result.deleted_count == 0:
                return JsonResponse({'warning': 'Contest deleted, but no corresponding finalQuestions found'}, status=200)

            return JsonResponse({'message': f'Contest with ID {contest_id} and its questions deleted successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)



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

@csrf_exempt
def start_test(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            contest_id = data.get("contest_id")
            student_id = data.get("student_id")

            if not contest_id or not student_id:
                return JsonResponse({"error": "contest_id and student_id are required"}, status=400)

            # Update or insert activity in the contest_activity collection
            db.contest_activity.update_one(
                {"contest_id": contest_id, "student_id": student_id},
                {"$set": {"status": "started", "start_time": datetime.utcnow()}},
                upsert=True
            )
            return JsonResponse({"message": "Test started successfully."}, status=200)
        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)


@csrf_exempt
def finish_test(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            contest_id = data.get("contest_id")
            student_id = data.get("student_id")

            if not contest_id or not student_id:
                return JsonResponse({"error": "contest_id and student_id are required"}, status=400)

            # Update or insert activity in the contest_activity collection
            db.contest_activity.update_one(
                {"contest_id": contest_id, "student_id": student_id},
                {"$set": {"status": "completed", "completion_time": datetime.utcnow()}},
                upsert=True
            )
            return JsonResponse({"message": "Test completed successfully."}, status=200)
        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)


@csrf_exempt
def contest_stats(request, contest_id):
    """
    API to fetch stats for a specific contest.
    """
    try:
        # Fetch students registered for the contest
        total_students = user_info_collection.count_documents({"contest_id": contest_id})

        # Fetch the number of students who started the test
        started = db.contest_activity.count_documents({"contest_id": contest_id, "status": "started"})

        # Fetch the number of students who completed the test
        completed = db.contest_activity.count_documents({"contest_id": contest_id, "status": "completed"})

        # Return the stats as JSON
        return JsonResponse({
            "total_students": total_students,
            "started": started,
            "completed": completed,
        }, status=200)
    except Exception as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

@csrf_exempt
def contest_students(request, contest_id):
    """
    API to fetch students for a specific contest.
    """
    try:
        # Fetch student activities for the contest
        contest_activities = db.contest_activity.find({"contest_id": contest_id})

        student_list = []
        for activity in contest_activities:
            student_id = activity["student_id"]
            student = db.students.find_one({"_id": ObjectId(student_id)})

            if student:
                student_list.append({
                    "id": str(student["_id"]),
                    "name": student["name"],
                    "registration_number": student["regno"],
                    "department": student["dept"],
                    "collegename": student["collegename"],
                    "status": activity.get("status", "not_started"),
                })

        return JsonResponse(student_list, safe=False, status=200)
    except Exception as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)
