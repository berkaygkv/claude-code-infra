# Prompt Engineering Playbook — Gemini Video Analysis

This is a collection of composable principles, not templates. Read the atoms, identify which ones apply to the current request, compose a prompt from them.

---

## Always-Apply Constraints

These go into every video analysis prompt. No exceptions.

### Timestamp Grounding
Every factual claim must cite a MM:SS timestamp. This is the primary hallucination defense — fabricated claims produce non-existent timestamps that are easy to spot.

```
System instruction atom:
"Every factual claim must include a timestamp citation in MM:SS format.
If you cannot locate evidence for a claim in the video, say so explicitly
rather than guessing."
```

### Forced Abstention
Gemini confabulates under uncertainty rather than abstaining. You must explicitly instruct it to say "not found" instead of guessing.

```
System instruction atom:
"If you cannot find evidence for something in the video, state that it
was not found rather than inferring or guessing. It is better to have
gaps than fabricated information."
```

### System Instruction for Role + Output Contract
The system instruction defines who Gemini is for this task and what the output structure must look like. This is more effective than putting formatting instructions in the user prompt.

```
Pattern:
"You are a [ROLE] analyzing this video to [PURPOSE]. Your output must
include [REQUIRED_SECTIONS]. [CONSTRAINTS]."
```

### Low Temperature for Extraction
Use `temperature=0.1` (or 0.0) for structured extraction. Hallucination risk increases with temperature. Only use 0.5+ for narrative synthesis where variation is acceptable.

---

## Situational Techniques

Select based on video type and user goal.

### Ask for Rejected Alternatives
**When:** Video involves choices, decisions, architecture discussions.
**Why:** Speakers often mention what they chose NOT to do — this is as valuable as what they chose.

```
Prompt atom:
"For each decision identified, also extract any alternatives the speaker
mentioned considering or rejecting, and their stated reasons for rejection."
```

### Request Meta-Commentary on What's NOT Shown
**When:** Evaluating demos, product videos, tool walkthroughs.
**Why:** Gets Gemini to assess completeness — "happy path only?" vs. production-readiness.

```
Prompt atom:
"Assess what the demo does NOT show: error handling, edge cases,
production deployment, scale characteristics. Note whether the
demonstration appears to be a happy-path walkthrough or a realistic
usage scenario."
```

### Extract Exact Commands/Code Shown on Screen
**When:** Tutorials, terminal demos, coding walkthroughs.
**Why:** Gemini paraphrases code by default unless told to transcribe verbatim.
**Note:** OCR in video has a known regression. Warn user if precision is critical.

```
Prompt atom:
"Transcribe commands and code shown on screen exactly as displayed,
including flags, arguments, and file paths. Note the MM:SS where each
appears. If text is unclear or partially visible, indicate this rather
than guessing the content."
```

### Detect Slide-Speech Divergence
**When:** Presentation-heavy content with slides.
**Why:** Speakers often say things that contradict or extend what's on their slides.

```
Prompt atom:
"Note cases where the slide content and the speaker's verbal explanation
diverge — where the speaker adds context not on the slide, or where
the slide shows something the speaker doesn't address."
```

### Decompose Temporal Comparisons
**When:** Videos that show evolution (before/after, version 1 vs. version 2, iterative approaches).
**Why:** Gemini's temporal reasoning degrades for complex comparisons across distant timestamps.

```
Prompt atom:
"Describe the approach shown at [TIME_A] in detail. Then describe the
approach shown at [TIME_B] in detail. Then explain what changed between
them and why."
```

### Identify Speaker Uncertainty Signals
**When:** Technical talks where confidence level matters.
**Why:** Hedging, pauses, and backtracking mark contested or evolving claims.

```
Prompt atom:
"Note moments where the speaker hedges, backtracks, or expresses
uncertainty. These often mark contested claims or areas where best
practices are still evolving."
```

### Extract Visual Content Speaker Skips
**When:** Dense presentations where slides contain more than the speaker covers.
**Why:** Exploits multimodal capability — correlates what's shown vs. what's said.

```
Prompt atom:
"Identify diagrams, charts, URLs, resource names, or code samples shown
on screen that the speaker does NOT verbally explain or only briefly
references. List them with timestamps."
```

---

## Multimodal Leverage Patterns

These exploit the fact that Gemini processes both video and audio simultaneously.

### Speaker Behavior Detection
Gemini can see when a speaker shifts from slides to live demo, and detect visual transitions.

```
"Note when the speaker transitions between slides and live demonstration.
For live demo segments, describe what is being shown on screen."
```

### Audience Interaction
If Q&A is included, Gemini can identify question-answer exchanges.

```
"If the video includes Q&A or audience interaction, identify the
questions asked and the speaker's responses."
```

### Deictic Reference Resolution
When speakers say "this" or "here" while pointing at something on screen.

```
"When the speaker uses references like 'this', 'here', or 'as you can see',
identify what they are pointing to or referring to on screen."
```

---

## Failure Mode Mitigations

### Confabulation Under Uncertainty
**Problem:** Gemini invents rather than abstaining.
**Mitigation:** Always-apply constraints (timestamp grounding + forced abstention) handle this. Additionally, add a confidence field when using structured output:

```
Prompt atom:
"For each finding, indicate confidence level:
- STATED: speaker explicitly said this
- SHOWN: visible on screen but not verbally stated
- INFERRED: deduced from context, not directly stated or shown
- UNCLEAR: ambiguous, could not be determined with confidence"
```

