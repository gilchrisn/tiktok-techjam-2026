# Spoken script

Play `kit/deliver/architecture.mp4`. Read this. Do not read the captions.

One idea per sentence. Point at what you are naming.
Then show one session, then run the evaluator and hold 0.842183.

~385 spoken words. About 2:50 at a measured pace. Shot list in `RECORDING.md`.

---

## 0:00–0:18 · the task, and the number to beat

We are writing a shopping agent.

Each session hides one product in a catalog of fifty thousand.

We have ten turns to get that product into a list of ten.

The official starter scores zero point one zero seven. We score zero point eight four two.

## 0:18–0:42 · why the split matters

They score the list. They do not score the sentence we show a person.

The simulator is this box.

Only the ask fits through it. The ranking bounces and falls to the scorer.

The titles never go in.

So the next thing the user says depends only on what we asked.

## 0:42–1:04 · two policies, one turn

That split is our design, so we return two policies every turn.

The adapter plays the scored game. The construction policy talks to the person.

A shopper often cannot name what they want. Showing ten concrete items is how they form
a preference.

The harness cannot see that. We shipped it anyway, because a copilot is for people.

## 1:04–1:28 · what the adapter does

The session has four constraints to disclose.

Ask a named facet and you only get the matching slice.

Ask `other` and you cover the whole set. Two come out — that is the cap per turn.

Two leave. Then the other two.

By turn three we hold every constraint this customer will ever give us.

## 1:28–1:44 · how they score a hit

The scorer keeps ten slots.

If the hidden product lands in those ten, that turn is the score, and the session stops.

We sort those ten by review count. Most hits already sit in slot one.

## 1:44–2:08 · what we kept, and what we threw away

These 175 dots are sessions we had already solved.

Popularity inside the ten leaves all of them in place.

Sorting a window of four hundred instead dropped our matched sessions from 102 to 74.
We measured that, and rejected it.

The first sentence already names the category. Putting that in front took us from
zero point eight seven five to zero point nine one five.

## 2:08–2:34 · a real session

One full session, turn by turn.

Turn one, the customer is only browsing — no constraints at all.

We ask `other`, and we still show ten items, because showing is free.

Turn two, two constraints arrive. Turn three, the last two.

The hidden product enters the ten at rank one, and the session stops.

## 2:34–2:50 · the number

Unmodified official evaluator, two hundred public sessions.

Zero point eight four two. Python standard library only. Zero tokens. Zero dollars.

The titles sit outside that number. They are not scored, and we shipped them anyway.

---

If you run long, cut "We sort those ten by review count" and shorten the session shot to
turns one and three. Do not cut the task, the box, the two policies, or the 0.107 anchor.

## If a judge asks afterwards

- **"Why not MiniLM / a neural reranker?"** We did not build one, so we claim no ablation.
  A peer's MiniLM scored 0.64. Our reason for not spending the dependency: `"other"`
  already dumps all four constraints by turn 3, and our remaining misses are generic
  listing text, not a missing neural rerank.
- **"Is `other` an exploit?"** Dominance, not an exploit. Specific labels return a subset
  of the same batch-of-two filter. Proved in `THEOREM.md`.
- **"Is popularity gaming the metric?"** Possibly a leave-last-out artifact — we say so in
  Limitations. Cañamares & Castells (SIGIR 2018) analyse exactly when popularity is a real
  signal versus an experimentation bias.
