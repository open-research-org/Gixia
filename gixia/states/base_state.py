import reflex as rx

class BaseState(rx.State):
    """Base state for sharing common state across pages."""
    user_name: str = ""
    is_logged_in: bool = False
