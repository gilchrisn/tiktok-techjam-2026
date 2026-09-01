# Method

## The idea

A shopper often cannot name the product they want. They can react to one, though, so
showing ten concrete items narrows the search faster than asking them to describe
something they have not yet pictured.

Saracay, Schmidt and Guestrin make this argument in
[Beyond expert users](https://arxiv.org/abs/2606.30863) (Stanford, June 2026) and built
CoShop to test it. On that benchmark five frontier models stayed under 56% accuracy across
five turns. They failed not at finding items but at expanding what the shopper knew.

This evaluator cannot measure that. The function that writes the shopper's next line is
`customer_reply(sample, ask_attribute, disclosed, boundary_used)`, and the ranking is not
one of its arguments. The target is fixed before turn one, so nothing the agent shows can
change it. Kim et al. name this failure mode in
[Stop Playing the Guessing Game!](https://arxiv.org/abs/2411.16160) (EMNLP 2025 Findings):
a simulator with a predefined target turns recommendation into guessing. τ-Rec
([RecSys 2026](https://arxiv.org/abs/2606.10156)) reveals constraints through the same kind
of channel. ConvApparel ([EACL 2026](https://arxiv.org/abs/2602.16938)) measured how far
these simulators sit from real shoppers, in this same apparel domain.

Because the scored task and the useful task differ, the agent answers both in one response.

| | Construction policy | Eval adapter |
|---|---|---|
| lives in | `message`, and the slate itself | `ask_attribute`, accumulated BM25, the reordered ten |
| the shopper | would use the list to narrow down | is a state machine and ignores it |
| the rubric | Innovation and Impact | an input to Technical Execution |

We do not claim the slate steers the hidden target. The function signature shows it cannot.
We built the construction policy regardless, and everything below is the adapter.

---

## 1. Why the starter scores 0.107

Two lines of `starter/agent.py` account for it. The agent queries only the current turn's
message, so it forgets what the shopper said earlier. It also hardcodes `ask_attribute` to
`None`, which makes the shopper reply *"ask me about one specific attribute"* and disclose
nothing.

An agent that never asks never learns. Browsing sessions show that most clearly, because
their opening line names a category and supplies no constraints: the starter solves 0.025
of them, and no boundary session at all.

## 2. Memory and asking are independent failures

Fixing one without the other leaves most of the gap open.

| arm | the single change | Hit@10 | TechnicalScore |
|---|---|---:|---:|
| v1 | accumulate the dialogue, still never ask | 0.270 | 0.228414 |
| v2 | ask `other`, but stay stateless | 0.560 | 0.496973 |
| v3 | both | 0.875 | 0.750401 |

Accumulating alone solves 17 sessions and asking alone solves 75, while 48 need both.
Asking is the larger lever, which we did not expect: memory has nothing to store until a
question produces an answer. Per-session detail is in
[`results/miss_tree.json`](results/miss_tree.json).

Asking `other` beats naming a facet because of how the simulator filters. Its condition is
`attribute == "other" or classify_constraint(c) == attribute`, so a named label returns
only constraints of that class while `other` matches all of them. The simulator releases at
most two per turn and every session holds exactly four, which puts all four on the table by
turn three.

## 3. Retrieval found the target; the ordering buried it

After v3, 175 of 200 sessions hit, and 42 of those hits landed at rank 5 through 10.

Those 42 changed what we worked on. BM25 had already retrieved the product, so no better
query would help; the position it arrived in was the problem. The evaluator locks the
recorded rank at the first turn the target enters the ten, so improving the list afterwards
recovers nothing. A different failure accounts for the 25 sessions that never hit at all.

## 4. Reordering the scored ten by review count

Sorting those ten by `rating_number` holds hit rate at 0.875 and lifts MRR from 0.540 to
0.716, taking TechnicalScore from 0.750401 to 0.803243. On the 42 buried hits alone, MRR
moves from 0.145 to 0.846.

Sorting a wider window instead loses ground. Ordering the BM25 top 400 by popularity and
then cutting to ten drops sessions we had already solved from 102 to 74, so we rejected it
([`results/pop_window400.json`](results/pop_window400.json)). Popularity works as a
tiebreak within a set that retrieval has already narrowed, and fails as a retrieval signal
on its own.

We report that gain without claiming it as a modelling result. Amazon targets sampled
leave-last-out skew popular, so the prior may be measuring how the evaluation set was built
rather than how shoppers behave. Cañamares and Castells set out when popularity is genuine
signal and when it is an artifact of the test collection, in *Should I Follow the Crowd?*
(SIGIR 2018).

## 5. The opening line already names the category

Every session begins with `I'm looking for {category}`, and the final-evaluation FAQ froze
those templates, so no paraphrase will break the pattern. Moving products in that category
to the front of the BM25 top 400, then cutting to ten, then applying popularity, raises
Hit@10 from 0.875 to 0.915. Eight sessions convert and none are lost.

That is the shipped agent, at **0.842183**.

We also tested withholding a badly ranked early hit to land a better ranked later one. The
scoring arithmetic allows it, because rank is locked at first appearance. After popularity
it no longer pays: three early bad hits remain, worth about 0.003, so we did not ship it.

## 6. The pivot is rhetorical, so we do not erase

Thirty sessions have the shopper change their mind: *"Actually, ignore my earlier
preference. What I need is: X."* The obvious response is to drop what they said before, and
here that is wrong.

The hidden target never moves. `behavior_for()` draws `old_value` from
`soft_preferences[-1]` and `new_value` from `hard_constraints[0]`, both out of the same
intent card for the same product, so what the shopper retracts stays true of the answer. The
pivot changes which fact they emphasise, not which item they want.

Erasing on the pivot costs half the scenario. Keeping everything scores 0.900 hit and 0.8089
across those thirty sessions, while clearing the accumulated messages on that phrase drops
them to 0.500 and 0.4379. The agent has no override branch, and that is the measurement
behind its absence.

## 7. The user profile has signal we could not convert

Every session hands `reset()` an anonymized `user_profile` carrying preference tags, a
purchase frequency, a rating style and a summary sentence. The tags do correlate with the
target. Across the 666 tag instances in the public set, a tag appears in its own target's
listing text 44.0% of the time and in a randomly drawn product 25.1% of the time, a lift of
1.75. Per tag the pattern holds: `comfort` appears in 65.3% of its own targets against 34.0%
of random products, `fit` in 57.1% against 33.7%, `style` in 44.6% against 20.8%.

Three ways of spending that signal all cost score.

| variant | TechnicalScore | Hit@10 | MRR |
|---|---:|---:|---:|
| shipped, profile unread | **0.842183** | 0.915 | 0.750276 |
| preference tags appended to the query | 0.836100 | 0.910 | 0.737 |
| profile summary appended to the query | 0.831600 | 0.905 | 0.734 |
| tags used to rerank the scored ten | 0.757400 | 0.915 | 0.468 |

The first two dilute retrieval. Nine distinct tags cover all 200 sessions and the common ones
appear in most of them, so adding them to a BM25 query contributes low-IDF terms that broaden
the match without narrowing it. The third leaves retrieval untouched and fails differently:
reordering ten items cannot change whether the target is among them, so hit rate holds at
0.915 while MRR falls from 0.750 to 0.468, because ranking on tag count displaces the
popularity ordering that section 4 showed was worth 0.053.

A 1.75 lift is real and too weak to beat what it would replace. We read the profile and do
not use it, and this is the measurement behind that rather than an assumption.

---

## Result

Unmodified official evaluator, 200 public sessions, run twice with identical output.

| Hit@10 | MRR | MTTC | TechnicalScore | tokens | cost |
|---:|---:|---:|---:|---:|---:|
| 0.915 | 0.750276 | 3.02 | **0.842183** | 0 | $0 |

```bash
python3 -m evaluator.local_evaluator
```

Seventeen sessions still miss. In those the listing text the shopper quotes is not unique
to one product: a belt described as leather, 100% leather, imported, buckle closure matches
thousands of belts, and no ordering recovers a detail the shopper never gave.
