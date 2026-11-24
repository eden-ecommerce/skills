---
name: construct-sub-plan
description: "Build-ready plan for one master-plan sub row. Use from construct-master-plan, or on its own for one sub. No code."
agents:
  - cursor
---

**No code.** One sub becomes one `## Sub NN` section inside the master plan. When a person runs this skill alone, write that section into the master plan. Do not create `sub-plans/`.

**Input:** `{feature}-master-plan.md` and one sub outcome. When a parent agent calls this skill, it passes that outcome and the matrix ids. Do not look up other subs except their `Needs` line.

**Bind:** copy this sub's repo row from the master **Repos** table. Read `.cursorrules`, `AGENTS.md`, every `alwaysApply: true` rule, and every glob rule whose globs match the files you will list. Those rules decide paths, gates, and companion files (change log, generated client). A JavaScript repo uses pnpm. Do not write `npm` or `yarn` commands.

**Path:** insert under `## Sub {step}` in `{feature}-master-plan.md`. Do not write a second file.

---

## Steps

1. **Scope.** Cite the master Context, Impact, and the matrix ids this sub implements. State out of scope, including the other subs.
2. **Repo.** Open every file this sub will change. Match the neighbouring style the rules name.
3. **Steps.** Smallest diff. Name the sub steps this one `needs`, as already deployed.
4. **Scaffold.** Files, public APIs, data shapes. No speculative layers.
5. **Tests.** File paths and `describe` / `it` intent. The test plan holds the full cases.
6. **Deploy.** How this step deploys on its own, and how to revert it without reverting later steps. Use the repo's real deploy mechanism. Write `unknown` and an ambiguity if the repo does not say. When this sub changes an API, a schema, or a generated client, list that repo's regenerate commands in order under **Deploy**, and list the generated paths under **Files**. c360 is environment `./run.sh generate typescript`, then `./run.sh push database schema`, then hub `./run.sh open api regenerate`. Another repo uses the scripts recon opened. An unknown command is an ambiguity, not a guess.
7. **Ambiguities.** Blocking ones stop the file: report them to the parent instead of inventing a behaviour.

---

## Output

Return these blocks. The parent places them under `## Sub NN` in the master plan.

### Files

| Action | Path | Notes |
|--------|------|-------|
| change | | |

### Scaffold

### Deploy

- generate: commands in order, or none
- alone: flag, dormant route, additive, or yes
- requires deployed: none or step numbers
- revert: code rollback, or the recovery this repo needs
