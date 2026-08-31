from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from starter.agent import Agent


def _write_catalog(path: Path) -> None:
    rows = [
        {
            "parent_asin": "A",
            "title": "cotton shirt alpha",
            "features": ["cotton"],
            "details": {},
            "description": ["everyday cotton shirt"],
            "categories": ["Clothing"],
            "store": "X",
            "rating_number": 10,
        },
        {
            "parent_asin": "B",
            "title": "cotton shirt beta",
            "features": ["cotton"],
            "details": {},
            "description": ["everyday cotton shirt"],
            "categories": ["Clothing"],
            "store": "X",
            "rating_number": 100,
        },
        {
            "parent_asin": "C",
            "title": "cotton shirt gamma",
            "features": ["cotton"],
            "details": {},
            "description": ["everyday cotton shirt"],
            "categories": ["Clothing"],
            "store": "X",
            "rating_number": 50,
        },
        {
            "parent_asin": "D",
            "title": "tungsten widget uniquezz",
            "features": ["tungsten"],
            "details": {},
            "description": ["industrial widget uniquezz"],
            "categories": ["Tools"],
            "store": "X",
            "rating_number": 99999,
        },
    ]
    path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")


class ShippedAgentTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.catalog = Path(self.tmp.name) / "catalog.jsonl"
        _write_catalog(self.catalog)
        self.agent = Agent(self.catalog)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _asins(self, response: dict) -> list[str]:
        return [item["parent_asin"] for item in response["recommendations"]]

    def test_ask_attribute_is_other_every_turn(self) -> None:
        self.agent.reset("s", {})
        first = self.agent.respond("s", "cotton shirt", 1, 3)
        second = self.agent.respond("s", "still exploring more cotton", 2, 3)
        self.assertEqual(first["ask_attribute"], "other")
        self.assertEqual(second["ask_attribute"], "other")
        self.assertIsInstance(first["message"], str)
        self.assertTrue(first["message"])

    def test_accumulate_keeps_terms_from_both_messages(self) -> None:
        self.agent.reset("s", {})
        turn1 = self._asins(self.agent.respond("s", "tungsten widget uniquezz", 1, 3))
        self.assertIn("D", turn1)
        turn2 = self._asins(self.agent.respond("s", "cotton shirt", 2, 10))
        self.assertIn("D", turn2, "turn-1 terms must remain in the FTS query")
        self.assertTrue({"A", "B", "C"} & set(turn2), "turn-2 terms must enter the query")

    def test_reorder_scored_window_by_rating_number(self) -> None:
        self.agent.reset("s", {})
        order = self._asins(self.agent.respond("s", "cotton shirt", 1, 3))
        self.assertEqual(order, ["B", "C", "A"])

    def test_high_rating_outside_bm25_window_does_not_enter(self) -> None:
        self.agent.reset("s", {})
        order = self._asins(self.agent.respond("s", "cotton shirt", 1, 3))
        self.assertNotIn("D", order)
        self.assertEqual(len(order), 3)

    def test_dual_track_from_opening_message_not_scenario_field(self) -> None:
        self.agent.reset("browse", {})
        browse = self.agent.respond(
            "browse", "I'm looking for Jewelry Necklaces, but I'm still exploring.", 1, 3
        )
        self.agent.reset("buy", {})
        buy = self.agent.respond(
            "buy", "I'm looking for Jewelry Necklaces. A key requirement is: cotton.", 1, 3
        )
        self.assertIn("browsing", browse["message"].lower())
        self.assertNotIn("browsing", buy["message"].lower())
        self.assertIn("form one", browse["message"].lower())
        self.assertIn("examples", buy["message"].lower())
        self.assertEqual(browse["ask_attribute"], "other")
        self.assertEqual(buy["ask_attribute"], "other")


if __name__ == "__main__":
    unittest.main()
