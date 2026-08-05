# Definition — shared

Stage 1 subagent. Output: `definitionBundle.json`

Orchestrator must already have clarified the project outline: **target**, **brief**, **domain**, plus any target-specific requirements (see `constants/targets/{T}.md`).

## In

- Confirmed `target`, `brief`, `domain`
- Target requirements (e.g. `productId` when `target=product`)
- One `constants/domains/{id}.md`
- One `constants/targets/{T}.md`
- `templates/{T}.md` for spine

## Process

1. Assert outline complete — if `target`, `brief`, or `domain` missing → block, ask user
2. Load target file → assert its **Requirements** table is satisfied (product → `productId`; article/email → none)
3. Resolve domain from `_index` → load one domain file
4. If `requiresTenantBrief` and no `tenantBrief` → block, ask user
5. Pick `template` spine from `templates/{T}.md`; adapt note for `{brief}` only
6. Distill `domainSnapshot` — copy id, website, delivery, tone, surfaces, locale, catalogue, cms, urls, constraints from domain file
7. Resolve CMS placeholders — if `cms.projectId` / `cms.dataset` are `{NEXT_PUBLIC_SANITY_PROJECT_ID}` / `{NEXT_PUBLIC_SANITY_DATASET}`, substitute from env (after `source scripts/.env`). Block if missing.
8. Do not invent catalogue items or panel `_type`s

## Out (`definitionBundle`)

```json
{
  "target": "article",
  "brief": "...",
  "domain": "eden",
  "productId": null,
  "template": ["Hero", "...", "CTA"],
  "domainSnapshot": { "id", "cms", "urls", "catalogue", "constraints", ... },
  "tenantBrief": null
}
```

`productId` required string when `target=product`; otherwise `null`.

Write to `scripts/.artifacts/{runId}/definitionBundle.json`.

## Gate

Show project outline: target, brief summary, domain id, target requirements (e.g. `productId`), template spine. User approves or `userFeedback` → re-run stage 1.
