# main.py
import streamlit as st
import pandas as pd
import json
import os

# Question Selector Functions
def load_questions():
    with open("../questions.json", "r") as f:
        data = json.load(f)
    return data

def get_questions_by_level(data, level):
    return [{"id": q["id"], "title": q["title"]} for q in data["problems"] if q["level"] == level]

def save_to_csv(filename, selected_questions):
    df = pd.DataFrame(selected_questions)
    df.to_csv(f"test/{filename}.csv", index=False)
    st.success(f"Selected questions saved to '{filename}.csv'.")

# CSV Manager Functions
def get_csv_files():
    return [f for f in os.listdir("test") if f.endswith('.csv')]

def preview_csv(file_name):
    file_path = os.path.join("test", file_name)
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
            st.write("### Preview of", file_name)
            st.dataframe(df, width=1200)
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
    else:
        st.error("File not found.")

def delete_csv(file_name):
    file_path = os.path.join("test", file_name)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            st.success(f"{file_name} has been deleted.")
            if st.session_state.get('previewed_file') == file_name:
                st.session_state.previewed_file = None
        except Exception as e:
            st.error(f"Error deleting file: {str(e)}")
    else:
        st.error("File not found.")

def main():
    st.title("Test Case Generator and Manager")

    # Initialize session states for CSV Manager
    if "previewed_file" not in st.session_state:
        st.session_state.previewed_file = None
    if "show_options" not in st.session_state:
        st.session_state.show_options = set()

    # Create two tabs for the different functionalities
    tab1, tab2 = st.tabs(["Question Selector", "CSV Manager"])

    # Question Selector Tab
    with tab1:
        st.header("Question Selector")
        
        # "Text Name" input for the CSV file name
        filename = st.text_input("Text Name", value="TestCase1")

        # Load and categorize questions by level
        data = load_questions()
        easy_questions = get_questions_by_level(data, "easy")
        medium_questions = get_questions_by_level(data, "medium")
        hard_questions = get_questions_by_level(data, "hard")

        st.subheader("Select Questions by Difficulty Level")

        # Multi-select dropdowns for each level
        selected_easy = st.multiselect("Easy Questions", 
                                     options=[q["title"] for q in easy_questions])
        selected_medium = st.multiselect("Medium Questions", 
                                       options=[q["title"] for q in medium_questions])
        selected_hard = st.multiselect("Hard Questions", 
                                     options=[q["title"] for q in hard_questions])

        # Collect selected questions with IDs
        selected_questions = []
        for question in easy_questions + medium_questions + hard_questions:
            if question["title"] in selected_easy + selected_medium + selected_hard:
                selected_questions.append({
                    "ID": question["id"], 
                    "Question Title": question["title"]
                })

        # Button to submit and save selection
        if st.button("Submit Selection"):
            if filename.strip() == "":
                st.warning("Please enter a valid filename.")
            elif selected_questions:
                save_to_csv(filename, selected_questions)
            else:
                st.warning("Please select at least one question before submitting.")

    # CSV Manager Tab
    with tab2:
        st.header("CSV File Management")
        
        with st.expander("Test Case Files", expanded=True):
            st.write("Available CSV files:")
            
            csv_files = get_csv_files()

            if csv_files:
                for file_name in csv_files:
                    cols = st.columns([8, 2])
                    with cols[0]:
                        st.write(f"**{file_name}**")
                    with cols[1]:
                        if st.button("Show Options", 
                                   key=f"options_{file_name}",
                                   on_click=lambda fname=file_name: st.session_state.show_options.add(fname) 
                                   if fname not in st.session_state.show_options 
                                   else st.session_state.show_options.remove(fname)):
                            pass

                    if file_name in st.session_state.show_options:
                        option_cols = st.columns(3)
                        with option_cols[0]:
                            if st.button("Preview", key=f"preview_{file_name}"):
                                st.session_state.previewed_file = file_name
                        with option_cols[1]:
                            if st.button("Trigger", key=f"trigger_{file_name}"):
                                st.info(f"Trigger clicked for {file_name}")
                        with option_cols[2]:
                            if st.button("Delete", key=f"delete_{file_name}"):
                                delete_csv(file_name)
                                if file_name in st.session_state.show_options:
                                    st.session_state.show_options.remove(file_name)
                                st.rerun()
            else:
                st.warning("No CSV files found in the directory.")

        if st.session_state.previewed_file:
            with st.container():
                preview_csv(st.session_state.previewed_file)
                if st.button("Clear Preview"):
                    st.session_state.previewed_file = None
                    st.rerun()

if __name__ == "__main__":
    main()