import streamlit as st
from streamlit_ace import st_ace
import requests
import base64
import pandas as pd
import os

# API details
url = "https://judge029.p.rapidapi.com/submissions"
headers = {
    "x-rapidapi-key": "4c6f0f6fc5msh9ca8144c4f547fep16ac54jsndd5114267fd4",
    "x-rapidapi-host": "judge029.p.rapidapi.com",
    "Content-Type": "application/json"
}
querystring = {"base64_encoded": "true", "wait": "true", "fields": "*"}

# Set page configuration to wide mode
st.set_page_config(layout="wide")

# Load test cases from CSV file
@st.cache_data
def load_test_cases():
    file_path = os.path.join(os.path.dirname(__file__), 'test.csv')
    return pd.read_csv(file_path)

# Custom layout for columns
col1, col2 = st.columns([2, 3])

try:
    # Load test cases
    df = load_test_cases()
    
    # Left Column: Test Cases
    with col1:
        st.markdown("### Test Cases")
        
        # Dropdown for test case selection
        selected_row = st.selectbox(
            "Select a problem to solve:",
            options=range(len(df)),
            format_func=lambda x: f"Problem {df.at[x, 'S.no']}: {df.at[x, 'Description']}"
        )
        
        # Display Problem Details
        st.markdown("### Problem Details")
        st.markdown("**Description:**")
        st.text_area("", df.at[selected_row, "Description"], height=60, disabled=True)
        
        # Display Example Inputs
        stdin_input = ""
        inputs = []
        if df.at[selected_row, 'Has input'] == 'Yes':
            st.markdown("**Example Input(s):**")
            num_inputs = int(df.at[selected_row, 'No of inputs'])
            for i in range(1, num_inputs + 1):
                input_value = df.at[selected_row, f'Input{i}']
                user_input = st.text_input(f"Input {i}:", value=str(input_value))
                inputs.append(user_input)
            stdin_input = "\n".join(inputs)
        
        # Display Expected Output
        st.markdown("**Expected Output:**")
        expected_output = str(df.at[selected_row, 'Output']).strip()
        st.text_area("", expected_output, height=30, disabled=True)

    # Right Column: Code Editor and Run
    with col2:
        st.markdown("### Code Editor")
        language = st.selectbox("Select Programming Language", ["python", "c_cpp", "java"], key="language")

        # Code Editor
        user_code = st_ace(
            language=language,
            theme="dracula",
            placeholder="Write your code here...",
            keybinding="vscode",
            height=300,
            font_size=16,
            show_gutter=True,
            show_print_margin=False,
            wrap=True,
            auto_update=True,
            key="editor"
        )
        
        # Buttons for Compile & Run and Submit
        col3, col4 = st.columns(2)
        with col3:
            if st.button("Compile & Run"):
                # Encode the code and input to base64 as required by the API
                encoded_code = base64.b64encode(user_code.encode()).decode()
                encoded_stdin = base64.b64encode(stdin_input.encode()).decode() if stdin_input else ""
                
                # Set language_id based on selected language
                language_id = 71 if language == "python" else 52 if language == "c_cpp" else 62
                
                payload = {
                    "source_code": encoded_code,
                    "language_id": language_id,
                    "stdin": encoded_stdin
                }

                # Make API request
                try:
                    response = requests.post(url, json=payload, headers=headers, params=querystring)
                    result = response.json()
                    
                    # Check for output
                    if "stdout" in result:
                        st.write("### Output:")
                        output = base64.b64decode(result["stdout"]).decode().strip()
                        st.code(output, language="text")
                        
                        # Compare with expected output
                        if output == expected_output:
                            st.success("✅ Output matches expected result!")
                        else:
                            st.error("❌ Output doesn't match expected result")
                            st.write(f"Expected: {expected_output}")
                            
                    elif "stderr" in result:
                        st.write("### Error:")
                        st.code(base64.b64decode(result["stderr"]).decode(), language="text")
                    else:
                        st.write("### Unexpected API Response:")
                        st.json(result)
                        
                except Exception as e:
                    st.error(f"Failed to execute code: {e}")
        
        with col4:
            if st.button("Submit"):
                st.write("### Submitted Code:")
                st.code(user_code, language=language)

except FileNotFoundError:
    st.error("Error: testcases.csv file not found. Please ensure the file exists in the same directory as the script.")
except Exception as e:
    st.error(f"Error loading test cases: {e}")
