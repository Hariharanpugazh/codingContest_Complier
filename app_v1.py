import streamlit as st
from streamlit_ace import st_ace
import requests
import base64
import pandas as pd
import os

# API details
url = "https://judge029.p.rapidapi.com/submissions"
headers = {
    "x-rapidapi-key": "294b47d3a3mshaa7387d693fb899p11022djsnd205901aa3c7",
    "x-rapidapi-host": "judge029.p.rapidapi.com",
    "Content-Type": "application/json"
}
querystring = {"base64_encoded": "true", "wait": "true", "fields": "*"}

# Set page configuration to wide mode
st.set_page_config(layout="wide")

# Custom CSS for layout and border between columns
st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        font-family: "Sans-serif";
    }
    .css-1d391kg, .css-18e3th9 {
        padding: 1rem 2rem;
    }
    .left-column {
        padding-right: 1rem;
        border-right: 2px solid #3E3E3E;
    }
    .right-column {
        padding-left: 1.5rem;
    }
    .stButton { 
        margin-top: 0.5rem;
    }
    .test-case-header {
        
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .description-box {
        
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        margin-bottom: 1rem;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# Load test cases from CSV file
@st.cache_data
def load_test_cases():
    # Assuming the CSV file is in the same directory as the script
    file_path = os.path.join(os.path.dirname(__file__), 'test.csv')
    return pd.read_csv(file_path)

# Create two columns with different width ratios
col1, col2 = st.columns([2, 3])

try:
    # Load test cases
    df = load_test_cases()
    
    # Left Column: Test Cases
    with col1:
        st.markdown("### Test Cases", unsafe_allow_html=True)
        
        # Create dropdown for test case selection
        selected_row = st.selectbox(
            "Select a problem to solve:",
            options=range(len(df)),
            format_func=lambda x: f"Problem {df.at[x, 'S.no']}: {df.at[x, 'Description']}"
        )
        
        # Store selected row in session state
        st.session_state['selected_row'] = selected_row
        
        # Display selected test case details
        st.markdown('<div class="test-case-header">', unsafe_allow_html=True)
        st.markdown("### Problem Details")
        st.markdown("**Description:**")
        st.markdown(f'<div class="description-box">{df.at[selected_row, "Description"]}</div>', unsafe_allow_html=True)
        
        if df.at[selected_row, 'Has input']:
            st.markdown("**Example Input(s):**")
            num_inputs = int(df.at[selected_row, 'No of inputs'])
            for i in range(1, num_inputs + 1):
                st.write(f"Input {i}: {df.at[selected_row, f'Input{i}']}")
        
        st.markdown("**Expected Output:**")
        st.markdown(f'<div class="description-box">{df.at[selected_row, "Output"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Right Column: Code Editor and Run
    with col2:
        st.markdown("### Code Editor")
        language = st.selectbox("Select Programming Language", ["python", "c_cpp", "java"], key="language")

        # Ace editor setup with fixed height
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
        
        # Get the selected test case details
        selected_row = st.session_state.get('selected_row', 0)
        
        # Handle inputs based on Has input and No of inputs
        stdin_input = ""
        if df.at[selected_row, 'Has input']:
            num_inputs = int(df.at[selected_row, 'No of inputs'])
            inputs = []
            
            # Create columns for inputs
            input_cols = st.columns(num_inputs)
            for i, col in enumerate(input_cols, 1):
                with col:
                    input_value = st.text_input(
                        f"Input {i}:", 
                        value=str(df.at[selected_row, f'Input{i}']),
                        key=f"input_{i}"
                    )
                    inputs.append(input_value)
            stdin_input = "\n".join(inputs)

        # Button Row: Compile & Run and Submit
        col3, col4 = st.columns(2)
        with col3:
            if st.button("Compile & Run"):
                # Encode the code and input to base64 as required by the API
                encoded_code = base64.b64encode(user_code.encode()).decode()
                encoded_stdin = base64.b64encode(stdin_input.encode()).decode()
                
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
                        expected_output = str(df.at[selected_row, 'Output']).strip()
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