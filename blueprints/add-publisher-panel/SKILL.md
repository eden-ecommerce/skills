---
name: add-publisher-panel
description: End-to-end publisher panel across API registry, hub Zod form, packages/ui, Storybook, next-next-eden renderer. Use when adding publisher panel, publisher* schema, panelProducts block, or carousel layout variant.
argument-hint: "<panel _type or layout name>"
---

/caveman ultra

New `publisher*` panel. Full stack: API → hub regen → UI → SB → nne renderer. `panelProducts` scope only.

Sibling **API** repo + monorepo (`apps/hub`, `packages/ui`, `apps/storybook`, `apps/next-next-eden`).

**Bind:** load **one** reference per step. Never load all refs at once.

## When

- New `publisher*` type (schema + hub form + UI + storefront renderer)
- New layout variant or carousel `navVariant`
- Carousel-like panel → `references/carousel-reuse.md` first

## Not

- Generic hub forms (`implement` + add-form)
- Org-page panels (`markdown`, `multiMediaCarousel`)
- Non-publisher product panels

## Workflow

1. **Clarify** (constitution): panel name, asset dims, static vs interactive. Read:
   - user / task design spec
   - `apps/next-next-eden/docs/panels/publisher/publisher-panels.md` (existing mappings)
2. **Reuse:** carousel/gallery → `references/carousel-reuse.md`; else grep `packages/ui/src/storefront` for `publisher*` (`PublisherImageGrid`, FAQ, hotspots, comparison)
3. **Wireframe + confirm:** load `references/wireframes.md` → fill ascii → post `_type`, UI reuse, layer checklist → **stop until user OK**
4. **Execute** (strict order, one ref per step):
   1. `references/api-schema.md` — API Zod + `panelsRegistry`
   2. `references/hub-form.md` — regen + hub form
   3. `references/ui-and-stories.md` — `packages/ui` + Storybook
   4. `references/storefront-renderer.md` — nne renderer
5. **Validate:** **review** (ts-check then lint per touched app) → **review-standards** (standards for changed dirs only)
6. **Docs:** update `publisher-panels.md` mapping table when panel ships

## Index

| Layer | Path | Reference |
|-------|------|-----------|
| All | tick list | `references/end-to-end-checklist.md` |
| Wireframe gate | pre-Execute | `references/wireframes.md` |
| API | sibling `christian-360/api` | `references/api-schema.md` |
| Hub | `apps/hub` | `references/hub-form.md` |
| UI + SB | `packages/ui`, `apps/storybook` | `references/ui-and-stories.md` |
| Storefront | `apps/next-next-eden` | `references/storefront-renderer.md` |
| Carousel reuse | before Execute if applicable | `references/carousel-reuse.md` |

Mirror standalone `christian-360/hub` + `next-next-eden` only when those trees in workspace and still deployed.

## Related

- **implement** — `add-component.md`, `add-stories.md` for generic UI/story detail
- **review** / **review-standards** — post-impl validation
- **constitution.mdc** — clarify → wireframe+confirm → implement → validate
