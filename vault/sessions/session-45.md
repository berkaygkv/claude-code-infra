---
type: session
session: 45
date: 2026-02-23
mode: brainstorm
topics: [gemwrap-integration, video-research-skill, prompt-engineering, playbook-design]
outcome: successful
continues_from: "[[sessions/session-44]]"
decisions: []
---

# Session 45: Design gemwrap video research skill

## Context

Brainstormed how to integrate gemwrap (user's Gemini CLI tool with YouTube video analysis) into the kh system. Ran deep research on Gemini multimodal video prompt engineering — found that timestamp grounding, confidence fields, purpose-specific system instructions, and low temperature are the key levers. Initially proposed static template selection (5 purpose types), user pushed back — converged on a playbook-of-principles approach where Claude composes prompts dynamically from atoms rather than selecting from a menu. Plan drafted at vault/plans/gemwrap-video-research.md (status: draft, pending approval).

## Decisions

### Locked

None — design choices are captured in the plan, pending approval.

### Open

- Plan approval for gemwrap-video-research.md — designed but not formally approved before wrap
- Whether gemwrap integration warrants a standalone decision file or if the plan is sufficient

## Memory

- gemwrap lives at /Users/berkayg/Codes/gemwrap, installed via `pip install -e`, CLI command is `gemwrap`
- gemwrap uses OAuth from gemini-cli, ~2,000 free req/day across 2 accounts (round-robin rotation)
- Key flags for skill: `--youtube URL`, `--system "..."`, `-m model`, `-t temperature`, `--max-tokens N`
- Gemini video: 1 FPS frame sampling, real audio+visual (not transcript), can read text on screen with high resolution
- Gemini hallucination profile: confabulates under uncertainty rather than abstaining — timestamp grounding is the primary mitigation
- OCR in video has a known regression — sometimes produces nonsense while static frame OCR works fine. Workaround: note limitation to user
- response_schema (API-level structured output) unavailable via CLI — must achieve structure through prompt engineering
- Deep research auto-captured to vault/research/ (Gemini video prompt engineering)
- Key design principle: playbook of composable atoms > static template selection. Claude composes the right prompt from principles, not picks from a menu.

## Next Steps

1. Approve gemwrap video research plan (user didn't formally approve before wrap — confirm at next session start)
2. `/begin build` to execute the plan — single phase, single session
3. Test the skill with a real YouTube video
4. Carried over: template syncs (S42 + S44), test /upgrade skill, test excalidraw, Catalyst purchase, output style design
