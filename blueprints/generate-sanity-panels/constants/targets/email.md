# Email target

| Field | Value |
|---|---|
| id | `email` |
| sanityDoc | tenant-specific or template id from brief |
| seed identifier | campaign name or template slug |
| seed surface | Campaign landing URL from brief if defined — **no links back** |
| panelField | slice / block array per tenant schema |
| algolia | optional — multi-SKU commerce emails |
| galleryKey | from `domainSnapshot.urls` |
| previewType | `email` or tenant value |
| editorRole | email marketing editor |

## Requirements

Narrative brief enough — no hard IDs.

## Spine

See `templates/email.md`.

## packMode stub

Multi-SKU listicle emails: score relevance in Research Findings; no separate pack FSM in v1.
