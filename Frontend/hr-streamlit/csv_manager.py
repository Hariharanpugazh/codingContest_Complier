import streamlit as st
import os
import pandas as pd

# Directory path where CSV files are stored
CSV_DIRECTORY = "test"

# Load all CSV files in the specified directory
def get_csv_files():
    return [f for f in os.listdir(CSV_DIRECTORY) if f.endswith('.csv')]

# Display preview of the selected CSV file
def preview_csv(file_name):
    file_path = os.path.join(CSV_DIRECTORY, file_name)
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
            st.write("### Preview of", file_name)
            st.dataframe(df, width=1200)  # Display the dataframe in a wide format
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
    else:
        st.error("File not found.")

# Delete the selected CSV file
def delete_csv(file_name):
    file_path = os.path.join(CSV_DIRECTORY, file_name)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            st.success(f"{file_name} has been deleted.")
            # Reset the preview if we just deleted the file being previewed
            if st.session_state.previewed_file == file_name:
                st.session_state.previewed_file = None
        except Exception as e:
            st.error(f"Error deleting file: {str(e)}")
    else:
        st.error("File not found.")

# Main function for the Streamlit app
def main():
    st.title("CSV File Management")

    # Initialize session state for previewed_file if it doesn't exist
    if "previewed_file" not in st.session_state:
        st.session_state.previewed_file = None

    # Initialize session state for showing options
    if "show_options" not in st.session_state:
        st.session_state.show_options = set()

    # Create a collapsible container for the Test Case section
    with st.expander("Test Case", expanded=True):
        st.write("Click below to view available CSV files:")
        
        # Get list of CSV files in the directory
        csv_files = get_csv_files()

        if csv_files:
            # Loop through each CSV file
            for file_name in csv_files:
                # Create a row to display the file name and show options button
                cols = st.columns([8, 2])
                with cols[0]:
                    st.write(f"**{file_name}**")
                with cols[1]:
                    # Use a unique key for each button
                    if st.button("Show Options", 
                               key=f"options_{file_name}",
                               on_click=lambda fname=file_name: st.session_state.show_options.add(fname) 
                               if fname not in st.session_state.show_options 
                               else st.session_state.show_options.remove(fname)):
                        pass

                # Display the option buttons if this file's options should be shown
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
                            # Remove from show_options if it was being shown
                            if file_name in st.session_state.show_options:
                                st.session_state.show_options.remove(file_name)
                            st.rerun()

        else:
            st.warning("No CSV files found in the directory.")

    # Display the preview of the selected file in a separate container
    if st.session_state.previewed_file:
        with st.container():
            preview_csv(st.session_state.previewed_file)
            # Add a button to clear the preview
            if st.button("Clear Preview"):
                st.session_state.previewed_file = None
                st.rerun()

if __name__ == "__main__":
    main()