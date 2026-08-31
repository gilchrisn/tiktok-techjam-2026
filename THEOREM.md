# First-passage scoring on a rank-1 reveal channel

A short note on the topology of the TechJam 2026 Track 4 evaluator.
Every statement is tagged **proved** (from `evaluator/local_evaluator.py` and
`docs/evaluation_config.json`) or **measured** (public 200). Nothing here is
claimed of a real shopper.

---

## 0. Objects

A session has a frozen target `y` (a catalog `parent_asin`), a set `C` of
constraint strings with `|C| = 4` **(measured, public 200)**, a disclosed set
`D ⊆ C`, and a turn `t ∈ {1,…,10}`.

The agent, at each turn, emits a triple `(m, a, R)`:

- `m` — a string (`message`)
- `a` — one of ten labels, or `null` (`ask_attribute`)
- `R` — an ordered list; the scorer keeps the first 10 valid unique ids

The environment then either **stops** (if `y ∈ R` and the override lock is
open) or replies with a new message and an updated `D`.

Write `T = inf{ t : y ∈ R_t }` and `r_T` for the position of `y` in `R_T`
(1-indexed). Misses: `T = ∞`.

---

## 1. Invariances (the topology)

**I-Channel (proved).** `customer_reply(sample, ask_attribute, disclosed,
boundary_used)` does not take `R` or `m`. The next `(message, D)` is a function
of `(sample, a, D)` only. Source: `local_evaluator.py` `customer_reply`,
`evaluate` loop.

**I-First-passage (proved).** If `y ∈ R_t` and the override lock is open, the
session records `(T, r_T) = (t, index(y)+1)` and **breaks**. Later lists are
never scored. Source: `evaluate`, the `if override_applied and target in ranked:
break` branch.

**I-Miss-pin (proved).** A miss contributes turn 11 to MTTC.
`docs/evaluation_config.json`: `miss_turn_value = 11`.

**I-Batch (proved).** A non-null, non-boundary-burn `a` reveals at most 2
elements of `C \ D`, namely those matching
`(a == "other") or classify(c) == a`. Source: `matches[... ][:2]`.

**I-Open-type (proved).** Every opening message contains
`I'm looking for {coarse_category(y)}`. Buying also inserts `hard[0]` into `D`.
Browsing and boundary insert nothing into `D`. Override speaks a soft
preference but does **not** mark it disclosed. Source: `initial_message`.

**I-Lock (proved).** On `intent_override`, a hit is illegal until
`turn+1 == override.turn` with `override.turn ∈ {3,4}`. Source: `override_applied`
gate.

**I-Score (proved).** Over `N` sessions,

```
h   = |{T ≤ 10}| / N
MRR = mean( 1{T≤10} / r_T )
MTTC = mean( T if T≤10 else 11 )
Eff = clip((11 − MTTC)/10, 0, 1)
S   = 0.50 h + 0.30 MRR + 0.20 Eff
```

---

## 2. Theorems that follow

### Theorem 1 — The slate is silent

**The environment kernel does not depend on `R` or `m`.**

Proof. I-Channel. The only agent field that enters `customer_reply` is `a`.
Invalid `a` is coerced to `"other"`. Null `a` discloses nothing.

**Corollary 1.1 (unidentifiability).** Any hypothesis of the form “the ranking
constructs the user’s preference” has measure zero under this evaluator. It can
be true of a real shopper and is still untestable here. That is the Innovation
claim, not a scoring rule.

### Theorem 2 — `"other"` dominates label-cycling

Let `U = C \ D`. One ask of `"other"` returns `min(2, |U|)` constraints. One
ask of a specific label `λ` returns `min(2, |{c ∈ U : classify(c)=λ}|)`.
Hence `"other"` weakly dominates every specific `λ` for the criterion
“number of new disclosures this turn.”

Proof. The match filter is `(a == "other") or classify(c) == a`. The left
disjunct is true for every `c ∈ U`. The right disjunct is a subset.
The `[:2]` cap is the same in both cases.

**Corollary 2.1 (horizon).** After a boundary-burn of at most one turn,
`⌈|U|/2⌉` successful `"other"` asks empty `U`. With `|C|=4` **(measured)** and
I-Open-type, complete `D = C` is available at the **start of turn 3** on
non-boundary, non-lock sessions. **Measured:** 200/200 sessions have all 4
constraints after turn 3 under always-`"other"`.

