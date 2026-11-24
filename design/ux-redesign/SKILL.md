---
name: ux-redesign
description: Steps back from a page, feature or user journey and proposes an incremental or radical redesign. Reviews the current UI against the project's own rules, existing evidence and established design systems, researches UX best practice, and proposes the design in ASCII with references and decisions to confirm, scaled to the size of the change. Use when the user runs /ux-redesign or /redesign, asks to "step back and reimagine", redesign or evaluate the UX of a page, feature or journey, or asks which UI or UX option is better.
agents:
  - cursor
---

# Redesign a page

- Propose first. Don't build the real change until the user accepts the proposal. Use Plan mode if it is available.
- Start incremental unless the developer asks for something more radical.
- Never invent or guess a reference.

## Scale the response to the change

Every response shows what changes in ASCII. Words alone rarely convey a design. Back design claims with research where it shapes the decision. For small changes, references are recommended rather than required. Only the depth changes:

| Size   | Examples                                                         | Response                                                                                                                                                                                  |
| ------ | ---------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Small  | One component or state, a copy change, "which option is better?" | A short answer: before and after ASCII of the part that changes, with enough of the page around it to place it. Pros, cons and a recommendation. References where they help. No template. |
| Medium | Several parts of one page                                        | The plan template, leaving out sections that don't apply.                                                                                                                                 |
| Large  | A new page, a whole page reimagined, a journey                   | The full workflow and template.                                                                                                                                                           |

- **Detail answers the question.** Draw the parts the decision depends on, and keep the rest rough or out.
- **Annotate where things are unclear.** That means behaviour, states and what happens after an action. Don't restate what the drawing already shows.
- **Pair each drawing with short text.** The drawing shows layout and relationships. The text gives rules, limits and edge cases.
- **Grow the response when the change grows.** If a small change turns out to affect other parts of the page, say so and move up a size.

