import streamlit as st
from streamlit_ace import st_ace
import pandas as pd
from utils import load_test_cases
from api_handler import execute_code
from config import API_URL, QUERY_STRING

# Set page configuration to wide mode
st.set_page_config(layout="wide")

# Custom CSS for layout and border between columns
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: "Sans-serif";
    }
    .left-column { padding-right: 1rem; border-right: 2px solid #3E3E3E; }
    .right-column { padding-left: 1.5rem; }
    .stButton { margin-top: 0.5rem; }
    .test-case-header { padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem; }
    .description-box { padding: 1rem; border-radius: 0.5rem; border: 1px solid #e0e0e0; margin-bottom: 1rem; }
    </style>
""", unsafe_allow_html=True)

# Create two columns with different width ratios
col1, col2 = st.columns([2, 3])

try:
    # Load test cases
    df = load_test_cases()
    
    # Left Column: Test Cases
    with col1:
        st.markdown("### Test Cases")
        selected_row = st.selectbox(
            "Select a problem to solve:",
            options=range(len(df)),
            format_func=lambda x: f"Problem {df.at[x, 'S.no']}: {df.at[x, 'Description']}"
        )
        st.session_state['selected_row'] = selected_row
        
        # Display selected test case details
        st.markdown('<div class="test-case-header">', unsafe_allow_html=True)
        st.markdown("### Problem Details")
        st.markdown(f'<div class="description-box">{df.at[selected_row, "Description"]}</div>', unsafe_allow_html=True)
        
        # Display number of inputs and expected output
        if df.at[selected_row, 'Has input']:
            st.markdown(f'<div class="description-box">{int(df.at[selected_row, "No of inputs"])}</div>', unsafe_allow_html=True)
            num_inputs = int(df.at[selected_row, 'No of inputs'])
            for i in range(1, num_inputs + 1):
                st.write(f"Input {i}: {df.at[selected_row, f'Input{i}']}")
        
        st.markdown(f'<div class="description-box">{df.at[selected_row, "Output"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Right Column: Code Editor and Run
    with col2:
        st.markdown("### Code Editor")
        language = st.selectbox("Select Programming Language", ["python", "c_cpp", "java"], key="language")
        
        # Code editor
        user_code = st_ace(
            language=language,
            theme="dracula",
            placeholder="Write your code here...",
            height=300,
            font_size=16
        )
        
        # Dynamic input fields for user input based on No of inputs
        selected_row = st.session_state.get('selected_row', 0)
        stdin_input = ""
        if df.at[selected_row, 'Has input']:
            num_inputs = int(df.at[selected_row, 'No of inputs'])
            
            # Arrange inputs in columns to match your UI
            input_cols = st.columns(num_inputs)
            input_fields = []
            for i in range(1, num_inputs + 1):
                with input_cols[i - 1]:
                    input_value = st.text_input(
                        f"Input {i}:",
                        value=str(df.at[selected_row, f'Input{i}']),
                        key=f"input_{i}"
                    )
                    input_fields.append(input_value)
            stdin_input = "\n".join(input_fields)

        # Compile & Run button
        if st.button("Compile & Run"):
            output, expected_output = execute_code(user_code, language, stdin_input, selected_row, df)
            st.write("### Output:")
            if output == expected_output:
                st.success("✅ Output matches expected result!")
            else:
                st.error("❌ Output doesn't match expected result")
            st.code(output, language="text")

except FileNotFoundError:
    st.error("Error: testcases.csv file not found.")
except Exception as e:
    st.error(f"Error loading test cases: {e}")
