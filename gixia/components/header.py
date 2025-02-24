import reflex as rx
from gixia.states.base_state import BaseState


def header() -> rx.Component:
    return rx.hstack(
        rx.spacer(),
        rx.link(
            rx.button(
                rx.cond(
                    BaseState.is_logged_in,
                    BaseState.user_name,
                    "Login"
                ),
                background_color="transparent",
                border="none",
                color=rx.color_mode_cond(
                    light="black",
                    dark="white",
                ),
                cursor="pointer",
            ),
            href="/profile",
            is_external=False,
        ),
        rx.color_mode.button(),
        spacing="2",
    )