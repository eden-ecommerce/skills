---
name: implement-plan
description: "Build the ready master plan in deploy order, one subagent per sub section, then review each diff. Use when the user clicks Build. No new questions. No scope beyond the plan."
agents:
  - cursor
---

**Build the plan. Then deploy.** This is what the Build button runs. The master plan is the only input.

**Refuse** when `ready` is `pending` or missing, or when **Ambiguities** still has a blocking row with no **Decisions** entry. Finish `/construct-master-plan`. Do not re-plan during Build.

**Scope.** A subagent implements its `## Sub NN` section and nothing else. A missing fact stops that sub. Name the matrix id. Do not invent behaviour and do not add a feature.

**Bind:** before a subagent edits a repo, it reads the rules on that sub's **Repos** row. Those files win over this skill.

**Git.** Hard human gate. A person merges into `main` and `master`.

Before the first edit in a repo, `git fetch origin` and read `git branch --show-current`. When the branch is `main` or `master`, stop. Do not edit, commit, or push. Create `feature/<feature>/<step>-<repo>-<task>` from `origin/main`, or `origin/master` when `main` does not exist. A PHP repo uses `origin/develop`. When this sub continues an existing feature branch, branch off that feature branch. `git checkout -b <name> <base>`. Push only that branch with `git push -u origin HEAD`. Open the pull request or merge request. Do not `gh pr merge` or `glab mr merge`. Do not push a refspec of `main` or `master`.

Commit one line: `type(entity): outcome`. Type is `fix`, `chore`, `doc`, or `feature`. Entity is the table or the domain. Outcome is the task result, caveman. Author stays the existing git identity. No `--author`, no `--trailer`, no `Co-authored-by`, no `Signed-off-by`, no provider name. Do not change git config.

---

## Build the feature

Read `{feature}-master-plan.md`. Walk each `## Sub` in step order. Do not start a sub whose `Needs` steps are not yet implemented in this run.

For each sub, dispatch one subagent. Wait for it before the next sub. Give it only:

- that `## Sub` section
- the **Repos** row for its repo
- the rules list on that row
- the instruction to follow `/ponytail` and this section only

Do not paste the other subs.

The subagent:

1. Implements the Files table. A companion edit (change log, generated client) needs a named repo rule.
2. Writes the automated tests in the Tests table, then the code that makes them pass.
3. Runs the gate commands from the repo row. A failing gate stops this sub. Paste the failure. Do not start the next sub.
4. Follows [review-implementation](../review-implementation/SKILL.md) on this sub's diff. Applies the required refactors that stay inside the section. Re-runs the gates.

The parent appends **Sync Log**: step, gates, review. It does not widen the plan.

When every sub's gates pass, stop. The manual rows in each Tests table are the user's check. Then `/merge-plan`. A failed manual row names the test number. Fix that row only.