### OCR Regression in Video
**Problem:** In-video text extraction sometimes produces nonsense while static frame OCR works fine. Documented across Gemini 2.5 and 3 variants.
**Mitigation:** Warn the user when they need precise text from screen. If the output contains garbled text, note it. Don't re-run expecting different results — the issue is in the model, not the prompt.

### 1 FPS Temporal Blind Spots
**Problem:** Content visible for less than 1 second may not be sampled.
**Mitigation:** If the user mentions fast-paced screen content, flag this upfront:

```
"Note: Gemini samples video at 1 frame per second. Content shown for
less than 1 second (rapid scrolling, brief screen flashes) may be missed."
```

### Temporal Reasoning Degradation
**Problem:** Complex comparisons across distant timestamps are unreliable.
**Mitigation:** Use the "decompose temporal comparisons" technique above — describe each segment independently, then compare.

---

## Archetype Examples

These show how principles combine. They illustrate composition, not prescribe selection.

### Decision Extraction (architecture talk)

**Always-apply:** timestamp grounding, forced abstention, low temperature
**Situational:** rejected alternatives, speaker uncertainty signals
**Flag selection:** `gemini-2.5-pro`, `-t 0.1`, `--max-tokens 8192`

```
System: "You are a senior engineer extracting architecture decisions from
this technical talk. Every decision must include a MM:SS timestamp, the
decision itself, stated rationale, any alternatives mentioned as rejected,
and whether the decision was explicitly stated or inferred from context.
If you cannot find evidence for a decision, omit it rather than guessing."

Prompt: "Extract all technical decisions made in this talk. For each, provide:
timestamp, the decision in one sentence, rationale, rejected alternatives,
and confidence (stated/inferred). Also note any topics where the speaker
expressed uncertainty or hedged their recommendation."
```

### Tutorial Distillation (coding walkthrough)

**Always-apply:** timestamp grounding, forced abstention, low temperature
**Situational:** exact commands on screen, visual content speaker skips
**Flag selection:** `gemini-2.5-pro`, `-t 0.1`, `--max-tokens 8192`

```
System: "You are a documentation writer creating a self-contained tutorial
from this video walkthrough. Your output should be usable by someone who
has NOT watched the video. Transcribe commands exactly as shown on screen.
If text is unclear, indicate this rather than guessing."

Prompt: "Extract a step-by-step tutorial from this video. Include:
prerequisites assumed, exact commands shown (with MM:SS), common mistakes
warned about, and the end state. Also list any URLs, tools, or resources
shown on screen that the speaker doesn't verbally mention."
```

### Tool Evaluation (product demo)

**Always-apply:** timestamp grounding, forced abstention, moderate temperature
**Situational:** meta-commentary on what's NOT shown, rejected alternatives
**Flag selection:** `gemini-2.5-pro`, `-t 0.3`, `--max-tokens 8192`

```
System: "You are a technical evaluator assessing the tool demonstrated in
this video. Your job is to extract information that helps a team decide
whether to adopt what is shown. Distinguish between demonstrated capabilities
and marketing claims."

Prompt: "Evaluate the tool shown in this video. For each capability demonstrated:
what it does, how it's invoked, any limitations mentioned. Assess: is this a
happy-path demo or production-realistic? What is NOT shown (error handling,
scale, deployment)? What alternatives are mentioned? Include MM:SS for all claims."
```

### Conference Summary (keynote / survey talk)

**Always-apply:** timestamp grounding, forced abstention, moderate temperature
**Situational:** detect slide-speech divergence, speaker uncertainty signals
**Flag selection:** `gemini-2.5-flash`, `-t 0.5`, `--max-tokens 8192`

```
System: "You are summarizing this conference talk for a research digest.
Your audience are senior engineers deciding whether to watch the full talk.
Be precise and complete. Cite timestamps for all claims."

Prompt: "Summarize this talk. Include: core thesis (2-3 sentences), key claims
with evidence and timestamps, quantitative claims (benchmarks, numbers), what
is new vs. already established, who should watch, strongest and weakest parts
of the argument. Note any moments where the speaker's slides and spoken
explanation diverge."
```

### Freeform Analysis (user-defined goal)

**Always-apply:** timestamp grounding, forced abstention
**Situational:** chosen based on user's specific question
**Flag selection:** based on complexity

When the user has a specific question that doesn't fit the archetypes above, compose from first principles:

1. What does the user actually need to know?
2. Which always-apply constraints are relevant?
3. Which situational techniques help answer their specific question?
4. Compose system instruction: role (matches the expertise needed) + output contract (matches what would be useful) + constraints (always-apply + relevant situational)
5. Compose user prompt: specific to their question, referencing timestamp requirements

---

## Flag Selection Guidance

### Model

| Scenario | Model | Why |
|----------|-------|-----|
| Multi-topic, long talks (>30 min), decision extraction, temporal reasoning | `gemini-2.5-pro` | Better at complex reasoning, longer context |
| Single-topic summaries, quick extraction, straightforward content | `gemini-2.5-flash` | Faster, cheaper, sufficient for simple tasks |
| When you need latest capabilities | `gemini-3-flash-preview` | Newest model — but higher confabulation risk |

### Temperature

| Task Type | Temperature | Why |
|-----------|-------------|-----|
| Structured extraction (decisions, commands, facts) | 0.1 | Minimize hallucination |
| Evaluation with judgment calls | 0.3 | Some flexibility for nuanced assessment |
| Narrative summary, conference digest | 0.5 | Natural prose, acceptable variation |

### Max Tokens

| Video Length | Max Tokens |
|-------------|------------|
| < 15 min | 4096 |
| 15–45 min | 8192 |
| 45+ min or exhaustive extraction | 16384 |
