# API — publisher panel schema

Repo: `christian-360/api` (sibling to monorepo).

## 1. Schema file

Path: `src/data/seeds/panel-schemas/product-schemas/publisher{Name}.ts`

Pattern (follow `publisherFaq.ts`):

```typescript
import type { BasePanel } from "../config/panel.types";
import { imageWithAltV2Schema } from "../shared-schemas/imageWithAlt";
import { z } from "zod";

export const publisherExampleSchema = z.object({
  _type: z.literal("publisherExample"),
  heading: z.string().min(1),
  image: imageWithAltV2Schema,
});

export type PublisherExamplePanelData = z.infer<typeof publisherExampleSchema>;

export const publisherExample = {
  type: "base",
  name: "publisherExample",
  zodSchema: publisherExampleSchema,
  deprecated: false,
} satisfies BasePanel<"publisherExample">;
```

## 2. Shared schemas

| Location | Use for |
|----------|---------|
| `shared-schemas/imageWithAlt.ts` / `imageWithAltV2.ts` | Image + alt (+ assetId V2) |
| `shared-schemas/publisherSpecRow.ts` | Spec label/value rows |
| `shared-schemas/publisherHotspot.ts` | Hotspot x/y/heading/body |
| `shared-schemas/publisherFaqItem.ts` | FAQ question/answer |
| `shared-schemas/publisherHighlight.ts` | Highlight title/body |
| `shared-schemas/publisherSidebarContent.ts` | Sidebar block |
| `shared-schemas/publisherComparison.ts` | Comparison columns/rows |
| `shared-schemas/link.ts` | Product links in comparison |

Extract `PUBLISHER_MIN_*` / `PUBLISHER_MAX_*` at module level when design spec caps min/max.

## 3. panelsRegistry

File: `src/data/seeds/panel-schemas/config/panelsRegistry.ts`

1. Import: `import { publisherExample } from "../product-schemas/publisherExample";`
2. Add `"publisherExample"` to `_registeredPanelsEnum`
3. Add `publisherExample` to `panelsRegistry` array

TypeScript enforces completeness via `RegistryCompleteness`.

## 4. Asset collection (images)

File: `src/routeHandlers/panels/collection-version/getPanelLocationVersionV1.ts`

Add `case "publisherExample":` — collect `assetId` into `assetIds` (see `publisherFaq`, `publisherImageHotspots`, `publisherComparisonChart`).

## 5. V1 → V2 migrations (optional)

Superseding V1 panel → add `migrations` on panel object (see `publisherImage970X300.ts`). Keep V1 in registry for legacy data.

## 6. Expose schemas

`GET /v1/panel/schemas` via `getPanelSchemasV1.ts` (reads `panelsRegistry` → JSON Schema). No extra wiring after registry update.

## 7. Validate

```bash
docker exec christian-360-api pnpm ts-check
docker exec christian-360-api pnpm lint
```

Container must run. Down → tell user start `christian-360-api` first.
