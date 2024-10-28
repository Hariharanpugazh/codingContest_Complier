import pandas as pd
import os
import streamlit as st

@st.cache_data
def load_test_cases():
    file_path = os.path.join(os.path.dirname(__file__), 'test_cases.csv')
    return pd.read_csv(file_path)
