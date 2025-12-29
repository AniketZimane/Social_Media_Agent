import streamlit as st

# Page config
st.set_page_config(
    page_title="Login Test", 
    layout="wide", 
    page_icon="🔐"
)

# Test authentication - this should show login page
try:
    from auth import auth_manager
    
    # This should show the login page if not authenticated
    if not auth_manager.require_auth():
        st.stop()
    
    # If we get here, user is authenticated
    st.success(f"✅ Successfully logged in as: {st.session_state.username}")
    st.write("🎉 Authentication is working correctly!")
    
    # Show logout button
    if st.button("🚪 Logout"):
        auth_manager.logout()

except Exception as e:
    st.error(f"❌ Error: {e}")
    st.write("Make sure MongoDB is running and dependencies are installed:")
    st.code("pip install pymongo")
    st.code("python test_mongodb.py")