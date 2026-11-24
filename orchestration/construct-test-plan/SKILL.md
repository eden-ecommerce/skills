---
name: construct-test-plan
description: "Test design for one sub-plan, before Build. Edge cases, security cases, automated specs, and a manual checklist. Use from construct-master-plan, or when a test plan is missing."
agents:
  - cursor
---

**No code.** The Tests table for one sub, inside the master plan. Specs describe the plan, not the current implementation.

**Input:** the sub's matrix rows and the master **Edge Cases** table.

**Do not** read the implementation diff or production files written for this task. Do not write `test-plans/`.

---

## Steps

1. **Edge cases.** Take every master **Edge Cases** row this sub owns. Add cases the matrix missed: empty input, boundaries, auth failure, wrong owner, illegal state, race, double submit, refresh, back navigation, timeout, partial failure.
2. **Security.** Add abuse cases from OWASP WSTG for the controls in the master **Security** section. Each case names a WSTG id and the matrix row it proves, or `extra` when the matrix has no row.
3. **Automated specs.** File path, `describe` / `it`, assertion intent, red-first. No production code and no implementation hints.
4. **Manual checklist.** The clicks a person runs after Build. Columns: step_id, action, expected, pass.

---

## Output

Return one table. The parent places it under that sub's Tests heading. Do not write a file.

| # | edge | wstg | check | expected |
|---|------|------|-------|----------|
| 1 | 1 | WSTG-INPV-01 | automated or manual | |
