---
name: preview-and-verify
description: Preview draft and verify vs persona-scored plan.
---

# PREVIEW + VERIFY

## URL

```
{NEXT_NEXT_EDEN_BASE_URL}/api/preview?type=<TYPE>&token=<SANITY_PREVIEW_TOKEN>&slug=<SLUG>
```

| type | slug |
|---|---|
| `product` | product_id |
| `home` | omit |
| `category` / `department` | browse slug |
| `article` | article slug |

Token from env. Never log or commit.

## CHECK (GATE 3)

1. `browser_navigate` to URL
2. Scroll full page
3. Compare vs approved panel map + persona scores
4. Re-score sections 0–5 vs personas
5. Mismatch → patch draft → re-preview

Pass when mean persona score ≥ user threshold or user says ship.

## TROUBLE

- Blank page → expired token
- Wrong page → check `type` + `slug`
- Missing panels → check draft doc field (`panels` vs `richText`)
