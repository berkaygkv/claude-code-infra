---
type: research
title: "No Vibes Allowed: Solving Hard Problems in Complex Codebases"
date: 2026-02-24
topic: context-engineering, RPI-workflow
source: "AI Engineer Code Summit 2025 (Dex Horthy, HumanLayer)"
---

# No Vibes Allowed: Solving Hard Problems in Complex Codebases

**Speaker:** Dex Horthy (Founder & CEO, HumanLayer)
**Event:** AI Engineer Code Summit 2025

---

## The Core Problem: The "Slop" Factory
Current AI integration in software engineering often leads to **rework and codebase churn**, particularly in "brownfield" (existing, complex) projects. While productivity increases for simple tasks, it plateaus or declines for complex systems.

> [!warning] The Naive Way
> Asking an agent for a change, correcting its mistakes, and repeating until the context window is full or the user gives up. This leads to "Resteering in context," which often confuses the model further.

---

## Context Engineering & The "Dumb Zone"
LLMs are stateless functions: **Tokens In → Tokens Out**. The only way to improve performance is to provide better tokens.

### The 40% Rule
Dex introduces the concept of the **"Dumb Zone"**:
* **Smart Zone:** Context usage below ~40%.
* **Dumb Zone:** Context usage above 40%. As the context window fills with noise (JSON tool responses, build logs, UUIDs), the model's ability to call tools and reason correctly diminishes.

> [!tip] Intentional Compaction
> Periodically summarize progress into a markdown file and start a fresh context window. This "cleverly avoids the dumb zone."

---

## The RPI Workflow: Research, Plan, Implement
To solve complex problems, Dex advocates for a structured, three-phase workflow designed to maintain **Mental Alignment**.

### 1. Research (Compression of Truth)
* **Goal:** Understand how the system works without jumping to fixes.
* **Output:** A `research.md` file (300-1000 lines) documenting relevant files and code flow.
* **Technique:** Use **Sub-agents** to fork new context windows for specific searches, returning only succinct summaries to the parent agent.

### 2. Planning (Compression of Intent)
* **Goal:** Outline exact implementation steps, including filenames and line numbers.
* **Output:** A `plan.md` file.
* **Benefit:** High leverage. A bad line in a plan can lead to 100 bad lines of code.

### 3. Implementation (Reliable Execution)
* **Goal:** Write the code following the plan.
* **Rule:** Keep context under 40% by only pulling in the specific files mentioned in the plan.

---

## Advanced Context Management

### Progressive Disclosure (Sharding)
Instead of dumping an entire monorepo's context into the agent, shard the documentation down the stack:
1. **Org/Repo Level:** High-level architecture.
2. **Module Level:** Specific logic and dependencies.
3. **File Level:** The source of truth.

> [!info] The Hierarchy of Lies
> Documentation lies more than comments; comments lie more than function names; function names lie more than the actual code. **Always prioritize the code as the source of truth.**

---

## The Human Element: Don't Outsource the Thinking
AI cannot replace thinking; it only **amplifies** it.

* **Code Review Evolution:** Reviewing 300 lines of an implementation plan is more effective for mental alignment than reviewing 1,000 lines of AI-generated Go code.
* **The Growing Rift:** Senior engineers often resist AI because they lack the "reps" to see its value, while junior engineers use it heavily but produce "slop."
* **Solution:** Technical leaders must pick **one tool**, get the reps in, and drive cultural change from the top.

---

## Key Takeaways
* **Context is everything:** Manage it like a precious resource.
* **Avoid the Dumb Zone:** Use compaction and sub-agents to stay under 40% context.
* **RPI over "Vibes":** Research and Plan before you Implement.
* **Leverage the Plan:** Use implementation plans as the primary tool for team alignment and code review.

## Sources
* [HumanLayer Jobs](https://hlur.dev/jobs)
* [Dex Horthy on X](https://x.com/dexhorthy)
