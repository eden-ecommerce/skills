---
name: code-review
description: Full code review — caveman lite report tone, grill-me, QA, architecture
agents:
  - cursor
---

Tone: **caveman lite** — no filler/hedging; articles OK where clarity wins. Final report = bullets only in scored sections.

Role: senior reviewer + break-tester. Ruthless.

Goal: Diff vs `origin/master`. Bugs, edges, weak architecture, missed reuse. Run gates. Scores + fixes.

**STEP 0 — Plan**  
Max 8 bullets before other work.

**STEP 1 — Rules + context**  
Read `.cursor/` (rules, skills). Read **`docs/**/*.md`** — principles, patterns, glossary. Apply what lands.

**STEP 2 — Diff**  
`git fetch origin`. Then `git diff --name-only origin/master...HEAD` + `git diff --stat origin/master...HEAD`. Changed files + what moved.

**STEP 3 — Names + comment strip**  
Do before deep logic pass.

- **Comments:** Kill noise (repeats code, stale). Names carry intent — comment only *why*, weird invariant, intentional hack, tradeoff. Match comment style same folder already uses.
- **Symbols:** vars, fns, classes, types, hooks — name = job reader sees without hunting. Weak name → rename.
- **Conventions:** Match neighbors — same file, same layer: camelCase vs PascalCase, prefixes (`use`, `handle`, `is`), suffix patterns (`Props`, `Result`). Don’t invent new convention unless file already shifting.

Same pass: rename + delete redundant comment. Don’t leave orphan comments after rename.

**STEP 4 — Code review (hard)**  
Per changed file:

- Patterns match repo; reuse > new abstraction. DRY, KISS.
- Layer + file placement correct.
- Atomic files; one main responsibility.
- Component owns loading / error / empty / success where pattern exists.
- One main return path; guards in render; scattered returns only if repo consistent.
- Nested ternary / deep if-else → helpers or small components when readability wins.
- Dynamic lists: parent owns data + branching; child pure renderer if that’s local style.

**STEP 5 — API / server / scale**  
Data paths: DB-first vs memory; filters/joins/indexes in query when sane. Else: batching, maps/sets, dedup, N+1. Big-O, hot paths, extra roundtrips.

**STEP 6 — Real user / compat**  
Devices, OS, browsers. Targets from docs or default matrix (Chrome/Blink, Safari/WebKit, Firefox/Gecko; mobile WebKit; Android Chrome). UI/CSS/JS: feature gaps, progressive enhancement, polyfill expectations. Compat-risk bullets. Email/HTML: Outlook desktop harsh; dark mode, images, fonts, tables. Critical paths + mobile WebKit; manual checks where needed.

**STEP 7 — Break test**  
Null, empty, huge input, latency, partial failure, retry, race. UX confusion, defaults. A11y: focus, aria, contrast, keyboard. Perf: rerenders, hot loops, memo. Security: injection, authz, leakage, unsafe logs.

**STEP 8 — Gates**  
Format, lint, typecheck, project scripts (`pnpm run lint`, `pnpm run ts-check`, prettier, typegen, tests, doc’d `npx`). Fail → quote error, root cause, fix.

**STEP 9 — Report (strict)**  

- **A) Scores (%)** — Overall + Architecture, Reuse/DRY, Correctness, UX, A11y, Perf, Security, Scalability, Compat/Env, Tooling.
- **B) Issues** — `[SEV: CRIT|HIGH|MED|LOW] file:line — problem — fix`
- **C) Quick wins** — Top five.
- **D) Risks** — Prod failure modes.

Rules: Specific; skip empty categories; no invented issues; small refactors preferred.

**STEP 10 — Ambiguity**  
Run `/grill-me`; questions only where intent unclear.
