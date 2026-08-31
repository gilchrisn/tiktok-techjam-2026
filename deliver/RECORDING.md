# Recording

1080p 30fps. OBS or Win+G. You talk. The film already moves.
Target under three minutes. Read `SCRIPT.md` in lockstep.

## Shot 1 — film (~2:50)

Fullscreen `kit/deliver/play.html` (or `architecture.mp4`). Space pauses. R restarts.

Point at the object each sentence names. Do not read the captions out loud.

The film now includes the task, the slit, two policies, the adapter, and one three-turn session.

## Shot 2 — receipt (~18s)

```
cd kit
python -m evaluator.local_evaluator
```

Hold on `"recommended_technical_score": 0.842183`.

Say: unmodified official evaluator, 200 public sessions, stdlib only, zero tokens.

## Assemble

film → eval. Upload YouTube, set public. Paste `YOUTUBE_URL` into `deliver/DEVPOST.md`.

## Before you upload

- [ ] 0.107 baseline said out loud
- [ ] two policies named out loud
- [ ] one complete multi-turn session on screen (the film's last geometry beat)
- [ ] no claim of a MiniLM ablation we did not run
