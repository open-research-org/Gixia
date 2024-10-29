"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config


class State(rx.State):
    """The app state."""

    ...


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Gixia", size="9", align="center"),
            rx.heading("A community to share your review of papers.", size="5"),
            rx.input(
                placeholder="Input a paper title, arxiv link or arxiv id to get started",
                type="text",
                width="50%",
                margin="10",
                align="center",
            ),
            rx.link(
                rx.button("Go to"),
                href="#",
                is_external=False,
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
        rx.logo()
    )


app = rx.App()
app.add_page(index)