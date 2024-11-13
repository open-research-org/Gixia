from google.auth.transport import requests
from google.oauth2.id_token import verify_oauth2_token
import reflex as rx

from gixia.pages.react_oauth_google import get_client_id, GoogleOAuthProvider, GoogleLogin


class State(rx.State):

    input: str = ""

    def on_success(self, id_token: dict):
        print(
            verify_oauth2_token(
                id_token["credential"],
                requests.Request(),
                get_client_id(),
            )
        )

@rx.page(route="/")
def index() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading(
                "Rate the Papers",
                size="9",
                align="center",
            ),
            rx.text(
                "A platform to rate the papers and share your comments with the community.",
                size="3",
                color="gray",
                align="center",
            ),
            rx.input(
                placeholder="Input a paper title, arxiv link or arxiv id to get started",
                type="text",
                on_change=State.set_input,
                width="60%",
                height="40px",
                margin_top="10px",
            ),
            rx.link(
                rx.button("Go to", width="100px"),
                href=f"/paper/{State.input}",
                is_external=False,
            ),
            GoogleOAuthProvider.create(
                GoogleLogin.create(on_success=State.on_success),
                client_id=get_client_id(),
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
            align="center",
        ),
        rx.logo(),
        size="3",
        background_color=rx.color("gold", 3),
    )


app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com/css?family=Hanken+Grotesk",
    ],
    theme=rx.theme(
        accent_color="gold",
        gray_color="gray",
    ),
    style={
        "font-family": "Hanken Grotesk",
    }
)