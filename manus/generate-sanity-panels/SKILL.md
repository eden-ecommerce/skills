---
name: generate-sanity-panels
description: Build Sanity panel drafts for Eden page types. Open research, persona-scored design, user feedback gates, entity gallery, draft, preview. Product, home, browse, article, hub, organisation.
---

# GENERATE SANITY PANELS

## HARD RULES

- Draft only (`_id` prefix `drafts.`). Publish only after explicit user yes.
- No Storybook. No Studio `previewUrl`.
- Panel images → Sanity assets only. No external URLs in final draft.
- Preview token sensitive. Never log or commit.
- Three user feedback gates mandatory (see FLOW). No silent draft→publish.

## ENV

Load `scripts/.env` for local scripts. See `scripts/.env.example`.

| Var | Use |
|---|---|
| `ALGOLIA_APP_ID` / `ALGOLIA_SEARCH_KEY` | `fetch_algolia.py` |
| `NEXT_NEXT_EDEN_BASE_URL` | Gallery + preview base (next-next-eden) |
| `EDEN_BLOG_BASE_URL` | Article gallery base (eden-blog) |
| `SANITY_PREVIEW_TOKEN` | `/api/preview` draft URLs |

Sanity project `bct7esy7`, dataset `eden` — MCP auth, not `.env`.

## FLOW

### 0 — CLARIFY TARGET + PERSONAS

If user did not state target, ask. Collect inputs per target.

→ [targets.md](references/targets.md)

Identify **2–4 personas** (shopper, gift buyer, church buyer, org visitor, SEO reader, etc.). State jobs-to-be-done and what “good” looks like per persona.

### 1 — GATHER DATA

Seed from Algolia, Eden API, existing Sanity doc, public web.

```bash
python3 scripts/fetch_algolia.py <PRODUCT_ID>
```

→ [2-gather-data.md](references/2-gather-data.md)

### 2 — RESEARCH (open-ended)

Deep/wide research before any panel typing. You choose topics and depth.

Start from gathered data. Expand wherever it strengthens the page — author, publisher, category story, FAQs, related catalogue, official assets, competitors, SEO intent, engagement hooks.

Stop when you can sketch the full page with confidence. No fixed checklist.

### 3 — DESIGN + SCORE

Design ideal page **before** panels. Narrative flow, not panel catalogue order.

Per section: purpose, copy angle, assets, SEO value. Score each candidate 0–5 on:

- Persona fit (per persona, then mean)
- SEO / discoverability
- Engagement
- Clarity / trust
- Feasibility (gallery `_type` exists + assets available)

Rank. Drop weak filler. Show ranked table to user.

**GATE 1:** User confirms narrative, personas, ranked sections (or edits weights / drops sections). Do not proceed without approval.

### 4 — GALLERY + SCHEMA

Fetch entity gallery (one URL per target):

| Target | Gallery URL |
|---|---|
| article | `{EDEN_BLOG_BASE_URL}/panels/article` |
| product, home, category, department, hub, organisation | `{NEXT_NEXT_EDEN_BASE_URL}/panels/{entity}` |

Parse `#panel-catalogue` JSON from page. Scroll samples for layout intent.

Schema:

```bash
curl -s https://cms.eden.co.uk/schema.json -o schema.json
python3 scripts/extract_panels.py schema.json <docName> [fieldName]
```

→ [1-schema-and-gallery.md](references/1-schema-and-gallery.md)

### 5 — FIT

Map scored sections → panel `_type`s from gallery + schema. Adapt to field constraints. Fewer strong panels beats filler.

**GATE 2:** User confirms panel map (`_type` + order + purpose). Do not write Sanity until approved.

### 6 — DRAFT

Fetch Sanity doc. Patch `drafts.<id>`. Article: embed panels in `richText[]`, not top-level `panels`.

→ [3-sanity-document.md](references/3-sanity-document.md)

### 7 — PREVIEW + GATE 3

Open preview URL. Scroll full page. Re-score vs personas. Patch loop until pass threshold or user says ship.

→ [4-preview-and-verify.md](references/4-preview-and-verify.md)

**GATE 3:** User rates preview vs personas or accepts agent re-score. Iterate until satisfied.

### 8 — PUBLISH

Explicit user yes → `manus-mcp-cli tool call publish_documents --server sanity`.
