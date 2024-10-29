import streamlit as st
from streamlit_ace import st_ace
from typing import Optional
from api_handler import execute_code
from config import API_URL, QUERY_STRING
import json

class StreamlitApp:
    def __init__(self):
        self.setup_page_config()
        self.load_custom_css()
        self.problems = self.load_json_test_cases()
    
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
    
    @staticmethod
    def load_json_test_cases():
        """Load test cases from a JSON file."""
        try:
            with open("json/test_cases.json", "r") as file:
                data = json.load(file)
            return data.get("problems", [])
        except FileNotFoundError:
            st.error("Error: test_cases.json file not found. Please ensure the file exists in the project directory.")
            return []

    def render_problem_details(self, selected_problem_index: int):
        """Render the problem details section along with an example test case."""
        problem = self.problems[selected_problem_index]
        st.markdown('<div class="test-case-header">', unsafe_allow_html=True)
        st.markdown("### Problem Details")
        st.markdown(f'<div class="description-box">{problem["problem_statement"]}</div>', 
                   unsafe_allow_html=True)
        
        # Display first sample test case as an example
        st.markdown("### Example Test Case")
        example_case = problem["samples"][0]  # First sample as example
        st.write("#### Input")
        for key, value in example_case["input"].items():
            st.text(f"{key} = {value}")
        
        st.write("#### Expected Output")
        st.text(example_case["output"])

        st.markdown('</div>', unsafe_allow_html=True)

    def get_user_inputs(self, selected_problem_index: int) -> Optional[str]:
        """Get and validate user inputs."""
        problem = self.problems[selected_problem_index]
        example_case = problem["samples"][0]  # Use first sample as example
        
        input_fields = []
        for i, (key, value) in enumerate(example_case["input"].items()):
            input_value = st.text_input(
                f"Input {i + 1} ({key}):",
                value=str(value),
                key=f"input_{selected_problem_index}_{i}"
            )
            input_fields.append(input_value)
        
        return "\n".join(input_fields)

    def display_test_cases_section(self, selected_problem_index: int):
        """Display test cases dynamically with the status of execution."""
        st.markdown("### Testcase Results")

        if self.problems:
            samples = self.problems[selected_problem_index]["samples"]
            tabs = st.tabs([f"Case {i + 1}" for i in range(len(samples))])

            # Display initial input and expected output without result
            for i, sample in enumerate(samples):
                with tabs[i]:
                    st.write("#### Input")
                    for key, value in sample["input"].items():
                        st.text(f"{key} = {value}")

                    st.write("#### Expected Output")
                    st.text(f"{sample['output']}")

    def run_code(self, user_code: str, language: str, selected_problem_index: int):
        """Execute each test case one by one, dynamically updating each result."""
        if not user_code.strip():
            st.error("Please enter code to execute.")
            return

        samples = self.problems[selected_problem_index]["samples"]
        tabs = st.tabs([f"Case {i + 1}" for i in range(len(samples))])

        # Execute each test case and display result in the corresponding tab
        for i, sample in enumerate(samples):
            with tabs[i]:
                st.write("#### Input")
                for key, value in sample["input"].items():
                    st.text(f"{key} = {value}")

                st.write("#### Expected Output")
                st.text(f"{sample['output']}")

                # Prepare input and expected output for the test case
                stdin_input = "\n".join([str(value) for value in sample["input"].values()])
                expected_output = str(sample["output"])

                # Execute the code and display the output in real-time
                with st.spinner(f'Running test case {i + 1}...'):
                    try:
                        output, _ = execute_code(user_code, language, stdin_input, selected_problem_index, self.problems)
                        is_success = output.strip() == expected_output.strip()

                        # Display the result dynamically
                        st.write("#### Program Output")
                        st.text(output.strip())
                        if is_success:
                            st.success("✅ Output matches expected result!")
                        else:
                            st.error("❌ Output doesn't match expected result.")
                    except Exception as e:
                        st.error(f"Error executing test case {i + 1}: {str(e)}")

    def run_hidden_tests(self, user_code: str, language: str, selected_problem_index: int):
        """Run hidden test cases and display results."""
        hidden_samples = self.problems[selected_problem_index].get("hidden_samples", [])
        failed_count = 0

        for i, sample in enumerate(hidden_samples):
            stdin_input = "\n".join([str(value) for value in sample["input"].values()])
            expected_output = str(sample["output"])

            try:
                output, _ = execute_code(user_code, language, stdin_input, selected_problem_index, self.problems)
                if output.strip() != expected_output.strip():
                    failed_count += 1
            except Exception as e:
                failed_count += 1
                st.error(f"Error executing hidden test case {i + 1}: {str(e)}")

        if failed_count == 0:
            st.success("✅ All hidden test cases cleared!")
        else:
            st.error(f"❌ {failed_count} hidden test case(s) failed.")

    def main(self):
        """Main application flow."""
        col1, col2 = st.columns([2, 3])

        with col1:
            st.markdown("### Test Cases")
            selected_problem_index = st.selectbox(
                "Select a problem to solve:",
                options=range(len(self.problems)),
                format_func=lambda x: f"{self.problems[x]['title']}: {self.problems[x]['problem_statement'][:50]}..."
            )
            st.session_state['selected_problem_index'] = selected_problem_index
            self.render_problem_details(selected_problem_index)

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
                key=f"editor_{selected_problem_index}"
            )

            col2_1, col2_2 = st.columns(2)
            with col2_1:
                if st.button("Compile & Run", key=f"run_{selected_problem_index}"):
                    self.run_code(user_code, language, selected_problem_index)
            with col2_2:
                if st.button("Submit", key=f"submit_{selected_problem_index}"):
                    self.run_hidden_tests(user_code, language, selected_problem_index)

            # Display initial test cases without results only
            if not st.session_state.get(f"run_{selected_problem_index}"):
                self.display_test_cases_section(selected_problem_index)


if __name__ == "__main__":
    app = StreamlitApp()
    app.main()
