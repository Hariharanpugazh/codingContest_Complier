import os
import csv
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Define the path to the directory and file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_DIR_PATH = os.path.join(BASE_DIR, 'contest_details', 'contest_csv')
CSV_FILE_PATH = os.path.join(CSV_DIR_PATH, 'contest_details.csv')

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

        # Ensure the directory exists
        os.makedirs(CSV_DIR_PATH, exist_ok=True)

        # Append the data to the CSV file
        file_exists = os.path.isfile(CSV_FILE_PATH)
        with open(CSV_FILE_PATH, mode='a', newline='') as file:
            writer = csv.writer(file)
            # Write the header only if the file is created for the first time
            if not file_exists:
                writer.writerow(['Contest Name', 'Start Time', 'End Time', 'Organization Type', 'Organization Name'])
            writer.writerow([contest_name, start_time, end_time, organization_type, organization_name])

        return JsonResponse({"message": "Details saved successfully"})

    return JsonResponse({"error": "Invalid request method."}, status=405)
