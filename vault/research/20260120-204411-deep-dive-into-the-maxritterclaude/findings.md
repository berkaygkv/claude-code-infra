---
type: research-output
id: OUTPUT-20260120-204411-deep-dive-into-the-maxritterclaude
target: '[[research/targets/TARGET-20260120-102231-the-best-practices-for-using-claude]]'
created: 2026-01-20
researcher: claude-deep-research
tags:
  - research
---

# Research Output: Deep dive into the maxritter/claude-codepro GitHub repository.

## Context
I'm b

**Target:** [[research/targets/TARGET-20260120-102231-the-best-practices-for-using-claude]]

**Question:** Deep dive into the maxritter/claude-codepro GitHub repository.

## Context
I'm building a "Symbiotic Collaboration Framework" for Claude Code with:
- Session lifecycle management (begin/wrap commands)...

---

## Findings

Let me now compile comprehensive research findings synthesizing all the information gathered.

---

This research investigated the maxritter/claude-codepro GitHub repository, a production-grade development environment for Claude Code that enforces Test-Driven Development, automates quality checks, and provides persistent cross-session memory through a structured workflow system. The analysis reveals a sophisticated architecture with modular rules, MCP-based memory persistence, strict TDD enforcement, and context management strategies that significantly exceed basic Claude Code configurations.

## Research Summary

### Question/Topic
Conduct a comprehensive analysis of the maxritter/claude-codepro repository to understand its architecture, session management, workflow patterns, hooks/automation, unique features, and identify specific patterns that could enhance our Symbiotic Collaboration Framework which currently uses Obsidian vault integration, scratch file staging, Mode 1/Mode 2 distinction, and TARGET/OUTPUT research artifacts.

### Key Findings

1. **Claude-codepro is a comprehensive production system** that transforms Claude Code from a general-purpose assistant into a structured development environment with enforced quality gates, persistent memory, and semantic code understanding.

2. **The architecture uses a modular rules system** where standard best practices are auto-updated while custom project rules remain untouched, enabling consistent team practices without blocking customization.

3. **TDD enforcement is automatic and strict** - code written before failing tests is automatically deleted through pre-edit hooks, forcing true red-green-refactor cycles.

4. **Context management uses a zone-based threshold system** with mandatory memory persistence at 90% usage, preventing context overload through `/remember` (store to vector DB) and `/clear` (reset context) commands.

5. **The spec-driven workflow separates planning from execution** through markdown files in `docs/plans/` that require human review and approval before implementation begins, reducing mid-implementation interruptions.

6. **MCP Funnel architecture solves context bloat** by exposing only 3 gateway tools for on-demand discovery instead of loading all MCP tools upfront, reducing token overhead by 85-90%.

### Detailed Analysis

#### Repository Architecture

**Directory Structure:**
```
claude-codepro/
├── .claude/
│   ├── rules/
│   │   ├── standard/          # Auto-updated best practices
│   │   │   ├── core/          # TDD, context management
│   │   │   ├── workflow/      # Plan, implement, verify rules
│   │   │   └── extended/      # Frontend, backend, testing
│   │   └── custom/            # User rules (never touched)
│   ├── commands/              # Slash command definitions
│   ├── skills/                # Extended capabilities
│   ├── hooks/                 # Pre/post-edit hooks
│   │   ├── file_checker_qlty.py      # General quality
│   │   ├── file_checker_python.py    # Python-specific
│   │   └── tdd_enforcer.py           # Test-first validation
│   └── settings.local.json    # Permissions, MCP config
├── ccp/                       # Core Python application
├── docs/plans/                # Spec-driven markdown plans
├── installer/                 # Installation automation
├── scripts/
│   ├── install.py             # Main installer
│   └── lib/                   # Modular components
│       ├── downloads.py
│       ├── files.py
│       ├── dependencies.py
│       ├── shell_config.py
│       ├── env_setup.py
│       └── migration.py
└── .mcp.json                  # MCP server definitions
```

**Configuration Hierarchy:**
- `.claude/rules/config.yaml` - Command and rule mappings (specifics not publicly documented)
- `.claude/settings.local.json` - Hook triggers, MCP servers, tool permissions
- `.mcp.json` - MCP server process definitions
- `.mcp-funnel.json` - Tool exposure filtering
- `.cipher/config.yml` - Vector DB and LLM configuration

**Installation Architecture:**

