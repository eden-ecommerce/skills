# Audit — product

Strip must not duplicate live buy-box chrome (title, price, primary buy).

## Overlay checklist rows

| id | Check |
|---|---|
| `format_sibling_panel` | Variant siblings use text-led `publisherComparisonChart`, buttons, or FAQ — not picker `publisherComparison` for same-title formats |
| `format_sibling_cover_dupe` | No variant catalogue covers side-by-side for same title |
| `carousel_no_seed` | Carousel omits seed `productId` and variant siblings; `showPrice: false`; sponsored pickers also omit seed |
| `format_coverage` | If buy box / findings list >2 formats or editions, format chart **or** FAQ names all of them (print / ebook / audio / seasonal edition as applicable) |
| `chrome_overlap_map` | Strip jobs do not duplicate live buy-box title, price, FBT, For you, or reviews aggregate as the primary beat |
| `panels_visible_on_preview` | Preview for seed `productId` shows the patched A+ panels — empty strip = fail. Doc `title` must be `{ISBN} - {name}` for Eden catalogue resolution |
| `seed_column_no_shop_now` | Seed column on `publisherComparison` has no Shop Now / seed PDP `edenLink` |
| `isbn_title_link` | Draft (and published if needed) `title` matches `{manuf_ref} - {product_name}` from Algolia |
| `comparison_row_trio` | Works comparison has `What it is` + `Best for` + `Skip if` rows (format charts may use `Choose when` / `Skip if`) |
| `skip_if_no_dead_end` | Product overlay: every Skip-if elimination has an in-table alternative column with outbound link (except seed display column) |
| `cre_outcome_headlines` | Product strip: hero + pathway H2s pass outcome test per `cre-conversion.md` |
| `cre_what_next_closing` | Closing band offers safe-step outbound path; live buy box owns purchase |
| `customer_facing_copy` | Product overlay: no Eden categorises/merchandises/Helpdesk placeholder copy |
| `no_jobs_widget` | Product strip has no jobs panel `_type` |
| `no_store_policy_faq` | FAQ covers product-fit only — not store returns/dispatch policy |
| `module_budget` | 6–9 content blocks unless `narrativeNote` exception |
| `hero_product_clarity` | Hero title/subtitle name product type + benefit |
| `section_subtitle_present` | Every A+ block shows title + subtitle on preview |
| `palette_consistency` | Eden locked palette on bands and accents |

## Required fields (`required_fields`)

| Panel `_type` | Required |
|---|---|
| `imageWithOverlayAndTextV2` | `locale` when schema includes it |
| `publisherImage300x300V2` | **3** images |
| `publisherImage220x220V2` | **4** images |
| `publisherComparison` | `cells[]` length = column count; no empty cells; includes **Skip if** row |

## Matrix preview walk

For each comparison/matrix panel:

1. Column headers left→right; cell copy under correct header
2. Fail shared matrix + `ticks_cells_safe` + `no_self_surface_links` on seed column links
3. **Skip if walk:** for each product column, read Skip-if cell → confirm it describes a use-case → confirm another column’s Best for is the natural landing → confirm that column has an outbound link (non-seed)
4. Fail `skip_if_points_to_alternative` / `skip_if_no_dead_end` if elimination leaves the shopper with nowhere to go in-table
5. Fail `skip_if_use_case_not_flaw` on harsh or defect-framed copy
6. Fail `skip_if_scannable` if any Skip-if cell is longer than ~8 words

## Commerce copy

Fail `no_commerce_chrome_copy` for prices, stock, dispatch in strip copy.

## Visual flags (`domain_visual`)

Off-domain imagery, catalogue cover as hero, dimension mismatch, safe-zone collision. Mobile overflow on wide panels.
