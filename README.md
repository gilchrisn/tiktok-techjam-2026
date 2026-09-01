# Opoyo — TechJam 2026, Track 4

A shopping agent for the Conversational E-Commerce Search Challenge.

On the 200 public sessions, scored by the unmodified official evaluator:

| | Hit@10 | MRR | MTTC | TechnicalScore |
|---|---:|---:|---:|---:|
| official starter | 0.125 | 0.068034 | 9.81 | 0.10671 |
| **this agent** | **0.915** | **0.750276** | **3.02** | **0.842183** |

No API keys, no model downloads, no network at scoring time. The agent imports
`json`, `re`, `sqlite3` and `pathlib`, and nothing else. A full run over 200 sessions
takes about 25 seconds on a laptop CPU, and reports zero tokens and zero dollars.

## What it does

A shopper is thinking of one product out of fifty thousand and will not say which.
Each turn, the agent shows ten products and asks one question. The session ends when
the hidden product appears in those ten, or after ten turns.

The agent returns two things every turn, written for different readers.

The **eval adapter** is what the scoring sees. It accumulates everything the shopper has
said, queries BM25 over the catalog, moves the named category to the front, cuts to ten,
and reorders those ten by review count. It sets `ask_attribute` to `other` on every turn,
because a named facet returns only constraints of that class while `other` returns any of
them.

The **construction policy** is the `message` field. A shopper who cannot name the product
they want can still react to one, so the agent presents the ten as examples rather than as
a quiz. The evaluator never reads `message`, so this scores nothing. We built it because
the scored task and the useful task are not the same task, and
[`REPORT.md`](REPORT.md) sets out the evidence that they differ.

That report also gives the measurement behind each adapter step, including the variants we
rejected.

## Setup

Python 3.10 or later. There are no dependencies to install and no environment variables
to set.

The catalog is not in this repository; it is 58 MB and belongs to the organizer. Download
it from the participant kit release and unpack it into `data/`:

```bash
curl -L -o data/catalog.jsonl.gz \
  https://github.com/TechJam2026/techjam-conversational-search/releases/download/participant-kit/catalog.jsonl.gz
cd data && gzip -dk catalog.jsonl.gz && cd ..
```

Expected SHA256 of the archive:

```
07fd142631fd6b03e2b4d09988c3eb7d53720e9d57010c79db48eeaada50a8f8
```

## Reproduce the result

```bash
python3 -m evaluator.local_evaluator
```

That command loads `starter/agent.py`, runs all 200 public sessions, prints the metrics,
and writes `results.json`. The number in the table above is
`recommended_technical_score`. A copy of our run is checked in at
[`results/public200.json`](results/public200.json).

The evaluator in this repository is the organizer's, unmodified. Stripping carriage
returns, it hashes to `0cbd7aa78ade1d2b3b7d11c51e73f63f`, matching upstream.

Run the tests with:

```bash
python3 -m unittest discover -s tests -v
```

## Environment and cost

Measured on the machine that produced the result above.

| | |
|---|---|
| Python | 3.10.12, x86-64 |
| hardware | laptop CPU, 24 cores, 15 GB RAM; no GPU used |
| dependencies | none beyond the standard library |
| agent startup | 4.3 s, building its own SQLite FTS5 index over the catalog |
| full 200-session run | 22.7 s |
| per-turn latency | 39 ms median, 41 ms at p95 |
| token usage | 0 |
| model cost | $0 |

There are no external services to reach, so nothing here depends on network
availability, an API quota, or a cached model download. The same run on a slower
machine changes the timings and nothing else.

## Layout

```
starter/agent.py      the agent
evaluator/            the official evaluator, unmodified
tests/                unit tests
data/                 public sessions; catalog downloaded separately
results/              our measured runs, including the variants we rejected
REPORT.md             what we built, and the measurement behind each step
```

## Limitations

**Popularity may be measuring the data, not the shopper.** Reordering the scored ten by
review count is worth 0.053 of the final score. Amazon targets sampled leave-last-out
skew popular, so a popularity prior can look like skill when it is an artifact of how the
evaluation set was built. Cañamares and Castells analysed exactly this in *Should I Follow
the Crowd?* (SIGIR 2018). We report the gain and label its likely cause rather than
claiming a modelling insight.

**Seventeen sessions still miss.** In those, the listing text the shopper quotes is not
unique to one product, or BM25 never placed the target in the ten even given an oracle
query. A belt described only as leather, 100% leather, imported, buckle closure matches
thousands of belts, and no amount of ranking recovers it from what the shopper says.

**We did not build a neural reranker, so we claim no ablation against one.** A peer's
MiniLM cross-encoder scored 0.64 on this task. Our reason for not spending the dependency
is that asking `other` already extracts all four constraints by turn three, and our
remaining misses are generic listing text rather than a ranking failure a cross-encoder
would fix.

**The construction policy is untestable here by design.** `customer_reply` takes
`ask_attribute` and never receives the ranking, so nothing the agent shows can change what
the shopper wants. Measuring it needs a target-free protocol of the kind Kim et al.
propose, which this challenge does not use.

**We do not claim 0.842 on the private 800.** That package is released after the deadline.

## What we would do next

Two directions, in order of expected value.

The first is the ranking of the ten, which is where the remaining headroom sits. Hit rate
is 0.915 and MRR is 0.750, so lifting MRR toward 0.9 is worth roughly twice what lifting
recall is worth. A cross-encoder over ten candidates is cheap enough to test properly, and
we would run it as an ablation rather than adopt it on reputation.

The second is honest evaluation of the idea the scoreboard cannot see. CoShop measures
whether a dialogue expands what the shopper knows, and five frontier models stayed under
56% on it. Running the construction policy against that kind of protocol would tell us
something the TechnicalScore cannot.

## Data

Catalog and sessions come from the frozen TechJam participant kit, derived from Amazon
Reviews 2023 (`Clothing_Shoes_and_Jewelry`). See [`DATA_ATTRIBUTION.md`](DATA_ATTRIBUTION.md).