The `install.py` script orchestrates modular installation through specialized library components:
- Downloads latest code from GitHub at specific version tags
- Preserves custom rules during updates (never overwrites `.claude/rules/custom/`)
- Detects previous installations and migrates configurations
- Installs dependencies: Node.js v22, uv (Python), qlty (quality), newman (testing)
- Configures shell aliases (`ccp`) for bash/zsh/fish
- Interactive API key setup for Cipher, Ref, OpenAI

#### Session Management and Memory

**Context Monitoring System:**

Claude-codepro implements zone-based context management with specific thresholds:

| Usage Level | Context Remaining | Behavior |
|-------------|-------------------|----------|
| Green | 0-80% | Normal operation |
| Yellow | 80-85% (148k-158k) | Finish current work |
| Orange | 85-90% (158k-168k) | Small fixes only |
| Critical | 90%+ (168k+) | **Mandatory `/remember` + `/clear`** |

**Note:** Claude Code itself doesn't expose these thresholds natively - this is implemented through monitoring and rules enforcement in claude-codepro.

**Persistent Memory Strategy:**

Claude-codepro uses **Cipher MCP** (an external vector database system) for cross-session memory:

1. **Architecture:** Dual memory system
   - **System 1 Memory (Knowledge):** Codebase knowledge, business logic, past interactions
   - **System 2 Memory (Reflection):** AI reasoning steps, problem-solving patterns
   - **Workspace Memory:** Team-shared context across sessions

2. **Workflow at Context Limit:**
   ```
   [90% context threshold reached]
   → Execute `/remember` → Stores current progress in Cipher Vector DB
   → Execute `/clear` → Resets conversation context
   → Resume with `/implement` → Retrieves stored context from Cipher
   ```

3. **Technical Implementation:**
   - Vector DB: Zilliz Cloud (Milvus-based)
   - Configuration: `.cipher/config.yml`
   - Environment variables: `MILVUS_TOKEN`, `MILVUS_ADDRESS`, `OPENAI_API_KEY`
   - Embeddings: OpenAI (configurable)
   - Storage: Persistent across all sessions and projects

**Comparison to Our Framework:**

| Aspect | Our Framework | Claude-codepro |
|--------|---------------|----------------|
| Memory Store | Obsidian vault (markdown files) | Cipher vector DB (embeddings) |
| Retrieval | Manual file reading | Semantic search via MCP |
| Structure | Structured documents (session handoffs, locked decisions) | Unstructured embeddings (conversations, code context) |
| Persistence Trigger | `/wrap` at session end | `/remember` at 90% context |
| Cross-session | Explicit session handoff notes | Automatic vector retrieval |

**Key Insight:** We use explicit, structured memory (markdown documents in Obsidian). They use implicit, semantic memory (vector embeddings in Cipher). These are complementary approaches - ours is better for decisions/agreements, theirs is better for technical context.

#### Workflow Patterns

**Two-Mode System:**

Claude-codepro distinguishes between Quick Mode and Spec-Driven Mode:

| Mode | Model | Use Case | TDD | Planning |
|------|-------|----------|-----|----------|
| **Quick Mode** | Sonnet 4.5 | Bug fixes, refactoring, experiments | Optional | None |
| **Spec Mode** | Opus 4.1 (plan) + Sonnet 4.5 (implement) | Complex features, major changes | Mandatory | Required |

**Spec-Driven Workflow (Three-Phase):**

```
1. /plan (Opus 4.1)
   ↓
   Creates: docs/plans/YYYY-MM-DD-feature-name.md
   ├── Context exploration
   ├── Clarifying questions
   └── Detailed implementation spec
   
2. Human Review & Approval
   ↓
   Edit markdown file if needed
   Approve when ready
   
3. /implement (Sonnet 4.5)
   ↓
   Executes with mandatory TDD
   Quality hooks on every file change
   
4. /verify (Sonnet 4.5)
   ↓
   Runs test suite
   Quality checks
   Security validation
   ↓
   [Pass] → Complete
   [Fail] → Loop back to step 3
```

**Comparison to Our Framework:**

| Aspect | Our Framework | Claude-codepro |
|--------|---------------|----------------|
| Mode Names | Mode 1 (Brainstorming) / Mode 2 (Execution) | Quick Mode / Spec Mode |
| Mode Trigger | Context-based or explicit | Command-based (`/quick` vs `/spec`) |
| Planning Artifact | scratch.md → vault at `/wrap` | `docs/plans/*.md` → approved before execution |
| Approval Gate | No formal approval (human drives conversation) | Explicit approval required between plan and implementation |
| Quality Enforcement | None (relies on human judgment) | Automatic (TDD enforcer, post-edit hooks) |

