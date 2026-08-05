# Desired Content — shared

Stage 5. In: `target`, `brief`, `personas`, `findings`, `products`. Out: `desiredPageContent.json`

## Creative mandate

This stage is **unconstrained design** for **content hierarchy + persuasion** — not unimplemented web-app motion. You are a senior product / ecommerce design professional.

- **No Sanity panel `_type` limits** — those come later in Draft (hints via `targetPanelType` OK)
- **No obligation to mirror the live page, retailer strip conventions, or prior template spine** — invent the ideal page for the brief. Do not copy Amazon/A+/retailer layouts because the brief mentioned a retailer.
- **No artificial length, block-count, or layout-kind ceilings**
- Still ground **facts** in `findings` + `products` (quotes, bios, titles, URLs) — do not invent product facts or ratings
- **Never render live commerce chrome in copy** — no prices, stock counts, availability strings, or dispatch/fulfillment promises (they change; live page already shows them). Related-entity modules: title, maker, format/variant, cover, link only
- **Reader-facing copy** — name entities by human label (title, format, maker) + working URL/CTA. **Never** put raw internal IDs (`productId`, SKU codes) in body/FAQ/CTA text. IDs belong in artifact JSON / picker fields only.
- Respect `sourcePolicy` for attributed claims
- **Do not specify** `motionIntent`, parallax, sticky page chrome, accordion JS, or other interactions Sanity panels cannot ship — Draft maps to real panel `_type`s only

## Comparison / matrix modules (when used)

- Column **i** describes entity **i** — header and cells must align
- **No empty cells** — every row fills every column (no blank, no `—` filler)
- Same work in multiple variants (format, tier, duration): use discriminating headers (e.g. Hardback | Ebook), not duplicate titles only
- Prefer text-led chooser over cover-vs-cover for format siblings

## Design brief (always apply)

1. **One composition** — first viewport reads as one idea (brand/product voice + one promise + one path)
2. **Engagement** — scannable hierarchy, progressive disclosure, proof near claims, clear next actions
3. **SEO** — entity-clear H1/H2 story (who / what / for whom / why), FAQ-ready answers, internal links to maker/catalogue URLs
4. **Web guidelines** — accessible contrast intent, mobile-first stacking notes, readable line lengths, CTA affordances
5. **Emotion + trust** — match `domainSnapshot.tone` and personas; delight without hype
6. **Panel-aware imagery** — annotate `imageIntent.safeZones` for overlay text, carousel L/R arrows, captions below tiles (see domain visual rules)

## Role

Use `editorRole` from target constants as the writing voice — then design beyond it.

## Process

1. Re-imagine the ideal page from personas + findings + brief
2. Invent sections that maximise engagement **within what panels can render**
3. Write **near-final shippable copy** everywhere — full headlines, body paragraphs, CTA labels + real URLs
4. Annotate **`imageIntent`** per block (subject, placement, overlay, safe zones, optional `targetPanelType` hint) — Stage 6 locks type + dimensions
5. Weave catalogue entities into commerce modules (title / maker / format / link / cover) — never bake in price or stock text
6. Include SEO outline: primary entity phrase, supporting H2 intents, FAQ entities (one FAQ home in `blocks[]` only)
7. Produce a **page structure map** (`pageStructure`) so Gate 5 can present a wireframe-like mockup

## Out (flexible schema)

Prefer rich mockup JSON. Use **`blocks[]` as single source of truth** — do not duplicate FAQ or modules in parallel top-level arrays.

Minimum shape:

```json
{
  "pageTitle": "...",
  "seo": {
    "primaryEntity": "...",
    "metaTitle": "...",
    "metaDescription": "...",
    "h1": "...",
    "secondaryHeadings": ["..."]
  },
  "designConcept": "1–3 paragraphs: visual direction, engagement strategy, why this composition wins",
  "pageStructure": [
    {
      "order": 1,
      "blockId": "hero-...",
      "layoutKind": "imageWithTextOverlay | authorSpotlight | faq | carousel | comparison | ...",
      "purpose": "one job for this area",
      "image": { "role": "hero|author|publisher|catalogue|none", "srcIntent": "..." },
      "text": { "title": "...", "body": "full near-final copy...", "ctaLabel": "...", "ctaUrl": "https://..." }
    }
  ],
  "blocks": [
    {
      "id": "...",
      "layout": "descriptive layout name",
      "purpose": "engagement / SEO / conversion job",
      "personaFit": ["..."],
      "viewport": "above-fold | mid | late",
      "imageIntent": {
        "subject": "...",
        "placement": "full-bleed | beside-text | product-tile | text-led",
        "overlay": true,
        "targetPanelType": "optional hint — Stage 6 locks dimensions",
        "safeZones": "e.g. left 40% clear for headline; bottom 20% for carousel captions; L/R 10% for arrows",
        "notes": "..."
      },
      "headline": "...",
      "body": "...",
      "ctaLabel": "...",
      "ctaUrl": "..."
    }
  ],
  "narrativeNote": "top→bottom story and engagement beats"
}
```

**Forbidden fields:** `motionIntent`, sticky-commerce-as-page-chrome, parallax/JS interaction specs, top-level `faq[]` (use FAQ block in `blocks[]`), unmapped `modules[]`.

## Gate presentation (orchestrator MUST show)

Gate 5 is a **comprehensive content mockup**, not a thin block-id table. Present top→bottom like a wireframe:

```
[layoutKind]: Hero / purpose
  image: src intent (e.g. author portrait / cover-led split)
  title: «final headline»
  body: «final copy or first ~400 chars + …»
  CTA: «label» → https://...

[layoutKind]: Author Spotlight / purpose
  image: author
  title: …
  body: …
  CTA: link to maker page → https://...
```

For every block include: **layout kind**, **purpose**, **image role/src intent**, **final title**, **final body** (not outline stubs), **CTA label + URL** when present.

Reject if copy is outline-only, `designConcept` missing, raw internal IDs in reader copy, or gate cannot be rendered as the mockup above.
