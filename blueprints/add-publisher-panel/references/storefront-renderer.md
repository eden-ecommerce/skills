# Storefront — publisher panel renderer

Primary: `apps/next-next-eden`. Mirror standalone `next-next-eden` when still deployed.

Load **next-next-eden-standards** via review-standards.

## 1. Sync generated types

After hub `panels-regen.sh`, match `apps/next-next-eden/generated/panels/` to hub:

- `panelsSchema.d.ts`
- `panelsZodSchema.ts`
- `panelsJsonSchemaToZod.ts`

## 2. types/panels.ts

File: `apps/next-next-eden/types/panels.ts`

1. Import Zod fragment from `@/generated/panels/panelsJsonSchemaToZod`
2. Add to `zodPanels` union

Drives `SupportedPanels` + `StandardProps` typing.

## 3. Publisher{Name}Renderer.tsx

Path: `components/renderer/edenProducts/Publisher{Name}Renderer.tsx`

Thin adapter — resolve assets, map to UI:

```typescript
import type { StandardProps } from "@/types/panels";
import { PublisherExample } from "@christian-360/next-design/storefront/publisher-example";

export const PublisherExampleRenderer = ({
  panel,
  extraData,
}: StandardProps) => {
  if (panel._type !== "publisherExample") {
    return null;
  }
  const asset = extraData.assets[panel.image.assetId];
  if (!asset?.url || !asset.width || !asset.height) {
    return null;
  }
  return (
    <PublisherExample
      heading={panel.heading}
      image={{
        src: asset.url,
        alt: panel.image.alt ?? "",
        width: asset.width,
        height: asset.height,
      }}
    />
  );
};
```

- Guard `panel._type` first
- Resolve `extraData.assets[assetId]` for V2 image panels
- `storefront/client/` import for interactive components
- Pass `shopNowLabel` / translations from `extraData` for comparison CTAs

### Copy from

- `PublisherImage970x300V2Renderer.tsx` — `PublisherImageGrid` facade
- `PublisherFaqRenderer.tsx` — client component
- `PublisherComparisonChartRenderer.tsx` — comparison + `shopNowLabel`

## 4. c360PanelComponents

File: `components/renderer/c360PanelComponents.tsx`

1. Import renderer
2. Add: `publisherExample: PublisherExampleRenderer`

## 5. PublisherRenderer (PDP)

File: `components/renderer/PublisherRenderer.tsx`

Spreads `c360PanelComponents` — **no change** unless noop type on product pages. New registry entries render PDP auto.

## 6. Validate

```bash
cd apps/next-next-eden && pnpm run ts-check && pnpm run lint
```

## 7. Manual test

Add panel via hub on org **panelProducts** collection. View product page using `PublisherRenderer`.
