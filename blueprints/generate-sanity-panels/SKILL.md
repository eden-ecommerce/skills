---
name: generate-sanity-panels
description: Orchestrates content-first Sanity panel drafts via 9 subagent stages with user gates. Product, article, email. Domain + target swappable prompts. Use when building Sanity panel pages, blog articles, product content strips, or email slices from a brief.
---

# GENERATE SANITY PANELS

Thin orchestrator. One subagent per stage. Orchestrator validates artifacts + runs gates only.

**Gate machine:** nine stages, nine gates — see `docs/state-machine.md`. Stage refs live under `references/{N}-*/` per `docs/file-structure.md`. Load only the current stage's `shared.md` + target overlay; rules are not duplicated in this file.

## HARD RULES

- Draft only (`_id` prefix `drafts.`). Publish after explicit user yes.
- Never preview on `www.eden.co.uk`. Use the preview host the user supplied at FIRST RUN.
- **Generated or custom panel art = Sanity assets.** Catalogue imagery = picker IDs or CDN URL per schema — never duplicate catalogue covers into Sanity when picker resolves them.
- Max 2 identical panel `_type` on one surface. Prefer distinct layout jobs over same-family variants.
- **Never use panel `_type` `markdown` or `richText`** on any target. Use structured gallery panels (`highlightBlock`, FAQ panels, hero overlays, labelled comparison charts, tile grids, carousels, etc.). A Sanity **field** named `richText[]` (article embeds) is not permission to use the `richText` panel type.
- **No self-surface links:** never link CTAs, `edenLink`, or copy URLs back to the **seed content surface** the user is already on. Link outbound only — maker/brand pages, other catalogue entities, trusted external sources. See `references/5-desired-content/shared.md`.
- Nine user gates. No silent draft to publish.
- One subagent per stage. No agent does research + draft + publish.
- Max 2 ref files per stage. Stages 2–9 use `domainSnapshot` from artifact, not re-read domain file.
- **Reader-facing copy:** human labels + outbound links only — never raw internal IDs (`productId`, SKU codes, Sanity `_id`) in panel body/FAQ/CTA text.
- **No em-dash voice:** never use em-dash (`—`, `–`, `\u2014`, `\u2013`) in reader copy — reads as AI-generated. Use commas, colons, parentheses, or a new sentence. See `references/shared/copy-voice.md`.
- **No markdown in plain string fields:** panel `body`, FAQ `answer`, banner text, etc. are not markdown — no `>`, `**`, `[text](url)`. Use panel headings, testimonial panels, and `edenLink` CTAs.
- **Stage 8 refinement pass:** Audit is not checklist-only — refine section titles, copy, layout rhythm, comparison columns, banner length, and CTA contrast before sign-off (`references/8-audit/shared.md`, `references/shared/page-structure.md`).
- **No cross-panel content reuse:** never pad a tile/grid panel by copying title+body (or the same image `_ref`) from another block. Schema cardinality must be filled with **on-job** items only — or pick a panel type whose count matches.
- **No chrome / strip overlap:** Stage 5 must map live surface chrome jobs vs strip jobs; strip never restates buy-box title/price/FBT/reviews aggregate as its primary beat. FAQ must not fully rehash a prior panel’s answer.
- **Carousels omit seed:** `productCarousel` never includes seed `productId` or same-title format siblings; `showPrice: false`.
- **Preflight pillars:** before Gate 5 and Gate 8, score Commerce / Engagement / SEO / Conversion against `references/shared/page-structure.md` quality pillars.
- **CRE conversion (product strips):** What Next safe-step CTAs, outcome headlines, hero product clarity, top 2–3 hesitation gap coverage, cross-sell harmony with live FBT — see `references/shared/cre-conversion.md`. Stage 5 must emit `hesitationGapMap` + `buyQuestion` per block; Stage 8 runs CRE checklist ids.
- **Customer-facing copy:** no CMS/merchandising jargon, Helpdesk placeholders, or fourth-wall meta — see `references/shared/copy-voice.md`. FAQ tone is the benchmark for all body copy.
- **Scannable layout:** title + `sectionSubtitle` on every block; heading character limits; max 3 lines per markdown paragraph; 6–9 block module budget on product strips — see `references/shared/page-structure.md`.
- **Panel bans (product):** never `featuredOrganisationJobs`, `organisationJobSearch`, or `appJobs`. No store-policy FAQ (returns/dispatch). One maker-catalogue CTA job per strip.
- **Locked palette:** Stage 5 `designConcept` + Stage 6 `visualSystem` use domain tokens (`constants/domains/eden.md`); audit `palette_consistency`.
- **Product catalogue link:** Eden preview resolves panels by Sanity `product.title` = `{ISBN} - {name}` (Algolia `manuf_ref`). Set via `draftPatch` `title` / `set.title` — see `references/7-draft/product.md`.
- **No secrets in the skill.** Never hardcode project id, dataset, tokens, or host URLs. Collect at FIRST RUN. Pass on every script CLI. Never write tokens into artifacts, gate summaries, or skill files.

## FIRST RUN — PROJECT OUTLINE

Before any stage, clarify the outline **and** run credentials. Do not spawn Definition until all of this is set.

