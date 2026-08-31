from __future__ import annotations

import json
import re
import sqlite3
from pathlib import Path


TOKEN_RE = re.compile(r"[a-z0-9]+", re.IGNORECASE)
STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "from",
    "i", "in", "is", "it", "me", "my", "of", "on", "or", "please", "some",
    "that", "the", "this", "to", "want", "with", "would", "you", "looking",
}


def _text(value: object) -> str:
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
_EXCLUDED_CAT = {"clothing", "clothing shoes & jewelry", "clothing, shoes & jewelry"}


def _coarse(values: object) -> str:
    cleaned: list[str] = []
    for value in values or []:
        for part in str(value).split(","):
            part = part.strip()
            if part and part.lower() not in _EXCLUDED_CAT:
                cleaned.append(part)
    return " ".join(cleaned[-2:]).lower()


class Agent:
    """Two policies, one response.

    Construction policy (the idea): the slate is how a shopper *forms* a
    preference — examples, not a hidden-target hunt. It writes `message`.
    The simulator never reads `message` or the ranking.

    Eval adapter: accumulate text, ask `other`, BM25, bump the opening-template
    category to the front of the 400, cut to 10, reorder that 10 by review count.
    Buying vs browsing is inferred from the opening line, not `scenario_type`.
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
        if state["exploring"] is None:
            state["exploring"] = "still exploring" in user_message.lower()
        if state["cat"] is None:
            match = CAT_RE.search(user_message)
            if match:
                state["cat"] = match.group(1).strip().lower()

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
                ranked = []
        want = state["cat"]
        if want:
            in_cat = [pid for pid in ranked if want in self.cat_of.get(pid, "")]
            out_cat = [pid for pid in ranked if want not in self.cat_of.get(pid, "")]
            ranked = in_cat + out_cat
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
            "message": message,
            "ask_attribute": "other",
            "recommendations": [{"parent_asin": pid} for pid in ranked],
            "usage": {"prompt_tokens": 0, "completion_tokens": 0},
        }
