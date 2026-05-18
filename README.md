# Cursor skills

Each target repo needs `.cursor/STRUCTURE.md` and `.cursor/CONTEXT.md`. Task brief + PM sign-off = source of truth.

## Install

```bash
npx skills@latest add eden-ecommerce/skills -a cursor --global --skill '*' -y
npx skills@latest add mattpocock/skills -a cursor --global
npx skills@latest add JuliusBrussee/caveman -a cursor --global
```

Choose **Global** when prompted. Then reload Cursor (`Ctrl+Shift+P` → **Developer: Reload Window**).

## Skills (reference)

| Invoke in Cursor | Purpose |
|------------------|---------|
| `/document-current-state` | PM/sales constraints; what ships today |
| `/document-database` | ER / joins from code |
| `/document-flow` | Sequence or flowchart from code |
| `/construct-plan` | Pre-code plan, scaffold, verify vs docs |
| `/construct-test-plan` | Manual QA checklist |
| `/execute-test-plan` | Run checklist; browser tab + MCP or manual |
| `/generate-changelog` | Deploy notes → `docs/releases/<version>.md` |

## Developer steps

| # | Where | What to run |
|---|--------|-------------|
| 1 | Ticket / notes | Paste raw task as received (`brief`) — no interpretation |
| 2 | **ChatGPT** or **Copilot** | [Task interrogation prompt](#task-interrogation-prompt) — replace `TASK_TITLE`, `REPORTED_BY`, `TASK_DESCRIPTION` |
| 3 | **PM** | Take model output → clarification + concerns (`refine`, `concerns`, `solutions`) → **written sign-off** (`feedback_pre`, `accept`) |
| 4 | **Cursor Plan** | As needed → `docs/feature/<task-slug>/`: **`/document-current-state`**, **`/document-database`**, **`/document-flow`** |
| 5 | **Cursor Plan** | **`/construct-plan`** — research, plan, scaffold, edge cases, verify vs docs |
| 6 | **Cursor Plan** | **`/grill-with-docs`** — one question at a time; update `.cursor/CONTEXT.md` until signed off |
| 7 | **Cursor Agent** | Implement from scaffold; run STRUCTURE **Gates** until green (`scaffold` → `refinement`) |
| 8 | **Cursor** | **`/construct-test-plan`** — QA checklist (functional, abuse, responsive / theme / UI) |
| 9 | **Cursor** + **Browser tab** | **`/execute-test-plan`** — run each row (Cursor browser + MCP, or manual table) |
| 10 | **PM** / peers | Peer review, staging demo, final feedback (`code_review`, `ux_feedback`, `feedback_post`) |
| 11 | **Cursor** | **`/generate-changelog`** — when repo ships `docs/releases/<version>.md` |
| 12 | Deploy | Production deploy; close task (`deploy`) |

## Task interrogation prompt

Copy the **entire** block into ChatGPT or Copilot (step 2).

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

## Links

- [skills CLI](https://github.com/vercel-labs/skills)
- [Cursor skills docs](https://cursor.com/docs/context/skills)
- [This repository](https://github.com/eden-ecommerce/skills)
