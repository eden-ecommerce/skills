---
name: generate-changelog
description: "Hub deploy note — git diff master↔develop, new docs/releases file."
agents:
  - cursor
---

/caveman full

**Repo cockpit:** hub root. `docs/releases/` — **Titles** fixed below; still peek latest `0-2-*.md` for tone and bullet density.

**Bind:** user gives filename **or** next patch from latest release file. Optional **baseline** commit on `origin/master` → also `git log` / `git diff` `<baseline>..origin/master` **plus** usual `origin/master..origin/develop`. **@Branch** → footer note branch name only; default diff still `master..develop` unless user overrides.

**Output:** new `docs/releases/<version>.md`. **Titles (exact, in order):** `# Deployment Notes` → `## ✨ New Features` → `## 🔧 Improvements` → `## 🐛 Bug Fixes` → `## 🔒 Technical Improvements`. Omit an `## …` block if empty. End file: italic one-line `_Preparation:_` (git ranges + deploy-branch caveat). British English, plain language, themes not raw paths.

**Git:** `git fetch origin`; then `git diff --stat` + `git log --oneline` on `origin/master..origin/develop` (+ baseline range if given). Hub repo only.

**Cavecrew:** `cavecrew-investigator` → `name-only` path prefix counts (both ranges if baseline). Main thread → prose. `cavecrew-builder` only if **single** output file; else skip. Optional `cavecrew-reviewer` on `.md`.

**Handoff:** path + ranges used.
