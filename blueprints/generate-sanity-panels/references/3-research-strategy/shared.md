# Research Strategy — shared

Stage 3. In: `personas`, `brief`, `domain`, `target` from artifacts. Out: `topics.json`

## Process

- Generate research topics from personas + `{brief}` + **target surface type**
- 4–10 topics. Each: `topic`, `rationale`, `priority` (high|mid|low)
- Topics must be answerable — not vague "learn more"
- Include **FAQ / audience-question** topic when brief supports — mine review themes, Q&A, trusted sources. Do not prescribe one retailer as layout model.
- Include **layout / module best practices** topic (high priority when brief is thin):
  - Agent web-researches how strong surfaces in **this category + target type** structure content (product strip, long-form article, email modules)
  - Findings inform Stage 5 composition — skill does **not** hardcode retailer layouts; agent discovers what works
- No web fetch here — topics only

## Out

```json
{ "topics": [ { "topic": "...", "rationale": "...", "priority": "high" } ] }
```

Gate: user approves topic list or trims.