**Key Insight:** Our modes distinguish *intellectual work* (brainstorming) from *implementation work* (execution). Their modes distinguish *lightweight* (quick) from *heavyweight* (spec-driven) workflows. Our framework could benefit from adding an approval gate between planning and execution for complex features.

#### TDD Enforcement Architecture

**Pre-Edit Hook System:**

Claude-codepro implements strict TDD through a pre-edit hook that intercepts file modification operations:

```python
# Conceptual flow (actual implementation in .claude/hooks/)
def pre_edit_hook(file_path, operation):
    if is_production_code(file_path):
        if not has_failing_test_for_change():
            return BLOCK_EDIT  # Prevents the file write
    return ALLOW_EDIT
```

**Key Mechanisms:**

1. **Automatic Code Deletion:** "Code written before tests gets deleted automatically"
2. **Test Naming Convention:** `test_<function>_<scenario>_<expected_result>`
3. **Verified Failures:** Test failure must be confirmed by actual execution, not assumption
4. **Red-Green-Refactor Cycle:** Enforced through rules in `standard/core/tdd-enforcement.md`

**Integration with Workflow:**

- Quick Mode: TDD optional (configurable)
- Spec Mode (`/implement`): TDD mandatory, cannot be disabled
- Rules: Defined in `standard/workflow/implement.md`

**Alternative Implementation:**

There's also a standalone tool called **TDD Guard** (by a different developer) that provides similar functionality as an MCP server, showing this is a recognized pattern in the Claude Code community.

**Comparison to Our Framework:**

We have no TDD enforcement mechanisms. This is a significant gap if building production code. The pre-edit hook pattern could be valuable for enforcing other disciplines (e.g., "Don't write to vault directly, use scratch.md").

#### Quality Automation Hooks

**Post-Edit Hook System:**

Claude-codepro triggers quality checks immediately after any file modification:

```
File Write/Edit Operation
↓
Hook Triggered (via settings.local.json)
↓
file_checker_qlty.py (all files)
│
├─→ Runs: qlty check <file>
│   ├── Formatting
│   ├── Linting
│   └── Style checks
│
file_checker_python.py (.py files only)
│
└─→ Runs: ruff, mypy, basedpyright
    ├── ruff: Fast linting
    ├── mypy: Type checking
    └── basedpyright: Enhanced type checking

Results appear in conversation context
Claude can fix issues and retry
```

**Hook Configuration (`settings.local.json`):**

```json
{
  "hooks": {
    "PostEdit": [
      ".claude/hooks/file_checker_qlty.py",
      ".claude/hooks/file_checker_python.py"
    ],
    "PreEdit": [
      ".claude/hooks/tdd_enforcer.py"
    ]
  }
}
```

**Key Features:**

- **Immediate Feedback:** Results appear in conversation before Claude continues
- **Auto-Fix Capability:** Claude sees errors and can correct them
- **Language-Specific:** Python gets extra scrutiny (ruff, mypy, basedpyright)
- **TypeScript Support:** eslint, tsc for TypeScript files
- **Universal Quality:** qlty runs on all file types

**Tools Used:**

