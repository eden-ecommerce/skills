# GitHub (this target)

Concrete mechanics for the git-host choice this project made at intake. If the project uses GitLab, Bitbucket, or another host instead, this file does not apply — write its equivalent (`docs/environment/gitlab.md`, etc.) with that host's real CLI/CI shape rather than guessing GitHub's onto it.

## PR mechanics (generic law: `pull-requests.mdc`)

1. Ensure the branch is on the remote (`git push -u` if needed).
2. If no open PR for `HEAD`: `gh pr create` with the body from the template, passed via HEREDOC.
3. If a PR already exists: `gh pr edit <n> --body` with a refreshed template fill from `origin/main...HEAD` (every commit + file list on the branch — not just the tip commit).
4. Return the PR URL.

```bash
gh pr create --title "the pr title" --body "$(cat <<'EOF'
## Summary
...
EOF
)"
```

## CI wiring

Workflow files under `.github/workflows/`. Plan/build/test stages run there, not locally, for anything gated on merge (e.g. Terraform plan — see `docs/environment/terraform.md`).

## GitHub Packages (only if the shared-package tier resolves from here)

- Registry host: `npm.pkg.github.com`
- Install auth: a token with `read:packages`, set via `.npmrc` or `pnpm config set //npm.pkg.github.com/:_authToken "$TOKEN"`
- Publish: a Changeset in the package's own repo, tagged (e.g. `design-vX.Y.Z`), pushed to this registry
- The generic exact-semver-pin law lives in `docs/ARCHITECTURE.md` § Shared-package strategy and `ownership.mdc` — this section is only "which registry host, which token."
