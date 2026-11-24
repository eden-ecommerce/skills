---
name: merge-plan
description: "Deploy step. Write what shipped back into the one master plan and a merge request body per sub. Use after Build, when the plan's automated tests passed."
agents:
  - cursor
---

**Deploy the plan that was built.** No new feature code. Docs and merge request bodies only.

**Input:** `{feature}-master-plan.md` and the git diff per repo.

**Refuse** when `ready` is `pending`. A diff that adds behaviour with no matrix row is a deviation, not a new feature. Do not extend the plan to match the creep. Record it and stop that sub's body until the user deletes the extra diff or accepts the deviation in **Decisions**.

**Bind:** read **Repos**. Each body uses that repo's `mr_template`.

---

## Flow

### 1. Read what shipped

For each repo, read `git diff` against the default branch (`origin/main`, else `origin/master`). The diff wins over the plan text.

Read automated and manual rows in each sub's **Tests** table. Unticked manual rows are listed as not run. Do not tick them yourself.

### 2. Update the master plan

On each sub that has a diff:

- check that sub's heading
- fill **As built** with the actor, the input, and the output the code produces
- set each matrix row `status` to `shipped`, `changed`, `dropped`, or `added`
- a `changed` or `added` row states the output, the side effect, and `path:line`
- a `dropped` row says what was not built
- append **Deviations** for anything that is not `shipped`
- append **Sync Log** with the date, the step, the gate results, and the manual rows still open

Keep the original matrix rows. Do not delete a planned row.

### 3. One merge request body per sub

Write `merge-requests/{step}-{repo}-{task}.md`.

Read the template file at `mr_template`. Keep that file's headings. Fill them from this sub's diff only. Delete placeholder comments. Where a heading does not apply, write `none`. Do not invent commands, URLs, SQL, or hosts. Do not add headings the template does not have.

When `mr_template` is `default`, use only these headings:

```md
## Summary

## Scope

## Test steps

## Reviewer checklist

## Deployment

## Reversion
```

- **Summary.** One or two sentences. What this sub changes and why.
- **Scope.** What is in this sub. What a later sub still does. Whether this sub is safe to deploy on its own. Package pin, or `none`.
- **Test steps.** Numbered. The gate commands that passed, then the manual rows from that sub's Tests table. Name the command, the URL, and the click path when the diff contains them.
- **Reviewer checklist.** Leave the boxes unchecked. Include only checks this repo's rules already require.
- **Deployment.** Merge this request only. Choose the steps with the file checks in [vertically-slice-changes/references/pull_request_template.md](../vertically-slice-changes/references/pull_request_template.md). Keep the sections that match. Delete the rest. The earlier step that must already be deployed (`requires 01 deployed`), or `none`. Do not merge the next sub until this one is deployed and tested. For a PHP repo, write the human steps and do not run them. Do not push `develop`, `master`, or the `production` remote.
- **Reversion.** How to undo this sub without undoing a later one, from the matching reversion block in that template. When the diff has a migration, say code rollback is not enough and name the recovery. When it does not, write `code rollback`.

### 4. Flag large diffs

Count changed lines per sub (`git diff --numstat` on that sub's files). A sub over about 300 changed lines is too big for one review. List those steps and tell the user to run `/vertically-slice-changes` on that repo. Do not split the branches in this skill.

### 5. Stop

Do not push and do not open the merge request unless the user asks. A person lands code on `main` and `master`. Never push those branches, never push those refspecs, and never `gh pr merge` or `glab mr merge`. Return the path of each body.
