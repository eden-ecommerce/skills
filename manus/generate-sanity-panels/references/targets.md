---
name: panel-targets
description: Hard-wired targets for generate-sanity-panels.
---

# TARGETS

Confirm target + identifier(s) + personas before research.

## GALLERY URLS

| Entity | Base | Path |
|---|---|---|
| article | `EDEN_BLOG_BASE_URL` | `/panels/article` |
| product | `NEXT_NEXT_EDEN_BASE_URL` | `/panels/product` |
| home | `NEXT_NEXT_EDEN_BASE_URL` | `/panels/home` |
| category | `NEXT_NEXT_EDEN_BASE_URL` | `/panels/category` |
| department | `NEXT_NEXT_EDEN_BASE_URL` | `/panels/department` |
| hub | `NEXT_NEXT_EDEN_BASE_URL` | `/panels/hub` |
| organisation | `NEXT_NEXT_EDEN_BASE_URL` | `/panels/organisation` |

Each page embeds `#panel-catalogue` JSON: `{ _type, title, intent, group, contextTags }`.

## PRODUCT

| | |
|---|---|
| `_type` | `product` |
| User gives | Eden `product_id` (Algolia) |
| Sanity query | `slug.current == "<product_id>"` |
| Panel field | `panels[]` |
| Allowlist | `webPageAllowedPanels` (= `allPanels`) |
| Preview | `type=product`, `slug=<product_id>` |

## HOME

| | |
|---|---|
| `_type` | `home` |
| User gives | Scheduled home doc context or merchandising brief |
| Sanity query | `*[_type == "home"][0]` or by `startDate` |
| Panel field | `panels[]` |
| Allowlist | `webPageAllowedPanels` |
| Preview | `type=home` (no slug) |

## CATEGORY / DEPARTMENT (browse)

| | |
|---|---|
| `_type` | `category` or `department` |
| User gives | Category/department slug or ID |
| Sanity query | `slug.current == "<slug>"` |
| Panel fields | `panels[]`, `bottomPanels[]` (richText only) |
| Allowlist | `webPageAllowedPanels` |
| Preview | `type=category` or `type=department`, `slug=<slug>` |

## ARTICLE

| | |
|---|---|
| `_type` | `article` |
| User gives | Slug, doc ID, or topic brief |
| Panel field | **`richText[]` embeds** — not top-level `panels` |
| Allowlist | `articleAllowedPanels` inside `richText` `of` |
| Gallery | eden-blog `/panels/article` |
| Preview | `type=article`, `slug=<slug>` |

## HUB PAGE CONTENT

| | |
|---|---|
| `_type` | `hubPageContent` |
| User gives | Hub slug |
| Panel fields | `topPanels[]`, `bottomPanels[]` |
| Allowlist | `webPageAllowedPanels` |
| Preview | Not in `/api/preview` map — verify manually or Studio |

## ORGANISATION PAGES

| | |
|---|---|
| `_type` | `organisationHome`, `organisationSearch`, `organisationEventSearch`, `organisationJobSearch` |
| User gives | Org slug or scope |
| Panel field | `panels[]` |
| Allowlist | `webPageAllowedPanels` |
| Preview | Per schema / Studio |

## ADS (appendix — not a page `panels` field)

Separate `ads` docs with `targetSelector` + panel refs (`adblock`, `adImage`, `adJob`). No `/panels` gallery route.

## PUBLISHER (flavour, not separate page target)

Publisher panels live on `product` docs (SPCK studio = `publisherPanelNames` only). Use product target + publisher gallery group.

## CONFIRM WITH USER

Before step 2, state back: target, identifier(s), personas, data sources, Sanity `_type`, gallery URL, open questions.
