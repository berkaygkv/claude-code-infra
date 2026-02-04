---
type: decision
title: I/O Strategy v2 — Hard Constraint
status: locked
date: 2026-02-04
session: "[[sessions/session-24]]"
supersedes: "[[decisions/vault-io-strategy]]"
superseded_by: null
related:
  - "[[decisions/vault-location]]"
tags:
  - decision
---

## Decision

**HARD CONSTRAINT:** Choose tools based on operation type, not convenience.

| Operation | Tool | Examples |
|-----------|------|----------|
| **Direct file access** (known path) | Native Read/Write | Read `vault/state.md`, Write `vault/sessions/session-24.md` |
| **Search & exploration** (discovery) | MCP Obsidian | Find files, list directories, search content, query tags |

### DO
- `Read vault/state.md` — you know the exact path
- `mcp__obsidian__list_directory` — discovering what sessions exist
- `mcp__obsidian__search_notes` — finding notes mentioning "TARGET"

### DO NOT
- `Glob("vault/sessions/*.md")` — use MCP list_directory instead
- `Grep` on vault/ — use MCP search_notes instead

## Rationale

MCP provides Obsidian-native search that understands vault structure, frontmatter, and links. Native Glob/Grep bypass this intelligence. The previous soft guideline was not followed consistently (behavioral failure in Session 24). Making it a hard constraint ensures compliance.

## Alternatives Considered

1. **Soft guideline** — "MCP preferred but native acceptable". Failed in practice.
2. **MCP for everything** — Unnecessary overhead for known-path operations.
