# Spoken script

Play `deliver/architecture.mp4` and talk over it. Don't read the captions — say this instead,
and point at whatever the picture is showing.

About 420 words — roughly 2:50 at a normal speaking pace. With the evaluator shot on the end
that's a shade over three minutes. The film runs 1:34, so you'll be ahead of it; see the note
at the bottom.

---

## The task

Fifty thousand clothing products, and the customer has one of them in mind
but won't tell you which. You get ten turns, you show them ten products each turn, and you win
the moment their item shows up in your list.

The challenge ships a basic agent as the thing to beat. It scores 0.107. Ours scores 0.842.

## What actually gets scored

The customer isn't a person, it's a simulator. And when it decides what to say next, it looks at
exactly one thing — the question you asked. It never sees the products you recommended, and it
never reads the sentence you wrote for it.

So your ranking gets scored, but it can't steer the conversation.

## Two outputs, two audiences

So we return two things every turn. One is for the scorer: the question, and ten product IDs.
The other is a sentence for a human, using the products on screen as examples — because someone who can't describe what they want works it out
by looking at options.

The evaluator throws that sentence away. A real shopper wouldn't.

## Asking the right question

Each session has exactly four facts the customer will give up, and you ask for them one topic at
a time, from a menu of ten.

Ask about colour and you get colour. But one option on that menu is `other`, and `other` matches
anything, so it hands back whichever two facts haven't come out yet. Ask twice and you have all
four by turn three.

## Getting their item to the top

Once their product lands in your ten, the session stops right there, and where it landed is what
you're scored on. A better answer next turn doesn't help.

So we reorder those ten by review count. Usually that puts the right answer first.

## What we kept, and what we threw out

These 175 dots are sessions we'd already solved, and reordering inside the ten keeps all of
them. The same trick across four hundred products didn't — a hundred and two solved sessions
dropped to seventy-four, so we cut it.

What we did keep: their opening line always names a category. Using it took us from 0.875 to
0.915.

## One real session

Turn one, they're just browsing, so we have nothing — but we still show ten and we still ask.
Turn two, two facts come back. Turn three, the last two. Their item lands at the top and the
session ends.

## The number

Official evaluator, unmodified, all two hundred public sessions. 0.842 against the starter's
0.107. No model, no API keys, no network.

And the sentence we write the shopper isn't in that number anywhere. We shipped it anyway.

---

**If you run long:** cut the review-count paragraph. That's about fifteen seconds.

**If a judge asks afterwards:**

- *Why not a neural reranker?* We didn't build one, so we're not claiming an ablation against
  one. A friend's MiniLM scored 0.64 here. We skipped it because `other` already gets all four
  facts out by turn three, and the sessions we still miss are ones where the listing text isn't
  unique to a single product — a reranker doesn't fix that.
- *Isn't `other` an exploit?* No, it dominates. A specific label returns a subset of exactly the
  same filter. Proved in `THEOREM.md`.
- *Isn't popularity gaming the metric?* Possibly, and Limitations says so. Amazon targets
  sampled leave-last-out skew popular. Cañamares and Castells worked out when popularity is real
  signal and when it's an artifact of the test set — SIGIR 2018, best paper.

---

**Film timing.** The film is 94s and this runs about 170s. Either hold the last frame of each beat
until you've finished the sentence — narration leading the visual is normal and nobody notices —
or multiply every `self.wait(x)` in `deliver/film.py` by 1.9 and re-render with
`python3 deliver/film.py`.
