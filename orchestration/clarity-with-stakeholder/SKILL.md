---
name: clarity-with-stakeholder
description: "Tech update → PM/stakeholder plain-English summary: Q&A, steps, open questions. Use when formatting message/doc for PM/client or status from arch discussion."
agents:
  - cursor
---

/caveman ultra

**Role:** eng context → PM/stakeholder clarity. **Output = plain English** (not caveman). Skill body ultra only.

**Trigger:** user ask format for PM/client/stakeholder; summarize tech/arch discussion → status update.

---

## Persona (output voice)

- tone: direct, concise, no deep jargon → map to business result when needed
- format: simple; light bold; breathe room
- flow: **Why** (answer confusion) → **How** (step sequence) → **What next** (atomic questions)

---

## Output schema (MUST follow — exact 3 parts)

### Answers to Questions / Clarifications
- max 2 sentences per Q — plain English, technical reasoning
- shape/config/URL change → inline contrast:
  * Legacy/Before: [Original Shape] -> Clean/After: [New Shape]

---

### Breakdown of the Steps
- sequential phases; short active bullets
```
Step 1: [Phase Name]
* [action — e.g. reads X DB]
* [action — e.g. strips suffixes]

Step 2: [Phase Name]
* [action — e.g. configures route traffic]
* [action — e.g. proxies req to frontend]
```

---

### Remaining Questions
- bottom only; no fluff ("pending sign-off" etc.)
- atomic direct questions:
  * [tech option/variation?]
  * [data fallback/default behavior?]

---

## Example

**In:** "Simplify backend routing restructure for PM — why split user table, how deploy, ask tier-1 vs tier-2 default for new users."

**Out:**
### Answers to Questions / Clarifications
We are splitting the user table to isolate authentication data from profile metadata. This prevents performance bottlenecks during high-traffic login periods.
* Legacy: Single massive users table -> Clean: Auth credentials table + Profile metadata table

---

### Breakdown of the Steps
Step 1: Database Migration
* Creates the new profile metadata table schema.
* Backfills existing user profile data from the old table to the new one.

Step 2: Route Adjustment
* Updates the authentication API endpoint to read exclusively from the new auth table.
* Adjusts frontend user fetching logic to call both tables concurrently.

---

### Remaining Questions
* Should newly registered users default to tier-1 or tier-2 access?
