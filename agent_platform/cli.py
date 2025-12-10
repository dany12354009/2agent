"""Text-first CLI for interacting with the conversation platform.

The CLI keeps dependencies minimal and relies only on the Python standard
library. It offers both single-command execution via ``argparse`` and an
interactive REPL with a lightweight text UI to inspect message history.
"""

from __future__ import annotations

import argparse
import shlex
from typing import Iterable, List, Sequence

from .agent import Agent
from .conversation import Conversation
from .coordinator import ConversationCoordinator
from .messages import Message


def build_default_conversation() -> Conversation:
    """Create a conversation preloaded with a few useful agents."""

    conversation = Conversation()

    conversation.add_agent(
        Agent("echo", lambda prompt, history: f"echo: {prompt} (seen {len(history)} messages)")
    )
    conversation.add_agent(Agent("uppercase", lambda prompt, _history: prompt.upper()))
    conversation.add_agent(Agent("reverse", lambda prompt, _history: prompt[::-1]))

    def counting_handler():
        counter = 0

        def _handler(prompt: str, _history: List[Message]) -> str:
            nonlocal counter
            counter += 1
            return f"#{counter}: {prompt}"

        return _handler

    conversation.add_agent(Agent("counter", counting_handler()))
    return conversation


def render_history(history: Iterable[Message]) -> str:
    """Return a compact text table summarizing the conversation history."""

    rows = list(history)
    if not rows:
        return "No messages yet. Use send, broadcast, or dialogue to create activity."

    header = f"{'Time (UTC)':10} | {'Route':22} | Content"
    divider = "-" * len(header)
    output = [header, divider]

    for message in rows:
        receiver = message.receiver or "broadcast"
        route = f"{message.sender} -> {receiver}"
        timestamp = message.timestamp.strftime("%H:%M:%S")
        output.append(f"{timestamp:10} | {route:22} | {message.content}")

    return "\n".join(output)


def _start_repl(conversation: Conversation) -> None:
    print("Type 'help' for commands, 'exit' to quit. Built-in agents: echo, uppercase, reverse, counter.")
    coordinator = ConversationCoordinator(conversation)

    while True:
        try:
            raw = input("2agent> ").strip()
        except (KeyboardInterrupt, EOFError):
            print()
            break

        if not raw:
            continue

        if raw.lower() in {"exit", "quit"}:
            break

        if raw.lower() == "help":
            print(
                "Available commands:\n"
                "  send <sender> <receiver> <message>   - send message between agents\n"
                "  broadcast <sender> <message>         - send to all other agents\n"
                "  dialogue <starter> <responder> <prompt> [turns] - run alternating exchange\n"
                "  history                              - show message table\n"
                "  clear                                - clear history\n"
                "  agents                               - list registered agents\n"
                "  exit | quit                          - leave the REPL"
            )
            continue

        parts = shlex.split(raw)
        command, *args = parts

        try:
            if command == "send" and len(args) >= 3:
                sender, receiver, message = args[0], args[1], " ".join(args[2:])
                conversation.send(sender, receiver, message)
                print(render_history(conversation.history))
            elif command == "broadcast" and len(args) >= 2:
                sender, message = args[0], " ".join(args[1:])
                conversation.broadcast(sender, message)
                print(render_history(conversation.history))
            elif command == "dialogue" and len(args) >= 3:
                starter, responder, prompt, *rest = args
                turns = int(rest[0]) if rest else 6
                coordinator.run_dialogue(starter, responder, prompt, max_turns=turns)
                print(render_history(conversation.history))
            elif command == "history":
                print(render_history(conversation.history))
            elif command == "clear":
                conversation.clear_history()
                print("History cleared.")
            elif command == "agents":
                print("Registered agents:", ", ".join(conversation.agent_names))
            else:
                print("Unrecognized command. Type 'help' for guidance.")
        except Exception as exc:  # noqa: BLE001 - bubble readable error to the CLI
            print(f"Error: {exc}")


def _run_send(conversation: Conversation, sender: str, receiver: str, message: str) -> None:
    conversation.send(sender, receiver, message)
    print(render_history(conversation.history))


def _run_broadcast(conversation: Conversation, sender: str, message: str) -> None:
    conversation.broadcast(sender, message)
    print(render_history(conversation.history))


def _run_dialogue(
    conversation: Conversation, starter: str, responder: str, prompt: str, turns: int
) -> None:
    coordinator = ConversationCoordinator(conversation)
    coordinator.run_dialogue(starter, responder, prompt, max_turns=turns)
    print(render_history(conversation.history))


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Text-based UI for the 2agent platform")
    subparsers = parser.add_subparsers(dest="command", required=True)

    send_parser = subparsers.add_parser("send", help="send a single message between agents")
    send_parser.add_argument("sender")
    send_parser.add_argument("receiver")
    send_parser.add_argument("message", help="message content")

    broadcast_parser = subparsers.add_parser("broadcast", help="broadcast a message to all other agents")
    broadcast_parser.add_argument("sender")
    broadcast_parser.add_argument("message")

    dialogue_parser = subparsers.add_parser("dialogue", help="run a multi-turn exchange between two agents")
    dialogue_parser.add_argument("starter")
    dialogue_parser.add_argument("responder")
    dialogue_parser.add_argument("prompt")
    dialogue_parser.add_argument("--turns", type=int, default=6, dest="turns")

    subparsers.add_parser("repl", help="launch an interactive REPL with a simple text UI")

    return parser


def main(argv: Sequence[str] | None = None) -> None:
    parser = _build_parser()
    args = parser.parse_args(argv)

    conversation = build_default_conversation()

    if args.command == "send":
        _run_send(conversation, args.sender, args.receiver, args.message)
    elif args.command == "broadcast":
        _run_broadcast(conversation, args.sender, args.message)
    elif args.command == "dialogue":
        _run_dialogue(conversation, args.starter, args.responder, args.prompt, args.turns)
    elif args.command == "repl":
        _start_repl(conversation)
    else:  # pragma: no cover - argparse ensures command presence
        parser.error("Unknown command")


if __name__ == "__main__":  # pragma: no cover
    main()
