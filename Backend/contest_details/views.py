import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ContestDetails  # Import your Django model for MongoDB

@csrf_exempt
def saveDetails(request):
    if request.method == "POST":
        # Parse JSON data from the request body
        data = json.loads(request.body)
        contest_id = data.get('contest_id', '')  # Get contest_id from the request
        contest_name = data.get('contest_name', '')
        start_time = data.get('start_time', '')
        end_time = data.get('end_time', '')
        organization_type = data.get('organization_type', '')
        organization_name = data.get('organization_name', '')
        testType = data.get('ContestType', '')

        # Prepare data for MongoDB
        contest_data = {
            'contest_id': contest_id,  # Include contest_id in the data
            'contest_name': contest_name,
            'start_time': start_time,
            'end_time': end_time,
            'organization_type': organization_type,
            'organization_name': organization_name,
            'testType': testType,
        }

        # Insert data into MongoDB collection
        try:
            ContestDetails.objects.create(**contest_data)  # Save to MongoDB collection
            return JsonResponse({"message": "Details saved successfully"})
        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)