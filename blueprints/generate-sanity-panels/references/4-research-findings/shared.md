# Research Findings — shared

Stage 4. Orchestrator spawns parallel subagents.

## In

- `topics[]`, `brief`, `domainSnapshot`
- `sourcePolicy` from topics artifact when present

## Parallel spawn

1. **One subagent per topic** — grounded research for that topic only
2. **One Algolia subagent** when `domainSnapshot.catalogue` has Algolia — see `algolia.md`

Orchestrator merges outputs. Subagents do not see each other's full context.

## Topic agent out (per topic)

```json
{
  "topic": "...",
  "bullets": ["..."],
  "quotes": [{ "text": "...", "source": "..." }],
  "faqCandidates": [
    { "question": "...", "theme": "...", "source": "Goodreads reviews | Eden Q&A | ..." }
  ],
  "mediaUrls": ["..."],
  "confidence": "high|mid|low",
  "aPlusRelevance": "why this finding belongs in the content strip (not live page chrome)"
}
```

Every finding must state `aPlusRelevance` (content-strip relevance). Drop or rewrite topics that only restate buy-box / spec chrome.

FAQ topic: include `faqCandidates[]` with `source` provenance — Stage 5 synthesizes answers from findings only (no invented ratings).

## Merged out

```json
{
  "findings": [ ... ],
  "products": [ ... ]
}
```

`products[]` from Algolia subagent only — compact cards (see `algolia.md`).

**Debug only:** raw slices may be written to `findings-raw/` on disk. Orchestrator never reloads after merge — use `researchFindings.json` only.

Never pass raw Algolia JSON to orchestrator.

Gate: user approves findings + product list (incl. stock/fulfillment for selection).
