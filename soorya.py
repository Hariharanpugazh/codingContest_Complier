import streamlit as st
from streamlit_ace import st_ace
import json
from api_handler import execute_code
from typing import Tuple, Optional


class StreamlitApp:
    def __init__(self):
        self.setup_page_config()
        self.load_custom_css()
        self.test_cases = None
    
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
        """Load test cases from JSON file with error handling."""
        try:
            with open("test_cases.json", "r") as f:
                self.test_cases = json.load(f)
            return True
        except FileNotFoundError:
            st.error("Error: test_cases.json file not found. Please ensure the file exists in the project directory.")
            return False
        except Exception as e:
            st.error(f"Error loading test cases: {str(e)}")
            return False


    def render_problem_details(self, selected_problem: dict):
        """Render the problem details section."""
        st.markdown('<div class="test-case-header">', unsafe_allow_html=True)
        st.markdown("### Problem Details")
        st.markdown(f'<div class="description-box">{selected_problem["description"]}</div>', 
                unsafe_allow_html=True)
        
        if "test_cases" in selected_problem:
            num_cases = len(selected_problem["test_cases"])
            st.markdown("#### Test Cases")
            st.markdown(f'<div class="description-box">Number of test cases: {num_cases}</div>', 
                    unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    def get_user_inputs(self, selected_problem: dict) -> Optional[str]:
        """Get and validate user inputs."""
        if "inputs" not in selected_problem:
            return ""
        
        num_inputs = len(selected_problem["inputs"])
        input_cols = st.columns(num_inputs)
        input_fields = []
        
        for i in range(1, num_inputs + 1):
            with input_cols[i - 1]:
                input_value = st.text_input(
                    f"Input {i}:",
                    value=str(selected_problem["inputs"][i - 1]),
                    key=f"input_{i}"
                )
                input_fields.append(input_value)
        
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

    def run_code(self, user_code: str, language: str, stdin_input: str, selected_problem: dict):
        """Execute the code and display results."""
        if not user_code.strip():
            st.error("Please enter code to execute.")
            return

        with st.spinner('Running your code...'):
            try:
                output, expected_output = execute_code(
                    user_code, language, stdin_input, selected_problem
                )
                self.display_output(output, expected_output)
            except Exception as e:
                st.error(f"Error executing code: {str(e)}")

    def main(self):
        """Main application flow."""
        if not self.load_data():
            return

        col1, col2 = st.columns([2, 3])

        with col1:
            st.markdown("### Test Cases")
            # Select problem from list of test cases
            selected_index = st.selectbox(
                "Select a problem to solve:",
                options=range(len(self.test_cases)),
                format_func=lambda x: f"Problem {self.test_cases[x]['problem_id']}: {self.test_cases[x]['description'][:50]}..."
            )
            selected_problem = self.test_cases[selected_index]
            st.session_state['selected_problem'] = selected_problem
            self.render_problem_details(selected_problem)

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
                key=f"editor_{selected_index}"
            )

            # Run each test case for the selected problem when the user clicks 'Compile & Run'
            if st.button("Compile & Run", key=f"run_{selected_index}"):
                results = []
                for i, case in enumerate(selected_problem["test_cases"]):
                    inputs = "\n".join(map(str, case["inputs"]))  # Join inputs for stdin
                    output, expected_output = execute_code(user_code, language, inputs, case)
                    results.append((output, expected_output))

                # Display test cases in tabs format
                st.markdown("### Testcase")
                test_case_tabs = st.tabs([f"Case {i+1}" for i in range(len(selected_problem["test_cases"]))])

                for i, tab in enumerate(test_case_tabs):
                    with tab:
                        case = selected_problem["test_cases"][i]
                        st.write(f"**Inputs:** {case['inputs']}")
                        st.write(f"**Expected Output:** {case['expected_output']}")

                        # Display program output and result verification
                        output, expected_output = results[i]
                        st.write("**Program Output:**")
                        st.code(output, language="text")

                        # Verification
                        if output == expected_output:
                            st.success("✅ Output matches expected result!")
                        else:
                            st.error("❌ Output doesn't match expected result")



if __name__ == "__main__":
    app = StreamlitApp()
    app.main()
