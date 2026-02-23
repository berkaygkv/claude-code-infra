---
type: plan
title: "Build gemwrap video research skill"
status: draft
date: 2026-02-23
session: "[[sessions/session-45]]"
phases_total: 1
phases_done: 0
---

# Build gemwrap video research skill

## Goal

Build a `/research-video` skill that acts as an intelligent prompt engineering layer on top of gemwrap's YouTube analysis. The skill understands user intent, composes purpose-specific Gemini prompts from a playbook of principles and techniques, executes via gemwrap, applies quality review, and outputs structured research artifacts to the vault. Single-session build.

## Scope

**Includes:**
- SKILL.md — skill spec with workflow, quality gates, output format
- references/playbook.md — prompt engineering playbook (principles, techniques, failure modes, multimodal patterns, archetype examples)
- references/gemwrap-reference.md — gemwrap CLI flags and usage (so the skill is self-contained)
- CLAUDE.md update — add gemwrap to research pipeline section
- Test run with a real YouTube video

**Excludes:**
- Python scripts (no computational logic needed)
- General `/gemini` skill (separate scope)
- Two-pass analysis (defer to future iteration)
- Deep-research agent integration (let manual usage patterns emerge first)
- MCP server wrapping (overkill for current needs)

## Phase 1: Build the skill

### What gets done

**1. SKILL.md** — the skill specification

Frontmatter: name, description, allowed-tools (Bash for gemwrap invocation), context, agent type.

Body defines the workflow:
1. **Intent capture** — Understand what the user needs from this video. What question are they trying to answer? What would a useful output look like for their current work?
2. **Prompt composition** — Read the playbook. Identify which principles, techniques, and failure mitigations apply to this specific request. Compose a system instruction + user prompt from those atoms. Select gemwrap flags (model, temperature, max-tokens) based on task demands.
3. **Execution** — Shell out to gemwrap with the crafted prompt. Capture output.
4. **Quality review** — Check output for: timestamp grounding (are claims evidence-backed?), confidence signals (does it distinguish stated vs. inferred?), coherence (does it answer the user's actual question?), hallucination signals (vague timestamps, overly confident claims about details). Flag issues to user if found.
5. **Output formatting** — Format into vault/research/ artifact with frontmatter (type: research, date, topic, source: youtube, url) and structured sections adapted to the analysis purpose.

**2. references/playbook.md** — prompt engineering playbook

Not templates. A collection of composable principles organized by:

- **Always-apply constraints** — timestamp-ground every claim, instruct "say not found rather than guess", use system instruction for role + output contract, low temperature for extraction
- **Situational techniques** — ask for rejected alternatives (when video involves choices), request meta-commentary on what's NOT shown (when evaluating demos), extract exact commands shown on screen (when video shows code/terminal), ask about slide-speech divergence (when content is slide-heavy)
- **Multimodal leverage** — patterns that exploit video+audio (visual content speaker skips over, diagrams shown briefly, speaker hesitation as uncertainty signal, live demo vs. slides transition detection)
- **Failure mode mitigations** — Gemini confabulates under uncertainty (force null over guess), OCR unreliable at default resolution (note limitation to user), 1 FPS misses sub-second content (flag fast transitions), temporal reasoning degrades for complex comparisons (decompose into sequential descriptions)
- **Archetype examples** — 4-5 worked examples showing how principles combine for different goals (decision extraction, tool evaluation, tutorial distillation, conference survey, freeform). These illustrate composition, not prescribe selection.
- **Flag selection guidance** — when to use gemini-2.5-pro vs flash, temperature ranges by task type, max-token sizing

**3. references/gemwrap-reference.md** — CLI reference

Condensed from GEMWRAP.md: invocation patterns, flags relevant to this skill (--youtube, --system, -m, -t, --max-tokens, --stream, -a), account rotation, quota notes. Makes the skill self-contained.

**4. CLAUDE.md update**

Add to research pipeline section:
- gemwrap as available tool for YouTube video analysis
- `/research-video` skill for structured video research
- Note: ~2,000 req/day quota across accounts

**5. Test run**

Pick a real YouTube technical talk. Run the full workflow: intent → prompt composition → execution → quality review → artifact output. Verify the skill produces a useful research artifact.

### Task checklist
- [ ] Write SKILL.md (skill spec + workflow)
- [ ] Write references/playbook.md (prompt engineering playbook)
- [ ] Write references/gemwrap-reference.md (CLI reference)
- [ ] Update CLAUDE.md research pipeline section
- [ ] Test with a real YouTube video
- [ ] Iterate based on test results

### Deliverables
- `.claude/skills/research-video/SKILL.md`
- `.claude/skills/research-video/references/playbook.md`
- `.claude/skills/research-video/references/gemwrap-reference.md`
- Updated `CLAUDE.md` (research pipeline section)
- One test artifact in `vault/research/`

## Decisions

- [[decisions/scratch-pad-v2]] — scratch.md as reasoning surface (active)
- [[decisions/research-format-v2]] — flat files, frontmatter, inline sources (output format)
- [[decisions/io-strategy-v2]] — native for known paths, MCP for discovery (vault writes)
