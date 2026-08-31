# Devpost — paste ready

**Project title:** Opoyo — two policies, one turn

**Tagline:** The ranking is how a shopper builds a preference. This evaluator cannot see
that. We built it anyway, and we play the scored game as a separate, honest adapter.

---

## How your solution addresses the problem statement

Track 4 asks for a shopping copilot and then scores a hidden product with Hit@10, MRR and
MTTC. Those two things are not the same problem, and our agent answers both separately.

A shopper who cannot name what they want builds a preference by seeing options. Showing
ten concrete items is therefore an act of elicitation, not a quiz. That claim is our
construction policy, and it lives in `message`, narrating the ranked titles as examples.

The official simulator never reads `message` or the ranking. Its reply function is
`customer_reply(sample, ask_attribute, disclosed, boundary_used)`, and the recommendations
are not an argument to it. The hidden product is fixed before turn one. Kim et al. (EMNLP
2025 Findings) call a simulator built this way a guessing game. We say so, using the
function signature as the evidence, and we still ship the construction policy because a
copilot is for people.

The eval adapter plays the scored game with four steps we measured one at a time. It asks
`other` every turn, because a named facet returns only its own slice while `other` covers
the whole set. It accumulates the dialogue, because asking without memory wastes the
answers. It pulls the category named in the shopper's first line to the front. It cuts to
ten and reorders those ten by review count.

Unmodified official evaluator, 200 public sessions: **Hit@10 0.915, MRR 0.750276,
MTTC 3.02, TechnicalScore 0.842183**. The official starter scores 0.10671. Zero tokens,
zero dollars, Python standard library only.

TechnicalScore is an input to Technical Execution, not the whole rubric. The reasoning
behind each step is in `REPORT.md`; the four evaluator properties the adapter relies on
are proved in `THEOREM.md`.

## Development tools used

VS Code and Cursor, Python 3.12, git, and the official participant-kit evaluator. Manim
for the architecture film. No notebooks.

## APIs used

None. No model API, no hosted reranker, no keys, no network at scoring time.

## Libraries and frameworks used

The Python standard library: `json`, `re`, `sqlite3`, `pathlib`. BM25 comes from SQLite's
built-in FTS5. Tests use `unittest`. The agent has no third-party dependencies and nothing
to install.

## Datasets and assets used

The frozen TechJam catalog of 50,000 `parent_asin` rows, derived from Amazon Reviews 2023
`Clothing_Shoes_and_Jewelry`, and the 200 public development sessions from the participant
kit. Attribution is in `DATA_ATTRIBUTION.md`. We used no external data.

## Video

YOUTUBE_URL

The video walks the geometry of the evaluator, then a complete multi-turn session, then a
live run of the official evaluator finishing on 0.842183.

## GitHub

GITHUB_URL

```bash
python3 -m evaluator.local_evaluator
```

Setup, catalog download and checksum are in the README. There are no environment
variables to set.

## Limitations

Reordering by review count is worth 0.053 of the score, and it may be measuring the
evaluation set rather than the shopper. Amazon targets sampled leave-last-out skew
popular, which makes a popularity prior look like skill. Cañamares and Castells set out
when that is real signal and when it is artifact in *Should I Follow the Crowd?* (SIGIR
2018). We report the gain and label the likely cause.

Seventeen public sessions still miss. In those, the listing text the shopper quotes is not
unique to one product, or BM25 never placed the target in the ten even under an oracle
query.

We did not build a neural reranker, so we claim no ablation against one. A peer's MiniLM
scored 0.64 on this task. Our reason for skipping the dependency is that `other` already
extracts all four constraints by turn three, and the remaining misses are generic listing
text rather than a ranking failure a cross-encoder would fix.

The construction policy cannot be measured on this harness, by design. We do not claim
0.842 on the private 800; that package is released after the deadline.

## Team member contributions

TEAM_PLACEHOLDER — one line each, naming what the person built.

## Built with

Python, SQLite FTS5, Manim, the official TechJam evaluator.
