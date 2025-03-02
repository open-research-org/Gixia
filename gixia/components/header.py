import reflex as rx
from gixia.states.base_state import BaseState
from gixia.components.login import login_button


def header() -> rx.Component:
    return rx.hstack(
        rx.spacer(),
        rx.cond(
            BaseState.user,
            rx.link(
                rx.button(
                    BaseState.user.name,
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
            # rx.button(
            #     "Login",
            #     background_color="transparent",
            #     border="none",
            #     color=rx.color_mode_cond(
            #         light="black",
            #         dark="white",
            #     ),
            #     cursor="pointer",
            #     on_click=LoginModalState.toggle_modal,
            # ),
            login_button(),
        ),
        rx.color_mode.button(),
        spacing="2",
    )