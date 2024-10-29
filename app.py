import streamlit as st
from streamlit_ace import st_ace

# Set page configuration to wide mode
st.set_page_config(layout="wide")

# Custom CSS for layout and border between columns
st.markdown(
    """
    <style>
    /* Set global font to Sans Serif */
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
        height=200,          # Set a fixed height in pixels
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
