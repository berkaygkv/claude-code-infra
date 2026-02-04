---
type: decision
title: Vault I/O Strategy
status: locked
date: 2026-01-22
session: "[[sessions/session-14]]"
supersedes: null
superseded_by: null
related: []
tags:
  - decision
  - infrastructure
---

## Decision
Native Read/Write for content operations, MCP for metadata operations (frontmatter, search, tags, directory listing, delete).

## Rationale
Reduces token overhead on high-frequency ops while preserving MCP's specialized capabilities.
