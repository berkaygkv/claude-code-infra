---
type: research
date: 2026-02-23
topic: "the following topic thoroughly:

**Gemini multimodal video understanding — prom"
---

# the following topic thoroughly:

**Gemini multimodal video understanding — prom

**Question:** Research the following topic thoroughly:

**Gemini multimodal video understanding — prompt engineering best practices**

I need to understand:

1. **What Gemini can actually see/hear in videos** — Doe...

---

## Findings

Now I have a complete picture. Here is the full research synthesis.

---

Gemini's video understanding is genuinely multimodal — it processes both visual frames (sampled at 1 FPS by default, configurable) and audio (1Kbps mono) simultaneously, not sequentially. The 2.5 Pro and Gemini 3 generations represent a meaningful jump in temporal reasoning and audio-visual integration. For a prompt engineering layer on top of a Gemini CLI tool, the most important design decisions are: (1) use `response_schema` for structured extraction rather than prose instructions alone, (2) always ask for timestamp evidence alongside claims to ground outputs and expose hallucinations, (3) tailor the system instruction to the purpose type before the video is mentioned, and (4) use `MEDIA_RESOLUTION_HIGH` for any task requiring OCR of slide text or code — low resolution reliably degrades text reading accuracy.

## Research Summary

### Question/Topic

How does Gemini's multimodal video understanding actually work at a technical level, and what prompt engineering patterns produce reliable, purpose-oriented output — specifically for a CLI tool that will analyze technical talks, tutorials, library demos, and conference keynotes?

---

### Key Findings

1. Gemini processes video as simultaneous audio + visual streams. It is not transcript-only. It can reason about what appears on screen and what is said in the same inference pass.
2. Default frame sampling is 1 FPS with configurable override. Token cost is approximately 300 tokens/second at default resolution, ~100 tokens/second at low resolution.
3. OCR of text on screen (slides, code, terminal output) works — but degrades with low `media_resolution`, small fonts, fast transitions, and motion blur. There is a documented regression in late 2024/early 2025 where in-video OCR gave nonsense on certain video types while static screenshots from the same video worked correctly.
4. `response_schema` (native API) is the correct mechanism for structured output, not prompt-only instructions. Prompts that say "return JSON" are unreliable; schemas enforced via the API parameter are reliable.
5. Timestamp grounding — asking Gemini to cite `MM:SS` timestamps as evidence for every claim — is the primary technique for reducing hallucination in video analysis. It forces the model to locate claims in the timeline.
6. Gemini 3's hallucination profile is aggressive: when it doesn't know, it invents rather than abstaining. The 91% rate on AA-Omniscience benchmark is specifically about confabulation under uncertainty, not about general accuracy.
7. Gemini 3 models have a documented bug: videos without an audio stream fail with a 404 error unless `MEDIA_RESOLUTION_HIGH` or `MEDIA_RESOLUTION_UNSPECIFIED` is explicitly set.
8. For Gemini 3 models, `thinking_level` (not `thinking_budget`) controls reasoning depth. Setting it to `high` for video analysis of complex technical content is recommended.

---

### Detailed Analysis

#### What Gemini Can See and Hear in Video

**Frame processing:** The File API samples at 1 FPS by default. This is fixed at upload time — the model does not "decide" which frames matter at inference. At 1 FPS, a 60-minute video generates 3,600 frames. Fast-motion content (code scrolling, rapid slide transitions under 1 second, quick terminal output) will have frames dropped between samples.

**Token budget per second of video:**
- Default resolution: ~258 tokens/frame + 32 tokens/second audio = ~290 tokens/second
- Low resolution: ~66 tokens/frame + 32 tokens/second audio = ~98 tokens/second
- Audio-only contribution: 32 tokens/second regardless of resolution

**Duration limits:**
- 1M token context (Gemini 2.5 Flash): up to 1 hour at default resolution, 3 hours at low resolution
- 2M token context (Gemini 2.5 Pro): up to 2 hours at default, 6 hours at low
- YouTube via URL: max 8 hours/day (free), no limit (paid), 1 video per request, public only

**Audio capability:** The model hears the actual audio track, not just a transcript. It can identify speech, background sounds, music, and non-speech audio events. Speaker diarization is supported — the model can label and differentiate multiple speakers. Audio-only transcription in a first pass, then visual analysis separately, is documented as a two-pass strategy for maximum transcription accuracy.

