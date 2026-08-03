---
name: gather-data
description: Seed data per target before open research.
---

# GATHER DATA

Env: `ALGOLIA_APP_ID`, `ALGOLIA_SEARCH_KEY`

## PRODUCTS INDEX

Index: `products`. Filter: `stores:eden`.

### Product

```bash
python3 scripts/fetch_algolia.py <PRODUCT_ID>
```

Filter: `product_id:<ID> AND stores:eden`. Related: same index by author, series, category.

### Browse

Query `products` with category/department filters. Capture representative hits for carousel/grid panels.

## ORGANISATIONHUB INDEX

Index: `organisationHub`. Org pages, jobs, events for org/search targets.

## OTHER

| Target | Sources |
|---|---|
| Article | Existing Sanity doc, public research on topic |
| Home | Merchandising brief, trending products from Algolia |
| Hub | Org hub index + user scope |

## OUTPUT

Seed context object — IDs, titles, images, relationships, **gaps to fill in research**.

## TROUBLE

- Empty Algolia → wrong ID or filter
- Auth error → check env keys
- API down → note gap, continue with Algolia + public research
