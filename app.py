import streamlit as st

# Set page configuration as the first command
st.set_page_config(layout="wide", page_title="Code Practice Platform", page_icon="💻")

# The rest of your imports and code follows
from streamlit_ace import st_ace

# Set page configuration to wide mode
st.set_page_config(layout="wide")

# Custom CSS to adjust alignment and reduce spacing
st.markdown(
    """
    <style>
    /* Overall page layout adjustments */
    .css-1d391kg, .css-18e3th9 {
        padding: 1rem 2rem;
    }
    
    /* Left column layout adjustments */
    .left-column {
        padding-right: 2rem;
    }

    /* Right column layout adjustments */
    .right-column {
        padding-left: 2rem;
    }

    /* Streamlined layout for button rows */
    .stButton { 
        margin-top: 0.5rem;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# Page Title
st.title("67. Add Binary")

# Create two columns with different width ratios for layout
col1, col2 = st.columns([3, 2])

# Left Column for Description, Examples, and Constraints
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

    st.write("### Constraints")
    st.markdown("""
    - `1 <= a.length, b.length <= 10^4`
    - `a` and `b` consist only of `'0'` or `'1'` characters.
    - Each string does not contain leading zeros except for the zero itself.
    """)

# Right Column for Code Editor and Test Cases
with col2:
    # Code Editor
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
    
    # Button Row: Compile & Run and Submit
    col3, col4 = st.columns(2)
    with col3:
        if st.button("Compile & Run"):
            st.write("### Output:")
            # Placeholder output
            st.write("Compiled and ran the code. (Placeholder for actual output)")
    with col4:
        if st.button("Submit"):
            st.write("### Submitted Code:")
            # Display the code from the editor
            st.code(user_code, language=language)

    # Divider for Test Cases section
    st.write("---")

    # Test Cases
    st.write("### Test Cases")
    a = st.text_input("Enter binary string a:", "11", help="Binary string input for variable 'a'")
    b = st.text_input("Enter binary string b:", "1", help="Binary string input for variable 'b'")
    
    if st.button("Run Test Case"):
        # Binary addition logic
        def add_binary(a, b):
            return bin(int(a, 2) + int(b, 2))[2:]

        # Display result
        result = add_binary(a, b)
        st.write("**Output:**", result)
