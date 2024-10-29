import requests
import base64
from config import API_URL, HEADERS, QUERY_STRING

def execute_code(code, language, stdin_input, selected_row, df):
    encoded_code = base64.b64encode(code.encode()).decode()
    encoded_stdin = base64.b64encode(stdin_input.encode()).decode()
    language_id = 71 if language == "python" else 52 if language == "c_cpp" else 62
    
    payload = {
        "source_code": encoded_code,
        "language_id": language_id,
        "stdin": encoded_stdin
    }
    
    response = requests.post(API_URL, json=payload, headers=HEADERS, params=QUERY_STRING)
    result = response.json()
    output = base64.b64decode(result["stdout"]).decode().strip() if "stdout" in result else ""
    expected_output = str(df.at[selected_row, 'Output']).strip()
    
    return output, expected_output
