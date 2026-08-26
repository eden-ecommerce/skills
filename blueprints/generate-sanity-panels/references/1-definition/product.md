# Definition — product

Delta for `target=product`.

- **`productId` required** — Eden `product_id`. Block if missing; do not proceed as catalogue-led
- Write `productId` onto `definitionBundle`
- `panelField` = `panels[]` on `product` doc
- Algolia seed in stage 4 must force-include this SKU
- Content strip only — no duplicate live PDP chrome (title, price, buy box, **core specs table**)
- Template “maker” section = author **or** manufacturer/brand by product type (books ≠ candles ≠ instruments)
