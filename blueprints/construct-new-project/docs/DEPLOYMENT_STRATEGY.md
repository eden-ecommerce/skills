# Deployment strategy

Production shipping strategy — separate from [SETUP.md](./SETUP.md) (local dev). This file answers: where does this run, what does production require, what has to be true before a PR can merge, and how does a bad deploy get undone.

Fill this file **at project intake**, not after the first deploy breaks — Stage 2 of `../SKILL.md` asks for a deployment-strategy answer (or proposes one) specifically so the first MVP has a real target to build toward, not just "runs on my machine."

## 1. Pick a strategy (decide at intake)

| Strategy | Pick when | Gives up |
|---|---|---|
| **Serverless platform** (Vercel, Netlify, Cloudflare Pages) | Framework has first-class support (Next.js → Vercel), fast iteration matters more than infra control, traffic is spiky | Long-running background workers need a separate host; cold starts on rarely-hit routes |
| **Managed container** (Cloud Run, Fargate, App Runner) | Need a real background worker process, or the framework doesn't have a serverless-native host, or per-request cost control matters | More ops surface than a fully serverless platform (Dockerfile, min/idle instances) |
| **Traditional VM / Kubernetes** | Existing platform team already runs one, or compliance requires it | Most ops surface, slowest to first deploy — do not default here for a new MVP without a reason |
| **Static host + API service split** | Frontend has no server-rendering need; backend is a thin API | Two deploy pipelines instead of one |

If the brief gives no strong reason to deviate, propose the **managed container** row when the project has any background worker (see `ARCHITECTURE.md` § Background / durable jobs) or the **serverless platform** row when it doesn't — state this as the recommendation, not a silent default, and let the user override it.

## 2. Production architecture requirements

Once a strategy is picked, the concrete checklist (worked example: Cloud Run + Terraform + GitHub, verbatim law in `environment/terraform.md` (incl. first-time setup checklist), `environment/docker.md`, `environment/developer.md`, `environment/github.md`). Serverless on Vercel: `environment/vercel.md` + `../templates/vercel.json.*.template`. A different target loads a different `environment/<target>.md` set — see `ARCHITECTURE.md` § Deployment-target rule files; write that target's own file when it has no worked example yet, rather than reusing Cloud Run's.

- [ ] Process listens on the platform's injected port (`$PORT` on Cloud Run); container/runtime config matches
- [ ] Image/build artifact tested locally before first deploy (`docker run` or platform-equivalent smoke test)
- [ ] Infra-as-code (if any) state is uniquely namespaced per app/environment — never copy another app's backend config unchanged
- [ ] Deploy config pins a released version, not a moving branch ref
- [ ] Secrets live in a secret manager, never in git, never baked into the image
- [ ] CI has a plan/build stage that runs on every PR; apply/deploy is a separate, explicitly triggered stage
- [ ] Someone (a person or a team) owns approving the first production apply — name that owner here once known

## 3. Environments

`local` → `staging` → `production`, minimum. Each environment:

- Has its own credentials — never share a production secret into a lower environment
- Secrets sync from a manager (`pnpm sync:secrets:<env>` pattern, or the platform's own env-var UI) — see `CONFIG.md`
- Staging is where a PR's e2e/deploy proof happens before production, not a place changes skip

## 4. Branch and PR/MR rules

- One long-lived integration branch (`main`); short-lived feature branches merge into it via PR/MR — avoid parallel long-lived release branches unless the strategy genuinely needs them
- A PR/MR body always comes from a template (`.github/pull_request_template.md` or equivalent) covering: summary, scope, dev test plan, reviewer checklist, deployment plan, reversion plan — never left with unfilled placeholders. Full law: `../rules/pull-requests.mdc`
- A PR is mergeable only once its checklist is honestly ticked — ticking a box that isn't true in the diff is worse than leaving it unticked

## 5. Pipeline checks (gate before merge)

One chained script — `predeploy` / `pipeline` — runs, in order: branch-is-current-with-main → typecheck → lint → test → build → e2e. Never merge to the integration branch while it's red; CI passing a subset (e.g. unit tests only) is not a substitute for the full local chain. Full law: `../rules/predeploy.mdc`.

## 6. Rollback / reversion plan

Every PR states, before merge, how to undo it if production breaks:

- **Code rollback** — revert the merge commit / redeploy the previous released image
- **Data rollback** — additive-only migrations roll back for free; anything destructive needs a named recovery step (restore point, backfill script) written down *before* the migration ships, not improvised during an incident

## What this doc is not

Not a copy of content-studio's actual Cloud Run/Terraform config. Section 2's checklist is the generic shape; the linked rule files are the one concrete worked implementation (Cloud Run) — swap them for the chosen platform's own checklist once Section 1 picks a strategy.
