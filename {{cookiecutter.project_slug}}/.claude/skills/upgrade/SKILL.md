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

## Step 0: Discover Vault

Find the Obsidian vault directory by looking for `.obsidian/` inside the project root's children:

```bash
VAULT=$(find . -maxdepth 2 -name ".obsidian" -type d | head -1 | xargs dirname)
```

If not found, fall back to `vault/`. Use `$VAULT` for all vault path references below.

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

**Single files:**

| Source | Target |
|--------|--------|
| `$SOURCE/.claude/settings.json` | `.claude/settings.json` |
| `$SOURCE/.gitignore` | `.gitignore` |

**Dashboard:** The template's dashboard is inside its vault directory. Find it at `$SOURCE/{{cookiecutter.project_slug}}/dashboard.md` (the inner `{{cookiecutter.project_slug}}` is the vault, matching the template structure). Copy it to `$VAULT/dashboard.md`.

**MCP config:** Copy `$SOURCE/.mcp.json` to `.mcp.json`. After copying, check that the vault path in the MCP config matches `$VAULT` (the template uses `{{cookiecutter.project_slug}}` as a placeholder — replace it with the actual vault directory name).

**Detect new additions:** List the full contents of `$SOURCE/` and `$SOURCE/.claude/`. If there are new directories or files not in the table above that are clearly infrastructure (not vault data, not scratch.md, not state.md), copy those too and note them in the summary.

**Do NOT copy:**
- `$SOURCE/CLAUDE.md` — handled separately in Step 3
- `$SOURCE/{{cookiecutter.project_slug}}/state.md` — project-specific
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
3. From the **template**: extract everything from `# Operational Protocol: Symbiotic Partner` to the end. Replace all `{{ cookiecutter.project_slug }}` occurrences with the actual vault directory name (`$VAULT` basename).
4. From the **current project**: extract everything BEFORE `# Operational Protocol: Symbiotic Partner` — this is the project identity to preserve.
5. **Project-specific sections within the protocol**: Some sections may have values unique to this project. For each section in the new protocol:
   - If the current CLAUDE.md has that same section with project-specific customizations, **keep the current project's version** of that section
   - If the section is entirely new in the template, include it
6. Write the merged result: `{project identity} + {updated protocol with project-specific sections preserved}`

---

## Step 4: Diff Schemas

1. Read the NEW schemas from `$SOURCE/.claude/skills/upgrade/references/schemas.md`
2. Read the CURRENT schemas from `.claude/skills/upgrade/references/schemas.md`
3. Compare them. For each file type (state, session, decision, plan, research), identify:
   - **Added fields**: new in template schema, absent in current
   - **Removed fields**: present in current, absent in template schema
   - **Changed fields**: type, required status, or description changed
   - **Content structure changes**: new sections, renamed sections, removed sections
