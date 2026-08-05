# Article target

| Field | Value |
|---|---|
| id | `article` |
| sanityDoc | `article` |
| identifier | slug, doc id, or topic brief |
| panelField | `richText[]` embeds |
| algolia | optional — author or topic catalogue hunt |
| galleryKey | `gallery.article` |
| previewType | `article` |
| editorRole | professional blog article editor |

## Requirements

None beyond the shared outline (`target`, `brief`, `domain`). Narrative brief is enough — no hard IDs.

## Spine default

See `templates/article.md`.

## Draft rules

- Hero + content panels in `richText`
- Max 2 identical `_type` on final page
- Never use `markdown` panel `_type` — pick another panel from gallery
- Text body field name `markdown` (not `content`) on panels that use it — not the `markdown` panel type
