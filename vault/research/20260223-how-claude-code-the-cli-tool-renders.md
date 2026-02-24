---
type: research
date: 2026-02-23
topic: "how Claude Code (the CLI tool) renders output in the terminal. I need to unders"
---

# how Claude Code (the CLI tool) renders output in the terminal. I need to unders

**Question:** Research how Claude Code (the CLI tool) renders output in the terminal. I need to understand:

1. What markdown features are supported and how they render (headers, bold, italic, code blocks, lists, h...

---

## Findings

Now let me create a comprehensive research file on Claude Code terminal rendering based on my findings.

Based on my thorough research, here's what I found about **Claude Code's terminal markdown rendering capabilities**:

## Summary: Claude Code Terminal Output Rendering

### 1. Current Rendering Architecture

**The Core Issue:** Claude Code CLI displays **raw markdown syntax** rather than rendered formatting. When Claude generates output, users see literal markdown characters (`**bold**`, `# Header`, triple backticks for code blocks, etc.) instead of visually formatted text. This is documented as a feature request (not yet implemented) in the GitHub issue tracker.

### 2. Markdown Features: What's Supported vs What's Not

**Technically Supported in Markdown Generation:**
- Headers (all levels)
- Bold and italic text (`**bold**`, `*italic*`)
- Code blocks (with language tags)
- Inline code
- Lists (ordered and unordered)
- Blockquotes
- Horizontal rules
- Tables
- Links

**What Gets Rendered in the Terminal:**
- **Syntax highlighting in code diffs** (native build only) — Claude uses a dedicated syntax highlighting engine for diff view
- **Inline code highlighting** — Some minimal highlighting in certain contexts
- **Link detection** — Links can be made clickable in some terminals
- **ANSI color codes** (with caveats — see below)
- **Unicode box drawing characters** — For UI elements (input boxes, dividers)

**What Does NOT Get Rendered:**
- **Markdown bold/italic** — Shows as raw `**text**` and `*text*`
- **Headers** — Show as raw `# Header` without visual hierarchy
- **Blockquotes** — Show as raw `> text` without visual formatting
- **Horizontal rules** — Show as raw `---` without visual line
- **Tables** — Display with formatting issues (misaligned columns, especially with Unicode/CJK characters)
- **List formatting** — Shows as raw markdown without indentation adjustments

### 3. Special Rendering Features Beyond Standard Markdown

**What Claude Code DOES Have:**
- **Syntax highlighting in diffs** (native build only) — Colored code with improved language support
- **Theme-aware coloring** — Adapts to light/dark terminal backgrounds via `/theme` and `/config`
- **Unicode support** — Box drawing characters (⏵, ┌, ─, etc.) for UI elements
- **ANSI escape codes** — For colors and text styles (with issues — see below)
- **24-bit truecolor support** — If terminal advertises via `COLORTERM=truecolor`
- **Terminal auto-detection** — Adapts colors based on `$TERM` and `COLORTERM` variables

**What's Missing:**
- No markdown-to-ANSI rendering engine (unlike tools like `glow`, `bat`, or `rich`)
- No dedicated markdown formatter for terminal output
- No CommonMark rendering pipeline

### 4. Known Limitations & Rendering Issues

**ANSI Color Code Problems:**

1. **Character Misalignment** — ANSI escape codes leak into adjacent characters
   - Random blue/purple letters appear in non-formatted text
   - Random bold (bright white) characters show up unexpectedly
   - Issue #20126: "Terminal rendering bugs: inconsistent bolding and blue text coloring"
   - Issue #25346: "ANSI escape codes leak color/bold into adjacent characters on Windows Terminal"

2. **Line Wrapping Issues** — Claude Code splices ANSI codes when output wraps
   - Part of an ANSI escape sequence prints mid-line
   - Causes color codes to bleed across line boundaries
   - Issue #13441: "Claude Code splices ANSI color codes when wrapping stdout"

3. **Chunk Boundary Problems** — Codes misalign based on streaming chunks
   - Issue #20827: "Intermittent Markdown Formatting Misalignment"
   - Random 2-4 character spans get styled incorrectly

4. **Windows-Specific Bugs** — `\r\n` line endings cause code misalignment
   - Fixed in recent versions but can still occur in edge cases

**Table Rendering Issues:**
- Issue #14641: Tables render with broken layout and truncated text in terminal
- Issue #11274: CJK (Chinese/Japanese/Korean) characters cause column misalignment
- Issue #11275: Markdown tables render with misaligned columns in web interface
- Workaround: Wrap tables in code blocks to prevent rendering attempts

**Code Block Issues:**
- Issue #20461: Leading spaces added to lines after the first in multi-line code blocks
- Missing language tags on code fences (feature request #4958)

**Unicode Issues:**
- Issue #24102: Unicode symbols render as hex codepoints on Linux without fonts-symbola
- Issue #4404: Box-drawing characters display incorrectly in Windows WSL
- Issue #6094: Unicode character input corruption in terminal

### 5. Syntax Highlighting (Native Build Only)

**Availability:** Syntax highlighting is **only available in the native build** of Claude Code, not in npm/Node.js versions.

**Where It Works:**
- **Diff view** — Main use case for syntax highlighting
- Code blocks in diffs with language-specific coloring
- Improved engine with more language support

**Where It Doesn't Work:**
- Regular markdown code blocks in responses (rendered as raw text)
- Bash command output colored with `--color` flags (codes are stripped/escaped)
- Status lines with ANSI codes (often display raw codes)

**Customization:**
- Use `/config` → Theme to select light/dark mode
- Set `COLORTERM=truecolor` for 24-bit color support
- Configure terminal color capabilities via environment

### 6. CommonMark & Rendering Standards

Claude Code **does not strictly follow CommonMark rendering standards** in the terminal. It:
- Does not render markdown formatting (treats it as raw text)
- Attempts to maintain CommonMark-compatible spacing (blank lines between sections)
- Does not have a dedicated CommonMark parser for terminal output

The closest equivalent would be tools like `glow` or `rich` that have actual markdown-to-terminal rendering engines.

### 7. What Works Well Visually

**Best Practices for Terminal Output:**

✓ **Use raw ASCII art** — Renders perfectly without formatting issues
✓ **Code blocks with language tags** — Syntax highlighting in diffs works
✓ **Inline code with backticks** — Visually distinguishable (though not special formatting)
✓ **Numbered/bulleted lists** — Readable as raw markdown
✓ **Horizontal rules** — Clear separator (e.g., `---` or `===`)
✓ **Blockquotes** — Readable as raw markdown (e.g., `> quote`)
✓ **ANSI colors for UI elements** — Works in theme and status lines (with caveats)

**What Falls Flat:**
✗ **Markdown bold/italic** — Indistinguishable from plain text
✗ **Header hierarchy** — No visual distinction between `# H1` and `## H2`
✗ **Complex tables** — Misaligned, especially with Unicode
✗ **Nested formatting** — Multiple layers of markup become noise
✗ **Colors in plain prose** — Causes misalignment and leakage issues

### 8. Configuration for Better Terminal Rendering

**Terminal Setup:**
```bash
# Enable truecolor support
export COLORTERM=truecolor

# Ensure proper locale for Unicode
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

# Use Claude Code native build (not npm)
# Install via: curl -fsSL https://claude.ai/install.sh | bash
```

**Claude Code Configuration:**
- Run `/terminal-setup` to configure Shift+Enter for multiline input
- Use `/theme` to match your terminal's background (light/dark)
- Use `/config` to adjust rendering and display options
- View syntax highlighting with `/theme` (inside the picker menu use Ctrl+T)

**For Status Lines:**
- Can use ANSI codes (e.g., `\033[32m` for green)
- Terminal must support them; test in `/statusline` command
- May display raw codes if terminal doesn't support them

### 9. Research Artifacts

The official documentation acknowledges:
- Output styles exist but focus on system prompt modification, not terminal rendering
- Terminal configuration page exists but doesn't cover markdown rendering details
- Troubleshooting guide mentions "Markdown formatting issues" but notes these are generation issues, not rendering issues
- Feature request #13600 is the main tracker for markdown renderer support in CLI

### 10. Practical Recommendations for Output Formatting

**If you're designing output for Claude Code users:**

1. **Use raw ASCII structures** — Eschew markdown formatting, go with pure text
2. **Leverage code blocks** — For syntax-highlighted content (native build only)
3. **Use Unicode box drawing carefully** — Test on target terminal before deploying
4. **Minimize ANSI colors** — Use in UI elements, avoid in prose
5. **Tables: avoid or use code blocks** — Don't rely on markdown table rendering
6. **Headers: use ASCII art** — `## Title ##` or line breaks with all caps
7. **Links: use full URLs** — Many terminals can detect and make them clickable
8. **Blockquotes: use indentation** — Plain indentation is more reliable than `>`

---

## Sources

- [FEATURE][CLI] Markdown renderer support in Claude Code CLI](https://github.com/anthropics/claude-code/issues/13600)
- [Terminal rendering bugs: inconsistent bolding and blue text coloring](https://github.com/anthropics/claude-code/issues/20126)
- [Markdown rendering disabled in CLI output](https://github.com/anthropics/claude-code/issues/11885)
- [BUG] Intermittent Markdown Formatting Misalignment](https://github.com/anthropics/claude-code/issues/20827)
- [Code block rendering adds leading spaces to lines after the first](https://github.com/anthropics/claude-code/issues/20461)
- [Markdown tables render incorrectly in terminal (broken layout, truncated text)](https://github.com/anthropics/claude-code/issues/14641)
- [Markdown tables render with misaligned columns in web interface](https://github.com/anthropics/claude-code/issues/11275)
- [Markdown tables render incorrectly with CJK characters (misaligned columns)](https://github.com/anthropics/claude-code/issues/11274)
- [ANSI escape codes leak color/bold into adjacent characters on Windows Terminal](https://github.com/anthropics/claude-code/issues/25346)
- [Claude Code splices ANSI color codes when wrapping stdout](https://github.com/anthropics/claude-code/issues/13441)
- [Unicode symbols render as hex codepoints on Linux without fonts-symbola](https://github.com/anthropics/claude-code/issues/24102)
- [Unicode box-drawing characters display incorrectly in Windows WSL](https://github.com/anthropics/claude-code/issues/4404)
- [BUG] Spurious syntax highlighting colors random words/characters in plain text output](https://github.com/anthropics/claude-code/issues/22255)
- [Claude Code CLI renderer colors itself](https://github.com/anthropics/claude-code/issues/23029)
- [Claude Code - Syntax Highlighting and Terminal Output](https://www.threads.com/@claudeai/post/DSVhg6-kqPZ/)
- [Fixing Claude Code's Flat or Washed-Out Remote Colors](https://ranang.medium.com/fixing-claude-codes-flat-or-washed-out-remote-colors-82f8143351ed)
- [Claude Code Terminal Configuration Guide](https://claudefa.st/blog/guide/terminal-setup-guide)
- [Claude Code - Output Styles Documentation](https://code.claude.com/docs/en/output-styles.md)
- [Claude Code - Terminal Configuration Documentation](https://code.claude.com/docs/en/terminal-config.md)
- [Claude Code - Interactive Mode Documentation](https://code.claude.com/docs/en/interactive-mode.md)
- [Claude Code - Troubleshooting Guide](https://code.claude.com/docs/en/troubleshooting.md)

---

## Sources

1. [Terminal rendering bugs: inconsistent bolding and blue text coloring](https://github.com/anthropics/claude-code/issues/20126)
2. [Markdown rendering disabled in CLI output](https://github.com/anthropics/claude-code/issues/11885)
3. [Code block rendering adds leading spaces to lines after the first](https://github.com/anthropics/claude-code/issues/20461)
4. [Markdown tables render incorrectly in terminal (broken layout, truncated text)](https://github.com/anthropics/claude-code/issues/14641)
5. [Markdown tables render with misaligned columns in web interface](https://github.com/anthropics/claude-code/issues/11275)
6. [Markdown tables render incorrectly with CJK characters (misaligned columns)](https://github.com/anthropics/claude-code/issues/11274)
7. [ANSI escape codes leak color/bold into adjacent characters on Windows Terminal](https://github.com/anthropics/claude-code/issues/25346)
8. [Claude Code splices ANSI color codes when wrapping stdout](https://github.com/anthropics/claude-code/issues/13441)
9. [Unicode symbols render as hex codepoints on Linux without fonts-symbola](https://github.com/anthropics/claude-code/issues/24102)
10. [Unicode box-drawing characters display incorrectly in Windows WSL](https://github.com/anthropics/claude-code/issues/4404)
11. [Claude Code CLI renderer colors itself](https://github.com/anthropics/claude-code/issues/23029)
12. [Claude Code - Syntax Highlighting and Terminal Output](https://www.threads.com/@claudeai/post/DSVhg6-kqPZ/)
13. [Fixing Claude Code's Flat or Washed-Out Remote Colors](https://ranang.medium.com/fixing-claude-codes-flat-or-washed-out-remote-colors-82f8143351ed)
14. [Claude Code Terminal Configuration Guide](https://claudefa.st/blog/guide/terminal-setup-guide)
15. [Claude Code - Output Styles Documentation](https://code.claude.com/docs/en/output-styles.md)
16. [Claude Code - Terminal Configuration Documentation](https://code.claude.com/docs/en/terminal-config.md)
17. [Claude Code - Interactive Mode Documentation](https://code.claude.com/docs/en/interactive-mode.md)
18. [Claude Code - Troubleshooting Guide](https://code.claude.com/docs/en/troubleshooting.md)
19. [claude.ai](https://claude.ai/install.sh)
20. [github.com](https://github.com/anthropics/claude-code/issues/13600)
21. [github.com](https://github.com/anthropics/claude-code/issues/20827)
22. [github.com](https://github.com/anthropics/claude-code/issues/22255)
