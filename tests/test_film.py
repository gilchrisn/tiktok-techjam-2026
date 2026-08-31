from __future__ import annotations

import json
import re
import subprocess
import unittest
from pathlib import Path

KIT = Path(__file__).resolve().parents[1]
DEMO = KIT / "deliver" / "demo.html"
PLAYER = KIT / "deliver" / "demo-player.js"

BEAT_ORDER = [
    "idea",
    "silent-slate",
    "session",
    "opposite-failure",
    "lines-meet",
    "adapter-score",
]


def _timeline() -> dict:
    html = DEMO.read_text(encoding="utf-8")
    match = re.search(
        r'<script type="application/json" id="film-timeline">\s*(\{.*?\})\s*</script>',
        html,
        re.S,
    )
    if not match:
        raise AssertionError("film-timeline JSON missing from demo.html")
    return json.loads(match.group(1))


class FilmContractTest(unittest.TestCase):
    def test_offline_and_dual_stream_markup(self) -> None:
        html = DEMO.read_text(encoding="utf-8")
        self.assertNotRegex(html, r"""https?://""")
        self.assertNotIn('type="module"', html)
        self.assertNotIn("import ", html)
        self.assertIn('id="stream-shopper"', html)
        self.assertIn('id="stream-eval"', html)
        self.assertIn('src="demo-player.js"', html)
        self.assertTrue(PLAYER.is_file())
        self.assertIn("Construction stage", html)
        self.assertIn("Adapter stage", html)
        self.assertIn("customer_reply", html)
        self.assertIn("user message", html)
        self.assertNotIn("storefront", html.lower())

    def test_theorems_on_matching_beats(self) -> None:
        html = DEMO.read_text(encoding="utf-8")
        data = _timeline()
        self.assertIn("Thm 1 silent slate", html)
        self.assertIn("Thm 2 other-dominance", html)
        self.assertIn("first-passage", html)
        self.assertIn("Thm 5 opening category", html)
        self.assertIn("within-10 pop", html)
        self.assertIn("400-pop", html)
        by_id = {b["id"]: json.dumps(b).lower() for b in data["beats"]}
        early = by_id["idea"] + by_id["silent-slate"] + by_id["session"]
        self.assertNotRegex(early, r"\bv0\b")
        self.assertIn("other-dominance", by_id["opposite-failure"])
        self.assertRegex(by_id["opposite-failure"], r"v0|0\.11")
        self.assertIn("within-10", by_id["lines-meet"])
        self.assertIn("adapter", by_id["adapter-score"])
        self.assertIn("0.84", by_id["adapter-score"])

    def test_timeline_six_beats_and_duration(self) -> None:
        data = _timeline()
        duration = data["duration"]
        self.assertGreaterEqual(duration, 150)
        self.assertLessEqual(duration, 180)
        ids = [beat["id"] for beat in data["beats"]]
        self.assertEqual(ids, BEAT_ORDER)
        starts = [beat["t"] for beat in data["beats"]]
        self.assertEqual(starts[0], 0)
        self.assertEqual(sorted(starts), starts)

    def test_space_toggles_pause_r_restarts(self) -> None:
        data = _timeline()
        payload = json.dumps({"duration": data["duration"], "beats": data["beats"]})
        script = f"""
const fs = require("fs");
eval(fs.readFileSync({json.dumps(str(PLAYER))}, "utf8"));
const timeline = {payload};
let queued = [];
const raf = (fn) => {{ queued.push(fn); return queued.length; }};
const caf = () => {{}};
const film = FilmPlayer.create({{ timeline: timeline, raf: raf, caf: caf, onTick: function(){{}} }});
film.play();
queued.shift()(0);
queued.shift()(500);
let st = film.getState();
if (st.paused) throw new Error("expected playing");
film.handleKey(" ");
st = film.getState();
if (!st.paused) throw new Error("Space should pause");
const tPaused = st.t;
film.handleKey(" ");
st = film.getState();
if (st.paused) throw new Error("Space should resume");
film.handleKey("R");
st = film.getState();
if (st.paused) throw new Error("R should play");
if (st.t !== 0) throw new Error("R should reset t=0, got " + st.t);
if (st.beat !== "idea") throw new Error("R should return to idea");
console.log("ok");
"""
        proc = subprocess.run(
            ["node", "-e", script],
            capture_output=True,
            text=True,
            cwd=str(KIT),
        )
        self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
        self.assertIn("ok", proc.stdout)


if __name__ == "__main__":
    unittest.main()
