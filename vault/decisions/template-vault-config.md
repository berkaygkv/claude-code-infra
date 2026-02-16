---
type: decision
title: "Template Vault Configuration — MCP + Dynamic Naming"
status: locked
date: 2026-02-16
session: "[[sessions/session-41]]"
tags: [decision]
---

# Template Vault Configuration — MCP + Dynamic Naming

Bundle of two related decisions about how the cookiecutter template configures vault access.

## D1: Obsidian MCP preset in template

The template ships a project-level `.mcp.json` with the Obsidian MCP server pre-configured, pointing at the vault directory. Brain vault is excluded — it's personal/machine-specific and requires separate setup. README documents how to add one.

## D2: Vault directory named after project slug

The vault directory uses `{{ cookiecutter.project_slug }}` instead of the generic `vault/`. This gives each project a meaningful Obsidian vault name. Consequences:

- Hooks use `.obsidian/` auto-discovery instead of hardcoding `vault/` — works for any vault name
- CLAUDE.md removed from `_copy_without_render` — section 7 (Codebase vs Template) stripped, no more literal `{{ }}` in content
- Template CLAUDE.md uses `{{ cookiecutter.project_slug }}` for vault path references
- Commands and protocols in template also use the slug
- Upgrade SKILL.md discovers vault at runtime via `find . -name ".obsidian"`

`project_slug` (hyphenated, no spaces) chosen over `project_name` (may have spaces) for CLI-friendliness.
