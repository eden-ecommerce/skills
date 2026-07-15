# Checklist — publisher panel end-to-end

Use with `add-publisher-panel` SKILL.md. Tick layers in order.

## Data flow

Stack diagram → `references/wireframes.md` §1.

## Phase 0 — Design

- [ ] Design spec clear (fields, dims, static vs interactive)
- [ ] `_type` chosen (`publisherCamelCase`)
- [ ] Asset dimensions documented
- [ ] Reuse decision (existing component vs carousel vs new UI)
- [ ] ASCII wireframes + confirm block posted (`references/wireframes.md`) — user OK

## Phase 1 — API (`christian-360/api`)

- [ ] Schema: `src/data/seeds/panel-schemas/product-schemas/publisher{Name}.ts`
- [ ] Shared schemas from `shared-schemas/` where possible
- [ ] Registered `config/panelsRegistry.ts` (import, enum, array)
- [ ] Asset IDs in `getPanelLocationVersionV1.ts` if images
- [ ] `docker exec christian-360-api pnpm ts-check` pass
- [ ] `docker exec christian-360-api pnpm lint` pass

## Phase 2 — Hub (`apps/hub`)

- [ ] `./panels-regen.sh` (API up) → `generated/panels/*`
- [ ] `PanelTypesConfig.tsx`: `SupportedPanelTypes` + `blockOptions` (`panelProducts` path)
- [ ] `ZodPanelFormsConfig.ts`: in `zodFormSupportedPanelTypes`
- [ ] `Publisher{Name}Form.tsx` created
- [ ] `ZodPanelFormSingle.tsx`: branch wired
- [ ] `docker exec eden-hub pnpm ts-check` pass
- [ ] ESLint clean on touched form files

## Phase 3 — UI (`packages/ui` + `apps/storybook`)

- [ ] Component in `storefront/` (server) or `storefront/client/` (interactive)
- [ ] `className` + `cn()` on root; typography tokens; max width constants from spec
- [ ] Story: `apps/storybook/src/stories/Storefront/publisher-panels/`
- [ ] Default + MinimalData variants; `play` for interactive panels
- [ ] `cd packages/ui && pnpm run lint` pass
- [ ] `cd apps/storybook && pnpm run ts-check && pnpm run lint` pass

## Phase 4 — Storefront (`apps/next-next-eden`)

- [ ] `generated/panels/*` synced from hub regen
- [ ] `types/panels.ts`: in `zodPanels` union
- [ ] `components/renderer/edenProducts/Publisher{Name}Renderer.tsx`
- [ ] `c360PanelComponents.tsx`: registry entry
- [ ] `cd apps/next-next-eden && pnpm run ts-check && pnpm run lint` pass

## Phase 5 — Docs + review

- [ ] `apps/next-next-eden/docs/panels/publisher/publisher-panels.md` updated
- [ ] **review** complete (all touched apps)
- [ ] **review-standards** complete (per-directory standards)

## Dual-repo mirror (when applicable)

- [ ] Standalone `christian-360/hub` mirrored
- [ ] Standalone `next-next-eden` mirrored
