# gemwrap CLI Reference

Gemini API wrapper using OAuth from gemini-cli. Hits Google's Code Assist endpoint — separate quota pool from standard API keys.

**Install:** `pip install -e /Users/berkayg/Codes/gemwrap`
**Requires:** gemini-cli authenticated (`gemini` command, sign in via browser)

## YouTube Video Analysis

```bash
# Basic — prompt after URL
gemwrap --youtube "https://youtu.be/VIDEO_ID" "Summarize this video"

# With system instruction
gemwrap --youtube "https://youtu.be/VIDEO_ID" \
  --system "You are a technical analyst..." \
  "Extract key decisions from this talk"

# Full flags
gemwrap --youtube "https://youtu.be/VIDEO_ID" \
  --system "SYSTEM_INSTRUCTION" \
  -m gemini-2.5-pro \
  -t 0.1 \
  --max-tokens 8192 \
  "USER_PROMPT"

# Streaming (shows output as it generates)
gemwrap --stream --youtube "https://youtu.be/VIDEO_ID" "Key points?"
```

## Flags Relevant to This Skill

| Flag | Short | Description | Default |
|------|-------|-------------|---------|
| `--youtube` | | YouTube URL for video analysis | — |
| `--system` | `-s` | System instruction | none |
| `--model` | `-m` | Model name | account default |
| `--temperature` | `-t` | Temperature | 0.7 |
| `--max-tokens` | | Max output tokens | 8192 |
| `--stream` | | Stream response to stdout | off |
| `--account` | `-a` | Force specific account | round-robin |

## Model Selection

| Model | Use When |
|-------|----------|
| `gemini-2.5-pro` | Complex analysis, multi-topic talks, decision extraction, temporal reasoning |
| `gemini-2.5-flash` | Straightforward summaries, single-topic extraction, quick lookups |
| `gemini-3-flash-preview` | Latest model, good general performance — but higher hallucination risk under uncertainty |

## Accounts & Quota

- Two accounts configured: `pro` and `free` (round-robin by default)
- ~1,000 req/day per account, ~2,000 total
- Quota is shared with gemini-cli interactive use (same OAuth token)
- Check quota: `gemwrap --quota`
- Force account: `gemwrap -a pro "..."` or `gemwrap -a free "..."`

## Constraints

- **One video per request.** Cannot analyze multiple URLs in a single call.
- **Public/unlisted only.** Private videos fail.
- **Max 8 hours/day** of video processing (free tier).
- **No response_schema.** Structured output must be achieved via prompt engineering. The CLI doesn't expose the API's `response_schema` parameter.
- **No image upload.** Text prompts and YouTube URLs only.
- **Rate limits per-user.** Shared between gemwrap and gemini-cli.
