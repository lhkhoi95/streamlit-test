import streamlit as st
import json
import os
import pickle
import hashlib
from google_auth_oauthlib.flow import Flow

def google_login_button():
    """Simple Google login button with persistent authentication"""
    
    # Initialize session state
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.user_info = None
    
    # Check for persistent authentication
    def check_persistent_auth():
        try:
            if os.path.exists('.streamlit_auth'):
                with open('.streamlit_auth', 'rb') as f:
                    stored_data = pickle.load(f)
                    # Simple validation - in production, use proper token validation
                    if 'user_info' in stored_data and 'email' in stored_data['user_info']:
                        return stored_data['user_info']
        except:
            pass
        return None
    
    def save_persistent_auth(user_info):
        try:
            with open('.streamlit_auth', 'wb') as f:
                pickle.dump({'user_info': user_info}, f)
        except:
            pass
    
    def clear_persistent_auth():
        try:
            if os.path.exists('.streamlit_auth'):
                os.remove('.streamlit_auth')
        except:
            pass
    
    # Check for persistent auth if not already authenticated
    if not st.session_state.authenticated:
        persistent_user = check_persistent_auth()
        if persistent_user:
            st.session_state.authenticated = True
            st.session_state.user_info = persistent_user
    
    # If already authenticated, show user info
    if st.session_state.authenticated:
        st.success(f"Logged in as: {st.session_state.user_info.get('name', 'Unknown')}")
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.user_info = None
            clear_persistent_auth()
            # Clear any lingering OAuth parameters
            st.query_params.clear()
            st.rerun()
        return True
    
    # Load credentials
    try:
        with open('google_credentials.json', 'r') as f:
            credentials = json.load(f)
    except FileNotFoundError:
        st.error("google_credentials.json not found")
        return False
    
    # Create OAuth flow
    flow = Flow.from_client_config(
        credentials,
        scopes=['openid', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile'],
        redirect_uri='http://localhost:8502'
    )
    
    # Handle OAuth callback
    query_params = st.query_params
    if 'code' in query_params:
        try:
            # Clear the code parameter immediately to prevent reuse
            auth_code = query_params['code']
            st.query_params.clear()
            
            flow.fetch_token(code=auth_code)
            
            # Get user info
            import requests
            user_info_url = f"https://www.googleapis.com/oauth2/v2/userinfo?access_token={flow.credentials.token}"
            user_info = requests.get(user_info_url).json()
            
            st.session_state.authenticated = True
            st.session_state.user_info = user_info
            save_persistent_auth(user_info)  # Save for next visit
            st.rerun()
        except Exception as e:
            st.error(f"Authentication failed: {e}")
            # Clear parameters on error to allow retry
            st.query_params.clear()
            if st.button("Try Again"):
                st.rerun()
    
    # Show login button
    auth_url, _ = flow.authorization_url(access_type='offline', include_granted_scopes='true')
    
    if st.button("🔐 Sign in with Google", type="primary"):
        st.markdown(f'<meta http-equiv="refresh" content="0; url={auth_url}">', unsafe_allow_html=True)
    
    return False
