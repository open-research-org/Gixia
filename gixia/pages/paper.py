import reflex as rx

from gixia.components.header import header
from gixia.core.service import service
from gixia.states.base_state import BaseState


class State(BaseState):

    arxiv_id: str = ""
    title: str = ""
    authors: str = ""
    abstract: str = ""

    def on_load(self):
        self.arxiv_id = self.router.page.params.get("_arxiv_id")
        paper = service.get_paper(self.arxiv_id)
        if paper:
            self.title = paper['title']
            self.authors = paper['authors']
            self.abstract = paper['abstract']

@rx.page(route="/paper/[_arxiv_id]", on_load=State.on_load)
def paper() -> rx.Component:
    return rx.container(
        header(),
        rx.hstack(
            rx.vstack(
                rx.heading(
                    State.title,
                    size="7",
                ),
                rx.text(
                    State.authors,
                    size="2",
                    color="gray",
                ),
                rx.text(
                    State.abstract,
                    size="3",
                    color=rx.color("black", 8),
                ),
                width="50%",
                margin="40px",
                margin_right="0px",
            ),
            rx.vstack(
                rx.heading(
                    "9.1",
                    font_family="Hanken Grotesk",
                    font_size="100px",
                    align="center",
                    justify="center",
                    margin="50px",
                ),
                rx.hstack(
                    rx.button(
                        "Want to Read",
                        size="3",
                    ),
                    rx.button(
                        "Mark as Read",
                        size="3",
                    ),
                    align="center",
                    margin="20px",
                ),
                rx.hstack(
                    rx.text("9", width="10%", align="center", size="1"),
                    rx.vstack(
                        rx.heading("Jinge Wang", size="1"),
                        rx.text(
                            "Good work!",
                            size="1",
                        ),
                        width="90%",
                    ),
                    width="100%",
                ),
                width="50%",
                margin="40px",
                align="center",
            ),
            margin_top="50px",
        ),
        size="4",
        background_color=rx.color("gold", 3),
    )