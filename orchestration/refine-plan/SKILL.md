---
name: refine-plan
description: "Optional re-check after a person edits the master plan by hand. The daily loop does not use this. construct-master-plan already closes the plan."
agents:
  - cursor
---

**Not a daily step.** `/construct-master-plan` already explains the options, settles every blocking choice, and sets `ready`. Build that file.

Run this only when a person edited `{feature}-master-plan.md` after `ready`. No production code. Do not call CreatePlan. Do not write a second plan.

One readonly subagent per `## Sub` section, plus one for the sections above the first sub. Give each agent that section, the **Decisions**, and that repo's rules. Do not paste the whole plan into every agent.

---

## Flow

### 1. Fan out

One readonly subagent per `## Sub` section. Run them in parallel. One more subagent reads the sections above the first sub.

- The top subagent gets **Objectives**, **Scope**, **Decisions**, and **Ambiguities**.
- Each sub agent gets that `## Sub` section and the **Repos** row.

Each subagent returns a table and nothing else:

| claim | evidence | verdict | fix |
|-------|----------|---------|-----|

Verdict is `keep`, `fix`, or `ask`. Evidence is `path:line` or a fetched standard URL plus section. A cited standard is fetched and checked in this run. A recalled standard with no fetch is `ask`, not `keep`.

Checklist, every row answered:

- What do you disagree with in this plan?
- Which sentence is an assumption, and what file contradicts it?
- Which behaviour has two readings?
- Which guard rail is missing, or named but not present in the cited code?
- Does this sub deploy on its own after the `needs` steps are deployed?
- Which repo rule does a planned change break?

`fix` includes the replacement sentence or the row to delete. `ask` is only for a decision the user must make. Do not invent the user's choice.

### 2. Cross-plan check

The parent checks, after the subagents return:

- response and request shapes match between a sub that calls and a sub that serves
- `needs` matches the deploy order in **Subs**
- every edge-case row has a test-plan row, and every test-plan row cites an edge-case number or a WSTG id
- no two subs write the same file

Add rows in the same claim table.

### 3. Apply and ask

Apply every `fix` to the plan files. Do not apply a `fix` that changes a **Decisions** row.

Before the questions, brief the `ask` rows the same way construct-master-plan briefs before grilling. Follow the wait-what skill: Simplified Technical English, and the terms in `.cursor/CONTEXT.md`. For each row, state the current behaviour with `path:line`, the options, and the tradeoff in one sentence. No question in that briefing. Stop so the user can read it.

Then ask the `ask` rows together, numbered, each with a recommended answer. Above each question, repeat the current-state fact and the options in one or two short sentences. Wait. Write the answers into **Decisions** and patch the affected rows.

When the user says they do not know, or asks you to simplify: do not repeat the question. Find the missing fact. Re-pitch that one choice with the new evidence. Ask again only after that re-pitch.

If a new `fix` appears from an answer, apply it. Loop until no blocking `ask` remains. A deferred item needs a written default in **Decisions**.

Code comments that the plans require: cite a standard only for a guard rail a reader would not see from the neighbouring code. Do not plan a comment that repeats the function name.

### 4. Mark ready

Set **Approvals** `ready` to today's date. Clear it if this pass changed scope. Tell the user to click Build. Do not call CreatePlan.
