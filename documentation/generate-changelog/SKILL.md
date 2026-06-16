---
name: generate-changelog
description: "Generate deploy note — git diff master↔develop, semver from changes, release doc + package.json."
agents:
  - cursor
---

/caveman ultra

**Cockpit:** project root. `docs/releases/` — peek latest `*-*-*.md` for tone/density. Hub `package.json` `version` must match release.

**Bind:** optional user filename/version override. Optional **baseline** on `origin/master` → also `git log` / `git diff` `<baseline>..origin/master` + usual `origin/master..origin/develop`. Default diff `master..develop`.

**Version:** read latest release + `package.json`. Infer bump from diff unless user overrides:
- **patch** (third) — bug fixes, tweaks, refactors, tech-only, no new user-facing capability
- **minor** (middle) — new features, new flows, non-breaking additions
- **major** (first) — breaking changes, removed APIs, incompatible migrations/schema

Filename dashes → semver dots: `0-2-16.md` → `0.2.16`.

**Output:**
1. `docs/releases/<version>.md` — titles exact order: `# Deployment Notes` → `## ✨ New Features` → `## 🔧 Improvements` → `## 🐛 Bug Fixes` → `## 🔒 Technical Improvements`. Omit empty `##`. No footer. British English, themes not paths.
2. Project root `package.json` — set `"version"` to matching semver. Only `version` key.

**Git:** `git fetch origin`; `git diff --stat` + `git log --oneline` on `origin/master..origin/develop` (+ baseline if given).
