import streamlit as st
from streamlit_ace import st_ace
import requests
import base64

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
    </style>
    """, 
    unsafe_allow_html=True
)

# Create two columns with different width ratios
col1, col2 = st.columns([2, 3])

# Left Column: Description and Examples
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

# Right Column: Code Editor and Run
with col2:
    st.write("### Code Editor")
    language = st.selectbox("Select Programming Language", ["python", "c_cpp", "java"], key="language")

    # Ace editor setup with fixed height
    user_code = st_ace(
        language=language,
        theme="dracula",
        placeholder="Write your code here...",
        keybinding="vscode",
        height=200,
        font_size=16,
        show_gutter=True,
        show_print_margin=False,
        wrap=True,
        auto_update=True,
        key="editor"
    )
    
    # Binary string inputs for test case
    a = st.text_input("Enter binary string a:", "11", help="Binary string input for variable 'a'")
    b = st.text_input("Enter binary string b:", "1", help="Binary string input for variable 'b'")
    stdin_input = f"{a}\n{b}"

    # Button Row: Compile & Run and Submit
    col3, col4 = st.columns(2)
    with col3:
        if st.button("Compile & Run"):
            # Encode the code and input to base64 as required by the API
            encoded_code = base64.b64encode(user_code.encode()).decode()
            encoded_stdin = base64.b64encode(stdin_input.encode()).decode()
            
            # Set language_id based on selected language
            language_id = 71 if language == "python" else 52 if language == "c_cpp" else 62  # IDs for Python, C++, Java
            
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
                    st.code(base64.b64decode(result["stdout"]).decode(), language="text")
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
            # Display the code from the editor
            st.code(user_code, language=language)

    # Divider for Test Cases section
    st.write("---")

    # Test Cases section
    st.write("### Test Cases")
    st.write("Example Inputs for Binary Addition")
