import streamlit as st
import pandas as pd
from streamlit_ace import st_ace

# Set page configuration to wide mode
st.set_page_config(layout="wide")

# Load CSV file
csv_file_path = 'prob.csv'  # Replace with the path to your CSV file
df = pd.read_csv(csv_file_path)



def display_test_case(row):
    # Display the description
    st.write("### Description")
    st.write(row['Description'])
    
    # Initialize stdin_data to collect input values
    stdin_data = ""

    # Check if input is available
    if row.get('Input available') == 'Yes':
        # Get the number of inputs and display them dynamically
        num_inputs = int(row['No.of.inputs'])
        inputs = []
        
        for i in range(1, num_inputs + 1):
            # Dynamically get the input columns (A, B, C, etc.)
            column_name = chr(64 + i)  # ASCII code: 65 is 'A', 66 is 'B', etc.
            input_value = row.get(column_name, '')  # Get value for the column if exists
            inputs.append(st.text_input(f"Input {i}:", value=input_value))
        
        # Join all inputs with newline to pass to the program
        stdin_data = '\n'.join(inputs)
    
    # If 'Input available' is not 'Yes', no inputs are shown
    else:
        st.write("No input required for this test case.")
    
    return stdin_data

# Page title
st.title("Code Testing with CSV-based Test Cases")

# Dropdown to select test case by S.no
st.write("Select S.no")
sno = st.selectbox("S.no", df['S.no'].unique())

# Filter the dataframe to get the row for the selected S.no
selected_row = df[df['S.no'] == sno].iloc[0]
stdin_data = display_test_case(selected_row)

# Code editor
st.write("### Code Editor")
language = st.selectbox("Select Programming Language", ["python", "c_cpp", "java"], key="language")

# Ace editor setup
user_code = st_ace(
    language=language,
    theme="dracula",
    placeholder="Write your code here...",
    keybinding="vscode",
    min_lines=15,
    font_size=16,
    show_gutter=True,
    show_print_margin=False,
    wrap=True,
    auto_update=True,
    key="editor"
)

# Run the code with the test case inputs
if st.button("Compile & Run"):
    st.write("### Output:")
    if user_code:
        # Placeholder for actual execution logic
        st.write("Running code with provided inputs...")
        st.write("Program Output:")
        st.code("Example output from the program")
    else:
        st.write("Please enter code to compile and run.")
