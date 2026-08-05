* constants
    * domains/
        * `_index.md` — id | delivery | path (picker only)
        * `eden.md` — profile, URLs, surfaces, tone, catalogue, CMS
        * `christian360.md`
        * `publish360.md` — `requiresTenantBrief: true`
        * `_custom.template.md`
    * targets/
        * `_index.md` — id | surfaces | default template | path (picker only)
        * `product.md`
        * `article.md`
        * `email.md`
    * `urls.md` — shared env var names only
* templates/
    * `product.md`, `article.md`, `email.md` — brief-agnostic spines
* scripts
    * `fetch_algolia.py` — product id or `--filter` / `--query`
    * `fetch_schema.sh` — curl schema → `.cache/`
    * `extract_panels.py` — allowlist JSON per doc + field
    * `.env.example`
    * `.cache/` — gitignored schema + panel allowlists
    * `.artifacts/{runId}/` — gitignored stage JSON handoffs (canonical: `researchFindings.json`, `draftPatch.json`, `draftResult.json`; `findings-raw/` debug-only; no parallel `draft-panels.json` / `panelsUsed.json`; upload `.err` only on failure)
* references — load `shared.md` + selected `{target}.md` only; never sibling domains/targets
    * `1-definition/` — shared, product, article, email
    * `2-personas/` — shared, product, article, email
    * `3-research-strategy/` — shared, product, article, email
    * `4-research-findings/` — shared, algolia, product, article, email
    * `5-desired-content/` — shared, product, article, email
    * `6-media/` — shared, product, article, email
    * `7-draft/` — shared, mcp-sanity, product, article, email
    * `8-audit/` — shared, product, article, email
    * `9-publish/` — shared only
* docs/
    * `specification.md`
    * `activity-diagram.md`
    * `state-machine.md`
    * `file-structure.md`
* `SKILL.md` — orchestrator; progressive-disclosure load; `domainSnapshot` after Definition
