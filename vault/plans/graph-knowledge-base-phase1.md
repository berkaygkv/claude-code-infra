---
type: plan
title: "Build graph knowledge base — Phase 1 pipeline"
status: superseded
date: 2026-02-13
session: "[[sessions/session-38]]"
phases_total: 4
phases_done: 0
assumptions_total: 5
assumptions_validated: 0
---

# Build Graph Knowledge Base — Phase 1 Pipeline

## Goal

Build a reusable pipeline that crawls, chunks, extracts, resolves, and merges documents into a Neo4j knowledge graph for financial intelligence. Schema designed with Phase 2 (agentic workflows) in mind. Validate make-or-break assumptions before committing to architecture.

## Scope

**Includes:** Document ingestion, entity extraction, entity resolution, graph construction, schema enforcement, source reliability testing.

**Excludes:** Phase 2 agentic workflows, UI, production deployment, SearXNG setup (use manual source selection for spikes).

## Assumptions

### A1: Entity resolution works with LLM-based approach — CRITICAL
Claude structured output can extract entities from heterogeneous sources and merge them by recognizing naming variants, abbreviations, and implicit references. The seed calls this "make-or-break" — most knowledge graph projects fail here.
- **Spike:** 5 docs about the same entity (Anthropic) from different source types. Extract entities, attempt merge, measure accuracy.
- **If fails:** Direction-level. Pipeline needs schema-first approach (define entities upfront, match incoming data) rather than extraction-first (discover entities from docs). Return to brainstorm.
- **Finding:** _pending_
- **Impact:** _pending_

### A2: Schema stays consistent across heterogeneous documents — HIGH
Pre-defined schema + structured output constraints keep entity/relationship types consistent regardless of source format. Risk: LLM output can drift — doc 1 is clean, doc 50 invents fields.
- **Spike:** Process 10 diverse docs (news, filings, press releases, blog posts), measure schema conformance against a reference.
- **Finding:** _pending_
- **Impact:** _pending_

### A3: Crawl4AI extracts structured financial data reliably — MEDIUM
- **Spike:** Crawl 3 distinct financial sources (news site, SEC EDGAR, company blog), compare extraction completeness.
- **Finding:** _pending_
- **Impact:** _pending_

### A4: Neo4j + Supabase dual-store is worth the complexity — MEDIUM
- **Spike:** Store one document's full extraction in both, test Phase 2 query patterns. Does dual-store enable queries a single store can't?
- **Finding:** _pending_
- **Impact:** _pending_

### A5: Financial data richness achievable from public sources — MEDIUM
- **Spike:** Crawl 5 sources about one company. Catalog what's actually extractable vs. what the seed's "richness" requirement demands.
- **Finding:** _pending_
- **Impact:** _pending_

## Phases

_Ordering: risk-first, dependency-aware. A1 (critical) is standalone → Phase 1. A3/A4/A5 (medium, standalone) bundle into Phase 2. A2 (high) depends on a working pipeline from Phases 1-2 → Phase 3. Phase 4 is pure build, no assumptions left._

### Phase 1: Validate entity resolution
**Targets:** A1 (entity resolution — CRITICAL)
**Type:** Spike

- [ ] Select 5 documents about Anthropic from different source types
- [ ] Build minimal extraction: Claude structured output → entities + relationships
- [ ] Define merge logic: name matching, abbreviation handling, implicit reference resolution
- [ ] Run extraction + merge, measure accuracy (precision, recall, F1)
- [ ] Record finding in plan (A1)
- [ ] Assess impact: task / phase / direction

**Deliverable:** Finding on entity resolution viability. Approach recommendation.
**Branch:** `spike/entity-resolution`

### Phase 2: Validate pipeline architecture
**Targets:** A3 (Crawl4AI extraction), A4 (dual-store), A5 (data richness)
**Type:** Spike + build (spike first, then build on findings)

_Tasks provisional — will adjust based on Phase 1 findings._

- [ ] Set up Neo4j + Supabase locally (Docker)
- [ ] Crawl 3 financial sources with Crawl4AI, assess extraction quality (A3)
- [ ] Store one doc's extraction in both stores, test query patterns (A4)
- [ ] Catalog extractable data types vs. richness requirements (A5)
- [ ] Record findings (A3, A4, A5)
- [ ] Decide: proceed with dual-store or consolidate?

**Deliverable:** Working single-source pipeline + architecture findings.
**Branch:** `spike/pipeline-architecture` → merge to main if validated

### Phase 3: Schema enforcement + multi-source
**Targets:** A2 (schema consistency)
**Type:** Spike + build

_Tasks provisional — depend on Phase 1-2 findings._

- [ ] Design graph schema based on Phase 1-2 evidence
- [ ] Build schema validation layer (structured output constraints + post-extraction check)
- [ ] Process 10+ docs from mixed sources, measure drift (A2)
- [ ] Record finding (A2)
- [ ] Iterate schema enforcement until consistency target met

**Deliverable:** Schema-enforced pipeline handling multiple sources.

### Phase 4: Scale + harden
**Type:** Build (all assumptions should be validated by this point)

_Tasks fully provisional — shaped entirely by Phase 1-3 findings._

- [ ] Process 50+ documents
- [ ] Handle edge cases (temporal data, naming variants, conflicting data)
- [ ] Entity resolution at scale (performance, accuracy under volume)
- [ ] Documentation

**Deliverable:** Production-ready Phase 1 pipeline.

## Decisions

- [[decisions/validation-loop]] — spike assumptions before executing
- [[decisions/plan-protocol]] — standard format and lifecycle
