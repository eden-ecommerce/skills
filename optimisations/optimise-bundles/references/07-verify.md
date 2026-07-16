# 07 — Verify

```bash
pnpm turbo-analyse-ci
pnpm run ts-check
pnpm run lint
```

Sync standalone `next-next-eden` ↔ `apps/next-next-eden` when both live.

## Sibling hard gate

Target green ≠ done. Peers (`/home`, `/o/*`, same-layout routes) must stay within threshold.

## Bundle Impact Summary

```markdown
### <change name>
- **Routes:** /product/[id]
- **kB before → after:** 1715.9 → 1591.4
- **Regression class:** route-specific
- **What moved:** <edge cut>
- **Why safe:** <behaviour unchanged>
- **Siblings:** /home, /o/* unchanged
```
