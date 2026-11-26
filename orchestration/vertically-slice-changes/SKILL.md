---
name: vertically-slice-changes
description: Guides feature planning and implementation using vertical slicing, stacked git pull requests or GitLab merge requests, and failure-recovery protocols. Use when breaking large tasks into small, testable, end-to-end pull requests or merge requests, writing each one so it can be tested and deployed on its own, managing stacked branches with GitHub CLI (`gh` / `gh stack`) or GitLab CLI (`glab`), or handling stack collapse and local backup branches.
agents:
  - cursor
---

# Stacked Vertical Slicing & Safety Workflow

## Core Philosophy
- **Vertical Slicing:** Every pull request delivers a thin, complete, functional end-to-end increment (DB/schema, API, and UI together) rather than architectural horizontal layers.
- **Stacked pull requests or merge requests:** Each slice branches off the preceding slice (`Slice 1` -> `Slice 2` -> `Slice 3`). Work on downstream slices immediately without waiting for lower review approvals.
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

Read the host from `git remote get-url origin`. A `github.com` URL uses the GitHub path. A GitLab URL uses the GitLab path. If the host is unclear, ask before creating branches.

The base branch is `main`. A PHP repo (`composer.json` present and `vercel.json` absent) uses `develop`. Do not open a slice against `master`.

**Branch.** `git fetch origin` first. Read `git branch --show-current`. When it is `main` or `master`, stop. Do not commit and do not push. Create the slice branch from the latest `origin/main`, or `origin/master` when `main` does not exist. A PHP repo uses `origin/develop`. The next slice branches off the previous slice, not off `main`. A person merges each request into `main`, `master`, or `develop`.

**Push gate.** Push only the slice branch: `git push -u origin HEAD`. Stop when the branch or the refspec is `main`, `master`, `HEAD:main`, or `HEAD:master`. Do not `gh pr merge` or `glab mr merge`. Do not push `develop` or the `production` remote. See [references/pull_request_template.md](references/pull_request_template.md).

**Commit.** One line: `type(entity): outcome`. Type is `fix`, `chore`, `doc`, or `feature`. Entity is the table or the domain. Outcome is the task result, caveman. Author stays the existing git identity. No `--author`, no `--trailer`, no `Co-authored-by`, no `Signed-off-by`, no provider name. Do not change git config. Do not commit on `main` or `master`.

Branch hierarchy is the same on both hosts. Each review targets the branch under it. For a PHP repo, replace `main` below with `develop`:

```text
main
 └── feature/<name>/slice-1-base     (review 1 -> base: main)
      └── feature/<name>/slice-2-core  (review 2 -> base: feature/<name>/slice-1-base)
           └── feature/<name>/slice-3-ui    (review 3 -> base: feature/<name>/slice-2-core)
```

Commit with `git add` and `git commit -m "type(entity): outcome"` so each slice contains only its own files. Pass branch names exactly as above. The message follows the commit rule above.

### GitHub

Requires `gh` and the extension `gh extension install github/gh-stack`. `gh stack` does not rewrite the branch names.

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

To change an earlier slice, `gh stack checkout` that branch, commit there, then `gh stack rebase --upstack` and `gh stack push --remote origin`.

### GitLab

Requires `glab`, installed and authenticated. `glab stack` is experimental and names its own branches, so do not use it for this workflow. Create the named branches and open each merge request with the parent as the target.

```bash
git checkout -b feature/<name>/slice-1-base main
# commit slice 1 only
git push -u origin HEAD
glab mr create --source-branch feature/<name>/slice-1-base --target-branch main --title "<title>" --draft --yes --description-file /tmp/slice-1.md

git checkout -b feature/<name>/slice-2-core
# commit slice 2 only
git push -u origin HEAD
glab mr create --source-branch feature/<name>/slice-2-core --target-branch feature/<name>/slice-1-base --title "<title>" --draft --yes --description-file /tmp/slice-2.md
```

To change an earlier slice, check out that branch, commit there, rebase the branches above it, then `git push --force-with-lease` each rewritten branch. Do not use `--force` without `--force-with-lease`.

### GitLab without `glab`

When `command -v glab` finds nothing, open each merge request with GitLab push options on the push itself. Do not install `glab` and do not call the GitLab API with a token.

Write the body to a file first. Git refuses a push option that contains a newline, so replace each newline with the two characters `\n`. GitLab 15.0 and later turn them back into newlines.

```bash
desc=$(< /tmp/slice-1.md)
desc=${desc//$'\n'/\\n}
git push -u origin HEAD \
  -o merge_request.create \
  -o merge_request.target=main \
  -o "merge_request.title=Draft: <title>" \
  -o "merge_request.description=$desc"
```

