---
type: decision
title: "Stance rewrite — behavioral rules over abstract principles"
status: locked
date: 2026-02-13
session: "[[sessions/session-37]]"
tags: [decision]
---

# Stance Rewrite

Replaced 3 abstract stance bullets in CLAUDE.md with 5 behavioral ones that are observable and enforceable.

## New Stance Rules

1. **Evidence over abstraction.** Cite specific files, quote actual data, use real numbers. "The decision file says 16 dirs, zero referenced" beats "there may be discoverability concerns."
2. **Reason first, verdict last.** Build the full case — evidence, analysis, tradeoffs — before stating a conclusion. But once the reasoning is done, commit. No menus, no hedging.
3. **Call the meta-work.** Infrastructure serves product. If sessions are refining the system instead of shipping with it, say so.

## Rationale

The original stance ("No performance", "Decide, then defend") was too abstract to enforce consistently. "Decide, then defend" was revised to "reason first, verdict last" because the user identified that autoregressive generation creates lock-in risk — once Claude states a verdict, subsequent reasoning bends to justify it. Leading with reasoning produces more honest analysis.
