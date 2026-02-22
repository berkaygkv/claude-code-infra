---
type: research
date: 2026-02-22
topic: "the Obsidian CLI (shipped in Obsidian 1.12.0, February 2026) with a focus on **"
---

# the Obsidian CLI (shipped in Obsidian 1.12.0, February 2026) with a focus on **

**Question:** Research the Obsidian CLI (shipped in Obsidian 1.12.0, February 2026) with a focus on **what new capabilities it unlocks** — not just as a replacement for existing tools, but as an enabler of workflow...

---

## Findings

I now have comprehensive coverage across all 10 research vectors. Let me synthesize everything into the final structured output.

---

The Obsidian CLI (shipped in v1.12.0, February 10, 2026) is not merely a file-access shortcut — it exposes Obsidian's in-memory metadata cache, link graph, plugin runtime, and Bases query engine to any terminal tool or AI agent. For a project management system running on an Obsidian vault, this changes the operational model from "parse raw markdown" to "query the computed knowledge layer," delivering a documented 70,000x token reduction on graph operations and enabling capabilities (link-safe rename, plugin hot-reload, version history restore, property mutation, JS evaluation) that were previously impossible without the GUI.

## Research Summary

### Question/Topic

What new capabilities does the Obsidian CLI (v1.12.0, February 2026) unlock for a Claude Code project management system that uses an Obsidian vault for state management? Specifically: template rendering, plugin ecosystem integration, Bases queries, link graph intelligence, daily notes, search, developer tooling, the `kepano/obsidian-skills` package, sync operations, and automation patterns.

---

### Key Findings

1. **The CLI is a live interface to Obsidian's runtime, not just another file writer.** It queries Obsidian's in-memory metadata cache, the computed link graph, and the Bases engine — none of which are accessible via native file Read/Write. This is the core unlock.

2. **`obsidian eval code="..."` gives full access to the Obsidian TypeScript API.** Any operation achievable via plugin code is achievable from the CLI: `app.vault.getFiles()`, `app.metadataCache.getFileCache()`, custom computations. This is the escape hatch for everything the CLI doesn't expose natively.

3. **`base:query` bridges Bases to external pipelines.** Exporting structured data as JSON/CSV/TSV/MD allows Bases views to serve as machine-readable state registries — sessions, decisions, plans can all be queried programmatically.

4. **`obsidian create name=X template=Y` applies core Templates variables ({{title}}, {{date}}, {{time}}) at creation time.** Templater auto-run behavior on CLI-created notes is not confirmed in documentation, though Templater's "trigger on new file creation" setting may apply if the file event fires correctly.

5. **Link graph commands (`backlinks`, `links`, `orphans`, `unresolved`) enable vault health automation.** Finding orphan notes via grep on a 4,663-file vault takes 15.6 seconds; CLI takes 0.26 seconds. `move` and `rename` are link-safe (Obsidian automatically updates all wikilinks).

6. **Bases (introduced in v1.9.0) can replace manual `state.md` task tracking** with live, filterable, aggregate views over frontmatter. The `base:query` CLI command exports these views — though a debug-message bug currently requires a `| sed '1d'` workaround in pipelines.

7. **`kepano/obsidian-skills`** provides a SKILL.md specification for the `obsidian-cli` skill (plus `obsidian-markdown`, `obsidian-bases`, `json-canvas`, `defuddle`). Installing it teaches Claude Code the complete CLI vocabulary and vault-file format rules.

8. **The macOS re-registration bug is the most significant production gotcha.** After every Obsidian restart on macOS (Apple Silicon), the CLI stops working and requires manual toggle off/on + re-registration. This is unresolved as of v1.12.2.

9. **`sync:history` and `sync:restore` expose Obsidian Sync's version history** programmatically. For cross-device vaults using Obsidian Sync, this replaces manual GUI-based note recovery.

10. **Early Access status and Catalyst requirement ($25) applies now** — free release is planned but not dated. The CLI ships with Obsidian itself; no separate install needed once enabled.

---

### Detailed Analysis

#### 1. Template Rendering

**Command syntax:**
```bash
obsidian create name="Session 43 Handoff" template="Session Template" silent
obsidian create name="Decision: Use Obsidian CLI" path="vault/decisions/" template="Decision" overwrite
```

