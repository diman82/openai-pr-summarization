import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import streamlit as st

from authentication_engine.auth_engine_types import BaseAuth


# Basic Authentication
class BasicAuthentication(BaseAuth):
    def __init__(self):
        super().__init__()

    def authenticate(self) -> bool:
        with open('.streamlit/config.yaml') as file:
            config = yaml.load(file, Loader=SafeLoader)

        authenticator = stauth.Authenticate(
            config['credentials'],
            config['cookie']['name'],
            config['cookie']['key'],
            config['cookie']['expiry_days'],
        )

        try:
            email_of_registered_user, \
                username_of_registered_user, \
                name_of_registered_user = authenticator.register_user(pre_authorized=config['pre-authorized']['emails'])
            if email_of_registered_user:
                st.success('User registered successfully')
        except Exception as e:
            st.error(e)

        if st.session_state["authentication_status"] == "":
            try:
                authenticator.login()
                authenticator.experimental_guest_login('Login with Google',
                                                       provider='google',
                                                       oauth2=config['oauth2'])
                authenticator.experimental_guest_login('Login with Microsoft',
                                                       provider='microsoft',
                                                       oauth2=config['oauth2'])
            except Exception as e:
                st.error(e)
        else:
            return False

        if st.session_state["authentication_status"]:
            authenticator.logout()
            st.write(f'Welcome *{st.session_state["name"]}*')
        elif st.session_state['authentication_status'] is False:
            st.error('Username/password is incorrect')
        elif st.session_state['authentication_status'] is None:
            st.warning('Please enter your username and password')
        return st.session_state["authentication_status"]
