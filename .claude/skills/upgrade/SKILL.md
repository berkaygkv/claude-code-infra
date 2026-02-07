---
name: upgrade
description: Pull the latest kh template from GitHub and upgrade the current project — copy infrastructure files, merge CLAUDE.md, migrate vault files to match new schemas, and validate.
context: fork
disable-model-invocation: true
---

# Upgrade Project from Latest Template

Pull the latest cookiecutter template, update all infrastructure, migrate vault files to new schemas.

**Principles:**
- Each run is a full sync — no version tracking, idempotent
- Infrastructure files are overwritten completely
- Vault content (human-written narratives) is NEVER altered — only structure (frontmatter, section headings)
- Everything stays unstaged — user reviews with `git diff` before committing

---

## Step 1: Clone Latest Template

```bash
rm -rf /tmp/kh-upgrade-source
git clone --depth 1 https://github.com/berkaygkv/claude-code-infra.git /tmp/kh-upgrade-source
```

The template files are at the literal path (curly braces are the actual directory name):

```bash
SOURCE="/tmp/kh-upgrade-source/{{cookiecutter.project_slug}}"
```

Verify this directory exists before proceeding. If it doesn't, the template structure may have changed — abort and report.

Record the commit hash for the summary:
```bash
git -C /tmp/kh-upgrade-source rev-parse --short HEAD
```

---

## Step 2: Copy Infrastructure Files

These files have NO project-specific content. Overwrite completely using `cp -r`.

**Directories (recursive copy):**

| Source | Target |
|--------|--------|
| `$SOURCE/.claude/skills/` | `.claude/skills/` |
| `$SOURCE/.claude/agents/` | `.claude/agents/` |
| `$SOURCE/.claude/hooks/` | `.claude/hooks/` |
| `$SOURCE/.claude/commands/` | `.claude/commands/` |
| `$SOURCE/protocols/` | `protocols/` |
| `$SOURCE/scripts/` | `scripts/` |
| `$SOURCE/vault/templates/` | `vault/templates/` |

**Single files:**

| Source | Target |
|--------|--------|
| `$SOURCE/.claude/settings.json` | `.claude/settings.json` |
| `$SOURCE/vault/dashboard.md` | `vault/dashboard.md` |
| `$SOURCE/.gitignore` | `.gitignore` |

**Detect new additions:** List the full contents of `$SOURCE/` and `$SOURCE/.claude/`. If there are new directories or files not in the table above that are clearly infrastructure (not vault data, not scratch.md, not state.md), copy those too and note them in the summary.

**Do NOT copy:**
- `$SOURCE/CLAUDE.md` — handled separately in Step 3
- `$SOURCE/vault/state.md` — project-specific
- `$SOURCE/vault/schemas.md` — handled separately in Step 4
- `$SOURCE/scratch.md` — session-scoped
- Any `.gitkeep` files into directories that already have content

**CRITICAL:** After copying, you MUST re-read this SKILL.md file since it was just overwritten by the copy. If the new version has different instructions, follow those instead. If it's the same, continue.

---

## Step 3: Merge CLAUDE.md

CLAUDE.md has two zones:

### Zone 1: Project Identity (KEEP)
Everything in the current project's CLAUDE.md that comes BEFORE `# Operational Protocol: Symbiotic Partner`. This includes the project name, description, and any project-specific preamble.

If the current CLAUDE.md starts directly with `# Operational Protocol`, then there is no project identity header — that's fine, skip this zone.

### Zone 2: Operational Protocol (UPDATE from template)
Everything from `# Operational Protocol: Symbiotic Partner` onward in the template CLAUDE.md. This is the shared protocol.

### Merge Procedure

1. Read the current project's `CLAUDE.md`
2. Read the template's `$SOURCE/CLAUDE.md`
3. From the **template**: extract everything from `# Operational Protocol: Symbiotic Partner` to the end. Strip any `{{ cookiecutter.* }}` lines and the `<!-- SESSION 0 -->` comment block from the top.
4. From the **current project**: extract everything BEFORE `# Operational Protocol: Symbiotic Partner` — this is the project identity to preserve.
5. **Project-specific sections within the protocol**: Some sections have values unique to this project (e.g., §7 "Codebase vs Template" may have hardcoded worktree paths, project names, absolute paths). For each section in the new protocol:
   - If the current CLAUDE.md has that same section with project-specific values (paths, project names, branch names), **keep the current project's version** of that section
   - If the section is entirely new in the template, include it. If it contains placeholder values or cookiecutter vars, add `<!-- TODO: fill in project-specific values -->` next to them
