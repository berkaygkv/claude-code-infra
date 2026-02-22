---
type: research
date: 2026-02-22
topic: "I need you to thoroughly explore the kepano/obsidian-skills GitHub repository. D"
---

# I need you to thoroughly explore the kepano/obsidian-skills GitHub repository. D

**Question:** I need you to thoroughly explore the kepano/obsidian-skills GitHub repository. Do NOT write any code — just research.

1. Use `gh api repos/kepano/obsidian-skills` to get repo metadata
2. Use `gh api ...

---

## Findings

Excellent. I now have a comprehensive picture. Here is the full research report.

---

## Research Report: `kepano/obsidian-skills`

### Repository Metadata

| Field | Value |
|-------|-------|
| **Owner** | kepano (Steph Ango, CEO of Obsidian) |
| **Stars** | 10,306 |
| **Forks** | 546 |
| **License** | MIT |
| **Created** | 2026-01-02 |
| **Last pushed** | 2026-02-10 |
| **Language** | None (pure documentation) |
| **Description** | "Agent skills for Obsidian. Teach your agent to use Markdown, Bases, JSON Canvas, and use the CLI." |
| **Topics** | claude, clawdbot, cli, codex, defuddle, obsidian, openclaw, opencode, skills |

---

### Full File Tree

```
.claude-plugin/
  marketplace.json
  plugin.json
LICENSE
README.md
skills/
  defuddle/
    SKILL.md
  json-canvas/
    SKILL.md
  obsidian-bases/
    SKILL.md
  obsidian-cli/
    SKILL.md
  obsidian-markdown/
    SKILL.md
