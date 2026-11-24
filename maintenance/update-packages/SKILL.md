---
name: update-packages
description: >-
  Weekly dependency updates from Dependabot alerts, pnpm audit/outdated, and
  composer audit/outdated. Applies a 7-day publish guard on packages outside
  eden-ecommerce and christian-360, branches update-DD-MM-YYYY off the latest
  base, and stops for a scope gate and a manual test gate. Use when the user
  asks for a weekly package update, Dependabot fixes, pnpm audit, composer
  audit, or force latest.
---

# Update packages

One repo per run. The current checkout, or the repo the user names. Security fixes are the minimum. Currency updates are offered in the same gate. The user picks this week's set. The agent does not merge.

**Refuse** a second repo in the same run. Finish this one, including both gates, first.

---

## Git

Hard human gate. A person merges.

1. `git fetch origin`
2. Read `git branch --show-current`. When it is `develop`, `master`, or `main`, stop. Do not edit, commit, or push on those branches.
3. Base is the first remote that exists: `origin/develop`, then `origin/master`, then `origin/main`. Same order for PHP and JS.
4. Branch name is `update-DD-MM-YYYY` (example `update-24-11-2026`). `git checkout -b <name> <base>`. When that name already exists locally or on `origin`, stop and ask. Do not add a suffix.
5. Push only that branch: `git push -u origin HEAD`. Open the pull request against the same base. Do not `gh pr merge`.
6. Commit one line: `chore(deps): outcome`. Outcome is the task result, caveman. No `--author`, no `--trailer`, no `Co-authored-by`, no `Signed-off-by`. Do not change git config. Do not use `--no-verify`.

Create the branch only after the scope gate. Inventory happens on the current checkout without edits.

---

## Pins

Read these before proposing a version. A bump that needs a higher pin than production is **blocked**.

- `package.json` `engines`, `.nvmrc`, `.node-version`
- `composer.json` `require.php` and `config.platform`
- Docker image tags (`Dockerfile`, `docker-compose`)
- CI: `setup-node`, `setup-php`, and image tags in `.github/workflows`

---

## Inventory

Run every source that exists. The package manager writes the lockfile. Do not hand-edit it.

JavaScript uses pnpm. Install, update, audit, outdated, and scripts are `pnpm`. Do not run `npm` or `yarn`. Registry lookups are `pnpm view`.

**Dependabot.** `gh repo view --json nameWithOwner -q .nameWithOwner`, then:

```bash
gh api --paginate "repos/OWNER/REPO/dependabot/alerts?state=open"
```

Record package, ecosystem, manifest, severity, vulnerable range, and `first_patched_version`. On 403 or a disabled Dependabot, say so and continue with the local audit.

**pnpm.** When `package.json` exists. On an EdenServer docker project, run these inside the container (see below). Otherwise:

```bash
pnpm audit --json
pnpm outdated --format json
```

**Composer.** When `composer.json` exists:

```bash
composer audit --format=json
composer outdated --direct --format=json
```

Run both ecosystems when both files exist. A missing `composer audit` (old Composer) is reported; Dependabot and `composer outdated` still count.

---

## Classify

Trusted orgs, no age wait: `eden-ecommerce`, `christian-360`.

A package is trusted when its scope is `@eden-ecommerce/` or `@christian-360/`, or the repository URL owner is one of those orgs (`pnpm view <pkg> repository`, Composer `source` from `composer show -a <pkg>`).

Every other package is external. The target version's publish time must be at least 7 days before today.

- pnpm: `pnpm view <pkg> time --json`, then the target version key
- Packagist: `https://repo.packagist.org/p2/VENDOR/NAME.json`, that version's `time`

Unknown publish time counts as too new. Those versions stay off the branch unless the user forces them by name.

Put each candidate in one list:

- **Security** — open Dependabot alert or audit finding. Minimum set.
- **Currency** — direct dependency that can move to latest inside the current major. A major only when call sites can be adjusted and existing behaviour stays the same.
- **Blocked** — under 7 days, a production pin would break (PHP, Node, Ubuntu image), or the bump would change behaviour. State the reason.

---

## Scope gate

Stop before any edit, branch, or install. Show three lists. Each row is package, from, to, and why (security id, currency, age, or pin).

The user marks what goes in this week. Do not choose for them. An empty selection stops the run.

`force latest` is off unless the user says it at this gate. It bypasses only the 7-day guard, and only for packages they name (including a forced PHP or Ubuntu pin). It does not skip tests, the browser check, CI, or the manual test gate. Repeat each forced name back and wait for a yes.

---

## EdenServer docker

A project under the EdenServer path whose dev stack is `./deploy-dev.sh` in the env directory installs on the container, not the host. The container name is per project (`eden-hub` is one example). Read it from `docker ps` for this project. Do not reuse another project's name.

```bash
docker exec -it <container> pnpm install
```

Audit, outdated, update, and pnpm scripts (typecheck, lint, test) use that same container: `docker exec <container> pnpm <args>`. When `-it` has no TTY, rerun that command without `-it`. Do not fall back to host `pnpm`.

## Apply

On the new branch, update only the approved set.

- pnpm: `pnpm update <pkg>@<version>` (add `-r` only when the lockfile is a workspace and that package is in more than one project). EdenServer docker: `docker exec <container> pnpm update <pkg>@<version>`, then `docker exec -it <container> pnpm install`.
- Composer: `composer update <vendor/name> --with-dependencies`

Do not bump a package the user left off. If a security fix only exists in a major, and the user did not include that major, leave it blocked and say so in the pull request.

---

## Automated checks

Run what this repo already has. Read `package.json` scripts, `composer.json` scripts, and `.github/workflows`. Typical order:

1. typecheck
2. lint
3. unit
4. integration
5. e2e

A failing command stops the run. Paste the failure. Do not weaken a threshold and do not add `continue-on-error`. On an EdenServer docker project, run the pnpm scripts with `docker exec <container> pnpm <script>`.

When the repo has a UI, start the documented dev server and exercise the flows that depend on the updated packages in the browser. A backend-only change with no UI route skips the browser; say that in the pull request. The manual test gate still asks the user to test the affected behaviour.

---

## Pull request

Push the branch. Open the pull request against the base. Title: `update DD-MM-YYYY`. Body:

- Security rows included
- Currency rows included
- Blocked rows left out, with the reason
- Commands that passed, and the browser result
- Manual test checklist for the user

Watch `gh pr checks`. Wait until they finish. A failing check stops the run.

---

## Manual test gate

Stop when CI is green. The user tests on the branch. Do not merge. Do not push `develop`, `master`, or `main`. A failed manual check is fixed on this same branch only.
