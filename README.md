## Recommended (install first)

```bash
npx skills@latest add mattpocock/skills -a cursor --global
npx skills@latest add JuliusBrussee/caveman -a cursor --global
```

## Install skills

```bash
npx skills@latest add eden-ecommerce/skills -a cursor --global --skill '*' -y
```

Or one skill by name:

```bash
npx skills@latest add eden-ecommerce/skills --skill implement -a cursor --global -y
```

**Always choose Global** when prompted for installation scope.

## Setup (Windows)

1. Open **Git Bash**
2. Run the commands above
3. Confirm skills exist under `C:\Users\<USERNAME>\.agents\skills\` (and/or `C:\Users\<USERNAME>\.cursor\skills\`)
4. **Restart Cursor** — `Ctrl+Shift+P` → **Developer: Reload Window**
5. **Cursor Settings** — `Ctrl+Shift+J` → **Rules and Skills**

**Not showing in Cursor?** Run the same `npx skills add` from **WSL** and check `~/.agents/skills/` and `~/.cursor/skills/` in your WSL home.

# Cursor skills

Agent skills. Each project still needs `.cursor/CONTEXT.md` and `.cursor/STRUCTURE.md` — skills read those for gates and conventions.

Treat the **task brief** and **written PM or stakeholder feedback** as the source of truth at each gate. Do not skip a stage that requires sign-off.

## Task workflow

Work moves between **ChatGPT or Copilot**, **PM or stakeholders**, and **Cursor**. Stage keys below match the lifecycle table.

### ChatGPT or Copilot plus PM (early)

- **`brief`** — Enter the task exactly as the reporter gave it; no interpretation yet.
- **`refine`** — Use the [Task interrogation prompt](#task-interrogation-prompt-chatgpt) below; take the generated questions to the project team.
- **`concerns`** — List data, performance, and research concerns; propose mitigations and edge cases per concern.
- **`solutions`** — Capture the agreed solution as short bullets the team accepts.
- **`feedback_pre`** — Get written sign-off on that solution from PM or stakeholders.
- **`accept`** — Record that the solution is accepted (ticket note, ADR, or reply thread).

### Cursor Plan mode (research and planning)

- Create **`docs/feature/<task-slug>/`** in the target repo (unless `.cursor/STRUCTURE.md` defines another path).
- Run documentation skills as needed: **`documentation/document-current-state`**, **`documentation/document-database`**, **`documentation/document-flow`** — one artefact per concern (current state, ER-style diagram, control-flow diagram).
- Run **`orchestration/construct-plan`** for a research-backed plan, scaffold, `/grill-with-docs`, edge-case pass, and verification against those docs **before** large implementation work.

### PM checkpoint

- Bring Cursor outputs, research markdown, and model-generated question lists back to PM.
- If scope shifted, run the interrogation prompt again and update sign-off.

### Cursor execution (build and ship)

- Continue with **`/grill-with-docs`** and keep **`.cursor/CONTEXT.md`** aligned with agreed terminology.
- Follow the remaining stages from **`scaffold`** through **`deploy`**: structure, prototype, UX feedback, refinement, code review, testing on staging, final stakeholder feedback, production deploy.
- For **`testing`**: **`test/construct-test-plan`** (checklist) then **`test/execute-test-plan`** (run rows, browser MCP or manual table).
- Before **`deploy`**: **`documentation/generate-changelog`** when your repo uses release notes under `docs/releases/`.

## Task Lifecycle Stages

| # | Stage Key | Display Name | Guidance | AI |
|---|-----------|--------------|----------|-----|
| 1 | `brief` | Task Brief | Enter the task as received from the reporter — no interpretation yet | — |
| 2 | `refine` | Refine Task | Use AI to generate critical clarification questions for the project team | ChatGPT / Copilot |
| 3 | `concerns` | Outline Concerns | List data, performance, and research concerns. Propose solutions and edge cases for each | ChatGPT / Copilot |
| 4 | `solutions` | Bullet Point Solutions | Document the accepted solution approach in bullet points | ChatGPT / Copilot |
| 5 | `feedback_pre` | Feedback | Get written sign-off on the proposed solution from the project team | — |
| 6 | `accept` | Accept Solution | Confirm the solution is accepted and record the decision | — |
| 7 | `scaffold` | Scaffold Structure | Plan the file, component, and database structure before writing code | — |
| 8 | `prototype` | Quick Prototype | Build a working prototype focused on the core logic | — |
| 9 | `ux_feedback` | UX Feedback | Demo the prototype and capture UX feedback | — |
| 10 | `refinement` | Refinement | Polish the implementation based on UX feedback | — |
| 11 | `code_review` | Code Review | Submit for peer review and address comments | — |
| 12 | `testing` | Testing | Deploy to staging and run through the QA checklist | — |
| 13 | `feedback_post` | Feedback | Final stakeholder feedback on staging | — |
| 14 | `deploy` | Deploy | Deploy to production and mark the task complete | — |

### Task interrogation prompt (ChatGPT)

Copy the **entire** block below into ChatGPT or Copilot. Replace `TASK_TITLE`, `REPORTED_BY`, and `TASK_DESCRIPTION` with your ticket details. Use the reply in lifecycle stages **`refine`** and **`concerns`**.

````text
You are a principal software engineer reviewing a development task BEFORE implementation begins.

Your responsibility is to interrogate the task for ambiguity, hidden assumptions, missing requirements, business logic gaps, operational risks, and technical unknowns.

DO NOT solve the task.
DO NOT write implementation details.
DO NOT make assumptions unless explicitly stated.

Your objective is to generate a concise, structured list of clarification questions and concerns the developer should raise before coding begins.

--------------------------------------------------
TASK TITLE:
TASK_TITLE

REPORTED BY:
REPORTED_BY

TASK DESCRIPTION:
TASK_DESCRIPTION
--------------------------------------------------

Analyse the task critically.

Assume the ticket is incomplete unless proven otherwise.

Look for:
- vague wording
- undefined business behaviour
- missing scope boundaries
- unclear ownership
- hidden operational impact
- migration concerns
- rollout risks
- edge cases
- permissions/access ambiguity
- missing acceptance criteria
- backwards compatibility risks
- unclear failure behaviour
- dependencies on external systems or teams

IMPORTANT OUTPUT RULES:
- Questions MUST be concise and direct
- Group questions by topic
- Prefer bullet points over explanations
- Avoid generic filler commentary
- Highlight high-risk unknowns
- Prioritise questions that block implementation
- Focus on questions a developer would actually ask a PM/stakeholder
- Every question should uncover a meaningful ambiguity or risk

Return the response inside a SINGLE markdown code block.

Use EXACTLY this structure:

```md
## Blocking Questions
### Business Logic
- Question
- Question

