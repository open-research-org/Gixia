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
            ),
            rx.vstack(
                rx.heading(
                    "9.1",
                    size="9",
                    align="center",
                    justify="center",
                    margin="20px",
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
                width="50%",
                margin="40px",
                align="center",
            ),
        ),
        size="3",
        height="100vh",
        background_color=rx.color("gold", 3),
    )