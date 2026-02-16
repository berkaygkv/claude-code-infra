---
type: decision
title: Research Pipeline v2 — TARGET Enforcement
status: superseded
date: 2026-02-04
session: "[[sessions/session-24]]"
supersedes: null
superseded_by: "[[decisions/system-overhaul-v1]]"
related:
  - "[[decisions/vault-location]]"
  - "[[decisions/vault-io-strategy]]"
tags:
  - decision
  - research
---

## Decision

Research operations are tiered with hard enforcement:

### Quick Lookup (No TARGET)
- 2-3 pages max, single source
- Use tools directly: Context7, WebFetch, WebSearch
- No pre-registration required

### Deep Research (TARGET REQUIRED)
- Multi-source investigation, 5+ searches
- TARGET file MUST be created before spawning deep-research agent

### TARGET Flow (Automatic)
1. Claude assesses: Is this quick lookup or deep research?
2. If deep: Create TARGET file with focused question, scope, success criteria
3. Spawn deep-research agent
4. On completion: Compare OUTPUT against TARGET, update TARGET status

### TARGET Location
`vault/research/targets/TARGET-{timestamp}-{slug}.md`

### Bidirectional Linking
- OUTPUT frontmatter: `target: "[[research/targets/TARGET-xxx]]"`
- TARGET updated: `status: complete`, `output: "[[research/{timestamp}/findings]]"`

## Rationale

Session 6 LOCKED a TARGET system that was never implemented. The vault redesign (Session 20/21) simplified it away without formal unlocking. This decision restores TARGET with proper enforcement for deep research while allowing quick lookups without ceremony.

The two-tier approach balances:
- Traceability for significant research investments
- Low friction for simple lookups

## Alternatives Considered

1. **No TARGET at all** — Current state. Lost traceability between questions and findings.
2. **TARGET for everything** — Too much ceremony for simple lookups.
3. **Optional TARGET** — No enforcement means it won't be used consistently.
