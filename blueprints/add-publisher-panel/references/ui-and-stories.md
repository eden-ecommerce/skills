# UI + Storybook — publisher panel

Apps: `packages/ui`, `apps/storybook`.

Load **christian-360-next-design-standards** via review-standards. Generic component/story detail → `implement/references/add-component.md`, `add-stories.md` — no duplicate here.

## 1. Component placement

| Interactive? | Path | Import |
|--------------|------|--------|
| No | `packages/ui/src/storefront/{kebab-case}/` | `@christian-360/next-design/storefront/{kebab-case}` |
| Yes | `packages/ui/src/storefront/client/{PascalCase}/` | `@christian-360/next-design/storefront/client/{PascalCase}` |

`'use client'` only in `storefront/client/`.

## 2. Reuse before create

| Component | When |
|-----------|------|
| `PublisherImageGrid` + variants | Banner, single+text, 3/4 image columns |
| `PublisherBrandLogo` | Company logo |
| `PublisherSingleImageWithSidebar` | Sidebar layout |
| `PublisherImageWithSpecs` / `PublisherSpecsTable` | Specs |
| `PublisherImageWithHighlights` | Highlights |
| `client/PublisherFaq` | FAQ accordion |
| `client/PublisherImageHotspots` | Hotspots |
| `client/PublisherComparison` | Comparison table |
| Carousel primitives | `carousel-reuse.md` |

Extend via props (`variant`, `layout`, `displayMode`, `navVariant`) — no fork for small layout diff.

## 3. Component reqs

- `className?: string` on root; merge `cn()`
- Typography: `text-heading-small`, `text-body-medium`, `text-body-small`, `text-caption` — no ad-hoc `text-lg font-semibold`
- Max width: module constant e.g. `PANEL_MAX_WIDTH_PX = 970` from design spec; `style={{ maxWidth }}` or Tailwind
- No API types in `packages/ui`; props only (string, number, boolean, ReactNode, callbacks)
- Images via `PublisherImage` / `Image` + alt

## 4. Storybook

Path: `apps/storybook/src/stories/Storefront/publisher-panels/`

- Title: `Storefront/Publisher Panels/{ComponentName}`
- Description cites `_type`
- **Default** — fixtures from `fixtures.ts` or `publisher-image-grid/fixtures.ts`
- **MinimalData** — required props only
- **play** for interactive panels (FAQ, hotspots, comparison, carousels)

Image-grid sub-stories: `publisher-panels/publisher-image-grid/`.

## 5. Validate

```bash
cd packages/ui && pnpm run lint
cd apps/storybook && pnpm run ts-check && pnpm run lint
```

From repo root (ui or storybook changes):

```bash
pnpm exec prettier --check .
# fix: pnpm format
```