**OCR / text on screen:** Gemini can read slide text, code on screen, terminal output, and diagram labels. Quality depends on:
- `MEDIA_RESOLUTION_HIGH` is required for reliable OCR — low and medium resolution lose fine text
- Text must be visible for at least 1 second (the frame sampling window) to be captured
- Dense code or small fonts in fast-moving screen recordings are problematic
- There is a known regression (reported by multiple users across all Gemini variants including 2.5 Pro, Flash, Flash-lite) where in-video OCR produces nonsense while static image OCR from the same frames works correctly. No official resolution documented as of early 2026.

**Timestamps:** The model uses MM:SS format internally. You can reference timestamps in prompts ("describe what happens around 04:30") and request timestamp citations in outputs ("list the three key claims made in the talk, each with its MM:SS location").

---

#### Prompt Engineering Patterns That Work

**The media-first rule:** For single-media prompts, the video should come before the instruction text in the `contents` array. For large context (long video + long instructions), place data first, instructions last, with a framing phrase like "Based on the video above...". This mirrors how Gemini was trained.

**System instruction = persona + output contract:** The system instruction should define who Gemini is for this task and what the output structure must look like. This is more effective than putting formatting instructions in the user turn.

```
System: You are a technical research analyst extracting actionable 
intelligence from engineering talks. You output structured JSON only. 
Every factual claim must be accompanied by a timestamp citation in MM:SS 
format. If you cannot locate evidence for a claim in the video, mark it 
as inferred rather than stated.
```

**Conciseness calibration:** Gemini 3 is less verbose by default than 2.5 Pro. For extraction tasks, this is fine. For detailed analysis, explicitly say "provide exhaustive detail" or "do not summarize". The phrase "Be concise" measurably reduces output length for technical tasks; avoid it when you need full coverage.

**Temperature for extraction:** Use `temperature=0.0` or low temperature (0.1) for structured extraction tasks. The model's hallucination risk increases with temperature. For summarization and narrative, 0.7-1.0 is acceptable.

**Thinking level for complex analysis:** For technical decision extraction or multi-topic conference talk analysis, set `thinking_level=high` (Gemini 3) or `thinking_budget` tokens (Gemini 2.5). This enables internal chain-of-thought before output. The improvement is measurable for tasks requiring temporal tracking ("what changed between the first and second approach shown") and comparative reasoning ("how does the library shown at 15:00 differ from the one mentioned at 42:00").

**Delimiter consistency:** Pick XML tags or Markdown headers — not both. XML tags provide more semantic precision for multi-section instructions:

```xml
<role>Technical analysis specialist</role>
<task>Extract architecture decisions from this engineering talk</task>
<output_format>JSON conforming to the provided schema</output_format>
<constraints>
- Cite MM:SS for every decision extracted
- If slide content contradicts spoken content, note the discrepancy
- Mark inferred content with "inferred: true"
</constraints>
```

---

#### Structured Output: The Correct Approach

**Use `response_schema`, not prompt-only JSON instructions.** Prompt instructions to "return JSON" are unreliable — the model may wrap in markdown code fences, add prose preambles, or omit fields. The `response_schema` API parameter enforces structure at the generation level.

```python
from google import genai
from google.genai import types
from pydantic import BaseModel
from typing import List, Optional

class Decision(BaseModel):
    timestamp: str          # MM:SS format
    decision: str           # What was decided
    rationale: str          # Why
    alternatives_discussed: List[str]
    confidence: str         # "stated" | "inferred"

class TalkAnalysis(BaseModel):
    talk_title: str
    speakers: List[str]
    main_thesis: str
    decisions: List[Decision]
    open_questions: List[str]
    key_libraries_mentioned: List[str]

response = client.models.generate_content(
    model="gemini-2.5-pro",
    contents=[video_part, "Analyze this technical talk."],
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=TalkAnalysis,
        temperature=0.1,
        system_instruction="You are a technical research analyst..."
    )
)
```

**Schema design principles:**
- Use `description` fields on schema properties — these function as inline prompt instructions for that field
- Use `enum` for categorical fields (confidence: "stated" | "inferred" | "unclear")
- Use `Optional` / `nullable` for fields the model may legitimately not find (some talks have no live demos)
- Add `minItems`/`maxItems` to array fields where appropriate
- Validate outputs in application code — schema compliance does not guarantee semantic correctness

---

#### Purpose-Specific Prompt Patterns

**Technical Decision Extraction (architecture talks, design discussions)**

The goal is capturing what was decided, the reasoning, and the trade-offs considered.

