# Publish — shared

Stage 9. In: `draftPatch` + explicit user yes in chat.

## Process

1. Remind user of internal review they own (editorial, legal, merchandising)
2. Require explicit **yes** — not implied approval
3. MCP publish:

```bash
manus-mcp-cli tool call publish_documents --server sanity --input '{
  "ids": ["<draft_doc_id>"],
  "resource": { "projectId": "'"$NEXT_PUBLIC_SANITY_PROJECT_ID"'", "dataset": "'"$NEXT_PUBLIC_SANITY_DATASET"'" }
}'
```

Prefer `domainSnapshot.cms` project/dataset (from env at Definition). Override when not Eden.

## Out

```json
{ "publishedId": "..." }
```

No publish without gate 9 approval + audit pass.