| Definition | What | How to resolve |
|---|---|---|
| **target** | What we are building | Load `constants/targets/_index.md`. Ask user if missing. |
| **brief** | What the content is about | Ask user for a short narrative brief. |
| **domain** | Whose brand / catalogue / CMS | Load `constants/domains/_index.md`. Ask user if missing. |
| **credentials** | CMS + catalogue + preview access | Load `constants/urls.md`. Ask user. Block if missing. |

Confirm aloud as the project outline, then collect **target requirements** from the chosen target file:

| target | Extra requirements |
|---|---|
| `product` | **`productId`** (Eden `product_id`) — required. Block until provided. |
| `article` | None — narrative brief is enough. |
| `email` | None — narrative brief is enough. |

If `domain.requiresTenantBrief` → also collect `tenantBrief` before Definition.

Then collect **run credentials** (same gate as `productId`). User pastes values in chat — e.g. `productId=1000000`, `NEXT_PUBLIC_SANITY_PROJECT_ID=…`. Names and when-required: `constants/urls.md`.

**Pass-through:** keep tokens in session only. Prefix env vars or pass `--flags` on every script. Non-secret `projectId`, `dataset`, `schemaUrl`, and hosts go into `domainSnapshot`. Never tokens.

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

**Ref layering:** rules live in `shared.md` (all targets). Target overlays (`product.md`, `article.md`, `email.md`) add surface-specific identifiers and panel-field mapping only — do not duplicate shared rules.

## ORCHESTRATION

Each stage:

1. Spawn `Task` `generalPurpose` with stage ref paths + artifact JSON path + output contract
2. Validate required keys on artifact file under `scripts/.artifacts/{runId}/`
3. Gate: show condensed summary; block until user approves or gives `userFeedback`
   - **Gate 5 special:** present a **wireframe mockup** (layout kind, purpose, image src intent, final title/body, CTA + URL per block) — see `references/5-desired-content/shared.md` Gate presentation. Do not ship a block-id table alone.
   - **Gate 8 special:** present Audit **checklist table** (id / pass|fail / evidence) from `auditResult.json` — see `references/8-audit/shared.md`. **No Gate 8 summary without `auditResult.json` and preview evidence.**
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
- Findings: fixed small schema per topic agent + `contentRelevance`; no live-surface chrome-duplicate specs
- Maker = author, brand, or manufacturer by entity type
- Handoff = artifact path + one-line summary
- Stage 5: no `motionIntent`; `blocks[]` only; **`sectionTitle` + `sectionSubtitle` + `buyQuestion` on every block**; **`chromeOverlapMap`** + **`hesitationGapMap`** (CRE); product module budget 6–9; full content mockup at Gate 5; see `references/shared/page-structure.md`, `references/shared/cre-conversion.md`
- Stage 6: Phase A locks `targetPanelType` + dimensions; locked `visualSystem.palette` from domain; crop to target pixels before upload; catalogue = picker IDs (no cover upload); generated filenames `{target}-{id|slug}__{role}__{desc}`
- Stage 7: fill schema-required fields **on-job** (no tile padding from other blocks); honor Media lock; map `sectionTitle` + `sectionSubtitle` to panel `title`/`heading`/`subheading`; gallery-first mapping; single canonical `draftPatch` + `draftResult`; strip self-surface links; carousel omits seed; reject jobs panels on product
- Stage 8: mandatory browser preview + deterministic checklist (incl. dedup / FAQ rehash / format coverage / **Skip if** + **CRE** + **layout/copy ids**: `customer_facing_copy`, `scannable_body`, `heading_char_limits`, `section_subtitle_present`, `panel_spacing`, `hero_product_clarity`, `module_budget`, `one_maker_cta`, `no_jobs_widget`, `no_store_policy_faq`, `palette_consistency`) + **refinement pass** (`copy-voice.md`, `cre-conversion.md`, `page-structure.md`) — Audit loads `draftPatch` + `pageWithMedia` path, not full schema

## SCRIPTS

Pass FIRST RUN credentials on every call — env prefix **or** `--flags`. See `references/7-draft/http-sanity.md`.

```bash
python3 scripts/fetch_algolia.py <product_id> --algolia-app-id … --algolia-search-key …
python3 scripts/fetch_algolia.py --filter 'author:"Name" AND stores:eden' --query "" --algolia-app-id … --algolia-search-key …
bash scripts/fetch_schema.sh <schemaUrl>
python3 scripts/get_sanity_document.py --product-id <id> --project-id … --dataset … --token …
python3 scripts/upload_sanity_image.py <file> --filename <name> --project-id … --dataset … --token …
python3 scripts/patch_sanity_draft.py scripts/.artifacts/<run>/draftPatch.json --project-id … --dataset … --token …
python3 scripts/publish_sanity_document.py <draftId> --project-id … --dataset … --token …
```

Equivalent env prefix (same names as `constants/urls.md`):

```bash
ALGOLIA_APP_ID=… ALGOLIA_SEARCH_KEY=… python3 scripts/fetch_algolia.py <product_id>
NEXT_PUBLIC_SANITY_PROJECT_ID=… NEXT_PUBLIC_SANITY_DATASET=… SANITY_API_EDITOR_TOKEN=… \
  python3 scripts/patch_sanity_draft.py scripts/.artifacts/<run>/draftPatch.json
```