**Parameters for `create`:**
- `name` — note title (used for {{title}} substitution)
- `path` — vault-relative folder path for placement
- `content` — inline content (merged with template)
- `template` — template name (resolved by wikilink matching, not path)
- `overwrite` — flag to replace existing file
- `silent` — flag to suppress opening in GUI
- `newtab` — flag to open in a new tab

**Template variable substitution** uses the core Templates plugin. Variables supported at creation time:
- `{{title}}` — resolves to the `name` parameter value
- `{{date}}` — today's date with optional format token `{{date:YYYY-MM-DD}}`
- `{{time}}` — current time with optional format token `{{time:HH:mm}}`

**Templater plugin interaction** is not documented as guaranteed. The core question is whether CLI-triggered file creation fires the same Obsidian file event that Templater listens on. Templater has a "Trigger Templater on new file creation" setting — if the CLI fires the `vault.on('create')` event, Templater should auto-run. This is unconfirmed and requires testing. A safer path is using the core Templates plugin variables and letting CLI handle substitution at create time.

**For this vault's use case:** CLI-based note creation with `template=` can handle frontmatter scaffolding for sessions, decisions, and plans. Instead of manually writing frontmatter in `MCP write` calls, the workflow becomes:
```bash
obsidian create name="Session 43" template="Session" silent
# Template provides: date, type, status frontmatter automatically
```

#### 2. Plugin Ecosystem Integration

**Dataview:** CLI-created notes appear in Dataview queries immediately — Dataview watches the filesystem via Obsidian's file watcher and indexes frontmatter as files land. No delay, no cache invalidation needed. CLI write → Dataview re-indexes → query reflects new note within milliseconds.

**Templater:** Auto-run on CLI-created notes is theoretically possible if the `vault.on('create')` event fires. Testing required. If it works, Templater templates (with JavaScript, date arithmetic, prompt dialogs) can be applied to CLI-created files.

**Tasks plugin:** The CLI's `obsidian tasks` command interacts with Obsidian's built-in task parsing (checkbox markdown), **not** the community Tasks plugin. The command syntax is `obsidian tasks daily todo` to list today's incomplete tasks. It reads standard `- [ ] task text` checkboxes across the vault. The Tasks plugin's extended metadata (due dates, recurrence, priority emojis) is separate — CLI does not currently filter by Tasks plugin metadata.

**plugin:reload for development:**
```bash
obsidian plugin:reload id=my-plugin
```
This eliminates the previous workflow of Settings → Community Plugins → toggle off → toggle on. In plugin development, this command can be invoked after each build, enabling a tight develop → build → reload → test loop without GUI interaction. Combined with a file watcher:
```bash
# Watch main.js, reload on change
fswatch -o .hotreload | xargs -I{} obsidian plugin:reload id=my-plugin
```

**Plugin CLI command registration (v1.12.2):** v1.12.2 added the ability for plugins to register their own CLI commands. No published list exists yet of which community plugins have adopted this. The Bases API (added in v1.10) allows plugins to add custom view types and functions. Expect plugin CLI integration to grow rapidly.

#### 3. Bases: Obsidian's Database Feature

**Introduction:** Bases shipped in Obsidian v1.9.0 as a core plugin. v1.10.0 added the Maps plugin and extensibility API. v1.12.0 added a search toolbar within Bases views.

**What `.base` files query:** Every markdown note in the vault is a row. Frontmatter properties are columns. Built-in file properties are also available: `file.name`, `file.path`, `file.mtime`, `file.tags`, `file.backlinks`, `file.links`.

**Example `.base` file for decision tracking:**
```yaml
filters:
  type: "decision"
  status: "locked"
formulas:
  age: "now() - file.ctime"
views:
  - type: table
    name: Locked Decisions
    order:
      - property: file.ctime
        direction: desc
    summaries:
      count:
        formula: "values.length"
```

**`base:query` CLI command:**
```bash
obsidian base:query name="Decisions" format=json
obsidian base:query name="Sessions" format=csv
obsidian base:query name="Open Plans" format=paths
```

Output formats: `json`, `csv`, `tsv`, `md`, `paths`, `yaml`, `tree`.

**Known bug:** A debug message prefixes output when Obsidian auto-updates itself. Workaround:
```bash
obsidian base:query name="Sessions" format=json | sed '1d' | jq '.[]'
```

