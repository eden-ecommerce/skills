# Research Findings — Algolia subagent

Run when catalogue = Algolia.

## Commands

```bash
python3 scripts/fetch_algolia.py <product_id> --algolia-app-id "$ALGOLIA_APP_ID" --algolia-search-key "$ALGOLIA_SEARCH_KEY"
python3 scripts/fetch_algolia.py --filter 'author:"<NAME>" AND stores:eden' --query "" --algolia-app-id "$ALGOLIA_APP_ID" --algolia-search-key "$ALGOLIA_SEARCH_KEY"
python3 scripts/fetch_algolia.py --filter 'manuf:"<NAME>" AND stores:eden' --query "" --algolia-app-id "$ALGOLIA_APP_ID" --algolia-search-key "$ALGOLIA_SEARCH_KEY"
```

App id + search key from FIRST RUN. Never hardcode. Env-prefix form also works.

## Process

- Derive filter from seed hit — **maker role is product-type aware**:
  - books / Bibles / media with `author` → filter `author:"…"`
  - candles, instruments, gifts, other goods → filter `manuf:"…"` (manufacturer / brand)
  - if both present, prefer the role that drives related catalogue for this SKU; may run both and merge deduped
- Force-include named seed SKU at top of `products[]`
- Summarize hits to compact cards only — **include stock + fulfillment speed signals for Gate 4 / later selection** (e.g. prefer in-stock siblings when choosing related tiles)
- **Do not treat price/stock/fulfillment as on-page copy** — Stages 5–7 must not render those fields in panel text (they change; live PDP shows them)
- Cap 20 hits unless brief needs more

## Card schema (required keys)

```json
{
  "productId": "...",
  "title": "...",
  "maker": "...",
  "makerRole": "author|manufacturer|publisher|brand|unknown",
  "price": 0,
  "url": "...",
  "imageUrl": "...",
  "availability": "...",
  "stock": 0,
  "inStock": 0,
  "fulfillment": "..."
}
```

| Field | Source (typical Algolia) |
|---|---|
| `maker` | `author` if book-like; else `manuf` / brand |
| `makerRole` | which field was used |
| `availability` | `availabilityString` or `stockLevelText` |
| `stock` | `stock` (numeric on-hand when present) |
| `inStock` | `inStock` |
| `fulfillment` | short dispatch signal e.g. `availabilitydays` / bottom convincer / “Usually dispatched within N days” |

Never invent stock. If field missing, use `null` and say so in gate summary.

## Out

Write `products.json` — orchestrator merges into stage 4 artifact.
