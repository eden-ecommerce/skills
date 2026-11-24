# Plan template

Use this for medium and large changes. Leave out sections that don't apply.

Contents: review of the current page, proposed design, options considered,
structure and data, files, copy, decisions to confirm, how we'll know it
worked, verification, references.

````markdown
# {Page}: review and redesign

## 1. Review of the current page

For a new page, review what exists around it instead: the pages it links to and
from, what it replaces, and the precedent it should follow.

Link to the page file. Group the findings, each one a bold lead and a sentence:

### Evidence

What data exists and what it shows, or that there is none.

### Bugs you can see on the page

### Copy and naming (against the project's rules)

### UI best practice

### Accessibility

### Form best practice (if there is a form)

### Architecture and deprecated code

## 2. Proposed design

**Approach:** incremental or radical, and why.

### Incremental: changes, ranked by impact (incremental only)

Each change with before and after ASCII, and why it ranks where it does.

### The organising idea (radical only)

One or two sentences.

### Desktop: `/{route}`

One sentence describing the layout, for anyone who can't see the drawing.

```text
+--------------------------------------------------------------------------+
| Page title                                           [ Primary action ]  |
| Subtitle giving context                                                  |
+--------------------------------------------------------------------------+
  +----------------------------------+  +----------------------------------+
  | [icon] Card title     [ Action ] |  | [icon] Card title     [ Action ] |
  | ...                              |  | ...                              |
  +----------------------------------+  +----------------------------------+
```

- Why each area is where it is, and what each action does.

### Mobile (one column)

### Dialogs and sub-pages

### Other states (loading, empty, error, no permission)

### Transition for current users (radical only)

How current users will be warned, told what changed and why, and heard. If
switching back to the old design is worth offering, say why it's practical and
needed here. Otherwise leave it out.

## 3. Options considered (if there was a real choice)

| Option | Pros | Cons |
Then: **Recommendation:** … because … (cite references).

## 4. Structure and data

Mermaid component tree and data flow. Name the hooks, services and endpoints,
and confirm each one is permitted for this page.

## 5. Files

New, changed and deleted files, routes, navigation entries, and any URL schema
or routing docs to update.

## 6. Copy

Keys grouped by concept, not by page. Reuse existing keys first. Follow the
project's copy, tone and spelling rules. If the project is translated, add keys
to every locale, then stop and ask the user to run any type or key generation
step before linting.

## 7. Decisions to confirm

## 8. How we'll know it worked

The measures of success, and a short plan for testing with users: who to test
with, the tasks to give them, and the questions the test should answer.

## 9. Verification

The project's own typecheck, lint and test commands (from its rules, README or
package scripts), plus the screens to check by hand: mobile, wide, 400% zoom,
200% text resize, increased text spacing, keyboard only, a screen reader, and
long content.

## References

- [Title](url) (Publisher): the finding that shaped this design, in one sentence.
````
