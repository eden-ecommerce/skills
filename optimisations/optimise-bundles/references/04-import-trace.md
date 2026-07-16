# 04 — Import trace

Work back from heavy module (step 03).

## Value imports (not type-only)

```bash
rg 'from \"@/path/to/heavy\"' --glob '*.{ts,tsx}' | rg -v 'import type'
rg 'HeavyExport|heavyModule' --glob '*.{ts,tsx}' -l
```

## Client boundaries

```bash
rg -l '"use client"' --glob '*.tsx' | xargs rg -l 'HeavyExport|heavy/path'
```

## Static page imports

Top-level import always in graph. Conditional JSX no help.

```tsx
// BAD — always linked
import { OptionalFeature } from "@/components/...";

// BETTER — optional feature from Server Component
let feature = null;
if (needIt) {
  const { OptionalFeature } = await import("@/components/...");
  feature = <OptionalFeature />;
}
```

## Rules

- `"use client"` anywhere in chain → module + deps go client chunks
- Do not `next/dynamic()` a Server Component
- `import type` safe; value import of const from Zod file pulls Zod

Site leak examples: `references/next-next-eden.md`.
