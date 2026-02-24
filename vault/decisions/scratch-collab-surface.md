---
type: decision
title: "Collaborative Scratch Surface"
status: locked
date: 2026-02-24
session: "[[sessions/session-48]]"
supersedes: "[[decisions/scratch-pad-v2]]"
tags: [decision]
---

# Collaborative Scratch Surface

Evolve scratch.md from a Claude-only reasoning surface to a shared working surface with Obsidian callout annotations. Move from project root to `vault/scratch.md`.

## Why

Chat turns are one-directional — Claude produces structured analysis, user responds with a new message, and the mapping between feedback and specific points is lossy. No mechanism for positional feedback on proposals. Additionally, content in early chat messages dies when context compresses; a file-based surface survives.

## Design

**Location:** `vault/scratch.md` (was root `scratch.md`). Single file, single source of truth.

**Ownership:** Both parties write content and annotate. Not Claude's notepad — a shared working surface.

**Markup convention (Obsidian-native):**
- `> [!question]` — Don't follow / clarify
- `> [!warning]` — Disagree / flaw
- `> [!tip]` — Extend / yes-and
- `> [!info]` — Context / FYI
- `==highlight==` — inline emphasis
- `%%comment%%` — invisible in preview

**Core rule:** Silence = agree. Only mark what needs attention.

**Protocol:**
- "Ready for marks" = author signals content needs review
- "Read it" = reviewer signals annotations are done
- Respond only to marked items; unmarked sections are agreed

**What survives from scratch-pad-v2:**
- Objective lifecycle: `[TBD]` → `[LOCKED]`
- Problem section as reasoning anchor
- Rewrite-not-append maintenance
- Reset at `/wrap`

**What's new:**
- Bidirectional — both parties use same callout convention
- `## Decided` section added on-demand (not in init template)
- "3+ points" threshold — use surface for structured multi-point content, chat for quick exchanges
- Reference card at `vault/reference/scratch-convention.md`
- Claude reads reference card silently at `/begin` for cold-start awareness
- Brainstorm protocol: surface usage folded into "Drive to Consensus" step
- Build mode: path update only, no protocol changes

**What changed:** CLAUDE.md (5 locations), begin.md (2 locations), wrap.md (5 locations), brainstorm.md (2 locations), build.md (1 location). New reference card. Root scratch.md deleted.

## Rejected alternatives
- Two files (root scratch + vault collab) — sync risk, one source of truth is better
- Inline markers (`[?]`, `[!]`, `[+]`) instead of callouts — not visually distinct in Obsidian, no collapsing
- Convention embedded in scratch.md init template — noise at session start; reference card is cleaner
- Separate step 4 in brainstorm protocol — overpromotes a tool; it's a technique within consensus-driving, not a cognitive step
- "Ready for marks" in build mode — build has its own inspect & align flow, adding the surface would slow a fast loop
