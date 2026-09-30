#!/usr/bin/env node
// Fails when the agent entry files drift apart. Wired into `check`.
import { readFileSync } from 'node:fs';

const entryFiles = ['CLAUDE.md', 'AGENTS.md', 'PROJECT_RULES.md'];
const [first, ...rest] = entryFiles.map((file) => readFileSync(file, 'utf8'));
const drifted = entryFiles.slice(1).filter((_, index) => rest[index] !== first);

if (drifted.length) {
  console.error(`Entry files differ from CLAUDE.md: ${drifted.join(', ')}. Copy CLAUDE.md over them.`);
  process.exit(1);
}
