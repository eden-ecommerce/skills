# Desired Content — product

**Creative freedom first** for copy, hierarchy, and image placement — not for unimplemented motion or page chrome Sanity cannot render.

## Still required (facts only)

- Product identity, maker, publisher/brand, quotes, ratings, URLs — only from `findings` / `products`
- Maker may be author or manufacturer by product type
- No invented endorsements or institutional claims
- **Do not put prices, stock, availability, or dispatch promises in any block body/CTA** — live PDP owns those; Algolia cards are selection/gate data only
- **Format siblings are not different products** — hardback / ebook / audiobook of the **same title** share near-identical covers. Do not design a cover-vs-cover comparison. Prefer text-led format chooser with discriminating labels: “Hardback (this page)” vs “Ebook edition” + links. Save cover comparison for **different works** only.
- **Human links in copy** — e.g. `[Ebook edition](https://www.eden.co.uk/.../my-story-9780281092024/)` or “the ebook edition (Christian360 download)”. Never `product 7355311` or bare SKU codes in reader text.

## Encouraged

- Hero compositions, narrative arcs, modular storytelling, comparison tools (**distinct titles**), social proof, gift/ministry pathways, bulk/institutional chapters, FAQ hubs (in `blocks[]`), related-product galleries (other titles — title/maker/format/link/cover — no price/stock)
- SEO entity clarity for title + maker + use cases
- **`imageIntent` with `safeZones`** on every image-led block
- **`pageStructure`** wireframe rows with full title/body/CTA URLs so Gate 5 reads like a content mockup

## Example Gate 5 rows (product)

```
imageWithTextOverlay: Hero
  image: cover-led split (SKU cover colours; left text-safe)
  title: The Greatest Story Ever Told — …
  body: «full hero copy»
  CTA: Explore the story → https://www.eden.co.uk/...

highlightBlock: Trust ribbon
  image: none
  title: Three reasons readers choose this title
  body: «full copy»

publisherComparisonChart: Format chooser (NOT publisherComparison)
  image: none
  title: Hardback or ebook — same life story
  body: columns: Hardback | Ebook — full prose per cell, no empty cells

productCarousel: Related titles
  image: catalogue via picker (no upload)
  title: More from this maker
```

## Do not specify

- `motionIntent`, parallax, sticky bars, accordion/tabs JS — Draft maps to Sanity panels only
- Sticky “Add to basket” as a page module (live PDP already has buy box)
- Retailer A+ strip layout because brief mentioned Amazon or similar

Draft (Stage 7) maps creative blocks onto real panel `_type`s — design for what panels can show.
