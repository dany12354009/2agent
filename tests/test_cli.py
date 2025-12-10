import unittest

from agent_platform.cli import build_default_conversation, render_history


class CLITests(unittest.TestCase):
    def test_default_agents_registered(self):
        conversation = build_default_conversation()
        for name in {"echo", "uppercase", "reverse", "counter"}:
            self.assertTrue(conversation.has_agent(name))

    def test_render_history_formats_table(self):
        conversation = build_default_conversation()
        conversation.send("echo", "uppercase", "hello")
        output = render_history(conversation.history)
        self.assertIn("echo -> uppercase", output)
        self.assertIn("uppercase -> echo", output)
        self.assertNotIn("No messages yet", output)

    def test_render_history_handles_empty(self):
        conversation = build_default_conversation()
        output = render_history(conversation.history)
        self.assertIn("No messages yet", output)


if __name__ == "__main__":
    unittest.main()
