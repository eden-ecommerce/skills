# Email target

| Field | Value |
|---|---|
| id | `email` |
| sanityDoc | tenant-specific or template id from brief |
| identifier | campaign name or template slug |
| panelField | slice / block array per tenant schema |
| algolia | optional — multi-SKU commerce emails |
| galleryKey | from `domainSnapshot.urls` |
| previewType | `email` or tenant value |
| editorRole | email marketing editor |

## Requirements

None beyond the shared outline (`target`, `brief`, `domain`). Narrative brief is enough — no hard IDs.

## Spine default

See `templates/email.md`.

## packMode stub

Multi-SKU listicle-commerce email may need several products. Score relevance in Research Findings; no separate pack FSM in v1.
