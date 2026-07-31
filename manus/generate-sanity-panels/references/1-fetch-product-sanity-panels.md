---
name: fetch-product-sanity-panels
description: Fetch Eden CMS product panel schemas and map gallery titles to types. Use when need panel field shapes or visual-to-schema mapping.
---

# SCHEMA + GALLERY

## SCHEMA

```bash
curl -s https://cms.eden.co.uk/schema.json -o schema.json
python3 scripts/extract_panels.py schema.json
```

Output: full JSON schema per `product.panels` union member.

## GALLERY

Open `https://eden-xi.vercel.app/panels/product`.

Per panel on page:

1. Note rendered title/label
2. Check responsive layout (mobile + desktop)
3. Note variant options if shown
4. Map title → `_type` from schema extract
5. Read schema `description` + fields for intent

Build map: `{ title, _type, intent, requiredFields }`.

## TROUBLE

- No `product` doc in schema → `grep '"name": "product"' schema.json`
- No `panels` attr → grep product attributes for union field
- Gallery title ≠ schema name → match by visual + description, not string equality