6. Write the merged result: `{project identity} + {updated protocol with project-specific sections preserved}`

---

## Step 4: Diff Schemas

1. Read the NEW `vault/schemas.md` from `$SOURCE/vault/schemas.md`
2. Read the CURRENT `vault/schemas.md` from `vault/schemas.md`
3. Compare them. For each file type (state, session, decision, plan, research-target, research-output), identify:
   - **Added fields**: new in template schema, absent in current
   - **Removed fields**: present in current, absent in template schema
   - **Changed fields**: type, required status, or description changed
   - **Content structure changes**: new sections, renamed sections, removed sections
4. Overwrite `vault/schemas.md` with the template version (this is the new source of truth)

**If schemas are identical:** Skip to Step 6. Report "schemas unchanged."

---

## Step 5: Migrate Vault Files

For each file type that has schema changes:

### 5a: Discover Files

| Type | Path Pattern |
|------|-------------|
| state | `vault/state.md` (single file) |
| session | `vault/sessions/session-*.md` |
| decision | `vault/decisions/*.md` |
| plan | `vault/plans/*.md` |
| research-target | `vault/research/targets/TARGET-*.md` |
| research-output | `vault/research/*/findings.md` |

List all matching files. Skip `.gitkeep` and directories.

### 5b: Migrate Each File

For every file of a changed type:

1. **Read** the file completely
2. **Parse** frontmatter (YAML between `---` markers) and content (everything after second `---`)
3. **Apply frontmatter changes:**
   - **Added required field**: Set a sensible default. Infer from file content when possible. Examples:
     - `continues_from` on sessions: infer from session number (session N → `"[[sessions/session-{N-1}]]"`)
     - Date fields: use file's existing date
     - String fields: use `""` if truly unknown
   - **Added optional field**: Only add if a value can be confidently inferred. Otherwise omit.
   - **Removed field**: Delete from frontmatter
   - **Type change**: Convert the value to the new type
4. **Apply content structure changes:**
   - **New section**: Add the section heading with placeholder or infer from existing content
   - **Renamed section**: Rename the heading, preserve all content underneath
   - **Removed section**: Delete the heading and its content
5. **Write** the updated file

### 5c: Content Safety Rules

**NEVER** alter:
- Session narratives (Context, Decisions, Memory, Next Steps content)
- Decision rationales and alternatives
- Plan descriptions and phase details
- Research findings and sources
- Any human-written prose

**ONLY** modify:
- Frontmatter field names, values, and structure
- Section headings (rename/add/remove to match schema)
- Structural markdown (heading levels, section order)

---

## Step 6: Validate

For every vault file (all types):

1. Read the file
2. Check frontmatter against new schema:
   - All required fields present?
   - Field values are correct types?
   - `type` field matches expected value for this file type?
3. Check content structure:
   - Expected sections present?
   - Section headings match schema template?
4. Collect results

Report:
```
### Validation Results
- ✓ vault/state.md
- ✓ vault/sessions/session-1.md
- ✓ vault/sessions/session-2.md
- ✗ vault/decisions/some-decision.md — missing required field: `tags`
...
```

If any files fail validation, attempt to fix them. If the fix is ambiguous, list the issue and let the user resolve it.

---

## Step 7: Cleanup and Summary

```bash
rm -rf /tmp/kh-upgrade-source
```

Display:

```
## Upgrade Complete

**Source:** github.com/berkaygkv/claude-code-infra @ {commit-hash}

### Infrastructure Updated
- {list each directory/file that was copied}
- {note any NEW files/dirs detected}

### CLAUDE.md
- Protocol sections updated from template
- Project identity preserved
- {list any project-specific sections kept}
- {list any TODO items for user to fill in}

### Schema Changes
{For each file type with changes:}
- **{type}**: {summary — e.g., "added `continues_from` field, removed `foo` field"}

{If no changes: "Schemas unchanged — no migration needed."}

### Vault Migration
- {count} state files migrated
- {count} session files migrated
- {count} decision files migrated
- {count} plan files migrated
- {count} research files migrated

### Validation
- {pass} ✓ / {fail} ✗

---
All changes are unstaged. Review with `git diff` then commit when ready.
```
