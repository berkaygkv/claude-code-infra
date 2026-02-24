---
type: research
date: 2026-02-23
topic: "Search the web for best practices and patterns for CLI tool output styling, spec"
---

# Search the web for best practices and patterns for CLI tool output styling, spec

**Question:** Search the web for best practices and patterns for CLI tool output styling, specifically:

1. "Claude Code output formatting" or "Claude Code terminal styling" — any community discussion about formatt...

---

## Findings

Now I have enough material across all five of the requested areas. Let me synthesize.

---

Comprehensive research into CLI output formatting patterns reveals a strong consensus around a small set of battle-tested conventions, with box-drawing Unicode characters being safe on all modern terminals, color serving semantic purposes rather than aesthetic ones, and the context (TTY vs pipe) determining formatting level. The most admired CLI tools—cargo, gh, rich, pnpm—all follow the same underlying logic: heavy formatting for interactive terminals, clean plain text for pipes, and a structured verb/label hierarchy that trades visual density for rapid scanning. Claude Code's own terminal rendering currently displays raw markdown, which the community has flagged as a friction point; there is no built-in renderer yet.

## Research Summary

### Question/Topic
Best practices and concrete patterns for CLI tool output styling in monospace terminals, covering: Claude Code community feedback, exemplary tools (gh, npm, cargo, poetry), Unicode box-drawing compatibility, structured text hierarchy/scanability, and LLM output formatting in terminal contexts.