```

That is it. 15 tree entries total. No code, no scripts, no `.claude/` directory, no `CLAUDE.md`. This is a pure instruction-only skill repository -- every file is either metadata or Markdown documentation.

---

### README Content (Complete)

The README states this follows the [Agent Skills specification](https://agentskills.io/specification), making it compatible with any skills-compatible agent including Claude Code and Codex CLI.

**Installation methods:**

1. **Marketplace (Claude Code plugin system):**
   ```
   /plugin marketplace add kepano/obsidian-skills
   /plugin install obsidian@obsidian-skills
   ```

2. **Manual for Claude Code:** Copy the repo contents into a `/.claude` folder at the root of your Obsidian vault.

3. **Manual for Codex CLI:** Copy the `skills/` directory into `~/.codex/skills`.

**Five skills are provided:**

| Skill | File Format | Description |
|-------|-------------|-------------|
| `obsidian-markdown` | `.md` | Obsidian Flavored Markdown syntax reference |
| `obsidian-bases` | `.base` | Obsidian Bases (YAML-based dynamic views) |
| `json-canvas` | `.canvas` | JSON Canvas spec for visual canvases |
| `obsidian-cli` | CLI | Obsidian CLI command reference |
| `defuddle` | CLI | Web page content extraction tool |

---

### Complete Skill File Contents

#### 1. `skills/obsidian-markdown/SKILL.md` (10,813 bytes)

Comprehensive reference for Obsidian Flavored Markdown. Covers:

- **Frontmatter:** `name: obsidian-markdown`, triggers on `.md` files or mentions of wikilinks, callouts, frontmatter, tags, embeds
- **Syntax covered:** CommonMark + GFM + LaTeX + Obsidian extensions
- **Wikilinks:** `[[Note]]`, `[[Note|Alias]]`, `[[Note#heading]]`, `[[Note#^block-id]]`, search links `[[##heading]]`
- **Embeds:** `![[Note]]`, `![[image.png|300]]`, `![[audio.mp3]]`, `![[doc.pdf#page=3]]`
- **Callouts:** Full table of 16 callout types with aliases, foldable syntax (`>  [!faq]-`)
- **Properties/Frontmatter:** YAML types (text, number, checkbox, date, list, links), default properties (`tags`, `aliases`, `cssclasses`)
- **Tags:** Inline `#tag`, nested `#nested/tag`, frontmatter tags
- **All standard Markdown:** headings, lists, task lists, tables, code blocks, math (LaTeX), Mermaid diagrams, footnotes, comments (`%%hidden%%`), horizontal rules, HTML
- **Complete example note** at the end demonstrating all features combined

#### 2. `skills/obsidian-bases/SKILL.md` (17,906 bytes -- the largest)

Exhaustive reference for Obsidian Bases (`.base` files). Covers:

- **Frontmatter:** `name: obsidian-bases`, triggers on `.base` files or mentions of Bases, table/card views, filters, formulas
- **Schema:** Complete YAML schema with `filters`, `formulas`, `properties`, `summaries`, `views`
- **Filter syntax:** AND/OR/NOT nesting, operators (`==`, `!=`, `>`, `<`, `>=`, `<=`, `&&`, `||`, `!`)
- **Properties:** Three types -- note properties (frontmatter), file properties (`file.name`, `file.mtime`, etc.), formula properties
- **Formula functions:** Massive function reference covering:
  - Global: `date()`, `duration()`, `now()`, `today()`, `if()`, `min()`, `max()`, `link()`, `list()`, `file()`, `image()`, `icon()`, `html()`
  - String: `contains()`, `lower()`, `replace()`, `split()`, `slice()`, etc.
  - Number: `abs()`, `ceil()`, `floor()`, `round()`, `toFixed()`
  - List: `filter()`, `map()`, `reduce()`, `flat()`, `join()`, `sort()`, `unique()`
  - Date: `format()`, `relative()`, date arithmetic with duration units
  - Duration: `.days`, `.hours`, `.minutes`, `.seconds`, `.milliseconds` (with explicit warning that Duration does NOT support `.round()` directly)
  - File: `hasLink()`, `hasTag()`, `hasProperty()`, `inFolder()`
- **View types:** Table, Cards, List, Map
- **Summary formulas:** 12 built-ins (Average, Min, Max, Sum, Range, Median, Stddev, Earliest, Latest, Checked, Unchecked, Empty, Filled, Unique)
- **Four complete examples:** Task Tracker, Reading List, Project Notes, Daily Notes Index

#### 3. `skills/json-canvas/SKILL.md` (14,401 bytes)

Complete JSON Canvas spec reference. Covers:

- **Frontmatter:** `name: json-canvas`, triggers on `.canvas` files or mentions of canvas, mind maps, flowcharts
- **File structure:** `{"nodes": [], "edges": []}`
- **Four node types:** text, file, link, group -- each with full attribute tables
- **Edges:** `fromNode`, `toNode`, `fromSide`, `toSide`, `fromEnd`, `toEnd`, `color`, `label`
- **Colors:** Hex (`#FF0000`) or presets (`"1"` through `"6"`)
- **ID format:** 16-character lowercase hexadecimal strings
- **Layout guidelines:** positioning, recommended sizes, spacing
- **Validation rules:** uniqueness, referential integrity, valid enums
- **Four complete examples:** Simple text+connections, Project board with groups, Research canvas with files/links, Flowchart
- **Common pitfall documented:** `\n` vs `\\n` in JSON strings (contributed via PR #32)

#### 4. `skills/obsidian-cli/SKILL.md` (2,941 bytes)

Obsidian CLI command reference. Covers:

- **Frontmatter:** `name: obsidian-cli`, triggers on vault interactions, note management, CLI operations, plugin/theme development
- **Syntax conventions:** Parameters with `=`, flags as boolean switches, `\n`/`\t` for multiline
- **File targeting:** `file=<name>` (wikilink-style) vs `path=<path>` (exact vault path)
- **Vault targeting:** `vault="My Vault"` parameter
- **Common patterns:** `read`, `create`, `append`, `search`, `daily:read`, `daily:append`, `property:set`, `tasks`, `tags`, `backlinks`
- **Plugin development commands:** `plugin:reload`, `eval` (run JS in app context), `dev:errors`, `dev:console`, `dev:screenshot`, `dev:dom`, `dev:css`, `dev:mobile`
- **Key tip:** "Run `obsidian help` to see all available commands. This is always up to date."

#### 5. `skills/defuddle/SKILL.md` (1,038 bytes -- the smallest)

Defuddle CLI for web page content extraction. Covers:

- **Frontmatter:** `name: defuddle`, positioned as a better alternative to WebFetch for standard web pages
- **Installation:** `npm install -g defuddle-cli`
- **Usage:** `defuddle parse <url> --md` for Markdown output
- **Output formats:** `--md`, `--json`, no flag (HTML), `-p <name>` (specific metadata)
- **Metadata extraction:** `title`, `description`, `domain`

---

### Claude Code Integration: `.claude-plugin/` Directory

This repo uses the **Claude Code Plugin** system (not the older `.claude/skills/` pattern). Two files:

**`plugin.json`:**
```json
{
  "name": "obsidian",
  "version": "1.0.0",
  "description": "Create and edit Obsidian vault files including Markdown, Bases, and Canvas.",
  "author": {"name": "Steph Ango", "url": "https://stephango.com/"},
  "repository": "https://github.com/kepano/obsidian-skills",
  "license": "MIT",
  "keywords": ["obsidian", "markdown", "bases", "canvas", "pkm", "notes"]
}
```

**`marketplace.json`:**
```json
{
  "name": "obsidian-skills",
  "owner": {"name": "Steph Ango", "url": "https://stephango.com/"},
  "plugins": [
    {
      "name": "obsidian",
      "source": "./",
      "description": "Claude Skills for Obsidian",
      "version": "1.0.0"
    }
  ]
}
```

The `marketplace.json` defines this as a marketplace entry. The `plugins` array maps the `"obsidian"` plugin name to the root of the repo (the `skills/` directory). This is what enables the `/plugin marketplace add` and `/plugin install` commands shown in the README.

**There is no `.claude/` directory and no `CLAUDE.md` in this repo.** The integration is entirely through the Agent Skills specification and the Claude Code plugin marketplace system.

---

### How It's Designed to Work

The architecture follows the **Agent Skills specification** (agentskills.io), which is a standard that works across multiple agent implementations:

1. **Discovery via metadata (Level 1):** Each `SKILL.md` has YAML frontmatter with `name` and `description`. At startup, the agent loads only these lightweight descriptions (~100 tokens each) into its system prompt. This tells it "obsidian-markdown exists and handles `.md` files with wikilinks, callouts, etc." without loading the 10K+ token body.

2. **On-demand activation (Level 2):** When the user's request matches a skill description (e.g., "create a canvas with these ideas"), the agent reads the full `SKILL.md` body into context. Only the relevant skill gets loaded -- not all five.

3. **Progressive disclosure (Level 3):** If a skill had `references/` or `scripts/` directories, those would load only when explicitly needed. This repo keeps everything in `SKILL.md` files directly (no Level 3 content), which is a design choice -- each skill is self-contained.

4. **Distribution via plugin marketplace:** The `.claude-plugin/` directory makes this installable as a Claude Code plugin. Users run two commands and the skills are available globally or per-project.

5. **Cross-agent compatibility:** The repo tags include `codex`, `openclaw`, `opencode`, and `clawdbot`, confirming this works with multiple Agent Skills-compatible runtimes, not just Claude Code.

---

### Workflow Patterns Demonstrated

1. **Pure documentation skills (no code):** Every skill is a Markdown reference document. No scripts, no executables. The agent applies the knowledge by writing correct file formats. This is a "teach the agent the spec" pattern rather than a "give the agent tools" pattern.

2. **Tool delegation via CLI:** The `obsidian-cli` and `defuddle` skills don't implement functionality -- they teach the agent how to call existing CLIs (`obsidian` and `defuddle`). The pattern is: install the CLI separately, then the skill teaches the agent the command vocabulary.

3. **Format-as-skill:** Each file format Obsidian uses (`.md`, `.base`, `.canvas`) gets its own dedicated skill with the complete syntax reference. This means an agent working in an Obsidian vault can create valid files in any format without hallucinating syntax.

4. **Skill description as trigger:** The `description` field doubles as the trigger condition. For example, defuddle's description says "Use instead of WebFetch when the user provides a URL" -- this directly instructs the agent's routing logic.

5. **Minimal packaging, maximum utility:** The entire repo is ~48KB across 5 Markdown files plus 2 JSON metadata files. No build step, no dependencies, no configuration. Copy the files and you're done.

6. **Community-maintained accuracy:** Recent PRs (#32, #35) show the community fixing documentation bugs (JSON newline escaping, Duration type docs). The skills serve as living references that improve over time.

---

## Sources

1. [Agent Skills specification](https://agentskills.io/specification)
2. [stephango.com](https://stephango.com/"})
3. [github.com](https://github.com/kepano/obsidian-skills)
