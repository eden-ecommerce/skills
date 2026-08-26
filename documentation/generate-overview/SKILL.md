---
name: generate-overview
description: "Generate VCS merge overview — git diff master↔develop."
agents:
  - cursor
---

When asked for MR/PR overview or description:

1. Read git diff.
2. Find core purpose.
3. Find changed components/routes/models.
4. Output exact template below. Fill brackets. NO FLUFF. STUPID SIMPLE.

TEMPLATE TO USE:

## Summary
[1-2 sentences: what diff does]

## Development Plan
- [x] Branch correct
- [ ] Changes: [Bullet list: exact components/routes/models from diff]
- [ ] Checked backward compatibility

- **Testing Steps:**
1. Step 1: DB migration (BASH): `[e.g. ./migrate.sh]`
2. Step 2: Run script (PHP): `[e.g. sudo php backfill.php --dry-run]`
3. Step 3: Check DB table (SQL): `[e.g. SELECT * FROM table WHERE ...]`
4. Step 4: Check frontend (URL): `[e.g. https://www.eden.local/test-screen]`

- **Checklist:**
1. [ ] Automated tests pass (PHPUnit/Selenium/Postman)
2. [ ] Lint/build pass (`eslint --fix` / `prettier --write`)
3. [ ] Preview link tested with prod data

## Reviewer Checklist
- [ ] Read task & check PO expectations
- [ ] Run locally & check visual flow
- [ ] Preview link tested & sent to PO
- [ ] Code check: Logic simple (useEffects -> handlers, kill timeouts/callbacks)
- [ ] Code check: Component structure (imports > consts > hooks > guards > errors > render)
- [ ] Code check: File structure (query hooks, form provider/schema/presenter)
- [ ] Code check: Backward compatibility & backend APIs
- [ ] Ask questions in VCS

## Deployment Plan
- [ ] Rebased on target
- [ ] PO approved
- [ ] `#it-private` & PO warned of deploy start

- **Deployment & Post-Deploy Testing Steps:**
1. Step 1: DB migration (BASH): `[e.g. ./migrate.sh]`
2. Step 2: Run script (PHP): `[e.g. sudo php backfill.php]`
3. Step 3: Check DB table (SQL): `[e.g. SELECT ...]`
4. Step 4: Check frontend dashboard (URL): `[e.g. https://eden.com/test-screen]`

- **Checklist:**
1. [ ] Eden core flows work (Login, Nav, Search, Basket, Express Pay)
2. [ ] APIs & cache work [List changed APIs here if any]
3. [ ] `#it-private` & PO told deploy success

## Reversion Plan
- [ ] 1. Tell PO & `#it-private` rolling back.
- [ ] 2. Vercel Rollback OR GitLab Revert.
