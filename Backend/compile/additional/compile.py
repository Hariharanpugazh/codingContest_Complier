import json
import subprocess
import tempfile
import os
from django.http import JsonResponse


def compilation(source_code, input_data, expected_output, language):
    try:
        # Determine the file extension based on language
        ext = {'python': 'py', 'c': 'c', 'cpp': 'cpp', 'java': 'java'}.get(language)
        if not ext:
            return {"error": "Unsupported language"}

        # Set up the temporary directory path
        temp_dir = "temp_dir"
        os.makedirs(temp_dir, exist_ok=True)

        # Define paths for source code and input file on the local host
        host_source_file_path = os.path.join(temp_dir, f"code.{ext}")
        host_input_file_path = os.path.join(temp_dir, "input.txt")

        # Write the source code to a file in temp_dir
        with open(host_source_file_path, "w") as source_file:
            source_file.write(source_code)

        # Convert input_data items to strings and write them to a file in temp_dir
        with open(host_input_file_path, "w") as input_file:
            input_file.write("\n".join(map(str, input_data)))  # Convert each item to a string

        # Define paths for source code and input file in the Docker container
        container_source_file_path = f"/code/code.{ext}"
        container_input_file_path = "/code/input.txt"

        # Copy the source code and input file into the Docker container
        subprocess.run(["docker", "cp", host_source_file_path, f"test_container:{container_source_file_path}"])
        subprocess.run(["docker", "cp", host_input_file_path, f"test_container:{container_input_file_path}"])

        # Execute compile.sh inside the container
        result = subprocess.run(
            [
                "docker", "exec", "test_container",
                "bash", "/code/compile.sh", language, container_source_file_path, container_input_file_path
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Capture and return output
        return {
            "input": input_data,
            "expected_output": expected_output,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "status": "Success" if result.returncode == 0 else "Error"
        }

    finally:
        # Clean up the files in temp_dir
        if os.path.exists(host_source_file_path):
            os.remove(host_source_file_path)
        if os.path.exists(host_input_file_path):
            os.remove(host_input_file_path)



    
def compilecode(PROBLEMS_FILE_PATH, problem_id, user_code, test_case, language):
    try:
        # Load problem data
        with open(PROBLEMS_FILE_PATH, 'r') as f:
            problems_data = json.load(f)
        problem = get_problem_by_id(problems_data, problem_id)
        
        # Check if the problem and test case exist
        if not problem or test_case not in problem:
            return JsonResponse({"error": "Problem not found or invalid test case."}, status=404)

        # Retrieve the samples for the specified test case
        samples = problem[test_case]

        # Collect results for each sample only once
        results = []
        for sample in samples:
            input_data = sample["input"]
            expected_output = sample["output"]
            result = compilation(user_code, input_data, expected_output, language)
            results.append(result)

        return JsonResponse({"results": results})

    except (IndexError, KeyError, FileNotFoundError):
        return JsonResponse({"error": "Problem not found or invalid index."}, status=404)


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