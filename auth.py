import os
import json
import base64
import uuid
from dotenv import load_dotenv
from streamlit_oauth import OAuth2Component
import streamlit as st

# Load environment variables
load_dotenv()

# Get credentials from .env
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
AUTHORIZE_ENDPOINT = os.getenv("AUTHORIZE_ENDPOINT")
TOKEN_ENDPOINT = os.getenv("TOKEN_ENDPOINT")
REVOKE_ENDPOINT = os.getenv("REVOKE_ENDPOINT")
REDIRECT_URI = os.getenv("REDIRECT_URI")

# Function for Google OAuth authentication
def authenticate_user():
    if "email" not in st.session_state:
        # Create a button to start the OAuth2 flow
        oauth2 = OAuth2Component(CLIENT_ID, CLIENT_SECRET, AUTHORIZE_ENDPOINT, TOKEN_ENDPOINT, TOKEN_ENDPOINT, REVOKE_ENDPOINT)
        result = oauth2.authorize_button(
            name="Continue with Google",
            icon="https://www.google.com.tw/favicon.ico",
            redirect_uri=REDIRECT_URI,
            scope="openid email profile",
            key="google",
            extras_params={"prompt": "consent", "access_type": "offline"},
            use_container_width=True,
            pkce='S256',
        )
        
        if result:
            # Decode the id_token JWT and get user details
            id_token = result["token"]["id_token"]
            payload = id_token.split(".")[1]
            payload += "=" * (-len(payload) % 4)
            payload = json.loads(base64.b64decode(payload))
            
            st.session_state["email"] = payload["email"]
            st.session_state["user_name"] = payload["name"]
            st.session_state["token"] = result["token"]

            # Generate deterministic session ID from user ID
            st.session_state.session_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, payload["email"]))
            
            st.rerun()
