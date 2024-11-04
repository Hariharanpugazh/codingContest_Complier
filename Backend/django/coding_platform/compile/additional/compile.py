import requests
from django.http import JsonResponse
import json

API_URL = "https://judge029.p.rapidapi.com/submissions"


def compilation(source_code, input_data, expected_output, language):

    language_id = get_languageid(language)

    try:
        headers = {
            "x-rapidapi-key": "9e24c55881mshcdcdd68192b062bp10dea0jsnb05b06d6a8ee",
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
            "language_id": language_id, 
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
    
def compilecode(PROBLEMS_FILE_PATH, problem_id, user_code, test_case, language):

    try:
        with open(PROBLEMS_FILE_PATH, 'r') as f:
            problems_data = json.load(f)
        problem = get_problem_by_id(problems_data, problem_id)
        samples = problem[test_case]

    except (IndexError, KeyError, FileNotFoundError):
        return JsonResponse({"error": "Problem not found or invalid index."}, status=404)

    # Collect results for each sample
    results = []
    for sample in samples:
        input_data = sample["input"]
        expected_output = sample["output"]
        result = compilation(user_code, input_data, expected_output, language)
        results.append(result)

    return JsonResponse({"results": results})

def get_languageid(language):
    
    language_id = {
    'Assembly (NASM 2.14.02)': 45,
    'Bash (5.0.0)': 46,
    'Basic (FBC 1.07.1)': 47,
    'C (GCC 7.4.0)': 48,
    'C++ (GCC 7.4.0)': 52,
    'C (GCC 8.3.0)': 49,
    'C++ (GCC 8.3.0)': 53,
    'C (GCC 9.2.0)': 50,
    'C++ (GCC 9.2.0)': 54,
    'C# (Mono 6.6.0.161)': 51,
    'Common Lisp (SBCL 2.0.0)': 55,
    'D (DMD 2.089.1)': 56,
    'Elixir (1.9.4)': 57,
    'Erlang (OTP 22.2)': 58,
    'Executable': 44,
    'Fortran (GFortran 9.2.0)': 59,
    'Go (1.13.5)': 60,
    'Haskell (GHC 8.8.1)': 61,
    'Java (OpenJDK 13.0.1)': 62,
    'JavaScript (Node.js 12.14.0)': 63,
    'Lua (5.3.5)': 64,
    'OCaml (4.09.0)': 65,
    'Octave (5.1.0)': 66,
    'Pascal (FPC 3.0.4)': 67,
    'PHP (7.4.1)': 68,
    'Plain Text': 43,
    'Prolog (GNU Prolog 1.4.5)': 69,
    'Python (2.7.17)': 70,
    'Python (3.8.1)': 71,
    'Ruby (2.7.0)': 72,
    'Rust (1.40.0)': 73,
    'TypeScript (3.7.4)': 74
}
    return language_id[language]

def get_problem_by_id(problems_data, problem_id):
    for problem in problems_data["problems"]:
        if problem["id"] == problem_id:
            return problem
    return None