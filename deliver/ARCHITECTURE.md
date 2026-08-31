# Architecture — schematic in the film

The film draws this pipeline. Nodes light per beat.

```
user message
      │
      ▼
 Agent.respond()
   ├─ construction stage  →  message   (titles as examples; unscored)
   └─ adapter stage       →  ask_attribute='other'
                             accumulate → BM25-400
                             bump opening category
                             cut 10, sort by rating_number
      │
      ▼
 customer_reply(sample, ask_attribute, disclosed, boundary_used)
      ranking is write-only to the scorer
      first-passage: if y in top-10 and lock open, stop
```

`#stream-shopper` is the construction stage. `#stream-eval` is the adapter plus `customer_reply`. Neither is a storefront.

Theorems on the diagram:

| beat | claim |
|---|---|
| silent-slate | Thm 1 silent slate |
| opposite-failure | Thm 2 other-dominance, then v0–v3 |
| lines-meet | Thm 4 delay condition; Thm 5 opening category; keep within-10 pop, reject 400-pop |
| adapter-score | 0.84 is the adapter |

The simulator cannot see ranking or `message`.