```
System: You are a senior engineer reviewing this architecture talk to extract 
decisions your team should know about. Focus on: specific technology choices, 
rejected alternatives, performance or cost constraints that drove decisions, 
and anything the speaker expresses uncertainty about.

For every decision extracted, provide:
- timestamp (MM:SS)
- the decision in one sentence
- stated rationale
- alternatives the speaker mentioned rejecting
- whether this is stated explicitly or inferred from context
```

Key technique: ask specifically for "rejected alternatives" — speakers often mention what they chose NOT to do, and this is as valuable as what they chose. Ask for "what the speaker seemed uncertain about" — hedging language in technical talks is a signal of contested or evolving decisions.

**Tutorial / Educational Content Extraction**

The goal is a standalone learning artifact someone can follow without watching.

```
System: You are a documentation writer creating a self-contained tutorial 
summary from a video walkthrough. Your output should be usable by someone 
who has NOT watched the video.

Extract:
1. Prerequisites assumed (tools, knowledge, accounts)
2. Step-by-step procedure with exact commands shown on screen
3. Common mistakes the presenter warns about
4. The end state (what you have when done)

For commands shown on screen: transcribe them exactly as shown, 
including flags and arguments. Note the MM:SS where each appears.
```

Key technique: explicitly request "exact commands shown on screen" — Gemini tends to paraphrase code unless instructed to transcribe verbatim. The `MEDIA_RESOLUTION_HIGH` parameter is required here.

**Library / Tool Evaluation (demo videos, comparison talks)**

The goal is a structured evaluation matrix.

```
System: You are a technical evaluator assessing libraries/tools demonstrated 
in this video. Your job is to extract information that would help a team 
decide whether to adopt what is being shown.

For each library or tool demonstrated:
- Name and version (if shown)
- What problem it solves
- Integration surface (API style, language, dependencies)
- Concrete performance characteristics mentioned or shown
- Limitations or caveats the presenter mentioned
- Comparison to alternatives if discussed
- Your assessment of the demo quality: did it show production-readiness 
  or a happy path only?
```

Key technique: the last item — asking for meta-commentary on the demo itself ("happy path only?") — gets Gemini to assess what the video is NOT showing, not just what it shows.

**Conference Talk / Keynote Summarization**

The goal is a structured summary for someone who needs to decide whether to watch.

```
System: You are summarizing this conference talk for a research digest.
Your audience are senior engineers who will decide whether to watch the 
full talk. Be precise and complete.

Extract:
- The core argument or thesis in 2-3 sentences
- Three to five key claims with evidence or demonstrations supporting each
- Any quantitative claims (benchmarks, numbers, comparisons)
- What is new vs. already known (what the speaker claims is novel)
- Who should watch: which practitioners would benefit most
- The strongest and weakest parts of the argument

Use timestamps for all claims so readers can jump directly to 
relevant sections.
```

Key technique: asking "what is new vs. already known" forces the model to distinguish novelty from background — useful for filtering out talks that restate established patterns.

---

#### Multimodal-Specific Techniques

**Leveraging audio-visual integration:** Unlike transcript-only tools, Gemini can correlate what is shown with what is said. Prompts that exploit this:

- "Describe cases where the slide content and the spoken explanation diverge"
- "What does the speaker show on screen that they do NOT verbally explain?"
- "When the speaker references 'this' or 'here', what are they pointing to?"
- "Are there diagrams, charts, or code samples shown that the speaker skips over quickly? List them with timestamps."

**Speaker behavior signals:**

- "Identify moments where the speaker pauses, hesitates, or backtracks — these often mark important corrections or contested claims"
- "Note when the speaker shifts to live demo vs. slides" (Gemini can see this because the visual modality changes)
- "Identify audience questions if Q&A is included"

**Slide content extraction:** When slides are central to the content:

- "For each slide shown, describe its title and key content"
- "List every URL, resource, or tool name that appears on any slide"
- "Transcribe the exact text of any architecture diagram labels shown"

Note: Use `MEDIA_RESOLUTION_HIGH` for all slide-heavy content. If slides are shown for less than 1-2 seconds before transitioning, the 1 FPS sampling may miss them. Pre-processing the video to ensure 2+ seconds per slide is a practical workaround.

**Two-pass strategy for dense technical content:** For talks with both heavy audio (technical explanation) and heavy visual content (code, diagrams):

1. First pass: audio-focused — transcribe with speaker attribution and timestamps
2. Second pass: visual-focused — "Given this transcription [attach first pass output], now identify all visual content shown that adds information not in the transcript"

