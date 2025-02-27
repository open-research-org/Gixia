import os

from google.auth.transport import requests
from google.oauth2.id_token import verify_oauth2_token
import reflex as rx

from gixia.states.base_state import BaseState


class State(BaseState):

    def on_success(self, id_token: dict):
        user_info = verify_oauth2_token(
            id_token["credential"],
            requests.Request(),
            get_client_id(),
        )
        print(user_info)
        if user_info:
            email = user_info.get('email')
            name = user_info.get('name')
        self.is_logged_in = True

        # TODO: Add user to database if not exists
        # TODO: Save user id to base state

def get_client_id() -> str:
    return os.environ["GOOGLE_AUTH_CLIENT_ID"]

class GoogleOAuthProvider(rx.Component):
    library = "@react-oauth/google"
    tag = "GoogleOAuthProvider"

    client_id: rx.Var[str]


class GoogleLogin(rx.Component):
    library = "@react-oauth/google"
    tag = "GoogleLogin"

    on_success: rx.EventHandler[lambda data: [data]]

def login_button() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                "Login",
                background_color="transparent",
                border="none",
                color=rx.color_mode_cond(
                    light="black",
                    dark="white",
                ),
                cursor="pointer",
            ),
        ),
        rx.dialog.content(
            rx.vstack(
                GoogleOAuthProvider.create(
                    GoogleLogin.create(
                        on_success=State.on_success,
                    ),
                    client_id=get_client_id(),
                ),
                spacing="6",
                width="100%",
                align_items="center",
            ),
            max_width="400px",
        ),
    )