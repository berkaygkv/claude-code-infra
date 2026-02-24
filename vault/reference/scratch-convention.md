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

## Document Structure — Two-Tier Layout

For proposals and design discussions, use a two-tier structure. Deep context on top (expendable under compression), decision surface at the bottom (survives longest, closest to annotation point).

```markdown
# Scratch — Session {N}

Session objective: [TBD]

---

## Deep Context

> [!info] Reference material
> {Source description}. Decision surface below is self-contained — this is the "why."

### {Reasoning topic 1}
{2-4 sentences. Why this choice, what evidence supports it.}

### {Reasoning topic 2}
{Same pattern. One topic per heading. No multi-topic sections.}

---

## Decision Surface

> [!info] How to read this
> Mark up this section. Deep Context above is reference — dig in only if you need the "why."

### Problem
{2-3 sentences. What's broken, why it matters.}

### The Design
{Visual first — flowchart, table, or diagram. Then rules as bullets or table rows.
Use ==highlights== for hard constraints. Keep prose minimal.}

### Decisions

> [!question] Mark these: ✅ agree · ❌ disagree · 💬 comment

1. **{Decision}** — {one-line rationale}
2. **{Decision}** — {one-line rationale}
```

### Why this order

- **LLM writes top-down** — dense research lands first naturally
- **Context compression eats from the top** — reference material is expendable, decisions survive
- **Human reads bottom-up** — scan decisions, scroll up only when "why?" is needed

### Formatting principles

- **Tables over prose** for structured comparisons
- **Callouts** for stance markers and reading instructions
- **==Highlights==** for hard constraints and non-negotiables
- **ASCII diagrams** for flows (renders in any viewer)
- **One heading per reasoning topic** — no multi-topic sections

## What Survives from scratch-pad-v2

- Objective lifecycle: `[TBD]` → `[LOCKED]`
- Problem section as reasoning anchor
- Rewrite-not-append maintenance
