# 2agent

A minimal two-agent conversation platform. Agents are simple callables that receive a prompt and the full conversation history,
making it easy to script deterministic interactions or prototypes without external dependencies.

## Features
- Register lightweight agents implemented as Python callables.
- Send a message from one agent to another and automatically capture replies.
- Broadcast a prompt to all agents for quick fan-out behaviors.
- Inspect immutable conversation history for debugging or further processing.
- Run longer, alternating multi-turn dialogues with a built-in coordinator.

## Quickstart
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m unittest discover -s tests
```

### Basic usage
```python
from agent_platform import Agent, Conversation, ConversationCoordinator

def echo_handler(prompt, history):
    return f"echo: {prompt} (seen {len(history)} messages)"

def respond_all_caps(prompt, _history):
    return prompt.upper()

conversation = Conversation()
conversation.add_agent(Agent("alpha", echo_handler))
conversation.add_agent(Agent("beta", respond_all_caps))

reply = conversation.send("alpha", "beta", "hello")
print(reply)  # outputs: HELLO
print(conversation.history)
```

### Multi-turn coordination
```python
conversation = Conversation()
conversation.add_agent(Agent("alpha", echo_handler))
conversation.add_agent(Agent("beta", respond_all_caps))

coordinator = ConversationCoordinator(conversation)
coordinator.run_dialogue("alpha", "beta", "start", max_turns=5)
for message in conversation.history:
    print(message)
```

### Broadcast to multiple agents
```python
gamma = Agent("gamma", lambda prompt, history: f"saw {prompt} after {len(history)} entries")
conversation.add_agent(gamma)
all_replies = conversation.broadcast("alpha", "status check")
for reply in all_replies:
    print(reply)
```

## Running tests
The repository uses Python's built-in `unittest` module to avoid extra dependencies. Execute the full test suite with:

```bash
python -m unittest discover -s tests
```
