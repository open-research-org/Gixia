import os

from google.auth.transport import requests
from google.oauth2.id_token import verify_oauth2_token
import logging
import reflex as rx

from gixia.core.service import service
from gixia.states.base_state import BaseState


logger = logging.getLogger(__name__)

class State(BaseState):

    def on_success(self, id_token: dict):
        google_info = verify_oauth2_token(
            id_token["credential"],
            requests.Request(),
            get_client_id(),
        )
        if google_info:
            email = google_info.get('email')
            name = google_info.get('name')
            service.login_with_google(email, name, google_info)
            BaseState.user = service.login_with_google(email, name, google_info)
            if BaseState.user:
                logger.info(f"User ({email}, {name}) logged in successfully.")
                print(f"User ({email}, {name}) logged in successfully.")

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