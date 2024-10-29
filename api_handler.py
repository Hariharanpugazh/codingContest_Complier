import requests
import base64
from config import API_URL, HEADERS, QUERY_STRING

def execute_code(code, language, stdin_input, selected_problem_index, problems):
    encoded_code = base64.b64encode(code.encode()).decode()
    encoded_stdin = base64.b64encode(stdin_input.encode()).decode()
    language_id = 71 if language == "python" else 52 if language == "c_cpp" else 62
    
    payload = {
        "source_code": encoded_code,
        "language_id": language_id,
        "stdin": encoded_stdin
    }
    
    try:
        response = requests.post(API_URL, json=payload, headers=HEADERS, params=QUERY_STRING)
        response.raise_for_status()  # Check for HTTP errors
        result = response.json()
        
        # Check if stdout is available and not None
        if "stdout" in result and result["stdout"] is not None:
            output = base64.b64decode(result["stdout"]).decode().strip()
        else:
            output = result.get("stderr", "No output produced. Check your code or API response.").strip()
        
        # Access expected output from the problems list
        expected_output = str(problems[selected_problem_index]["samples"][0]["output"]).strip()
        return output, expected_output

    except requests.exceptions.RequestException as e:
        return f"API request failed: {str(e)}", ""
    except KeyError as e:
        return f"Unexpected API response format: missing key {str(e)}", ""
