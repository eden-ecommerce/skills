---
name: fetch-product-document-from-sanity
description: Fetch, patch draft, publish Eden Sanity product docs. Use when need current panels or deploy panel changes.
---

# SANITY PRODUCT

Project `bct7esy7`. Dataset `eden`.

## FETCH

```bash
manus-mcp-cli tool call query_documents --server sanity --input '{
  "query": "*[_type == \"product\" && product_id == \"<PRODUCT_ID>\"][0]",
  "resource": {
    "projectId": "bct7esy7",
    "dataset": "eden"
  }
}'
```

Grab `_id`, existing `panels`.

## PATCH DRAFT

Target `drafts.<id>`. Set `panels` array. Unique `_key` per item. Sanity asset refs for images.

```bash
manus-mcp-cli tool call patch_documents --server sanity --input '{...}'
```

Never patch published doc directly. Draft only until user approves.

## PUBLISH

User permission required.

```bash
manus-mcp-cli tool call publish_documents --server sanity --input '{...}'
```

## TROUBLE

- Empty result → product_id string vs number mismatch in CMS
- Patch fails → check draft `_id` prefix, required panel fields, asset ref shape
