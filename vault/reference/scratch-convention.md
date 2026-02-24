---
type: reference
title: "Scratch Surface Convention"
date: 2026-02-24
decision: "[[decisions/scratch-collab-surface]]"
---

# Scratch Surface Convention

Quick reference for `vault/scratch.md` — the shared working surface.

## Callouts

```markdown
> [!question]
> Don't follow / needs clarification

> [!warning]
> Disagree / see a flaw

> [!tip]
> Extend this with... / yes-and

> [!info]
> Context or reference (either party)
```

## Inline Markup

- `==highlight==` — emphasis on specific phrases
- `%%comment%%` — invisible in Obsidian preview

## Protocol

1. **"Ready for marks"** — author signals structured content needs review
2. **"Read it"** — reviewer signals annotations are done
3. Claude reads back, responds **only to marked items**
4. **Silence = agree** — unmarked sections are accepted

## When to Use

- **3+ related points** → write to scratch surface, signal "ready for marks"
- **Quick exchange** (1-2 points) → chat is fine

## Lifecycle

- Initialized at `/begin` with session number
- Either party writes content anytime
- `## Decided` section added on-demand when items are resolved
- Reset at `/wrap` — key reasoning migrates to handoff first

## What Survives from scratch-pad-v2

- Objective lifecycle: `[TBD]` → `[LOCKED]`
- Problem section as reasoning anchor
- Rewrite-not-append maintenance
