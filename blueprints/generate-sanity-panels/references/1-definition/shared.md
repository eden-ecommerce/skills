# Definition — shared

Stage 1 subagent. Output: `definitionBundle.json`

Orchestrator must already have clarified the project outline: **target**, **brief**, **domain**, **run credentials**, plus any target-specific requirements (see `constants/targets/{T}.md`).

## In

- Confirmed `target`, `brief`, `domain`
- Target requirements (e.g. `productId` when `target=product`)
- Run credentials from `constants/urls.md` (user-supplied at FIRST RUN)
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
7. Resolve CMS + host **placeholders from FIRST RUN user values** — `cms.projectId`, `cms.dataset`, `cms.schemaUrl`, gallery/preview/live hosts. Block if any required credential for this target is missing. **Never hardcode** project id, dataset, hosts, or tokens. **Never write tokens** into `definitionBundle` / `domainSnapshot`.
8. Do not invent catalogue items or panel `_type`s

## Out (`definitionBundle`)

```json
{
  "target": "article",
  "brief": "...",
  "domain": "eden",
  "productId": null,
  "template": ["Hero", "...", "CTA"],
  "domainSnapshot": { "id", "cms", "urls", "catalogue", "constraints", "credentialsReady": true },
  "tenantBrief": null
}
```

`productId` required string when `target=product`; otherwise `null`.

`domainSnapshot.cms` holds user-supplied `projectId`, `dataset`, `schemaUrl` only. `domainSnapshot.urls` holds substituted gallery/preview/live patterns (preview token stays a `{SANITY_PREVIEW_TOKEN}` placeholder until Stage 7 builds `previewUrl` in session).

`credentialsReady: true` means the orchestrator has the secrets in session for CLI pass-through — not that they are stored on disk.

Write to `scripts/.artifacts/{runId}/definitionBundle.json`.

## Gate

Show project outline: target, brief summary, domain id, target requirements (e.g. `productId`), cms projectId + dataset (not tokens), hosts, template spine. User approves or `userFeedback` → re-run stage 1.
