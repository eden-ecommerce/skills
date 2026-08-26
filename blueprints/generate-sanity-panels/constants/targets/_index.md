# Target picker

| id | surface | seed identifier | panel field | path |
|---|---|---|---|---|
| `product` | Product content strip (below live buy-box chrome) | Eden `product_id` — **required** | `panels[]` | `constants/targets/product.md` |
| `article` | Long-form article page | slug or doc id from brief | `richText[]` embeds (field, not panel type) | `constants/targets/article.md` |
| `email` | Email body / campaign slices | campaign name or template slug | slice array per tenant | `constants/targets/email.md` |

**Future:** `browse` (category/listing pages) — not in v1.

Load **one** row only. After pick, read that target file for identifier + spine pointer. Workflow rules live in stage `shared.md` refs — not here.
