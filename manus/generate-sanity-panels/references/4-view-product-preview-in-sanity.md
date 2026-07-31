---
name: view-product-preview-in-sanity
description: Preview Eden product draft on vercel and verify vs page plan. Use after draft patch, before publish.
---

# PREVIEW VERIFY

## URL

```
https://eden-xi.vercel.app/api/preview?type=product&token=<TOKEN>&slug=<PRODUCT_ID>
```

Token from user. Never log or commit.

## CHECK

1. `browser_navigate` to URL
2. Scroll full page
3. Compare vs page plan from step 3:
   - Panel order and types
   - Content accuracy
   - Images render
   - Responsive layout
4. Name/price match Algolia

Mismatch → patch draft → re-preview.

## TROUBLE

- Blank page → expired token
- Wrong product → check slug/ID
- Missing panels → check draft doc `panels` array
