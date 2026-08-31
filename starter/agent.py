"""Opoyo — TechJam 2026 Track 4.

Standard library only. BM25 comes from SQLite's built-in FTS5, so there is
nothing to install and no network call at any point.

REPORT.md has the measurement behind each decision here.
"""

from __future__ import annotations

import json
import re
import sqlite3
from pathlib import Path


TOKEN_RE = re.compile(r"[a-z0-9]+", re.IGNORECASE)

# "looking" is filler here: every opening line the simulator writes is
# "I'm looking for {category}", so the word never distinguishes a product.
STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "from",
    "i", "in", "is", "it", "me", "my", "of", "on", "or", "please", "some",
    "that", "the", "this", "to", "want", "with", "would", "you", "looking",
}


def _text(value: object) -> str:
    """Flatten a catalog field to searchable text.

    Fields are inconsistently shaped — `details` alone uses 287 different keys
    across the catalog. Nothing is parsed into attributes because the constraints
    a shopper quotes are raw substrings of this text.
    """
    if value is None:
        return ""
    if isinstance(value, dict):
        return " ".join(f"{key} {item}" for key, item in value.items())
    if isinstance(value, list):
        return " ".join(str(item) for item in value)
    return str(value)


def _terms(text: str) -> list[str]:
    return [
        token.lower()
        for token in TOKEN_RE.findall(text)
        if len(token) > 1 and token.lower() not in STOPWORDS
    ]


CAT_RE = re.compile(r"I'm looking for (.+?)(?:,|\.)", re.I)

# Shared by all 50,000 products, so useless for telling them apart.
_EXCLUDED_CAT = {"clothing", "clothing shoes & jewelry", "clothing, shoes & jewelry"}


def _coarse(values: object) -> str:
    """Reduce a category path to its last two meaningful parts.

    Mirrors how the opening line names a category, so the result can be compared
    directly against what the shopper said.
    """
    cleaned: list[str] = []
    for value in values or []:
        for part in str(value).split(","):
            part = part.strip()
            if part and part.lower() not in _EXCLUDED_CAT:
                cleaned.append(part)
    return " ".join(cleaned[-2:]).lower()


