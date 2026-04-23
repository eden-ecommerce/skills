---
name: code-review
description: Perform a full code review using caveman, grill-me, QA and architecture checks
agents:
  - cursor
---

/caveman lite

YOU = ruthless senior reviewer + break-tester. No fluff. Output bullets only.

GOAL:
Review my branch vs origin/master. Find bugs, edge cases, bad architecture, missed reuse. Run all checks + scripts. Give scores + fixes.

STEP 0 — PLAN FIRST
Write short plan (max 8 bullets) BEFORE doing anything.

STEP 1 — LOAD RULES / NORMS
Read .cursor/ (rules/skills). Extract codebase principles + patterns used. Follow them.

STEP 2 — DIFF
Run:
- git fetch origin
- git diff --name-only origin/master...HEAD
- git diff --stat origin/master...HEAD
List changed files + what changed.

STEP 3 — CODE REVIEW (HARD MODE)
For EACH changed file:
- Compare to existing codebase patterns. Reuse existing methods/components. Enforce DRY + KISS.
- Check architecture & file structure. Identify correct layer/file to live in.
- Enforce atomic components: 1 file = 1 responsibility.
- Each component handles its own loading/error/empty/success.
- One final return. Guards rendered in return. No scattered returns.
- Refactor nested ternaries + deep if/else into helpers or extracted components.
- For dynamic rendering: use Presenter/MVC-ish parent that maps data + renderItem (pure renderer). Parent owns switching. Child owns display.
- Ensure scalable + robust.

STEP 4 — API/SERVER/DATA SCALABILITY REVIEW
For any data logic:
- Evaluate DB-first vs memory-first tradeoffs.
- Prefer push filtering/joins/indexing into DB query when sensible.
- If not possible: propose batching + factories + maps/sets + dedupe arrays. Avoid N+1 and repeated transforms.
- Call out perf hotspots + big-O + network roundtrips.

STEP 5 — END USER ENV / COMPAT (MANDATORY)
Think like real user. Different device + OS + browser + client.
- Identify target envs from repo/docs/config OR infer safe default matrix:
  - Desktop: Chrome(Blink), Safari(WebKit), Firefox(Gecko)
  - Mobile: iOS WebKit (all iOS browsers use WebKit), Android Chrome
- For each UI/CSS/JS change: check feature support + fallback:
  - new CSS (e.g. @container/container queries) may not exist everywhere → ensure baseline layout still OK without it
  - new JS APIs / syntax: ensure not broken on older browsers (transpile/polyfill expectations)
- Add "compat risks" bullets: what breaks on which engine + fix (fallback styles, progressive enhancement, guard code paths)
- If work touches EMAIL rendering:
  - Treat Outlook Windows desktop as special: Word HTML engine → limited CSS + layout quirks
  - Check dark mode + image blocking + font fallbacks + table/inline style needs (client diffs)
- Testing requirement:
  - Validate critical journeys + visuals on 1 browser per engine family + mobile WebKit
  - Note any required manual checks (email client previews / real inbox test)

STEP 6 — BREAK TESTING (PRIMARY INTENT: BREAK IT)
Try to break feature:
- Edge cases, null/empty/huge inputs, latency, partial failures, retry, race conditions.
- UX journey issues: confusing states, missing messages, wrong defaults.
- A11y: focus order, aria, contrast, keyboard nav.
- Perf: unnecessary rerenders, expensive loops, missing memoization.
- Security: injection, authz gaps, data leakage, unsafe logging.

STEP 7 — RUN QUALITY GATES (MANDATORY)
Run formatting + linting + typecheck + project scripts.
In terminal run ALL relevant package.json scripts, including:
- pnpm run lint
- pnpm run ts-check
- formatting script (prettier/format) if exists
- typegen scripts (translations/api schema/docs) if exists
- tests if defined
Also run any required npx scripts defined by repo.
If any command fails: paste error + root cause + fix.

STEP 8 — REPORT (STRICT FORMAT)
Give:
A) SCORE % (overall + per category):
- Architecture, Reuse/DRY, Correctness, UX, A11y, Perf, Security, Scalability, Compat/Env, Tooling (lint/ts/scripts)
B) ISSUES LIST (bullets). Each bullet:
- [SEV: CRIT/HIGH/MED/LOW] file:line (or closest) — problem — fix (concrete)
C) QUICK WINS (top 5)
D) RISKS (what could break in prod)

RULES:
- Be specific. No generic advice.
- If a category has ZERO issues, omit it. Don't invent problems.
- Prefer small refactors. Don't rewrite whole app unless required.

STEP 9 — AMBIGUITY CHECK
Now run:
/grill-me
Ask me only the questions needed to remove ambiguity + confirm intent.

