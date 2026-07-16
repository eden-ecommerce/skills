# next-next-eden constraints

Hard limit: this skill only for Eden ecommerce Next app (`apps/next-next-eden` / standalone mirror).

## Commands

```bash
cd apps/next-next-eden   # or standalone root
pnpm turbo-analyse-ci
pnpm next experimental-analyze --output
```

Threshold script: `scripts/analyse-route-bundles.js`. Never bump without user OK.

## Guard routes

Fix `/product/[id]` → `/home` + `/o/*` stay green. No publisher renderers on org. No new shared Zod client edges.

## PDP publisher rules

- Publisher renderers: `components/renderer/edenProducts/` via `publisherPanelLoaders/` — **PDP only**
- `C360PanelRenderer` / `c360PanelComponents.tsx` must **not** import publisher renderers
- Server validation: `utilities/c360/productPanels.ts` + `publisherZodPanels` (`server-only`)
- Parallel `@publisherPanels` **grew** PDP here — last resort

## Grep → source

| Hit | Source |
|-----|--------|
| `audioCarouselV2`, `fileDownloadCarousel`, `z.object`, `_type.*literal` | `types/panels.ts` → `zodPanels` → `generated/panels/panelsJsonSchemaToZod.ts` |
| `publisherBrandLogo`, `publisherFaq` + zod | `publisherZodPanels` or full union |
| `MarkdownText`, `markdown-to-jsx` | `components/MarkdownText.tsx` or DS markdown pulled client |
| `PublisherCarouselClient` | `components/renderer/edenProducts/PublisherCarouselClient.tsx` |
| `LazyReactPlayer`, `react-player` | `components/video/LazyReactPlayer.tsx` |

Org panel names in PDP-only chunk → leak from `utilities/c360/panels.ts` / `types/panels.ts`, not publisher registry.

## Known leak (fixed pattern)

```
ProductDetailPage (static import)
  ExitDraftModeButton
    ClientExitDraftModeButton ("use client")
      DRAFT_EXIT from utilities/c360/panels  (VALUE)
        zodPanels from types/panels
          panelsJsonSchemaToZod  (~124 kB client)
```

Fix shape: `utilities/c360/draftConstants.ts` — no Zod, no generated.

## Intentional PDP weight

```
ProductDetailPage
  await import PublisherSection (conditional)
    PublisherRenderer
      productPanels.ts (server-only)
      publisherPanelLoaders.ts → per-type files
```

Org routes must never import this chain.

## Registries

| Registry | Scope |
|----------|-------|
| `publisherPanelLoaders/` | PDP only |
| `c360PanelComponents.tsx` | Org hub — no publisher types |

## Rendering (this repo)

- RSC markdown: `@christian-360/next-design/storefront/markdown`
- Client markdown: `components/MarkdownText.tsx` → `markdown-to-jsx` (~90 kB class)
- Pattern: server markdown → `children` into thin client (`TruncatedContent`, accordion)
- Publisher body: `storefront/publisher-body-content` pre-render in server shell

## Case notes (Jul 2026 PDP)

| Change | Class | Outcome |
|--------|-------|---------|
| Publisher Zod split | route | Small alone — validation already server |
| Per-panel loaders | route | Small — graph keeps async targets |
| Parallel `@publisherPanels` | route | **Regression** |
| `DRAFT_EXIT` off `panels.ts` | route accidental | **−124 kB** |
| Server `ProductMarkdown` | route | Marginal; still correct |

Handoff doc if present: `docs/pdp-bundle-reduction-handoff.md`.