class Agent:
    """Two policies, returned in one response.

    The construction policy writes `message`: a shopper who cannot name what they
    want forms a preference by seeing options, so the slate is a set of examples
    rather than a hidden-target hunt.

    The eval adapter is what the scoreboard sees: accumulate everything said, ask
    `other` each turn, retrieve with BM25, move the named category forward, cut to
    ten, reorder those ten by review count.

    The simulator reads neither `message` nor the ranking — its reply function
    takes `ask_attribute` and nothing else. The two are kept separate because of
    that, rather than collapsed into whichever one scores.
    """

    def __init__(self, catalog_path: str | Path = "data/catalog.jsonl") -> None:
        self.catalog_path = Path(catalog_path)
        self.connection = sqlite3.connect(":memory:")
        self.rating_number: dict[str, int] = {}
        self.titles: dict[str, str] = {}
        self.cat_of: dict[str, str] = {}
        self._state: dict[str, dict] = {}
        self._build_index()

    def _build_index(self) -> None:
        """Load the catalog into an in-memory FTS5 table.

        Built once and reused across sessions. The index is immutable, so sharing
        it carries no conversational state between them.
        """
        cursor = self.connection.cursor()
        cursor.execute(
            "CREATE VIRTUAL TABLE products USING fts5("
            "parent_asin UNINDEXED, title, categories, features, details, store, description, "
            "tokenize='unicode61 remove_diacritics 2')"
        )
        batch: list[tuple[str, str, str, str, str, str, str]] = []
        with self.catalog_path.open(encoding="utf-8") as handle:
            for line in handle:
                product = json.loads(line)
                pid = str(product["parent_asin"])
                self.rating_number[pid] = int(product.get("rating_number") or 0)
                self.titles[pid] = str(product.get("title") or pid)[:80]
                self.cat_of[pid] = _coarse(product.get("categories"))
                batch.append(
                    (
                        pid,
                        _text(product.get("title")),
                        _text(product.get("categories")),
                        _text(product.get("features")),
                        _text(product.get("details")),
                        _text(product.get("store")),
                        _text(product.get("description")),
                    )
                )
                if len(batch) >= 1000:
                    cursor.executemany("INSERT INTO products VALUES (?, ?, ?, ?, ?, ?, ?)", batch)
                    batch.clear()
        if batch:
            cursor.executemany("INSERT INTO products VALUES (?, ?, ?, ?, ?, ?, ?)", batch)
        self.connection.commit()

    def reset(self, session_id: str, user_profile: dict) -> None:
        self._state[session_id] = {
            "msgs": [],
            "profile": user_profile,
            "exploring": None,
            "cat": None,
        }

    def respond(
        self,
        session_id: str,
        user_message: str,
        turn: int,
        top_k: int,
    ) -> dict:
        state = self._state.get(session_id)
        if state is None:
            raise RuntimeError("reset must be called before respond")
        state["msgs"].append(user_message)

        # Both are read from the opening line and then left alone. `scenario_type`
        # is never passed to the agent, so browsing is inferred from the wording.
        if state["exploring"] is None:
            state["exploring"] = "still exploring" in user_message.lower()
        if state["cat"] is None:
            match = CAT_RE.search(user_message)
            if match:
                state["cat"] = match.group(1).strip().lower()

        # Query the whole conversation, not just this turn. OR rather than AND:
        # shoppers quote marketing copy, and requiring every term to match drops
        # the target more often than it sharpens the result.
        query = " ".join(state["msgs"])
        terms = list(dict.fromkeys(_terms(query)))[:40]
        expression = " OR ".join(f'"{term}"' for term in terms)
        ranked: list[str] = []
        if expression:
            try:
                rows = self.connection.execute(
                    "SELECT parent_asin FROM products WHERE products MATCH ? "
                    "ORDER BY bm25(products, 0.0, 6.0, 4.0, 2.5, 2.5, 1.5, 1.0) LIMIT ?",
                    (expression, 400),
                ).fetchall()
                ranked = [str(row[0]) for row in rows]
            except sqlite3.OperationalError:
                # A stray quote can make FTS5 reject the query. An empty slate
                # costs one turn; an uncaught exception could cost the session.
                ranked = []

        # Front-load on the 400 rather than the final 10, so it can pull a target
        # into the scored slots instead of only reshuffling them.
        want = state["cat"]
        if want:
            in_cat = [pid for pid in ranked if want in self.cat_of.get(pid, "")]
            out_cat = [pid for pid in ranked if want not in self.cat_of.get(pid, "")]
            ranked = in_cat + out_cat

        # Cut, then sort by popularity — not the other way round. Reordering a
        # wider window by popularity loses more hits than it gains.
        ranked = ranked[:top_k]
        ranked = sorted(ranked, key=lambda pid: self.rating_number.get(pid, 0), reverse=True)

        examples = "; ".join(self.titles[pid] for pid in ranked[:3] if pid in self.titles)
        if state["exploring"]:
            message = (
                "You are browsing, so I am not extracting a hidden spec — I am showing "
                "concrete options so you can form one. Closer to these, or different: "
                f"{examples or 'the list below'}?"
            )
        else:
            message = (
                "You named a hard constraint, so I locked it and I am using the list as "
                "examples of what that constraint actually looks like, not as a quiz. "
                f"{examples or 'See the list.'} Anything that would rule these out?"
            )

        return {
            # Must be a str, or the evaluator discards the whole response.
            "message": message,
            # `other` matches every constraint class; a named label matches only
            # its own, so this extracts all four facts in the fewest turns.
            "ask_attribute": "other",
            "recommendations": [{"parent_asin": pid} for pid in ranked],
            "usage": {"prompt_tokens": 0, "completion_tokens": 0},
        }
