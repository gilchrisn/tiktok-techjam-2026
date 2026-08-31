# What we built, and how we knew each step worked

The idea is not BM25. The idea is that a shopping copilot should help someone build a
preference, and that the ranking is how it teaches.

A real shopper often cannot name what they want. Showing them ten concrete items is an act
of elicitation — *closer to this, or not?* — rather than a probe for a frozen product ID.
Saracay, Schmidt and Guestrin argue exactly this in
[Beyond expert users](https://arxiv.org/abs/2606.30863) (Stanford, June 2026), and they
built CoShop to measure it. Five frontier models stayed under 56% accuracy over five turns
on that benchmark, and the failure was not in finding items but in how little the dialogue
expanded what the shopper knew.

This harness cannot measure any of that. The function that generates the shopper's next
line is `customer_reply(sample, ask_attribute, disclosed, boundary_used)`, and the
ranking is not one of its arguments. The target is fixed before turn one and nothing the
agent shows can move it. Kim et al. name this failure mode in
[Stop Playing the Guessing Game!](https://arxiv.org/abs/2411.16160) (EMNLP 2025 Findings):
a simulator with a predefined target turns recommendation into guessing. τ-Rec
([RecSys 2026](https://arxiv.org/abs/2606.10156)) uses the same reveal-tagged channel we
have. ConvApparel ([EACL 2026](https://arxiv.org/abs/2602.16938)) measured the realism gap
across simulators in this exact apparel domain, and fitting one does not produce a better
shopper.

So the agent returns two policies in a single response.

| | Construction policy | Eval adapter |
|---|---|---|
| lives in | `message`, and the act of showing a slate | `ask_attribute`, accumulated BM25, the reordered ten |
| the shopper | would use the list to form a preference | is a state machine and ignores it |
| the rubric | Innovation and Impact | an input to Technical Execution |

We do not claim the slate steers the hidden target. That would be false of the code, and
the function signature is how we know. We claim the opposite, and we built the
construction policy anyway.

The rest of this report is the adapter: four steps, each with the measurement that
justified it.

---

## 1. Where the guessing game breaks the starter

The official starter agent scores 0.10671, and two lines of `starter/agent.py` explain
why. It queries only the current turn's message, so it forgets everything the shopper
said. It hardcodes `ask_attribute` to `None`, so the shopper answers *"ask me about one
specific attribute"* and discloses nothing.

An agent that never asks therefore never learns. Browsing sessions show the cost most
plainly: their opening line names a category and gives no constraints at all, and the
starter hits 0.025 of them. Boundary sessions it never solves.

## 2. The two failures are independent

Fixing either flaw alone leaves most of the gap open.

| arm | the single change | Hit@10 | TechnicalScore |
|---|---|---:|---:|
| v1 | accumulate the dialogue, still never ask | 0.270 | 0.228414 |
| v2 | ask `other`, but stay stateless | 0.560 | 0.496973 |
| v3 | both | 0.875 | 0.750401 |

Only-accumulate solves 17 sessions, only-ask solves 75, and 48 need both. Asking is the
larger lever, which surprised us; memory alone gives the agent nothing new to remember.
The session-level breakdown is in [`results/miss_tree.json`](results/miss_tree.json).

Asking `other` rather than a named facet matters because of how the simulator filters.
A named label returns only constraints of that label; `other` matches the whole set. The
proof is in [`THEOREM.md`](THEOREM.md), and the consequence is that all four constraints
are on the table by turn three.

## 3. The list already held the target; the order lost it

After v3, 175 of 200 sessions hit. Of those hits, 42 landed at rank 5 through 10.

That number reframed the problem. The retrieval had found the product and the ordering
had buried it — and because the evaluator locks the recorded rank at the *first* turn the
target enters the ten, a better position on a later turn cannot rescue it. The remaining
25 sessions fail for a different reason, which section 5 covers.

## 4. Reordering the scored ten by review count

Sorting only those ten by `rating_number` leaves hit rate untouched at 0.875 and lifts MRR
from 0.540 to 0.716. On the 42 buried hits, MRR moves from 0.145 to 0.846. The
TechnicalScore goes from 0.750401 to 0.803243.

Sorting a wider window fails. Taking the BM25 top 400, ordering that by popularity, and
then cutting to ten drops the sessions we had already solved from 102 to 74, so we
rejected it ([`results/pop_window400.json`](results/pop_window400.json)). Popularity works
as a tiebreak inside a set the retrieval has already narrowed, and stops working as a
retrieval signal in its own right.

We label the gain rather than claim it. Amazon targets sampled leave-last-out skew
popular, so this may be measuring the evaluation set rather than the shopper. Cañamares
and Castells set out when popularity is real signal and when it is experimental artifact
in *Should I Follow the Crowd?* (SIGIR 2018, best paper).

## 5. The opening line names the category, free

Every session opens with `I'm looking for {category}`, and the final-evaluation FAQ froze
those templates, so no paraphrase will break the pattern. Pulling products in that
category to the front of the BM25 top 400, then cutting to ten, then applying popularity,
raises Hit@10 from 0.875 to 0.915. It gains eight sessions and loses none.

That is the shipped agent, at **0.842183**.

We also tested withholding a badly-ranked early hit to land a better-ranked later one,
which the first-passage arithmetic in `THEOREM.md` says can pay. After popularity it
cannot: only three early bad hits remain, worth about 0.003. We did not ship it.

---

## The result

Unmodified official evaluator, 200 public sessions, run twice with identical output.

| Hit@10 | MRR | MTTC | TechnicalScore | tokens | cost |
|---:|---:|---:|---:|---:|---:|
| 0.915 | 0.750276 | 3.02 | **0.842183** | 0 | $0 |

```bash
python3 -m evaluator.local_evaluator
```

The idea is not this number. The number is what we do because the evaluator cannot see
the idea.