This is more reliable than asking for everything in one pass, because the model's attention is not split.

---

#### Known Limitations and Failure Modes

**1 FPS temporal blind spots**
Any content that appears for less than 1 second — a flash of code, a rapidly scrolled terminal, a diagram shown briefly — may not be sampled. For screen recording analysis, pre-process the source video to ensure key frames are held for at least 2 seconds, or request higher FPS sampling.

**In-video OCR regression**
Multiple users across Gemini 2.5 Pro, Flash, and Flash-lite documented that in-video text extraction produces nonsense (unrelated text, hallucinated content) while static image OCR from the same frames works correctly. This appears to be a persistent issue as of early 2026 with no official resolution. Workaround: extract key frames as images using FFmpeg and pass them as image inputs alongside the video, or use a two-pass approach (video for audio, frames for text).

**Hallucination under uncertainty**
Gemini (especially 3 Flash, but also Pro) does not reliably say "I don't know." When asked about a detail it cannot find in the video, it will often confabulate. Mitigation:
- Require timestamp citations for every factual claim — non-existent timestamps expose hallucinations
- Add `"confidence": "stated" | "inferred" | "unclear"` to schema fields
- Explicitly instruct: "If you cannot find evidence for a claim in the video, set the field to null rather than guessing"
- Cross-reference model outputs against video at random timestamps to calibrate reliability

**Temporal reasoning inconsistency**
Gemini can count events across a video (demonstrated: 17 phone-use instances in a 90-minute video) but struggles with more complex temporal queries like "what changed between the first and third approach shown." This is better with `thinking_level=high` but not eliminated. Frame complex temporal queries as explicit comparisons: "Describe the approach shown at 10:00, then describe the approach shown at 40:00, then explain what changed."

**Videos without audio streams (Gemini 3 bug)**
Gemini 3 models fail with a 404 NOT_FOUND error on videos that have no audio track, unless `media_resolution=MEDIA_RESOLUTION_HIGH` or `MEDIA_RESOLUTION_UNSPECIFIED` is set. Screen recordings without audio, silent demo videos, and tutorial files with audio stripped are all affected. Gemini 2.5 does not have this bug.

**Audio non-speech limitations**
The official docs state: "models that support audio might make mistakes recognizing sound that's not speech." Background noise, non-verbal audio events, and music are unreliable. Stick to speech content for audio extraction.

**YouTube resolution control**
When using YouTube URLs directly (rather than file upload), there is no API parameter to control which resolution YouTube serves. You cannot request a specific video quality when using the URL method. This affects OCR reliability for YouTube videos with high information density.

**Grounding hallucinations**
When using grounding with Google Search alongside video analysis, hallucinated grounding references (URLs cited that were not in grounding chunks) have been documented by users. Grounding reduces hallucination from the model's knowledge but does not eliminate it.

---

### Recommendations for Building a Prompt Engineering Layer

1. **Build a `MEDIA_RESOLUTION_HIGH` default into your layer.** The cost increase (3x tokens) is justified for any task involving text on screen. Make low resolution opt-in, not opt-out.

2. **Create purpose-specific system instruction templates** (4-5 templates matching your use cases). The system instruction should define role, output contract, timestamp requirements, and confidence handling. Store these as named templates in your CLI tool.

3. **Always enforce `response_schema` via API parameter**, not prompt instructions. Define Pydantic/Zod schemas for each template type. Make schema validation part of your pipeline before the output reaches the user.

4. **Require `timestamp` fields on every extracted claim.** Make this non-optional in the schema. Missing or invalid timestamps are the primary signal of hallucinated content.

5. **Add a `confidence` enum to every significant extracted field.** Values: `"stated"` (speaker explicitly said this), `"inferred"` (visible from context), `"unclear"` (ambiguous or not found). This makes model uncertainty explicit rather than invisible.

6. **Implement two-pass for OCR-heavy content.** Pass 1: full video for audio/narrative extraction. Pass 2: extracted key frames as images for text-on-screen extraction. Run passes in parallel and merge.

7. **Handle silent videos explicitly.** If your tool processes screen recordings or silent tutorials, detect audio absence before API call and set `media_resolution=MEDIA_RESOLUTION_HIGH` to avoid the Gemini 3 404 bug.

8. **Set `temperature=0.0`** for all structured extraction tasks. Use higher temperature only if you add a narrative synthesis step that needs variation.

