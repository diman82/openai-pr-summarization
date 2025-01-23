import os

import streamlit as st
from google.oauth2 import id_token
from google.auth.transport import requests

from authentication_engine.auth_engine_types import BaseAuth


# Google OAuth Authentication
class GoogleOauthAuthentication(BaseAuth):
    def __init__(self):
        super().__init__()
        self.client_id = os.getenv('CLIENT_ID')

    def authenticate(self, token) -> bool:
        # TODO: still not working, have to invest some time to fix this
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), self.client_id)
        if idinfo['aud'] != self.client_id:
            st.error('Invalid client ID or generated token')
            return False
        else:
            st.session_state["authentication_status"] = True
            return st.session_state["authentication_status"]
