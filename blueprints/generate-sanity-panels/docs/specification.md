# Generate Sanity Panels — Specification

Each stage = one subagent. Orchestrator validates artifacts + gates. Load: index → one domain → one target → `domainSnapshot` in artifact. Stages 2–9 use artifact only.

**First run:** clarify project outline before Stage 1 — `target`, `brief`, `domain`, **run credentials** (`constants/urls.md`). Then target requirements (`product` → `productId`; `article`/`email` → none). See [SKILL.md](../SKILL.md) FIRST RUN.

I/O vars per stage: [activity-diagram.md](activity-diagram.md).

Hard rules: see [SKILL.md](../SKILL.md) — draft only, nine gates, max 2 same `_type`, no `markdown`/`richText` panel types, no self-surface links, HTTP Sanity I/O with CLI-passed credentials (never hardcoded).

## Stages (summary)

| # | Stage | Out artifact |
|---|---|---|
| 1 | Definition | `definitionBundle`, `domainSnapshot`, `template` |
| 2 | Personas | `personas[]` |
| 3 | Research Strategy | `topics[]` |
| 4 | Research Findings | `findings[]`, `products[]` |
| 5 | Desired Content | `desiredPageContent` |
| 6 | Media | `pageWithMedia` |
| 7 | Draft | `draftPatch`, `previewUrl`, `panelsUsed[]` |
| 8 | Audit | `auditResult` |
| 9 | Publish | `publishedId` |

Gate after each stage. `userFeedback` restarts that stage. Audit fail → Definition with `auditFlags`.

## Stage notes

**4 Research Findings** — parallel subagents: one per `topics[]` + one Algolia when catalogue supports. Merge compact JSON only. Product cards include stock + fulfillment for gate/selection only (not on-page copy). FAQ candidates carry `source` provenance. `findings-raw/` is debug-only on disk.

**5 Desired Content** — creative mockup: near-final copy + `pageStructure` wireframe + `imageIntent` with safe zones. `blocks[]` only. Outbound links only — no self-surface URLs. No `markdown`/`richText` panel types. Gate presents layout/purpose/image/title/body/CTA per block.

**6 Media** — Phase A locks `targetPanelType` + dimensions. Phase B: generate/crop custom art only; catalogue via picker IDs (no cover upload); naming `{target}-{id}__{role}__{desc}` for generated uploads.

**7 Draft** — honor Media lock 1:1; fill schema-required fields; comparison matrices fully populated; single canonical `draftPatch`.

**8 Audit** — **mandatory browser preview** + deterministic checklist (`no_richtext_panel`, `no_self_surface_links`, matrix rows, etc.). No Gate 8 without `auditResult.json` + preview evidence.

**9 Publish** — explicit user yes. `publish_sanity_document.py` with CLI credentials. Remind internal sign-off first.
