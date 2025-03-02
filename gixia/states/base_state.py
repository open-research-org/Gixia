import reflex as rx

from gixia.core.user import User


class BaseState(rx.State):
    """Base state for sharing common state across pages."""
    user: User = None