### Key Findings
1. **Context-first rule**: The single most repeated pattern across all sources is TTY detection. When stdout is a pipe or file, drop all color, borders, and animation. When interactive, use the full palette.
2. **Cargo's verb-label pattern** is the gold standard for status output: right-aligned bold colored verb (12-char padded), then the subject. `   Compiling foo v1.0.0` / `    Finished dev [unoptimized] in 0.3s`.
3. **Unicode box-drawing characters (U+2500–U+257F) are safe** on all modern terminals (macOS Terminal, iTerm2, WezTerm, Alacritty, Windows Terminal, GNOME Terminal). The risk only comes from sub-character block elements (U+1FB00+).
4. **`glow` / Glamour is the reference implementation** for markdown rendering in terminals—Charm's approach is the established pattern Claude Code currently lacks.
5. **The Claude Code community explicitly wants** a markdown renderer toggle. Raw `**bold**` and `## Header` syntax in responses is a documented friction point (GitHub issue #13600).
6. **Color semantics have strong consensus**: red = error, yellow/amber = warning, green = success, cyan/blue = info/progress. Everything else is noise.

---

### Detailed Analysis

#### The Verb-Label Pattern (Cargo / Make-style)

Cargo's output is widely copied because it solves a real information-density problem. The pattern:

```
   Compiling tokio v1.35.0
   Compiling myapp v0.1.0 (/path/to/project)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 4.23s
     Running `target/debug/myapp`
```

Key specifics:
- Status verb is **right-aligned in a fixed 12-character field**, then a space, then the subject.
- Verb is **bold + colored** (green for normal progress, yellow for warning, red for error).
- Subject is unstyled default text—dim secondary info in parens.
- The consistent column width means the eye tracks a single left-aligned content column.

This pattern has been adopted by pnpm, Bun, and several Rust/Go build tools. It works because the label column has fixed visual weight and the content column always starts at the same x offset.

#### gh (GitHub CLI) Output Conventions

From the official formatting documentation:
- Default output is **tab-separated plain text** with no colors when piped.
- In TTY mode: aligned columns with implied spacing (not explicit borders).
- Timestamps use relative format (`about 1 day ago`) not ISO8601—this is a deliberate UX choice.
- The `#123` prefix for numeric references is consistent across all `gh` subcommands.
- Template functions: `autocolor` (color only in TTY), `tablerow` (aligns columns), `timeago`, `truncate`, `hyperlink`.
- Machine output (`--json --jq`) is a first-class concern, not an afterthought.

#### pnpm's "Not Fancy" Philosophy

pnpm explicitly rejected decorative output in favor of *informative minimalism*:
- Shows counts, not logs: `"117 new packages were added"`
- Distinguishes cache hits from network downloads
- Warns about deprecated packages but doesn't stop the output flow
- Multi-package repos get "zoomed out" reporting (counts only) vs single-package (full detail)
- Uses `ansi-diff` for frame-based updates that only redraw changed lines—no flicker

#### Rich (Python) — The Design System

Rich is the most complete reference implementation for terminal design patterns. Its conventions directly inform what "good" looks like:

**Borders** (from most to least visual weight):
- `ThickBorder` — for critical/primary containers
- `DoubleBorder` — for secondary containers
- `RoundedBorder` — softer, for info panels  
- `NormalBorder` — default, for most uses

**Box drawing characters used by Rich:**
- Normal border: `─│┌┐└┘├┤┬┴┼` (all U+2500 range)
- Rounded: `─│╭╮╰╯` (uses U+256D–U+2570)
- Heavy: `━┃┏┓┗┛`
- Double: `═║╔╗╚╝╠╣╦╩╬`

**Rules** (horizontal dividers with optional title):
```
─────────────────── Section Name ────────────────────
```
This is the Rich `rule()` function output. The title centers automatically.

**Text attributes** with semantic conventions:
- `bold` — primary labels, section headers, status verbs
- `dim` / `faint` — secondary/contextual info, timestamps
- `italic` — hints, suggestions, documentation text
- `underline` — hyperlinks only
- Avoid `blink` — poor support and annoying

#### Lipgloss (Go) — Layout Model

Lipgloss uses a CSS flexbox-inspired model:
- Margin: outer space (no background)
- Padding: inner space (with background color)
- Borders: `NormalBorder()`, `RoundedBorder()`, `ThickBorder()`, `DoubleBorder()` or custom
- `JoinHorizontal` / `JoinVertical` for multi-column layouts
- Auto-detects ANSI 16, ANSI 256, or True Color (24-bit) and degrades gracefully

For Claude Code output styles specifically: lipgloss patterns translate well to markdown-in-CLAUDE.md instructions if you think of each instruction as defining a visual slot.

#### Unicode Box-Drawing — What Is Actually Safe

The safe set for cross-terminal use is the **light box-drawing block (U+2500–U+257F)**:

```
Horizontal:   ─  (U+2500)
Vertical:     │  (U+2502)
Top-left:     ┌  (U+250C)
Top-right:    ┐  (U+2510)
Bottom-left:  └  (U+2514)
Bottom-right: ┘  (U+2518)
T-left:       ├  (U+251C)
T-right:      ┤  (U+2524)
T-top:        ┬  (U+252C)
T-bottom:     ┴  (U+2534)
Cross:        ┼  (U+253C)
```

Tree/hierarchy specifically:
```
├── non-terminal child       (U+251C U+2500 U+2500)
└── terminal child           (U+2514 U+2500 U+2500)
│   continuation indent      (U+2502)
```

**What is NOT safe:**
- U+1FB00+ (Symbols for Legacy Computing Supplement, Unicode 13+) — font support is sparse in 2025
- Sub-character block elements for "fancy" borders — rendering varies by font even in modern terminals
- Heavy/double-weight variants in some older Linux terminals (XFCE, st) may render incorrectly

**ASCII fallback** for environments without Unicode (CI logs, legacy terminals):
```
+-- non-terminal
|   +-- child
\-- terminal
```

#### Information Hierarchy in Monospace Contexts

From clig.dev and community consensus, the working hierarchy from most to least visual weight:

1. **Color + Bold** — section headers, primary status, error/warning labels
2. **Bold alone** — important inline values, key names
3. **Color alone** — secondary status indicators, categorical labels
4. **Plain text** — the majority of content
5. **Dim/faint** — secondary details, timestamps, hints

Spacing conventions that consistently improve scanability:
- **Blank line** between logical sections (equivalent to `<hr>` in HTML)
- **2-space indent** per hierarchy level (not 4 — terminal real estate is limited)
- **Hanging indent** for wrapped lines in lists (align second line to text start, not bullet)
- **Right-aligned secondary info** (timestamps, sizes, counts) when in a columnar layout

Section dividers in plain text:
```
# Works well in terminals - high contrast, scannable
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Also works, lower visual weight
────────────────────────────────────────

# Rich-style with title
─────────────── Section ────────────────

# Plain ASCII if Unicode is a concern
========================================
```

#### LLM/AI Output in Terminal Contexts

The Claude Code situation is a documented case study:

**Current state**: Claude Code renders markdown inline but does not transform it. Users see raw `**bold**`, `## headers`, `- [ ]` checkbox syntax.

**Community requests** (GitHub issue #13600):
- Rendered headings with visual weight
- Syntax-highlighted code blocks
- Aligned table borders
- Checkbox rendering from `- [ ]`
- An opt-in `renderMarkdown: true` setting

**What tools like `glow` do differently**: Uses Glamour's ANSI stylesheet to transform markdown:
- `#` H1 → bold + underline + padding + blank line before/after
- `##` H2 → bold + blank line
- `` ```python `` code blocks → syntax highlighted with muted background
- `---` → full-width rule
- Tables → box-drawing bordered grid

**Practical implication for Claude output**: When writing markdown that will display in Claude Code's terminal, the current best approach is to minimize markdown syntax that doesn't render and lean on:
- Blank lines for breathing room (always work)
- Indented code fences (render correctly)
- Plain prose over headers when possible for conversational responses
- Reserve `##` headers for genuinely document-like output

**For custom output style definitions** (`.claude/output-styles/*.md`): Writing markdown instructions that instruct Claude to use symbols rather than markdown syntax can improve readability in the unrendered context:
- Use `>` prefix for quotes/emphasis instead of `**bold**`
- Use labeled sections with `SECTION:` plain-text patterns
- Reserve code blocks for actual code

---

### Limitations & Gotchas

- **Bold ANSI (SGR 1) renders as "brighter color" in many terminals**, not heavier weight. On Solarized themes this means bold cyan becomes a lighter cyan—not visually heavier. This is a known Cargo complaint and why some tools avoid bold for hierarchy.
- **Dim/faint (SGR 2) has inconsistent support** — not implemented in some terminals at all. Test before relying on it.
- **Italic (SGR 3) renders as reverse-video in some older terminals** — treat as unreliable for anything except modern emulators (iTerm2, WezTerm, Kitty).
- **Windows compatibility is the main Unicode risk zone**: Windows Terminal (modern) handles the U+2500 box-drawing range fine. PowerShell ISE and older cmd.exe do not.
- **`glow` and `mdcat` have diverging support profiles**: `mdcat` needs Kitty/iTerm2 for image support; `glow` works in any terminal but renders inline without a pager unless passed `-p`.
- **Animations/spinners pollute CI logs**. Never output ANSI animations when stdout is not a TTY. The community consensus on this is absolute.
- **Color-only information fails accessibility** (color blindness, high-contrast modes). Always pair color with a symbol or text label: `[ERROR]` not just red text.
- **The cargo bold-color issue**: Cargo's green bold status verbs were reported to be illegible in Solarized themes. The resolution was to rely on user theme customization rather than adding config options—which means if you ship a tool, you can't fully control the visual output anyway.
- **Claude Code's markdown rendering issue is unresolved** as of 2025. There's no `renderMarkdown` setting in the current schema despite community requests.

---

### Recommendations

1. **Adopt the verb-label pattern for status output**: Right-align the verb in a 12-char field, bold + green, then plain text subject. Works in every tool type—build systems, installers, agents.

2. **Implement TTY detection as the first decision**: `process.stdout.isTTY` (Node), `isatty(1)` (Unix C/shell), `sys.stdout.isatty()` (Python). Format for humans in TTY mode, emit clean plain text otherwise.

3. **Use the U+2500 light box-drawing set and nothing fancier**: Tree structures (`├──`, `└──`, `│`) and panels work reliably. Skip heavy, double, and especially the U+1FB00+ characters.

4. **Follow the color semantic contract**: red=error, yellow=warning, green=success/normal-progress, cyan=info, bold=emphasis. No decorative color.

5. **For Rich/Glamour-style sections**, a titled rule is the cleanest structural divider:
   ```
   ─────────────── Plan ────────────────────
   ```

6. **For Claude output style definitions**: Write instructions that produce symbol-prefixed sections rather than raw markdown headings. E.g.: instruct Claude to use `[OK]`, `[WARN]`, `[ERROR]` labels for status lines rather than markdown bold.

7. **Provide `--json` as a first-class output mode** for any tool that outputs structured data. This is the gh model and it's correct.

8. **Use `glow` as the reference implementation** for how rendered markdown should look in a terminal. If building a terminal-native LLM tool, integrating glamour or a similar renderer is the expected baseline.

9. **Don't rely on bold for hierarchy** — pair bold with color or spacing. Bold-as-bright is a terminal emulator implementation decision outside your control.

10. **Test output on dark and light backgrounds** and on Solarized. These are the two most common failure modes for color choices.

---

### Open Questions

- Whether Claude Code will ship a native `renderMarkdown` toggle (GitHub issue #13600 is open, no timeline)
- Whether lipgloss/charm conventions will become a de facto standard for Go-based CLI tools the way Rich has become for Python ones
- How AI-generated terminal output should handle dynamic width (80-column vs wide terminals)—no consensus found

---

### Sources
1. [Command Line Interface Guidelines — clig.dev](https://clig.dev/) — Most comprehensive practical guide; covers color semantics, output modes, Unicode, error design
2. [gh formatting — GitHub CLI manual](https://cli.github.com/manual/gh_help_formatting) — gh's actual output conventions including template functions and TTY behavior
3. [pnpm's "not fancy" CLI output — DEV Community](https://dev.to/zkochan/the-not-fancy-cli-output-of-pnpm-36ao) — Design philosophy for minimalist-informative output
4. [Node.js CLI Apps Best Practices — lirantal/nodejs-cli-apps-best-practices](https://github.com/lirantal/nodejs-cli-apps-best-practices) — Comprehensive checklist including color, Unicode, piping
5. [charmbracelet/lipgloss — GitHub](https://github.com/charmbracelet/lipgloss) — Go terminal layout and border conventions
6. [charmbracelet/glow — GitHub](https://github.com/charmbracelet/glow) — Reference implementation for markdown rendering in terminals
7. [Box drawing characters — j2r2b.github.io](https://j2r2b.github.io/2020/07/23/text-representation-of-trees.html) — Specific character recommendations for hierarchy/tree structures
8. [Tree/hierarchy characters gist — GeorgeHernandez](https://gist.github.com/GeorgeHernandez/10dcbb5fd6ca8b087d169d5a44d72cd2) — Exact Unicode code points for tree characters
9. [Box drawing terminal "new way" — Hacker News](https://news.ycombinator.com/item?id=33216626) — Practitioner discussion of what works vs breaks in terminal rendering
10. [Cargo bold colors issue — rust-lang/cargo #2290](https://github.com/rust-lang/cargo/issues/2290) — Real-world breakdown of bold ANSI on Solarized themes
11. [Claude Code markdown renderer request — anthropics/claude-code #13600](https://github.com/anthropics/claude-code/issues/13600) — Community feedback on Claude Code's raw markdown output
12. [Claude Code output styles documentation](https://code.claude.com/docs/en/output-styles) — Official docs on how output style files work
13. [Rich Python library — GitHub](https://github.com/Textualize/rich) — Reference design system for terminal formatting including border styles and hierarchy

---

## Sources

1. [Command Line Interface Guidelines — clig.dev](https://clig.dev/)
2. [gh formatting — GitHub CLI manual](https://cli.github.com/manual/gh_help_formatting)
3. [pnpm's "not fancy" CLI output — DEV Community](https://dev.to/zkochan/the-not-fancy-cli-output-of-pnpm-36ao)
4. [Node.js CLI Apps Best Practices — lirantal/nodejs-cli-apps-best-practices](https://github.com/lirantal/nodejs-cli-apps-best-practices)
5. [charmbracelet/lipgloss — GitHub](https://github.com/charmbracelet/lipgloss)
6. [charmbracelet/glow — GitHub](https://github.com/charmbracelet/glow)
7. [Box drawing characters — j2r2b.github.io](https://j2r2b.github.io/2020/07/23/text-representation-of-trees.html)
8. [Tree/hierarchy characters gist — GeorgeHernandez](https://gist.github.com/GeorgeHernandez/10dcbb5fd6ca8b087d169d5a44d72cd2)
9. [Box drawing terminal "new way" — Hacker News](https://news.ycombinator.com/item?id=33216626)
10. [Cargo bold colors issue — rust-lang/cargo #2290](https://github.com/rust-lang/cargo/issues/2290)
11. [Claude Code markdown renderer request — anthropics/claude-code #13600](https://github.com/anthropics/claude-code/issues/13600)
12. [Claude Code output styles documentation](https://code.claude.com/docs/en/output-styles)
13. [Rich Python library — GitHub](https://github.com/Textualize/rich)
