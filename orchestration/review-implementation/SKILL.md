---
name: review-implementation
description: "Post-build review of one sub-plan diff. Scope, repo rules, gates, secrets, and a ponytail review. Use from implement-plan after a sub builds, or on its own before merge-plan."
agents:
  - cursor
---

**No auto-fix** unless the caller is implement-plan or the user asks for the refactors.

**Input:** that sub's `## Sub` section and `git diff` for the files in its Files table. Creep is any file not in that table and not required by a named repo rule.

**Bind:** read the rules list on the sub-plan Repo row before judging the diff. Gates come from that row. Do not assume `pnpm lint`.

---

## Checks

1. **Ponytail.** Follow `/ponytail-review` on this diff. One line per finding: `L<n>: <tag> <what>. <replacement>.` Tags: delete, stdlib, native, yagni, shrink. End with `net: -<N> lines possible.` or `Lean already. Ship.`
2. **Scope.** Every changed file is in the Files table, or required by a named repo rule. Name any other file as creep.
3. **Rules.** Check the diff against each file in the rules list. One line per break: rule file, the break, the fix.
4. **Gates.** Run the repo gate commands. Record pass or fail with the command.
5. **Secrets.** Scan the diff for tokens, passwords, and credential literals.
6. **Tests.** Automated rows in the test plan exist. Manual rows stay unticked.

---

## Output

```md
# Review — {step}-{repo}-{task}

## Ponytail Review

## Scope

- [ ] matches the sub-plan
- creep:

## Rules

| rule | break | fix |
|------|-------|-----|

## Gates

| command | result |
|---------|--------|

## Security

- secrets: none found

## Tests

- automated present:
- manual still open:

## Required Refactors
```

A failing gate or an open required refactor blocks the next sub. implement-plan applies the refactors. A standalone run lists them and stops.
