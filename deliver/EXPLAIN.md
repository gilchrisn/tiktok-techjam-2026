# Cheat sheet — if you freeze

Open with the idea, not the score.

1. Shoppers form preference from the list. Frozen ASIN ≠ shopper.
2. `customer_reply` cannot see the list. That is the kernel.
3. `message` still teaches with titles. `ask_attribute='other'` + BM25 + category + popularity-in-10 is the adapter.
4. Ablations justified each adapter step. 400-pop failed lines-meet. Delay is dead once rank is 1.
5. 0.842 is the adapter. Innovation is the silent slate.

If a judge asks “why not MiniLM?”: friend’s MiniLM scored 0.64; `"other"` already dumps all four constraints by turn 3; remaining misses are generic text, not a missing neural rerank we can prove here.

If they ask “is `other` an exploit?”: it is dominance. Specific labels return a subset of the same batch-2 filter. We state that in `THEOREM.md`.

If they ask “does the slate steer the user?”: no. That would be false of this code. We claim the opposite.
