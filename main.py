import streamlit as st
from streamlit_ace import st_ace
import pandas as pd
from typing import Tuple, Optional
from utils import load_test_cases
from api_handler import execute_code
from config import API_URL, QUERY_STRING

class StreamlitApp:
    def __init__(self):
        self.setup_page_config()
        self.load_custom_css()
        self.df = None
    
    @staticmethod
    def setup_page_config():
        st.set_page_config(
            layout="wide",
            page_title="Code Practice Platform",
            page_icon="💻"
        )
    
    @staticmethod
    def load_custom_css():
        st.markdown("""
            <style>
            html, body, [class*="css"] {
                font-family: "Sans-serif";
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
            .output-container {
                margin-top: 1rem;
                padding: 1rem;
                border-radius: 0.5rem;
                border: 1px solid #e0e0e0;
            }
            .error-message {
                color: #ff4b4b;
                padding: 0.5rem;
                border-radius: 0.3rem;
            }
            .output-section {
                margin-top: 1rem;
                padding: 1rem;
                border-radius: 0.5rem;
                border: 1px solid #e0e0e0;
            }
            .output-comparison {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 1rem;
                margin-top: 1rem;
            }
            </style>
        """, unsafe_allow_html=True)
    
    def load_data(self) -> bool:
        """Load test cases with error handling."""
        try:
            self.df = load_test_cases()
            return True
        except FileNotFoundError:
            st.error("Error: testcases.csv file not found. Please ensure the file exists in the project directory.")
            return False
        except Exception as e:
            st.error(f"Error loading test cases: {str(e)}")
            return False

    def render_problem_details(self, selected_row: int):
        """Render the problem details section."""
        st.markdown('<div class="test-case-header">', unsafe_allow_html=True)
        st.markdown("### Problem Details")
        st.markdown(f'<div class="description-box">{self.df.at[selected_row, "Description"]}</div>', 
                   unsafe_allow_html=True)
        
        if self.df.at[selected_row, 'Has input']:
            num_inputs = int(self.df.at[selected_row, 'No of inputs'])
            st.markdown("#### Input Format")
            st.markdown(f'<div class="description-box">Number of inputs: {num_inputs}</div>', 
                       unsafe_allow_html=True)
            for i in range(1, num_inputs + 1):
                st.markdown(f'Input {i}: `{self.df.at[selected_row, f"Input{i}"]}`')
        
        st.markdown("#### Expected Output")
        st.markdown(f'<div class="description-box">{self.df.at[selected_row, "Output"]}</div>', 
                   unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    def get_user_inputs(self, selected_row: int) -> Optional[str]:
        """Get and validate user inputs."""
        if not self.df.at[selected_row, 'Has input']:
            return ""
        
        num_inputs = int(self.df.at[selected_row, 'No of inputs'])
        input_cols = st.columns(num_inputs)
        input_fields = []
        
        for i in range(1, num_inputs + 1):
            with input_cols[i - 1]:
                try:
                    default_value = str(int(float(self.df.at[selected_row, f'Input{i}'])))
                    input_value = st.text_input(
                        f"Input {i}:",
                        value=default_value,
                        key=f"input_{i}"
                    )
                    input_fields.append(input_value)
                except ValueError:
                    st.error(f"Invalid input format for Input {i}")
                    return None
        
        return "\n".join(input_fields)

    def display_output(self, output: str, expected_output: str):
        """Display the output and expected output in a formatted way."""
        st.markdown('<div class="output-section">', unsafe_allow_html=True)
        
        # Always display both outputs
        st.markdown("#### Program Output:")
        st.code(output, language="text")
        st.markdown("#### Expected Output:")
        st.code(expected_output, language="text")
        
        # Show match/mismatch status
        if output == expected_output:
            st.success("✅ Output matches expected result!")
        else:
            st.error("❌ Output doesn't match expected result")
        
        st.markdown('</div>', unsafe_allow_html=True)

    def run_code(self, user_code: str, language: str, stdin_input: str, selected_row: int):
        """Execute the code and display results."""
        if not user_code.strip():
            st.error("Please enter code to execute.")
            return

        with st.spinner('Running your code...'):
            try:
                output, expected_output = execute_code(
                    user_code, language, stdin_input, selected_row, self.df
                )
                self.display_output(output, expected_output)
            except Exception as e:
                st.error(f"Error executing code: {str(e)}")
    def display_test_cases_section(self):
        """Display the test cases section with multiple tabs."""
        st.markdown("### Testcase")
        
        # Create tabs for each test case
        tabs = st.tabs(["Case 1", "Case 2", "Case 3"])

        # Test case 1
        with tabs[0]:
            st.write("nums =")
            nums_1 = st.text_input("nums_case1", "[2, 7, 11, 15]", key="nums_case1")
            st.write("target =")
            target_1 = st.text_input("target_case1", "9", key="target_case1")
        
        # Test case 2
        with tabs[1]:
            st.write("nums =")
            nums_2 = st.text_input("nums_case2", "[1, 5, 3, 6]", key="nums_case2")
            st.write("target =")
            target_2 = st.text_input("target_case2", "8", key="target_case2")
        
        # Test case 3
        with tabs[2]:
            st.write("nums =")
            nums_3 = st.text_input("nums_case3", "[3, 2, 4]", key="nums_case3")
            st.write("target =")
            target_3 = st.text_input("target_case3", "6", key="target_case3")

    def main(self):
        """Main application flow."""
        if not self.load_data():
            return

        col1, col2 = st.columns([2, 3])

        with col1:
            st.markdown("### Test Cases")
            selected_row = st.selectbox(
                "Select a problem to solve:",
                options=range(len(self.df)),
                format_func=lambda x: f"Problem {self.df.at[x, 'S.no']}: {self.df.at[x, 'Description'][:50]}..."
            )
            st.session_state['selected_row'] = selected_row
            self.render_problem_details(selected_row)

        with col2:
            st.markdown("### Code Editor")
            language = st.selectbox(
                "Select Programming Language",
                ["python", "c_cpp", "java"],
                key="language"
            )
            
            user_code = st_ace(
                language=language,
                theme="dracula",
                placeholder="Write your code here...",
                height=400,
                font_size=16,
                auto_update=True,
                key=f"editor_{selected_row}"
            )
            
            stdin_input = self.get_user_inputs(selected_row)
            
            if stdin_input is not None:
                if st.button("Compile & Run", key=f"run_{selected_row}"):
                    self.run_code(user_code, language, stdin_input, selected_row)
            self.display_test_cases_section()
if __name__ == "__main__":
    app = StreamlitApp()
    app.main()