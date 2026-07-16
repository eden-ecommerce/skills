# 02 — Chunk diff

Fail route vs **healthy sibling** same layout. Isolate route-only weight from shared shell.

## Script

After `pnpm turbo-analyse-ci`, app root:

```bash
node -e "
const fs = require('fs');
const data = require('./.next/diagnostics/route-bundle-stats.json');
const baseline = data.find(r => r.route === '/home');
const target = data.find(r => r.route === '/product/[id]');
const baselineChunks = new Set(baseline.firstLoadChunkPaths);
const targetOnly = target.firstLoadChunkPaths.filter(c => !baselineChunks.has(c));
let total = 0;
const rows = targetOnly.map(c => {
  const size = fs.existsSync(c) ? fs.statSync(c).size : 0;
  total += size;
  return { size, name: c.split('/').pop() };
}).sort((a, b) => b.size - a.size);
for (const r of rows) console.log((r.size / 1024).toFixed(1) + 'kB', r.name);
console.log('Target:', (target.firstLoadUncompressedJsBytes / 1024).toFixed(1), 'kB');
console.log('Target-only chunks:', rows.length, 'total:', (total / 1024).toFixed(1), 'kB');
"
```

Swap route strings.

## Interpret

| See | Likely |
|-----|--------|
| Few large target-only chunks | Route feature / page imports |
| Many routes fail ~same % | Shared layout, provider, dep bump |
| Target-only total ≈ overshoot | Fix those chunks first |
