---
type: plan
title: "Upgrade Skill — Pull latest template and migrate project"
status: draft
created: 2026-02-07
project: kh
phases_total: 1
phases_done: 0
---

# Upgrade Skill

## Problem Statement

Projects generated from the cookiecutter template drift as the template evolves. There's no automated way to pull the latest infrastructure (skills, hooks, commands, protocols) and migrate vault files to match updated schemas. Currently this is a manual copy-paste process.

## Solution Overview

A Claude Code skill (`/upgrade`) that autonomously:
1. Clones the latest template from GitHub
2. Overwrites infrastructure files
3. Merges CLAUDE.md (preserve project identity, update protocol)
4. Reads new schemas, migrates every vault file to conform
5. Validates, shows summary, waits for user approval

No version tracking. Each run is idempotent — "make this project match the latest template."

---

## Skill File

**Location:** `.claude/skills/upgrade/SKILL.md`

```markdown
---
name: upgrade
description: Pull the latest kh template from GitHub and upgrade the current project — infrastructure files, schemas, vault migration, and validation.
---

# Upgrade Project from Latest Template

Pull the latest cookiecutter template, update infrastructure, migrate vault files to match new schemas.

## Step 1: Clone Latest Template

Clone the template repo (shallow, single branch) into a temp directory:

~~~bash
rm -rf /tmp/kh-upgrade-source
git clone --depth 1 https://github.com/berkaygkv/claude-code-infra.git /tmp/kh-upgrade-source
~~~

The template files live at:
~~~
/tmp/kh-upgrade-source/{{cookiecutter.project_slug}}/
~~~

That literal path (with curly braces) is the directory name. Assign it:
~~~
SOURCE="/tmp/kh-upgrade-source/\{\{cookiecutter.project_slug\}\}"
TARGET="."  (current project root)
~~~

## Step 2: Copy Infrastructure Files (Direct Overwrite)

These files have NO project-specific content. Overwrite completely:

| Source Path | Target Path |
|-------------|-------------|
| `$SOURCE/.claude/skills/` | `.claude/skills/` |
| `$SOURCE/.claude/agents/` | `.claude/agents/` |
| `$SOURCE/.claude/hooks/` | `.claude/hooks/` |
| `$SOURCE/.claude/commands/` | `.claude/commands/` |
| `$SOURCE/.claude/settings.json` | `.claude/settings.json` |
| `$SOURCE/protocols/` | `protocols/` |
| `$SOURCE/scripts/` | `scripts/` |
| `$SOURCE/vault/templates/` | `vault/templates/` |
| `$SOURCE/vault/dashboard.md` | `vault/dashboard.md` |
| `$SOURCE/.gitignore` | `.gitignore` |

Use `cp -r` for directories. Preserve directory structure.

**Important:** If the template introduces NEW directories or files not listed above, copy those too. List the full contents of `$SOURCE/.claude/` and `$SOURCE/` to detect new additions.

## Step 3: Merge CLAUDE.md

CLAUDE.md has two zones:

1. **Project identity** (top of current file) — project name, description, project-specific sections. KEEP THIS.
2. **Operational Protocol** (everything from `# Operational Protocol: Symbiotic Partner` onward in the template) — shared protocol. UPDATE THIS.

### Procedure:

1. Read the current project's `CLAUDE.md`
2. Read the template's `CLAUDE.md` at `$SOURCE/CLAUDE.md`
3. **From the template:** Extract everything starting from `# Operational Protocol: Symbiotic Partner` — this is the new protocol. Ignore the `{{ cookiecutter.* }}` header and the `<!-- SESSION 0 -->` comment.
4. **From the current project:** Extract everything BEFORE `# Operational Protocol: Symbiotic Partner` — this is the project identity.
5. **Project-specific sections within the protocol:** Some sections contain project-specific values (e.g., hardcoded paths, worktree locations in §7 "Codebase vs Template"). For each such section:
   - If the current CLAUDE.md has a version of that section with real project values, KEEP the project's version
   - If the section is new in the template and has no project equivalent, include it with a `<!-- TODO: fill in project-specific values -->` comment
6. **Write the merged result:** Project identity + updated protocol (with project-specific sections preserved)

## Step 4: Read Schema Changes

1. Read the NEW `vault/schemas.md` from `$SOURCE/vault/schemas.md`
2. Read the CURRENT `vault/schemas.md` from `vault/schemas.md`
3. Diff them. Identify for each file type (state, session, decision, plan, research-target, research-output):
   - **New fields** added to frontmatter
   - **Removed fields** no longer in schema
   - **Changed fields** (type change, required status change)
   - **Content structure changes** (new sections, renamed sections)
4. Write the new `vault/schemas.md` to the project (overwrite — this is the source of truth)

If schemas are identical, skip to Step 6.

## Step 5: Migrate Vault Files

For each file type with schema changes:

### 5a: Discover files
- `vault/state.md` — single file
- `vault/sessions/session-*.md` — all session files
- `vault/decisions/*.md` — all decision files
- `vault/plans/*.md` — all plan files
- `vault/research/targets/TARGET-*.md` — all research targets
- `vault/research/*/findings.md` — all research outputs

### 5b: Migrate each file
For every discovered file:

1. Read the file
2. Parse frontmatter (YAML between `---` markers)
3. Apply changes based on the schema diff:
   - **New required field:** Add with sensible default. Infer from file content if possible (e.g., a new `continues_from` field on sessions can be inferred from session number)
   - **New optional field:** Add only if a value can be inferred, otherwise omit
   - **Removed field:** Delete from frontmatter
   - **Type change:** Convert the value
4. Apply content structure changes:
   - **New section:** Add with placeholder content or infer from existing content
   - **Renamed section:** Rename the heading, keep content
   - **Removed section:** Delete
5. Write the updated file

### 5c: Preserve content
**CRITICAL:** Never discard or alter the actual content written by humans — session narratives, decision rationales, plan details. Only modify structure (frontmatter fields, section headings) to match the new schema.

## Step 6: Validate

For every vault file:
1. Read the file
2. Check frontmatter against the new schema:
   - All required fields present?
   - Field types correct?
   - `type` field matches expected value?
3. Check content structure:
   - Expected sections present?
4. Report results:
   - ✓ files that pass
   - ✗ files that fail with specific issues

## Step 7: Cleanup and Summary

1. Remove temp directory:
~~~bash
rm -rf /tmp/kh-upgrade-source
~~~

2. Show a summary:
~~~
## Upgrade Summary

**Template source:** github.com/berkaygkv/claude-code-infra (commit: {hash})

### Infrastructure Updated
- {list of copied files/directories}

### CLAUDE.md
- {what was updated vs preserved}

### Schema Changes
- {list of field changes per file type}

### Vault Files Migrated
- {count} session files
- {count} decision files
- {count} plan files
- state.md

### Validation
- {pass count} ✓ / {fail count} ✗

All changes are unstaged. Review with `git diff`, then commit when satisfied.
~~~
```

---

## Decisions to Lock

1. **Repo URL hardcoded:** `github.com/berkaygkv/claude-code-infra` — this is the single source of truth. If the repo moves, the skill file is the only thing to update.
2. **No version tracking:** Each run is a full sync. Idempotent by design.
3. **CLAUDE.md merge strategy:** Project identity preserved, protocol updated, project-specific protocol sections kept.
4. **Vault migration is content-safe:** Only frontmatter and section structure change. Human-written content is never altered.