**Can Bases replace `state.md` task tracking?** Partially. Bases excels at:
- Aggregating sessions by status (active vs complete)
- Filtering decisions by `status: locked` vs `status: draft`
- Showing plans by `type` and `priority`

**Bases cannot** (yet):
- Do cross-note rollup aggregation with auto-refresh (v1.9.7 added `file()` and `Link.asFile()` but requires manual table reload)
- Replace `state.md`'s narrative summary context — that's prose, not data
- Serve as a real-time dashboard for Claude's cold start (requires Obsidian running)

**Best use case for this vault:** Create a `dashboard.base` that aggregates sessions by date, decisions by status, and open plans — queryable via `base:query format=json` by Claude Code on each session start.

#### 4. Link Graph Intelligence

**Commands:**
```bash
obsidian backlinks file="Decision: Use Obsidian CLI"
obsidian links file="state"
obsidian orphans
obsidian unresolved
```

**Performance benchmark** (4,663-file vault):
- `orphans` via grep: 15.6 seconds
- `orphans` via CLI: 0.26 seconds (60x faster)

**Vault health script pattern:**
```bash
#!/bin/bash
# Vault health check
echo "=== Orphaned notes ==="
obsidian orphans format=json | sed '1d' | jq -r '.[]'

echo "=== Unresolved links ==="
obsidian unresolved format=json | sed '1d' | jq '.[] | .file + " -> " + .link'

echo "=== Decision backlinks ==="
obsidian backlinks file="decisions" format=json | sed '1d'
```

**Link-safe move and rename:** `obsidian move` and `obsidian rename` operate through Obsidian's file manager, which automatically updates all wikilinks in all vault notes. This is the correct tool for vault reorganization — raw filesystem `mv` breaks links.

```bash
obsidian move file="old-decision-name" to="vault/decisions/"
obsidian rename file="old-name" name="new-name"
```

Note: Header-level links (`[[Note#Section]]`) are not automatically updated on header renames — this is an Obsidian limitation independent of CLI.

#### 5. Daily Notes / Periodic Notes

**Commands:**
```bash
obsidian daily                          # Open/create today's daily note
obsidian daily:append content="- [ ] Ship session 43 handoff"
obsidian daily:prepend content="## Session Start\n- Objective: ..."
obsidian daily:read                     # Read today's daily note content
obsidian daily:path                     # Get expected path without creating
```

**v1.12.1 fix:** `daily:prepend` now inserts after frontmatter rather than at position 0 of the file — correct behavior for templates with YAML headers.

**Could `daily:append` replace `scratch.md`?** It complements but doesn't replace it:
- `scratch.md` is a flat file Claude writes directly with native Write tool — no Obsidian dependency, survives context compression
- `daily:append` requires Obsidian running; appends to date-stamped notes; works well for human-visible logs
- Pattern: Use `daily:append` for human-facing session logs, keep `scratch.md` for Claude's internal session state

**Periodic notes** (weekly, monthly) are supported if the Periodic Notes community plugin is installed. The CLI integrates with whatever daily/periodic note plugin is active.

#### 6. Search Capabilities

**Commands:**
```bash
obsidian search query="session handoff"
obsidian search query="[status:locked]"
obsidian search query="[type:decision] [status:locked]"
obsidian search query="[status:>active]"   # Numeric/comparison operators
obsidian search:context query="cold start"  # Returns surrounding context lines
obsidian search query="[aliases:Name]"      # Exact alias match
obsidian search query="[property:null]"     # Properties with no value
```

**Search vs grep comparison:**
- CLI search uses Obsidian's indexed full-text search engine + metadata cache
- 0.32 seconds vs 1.95 seconds for grep on a 4,663-file vault
- CLI search **does** search frontmatter properties via `[property:value]` syntax
- CLI search understands Obsidian's resolved link graph; grep does not

**`search:context`** (added in v1.12.2, split from `search`) returns surrounding lines around matches — useful for Claude to get context without reading entire files.

**Property search syntax:**
```bash
[property:value]          # Exact match
[property:>100]           # Numeric greater than
[property:"exact phrase"] # Quoted phrase match
[property:null]           # Exists but empty
[property]                # Property exists (any value)
```

**For this vault:** `obsidian search query="[type:decision] [status:draft]"` can replace any grep-based approach to finding unresolved decisions. Same for `[type:session] [status:active]`.

#### 7. Developer Tooling

