# Spoken script

Play `kit/deliver/architecture.mp4`. Do not read the captions.
Times match the current film (~1:34). Point at the picture for that beat.

---

## 0:00–0:10 · task

A session hides one product in a catalog of 50,000. The agent has ten turns to put that product in a list of ten.

The kit starter scores 0.107. This agent scores 0.842.

## 0:10–0:23 · slit

The score uses the list of ids, not the message text.

The simulator only takes the ask. The ranking is not an input. Neither are the titles. The next user sentence depends on the ask.

## 0:23–0:31 · two outputs

`respond()` returns two outputs. The ask and the list go to the scorer. The message is a sentence with product titles.

The evaluator does not read that message. A shopper would.

## 0:31–0:43 · other

Each session has four constraints. A named facet returns only that type. `other` returns any of them, two per turn.

Two are disclosed, then two more. All four are known by turn three.

## 0:43–0:52 · first-passage

If the hidden product is in the ten, that turn is recorded and the session ends.

We sort the ten by review count. Most hits are already rank one.

## 0:52–1:05 · keep / drop

These 175 sessions were already solved. Popularity inside the ten kept all of them.

Popularity over a window of 400 cut already-solved hits from 102 to 74. We did not use it.

The opening message contains the category. Using it moved Hit@10 from 0.875 to 0.915.

## 1:05–1:20 · one session

Turn 1: browsing, no constraints disclosed. We ask `other` and return ten products.

Turn 2: two constraints. Turn 3: the remaining two. The target is rank one and the session ends.

## 1:20–1:34 · score

Official evaluator, 200 public sessions, unmodified. TechnicalScore 0.842. No model. Zero tokens.

The message is not in that score.

---

If you run long, drop the review-count sentence.

If a judge asks later:

- MiniLM: we did not build one, so we claim no ablation. A peer MiniLM scored 0.64. `other` already returns all four constraints by turn 3. Remaining misses are generic listing text.
- Is `other` an exploit: no. A specific label is a subset of the same two-per-turn filter. `THEOREM.md`.
- Popularity: may be a leave-last-out artifact. Limitations says so. Cañamares and Castells, SIGIR 2018.
