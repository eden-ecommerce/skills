---
name: schema-and-gallery
description: Entity gallery URLs and schema extraction.
---

# SCHEMA + GALLERY

## GALLERY (per target)

Fetch one gallery URL from [targets.md](targets.md). Parse:

```html
<script type="application/json" id="panel-catalogue">…</script>
```

Each entry: `_type`, `title`, `intent`, `group`, `contextTags`.

Scroll rendered HTML for layout, variants, responsive behaviour.

Article gallery = eden-blog visual reimpl via `PortableText`. Other entities = next-next-eden real components.

## SCHEMA

```bash
curl -s https://cms.eden.co.uk/schema.json -o schema.json
python3 scripts/extract_panels.py schema.json product panels
python3 scripts/extract_panels.py schema.json article richText
```

Common panel field names:

| Field | Used on |
|---|---|
| `panels` | product, home, category, department, org pages |
| `richText` | article body embeds |
| `topPanels` / `bottomPanels` | hubPageContent |
| `bottomPanels` | category, department (richText only) |

## FIT NOTES

- Schema allowlist = `webPageAllowedPanels` (= `allPanels`) on web page docs
- PDP may still NullPanel some types for bundle — galleries show truth via entity renderer + `loadProductPanel` fallback
- Gallery title ≠ schema name → match by visual + description
