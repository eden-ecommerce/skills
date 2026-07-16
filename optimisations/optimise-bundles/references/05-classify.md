# 05 — Classify

Pick one before fix.

| Class | Signal | Fix |
|-------|--------|-----|
| **Route-specific** | Only target fails; big target-only chunks | Page imports, feature registry, route-only client |
| **Shared layout** | Many unrelated routes fail alike | `app/layout.tsx`, providers, global client wrappers |
| **Dependency bump** | Most routes up ~same %; new package paths in analyse | Review dep / DS package; may need threshold approve |

## Guard

Fix target without growing siblings. Remeasure peers every fix.