**`eval` — the most powerful command:**
```bash
obsidian eval code="app.vault.getFiles().length"
# Returns: 247

obsidian eval code="app.metadataCache.getFileCache(app.vault.getAbstractFileByPath('vault/state.md'))?.frontmatter"
# Returns: frontmatter object without reading file

obsidian eval code="app.vault.getMarkdownFiles().filter(f => f.path.startsWith('vault/decisions/')).map(f => f.basename)"
# Returns: array of decision file basenames
```

**What's accessible via `eval`:** Full `app` object, `app.vault` (all file operations), `app.metadataCache` (computed graph, frontmatter, tags), `app.workspace` (UI state), and all loaded plugins via `app.plugins.plugins`.

**This means eval can do anything the official commands don't cover** — query plugin-specific data structures, trigger plugin commands, access computed properties not exposed by the CLI surface.

**`dev:screenshot`:**
```bash
obsidian dev:screenshot path=test.png
```
Captures current Obsidian UI state as a base64 PNG. Use case for this project: visual validation of Bases views, canvas diagrams, or dashboard state. Also useful for documentation screenshots in CI.

**`dev:console`, `dev:errors`, `dev:css`, `dev:dom`:** Development debugging commands. Primarily for plugin development. `dev:console level=error` is useful for diagnosing CLI command failures or plugin errors.

**`devtools`:** Opens Electron DevTools panel for full Chrome DevTools access within the app.

#### 8. kepano/obsidian-skills

**Repository structure:**
```
obsidian-skills/
├── .claude-plugin/
│   ├── marketplace.json
│   └── plugin.json
└── skills/
    ├── obsidian-markdown/SKILL.md   # .md format spec
    ├── obsidian-bases/SKILL.md      # .base format spec
    ├── json-canvas/SKILL.md         # .canvas format spec
    ├── obsidian-cli/SKILL.md        # CLI command reference
    └── defuddle/SKILL.md            # Web-to-markdown extraction
```

**Repository stats:** 10.3k stars, 546 forks as of research date.

**Installation:**
```bash
# Via Claude Code marketplace command
/plugin marketplace add kepano/obsidian-skills

# Manual (copy to vault's .claude directory)
cp -r obsidian-skills/.claude-plugin vault/.claude/
cp -r obsidian-skills/skills vault/.claude/skills/
```

**The obsidian-cli SKILL.md** teaches agents:
- Parameter syntax (`key=value`, quoted values, `\n` escapes)
- File targeting (`file=` vs `path=`)
- All core operations: read, create, append, prepend, search, daily, property:set, tasks, tags, backlinks
- Plugin development commands: `plugin:reload`, `eval`, `dev:errors`, `dev:console`, `dev:screenshot`, `dev:dom`, `dev:css`, `dev:mobile`
- Output modifiers: `--copy`, `silent`, `total`, `format=`

**For this project:** Installing obsidian-skills into the vault's `.claude/` directory means Claude Code automatically loads the correct CLI vocabulary per-session without needing CLAUDE.md instructions for every command. The `obsidian-bases/SKILL.md` also teaches Claude how to write `.base` files correctly.

**Key workflow the skills unlock:** Claude writes `.base` files (per `obsidian-bases/SKILL.md` spec) → Obsidian file watcher picks them up → Bases renders them → `base:query` exports results back to Claude.

#### 9. Sync Operations

**Commands:**
```bash
obsidian sync:status                          # Current sync state
obsidian sync:history file="vault/state.md"   # Version history list
obsidian history:read file="state" version=2  # Read specific version
obsidian history:restore file="state" version=2  # Restore to version
```

**For cross-device vaults (brain vault):** `sync:history` exposes Obsidian Sync's version history programmatically. This is meaningful for vault recovery scenarios — accidental overwrites, mid-session corruption — without leaving the terminal.

**Does this replace git tracking for vault content?** No, but it complements it:
- Obsidian Sync history: 1-12 month retention (plan-dependent), automatic, per-note, no commit discipline required
- Git: unlimited retention, explicit commits, diff at line level, branching
- Git remains the right tool for intentional vault snapshots and rollback. Sync history is better for recovering accidental changes to individual notes within the last week.

