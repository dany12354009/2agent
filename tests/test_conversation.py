import unittest

from agent_platform import Agent, Conversation, ConversationCoordinator


def echo_handler(prompt, _history):
    return f"echo: {prompt}"


def summarizing_handler(prompt, history):
    prompts = [message.content for message in history if message.receiver]
    return f"received {len(prompts)} messages including '{prompt}'"


def stop_on_keyword(keyword: str):
    def _stop(message, _history):
        return keyword in message.content

    return _stop


class ConversationTests(unittest.TestCase):
    def setUp(self):
        self.conv = Conversation()
        self.conv.add_agent(Agent("alpha", echo_handler))
        self.conv.add_agent(Agent("beta", summarizing_handler))

    def test_round_trip_message(self):
        reply = self.conv.send("alpha", "beta", "hello")
        self.assertIn("hello", reply)
        self.assertEqual(len(self.conv.history), 2)
        self.assertEqual(self.conv.history[0].sender, "alpha")
        self.assertEqual(self.conv.history[1].sender, "beta")

    def test_unregistered_agent_raises(self):
        with self.assertRaises(ValueError):
            self.conv.send("gamma", "alpha", "who")
        with self.assertRaises(ValueError):
            self.conv.send("alpha", "gamma", "who")

    def test_handler_receives_history(self):
        self.conv.send("alpha", "beta", "first")
        reply = self.conv.send("alpha", "beta", "second")
        self.assertIn("3 messages", reply)

    def test_remove_and_readd_agent(self):
        self.conv.remove_agent("beta")
        with self.assertRaises(ValueError):
            self.conv.send("alpha", "beta", "noop")
        self.conv.add_agent(Agent("beta", summarizing_handler))
        self.assertTrue(self.conv.has_agent("beta"))

    def test_broadcast_sends_to_all(self):
        gamma = Agent("gamma", lambda prompt, history: f"got: {prompt} with {len(history)} entries")
        self.conv.add_agent(gamma)
        replies = self.conv.broadcast("alpha", "hi team")
        receiver_names = {message.sender for message in replies}
        self.assertSetEqual(receiver_names, {"beta", "gamma"})
        self.assertEqual(len(self.conv.history), 4)

    def test_coordinator_runs_multi_turn_dialogue(self):
        coordinator = ConversationCoordinator(self.conv)
        transcript = coordinator.run_dialogue("alpha", "beta", "start", max_turns=3)
        self.assertGreaterEqual(len(transcript), 1)
        self.assertEqual(transcript[-1].sender, "beta")
        self.assertEqual(len(self.conv.history), len(transcript) * 2)

    def test_coordinator_stops_on_condition(self):
        coordinator = ConversationCoordinator(self.conv)
        transcript = coordinator.run_dialogue(
            "alpha",
            "beta",
            "stop now",
            max_turns=5,
            stop_condition=stop_on_keyword("stop"),
        )
        self.assertEqual(len(transcript), 1)

    def test_handler_return_type_enforced(self):
        bad_agent = Agent("bad", lambda prompt, history: None)
        self.conv.add_agent(bad_agent)
        with self.assertRaises(TypeError):
            self.conv.send("alpha", "bad", "anything")


if __name__ == "__main__":
    unittest.main()
