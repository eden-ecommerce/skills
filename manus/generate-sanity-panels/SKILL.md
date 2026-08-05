---
name: generate-sanity-panels
description: Orchestrates content-first Sanity panel drafts via 9 subagent stages with user gates. Product, article, email. Domain + target swappable prompts. Use when building Sanity panel pages, blog articles, product content strips, or email slices from a brief.
---

# GENERATE SANITY PANELS

Thin orchestrator. One subagent per stage. Orchestrator validates artifacts + runs gates only.

## HARD RULES

- Draft only (`_id` prefix `drafts.`). Publish after explicit user yes.
- Never preview on `www.eden.co.uk`. Use `{NEXT_NEXT_EDEN_BASE_URL}` from env.
- **Generated or custom panel art = Sanity assets.** Catalogue product imagery = picker IDs or CDN URL per schema — never duplicate catalogue covers into Sanity when picker resolves them.
- Max 2 identical panel `_type` on one page. Prefer distinct layout jobs over same-family variants.
- Never use `markdown` panel `_type`.
- Nine user gates. No silent draft to publish.
- One subagent per stage. No agent does research + draft + publish.
- Max 2 ref files per stage. Stages 2–9 use `domainSnapshot` from artifact, not re-read domain file.
- **Reader-facing copy:** human labels + links only — never raw internal IDs (`productId`, SKU codes, Sanity `_id`) in panel body/FAQ/CTA text.

## ENV

`set -a && source scripts/.env && set +a` — see `scripts/.env.example`, [constants/urls.md](constants/urls.md).

Sanity `NEXT_PUBLIC_SANITY_PROJECT_ID` / `NEXT_PUBLIC_SANITY_DATASET` via `manus-mcp-cli` MCP auth.

## FIRST RUN — PROJECT OUTLINE

Before any stage, clarify the three required definitions. Do not spawn Definition until all three are set. This outline drives every later stage.

| Definition | What | How to resolve |
|---|---|---|
| **target** | What we are building | Load `constants/targets/_index.md`. Ask user if missing. |
| **brief** | What the content is about | Ask user for a short narrative brief. |
| **domain** | Whose brand / catalogue / CMS | Load `constants/domains/_index.md`. Ask user if missing. |

Confirm aloud as the project outline, then collect **target requirements** from the chosen target file:

| target | Extra requirements |
|---|---|
| `product` | **`productId`** (Eden `product_id`) — required. Block until provided. |
| `article` | None — narrative brief is enough. |
| `email` | None — narrative brief is enough. |

If `domain.requiresTenantBrief` → also collect `tenantBrief` before Definition.

Only then proceed to Stage 1.

## LOAD PROTOCOL

| When | Load |
|---|---|
| Domain pick | `constants/domains/_index.md` |
| Domain chosen | one `constants/domains/{id}.md` once at Definition |
| Target pick | `constants/targets/_index.md` |
| Target chosen | one `constants/targets/{T}.md` + stage ref |
| Stage N | `references/{N}-*/shared.md` + `{T}.md` if exists + prior artifact JSON path |

Forbidden: all domains, all targets, unrelated stage refs.

## ORCHESTRATION

Each stage:

1. Spawn `Task` `generalPurpose` with stage ref paths + artifact JSON path + output contract
2. Validate required keys on artifact file under `scripts/.artifacts/{runId}/`
3. Gate: show condensed summary; block until user approves or gives `userFeedback`
   - **Gate 5 special:** present a **wireframe mockup** (layout kind, purpose, image src intent, final title/body, CTA + URL per block) — see `references/5-desired-content/shared.md` Gate presentation. Do not ship a block-id table alone.
   - **Gate 8 special:** present Audit **checklist table** (id / pass|fail / evidence) — see `references/8-audit/shared.md`. No pass summary without preview evidence.
4. Reject: re-run same stage with feedback. Audit fail: restart Definition with `auditFlags`

### Stage map

| # | Stage | Ref | Out artifact |
|---|---|---|---|
| 1 | Definition | `references/1-definition/` | `definitionBundle`, `domainSnapshot`, `template` |
| 2 | Personas | `references/2-personas/` | `personas[]` |
| 3 | Research Strategy | `references/3-research-strategy/` | `topics[]` |
| 4 | Research Findings | `references/4-research-findings/` | `findings[]`, `products[]` |
| 5 | Desired Content | `references/5-desired-content/` | `desiredPageContent` (copy + imageIntent/safeZones; no motionIntent) |
| 6 | Media | `references/6-media/` | `pageWithMedia` (`imageBrief[]` locked type+dims; generate custom art only) |
| 7 | Draft | `references/7-draft/` | `draftPatch`, `previewUrl`, `panelsUsed[]` |
| 8 | Audit | `references/8-audit/` | `auditResult` (mandatory preview + checklist) |
| 9 | Publish | `references/9-publish/` | `publishedId` |

Gate after every stage. Audit fail → Definition.

### Token budget

- Schema: `scripts/.cache/*-panels.json` allowlist only — never full `schema.json` in prompt
- Algolia: subagent summarizes to product cards (incl. stock/fulfillment for gate/selection); raw JSON stays on disk in `findings-raw/` (debug only — orchestrator never reloads after merge); **never render price/stock/dispatch in panel copy**
- Social proof research: keep source choice open — do not prescribe named retailers/review sites as layout models
- Findings: fixed small schema per topic agent + `contentRelevance`; no live-page chrome-duplicate specs
- Maker = author or manufacturer by product type
- Handoff = artifact path + one-line summary
- Stage 5: no `motionIntent`; `blocks[]` only (no parallel top-level `faq[]`); full content mockup at Gate 5; format siblings = text-led chooser
- Stage 6: Phase A locks `targetPanelType` + `dimensions`; crop to target pixels before upload; catalogue = picker IDs (no cover upload); generated filenames `{target}-{id|slug}__{role}__{desc}`
- Stage 7: fill schema-required fields; honor Media lock; single canonical `draftPatch` + `draftResult`
- Stage 8: mandatory browser preview + deterministic checklist — Audit loads `draftPatch` + `pageWithMedia` path, not full schema

## SCRIPTS

```bash
python3 scripts/fetch_algolia.py <product_id>
python3 scripts/fetch_algolia.py --filter 'author:"Name" AND stores:eden' --query ""
bash scripts/fetch_schema.sh
```

Sanity I/O: `manus-mcp-cli` — see `references/7-draft/mcp-sanity.md`.

Publish: explicit yes → `manus-mcp-cli tool call publish_documents --server sanity`.
