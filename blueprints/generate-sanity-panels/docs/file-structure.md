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
    * `urls.md` — FIRST RUN credential names (env + CLI flags); no values
* templates/
    * `product.md`, `article.md`, `email.md` — brief-agnostic spines
* scripts
    * `cli_env.py` — shared CLI/env parsers (no hardcoded CMS ids)
    * `fetch_algolia.py` — product id or `--filter` / `--query`; Algolia creds via CLI/env
    * `fetch_schema.sh` — `<schemaUrl>` required → `.cache/`
    * `extract_panels.py` — allowlist JSON per doc + field
    * `get_sanity_document.py` — GROQ / product-id / slug
    * `upload_sanity_image.py` — local file → Sanity asset
    * `patch_sanity_draft.py` — draft mutate
    * `publish_sanity_document.py` — publish action
    * `.env.example` — names only; never fill in the skill tree
    * `.cache/` — gitignored schema + panel allowlists
    * `.artifacts/{runId}/` — gitignored stage JSON handoffs (canonical: `researchFindings.json`, `draftPatch.json`, `draftResult.json`; `findings-raw/` debug-only; no parallel `draft-panels.json` / `panelsUsed.json`; upload `.err` only on failure)
* references — load `shared.md` + selected `{target}.md` only; never sibling domains/targets
    * `1-definition/` — shared, product, article, email
    * `2-personas/` — shared, product, article, email
    * `3-research-strategy/` — shared, product, article, email
    * `4-research-findings/` — shared, algolia, product, article, email
    * `5-desired-content/` — shared, product, article, email
    * `6-media/` — shared, product, article, email
    * `7-draft/` — shared, http-sanity, product, article, email
    * `8-audit/` — shared, product, article, email
    * `9-publish/` — shared only
* docs/
    * `specification.md`
    * `activity-diagram.md`
    * `state-machine.md`
    * `file-structure.md`
* `SKILL.md` — orchestrator; progressive-disclosure load; `domainSnapshot` after Definition
