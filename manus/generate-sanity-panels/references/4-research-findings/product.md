# Research Findings — product

Algolia subagent: default on for Eden product target.

## Filters

- Seed: `product_id:{id} AND stores:eden`
- Related by creator: `author:"…"` **or** `manuf:"…"` per product type (see `algolia.md`)
- Force-include named SKU from brief at top of `products[]`

## Content strip vs live PDP chrome

Live Eden PDP already shows title, price, buy box, and core specs (format, ISBN, dimensions, etc.).

Stage 4 must **not** treat chrome-duplicating specs as research goals.

| Research | Do | Don't |
|---|---|---|
| Maker spotlight | Deep bio / brand story / faith link / why this maker for **this** SKU | Generic CV laundry list with no product tie-in |
| Themes / topics | What the product is **about**; concrete use cases | Restate subtitle only |
| FAQ / reviews | Mine customer Qs and review themes from trusted sources; `faqCandidates` with `source` | Invent ratings; bare product IDs in synthesized copy |
| Specs | Only deltas useful for comparison, institutional fit, or FAQ — flag `aPlusRelevance` | Dump full PDP spec table into findings |
| Institutional | Infer from audience signals + credited sources | Invent endorsements |
| Catalogue | Related SKUs (title, maker, format, URL, cover) — prefer **different works**; note format siblings (`all_formats`) for text-led choosers | Quoting live **price/stock/dispatch** as panel copy; HB+ebook as cover-comparison pair |

## Maker generality

Eden sells books, Bibles, candles, instruments, gifts, etc.

- Books/Bibles/media → author (and publisher as separate imprint topic when useful)
- Physical goods → manufacturer / brand
- Always name the role in findings (`author` vs `manufacturer`)
