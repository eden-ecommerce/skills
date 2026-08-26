# Eden

| Field | Value |
|---|---|
| id | `eden` |
| website | `eden.co.uk` |
| delivery | UK Christian ecommerce + blog |
| locale | UK English |
| surfaces | `web-page`, `email` |
| requiresTenantBrief | false |

## Tone

Trust over hype. Faith content for seekers + church buyers. UK English.

## Catalogue

| Target | Source |
|---|---|
| product | Algolia `products` index, filter `stores:eden` |
| article | Sanity + public web research |
| email | Algolia when commerce slice needed |

## CMS

| Field | Value |
|---|---|
| provider | Sanity |
| projectId | user supplies at FIRST RUN (`NEXT_PUBLIC_SANITY_PROJECT_ID`) |
| dataset | user supplies at FIRST RUN (`NEXT_PUBLIC_SANITY_DATASET`) |
| schemaUrl | user supplies at FIRST RUN (public schema JSON URL) |

Resolve `projectId` / `dataset` / `schemaUrl` from FIRST RUN into `domainSnapshot.cms`. Never hardcode.

## URLs (hosts from FIRST RUN — `constants/urls.md`)

| Key | Pattern |
|---|---|
| gallery.product | `{NEXT_NEXT_EDEN_BASE_URL}/panels/product` |
| gallery.article | `{EDEN_BLOG_BASE_URL}/panels/article` |
| preview | `{NEXT_NEXT_EDEN_BASE_URL}/api/preview?type={type}&token={SANITY_PREVIEW_TOKEN}&slug={slug}` |
| live.product | `{NEXT_NEXT_EDEN_BASE_URL}/product/{productId}` |
| live.article | `{EDEN_BLOG_BASE_URL}/blog/p1{articleId}` |

Never preview on `www.eden.co.uk`.

## Visual (imagery + palette)

Eden is a **UK Christian retailer**. All generated or sourced imagery must be Christian-retail appropriate.

| Rule | Detail |
|---|---|
| Faith context | Imagery supports Christian books, Bibles, gifts, church/ministry buyers — not generic spirituality |
| **Prohibited props** | Other-religion books, symbols, or readable titles as decorative objects (e.g. Buddhist/Hindu/Islamic texts, non-Christian sacred imagery) |
| Product-link | Generated heroes echo seed cover **via reference** (colours/mood) — carousel/comparison use catalogue files as final pixels |
| Scene with books | Use **this SKU’s cover only**, or blank/obscured spines — no foreign readable titles |
| Hero style | Split composition: **text-safe white space** (left ~40%), product cover(s) as focal, lifestyle secondary with brand wash — see `references/6-media/style-refs/` |
| Palette | **Locked strip tokens** (one palette per run — no drift between panels): |
| | **Ground:** `#FFFFFF` / mist grey `#F5F5F2` |
| | **Primary accent:** Eden green `#2F6B4F` (dark bands, trust ribbons) |
| | **Secondary accent:** Eden blue `#2B5F8A` (sparingly — links, secondary bands) |
| | **Highlight:** yellow `#F5C518` (sparse CTA accent only — not dominant) |
| | **Text on dark:** `#FFFFFF` or cream `#FFFBF4` |
| | Avoid random “AI lifestyle” palettes (cream/terracotta cliché) unless brief overrides |
| Panel chrome | Reserve safe zones for carousel L/R arrows, captions below tiles, overlay headline areas |

## Constraints

- Draft only until publish gate
- Generated/custom panel art = Sanity assets in final draft; catalogue covers = picker IDs (storefront resolves)
- Product body **field** = `markdown` not `content` — on panels that have text fields; not the `markdown` panel `_type`
- Product panels = content strip only; no duplicate Eden chrome (title, price, buy box, core specs)
