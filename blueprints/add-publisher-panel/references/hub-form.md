# Hub — publisher panel form

Primary: `apps/hub`. Mirror standalone `christian-360/hub` when tree still used.

## 1. Regen panel types

API running with new schema registered.

```bash
cd apps/hub
./panels-regen.sh
```

Writes `generated/panels/`:

- `panelsSchema.d.ts` — TS interfaces + `CollectionPanels` union
- `panelsZodSchema.ts` — Zod for Formik
- `panelsJsonSchemaToZod.ts` — per-panel Zod fragments

Needs `c360-api` at `http://c360-api:3000/v1/panel/schemas`.

Copy/sync `generated/panels/*` → `apps/next-next-eden/generated/panels/` after regen.

## 2. PanelTypesConfig

File: `components/blocks/CollectionVersion/PanelTypesConfig.tsx`

1. `SupportedPanelTypes`:
   ```typescript
   "publisherExample" satisfies CollectionPanelType,
   ```
2. `blockOptions` entry:
   - `type`: panel `_type`
   - `label`, `description`, `icon` (Lucide)
   - `ownerTypes: [""]`
   - `paths: ["/dashboard/organizations/${ownerId}/panelProducts"]`

## 3. ZodPanelFormsConfig

File: `components/blocks/CollectionVersion/zodPanelForms/ZodPanelFormsConfig.ts`

Add panel name to `zodFormSupportedPanelTypes`.

## 4. Publisher{Name}Form.tsx

Path: `components/blocks/CollectionVersion/zodPanelForms/Publisher{Name}Form.tsx`

### Pattern

```typescript
"use client";

import { useFormik } from "formik";
import { toFormikValidationSchema } from "zod-formik-adapter";
import { publisherExampleSchema } from "@/generated/panels/panelsZodSchema";
import { useZodPanelFormValidation } from "./useZodPanelFormValidation";
import { OwnerAssetImageField } from "../OwnerAssetImageField";
import { useCollectionVersionContext } from "../CollectionVersionContext";
import { usePopStateStopBack } from "@/hooks/usePopStateStopBack";
```

- Formik initial values match schema
- `validationSchema: toFormikValidationSchema(publisherExampleSchema)`
- `useZodPanelFormValidation(formik)` → `handleSubmit`, `showFieldError`, `hasVisibleFieldError`
- `form onSubmit={handleSubmit}` (not raw `formik.handleSubmit`)
- `OwnerAssetImageField` for images — supports `error` prop
- `<Input>` no `error` prop — sibling `<p className="text-sm text-destructive">`
- `usePopStateStopBack(!isSubmitDisabled)` when dirty
- Submit disabled: `!formik.isValid || !formik.dirty`

### Copy from

- Simple: `PublisherBrandLogoForm.tsx`, `PublisherFaqForm.tsx`
- Multi-image: `PublisherImage300x300V2Form.tsx`
- Hotspots: `PublisherImageHotspotsForm.tsx` + `HotspotPlacementEditor.tsx`
- Spec rows: `PublisherSpecRowsField.tsx` + `getFieldError`

## 5. ZodPanelFormSingle

File: `components/blocks/CollectionVersion/zodPanelForms/ZodPanelFormSingle.tsx`

```typescript
if (panelType === "publisherExample") {
  const result = publisherExampleSchema.safeParse(initialData);
  if (!result.success && props.panelId) {
    return <ErrorCard error={new Error("Sorry your block is broken")} />;
  }
  return (
    <PublisherExampleForm
      initialData={result.data}
      onSubmit={props.onSubmit}
      onCancel={props.onCancel}
      isLoading={false}
      panelId={props.panelId}
    />
  );
}
```

`PanelDialog.tsx` routes when type in `zodFormSupportedPanelTypes`.

## 6. Validate

```bash
docker exec eden-hub pnpm ts-check
docker exec eden-hub pnpm eslint components/blocks/CollectionVersion/zodPanelForms/Publisher*Form.tsx components/blocks/CollectionVersion/zodPanelForms/useZodPanelFormValidation.ts
```

Load **hub-standards** via review-standards on hub file changes.
