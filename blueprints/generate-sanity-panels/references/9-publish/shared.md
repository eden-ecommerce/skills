# Publish — shared

Stage 9. In: `draftPatch` + explicit user yes in chat.

## Process

1. Remind user of internal review they own (editorial, legal, merchandising)
2. Require explicit **yes** — not implied approval
3. HTTP publish with FIRST RUN credentials (never hardcoded):

```bash
python3 scripts/publish_sanity_document.py "<draft_doc_id>" --project-id "$NEXT_PUBLIC_SANITY_PROJECT_ID" --dataset "$NEXT_PUBLIC_SANITY_DATASET" --token "$SANITY_API_EDITOR_TOKEN"
```

Use `domainSnapshot.cms` project/dataset. Token from session only.

## Out

```json
{ "publishedId": "..." }
```

No publish without gate 9 approval + audit pass.