Why: developers discussing a design drawn as a diagram talked more actively and recalled more detail than those given the same design as text ([Jolak et al., 2020](https://link.springer.com/article/10.1007/s10664-020-09835-6)). A prototype only needs the detail its question needs ([GOV.UK Service Manual](https://www.gov.uk/service-manual/design/making-prototypes)).

## Choose the approach: incremental or radical

Start incremental. Go radical only when the developer hints at it ("start again", "reimagine from scratch", "rethink the whole journey"), the page is new, or the evidence shows the current design can't be fixed in steps. If you're unsure, say which you'd choose and why, and ask.

|            | Incremental (default)                               | Radical                                                                      |
| ---------- | --------------------------------------------------- | ---------------------------------------------------------------------------- |
| When       | An existing page people already use                 | A new page, an explicit request, or a design with no coherent structure left |
| Start from | The current page and its biggest problems           | The jobs people come to do, ignoring the current layout                      |
| Output     | A ranked list of changes, each shippable on its own | A new design, and why small changes won't get there                          |
| Main risk  | Patching over a structural problem                  | Upsetting current users who know the old page                                |

**Incremental?** Read [references/incremental.md](references/incremental.md).
**Radical?** Read [references/radical.md](references/radical.md).

## Workflow

```
- [ ] 1. Understand what the page does today
- [ ] 2. Choose the approach, and read its reference file
- [ ] 3. Read the project's rules and domain language
- [ ] 4. Research
- [ ] 5. Design around the jobs people come to do
- [ ] 6. Write the plan
- [ ] 7. Ask questions, then revise
```

### 1. Understand what the page does today

- Read the route, page, components, state, hooks or services, and API calls. Follow the data back to the endpoint.
- Gather the evidence that already exists: analytics, support tickets, feedback, earlier research and known bugs. Ask the user what they have. If there is none, say so, and treat the plan's recommendations as hypotheses to test.
- If the user gave a live URL, look at it in the browser and take a screenshot.
- List every job the page does, and every state: loading, empty, error, partial data, no permission, feature turned off, different roles or account types, and long or very short content.
- Write down any constraints the user stated, word for word. They override anything you infer.

### 2. Choose the approach

Follow "Choose the approach" above, and read only the reference file for the approach you chose. State the choice and the reason at the top of the plan.

### 3. Read the project's rules and domain language

Find the project's conventions before forming opinions. Look for, and read where present:

- Agent guidance: `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/`, `.github/copilot-instructions.md`.
- Domain language: `CONTEXT.md`, a glossary, or domain docs under `docs/`. Use the project's terms for things, not your own.
- Rules that touch UI: copy and tone, spelling locale, page names, navigation, breadcrumbs, forms, dialogs, accessibility, routing and URL schema, i18n, architecture, and deprecated code to avoid.
- The design system or component library the project uses, and its docs.
- Access rules: which endpoints or data each kind of page may use (for example, admin-only APIs never called from customer-facing pages).

Weigh the project's component library and established design systems fairly. The library is what the product is built with and keeps it consistent, but it may have design failings. Systems such as the GOV.UK Design System, Carbon, Fluent 2 and Material are researched and tested, but were made for other products and audiences. Where they disagree, show both, give the evidence for each, and recommend one of: use the library as it is, improve the library component, or depart from it on this page with a stated reason.

Look for precedent before you invent anything. Find the page in the codebase that already does a similar job best, and reuse its components and layout where they hold up against the research.

If the project has no rules on a topic, say so, and base the decision on the research and WCAG 2.2 AA.

### 4. Research

- Do the research properly. Use web search for the specific pattern, such as balances, address books, account home pages, settings or preference centres. Generic advice is not enough.
- Prefer primary sources: Nielsen Norman Group, GOV.UK Design System and Service Manual, W3C WCAG and APG, Baymard Institute, Carbon, Fluent 2, Material, etc.
- Start from any `## References` sections in the project's rules. They hold sources already checked for that codebase.
- Consider who uses the product. Where the audience includes older people or less confident users, weigh research on older users, plain language and cognitive accessibility.
- Look at how strong products solve the same job, and at any external system the page mirrors.
- Cite only sources you opened in this session. State the specific finding, not just the topic.
- Say how close the source is to this case: its audience, its type of product and its method. Don't stretch a finding beyond what it tested.
- If you find no specific research, say so rather than citing something loosely related.

### 5. Design around the jobs people come to do

- Put the most common job first. Give each area one clear primary action.
- Keep it calm: no alarm words or red for normal states, and no repeating the same fact in a summary, a tab and a badge (unless the research calls for it).
- On overview pages, put related cards side by side and use the width on wide screens. Keep forms and running text to a readable width, about 75 characters a line, and start from a single column on small screens ([GOV.UK Design System](https://design-system.service.gov.uk/styles/layout/)).
- Status must stand out from the text around it, and not by colour alone.
- Design for the edges: long and very short content, no data, and many items.
- Respect what the product can and cannot do. If a job belongs to another system, link to it rather than rebuilding it.
- If the design needs data that no permitted endpoint returns, propose the endpoint and ask for its exact schema before building.
- When the project's rules settle something, such as how forms and dialogs behave, follow them. If the research disagrees with a rule, say so and propose a change to the rule.

### 6. Write the plan

**Small change?** Answer in chat as described under "Scale the response". No template.
**Medium or large change?** Read [references/plan-template.md](references/plan-template.md) and use it.

Draw every screen and state that changes in ASCII. Follow each drawing with short bullets that explain the decisions. Use mermaid only for component structure and data flow, never in place of a mock-up.

### 7. Ask questions, then revise

- Ask every open question. Use a structured question tool (such as `AskQuestion`) for discrete choices when one is available.
- When the user asks "should we do X?", give the pros and cons, cite research, and end with a clear recommendation.
- Push back, with reasons, when you think the current design or the user's idea is worse.
- When the user asks for a change, update the plan and its ASCII art. Don't just reply in chat.

## ASCII art

- Use plain ASCII in a `text` block: `+ - |` for boxes, `[ Button ]`, `( ) / (o)` for radios, `[ ] / [x]` for checkboxes, `v` for selects, `< Back`, `(Badge)`, `[icon]`.
- Use real, plausible content from the product's domain (Mrs Jane Smith, £20.00, 3 orders), not "Lorem ipsum" or "xxx".
- Keep it under about 80 characters wide and line the columns up.
- Draw mobile separately whenever the layout changes.
- Put a one-sentence plain description before each drawing, so it makes sense to someone using a screen reader.
- ASCII shows structure, order and flow. It can't settle visual hierarchy, spacing, colour or type. When the decision depends on those, recommend a throwaway prototype built with the project's components, or an annotated screenshot, and ask before building it.

## References

- Prefer a reference for each design claim that rests on research: a link, the publisher and the finding in one sentence. For small changes this is a recommendation, not a requirement.
- A claim without a reference is better than a wrong one.
- Cite the project's rule files as links (for example `[copy.mdc](.cursor/rules/copy.mdc)`) when a finding comes from them.
- If the research produces guidance that will outlast this page, propose a new or updated rule in the project's rules location (`.cursor/rules/`, `AGENTS.md` or `CLAUDE.md`) with a `## References` section in the same format.

## Copy

- Follow the project's copy rules and domain language first.
- Where it has none, address people as "you" and "your", never "the user", and name things the way the people using the product do.
- Say what people can do, briefly. Don't over-explain what an address or setting is for.
