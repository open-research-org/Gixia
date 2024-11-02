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
            rx.heading(
                "Score the Papers",
                size="9",
                align="center",
            ),
            rx.text(
                "A platform to score the papers and share your reviews with the community.",
                size="3",
                color="gray",
                align="center",
            ),
            rx.input(
                placeholder="Input a paper title, arxiv link or arxiv id to get started",
                type="text",
                width="60%",
                height="40px",
                margin_top="10px",
            ),
            rx.link(
                rx.button("Go to", width="100px"),
                href="#",
                is_external=False,
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
            align="center",
        ),
        rx.logo(),
        size="3",
        background_color=rx.color("gold", 3)
    )


app = rx.App()
app.add_page(index)