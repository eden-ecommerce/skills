---
name: review-checklist
description: "Dead-simple pre-review sanity check. Diff the branch against origin/main, flag backwards-incompatible changes and database migrations, then fill the MR/PR overview: summary, features added/updated/removed, test plan, deployment plan, reversion plan. Use when handing a branch over for review, preparing a pull request or merge request, or asking to check compatibility, migrations, deploy, or revert."
agents:
  - cursor
---

Dead simple. Run before a branch is handed over for review. Do not edit code. Do not open a PR unless asked.

1. `git fetch origin`
2. Diff this branch against `origin/main`. If that ref is missing, use `origin/master`.
3. Read `git diff` and `git log` on that range. Find the core purpose and the changed components, routes, and models.
4. Run the checks. Then output the template. Fill every bracket from the diff. NO FLUFF.

## Checks

- **Backwards incompatible:** callers, routes, payloads, stored data, flags, removed behaviour. List each issue, or `none`.
- **Migrations:** search the diff for schema changes (`migrations/`, `drizzle/`, `schema.sql`, `ALTER TABLE`, `CREATE TABLE`). Result is `none` or the file list. Do not invent a migrate command when the result is `none`.
- **Deployment:** name every non-code step the diff needs (migrate, script, cache, flag, env). Code-only diffs say `code-only`.
- **Reversion:** code rollback is enough only when migrations are `none`. If a migration exists, say code rollback is not enough and name the recovery.

## Output

Paste-ready markdown. Write `none` on a step that does not apply. Do not leave placeholders. Do not invent commands, URLs, or SQL that are not in the diff.

## Sanity
- Backwards compatible: [none | list issues]
- Migrations: [none | files]
- Deploy: [code-only | extra steps]
- Revert: [code rollback | recovery needed]

## Summary
[1-2 sentences: what the diff does]

## Features
- **Added:** [or none]
- **Updated:** [or none]
- **Removed:** [or none]

## Development Plan
- [x] Branch correct
- [ ] Changes: [Bullet list: exact components/routes/models from diff]
- [ ] Checked backward compatibility

- **Testing Steps:**
1. Step 1: DB migration (BASH): `[none, or the real command]`
2. Step 2: Run script (PHP): `[none, or the real command]`
3. Step 3: Check DB table (SQL): `[none, or the real query]`
4. Step 4: Check frontend (URL): `[real local URL from the diff]`

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
1. Step 1: DB migration (BASH): `[none, or the real command]`
2. Step 2: Run script (PHP): `[none, or the real command]`
3. Step 3: Check DB table (SQL): `[none, or the real query]`
4. Step 4: Check frontend dashboard (URL): `[real prod URL from the diff]`

- **Checklist:**
1. [ ] Eden core flows work (Login, Nav, Search, Basket, Express Pay)
2. [ ] APIs & cache work [List changed APIs here if any]
3. [ ] `#it-private` & PO told deploy success

## Reversion Plan
- [ ] 1. Tell PO & `#it-private` rolling back.
- [ ] 2. Vercel Rollback OR GitLab Revert.
- Recovery: [code rollback only | exact recovery, because a migration shipped]
