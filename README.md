# Cursor skills

Each target repo needs `.cursor/STRUCTURE.md` and `.cursor/CONTEXT.md`. Task brief + PM sign-off = source of truth.

## Install

```bash
npx skills@latest add eden-ecommerce/skills -a cursor --global --skill '*' -y
npx skills@latest add mattpocock/skills -a cursor --global --skill '*' -y
npx skills@latest add JuliusBrussee/caveman -a cursor --global --skill '*' -y
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

| Step | Where | What to run |
|---|--------|-------------|
| 1 | **Slack List** | Paste raw task as received (`brief`) — no interpretation |
| 2 | **ChatGPT** | [Task interrogation prompt](#task-interrogation-prompt) — replace `TASK_TITLE`, `REPORTED_BY`, `TASK_DESCRIPTION` |
| 3 | **Slack List Thread** | Take model output → clarification + concerns (`refine`, `concerns`, `solutions`) → **written sign-off** (`feedback_pre`, `accept`) |
| 4 | **Cursor Plan** | As needed → `docs/task/<task-slug>/`: **`/document-current-state`**, **`/document-database`**, **`/document-flow`** |
| 5 | **Cursor Plan** | **`/construct-plan`** — research, plan, scaffold, edge cases, verify vs docs |
| 6 | **Cursor Plan** | **`/grill-with-docs`** — one question at a time; update `.cursor/CONTEXT.md` until signed off |
| 7 | **Cursor Agent** | Implement from scaffold; run STRUCTURE **Gates** until green (`scaffold` → `refinement`) |
| 8 | **Cursor Plan** | **`/construct-test-plan`** — QA checklist (functional, abuse, responsive / theme / UI) |
| 9 | **Cursor Agent** + **Browser tab** | **`/execute-test-plan`** — run each row (Cursor browser + MCP, or manual table) |
| 10 | **Slack List Thread** | Peer review, staging demo, final feedback (`code_review`, `ux_feedback`, `feedback_post`) |
| 11 | **Cursor Agent** | **`/generate-changelog`** — when repo ships `docs/releases/<version>.md` |
| 12 | **Deploy** | Production deploy; close task (`deploy`) |

## Task interrogation prompt

Copy the **entire** block into ChatGPT (step 2).

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

## Example AGENTS.md file (stored in root repository directory)

```
Context:
- you MUST use the /caveman full skill
- you MUST only run project script commands using pnpm in the correct docker container
- all styling implemented with tailwindcss - utilise packages like tailwind-merge and tailwind-variants
- all network requests MUST be handled using react query hook files
- consider page performance when constructing component hierarchy identifying component boundaries and verifying tradeoffs between server/client and partial prerendering with Suspense
- render all icons using LucideIcons pnpm package

Coding Standards:
- never use any or unknown you MUST always infer types from a method result or a generate api sdk/types or package types
- be strict when deciding react hook usage - use callbacks are generally unnecessary since this is due to a handler method being out of scope, use timeouts can produce inconsistent behaviour utilise awaited promises, use effects can produce multiple component or chain renders, use memo should be utilised for performance so should only be added to data that will not change
- SOLID - new components should be implemented using the SOLID and atomicity principles, with each component handling one area of concern
- methods added should be unit testable with one measurable outcome
- dynamic data with variations in keys should be handled with an extendable switch method with methods for each handler method - using exhaustive if else check validation with an assertNever() check
- KISS (keep it stupid simple) - keep code change minimal and concise do not add bloat with excess logic and unnecessary casting/validation
- DRY - research the codebase and determine where existing Presenter components and structures can be reused

File Structure:
- hooks (implement hooks using react query package with logic separate into getKey, getOptions, server fetchMethod, client useHook calls fetchMethod)
- app (nextjs route navigation and path using file structure, page entry server logic)
- components (localised component file structure with sub components grouped into hierarchical directories ie forms/CreateUserForm/sections/BasicSection/ and then each section has files for separation of concerns ui rendering, schema zod validation, hook for partial submissions)
- data (server actions files with server side data fetching structure data/User/CreateUser with each model having a dal dto dpo file following a OOP class structure - specifically for server)
```

## Cursor Plan Mode Steps

```
1. Start /caveman full
2. Plan Context with Git Diff (high model - Sonnet 4.5 medium thinking disabled)
   a. Scope out task taking in to consideration the users changes using git diff command
   b. Propose a component hierarchy - and make sure to utilise existing components in the project or if a new reusable Presenter component needs to be created
   c. Critique proposed task plan and hierarchy - taking the following issues into condideration; user journey edge cases, data validation, component boundaries for page performance
   d. Propose a QA testing plan for the user to follow
3. Manual Revise Plan with Grill Me
   a. use the /grill-me-with-docs skill to question the user and remove amiguity from the task scope
4. Implement (auto efficiency model - Composer 2.5)
   a. create a new worktree off of the current branch to isolate changes made
   b. stick to the accepted plan and begin code implementation
   c. once implementation is complete test changes using lint and formatting scripts in package.json
5. Manual User Review
   b. follow the QA testing plan and utilise the /grill-me skill to gain important and scoped feedback to the changes made
   c. work through and stage git changes made when feature has been successfully implemented and verified by the user manually - ensure secrets are protected using .gitignore
6. Feedback Loop (auto efficiency model - Composer 2.5)
   a. maintain our project CONTEXT.md file with ubiquitous language terminology and concepts as we develop new features - ensure no secrets are included in .md files
7. Documentation
   a. ask the user whether you should generate a new feature document - if verified manually by the user utilise the skills in /.claude/skills/documentation/* to create visual diagrams mapping user/logic flow and database/class entity relationships
```
