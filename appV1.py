import streamlit as st
from streamlit_ace import st_ace
import requests
import base64

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
    </style>
    """, 
    unsafe_allow_html=True
)

# Judge0 API URL and headers
JUDGE0_API_URL = "https://judge029.p.rapidapi.com/submissions"
JUDGE0_API_KEY = "4c6f0f6fc5msh9ca8144c4f547fep16ac54jsndd5114267fd4"

# Mapping of languages for Judge0 (example: Python, C++, Java)
LANGUAGE_MAP = {
    "python": 71,   # Python 3
    "c_cpp": 52,    # C++
    "java": 62      # Java
}

# Function to submit code to Judge0 API and get the result
def compile_and_run_code(source_code, language_id, stdin_data):
    querystring = {"base64_encoded": "true", "wait": "true", "fields": "*"}
    payload = {
        "source_code": base64.b64encode(source_code.encode()).decode(),
        "language_id": language_id,
        "stdin": base64.b64encode(stdin_data.encode()).decode(),  # Encode stdin as base64
    }
    headers = {
        "x-rapidapi-key": JUDGE0_API_KEY,
        "x-rapidapi-host": "judge029.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    response = requests.post(JUDGE0_API_URL, json=payload, headers=headers, params=querystring)
    result = response.json()
    
    # Check for stdout, stderr, and compile_output in the response
    if 'stdout' in result and result['stdout']:
        return base64.b64decode(result['stdout']).decode()
    elif 'stderr' in result and result['stderr']:
        return f"Error:\n{base64.b64decode(result['stderr']).decode()}"
    elif 'compile_output' in result and result['compile_output']:
        return f"Compilation Error:\n{base64.b64decode(result['compile_output']).decode()}"
    else:
        return "No output received."


# Create two columns with different width ratios
col1, col2 = st.columns([2, 3])

# Left Column
with col1:
    st.write("### Description")
    st.write("Given two binary strings `a` and `b`, return their sum as a binary string.")

    st.write("### Examples")
    st.markdown("""
    **Example 1:**  
    Input: `a = "11"`, `b = "1"`  
    Output: `"100"`

    **Example 2:**  
    Input: `a = "1010"`, `b = "1011"`  
    Output: `"10101"`
    """)

# Right Column
with col2:
    st.write("### Code Editor")
    language = st.selectbox("Select Programming Language", ["python", "c_cpp", "java"], key="language")

    # Ace editor setup with fixed height
    user_code = st_ace(
        language=language,
        theme="dracula",
        placeholder="Write your code here...",
        keybinding="vscode",
        height=200,  # Fixed height with scroll bar
        font_size=16,
        show_gutter=True,
        show_print_margin=False,
        wrap=True,
        auto_update=True,
        key="editor"
    )

    # Test case input
    st.write("### Test Cases")
    a = st.text_input("Enter binary string a:", "11", help="Binary string input for variable 'a'")
    b = st.text_input("Enter binary string b:", "1", help="Binary string input for variable 'b'")

    # Combine test case input as stdin for the code
    stdin_data = f"{a}\n{b}"

    # Compile & Run button
    if st.button("Compile & Run"):
        st.write("### Output:")

        if user_code:
            # Send the code and stdin data to the Judge0 API
            language_id = LANGUAGE_MAP.get(language)
            output = compile_and_run_code(user_code, language_id, stdin_data)
            
            # Display the output
            st.write("**Program Output:**")
            st.code(output)
        else:
            st.write("Please enter code to compile and run.")

    # Submit button
    if st.button("Submit"):
        st.write("### Submitted Code:")
        # Display the code from the editor
        st.code(user_code, language=language)
