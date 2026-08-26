# Draft — Sanity HTTP

Sanity I/O is HTTP scripts only. Project id, dataset, and token come from FIRST RUN — pass on every CLI call. Never hardcode. Never use `manus-mcp-cli`.

Values: `domainSnapshot.cms.projectId` / `dataset` plus session token (`SANITY_API_EDITOR_TOKEN`).

## Auth

| CLI flag | Env var | Use |
|---|---|---|
| `--project-id` | `NEXT_PUBLIC_SANITY_PROJECT_ID` | Project |
| `--dataset` | `NEXT_PUBLIC_SANITY_DATASET` | Dataset |
| `--token` | `SANITY_API_EDITOR_TOKEN` | Editor token — GROQ, draft patch, publish, asset upload |

## Query document

```bash
python3 scripts/get_sanity_document.py --product-id "<ID>" --project-id "$NEXT_PUBLIC_SANITY_PROJECT_ID" --dataset "$NEXT_PUBLIC_SANITY_DATASET" --token "$SANITY_API_EDITOR_TOKEN"

python3 scripts/get_sanity_document.py --slug "<slug>" --project-id "$NEXT_PUBLIC_SANITY_PROJECT_ID" --dataset "$NEXT_PUBLIC_SANITY_DATASET" --token "$SANITY_API_EDITOR_TOKEN"

python3 scripts/get_sanity_document.py --query '*[_type == "product" && product_id == "<ID>"][0]' --project-id "$NEXT_PUBLIC_SANITY_PROJECT_ID" --dataset "$NEXT_PUBLIC_SANITY_DATASET" --token "$SANITY_API_EDITOR_TOKEN"
```

Env-prefix equivalent: `NEXT_PUBLIC_SANITY_PROJECT_ID=… NEXT_PUBLIC_SANITY_DATASET=… SANITY_API_EDITOR_TOKEN=… python3 scripts/get_sanity_document.py --product-id "<ID>"`

## Patch draft

Use `drafts.{publishedId}` when a published doc exists. Panels array: unique `_key` per item. Image fields = Sanity asset refs.

```bash
python3 scripts/patch_sanity_draft.py scripts/.artifacts/<runId>/draftPatch.json --project-id "$NEXT_PUBLIC_SANITY_PROJECT_ID" --dataset "$NEXT_PUBLIC_SANITY_DATASET" --token "$SANITY_API_EDITOR_TOKEN"
```

Draft-only — never publish from this script (Stage 9).

## Upload asset (Stage 6)

```bash
python3 scripts/upload_sanity_image.py <file.png> --filename "{target}-{id}__{role}__{desc}.png" --project-id "$NEXT_PUBLIC_SANITY_PROJECT_ID" --dataset "$NEXT_PUBLIC_SANITY_DATASET" --token "$SANITY_API_EDITOR_TOKEN"
```
