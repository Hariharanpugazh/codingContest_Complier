import requests
from django.http import JsonResponse
import json

API_URL = "https://judge029.p.rapidapi.com/submissions"


def compilation(source_code, input_data, expected_output):
    try:
        headers = {
            "x-rapidapi-key": "b1dfe04abcmsh9913f5c4cec3b70p1afb24jsnf8efde41a2ea",
            "x-rapidapi-host": "judge029.p.rapidapi.com",
            "Content-Type": "application/json"
        }

        # Join input data with newline if it's a list; otherwise, treat it as a single string
        if isinstance(input_data, list):
            stdin_data = "\n".join(map(str, input_data))
        else:
            stdin_data = str(input_data)

        payload = {
            "source_code": source_code,
            "language_id": 71,  # Python
            "stdin": stdin_data,
            "expected_output": str(expected_output)
        }

        querystring = {"base64_encoded": "false", "wait": "true", "fields": "*"}
        response = requests.post(API_URL, json=payload, headers=headers, params=querystring)
        response.raise_for_status()

        response_data = response.json()
        return {
            "input": input_data,
            "expected_output": expected_output,
            "stdout": response_data.get("stdout"),
            "stderr": response_data.get("stderr"),
            "status": response_data.get("status", {}).get("description"),
            "time": response_data.get("time"),
            "memory": response_data.get("memory"),
        }

    except requests.RequestException as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}
    
def compilecode(PROBLEMS_FILE_PATH, selected_problem_index, user_code, test_case):

    try:
        with open(PROBLEMS_FILE_PATH, 'r') as f:
            problems_data = json.load(f)
        problem = problems_data["problems"][selected_problem_index]
        samples = problem[test_case]

    except (IndexError, KeyError, FileNotFoundError):
        return JsonResponse({"error": "Problem not found or invalid index."}, status=404)

    # Collect results for each sample
    results = []
    for sample in samples:
        input_data = sample["input"]
        expected_output = sample["output"]
        result = compilation(user_code, input_data, expected_output)
        results.append(result)

    return JsonResponse({"results": results})