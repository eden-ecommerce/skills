# 03 — Chunk grep

Source maps weak? Grep built chunks for distinctive strings.

## Commands

```bash
# paths from manifest first
rg 'DistinctiveExportOrString' .next/static/chunks/<chunk>.js
```

Pick strings unique to suspect modules (component name, package id, zod literal).

## Compare baseline

Grep same string on sibling route chunk. Bigger hit / extra chunk on target = extra linkage.

## Map hits

Site string → file map: `references/next-next-eden.md`.
