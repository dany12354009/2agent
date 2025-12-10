from typing import Dict, Iterable, List, Optional

from .agent import Agent
from .messages import Message


class Conversation:
    """Coordinates message exchange between registered agents."""

    def __init__(self):
        self._agents: Dict[str, Agent] = {}
        self._history: List[Message] = []

    @property
    def history(self) -> List[Message]:
        return list(self._history)

    @property
    def agent_names(self) -> List[str]:
        return sorted(self._agents)

    def add_agent(self, agent: Agent) -> None:
        if agent.name in self._agents:
            raise ValueError(f"Agent '{agent.name}' is already registered")
        self._agents[agent.name] = agent

    def remove_agent(self, name: str) -> None:
        if name not in self._agents:
            raise ValueError(f"Agent '{name}' is not registered")
        del self._agents[name]

    def has_agent(self, name: str) -> bool:
        return name in self._agents

    def _validate_sender_receiver(self, sender: str, receiver: Optional[str]) -> None:
        if sender not in self._agents:
            raise ValueError(f"Sender '{sender}' is not registered")
        if receiver is not None and receiver not in self._agents:
            raise ValueError(f"Receiver '{receiver}' is not registered")

    def send(self, sender: str, receiver: str, content: str) -> str:
        self._validate_sender_receiver(sender, receiver)

        outgoing = Message(sender=sender, receiver=receiver, content=content)
        self._history.append(outgoing)

        reply_text = self._agents[receiver].respond(content, list(self._history))
        reply = Message(sender=receiver, receiver=sender, content=reply_text)
        self._history.append(reply)
        return reply_text

    def broadcast(self, sender: str, content: str) -> List[Message]:
        """Send the same content to every registered agent except the sender."""

        self._validate_sender_receiver(sender, None)
        replies: List[Message] = []
        for receiver in self._agents:
            if receiver == sender:
                continue
            outgoing = Message(sender=sender, receiver=receiver, content=content)
            self._history.append(outgoing)
            reply_text = self._agents[receiver].respond(content, list(self._history))
            reply = Message(sender=receiver, receiver=sender, content=reply_text)
            self._history.append(reply)
            replies.append(reply)
        return replies

    def clear_history(self) -> None:
        self._history.clear()

    def iter_history(self) -> Iterable[Message]:
        return iter(self._history)
