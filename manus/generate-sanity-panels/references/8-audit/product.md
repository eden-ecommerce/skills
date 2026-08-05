# Audit — product

Content strip must not duplicate live PDP chrome (title, price, primary buy).

## Overlay checklist rows (add to shared)

| id | Check |
|---|---|
| `format_sibling_panel` | Format siblings (HB/ebook/audiobook same title) use text-led `publisherComparisonChart`, buttons, or FAQ — not `publisherComparison` with product picker or empty `images[]` |
| `format_sibling_cover_dupe` | No hardback+ebook catalogue covers side-by-side for same title |
| `format_sibling_image_required` | No comparison panel with image-required validation errors on format chooser |

## Required fields (fail `required_fields` if missing)

| Panel `_type` | Required |
|---|---|
| `imageWithOverlayAndTextV2` | `locale: { locale: "All" \| "GB", localeTitle: "…" }` when schema includes locale |
| `publisherImage300x300V2` | **Exactly 3** images in `images[]` |
| `publisherImage220x220V2` | **Exactly 4** images in `images[]` |
| `publisherComparison` | `images[]` populated when panel requires images; `cells[]` per row length = column count; no empty cells |

## Comparison / matrix (preview walk)

For each `publisherComparison` / `publisherComparisonChart`:

1. Read column headers left→right
2. Read each row cell under each header — copy must describe **that column's entity**
3. Fail `matrix_column_align` if entity A's text appears under entity B's header
4. Fail `matrix_no_empty_cells` if any cell is blank, `—`, or missing
5. Fail `ticks_cells_safe` if `ticks` + descriptive `cells` in same row shift columns (prefer prose-only rows OR ticks-only rows, not both)

## Commerce copy

**Fail `no_commerce_chrome_copy`:** prices (£…), stock counts, availability strings, dispatch promises in panel copy. Carousel `showPrice: false`.

## Visual flags (map to `domain_visual` / checklist)

| Flag | Example |
|---|---|
| `off_domain_imagery` | Non-domain religious book/symbol as prop |
| `invented_readable_title` | Generated image shows readable title that is not seed SKU |
| `catalogue_cover_pasted_as_hero` | Hero uses raw catalogue cover instead of generated art |
| `dimension_mismatch` | Asset aspect does not fit locked `targetPanelType` |
| `safe_zone_collision` | Headline illegible; carousel arrows overlap focal |

Overflow check on mobile width for wide panels.
