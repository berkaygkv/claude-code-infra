---
name: research-video
description: Analyze YouTube videos using gemwrap (Gemini CLI). Composes purpose-specific prompts from a playbook of principles, executes via gemwrap, reviews output quality, and produces structured research artifacts.
allowed-tools: Bash(gemwrap *)
context: fork
agent: general-purpose
---

# Video Research Skill

Analyze YouTube videos via gemwrap + Gemini multimodal video understanding. You are a prompt engineering layer — you compose the right Gemini prompt for each request, not a pass-through.

Read `references/playbook.md` before every invocation. Read `references/gemwrap-reference.md` for CLI usage.

## Workflow

### 1. Intent Capture

Understand what the user needs from this video:

- What question are they trying to answer?
- What would a useful output look like for their current work?
- What type of analysis fits? (decision extraction, tutorial distillation, tool evaluation, conference summary, freeform)

If the user's intent is vague, ask. Don't guess the analysis type.

### 2. Prompt Composition

Read the playbook. For this specific request:

1. **Start with always-apply constraints** — timestamp grounding, forced abstention, low temperature for extraction
2. **Select situational techniques** — which playbook atoms apply to this video type and user goal?
3. **Compose a system instruction** — role + output contract + constraints, tailored to the analysis purpose
4. **Compose the user prompt** — specific extraction instructions referencing the video
5. **Select gemwrap flags:**
   - Model: `gemini-2.5-pro` for complex analysis, `gemini-2.5-flash` for straightforward extraction
   - Temperature: `0.1` for structured extraction, `0.5` for narrative summary
   - Max tokens: `8192` default, increase for long videos or exhaustive extraction

### 3. Execution

Run gemwrap with the composed prompt:

```bash
gemwrap --youtube "URL" \
  --system "SYSTEM_INSTRUCTION" \
  -m MODEL \
  -t TEMPERATURE \
  --max-tokens MAX_TOKENS \
  "USER_PROMPT"
```

Capture the full output.

**Timeout:** Always set Bash timeout to 300000 (5 minutes) for gemwrap calls. Video analysis with `gemini-2.5-pro` on long videos can take 60-120 seconds for the API to respond.

### 4. Quality Review

Check the output for:

- **Timestamp grounding** — Are claims backed by MM:SS citations? Flag any claim without a timestamp.
- **Confidence signals** — Does it distinguish stated vs. inferred? If the output presents everything with equal certainty, that's a red flag.
- **Coherence** — Does it answer the user's actual question, not a generic summary?
- **Hallucination signals** — Vague timestamps (e.g., "around the middle"), overly confident claims about details that would be hard to see at 1 FPS, exact quotes that feel too polished.

If issues found:
- Minor (a few ungrounded claims): note them inline when presenting output
- Major (systematic hallucination, wrong video analyzed, incoherent): re-run with adjusted prompt. Tell the user what you changed.

### 5. Output Formatting

Format into a vault research artifact:

**File path:** `{{cookiecutter.project_slug}}/research/{YYYYMMDD}-{slug}.md`

**Frontmatter:**
```yaml
---
type: research
date: YYYY-MM-DD
topic: "descriptive title"
source: youtube
url: "the youtube URL"
model: "model used"
---
```

**Body structure** — adapt sections to the analysis purpose. Not every analysis needs every section. Use what fits:

- **Summary** — 2-4 sentence overview answering the user's core question
- **Key Findings** — numbered list of substantive findings with MM:SS citations
- **Detailed Analysis** — deeper breakdown organized by topic/theme/timeline
- **Limitations** — what the video didn't cover, what the analysis couldn't determine
- **Sources** — the YouTube URL plus any supplementary references

### 6. Present to User

Show the formatted artifact. Let them react before writing to disk. If they want adjustments, iterate — don't start over unless the whole approach was wrong.

## Important Constraints

- **One video per request.** Gemwrap processes one YouTube URL at a time.
- **Public/unlisted videos only.** Private videos won't work.
- **OCR is unreliable in video.** If the user needs exact text from slides or code on screen, warn them about the known regression. Suggest they provide screenshots separately if precision matters.
- **~2,000 req/day quota** across accounts. Each gemwrap call is one request. Don't waste quota on speculative runs — compose the prompt well the first time.
- **No response_schema via CLI.** Structure must be achieved through prompt engineering alone. The playbook covers this.
