# Software development lifecycle

One plan, then build, then deploy. Ambiguities are settled in the briefing, before any code. Build does not invent behaviour and does not ask new questions. The master plan is the only build input, so the work cannot drift into a second plan.

```
docs/feature/{feature}/
  references/
  {feature}-master-plan.md
  merge-requests/{step}-{repo}-{task}.md
```

Each `## Sub` is one repo and one deployable step. Sub 01 deploys on its own. Each later sub names the steps that must already be deployed. The sub section holds the files, the matrix, the flow, the tests, and the deploy steps.

| Step | You type | Skill | Result |
|------|----------|-------|--------|
| 1 | `/construct-master-plan` plus the brief | [construct-master-plan](../orchestration/construct-master-plan/SKILL.md) | Briefing, decisions, one master plan with `ready` set |
| 2 | Click Build | [implement-plan](../orchestration/implement-plan/SKILL.md) | That plan, built in order. Automated tests and gates pass |
| 3 | `/merge-plan` | [merge-plan](../orchestration/merge-plan/SKILL.md) | As built in the same file. One MR body per sub |

`/vertically-slice-changes` runs only when a sub is too big for one review.

## What you type

1. `/construct-master-plan @docs/feature/giftnotes/references/giftnotes.md` and one line of constraints, for example "new route in @EdenApi.php".
2. Read the briefing. It has the current behaviour, the expected outcome, a flow diagram, and a matrix. Answer the open choices.
3. Click Build.
4. Run the manual rows in each sub's Tests table.
5. `/merge-plan giftnotes`

## Why one file

A second plan, a second critique, and a feedback table each re-read the same scope. That spends tokens and lets the build diverge from the decision. Subagents receive one `## Sub` section, not the whole plan.

## Rules per repo

The master plan **Repos** table lists each repo's root, gate commands, merge request template, and rule files. Every subagent reads that list before it plans, builds, or reviews. A missing `.cursor/STRUCTURE.md` does not stop the run.

Cursor loads `alwaysApply` rules for the files you have open. It does not load them for a subagent. The table is what makes the subagent follow them.

## Human gates

The briefing in step 1. Manual test rows that automation cannot run. A person lands code on `main` and `master`. PHP production push, `worker-deploy`, and `terraform apply` stay with a person.

The agent does not push `main` or `master` and does not merge the request. Commit one line: `type(entity): outcome`. No co-author trailer.

## Building blocks

The daily drivers call these. You can still run them on their own.

| Skill | When |
|-------|------|
| `/refine-plan` | You edited the master plan by hand after `ready` |
| `/construct-sub-plan` | One sub section needs a new scaffold |
| `/construct-test-plan` | One sub needs its Tests table rewritten |
| `/review-implementation` | A diff needs a review outside Build |
| `/handoff-plan` | The thread is switching |
| `/generate-handoff-doc` | A process or a rebuild is too large to hold in the chat |
| `/clarity-with-stakeholder` | A PM needs the plain-English version |

## Plan mode and models

Step 1 runs in Plan mode and writes `docs/feature/{feature}/{feature}-master-plan.md`. It does not call CreatePlan.

Use a high model for step 1. Use a fast model for step 2. Step 3 can use either.

## Optional, before step 1

Paste a raw task through [task-refinement-prompt.md](task-refinement-prompt.md) when the brief is still a Slack message. The master plan reads that output. It does not require it.

## Target repo

Copy [AGENTS.md](AGENTS.md) to the repo root. Keep `.cursor/rules/` and, when the repo has them, `.cursorrules`, `.cursor/STRUCTURE.md`, and `.cursor/CONTEXT.md`.
