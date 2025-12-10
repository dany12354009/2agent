from typing import Callable, Iterable, List

from .messages import Message


class Agent:
    """Simple agent wrapper around a callable handler."""

    def __init__(self, name: str, handler: Callable[[str, Iterable[Message]], str]):
        if not name:
            raise ValueError("Agent name must be a non-empty string")
        self.name = name
        self._handler = handler

    def respond(self, prompt: str, history: List[Message]) -> str:
        reply = self._handler(prompt, history)
        if not isinstance(reply, str):
            raise TypeError("Agent handlers must return string responses")
        return reply
