---
type: plan
title: "Create shared vocabulary reference card"
status: active
date: 2026-02-27
session: "[[sessions/session-53]]"
phases_total: 1
phases_done: 0
---

# Create Shared Vocabulary Reference Card

## Goal

Create `vault/reference/shared-vocabulary.md` — a protocol compression layer of 18 named concepts that govern recurring decision patterns. Structure supports atomic entry access for future selective loading. Unblocks the `/vocab` command (separate chore, not in this plan).

## Scope

**Includes:**
- Write the vocabulary card with all 18 entries (finalized on scratch)
- Add scratch surface anti-pattern (decided during markup review)
- Frontmatter with type, title, date, decision link
- Update CLAUDE.md § Key Paths to reference the card
- Update state.md: move shaped item to active, capture `/vocab` command as new inbox item

**Excludes:**
- Loading strategy (parked — structure-first, mechanism later)
- `/vocab` slash command (separate chore, captured to inbox)
- Idempotency removal (kept — weakest entry but defensible)

## Phases

### Phase 1: Write card and update references

**What gets done:** Write the vocabulary card from finalized scratch content. Update CLAUDE.md and state.md references.

- [ ] Write `vault/reference/shared-vocabulary.md` with all 18 entries, organized by domain (SWE / PM / System-Specific)
- [ ] Add frontmatter: `type: reference`, `title`, `date`, `decision: "[[decisions/scratch-collab-surface]]"` (no standalone decision — card is a reference artifact, not a locked design choice)
- [ ] Add scratch surface anti-pattern to entry 12
- [ ] Verify all session references match real sessions (S1, S10, S19, S35, S37, S40, S45, S48, S50, S52)
- [ ] Append `/vocab` command idea to `vault/inbox.md`

**Deliverables:**
- `vault/reference/shared-vocabulary.md` — the card
- Updated `vault/inbox.md` — `/vocab` command captured

## Decisions

- [[decisions/scratch-collab-surface]] — scratch surface designed in S48, vocabulary card continues the shared language thread
- [[decisions/pm-lifecycle]] — appetite/shaping/WIP entries align with lifecycle definitions
- [[decisions/validation-loop]] — validation loop + focus as currency entries anchored to S37
- [[decisions/stance-rewrite]] — reason first, evidence over abstraction, call the meta-work entries sourced from stance rules