- The `Draft:` title prefix stands in for `--draft`.
- Read the body from a file. Do not build it with a heredoc inside `$(...)`. macOS ships bash 3.2, which fails on an apostrophe inside that heredoc.
- The push prints the merge request URL. Open it and check the description. If it shows a literal `\n`, the server is older than GitLab 15.0. Use `<br>` in place of `\n` from then on, and ask a person to fix that description in the GitLab UI.
- Push options travel only with a push that sends commits. When the branch is already up to date, git sends nothing and the options are dropped. Wherever this skill runs `glab mr update`, add the same option to the next push that sends commits instead, for example the `git push --force-with-lease` after a rebase: `-o merge_request.target=<base>` or `-o "merge_request.description=$desc"`. When no such push is due, ask a person to make the change in the GitLab UI.

---

## Phase 3: Review text, then deploy one slice at a time

Opening the stack does not write the review text. On GitHub, `gh stack submit --auto` opens draft pull requests. On GitLab, `glab mr create` opens the merge requests. Before anyone is asked to review, set each body. On GitHub use `gh pr edit`. On GitLab use `glab mr update <id> --description-file <file> --yes`.

A developer should be able to test this slice without reading the other reviews.

A slice that does not compile is not a slice. Land a file after the files it imports. Each slice stays safe to deploy on its own, through a feature flag, a dormant route, or an additive change. If a slice cannot be deployed alone, say so in the body and split the slice until it can.

Write the body in plain sentences. Do not use em dashes. Do not use filler such as "ensuring" or "highlighting". Do not start a line with a bold label that repeats the sentence. The body uses only these headings from [references/pull_request_template.md](references/pull_request_template.md): Summary, Scope, Dev test plan, Deployment plan, Reversion plan.

Run the file checks in that template before filling Deployment plan or Reversion plan. Keep each subsection the check matched. Delete every subsection it did not match. Do not leave another repo's deploy steps in this body. Where a kept line names a system this repo does not have, write "none". Do not delete a heading that the check kept.

### Summary

Heading in the template: `## Summary`.

One or two sentences on what this slice changes and why. Do not invent a different summary shape.

### Scope

Heading in the template: `## Scope`.

What is in this pull request. What is left for a later slice. The package pin, if this slice changes one. Whether this change is safe to ship on its own.

### Dev test plan

Heading in the template: `## Dev test plan`.

Numbered checks for this branch only. Name the command, the URL, and the click path. Mark what this slice cannot show yet.

### Deployment plan

Heading in the template: `## Deployment plan`.

Copy the numbered steps from the sections the file checks kept. Do not invent a host.

1. Merge this pull request only, into `main`, or into `develop` for a PHP repo.
2. Deploy this slice by the kept section. A PHP production push, `worker-deploy`, and `terraform apply` are a person's actions. The agent does not run them.
3. Run the dev test plan on the deployed result.
4. Point the next review at the base branch (`main`, or `develop` for PHP). On GitHub, run `gh stack sync --remote origin`. On GitLab, rebase the next branch onto that base, run `git push --force-with-lease`, then `glab mr update <id> --target-branch <base> --yes`.
5. Do not merge the next slice until this one has been deployed and tested.

### Reversion plan

Heading in the template: `## Reversion plan`.

How to undo this slice without undoing the slices above it.

Fill [references/pull_request_template.md](references/pull_request_template.md) for this slice, then set the body from that file.

```bash
# GitHub
gh pr edit <number> --body-file <filled-template>

# GitLab
glab mr update <id> --description-file <filled-template> --yes
```

---

## Phase 4: Stack collapse

Collapse is a merged lower slice (including a squash merge) leaving the branches above it without their parent commits.

### GitHub

1. Do not `git push --force` and do not retarget bases by hand.
2. Run `gh stack sync --remote origin`. It fetches, rebases upward (using `--onto` after a squash merge), retargets each open pull request, and pushes.
3. Exit code 3 means a conflict and that every branch was restored to its pre-rebase state. Resolve, then `gh stack rebase --continue`. Repeat per conflict. If the resolution is wrong, `gh stack rebase --abort`.
4. After the stack is green, `gh stack sync --prune --remote origin` drops local branches whose pull requests have merged.
5. Confirm with `gh stack view --json`: merged slices show `isMerged: true`, and the next open pull request's base is the new parent (or `main`).

### GitLab

1. Do not `git push --force` without `--force-with-lease`.
2. Rebase each open branch onto its new parent. After a squash merge, use `git rebase --onto <new-parent> <old-parent> <branch>`.
3. On a conflict, resolve it, then `git rebase --continue`. If the resolution is wrong, `git rebase --abort`.
4. `git push --force-with-lease` each rewritten branch, then `glab mr update <id> --target-branch <new-parent> --yes`.
5. Confirm the next open merge request targets the new parent (or `main`). Delete local branches whose merge requests have merged.

---

## Phase 5: Local backup branches

Take a local backup before a stack sync or rebase when a lower slice has merged or the stack has diverged. Do not push the backup and do not open a review for it.

1. For each open branch, read its SHA. On GitHub, read it from `gh stack view --json`. On GitLab, read it with `git rev-parse <branch>`.
2. `git branch backup/<branch> <sha>`.
3. Run the stack collapse phase.
4. If recovery is aborted, the backup branch still holds the old commits. Reset or cherry-pick from `backup/<branch>`.
5. When the recovered reviews are open and pushed, delete each `backup/<branch>` locally.
