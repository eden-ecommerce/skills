## Summary

[1-2 sentences: what changes and why]

## Scope

- **Layers:** [app / features / data / domain / services / workflows / drizzle / ...]
- **Routes:** [paths or "none"]
- **BUILD_STEPS changed?** [no | yes, master-plan row + migration + seed + `STEP_MANIFEST` in this pull request]
- **Migrations:** [none | list `drizzle/migrations/...`]
- **Package pins:** [unchanged | `@eden-ecommerce/design` / `lib` bump]
- **Backward compatibility:** [additive | breaking, describe]
- **Cloud Run / terraform:** [none | `terraform/service.yaml` only | other, list]

## Dev test plan

Manual steps only (pull request: Analyse + Test unit, no Cloud SQL on the runner):

1. [ ] Local migrate/seed: `[e.g. pnpm db:migrate && pnpm db:seed, or pnpm dev:docker]`
2. [ ] Local URL: `[e.g. http://localhost:3000/...]`
3. [ ] Verifying SQL (if any): `[e.g. SELECT ...]`
4. [ ] Operator journey: `[click path through shell / Build / Deliver]`
5. [ ] After Deploy staging: e2e at the staging URL (or the Test e2e job)
6. [ ] If schema change: Migrate database once (shared MySQL, not a dry-run), then e2e, then merge

## Reviewer checklist

- [ ] `pnpm predeploy` green. It must pass before merge to `main`
- [ ] Scope matches Summary
- [ ] Correct layer. No feature to sibling feature, domain to data/workflows, or services to domain imports
- [ ] No new barrels. No `any` / `unknown`
- [ ] No `@deprecated` left behind. Replaced code deleted in the same pull request
- [ ] `docs/public/` + `DOCUMENTATION_MANIFEST` updated when operator-facing

## Cloud Run / terraform

Default for every pull request (mark N/A if no terraform touch):

- [ ] N/A, no Cloud Run / terraform changes
- [ ] Only edited `terraform/service.yaml` (or Infrastructure-team-approved terraform files)
- [ ] Image URI is correct for this environment
- [ ] No secrets committed to git
- [ ] CI plan workflow passed (review `terraform-plan-dev` artifact) when `terraform/**` changed

## Deployment plan

- **Notify:** [who / channel, fill per pull request]
- [ ] Rebased on latest `main` (`pnpm pipeline:branch-base`)
- **Order** (shared MySQL, one migrate):
  1. [ ] Analyse, then Test unit, then Deploy staging
  2. [ ] If migrations: Migrate database once, then Test e2e at the staging URL
  3. [ ] Merge to `main`. Deploy prod (migrate before pin; safe to run again if already applied)

**Cloud Run** (preview and prod may briefly share schema while migrate is in flight):

- Staging: Deploy on a non-`main` push to `content-studio-dev`
- Prod: Deploy on `main`, migrate before pin, to `content-studio`

**Post-deploy:**

1. [ ] Studio shell loads. Tenant picker works
2. [ ] A Build advances a `stage_runs` row from queued to completed (if the pipeline was touched)
3. [ ] Deliver send/publish still works (if delivery was touched)
4. [ ] No new Sentry issue spike
5. [ ] Notify success (use the Notify field above)

## Reversion plan

**Code rollback** (pick one):

- [ ] Cloud Run: shift traffic to the previous revision, or re-apply the prior image URI in `terraform/service.yaml`
- [ ] Revert the merge commit on `main` and let deploy re-run

**Schema rollback does not exist** (`drizzle/migrations/` is forward-only; no `db:rollback`). Before merge, declare:

- [ ] Migration is additive only (new table, column, or index). Code rollback alone is safe
- [ ] Otherwise, the exact recovery SQL or restore point is written below

**Recovery for this pull request:** [SQL / restore point / "additive only, none needed"]
