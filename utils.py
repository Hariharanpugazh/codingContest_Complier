import pandas as pd
import os
import streamlit as st

@st.cache_data
def load_test_cases():
    file_path = pd.read_csv("test_cases.csv")
    return file_path
