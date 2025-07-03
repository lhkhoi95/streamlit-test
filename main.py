import streamlit as st
from simple_auth import google_login_button

# Page configuration
st.set_page_config(page_title="Sales Dashboard", layout="wide")

# Simple Google login
if google_login_button():
    st.title("🎯 Sales Performance Dashboard")
    st.success("Welcome to your dashboard!")
    
    # Your dashboard content goes here
    st.write("Dashboard content...")
else:
    st.title("Please login to continue")