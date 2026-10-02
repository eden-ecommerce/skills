---
name: stacked-vertical-slice
description: Guides feature planning and implementation using vertical slicing, stacked git pull requests, and failure-recovery protocols. Use when breaking large tasks into small, testable, end-to-end pull requests, writing each pull request so it can be tested and deployed on its own, managing stacked branches with GitHub CLI (`gh` / `gh stack`), or handling stack collapse and local backup branches.
agents:
  - cursor
---

# Stacked Vertical Slicing & Safety Workflow

## Core Philosophy
- **Vertical Slicing:** Every pull request delivers a thin, complete, functional end-to-end increment (DB/schema, API, and UI together) rather than architectural horizontal layers.
- **Stacked PRs:** Each slice branches off the preceding slice (`Slice 1` -> `Slice 2` -> `Slice 3`). Work on downstream slices immediately without waiting for lower PR code review approvals.
- **Defensive Slicing:** Every slice MUST compile, pass tests, and remain safe in production via feature flags or dormant routes.

---

## Phase 1: Feature Planning & Decomposition

Before modifying any code, present a **Vertical Slice Plan** conforming to these rules:

1. **Slice 1 (Foundation Slice):** Schema/migrations + baseline API endpoint + stub UI component (behind a feature flag or dev route).
2. **Slice 2 (Core Interaction Slice):** Full request validation + domain logic + primary UI interactions and state.
3. **Slice 3 (Hardening & Edge Cases):** Error recovery states, telemetry, performance optimization, and visual polish.

> **Constraint:** Target 150–250 lines of changed code per slice. If a slice exceeds ~300 lines, split it vertically into sub-slices (e.g., `1a` and `1b`). NEVER group by horizontal layers (e.g., "PR 1: Database, PR 2: UI").

---

## Phase 2: Stacked Git Branch Execution

Branch Hierarchy:
```text
main
 └── feature/<name>/slice-1-base     (PR #1 -> base: main)
      └── feature/<name>/slice-2-core  (PR #2 -> base: feature/<name>/slice-1-base)
           └── feature/<name>/slice-3-ui    (PR #3 -> base: feature/<name>/slice-2-core)
```

Requires `gh` and the extension `gh extension install github/gh-stack`. Pass branch names exactly as above. `gh stack` does not rewrite them.

Run every `gh stack` command non-interactively, or it hangs:

- `gh stack init` and `gh stack add` always get a branch name.
- `gh stack submit` always includes `--auto`.
- `gh stack view` always includes `--json`.
- Pass `--remote origin`.

```bash
gh stack init --base main feature/<name>/slice-1-base
# commit slice 1 only
gh stack add feature/<name>/slice-2-core
# commit slice 2 only
gh stack add feature/<name>/slice-3-ui
# commit slice 3 only
gh stack submit --auto --remote origin
gh stack view --json
```

Commit with `git add` and `git commit` so each slice contains only its own files. To change an earlier slice, `gh stack checkout` that branch, commit there, then `gh stack rebase --upstack` and `gh stack push --remote origin`.

---

## Phase 3: Pull request text, then deploy one slice at a time

`gh stack submit --auto` opens the stack. The generated title and body are not the review text. Before anyone is asked to review, set each pull request body with `gh pr edit`.

A developer should be able to test this slice without reading the other pull requests.

A slice that does not compile is not a slice. Land a file after the files it imports. Each slice stays safe to deploy on its own, through a feature flag, a dormant route, or an additive change. If a slice cannot be deployed alone, say so in the body and split the slice until it can.

Write the body in plain sentences. Do not use em dashes. Do not use filler such as "ensuring" or "highlighting". Do not start a line with a bold label that repeats the sentence. Do not paste a Cloud Run, Drizzle, or terraform checklist into a repo that does not have those. Use those lines only when that repo deploys that way.

Each body uses these sections, in this order.

### Summary

One or two sentences on what this slice changes and why.

### Scope

What is in this pull request. What is left for a later slice. The package pin, if this slice changes one. Whether this change is safe to ship on its own.

### Dev test plan

Numbered checks for this branch only. Name the command, the URL, and the click path. Mark what this slice cannot show yet.

### Deployment plan

1. Merge this pull request only.
2. Deploy this slice. Name the real command for this repo.
3. Run the dev test plan on the deployed result.
4. Run `gh stack sync --remote origin` so the next pull request targets `main`.
5. Do not merge the next slice until this one has been deployed and tested.

Design and lib publish with Changesets and a `design-v*` or `lib-v*` tag. A consumer then pins that exact version. An app deploys on its own host. Write that path in the body. Do not invent a host.

### Reversion plan

How to undo this slice without undoing the slices above it.

```bash
gh pr edit <number> --body "$(cat <<'EOF'
## Summary

<one or two sentences>

## Scope

<what is in this pull request, what is left for a later slice, package pin if any, safe to ship on its own or not>

## Dev test plan

1. [ ] <command, URL, and click path for this branch only>
2. [ ] <what this slice cannot show yet>

## Deployment plan

1. [ ] Merge this pull request only.
2. [ ] Deploy this slice with <real command for this repo>.
3. [ ] Run the dev test plan on the deployed result.
4. [ ] `gh stack sync --remote origin` so the next pull request targets `main`.
5. [ ] Do not merge the next slice until this one has been deployed and tested.

## Reversion plan

<how to undo this slice without undoing the slices above it>
EOF
)"
```

---

## Phase 4: Stack collapse

Collapse is a merged lower slice (including a squash merge) leaving the branches above it without their parent commits.

1. Do not `git push --force` and do not retarget bases by hand.
2. Run `gh stack sync --remote origin`. It fetches, rebases upward (using `--onto` after a squash merge), retargets each open PR, and pushes.
3. Exit code 3 means a conflict and that every branch was restored to its pre-rebase state. Resolve, then `gh stack rebase --continue`. Repeat per conflict. If the resolution is wrong, `gh stack rebase --abort`.
4. After the stack is green, `gh stack sync --prune --remote origin` drops local branches whose PRs have merged.
5. Confirm with `gh stack view --json`: merged slices show `isMerged: true`, and the next open PR's base is the new parent (or `main`).

---

## Phase 5: Local backup branches

Take a local backup before `gh stack sync` or `gh stack rebase` when a lower slice has merged or `gh stack view --json` shows the stack has diverged. Do not push the backup and do not open a pull request for it.

1. For each open branch, read its SHA from `gh stack view --json`.
2. `git branch backup/<branch> <sha>`.
3. Run the stack collapse phase.
4. If recovery is aborted, the backup branch still holds the old commits. Reset or cherry-pick from `backup/<branch>`.
5. When `gh stack view --json` shows the recovered PRs open and pushed, delete each `backup/<branch>` locally.