### Scope
- Question
- Question

### User Experience
- Question
- Question

### Permissions / Roles
- Question
- Question

### Data & Migration
- Question
- Question

### External Dependencies
- Question
- Question

### Rollout / Operations
- Question
- Question

## Technical Concerns
### API / Backend
- Concern
- Concern

### Performance
- Concern
- Concern

### Validation & Error Handling
- Concern
- Concern

### Edge Cases
- Concern
- Concern

### Security
- Concern
- Concern

### Observability
- Concern
- Concern

### Backwards Compatibility
- Concern
- Concern

## Suggested Acceptance Criteria
- Clear testable outcome
- Clear testable outcome
- Clear testable outcome

## Delivery Risks
- Risk
- Risk

## Recommended Next Actions
- Action
- Action
```

ADDITIONAL RULES:
- If a section has no meaningful items, omit the subsection entirely
- Do not generate placeholder questions
- Avoid overexplaining
- Avoid repeating the task description
- Prefer specific questions over broad questions
- If something could be interpreted multiple ways, explicitly question it
- If the task appears deceptively simple, identify hidden complexity
````



## Recommended skill order

Typical feature task after PM sign-off (use only the documentation skills you need):

1. **document-current-state** — business constraints / what ships today (`docs/feature/<task-slug>/`)
2. **document-database** — ER / joins from code (STRUCTURE-approved DB commands only)
3. **document-flow** — sequence or flowchart from code + user flow
4. **construct-plan** — plan, scaffold, `/grill-with-docs`, edge cases, verify vs research docs; then implement from scaffold per STRUCTURE gates
5. **construct-test-plan** — full manual QA checklist (functional, abuse, responsive / theme / overflow / deep links)
6. **Build in Cursor** — implement from accepted scaffold; match patterns in `.cursor/STRUCTURE.md`
7. **execute-test-plan** — run every checklist row (browser MCP or manual); severity + proposed fix + owner
8. **generate-changelog** — deployment notes into `docs/releases/<version>.md` when shipping

## Skills

| Skill | Folder | What it does |
|-------|--------|----------------|
| **document-current-state** | `documentation/document-current-state` | PM/sales-facing constraints; optional vault MCP per STRUCTURE |
| **document-database** | `documentation/document-database` | Trace code to tables/joins; ER mermaid; DB truth via approved commands |
| **document-flow** | `documentation/document-flow` | Control-flow sequence or activity mermaid from code |
| **generate-changelog** | `documentation/generate-changelog` | Hub-style deploy notes from `git diff` / `git log` → `docs/releases/<version>.md` |
| **construct-plan** | `orchestration/construct-plan` | 7-phase pre-code workflow; research folder; grill-with-docs; scaffold; verify; gates + handoff |
| **construct-test-plan** | `test/construct-test-plan` | Manual QA plan: matrix, personas, abuse, regression, UI/viewport rows, browser-ready steps |
| **execute-test-plan** | `test/execute-test-plan` | Execute plan rows: Cursor browser tab + MCP or manual; pass/fail, severity, proposed fix, owner |

## Links

- [skills CLI](https://github.com/vercel-labs/skills)
- [Cursor skills docs](https://cursor.com/docs/context/skills)
- [This repository](https://github.com/eden-ecommerce/skills)