- **qlty:** Multi-language code quality tool (https://qlty.sh/)
- **ruff:** Fast Python linter/formatter
- **mypy:** Python type checker
- **basedpyright:** Enhanced Python type checker (fork of Pyright)
- **eslint:** JavaScript/TypeScript linter
- **tsc:** TypeScript compiler (type checking mode)

**Comparison to Our Framework:**

We have no post-edit hooks. This would be valuable for ensuring quality of committed changes. Could implement hooks that:
- Validate scratch.md structure before `/wrap`
- Check TARGET/OUTPUT schema compliance
- Enforce Obsidian frontmatter requirements
- Run linters on generated code

#### MCP Server Integration

**Four Core MCP Servers:**

| Server | Purpose | Key Tools | Configuration |
|--------|---------|-----------|---------------|
| **Cipher** | Cross-session memory | `ask_cipher`, `store_context` | `.cipher/config.yml` |
| **Claude Context** | Semantic code search | `search_code`, `index_codebase` | Auto-configured |
| **Ref** | Documentation/web search | `ref_search_documentation`, `ref_read_url` | `REF_API_KEY` |
| **MCP Funnel** | Tool discovery gateway | `discover_tools_by_words`, `bridge_tool_request` | `.mcp-funnel.json` |

**MCP Funnel Architecture (Critical Innovation):**

Traditional MCP problem:
```
4 MCP servers × ~15 tools each = 60 tool definitions
60 tools × ~1000 tokens each = 60,000 tokens of overhead
Before writing a single prompt!
```

MCP Funnel solution:
```
MCP Funnel exposes only 3 tools:
├── discover_tools_by_words(keywords) → Returns relevant tool names
├── bridge_tool_request(tool_name, params) → Executes tool
└── list_available_tools() → Full catalog (rarely used)

Token overhead: ~3,000 tokens (95% reduction)
```

**How it Works:**

1. Claude needs to search code semantically
2. Instead of having `search_code` pre-loaded, Claude calls: `discover_tools_by_words("search code semantic")`
3. MCP Funnel returns: `["claude_context.search_code", "vexor.semantic_search"]`
4. Claude calls: `bridge_tool_request("claude_context.search_code", {...params})`
5. MCP Funnel proxies the request to the actual Claude Context server

**Benefits:**

- 85-90% reduction in context overhead
- Access to full tool library without upfront cost
- Policy-based access control (can restrict tools via `.mcp-funnel.json`)
- Prevents "tool definition bloat" issue plaguing MCP ecosystem

**Comparison to Our Framework:**

We don't currently use MCP Funnel, meaning if we add multiple MCP servers (Obsidian, Context7, deep-wiki, etc.), we'll experience context bloat. This is a high-priority adoption candidate.

#### Semantic Code Search (Vexor)

**Vexor Overview:**

Vexor is a local vector store for semantic code search, providing token-efficient retrieval without external API dependencies.

**Key Features:**

1. **Smart Routing by File Type:**
   - Python/JS/TS → Code mode (AST-aware chunking)
   - Markdown → Outline mode (heading-based structure)
   - Small files → Full mode (entire file)
   - Large files → Head mode (beginning only)

2. **Reranking Options:**
   - `bm25`: Lightweight lexical boost (fast)
   - `flashrank`: Stronger reranking (requires `pip install "vexor[flashrank]"`)

3. **Integration:**
   ```bash
   vexor install --skills claude  # Installs Claude Code integration
   vexor index --path ~/project --mode code
   ```

4. **Usage:**
   - Indexes are persistent and reusable
   - Configurable embedding providers
   - Python API: `from vexor import index, search`

**Comparison to Our Framework:**

We rely on Claude Code's built-in Grep/Glob tools for code search. Vexor adds semantic understanding - can find "authentication logic" without knowing exact variable names. Worth considering for large codebases, but adds complexity.

#### Rules System and Rules Builder

**Modular Rules Architecture:**

```
.claude/rules/
├── config.yaml              # Command → rule mappings (not publicly documented)
├── standard/                # Auto-updated on install
│   ├── core/
│   │   ├── tdd-enforcement.md
│   │   ├── context-management.md
│   │   └── quality-standards.md
│   ├── workflow/
│   │   ├── plan.md         # Injected during /plan
│   │   ├── implement.md    # Injected during /implement
│   │   └── verify.md       # Injected during /verify
│   └── extended/
│       ├── frontend-components.md  # Auto-becomes @frontend-components skill
│       ├── backend-api.md          # Auto-becomes @backend-api skill
│       └── testing-strategy.md     # Auto-becomes @testing-strategy skill
└── custom/                  # User-owned, preserved on updates
    └── project-specific.md
```

**Rules Builder (build.py):**

The Rules Builder reads `config.yaml` and assembles markdown from specified rules:

1. **Command Skills:** Injected when slash commands run
   - `/plan` → Loads `standard/workflow/plan.md`
   - `/implement` → Loads `standard/workflow/implement.md` + `standard/core/tdd-enforcement.md`
   - `/verify` → Loads `standard/workflow/verify.md`

2. **Extended Skills:** One-to-one mapping to `@skill` commands
   - `extended/frontend-components.md` → `@frontend-components`
   - Custom rules can also become skills

3. **Standard vs Custom:**
   - **Standard:** Overwritten on every update (latest best practices)
   - **Custom:** Never touched by installer (project-specific rules)

**YAML Frontmatter for Path-Specific Rules:**

```markdown
---
paths: src/**/*.py
---
# Python-specific rules for this project

Only activate when working on Python files in src/
```

**Comparison to Our Framework:**

Our `CLAUDE.md` + `locked.md` + `scratch.md` system is monolithic - all rules in one place. Claude-codepro's modular approach allows:
- Automatic updates to best practices without touching custom rules
- Context-specific rule injection (only load what's needed)
- Team-wide standard rules with per-project customizations

Worth considering a `.claude/rules/` structure for our framework.

#### Dev Container Integration

**Purpose:**

Isolates Claude Code's filesystem access within a Docker container, preventing AI agent from accessing host system files when using `--dangerously-skip-permissions`.

**Setup:**

- Automated provisioning via `scripts/lib/devcontainer.py`
- Detection function determines whether to offer dev container setup
- Supports VS Code, Cursor, Windsurf with Dev Containers extension

**Benefits:**

1. **Security:** AI cannot access files outside project directory
2. **Consistency:** Same environment across different machines
3. **Pre-configuration:** Dev tools and extensions already installed
4. **Headless Browser:** agent-browser for web automation (only works in container)

**Optional Feature:**

Users can choose local installation or dev container during setup. Not mandatory for claude-codepro usage.

**Comparison to Our Framework:**

We don't address security/sandboxing. For teams concerned about AI filesystem access, this is valuable. For individual developers on personal machines, less critical.

### Limitations & Gotchas

**License and Cost:**

- AGPL-3.0 for personal, student, educator, nonprofit, open source use
- Commercial license required for business use (pricing not publicly listed)
- Additional costs: Claude subscription (Max 5x/20x recommended), OpenAI API (for Cipher embeddings), Zilliz Cloud (for Cipher vector DB), Ref API key

**Complexity Overhead:**

- Requires managing multiple external services (Cipher, Ref, Zilliz, OpenAI)
- Environment variables: `OPENAI_API_KEY`, `MILVUS_TOKEN`, `MILVUS_ADDRESS`, `REF_API_KEY`
- Installation touches shell config (`.zshrc`, `.bashrc`, `.config/fish/config.fish`)
- Learning curve for spec-driven workflow and slash commands

**Context Monitoring Limitations:**

- Claude Code doesn't natively expose 90% threshold - must be monitored through rules
- `/remember` requires manual execution (not automatic at threshold)
- No built-in warnings at context thresholds (community identified this as a major issue)

**TDD Enforcement Trade-offs:**

- Strict TDD may slow initial development for exploratory work
- Requires discipline to write meaningful tests (not just tests that pass)
- Auto-deletion of code could be frustrating if working in non-TDD mode accidentally

**External Dependencies:**

- Cipher requires internet connection and external vector DB
- Semantic search requires pre-indexing (not automatic)
- Quality tools (qlty, ruff, mypy) must be installed and configured
- MCP servers add complexity to setup and maintenance

**Criticism from Community:**

While researching, found broader Claude Code criticisms (not specific to claude-codepro):
- Usage limits hit quickly for Pro subscribers
- Inconsistent code quality across sessions
- Context management issues (suggesting same wrong fix repeatedly)
- Cost concerns for regular use

**Note:** These criticisms apply to Claude Code generally, not claude-codepro specifically. Claude-codepro attempts to address some of these (context management, quality enforcement).

### Recommendations

**High-Priority Adoptions:**

1. **MCP Funnel Gateway Pattern**
   - **Why:** We're already using multiple MCP servers (Obsidian, plugin_context7, deepwiki). Adding more will cause context bloat.
   - **Action:** Implement MCP Funnel to reduce token overhead by 85-90%
   - **Effort:** Low (install existing MCP Funnel server, configure `.mcp-funnel.json`)

2. **Modular Rules System**
   - **Why:** Our monolithic `CLAUDE.md` mixes framework instructions, anti-patterns, git protocol, MCP notes, locked decisions, etc. Hard to update selectively.
   - **Action:** Reorganize into `.claude/rules/standard/` (framework-maintained) and `.claude/rules/custom/` (user-customizable)
   - **Structure:**
     ```
     .claude/rules/
     ├── standard/
     │   ├── framework-core.md      # Mode 1/Mode 2, delegation protocol
     │   ├── git-protocol.md         # Commit discipline, PR creation
     │   ├── obsidian-integration.md # Vault write discipline
     │   └── research-pipeline.md    # TARGET/OUTPUT workflow
     └── custom/
         └── project-specific.md     # User's own rules
     ```
   - **Benefit:** Framework updates don't overwrite user customizations
   - **Effort:** Medium (refactor existing CLAUDE.md)

3. **Approval Gate Between Planning and Execution**
   - **Why:** Currently, Mode 1 (brainstorming) flows directly into Mode 2 (execution) without formal checkpoint. For complex features, human should review plan before Claude starts building.
   - **Action:** Introduce `/plan` command that writes to `kh/plan.md` and waits for explicit approval before execution
   - **Workflow:**
     ```
     User: "Let's plan the authentication feature"
     Claude: [Mode 1 brainstorming, writes plan to kh/plan.md]
     User: [Reviews plan.md, edits if needed]
     User: "Approved, let's implement"
     Claude: [Mode 2 execution based on approved plan]
     ```
   - **Benefit:** Reduces mid-implementation course corrections
   - **Effort:** Medium (new command, workflow discipline)

4. **Post-Edit Hooks for Vault Write Validation**
   - **Why:** We have "Vault Write Discipline" but no enforcement - relies on Claude remembering not to write to vault directly.
   - **Action:** Implement post-edit hook that detects vault writes outside of `/wrap`
   - **Hook Logic:**
     ```python
     def post_edit_hook(file_path):
         if file_path.startswith("/home/berkaygkv/Dev/Docs/.obs-vault/notes/"):
             if not in_wrap_context():  # Check if /wrap is running
                 return ERROR("Vault writes only allowed during /wrap. Use scratch.md instead.")
         return SUCCESS
     ```
   - **Benefit:** Prevents accidental vault pollution
   - **Effort:** Low (simple hook implementation)

**Medium-Priority Considerations:**

5. **Semantic Code Search (Context7 vs Vexor)**
   - **Current State:** We use Context7 MCP for library documentation
   - **Consideration:** Evaluate if local Vexor provides better semantic code search for our codebase
   - **Trade-off:** Context7 is external (documentation), Vexor is local (codebase). Complementary, not competitive.
   - **Action:** Keep Context7, consider adding Vexor for large codebases
   - **Effort:** Low (install if needed)

6. **Session Context Monitoring**
   - **Why:** We currently have no visibility into context usage within sessions
   - **Action:** Add context monitoring to surface warnings at thresholds
   - **Challenge:** Claude Code doesn't expose native context percentage - must estimate
   - **Alternative:** Use third-party "Claude Code Usage Monitor" tool
   - **Effort:** Medium (depends on implementation approach)

7. **Quality Hooks for Generated Code**
   - **Why:** We generate code but have no automated quality checks
   - **Action:** Add post-edit hooks for Python (ruff, mypy) and TypeScript (eslint, tsc)
   - **Trade-off:** Adds complexity, requires installing tools
   - **Benefit:** Catches quality issues immediately
   - **Effort:** Medium (install tools, configure hooks)

**Low-Priority / Not Recommended:**

8. **Cipher Vector DB for Memory**
   - **Why Not:** We already have structured memory via Obsidian vault. Cipher is better for unstructured semantic retrieval.
   - **Our Use Case:** Decisions, agreements, locked schemas need structure, not semantic search
   - **Keep:** Obsidian for explicit memory
   - **Skip:** Cipher for now

9. **Strict TDD Enforcement**
   - **Why Not:** Our framework is for *general collaboration*, not just code development. TDD makes sense for production codebases, less so for research/planning/documentation.
   - **Alternative:** Document TDD best practices in rules, but don't enforce
   - **Skip:** TDD enforcer hooks

10. **Dev Container Integration**
    - **Why Not:** Adds significant complexity for security benefit that's less critical for individual developers on personal machines
    - **When Useful:** Team environments, untrusted codebases, paranoid security posture
    - **Our Context:** Single developer, trusted codebase
    - **Skip:** Dev containers for now

### Open Questions

1. **How does config.yaml actually map commands to rules?**
   - The Rules Builder reads `config.yaml` but the schema isn't publicly documented
   - Would need to examine the actual repository code to understand the mapping format

2. **What is the actual token overhead of standard MCP setup vs MCP Funnel?**
   - Claims 85-90% reduction, but specific numbers vary by MCP server configuration
   - Would need to benchmark our current setup (Obsidian + Context7 + deepwiki) to quantify benefit

3. **How does the Auditor Agent actually work?**
   - Mentioned as "monitors rule compliance in real-time" but implementation details unclear
   - Is this a separate agent spawn? A background process? Integrated into Claude's reasoning?

4. **What's in the actual hook implementations?**
   - `file_checker_qlty.py`, `file_checker_python.py`, `tdd_enforcer.py` implementation details not available
   - Would need to access repository code or purchase license to examine

5. **How does migration.py detect and migrate previous versions?**
   - Installation script includes migration logic but approach unclear
   - Relevant for our framework if we want to support version upgrades

6. **Can the modular rules system load rules conditionally based on context?**
   - YAML frontmatter supports `paths:` for file-specific rules
   - Can it also support conditional loading based on command, mode, or other context?

### Sources

1. [GitHub - maxritter/claude-codepro](https://github.com/maxritter/claude-codepro)
2. [maxritter/claude-codepro | DeepWiki](https://deepwiki.com/maxritter/claude-codepro)
3. [Getting Started | maxritter/claude-codepro | DeepWiki](https://deepwiki.com/maxritter/claude-codepro/2-getting-started)
4. [Dev Container Integration | maxritter/claude-codepro | DeepWiki](https://deepwiki.com/maxritter/claude-codepro/9.4-dev-container-integration)
5. [Claude Code Just Cut MCP Context Bloat by 46.9%](https://medium.com/@joe.njenga/claude-code-just-cut-mcp-context-bloat-by-46-9-51k-tokens-down-to-8-5k-with-new-tool-search-ddf9e905f734)
6. [Agent Gateway | MCP Cow](https://mcpcow.com/en/service/agent-gateway/)
7. [Hands-on] Build a Memory Layer for Claude Code](https://aiengineering.beehiiv.com/p/hands-on-make-coding-agents-10x-smarter-1)
8. [GitHub - campfirein/cipher](https://github.com/campfirein/cipher)
9. [Unlocking the Power of Persistent Memory - Cipher Deep Dive](https://rimusz.net/unlocking-the-power-of-persistent-memory-in-coding-a-deep-dive-into-cipher-for-smarter-ide-workflows/)
10. [GitHub - nizos/tdd-guard](https://github.com/nizos/tdd-guard)
11. [TDD Guard for Claude Code](https://nizar.se/tdd-guard-for-claude-code/)
12. [Claude Code vs Cursor: Complete comparison guide in 2026](https://northflank.com/blog/claude-code-vs-cursor-comparison)
13. [Cursor vs Claude Code: The Ultimate Comparison Guide](https://www.builder.io/blog/cursor-vs-claude-code)
14. [Get started with Claude Code hooks](https://code.claude.com/docs/en/hooks-guide)
15. [Agent Skills - Claude Code Docs](https://code.claude.com/docs/en/skills)
16. [Inside Claude Code Skills: Structure, prompts, invocation](https://mikhail.io/2025/10/claude-code-skills/)
17. [GitHub - Pimzino/claude-code-spec-workflow](https://github.com/Pimzino/claude-code-spec-workflow)
18. [Spec-Driven Development with Claude Code: An AI Dev Guide](https://www.arsturn.com/blog/spec-driven-development-with-claude-code)
19. [Spec Driven Development with Claude Code](https://medium.com/@universe3523/spec-driven-development-with-claude-code-206bf56955d0)
20. [GitHub - scarletkc/vexor](https://github.com/scarletkc/vexor)
21. [vexor · PyPI](https://pypi.org/project/vexor/)
22. [Local RAG Guide: Semantic Search for Code with Claude Code](https://www.arsturn.com/blog/local-rag-claude-code-semantic-search-guide)
23. [Why Developers Are Suddenly Turning Against Claude Code?](https://ucstrategies.com/news/why-developers-are-suddenly-turning-against-claude-code/)
24. [Claude devs complain about surprise usage limits](https://www.theregister.com/2026/01/05/claude_devs_usage_limits/)
25. [My Experience With Claude Code After 2 Weeks](https://sankalp.bearblog.dev/my-claude-code-experience-after-2-weeks-of-usage/)

---

## Key Sources

- [Get started with Claude Code hooks](https://code.claude.com/docs/en/hooks-guide)
- [Agent Skills - Claude Code Docs](https://code.claude.com/docs/en/skills)

**Full sources:** [[research/outputs/OUTPUT-20260120-204411-deep-dive-into-the-maxritterclaude/sources]]
