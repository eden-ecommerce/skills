---
name: fetch-product-data-from-algolia
description: Fetch live Eden product from Algolia by product ID. Use when need price, stock, categories, author, images.
---

# ALGOLIA PRODUCT

## ENV

`ALGOLIA_APP_ID`, `ALGOLIA_SEARCH_KEY`

## RUN

```bash
python3 scripts/fetch_algolia.py <PRODUCT_ID>
```

Index `products`. Filter `product_id:<ID> AND stores:eden`.

## OUTPUT

JSON hit: title, price, author, ISBN, categories, series, related products, images, stock.

## TROUBLE

- Empty → wrong ID or not in Eden store
- Auth error → check env keys
