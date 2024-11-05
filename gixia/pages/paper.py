import reflex as rx


@rx.page(route="/paper")
def paper() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.hstack(
            rx.vstack(
                rx.heading(
                    "Nova: An Iterative Planning and Search Approach to Enhance Novelty and Diversity of LLM Generated Ideas",
                    size="7",
                ),
                rx.text(
                    "Xiang Hu, Hongyu Fu, Jinge Wang, Yifeng Wang, Zhikun Li, Renjun Xu, Yu Lu, Yaochu Jin, Lili Pan, Zhenzhong Lan",
                    size="2",
                    color="gray",
                ),
                rx.text(
                    "Scientific innovation is pivotal for humanity, and harnessing large language"
                    "models (LLMs) to generate research ideas could transform discovery. "
                    "However, existing LLMs often produce simplistic and repetitive suggestions"
                    "due to their limited ability in acquiring external knowledge for innovation.",
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
        height="100vh",
        background_color=rx.color("gold", 3),
    )