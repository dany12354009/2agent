from typing import Callable, List, Optional

from .conversation import Conversation
from .messages import Message

StopCondition = Callable[[Message, List[Message]], bool]


class ConversationCoordinator:
    """Runs longer multi-turn exchanges between two agents."""

    def __init__(self, conversation: Conversation):
        self.conversation = conversation

    def run_dialogue(
        self,
        starter: str,
        responder: str,
        initial_prompt: str,
        max_turns: int = 10,
        stop_condition: Optional[StopCondition] = None,
    ) -> List[Message]:
        if max_turns < 1:
            raise ValueError("max_turns must be at least 1")

        transcript: List[Message] = []
        sender, receiver, prompt = starter, responder, initial_prompt

        for _ in range(max_turns):
            reply_text = self.conversation.send(sender, receiver, prompt)
            last_message = self.conversation.history[-1]
            transcript.append(last_message)
            if stop_condition and stop_condition(last_message, self.conversation.history):
                break
            sender, receiver, prompt = receiver, sender, reply_text
        return transcript