**Corollary 2.2.** An elaborate ask-policy over the ten labels cannot extract
more of `C` than always-`"other"`. It can only delay Corollary 2.1. This is why
the friend’s facet-cycling Policy C is slower (MTTC 6.28 vs 3.02) on the same
catalog.

### Theorem 3 — Efficiency is hit-rate times speed

From I-Miss-pin, `MTTC = 11(1−h) + h·t̄` where `t̄` is mean `T` on hits.
Therefore `Eff = h·(11 − t̄)/10` (on the interior of the clip).
Substitute into I-Score:

```
S = 0.50 h + 0.30 MRR + 0.02 h (11 − t̄)
```

**Corollary 3.1.** You cannot buy Efficiency without hits. Fast misses are still
worth 0. MTTC is not an independent objective.

### Theorem 4 — First-passage value, and when delay pays

On a single session the recorded payoff is

```
V(T, r) = 1{T≤10} · ( 1/2 + 3/(10 r) + (11−T)/50 )
```

which is I-Score with `N=1`. Replacing a hit `(T, r)` by `(T+Δ, r')` with
`T+Δ ≤ 10` changes `V` by

```
ΔV = (3/10)(1/r' − 1/r) − Δ/50
```

**Delay is +EV iff** `1/r' − 1/r > Δ/15`.

Examples: `r=10, r'=1, Δ=1` → 0.9 > 0.067, pay. `r=1`, any `Δ>0` → left side
≤ 0, delay is dominated.

**Corollary 4.1 (why withhold died).** After reordering the scored 10 by
`rating_number`, **122 of 175 hits are already `r=1` (measured).** The set of
sessions with `T≤2` and `r≥5` has size 3; replacing them by `(T=3, r=1)`
moves `S` by at most ~0.003. First-passage delay is a real invariant that
**has already been harvested** by the ranker. It is not a remaining lever.

### Theorem 5 — Opening category is a free blocking key

By I-Open-type the agent observes `coarse_category(y)` at `t=0` with no ask.
That string is a coarsening of the target’s catalog path. Soft-moving BM25
candidates whose stored coarsening contains that string to the front of the
list is therefore a function of an **observed** type, not of a guessed slot.

**Measured, one-property, lines-meet:** stacked on accumulate + `"other"` +
within-10 popularity, this move sent Hit@10 0.875 → 0.915 (+8 sessions, 0
lost) and `S` 0.803 → **0.842183**.

The overnight paraphrase-risk that killed this move is **not** an invariance
of the released evaluator: `docs/final_evaluation_faq.md` freezes the
templates. I23 in the old recon list is superseded.

### Theorem 6 — The task is interactive entity resolution, not CRS

`C` is derived from `y`’s own `features` / `details` / regex material and
colour (`intent_card`). Hits require exact `parent_asin` equality. Combined
with Theorem 1, the evaluator is **blocking a 50k catalog with a reveal
oracle, then ranking the block.** It is not constructive preference (G2) and
it is the guessing game of G1.

**Corollary 6.1.** A method that treats `C` as clean facets (AND of
attribute-values) is misspecified: `C` contains truncated marketing copy.
**Measured:** phrase-AND of disclosed strings cut `S` by 0.34.

**Corollary 6.2.** Retrieval is not the open problem on the public 200:
accumulated-query BM25 recall@1000 = 100% **(measured)**. Residual misses
(17 after Theorem 5) sit in a **generic-text regime** (pool after 4
constraints still 13–1358, or oracle BM25 rank 17–969). There is no further
invariance of Theorem-2/4/5 size on that slice.

---

## 3. What this note is for

It is the Innovation paragraph with proofs. The construction policy in
`message` (slate as examples) is the thing Theorems 1 and 6 say the
evaluator cannot see. The adapter in `ask_attribute` / BM25 / category /
popularity is what Theorems 2–5 say is optimal *inside* the kernel.

Cite in the writeup as this file, not as a result on CoShop or PEPPER.
Those papers name the *other* objective; they do not prove these lemmas.
