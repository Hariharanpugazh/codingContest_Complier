import subprocess
from typing import Tuple

def execute_code(user_code: str, language: str, inputs: str, test_case: dict) -> Tuple[str, str]:
    """
    Execute user code and return the output along with the expected output for comparison.
    """
    expected_output = str(test_case["expected_output"])

    try:
        # Command to execute Python code with standard input simulation
        command = ["python", "-c", user_code] if language == "python" else ["your_language_interpreter"]

        # Join input list items into newline-separated string for each input
        simulated_input = "\n".join(map(str, inputs.split("\n")))

        # Run the process and pass the inputs as standard input
        process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(input=simulated_input)

        # If there's an error, return it
        if stderr:
            return stderr.strip(), expected_output

        # Return both the actual output and the expected output for comparison
        return stdout.strip(), expected_output

    except Exception as e:
        return str(e), expected_output