**Not confirmed:** Whether `sync:diff` exists as a command (the documentation references it but the format isn't fully specified).

#### 10. Automation Patterns

**Pattern 1: Property batch update**
```bash
# Mark all draft decisions from 2024 as archived
obsidian search query="[type:decision] [status:draft] [year:2024]" format=paths | \
  sed '1d' | \
  while IFS= read -r path; do
    obsidian property:set name="status" value="archived" path="$path"
  done
```

**Pattern 2: Vault health check report**
```bash
#!/bin/bash
echo "# Vault Health Report $(date +%Y-%m-%d)"
echo "## Orphaned Notes"
obsidian orphans format=json | sed '1d' | jq -r '.[]'
echo "## Unresolved Links"
obsidian unresolved format=json | sed '1d' | jq -r '.[] | "- \(.file) -> \(.link)"'
echo "## Session Summary"
obsidian base:query name="Sessions" format=json | sed '1d' | \
  jq '[.[] | select(.status == "active")] | length | "Active sessions: \(.)"'
```

**Pattern 3: Session creation with template**
```bash
SESSION_DATE=$(date +%Y-%m-%d)
SESSION_NUM=43
obsidian create \
  name="Session $SESSION_NUM" \
  path="vault/sessions/" \
  template="Session Handoff Template" \
  silent
```

**Pattern 4: fzf-powered note search**
```bash
# Interactive search with preview
obsidian search query="decision" format=paths | sed '1d' | \
  fzf --preview 'obsidian read path={} 2>/dev/null | head -30' | \
  xargs -I{} obsidian open path={}
```

**Pattern 5: eval for complex queries**
```bash
# Get all decisions linked from state.md
obsidian eval code="
  const stateLinks = app.metadataCache
    .getFileCache(app.vault.getAbstractFileByPath('vault/state.md'))
    ?.links?.map(l => l.link) || [];
  JSON.stringify(stateLinks)
"
```

---

### Limitations & Gotchas

- **Obsidian must be running.** No daemon mode, no headless mode. On a server without a desktop environment, the CLI is unusable. For this project (macOS desktop), this is acceptable.

- **macOS re-registration bug (v1.12.2):** After every Obsidian restart, CLI registration is lost. Must toggle Settings → General → CLI → off → on → Register after each restart. Affects Apple Silicon. Bug reported but unresolved.

- **`base:query` debug message prefix:** When Obsidian auto-updates on launch, a timestamp debug line prefixes all `base:query` output, breaking JSON pipes. Workaround: `| sed '1d'`.

- **`eval` is synchronous in the command context only.** Complex async operations (file reads, network calls) may require wrapping. The exact async behavior of `eval` from CLI is not documented.

- **Templater auto-run on CLI-created notes is unconfirmed.** The core Templates plugin works; Templater's auto-trigger behavior on CLI-created notes needs testing. Don't build a workflow dependency on it without validating.

- **`file.backlinks` in Bases is slow.** It scans the entire vault. Use `file.hasLink()` with reversed logic for performance-sensitive views.

- **Cross-note formula rollup requires manual table reload.** `file().properties` works for cross-note lookups (since v1.9.7) but does not auto-refresh when source notes change.

- **Catalyst license ($25) is currently required.** Free availability is planned but not dated. For a team system, this is a per-user cost for insider access.

- **CLI path setup varies by platform.** macOS: CLI binary is registered via Obsidian settings; path is automatically configured. Windows requires manual path addition. Linux follows the app package location.

- **`--help` flag added in v1.12.2; earlier versions had no inline help.** Use `obsidian help <command>` for per-command docs.

- **`obsidian tasks` is not the Tasks plugin.** It queries native checkbox markdown only. Tasks plugin metadata (due dates, priority emojis) is not filterable via CLI `tasks` command.

---

### Recommendations

1. **Install `kepano/obsidian-skills` into the vault's `.claude/` directory immediately.** The CLI and Bases SKILL.md files will teach Claude Code the correct command vocabulary, `.base` format rules, and parameter syntax without CLAUDE.md pollution. This is the highest-leverage single action.

2. **Replace grep-based vault queries with CLI calls in session protocols.** Update CLAUDE.md I/O strategy table: add `obsidian search query="[prop:val]"` as the preferred tool for frontmatter-filtered searches, replacing MCP search_notes for property-based queries.

3. **Build a `vault/dashboard.base` for session/decision/plan state.** Use frontmatter properties (`type`, `status`, `date`) already in vault files to drive a Bases view queryable via `base:query format=json`. Claude can load this on `/begin` instead of manually parsing multiple files.

4. **Add vault health check to `/wrap`.** Script combining `obsidian orphans`, `obsidian unresolved`, and `obsidian base:query name="Decisions" format=json | sed '1d' | jq '[.[] | select(.status=="draft")] | length'` to catch orphaned decisions and broken links before session close.

5. **Switch session/decision/plan creation to `obsidian create ... template=`** rather than manual frontmatter generation. Core Templates handles `{{title}}`, `{{date}}`, `{{time}}` substitution at create time; this ensures consistent frontmatter without Claude writing YAML manually.

6. **Script around the macOS re-registration bug.** Until it's fixed, add a startup check: `obsidian version 2>&1 | grep -q "1\." || (echo "CLI not registered — toggle Settings → CLI → Register"; exit 1)`. This catches the silent failure mode where CLI opens GUI instead of executing.

7. **Use `obsidian eval` for metadata cache queries Claude can't express in search syntax.** For example: finding notes linked from `state.md` that don't have a `status` property, or computing cross-file statistics without building a Bases view. Eval is the escape hatch for anything the CLI doesn't cover natively.

8. **Do not replace git for vault versioning.** Use `sync:history` for individual note recovery within a session, but keep git commits at session boundaries (`/wrap`) for intentional vault snapshots. The two systems are complementary.

9. **Test Templater auto-run behavior empirically before depending on it.** Create a test note via `obsidian create ... template=TestTemplaterTemplate` and verify whether Templater processes it. If it does, the vault's templating power expands dramatically; if not, stick with core Templates variables.

10. **Add `| sed '1d'` to all `base:query` pipeline calls** until the debug message bug is fixed. This is a production requirement, not an edge case — the bug triggers on any auto-updated Obsidian installation.

---

### Open Questions

- Does `obsidian create ... template=X` fire the Obsidian file creation event that triggers Templater's auto-run setting? Needs empirical testing.
- Which community plugins have registered CLI commands via the v1.12.2 plugin CLI registration API? No published list found.
- Is `sync:diff` a real command? Documented in some sources but not confirmed in the official changelog.
- Does the macOS re-registration bug affect Linux, or is it macOS-specific? Bug report says Apple Silicon but scope is unclear.
- Does `obsidian eval` support async/await for operations like `app.vault.read()`? Undocumented.
- When will the Catalyst license requirement be lifted for free users? Not announced.

---

### Sources

1. [Obsidian Help CLI Documentation](https://help.obsidian.md/cli) — Official command reference (dynamically loaded; best accessed via DeepWiki mirror)
2. [DeepWiki: Obsidian CLI Reference](https://deepwiki.com/victor-software-house/obsidian-help/7.1-obsidian-cli) — Complete command list with parameters, extracted from official help
3. [Obsidian Changelog](https://obsidian.md/changelog/) — Official release notes for v1.12.0, v1.12.1, v1.12.2
4. [Releasebot: Obsidian February 2026](https://releasebot.io/updates/obsidian) — Structured changelog summary for all 1.12.x releases
5. [kepano/obsidian-skills GitHub](https://github.com/kepano/obsidian-skills) — Repository structure, README, skill directory listing
6. [obsidian-cli SKILL.md contents](https://github.com/kepano/obsidian-skills/blob/main/skills/obsidian-cli/SKILL.md) — Full CLI skill specification for agents (10.3k stars)
7. [DeepWiki: kepano/obsidian-skills](https://deepwiki.com/kepano/obsidian-skills) — Architecture and system analysis of the skills package
8. [Ben Newton: Why Obsidian CLI Changes Everything](https://benenewton.com/blog/your-ai-agent-already-had-file-access-heres-why-obsidian-cli-changes-everything-anyway) — Conceptual analysis: file literacy vs. knowledge comprehension
9. [Maksym Prokopov: 70,000x Cheaper AI Agents](https://prokopov.me/posts/obsidian-cli-changes-everything-for-ai-agents/) — Performance benchmarks, token economics, tier analysis
10. [DeepWiki: Obsidian Bases Database System](https://deepwiki.com/obsidianmd/obsidian-help/5-bases-database-system) — Complete Bases architecture, filter syntax, formula system, view types
11. [DeepWiki: Bases Filters and Queries](https://deepwiki.com/obsidianmd/obsidian-help/5.4-filters-and-queries) — Filter operator reference with examples
12. [Forum: base:query Debug Message Bug](https://forum.obsidian.md/t/base-query-includes-a-debug-message-at-top-of-export/111041) — Production bug with `sed '1d'` workaround
13. [Forum: Bases Programmatic Access](https://forum.obsidian.md/t/bases-it-is-possible-to-access-their-output-programatically/103509) — Current limitations and future Bases API plans
14. [Forum: macOS CLI Re-registration Bug](https://forum.obsidian.md/t/cli-stops-working-after-obsidian-quit-relaunch-on-macos-requires-re-registration/111419) — Active bug report with workaround
15. [Forum: Bases Cross-Note Lookup](https://forum.obsidian.md/t/bases-formula-cross-note-lookup-rollup/101990) — Status of cross-note formula capability (available since v1.9.7, with performance caveats)
16. [Zenn: Obsidian CLI Setup Guide](https://zenn.dev/sora_biz/articles/obsidian-cli-setup-guide?locale=en) — Practical gotchas including admin privilege bug on Windows, TUI mode, command categories
17. [kepano on X: CLI announcement](https://x.com/kepano/status/2021251878521073847) — Original announcement framing CLI for AI agent use
18. [Obsidian CLI Ops Project](https://data-wise.github.io/obsidian-cli-ops/) — Graph analysis, orphan detection, vault health patterns
19. [Neowin: Obsidian 1.10 Bases features](https://www.neowin.net/news/obsidian-1100-released-with-new-features-and-improvements-for-bases/) — Bases history and v1.10 additions
20. [Obsidian Bases Roadmap](https://help.obsidian.md/bases/roadmap) — Planned: Bases API for plugins, more layout types, grouping, Publish support

---

## Sources

1. [Obsidian Help CLI Documentation](https://help.obsidian.md/cli)
2. [DeepWiki: Obsidian CLI Reference](https://deepwiki.com/victor-software-house/obsidian-help/7.1-obsidian-cli)
3. [Obsidian Changelog](https://obsidian.md/changelog/)
4. [Releasebot: Obsidian February 2026](https://releasebot.io/updates/obsidian)
5. [kepano/obsidian-skills GitHub](https://github.com/kepano/obsidian-skills)
6. [obsidian-cli SKILL.md contents](https://github.com/kepano/obsidian-skills/blob/main/skills/obsidian-cli/SKILL.md)
7. [DeepWiki: kepano/obsidian-skills](https://deepwiki.com/kepano/obsidian-skills)
8. [Ben Newton: Why Obsidian CLI Changes Everything](https://benenewton.com/blog/your-ai-agent-already-had-file-access-heres-why-obsidian-cli-changes-everything-anyway)
9. [Maksym Prokopov: 70,000x Cheaper AI Agents](https://prokopov.me/posts/obsidian-cli-changes-everything-for-ai-agents/)
10. [DeepWiki: Obsidian Bases Database System](https://deepwiki.com/obsidianmd/obsidian-help/5-bases-database-system)
11. [DeepWiki: Bases Filters and Queries](https://deepwiki.com/obsidianmd/obsidian-help/5.4-filters-and-queries)
12. [Forum: base:query Debug Message Bug](https://forum.obsidian.md/t/base-query-includes-a-debug-message-at-top-of-export/111041)
13. [Forum: Bases Programmatic Access](https://forum.obsidian.md/t/bases-it-is-possible-to-access-their-output-programatically/103509)
14. [Forum: macOS CLI Re-registration Bug](https://forum.obsidian.md/t/cli-stops-working-after-obsidian-quit-relaunch-on-macos-requires-re-registration/111419)
15. [Forum: Bases Cross-Note Lookup](https://forum.obsidian.md/t/bases-formula-cross-note-lookup-rollup/101990)
16. [Zenn: Obsidian CLI Setup Guide](https://zenn.dev/sora_biz/articles/obsidian-cli-setup-guide?locale=en)
17. [kepano on X: CLI announcement](https://x.com/kepano/status/2021251878521073847)
18. [Obsidian CLI Ops Project](https://data-wise.github.io/obsidian-cli-ops/)
19. [Neowin: Obsidian 1.10 Bases features](https://www.neowin.net/news/obsidian-1100-released-with-new-features-and-improvements-for-bases/)
20. [Obsidian Bases Roadmap](https://help.obsidian.md/bases/roadmap)