4. The schemas file is already overwritten in Step 2 (it's inside `.claude/skills/`). No separate copy needed.

**If schemas are identical:** Skip to Step 7. Report "schemas unchanged."

---

## Step 5: Migrate Vault Files

For each file type that has schema changes:

### 5a: Discover Files

| Type | Path Pattern |
|------|-------------|
| state | `$VAULT/state.md` (single file) |
| session | `$VAULT/sessions/session-*.md` |
| decision | `$VAULT/decisions/*.md` |
| plan | `$VAULT/plans/*.md` |
| research | `$VAULT/research/*.md` |

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

## Step 6: Alignment Audit

After migration, audit project-specific content for consistency with the upgraded infrastructure. This catches broken cross-references, stale constraints, and structural drift that schema migration alone cannot detect.

Run each checklist item and report **pass**, **warn**, or **fail**:
- **Pass**: consistent, no action needed
- **Warn**: technically valid but worth noting (e.g., many superseded decisions, gaps in session numbering that predate this upgrade)
- **Fail**: inconsistency found — include file path and what's wrong

### 6a: CLAUDE.md Integrity

1. **Section coverage**: All numbered sections from the template protocol are present in the merged CLAUDE.md and correctly numbered (sequential, no gaps, no duplicates)
2. **Vault path consistency**: All vault path references in CLAUDE.md use the same directory name (matching `$VAULT`). No leftover `vault/` references if the vault has been renamed.
3. **Key Paths section**: Every directory listed in the Key Paths section should exist on disk. Flag any listed paths that don't exist and any vault subdirectories that exist but aren't listed

### 6b: Decision Coherence

1. **Status validity**: Every `$VAULT/decisions/*.md` has a `status` field with value `locked` or `superseded`. Any other value (or missing field) is a fail
2. **Supersession forward link**: Every decision with `status: superseded` should have a `superseded_by` field pointing to a file that actually exists in `$VAULT/decisions/`
3. **State constraint references**: All decision wikilinks in `state.md` constraints resolve to existing, non-superseded decision files. A constraint referencing a superseded decision is a fail

### 6c: State.md Consistency

1. **Current session number**: `current_session` value matches the highest N found across `$VAULT/sessions/session-*.md` filenames
2. **Last session link**: `last_session` wikilink resolves to an existing session file
3. **Active plan**: If `active_plan` is non-null, the referenced plan file exists and its `status` is not `completed` or `abandoned`
4. **Task tags**: All task entries use valid tags: `#pending`, `#done`, `#blocked/{id}`, `#in-progress`. Any other tag format is a warn

### 6d: Session Continuity

1. **Sequential numbering**: Session files form a contiguous sequence from 1 to N (no gaps). Missing sessions are a warn (they may predate this project's tracking)
2. **continues_from chain**: Each session N with a `continues_from` field points to session N-1. A broken chain (pointing to wrong session or missing file) is a fail
3. **Decision wikilinks**: All `[[decisions/...]]` wikilinks in session frontmatter resolve to existing decision files

### 6e: Plan Integrity

1. **Phase counts**: For every plan, `phases_done` <= `phases_total`. If violated, **auto-fix** by clamping `phases_done` to `phases_total`
2. **Status consistency**: If `phases_done` == `phases_total`, status should be `completed`. If status is `active` but all phases are done, this is a warn
3. **State.md references**: Every plan referenced as `active_plan` in `state.md` must exist in `$VAULT/plans/`

### 6f: Auto-Fix Rules

Apply fixes automatically for unambiguous issues:
- `phases_done > phases_total` → set `phases_done = phases_total`
- Missing `status` on decisions → set `status: locked` (conservative default)
- `continues_from` missing on sessions → infer `"[[sessions/session-{N-1}]]"` from filename

For ambiguous issues (e.g., constraint referencing superseded decision — should the constraint be removed or updated?), list them for the user without modifying.

### 6g: Report

```
### Alignment Audit
- ✓ CLAUDE.md integrity (3/3 checks passed)
- ⚠ Decision coherence (2/3 passed, 1 warn: 3 superseded decisions)
- ✓ State.md consistency (4/4 checks passed)
- ✗ Session continuity (2/3 passed, 1 fail: session-12 continues_from points to session-10)
- ✓ Plan integrity (3/3 checks passed)

**Auto-fixed:**
- $VAULT/plans/some-plan.md: clamped phases_done from 5 to 4

**Requires attention:**
- $VAULT/sessions/session-12.md: continues_from → [[sessions/session-10]] (expected session-11)
```

---

## Step 7: Validate

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
- ✓ $VAULT/state.md
- ✓ $VAULT/sessions/session-1.md
- ✓ $VAULT/sessions/session-2.md
- ✗ $VAULT/decisions/some-decision.md — missing required field: `tags`
...
```

If any files fail validation, attempt to fix them. If the fix is ambiguous, list the issue and let the user resolve it.

---

## Step 8: Cleanup and Summary

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

### Alignment Audit
- CLAUDE.md integrity: {pass/warn/fail summary}
- Decision coherence: {pass/warn/fail summary}
- State.md consistency: {pass/warn/fail summary}
- Session continuity: {pass/warn/fail summary}
- Plan integrity: {pass/warn/fail summary}
{If auto-fixes applied: list them}
{If issues need attention: list them}

### Validation
- {pass} ✓ / {fail} ✗

---
All changes are unstaged. Review with `git diff` then commit when ready.
```
