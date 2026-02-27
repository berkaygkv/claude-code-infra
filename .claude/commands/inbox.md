# Inbox Capture Command

Append an idea to `vault/inbox.md` mid-session.

## Usage

```
/inbox [idea text]
```

## Instructions

When the user invokes `/inbox`, perform these steps:

### Step 0: Resolve Vault Path

The vault is the directory containing `.obsidian/` inside the project root. All `vault/` references below use this as the default — substitute with the actual vault directory name if different.

### Step 1: Get the idea

If `$ARGUMENTS` is provided, use it as the idea text.
If empty, ask: "What should I capture?"

### Step 2: Append to inbox

Read `vault/inbox.md` using native Read.

Append a new line at the end:

```
- {idea text} (S{current_session + 1})
```

Use the current session number from `vault/scratch.md` header (parse from "Session {N}").

Update the `updated` field in frontmatter to today's date.

### Step 3: Confirm

```
Captured to inbox: {idea text}
```

## Notes

- No shaping, no formatting — raw capture only
- Session tag `(S{N})` provides provenance
- Triage happens at `/begin` when count > 5, not here
