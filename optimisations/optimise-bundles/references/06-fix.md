# 06 — Fix patterns

Smallest cut that removes import edge. Remeasure after **each** change.

## A. Boundaries

### Split constants from heavy modules

```ts
// safe for client — no Zod, no generated
export const MY_CONST = "value";
```

Client never value-import modules that pull validation graphs or generated schemas.

### Conditional server import

```tsx
let section = null;
if (needFeature) {
  const { FeatureSection } = await import("@/components/FeatureSection");
  section = (
    <Suspense fallback={<Fragment />}>
      <FeatureSection {...props} />
    </Suspense>
  );
}
```

### Server / client pair

- Server shell: fetch, markdown pre-render, pass props/children
- Client shell: `"use client"`, interaction only

## B. Rendering

| Content | Where | Import |
|---------|-------|--------|
| Static markdown | RSC | DS server markdown (no `"use client"`) |
| Truncate / accordion | Client shell + server children | Pass pre-rendered `children` |
| Avoid | Server page static-import client markdown | Client markdown libs stay out of page graph |

## C. Tree shaking reality

**Works:** separate files, `server-only`, `import type`, narrow Zod on server, one lazy module for heavy dep.

**Weak for this metric:**

- `await import()` alone — targets still in route graph
- Flat `Record` of loaders — all targets may stay associated
- Parallel routes without remeasure — can grow route

Verify loader registries with chunk diff after every change.

## D. Site rules

PDP / org registry constraints: `references/next-next-eden.md`.
