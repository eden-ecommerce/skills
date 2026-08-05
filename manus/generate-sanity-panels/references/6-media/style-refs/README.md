# Eden hero style reference

`eden-hero-split-safezone.png` — Children’s Bibles marketing hero (Eden retail).

## Use as **composition reference** for generated heroes

Stage 6 must **generate a new banner image** informed by this ref — do **not** upload the catalogue cover JPEG/WebP as the final hero asset.

| Element | What to copy in **generated** art |
|---|---|
| **Left safe zone** | ~40% clear white/light grey for overlay headline, subhead, CTA |
| **Right visual** | Engaging lifestyle or product-cluster zone — colours/mood echo seed cover **reference** |
| **Brand wash** | Optional colour overlay on lifestyle (adapt to category palette) |
| **White space** | Generous padding; responsive crop; no detail under future overlay text |
| **Dimensions** | Target **970×300** banner (`imageWithOverlayAndTextV2`) — see `panel-dimensions.md` |

## Reference images to pass when generating

1. This file (`eden-hero-split-safezone.png`) — layout/composition
2. Seed SKU `products[].imageUrl` — **colour, illustration style, product identity** — not final pixels

## Do not copy blindly

- Category-specific blue wash — adapt palette per SKU
- Children's Bibles products — use **this run's** cover as reference only
- Readable titles on props — only echo **this SKU** if a book must appear; never other-faith texts

## When to load

Stage 6 when `domainSnapshot.id === "eden"` and `target === "product"`.
