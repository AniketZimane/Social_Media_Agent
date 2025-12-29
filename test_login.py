import streamlit as st
from auth import auth_manager

# Page config
st.set_page_config(
    page_title="Login Test", 
    layout="wide", 
    page_icon="🔐"
)

# Test authentication
if not auth_manager.require_auth():
    st.stop()

# If authenticated, show success message
st.success(f"✅ Successfully logged in as: {st.session_state.username}")
st.write("🎉 Authentication is working correctly!")

# Show logout button
if st.button("🚪 Logout"):
    auth_manager.logout()