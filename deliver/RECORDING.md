# Recording

1080p 30fps. OBS or Win+G. You talk. The film already moves.
Target under three minutes. Read `SCRIPT.md` in lockstep.

## Shot 1 — geometry (~2:12)

Fullscreen `kit/deliver/play.html` (or `architecture.mp4`). Space pauses. R restarts.

Point at the object each sentence names.

## Shot 2 — one full session (~28s)  [REQUIRED]

FAQ section 7: "The demonstration should show at least one complete multi-turn session."
The film alone does not satisfy this.

Fullscreen `kit/deliver/demo.html`. Step turn 1 -> 2 -> 3 on a browsing session.
Say the 2:12-2:40 block. Land on the hit at rank 1.

## Shot 3 — receipt (~18s)

```
cd kit
python -m evaluator.local_evaluator
```

Hold on `"recommended_technical_score": 0.842183`.

Say: unmodified official evaluator, 200 public sessions, stdlib only, zero tokens.

## Assemble

film -> session -> eval. Under three minutes. Upload YouTube, set public.
Paste `YOUTUBE_URL` into `deliver/DEVPOST.md`.

## Before you upload

- [ ] 0.107 baseline said out loud
- [ ] "two policies" named out loud
- [ ] one complete multi-turn session on screen
- [ ] no claim of a MiniLM ablation we did not run
