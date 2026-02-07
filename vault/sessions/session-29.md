---
type: session
session: 29
date: 2026-02-07
mode: brainstorm
topics: [upgrade-skill, template-sync, cookiecutter-drift, vault-migration]
outcome: successful
continues_from: "[[sessions/session-28]]"
decisions: []
---

# Session 29: Upgrade Skill for Template-Driven Project Migration

## Context
Brainstormed how downstream projects should pull updates from the evolving cookiecutter template. Evaluated cruft, git template branches, and custom sync scripts — user proposed an AI-driven Claude Code skill instead. Built the `/upgrade` skill that autonomously clones the template repo, copies infrastructure files, merges CLAUDE.md, diffs schemas, migrates vault files, and validates. Synced skill to both main and template branches.

## Decisions

### Locked
None — skill design is embedded in the artifact itself (`.claude/skills/upgrade/SKILL.md`).

### Open
- Should the upgrade skill support a dry-run mode (show what would change without writing)?
- Should bootstrap instructions be added to the template README?

## Memory
- **Upgrade skill location:** `.claude/skills/upgrade/SKILL.md` — invoked via `/upgrade`
- **Skill is self-upgrading:** Step 2 copies `.claude/skills/` from template, overwriting itself. Step 2 includes instruction to re-read SKILL.md after copy.
- **Template repo default branch is `template`**, not `main`. `main` is the kh dev workspace only.
- **Bootstrap for existing projects:** Must manually fetch SKILL.md from the template branch before first `/upgrade` run. New projects generated from cookiecutter get it automatically.
- **No version tracking by design:** Each `/upgrade` run is a full idempotent sync — "make this project match the latest template."
- **Vault migration is content-safe:** Only frontmatter and section structure change. Human-written narratives are never altered.
- **Plan file created:** `vault/plans/upgrade-skill.md` (draft, used as design reference during build)

## Next Steps
1. Test `/upgrade` on the other machine (existing project generated from cookiecutter)
2. Verify vault migration works correctly with schema differences
3. Add bootstrap instructions to template README
4. Still pending from prior sessions: verify capture-research and export-transcript hooks
5. Still pending: test excalidraw skill on a different diagram type
