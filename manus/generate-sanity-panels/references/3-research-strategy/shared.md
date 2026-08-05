# Research Strategy — shared

Stage 3. In: `personas`, `brief`, `domain` from artifacts. Out: `topics.json`

## Process

- Generate research topics from personas + `{brief}`
- 4–10 topics. Each: `topic`, `rationale`, `priority` (high|mid|low)
- Topics must be answerable — not vague "learn more"
- Include **FAQ / customer-question** topic when brief supports it — mine review themes, "people also ask", and trusted Q&A from discoverable sources (marketplaces, Goodreads, publisher pages, on-site reviews). Do not prescribe one retailer as layout model.
- No web fetch here — topics only

## Out

```json
{ "topics": [ { "topic": "...", "rationale": "...", "priority": "high" } ] }
```

Gate: user approves topic list or trims.