9. **Use `thinking_level=high`** for complex multi-topic talks. This has measurable impact on comparative and temporal reasoning tasks at the cost of latency. Make it configurable per use case.

10. **Build a spot-check harness into your CLI.** Take 3-5 random timestamp claims from output, jump to those timestamps in the video, verify the claim. This establishes per-talk confidence rather than relying on the model's self-assessment.

---

### Open Questions

- Whether the in-video OCR regression has been patched in more recent Gemini 3 point releases (no official resolution documented as of early 2026)
- Practical accuracy of speaker diarization for technical talks with 2-3 panelists at similar voice pitches
- Whether custom FPS sampling (above 1 FPS) meaningfully improves code screen-recording analysis or just increases token cost
- Optimal thinking budget allocation for different talk lengths — no empirical data found
- Whether the YouTube URL path uses the same frame sampling as the File API, or applies different internal preprocessing

---

### Sources

1. [Video understanding | Gemini API](https://ai.google.dev/gemini-api/docs/video-understanding) - Primary reference for frame sampling rate, token counts, duration limits, format support, timestamp handling
2. [Advancing the frontier of video understanding with Gemini 2.5 - Google Developers Blog](https://developers.googleblog.com/en/gemini-2-5-video-understanding/) - Gemini 2.5 benchmarks (VideoMME 85.2%), audio-visual integration improvements, use case demonstrations
3. [Structured outputs | Gemini API](https://ai.google.dev/gemini-api/docs/structured-output) - `response_schema` parameter, Pydantic/Zod patterns, schema field types, best practices
4. [Media resolution | Gemini API](https://ai.google.dev/gemini-api/docs/media-resolution) - Token counts per resolution level, per-part resolution control (Gemini 3), tradeoffs
5. [Gemini response nonsense when prompting to OCR texts in video - Google AI Forum](https://discuss.ai.google.dev/t/gemini-response-nonsense-when-prompting-it-to-ocr-texts-in-video/107315) - Community report of in-video OCR regression across all Gemini variants
6. [Optimal Video Pre-processing Parameters - Google AI Forum](https://discuss.ai.google.dev/t/optimal-video-pre-processing-parameters-fps-resolution-for-file-api/87440) - Community findings on pre-processing at 1 FPS before upload, 720p optimal resolution
7. [Best practices for video pre-processing with media_resolution - Google AI Forum](https://discuss.ai.google.dev/t/best-practices-for-video-pre-processing-resolution-with-media-resolution-parameter-in-gemini-3-0/109808) - Community discovery that 360-480p pre-processing is sufficient, internal downscaling behavior
8. [Gemini 3 error 404 with videos without audio stream](https://discuss.ai.google.dev/t/gemini-3-error-404-not-found-with-videos-without-an-audio-stream-and-media-resolution-not-set-to-high/113805) - Bug documentation: silent videos fail on Gemini 3 without explicit media_resolution
9. [Prompt design strategies | Gemini API](https://ai.google.dev/gemini-api/docs/prompting-strategies) - Official few-shot, decomposition, formatting guidance
10. [Gemini 3 Prompting: Best Practices - philschmid.de](https://www.philschmid.de/gemini-3-prompt-practices) - XML template structure, media-first ordering, context placement rules
11. [System Instructions and Prompting Fundamentals - DeepWiki](https://deepwiki.com/google-gemini/cookbook/3.4-system-instructions-and-prompting-fundamentals) - System instruction persistence, role assignment, configuration patterns
12. [Video Analysis and Understanding - DeepWiki Gemini Cookbook](https://deepwiki.com/google-gemini/cookbook/5.4-video-analysis-and-understanding) - Concrete prompt patterns, state machine for file upload, model selection guidance
13. [Gemini CLI Tips and Tricks - Addy Osmani](https://addyosmani.com/blog/gemini-cli/) - `@` file reference syntax, GEMINI.md context files, headless scripting, custom slash commands
14. [Gemini 2.0 Video Understanding - Google AI Forum](https://discuss.ai.google.dev/t/gemini-2-0-video-understanding/58261) - Community questions and findings about video encoding, resolution, frame rate tradeoffs
15. [Why Gemini 2.5 Pro Won't Stop Talking - 16x Engineer](https://eval.16x.engineer/blog/gemini-2-5-pro-verbose-output-control) - "Be concise" instruction effectiveness, 1.7k → 1.4k token reduction, task-type caveats
16. [Technical Report: Multimodal Inconsistencies in Google Gemini - Medium](https://medium.com/@jabbalarajamohan/technical-report-multimodal-inconsistencies-in-google-gemini-9b15bcc81fb4) - Embedding misalignment as source of errors, modality inconsistency patterns
17. [Gemini 3 Flash Hallucination Rate - Better Stack](https://betterstack.com/community/guides/ai/gemini-3-flash-review/) - 91% confabulation rate on AA-Omniscience (meaning: invents when it doesn't know), mitigation strategies
18. [Gemini's Hidden Power: Speaker Diarization - Medium](https://medium.com/@samarrana407/geminis-hidden-power-the-ultimate-guide-to-speaker-diarization-audio-transcription-ad9a1a660244) - Speaker identification prompts, two-pass transcription strategy
19. [Gemini Video Analysis Test - Android Police](https://www.androidpolice.com/tested-geminis-video-analysis-heres-what-happened/) - Independent test findings: temporal data failure (dates), strong contextual pattern matching, location identification
20. [Google Gemini multimodal input 2025 - Data Studios](https://www.datastudios.org/post/google-gemini-multimodal-input-in-2025-vision-audio-and-video-capabilities-explained) - Summary of 2025 capability landscape

---

## Sources

1. [Video understanding | Gemini API](https://ai.google.dev/gemini-api/docs/video-understanding)
2. [Advancing the frontier of video understanding with Gemini 2.5 - Google Developers Blog](https://developers.googleblog.com/en/gemini-2-5-video-understanding/)
3. [Structured outputs | Gemini API](https://ai.google.dev/gemini-api/docs/structured-output)
4. [Media resolution | Gemini API](https://ai.google.dev/gemini-api/docs/media-resolution)
5. [Gemini response nonsense when prompting to OCR texts in video - Google AI Forum](https://discuss.ai.google.dev/t/gemini-response-nonsense-when-prompting-it-to-ocr-texts-in-video/107315)
6. [Optimal Video Pre-processing Parameters - Google AI Forum](https://discuss.ai.google.dev/t/optimal-video-pre-processing-parameters-fps-resolution-for-file-api/87440)
7. [Best practices for video pre-processing with media_resolution - Google AI Forum](https://discuss.ai.google.dev/t/best-practices-for-video-pre-processing-resolution-with-media-resolution-parameter-in-gemini-3-0/109808)
8. [Gemini 3 error 404 with videos without audio stream](https://discuss.ai.google.dev/t/gemini-3-error-404-not-found-with-videos-without-an-audio-stream-and-media-resolution-not-set-to-high/113805)
9. [Prompt design strategies | Gemini API](https://ai.google.dev/gemini-api/docs/prompting-strategies)
10. [Gemini 3 Prompting: Best Practices - philschmid.de](https://www.philschmid.de/gemini-3-prompt-practices)
11. [System Instructions and Prompting Fundamentals - DeepWiki](https://deepwiki.com/google-gemini/cookbook/3.4-system-instructions-and-prompting-fundamentals)
12. [Video Analysis and Understanding - DeepWiki Gemini Cookbook](https://deepwiki.com/google-gemini/cookbook/5.4-video-analysis-and-understanding)
13. [Gemini CLI Tips and Tricks - Addy Osmani](https://addyosmani.com/blog/gemini-cli/)
14. [Gemini 2.0 Video Understanding - Google AI Forum](https://discuss.ai.google.dev/t/gemini-2-0-video-understanding/58261)
15. [Why Gemini 2.5 Pro Won't Stop Talking - 16x Engineer](https://eval.16x.engineer/blog/gemini-2-5-pro-verbose-output-control)
16. [Technical Report: Multimodal Inconsistencies in Google Gemini - Medium](https://medium.com/@jabbalarajamohan/technical-report-multimodal-inconsistencies-in-google-gemini-9b15bcc81fb4)
17. [Gemini 3 Flash Hallucination Rate - Better Stack](https://betterstack.com/community/guides/ai/gemini-3-flash-review/)
18. [Gemini's Hidden Power: Speaker Diarization - Medium](https://medium.com/@samarrana407/geminis-hidden-power-the-ultimate-guide-to-speaker-diarization-audio-transcription-ad9a1a660244)
19. [Gemini Video Analysis Test - Android Police](https://www.androidpolice.com/tested-geminis-video-analysis-heres-what-happened/)
20. [Google Gemini multimodal input 2025 - Data Studios](https://www.datastudios.org/post/google-gemini-multimodal-input-in-2025-vision-audio-and-video-capabilities-explained)
