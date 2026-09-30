# Context — ubiquitous language

One glossary table: every domain noun gets exactly one row and one spelling. Every doc, rule, identifier, and UI label reuses that spelling — never two words for the same concept (this is what `../rules/naming.mdc`'s canonical-nouns line enforces day to day).

| Term | Meaning |
|---|---|
| Tenant | Workspace-level owner of the data set. Integer PK, table `tenants`. |
| Widget | *(placeholder — replace with the new project's first core noun and its exact, one-line meaning)* |

## How to fill this table

During intake Stage 2 "Features / entities" (`../SKILL.md`), every noun the user names becomes one row here, decided once, before any code references it. If the same concept later shows up under a second name anywhere (a variable, a column, a button label), that's a naming-law violation to fix, not a synonym to tolerate.

Keep the table short and load-bearing — a term earns a row when getting it wrong would cause a real bug or a confused reviewer, not for every noun in the brief.
