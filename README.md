# Cursor skills

One plan, then build, then deploy. The master plan is the only build input. Detail: [docs/software-development-lifecycle.md](docs/software-development-lifecycle.md).

## Install

```bash
npx skills@latest add eden-ecommerce/skills -a cursor --global --skill '*' -y
npx skills@latest add mattpocock/skills -a cursor --global --skill '*' -y
npx skills@latest add JuliusBrussee/caveman -a cursor --global --skill '*' -y
npx skills@latest add DietrichGebert/ponytail -a cursor --global --skill '*' -y
```

Choose **Global** when prompted. Reload Cursor (`Ctrl+Shift+P` → **Developer: Reload Window**).

Cursor reads `~/.claude/skills/`. Those entries are symlinks to `~/.agents/skills/`, which is where `npx skills add` writes. After a skill change in this repo, run the eden-ecommerce install again, then reload the window. Do not keep a second copy under `~/.cursor/skills/` for a skill this repo already ships.

## Daily loop

One plan, then build, then deploy. You answer the briefing. After that the same file is the build and the deploy record. The agent does not open a second plan and does not add scope during Build.

```
docs/feature/{feature}/
  references/                              # brief, process notes
  {feature}-master-plan.md                 # the only plan
  merge-requests/{step}-{repo}-{task}.md   # written at deploy
```

Each `## Sub` is one repo and one deployable step. Sub 01 deploys on its own. A later sub names the step that must already be deployed. The section holds the files, the matrix, the flow, the tests, and the deploy steps.

### 1. Plan

Put the brief in `references/` and point at it.

```
/construct-master-plan @docs/feature/giftnotes/references/giftnotes.md
new route in @EdenApi.php
```

You get a briefing before any question. It has:

- what the code does today, with file and line
- the expected outcome, in one sentence
- a flow diagram
- a matrix of operations, outputs, and side effects
- each open choice, the options, and the tradeoff

Answer those choices. When you do not know, say so. The agent looks up the missing fact and explains that choice again.

It then writes `{feature}-master-plan.md` and sets `ready`. Click Build. Do not run another planning command.

### 2. Build

Click Build. `/implement-plan` reads that file and builds each `## Sub` in order. A subagent sees only its own section.

The work is not done on `main` or `master`. The agent fetches the latest base and creates `feature/<feature>/<step>-<repo>-<task>` from `origin/main`, from `origin/master` when `main` does not exist, or from the feature branch already in use. A PHP repo starts from `origin/develop`. It pushes that branch and opens the pull request or merge request. You merge it into `main` or `master`.

Build stops when a gate fails or a fact is missing from the plan. It does not invent the missing behaviour.

When the gates pass, run the manual rows in each sub's Tests table. A failed row is fixed as that row only. Then go to deploy.

### 3. Deploy

```
/merge-plan giftnotes
```

The same master plan gains an As built section and a deviations table. You also get one merge request body per sub, filled from that repo's own template.

You land `main` and `master`. The agent does not push those branches and does not merge the request. On a PHP repo you merge into `develop`, test, merge into `master`, push `origin`, then push the `production` remote. The agent does not run that sequence. It also does not run `worker-deploy` or `terraform apply`.

### When a change is too big

`/vertically-slice-changes` only when `/merge-plan` says a sub is over about 300 changed lines. Each slice is still one review, one test, and one deploy. The master plan stays the source.

## Git guards

Hard human gate. A person merges into `main` and `master`.

Before a master plan or a sub is edited, the agent fetches the latest base. When the current branch is `main` or `master`, it stops. It creates `feature/<feature>` or `feature/<feature>/<step>-<repo>-<task>` from `origin/main`, from `origin/master` when `main` does not exist, from `origin/develop` on a PHP repo, or from the feature branch already in use. It pushes only that branch and opens the pull request or merge request. It does not merge the request.

Commit one line, caveman: `type(entity): outcome`. Type is `fix`, `chore`, `doc`, or `feature`. Entity is the table or the domain. Outcome is the task result. Author stays the existing git identity. No `Co-authored-by`, no `Signed-off-by`, no provider trailer.

## Other orchestration skills

Called by the loop. Still usable on their own.

| Invoke | When |
|--------|------|
| `/refine-plan` | Only after you edited the master plan by hand |
| `/construct-sub-plan` | Redo one sub section inside the master plan |
| `/construct-test-plan` | Redo one test plan |
| `/review-implementation` | Review a diff outside Build |
| `/handoff-plan` | Switch threads |
| `/clarity-with-stakeholder` | Plain English for a PM |

Path: [`orchestration/`](orchestration/). [`vertically-slice-changes`](orchestration/vertically-slice-changes/) stays a standalone skill.

## Blueprint skills

End-to-end implementation playbooks. Invoke directly. No master plan required.

| Invoke | When |
|--------|------|
| `/add-publisher-panel` | New `publisher*` panel across API, hub, UI, Storybook, storefront (`panelProducts`) |
| `/construct-new-project` | Scaffold a new app from the blueprint |
| `/generate-sanity-panels` | Sanity panel copy workflow |

## Optimisations

| Invoke | When |
|--------|------|
| `/optimise-bundles` | Route JS budget / `firstLoadUncompressedJsBytes` CI failure |
| `/optimise-core-web-vitals` | CLS, LCP, INP, FCP, TTFB, TBT, layout shift, render-blocking, GTmetrix/Lighthouse/CrUX |

## Documentation

Invoke on their own: `/document-current-state`, `/document-database`, `/document-flow`, `/generate-changelog`, `/generate-overview`, `/generate-handoff-doc`, `/refine-rules`, `/review-checklist`.

`/generate-handoff-doc` explains a large process or writes a rebuild handoff. Step 1 calls it when the brief depends on a process the thread cannot hold.

`/review-checklist` and `/generate-overview` fill a single branch overview when you are not in the master-plan loop. Inside the loop, `/merge-plan` uses each repo's own template.

## Design

`/ux-redesign` proposes an incremental or radical redesign of a page, feature, or journey before building it. Path: [`design/`](design/).

## Target repo setup

Copy [docs/AGENTS.md](docs/AGENTS.md) to the repo root as `AGENTS.md`. Keep `.cursor/rules/`. Add `.cursor/STRUCTURE.md` and `.cursor/CONTEXT.md` when the repo uses them. The master plan **Repos** table is what subagents read, so each repo's rules still apply when several repos are open.
