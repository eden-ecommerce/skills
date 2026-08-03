---
name: sanity-document
description: Fetch, create, patch draft Sanity documents.
---

# SANITY DOCUMENT

Project `bct7esy7`. Dataset `eden`.

## FETCH

```bash
manus-mcp-cli tool call query_documents --server sanity --input '{
  "query": "*[_type == \"<TYPE>\" && <FIELD> == \"<ID>\"][0]",
  "resource": { "projectId": "bct7esy7", "dataset": "eden" }
}'
```

### Query fields

| Target | Field |
|---|---|
| product | `slug.current == "<product_id>"` |
| category / department | `slug.current == "<slug>"` |
| article | `slug.current == "<slug>"` |
| home | `*[_type == "home"]` ordered by `startDate` |
| hubPageContent | `slug.current == "<slug>"` |

**Not** `product_id` — Algolia uses `product_id`; Sanity product slug = Eden product ID.

Grab `_id`, `slug`, existing panels / `richText`, other fields.

## ARTICLE PATCH

Panels are blocks inside `richText[]`:

```json
{ "_type": "carouselV2", "_key": "unique-key", … }
```

Do not create a top-level `panels` field on article docs.

## MISSING DOC

1. Tell user. Ask confirm create.
2. Query sample docs: `*[_type == "<TYPE>"]{...}[0..2]`
3. Mirror field shapes. Product new draft: `slug.current` = product ID.

## PATCH DRAFT

Target `drafts.<id>`. Unique `_key` per panel item. Sanity asset refs for images.

Never patch published doc directly.

## PUBLISH

User permission only.

## TROUBLE

- Empty result → wrong field or doc missing
- Preview 404 → check `slug` matches preview URL
- Article panels missing → check `richText` embeds, not `panels`
