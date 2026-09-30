# App terraform/ (this target)

Only applies once `docs/DEPLOYMENT_STRATEGY.md` § 1 picked "managed container" and Terraform as the infra-as-code tool. A different target (Vercel, plain Docker + a VM, etc.) needs its own `docs/environment/<target>.md` instead — do not force this file's specifics onto a different strategy.

## Ongoing law

- Contributors edit `service.yaml` only unless the platform/infra owner approves other files.
- Module pinned in `main.tf` — bump `ref=` deliberately after reading the module's own changelog.
- When `main.tf` is open or on request: compare `ref=` to the latest tag; suggest a bump, never auto-bump.
- Plan/apply runs in this repo's CI (GitLab pipeline or GitHub Actions — see `docs/environment/github.md` for the GitHub wiring) — not locally.
- State prefix is unique to this app — do not copy `backend.tf` from another app unchanged.
- Secrets live in a cloud secret manager, never in git.

## First-time setup (before the first production apply)

- [ ] `Dockerfile` builds and listens on `$PORT` (scaffold default: 8080) — see `docs/environment/docker.md`
- [ ] Image pushed to the URI in `service.yaml`; hello-world tested locally with `docker run`
- [ ] `backend.tf`: state prefix is unique to this app (e.g. `cloud-run/<project-name>/dev`)
- [ ] `main.tf`: `ref=` points to a released tag, not a moving branch
- [ ] `service.yaml`: name, image URI, and port match the container; `secrets:` filled when the app needs the secret manager
- [ ] CI wired: GitLab `.gitlab-ci.yml` + `terraform.yml` include, or GitHub `.github/workflows/build.yml` + `terraform.yml` (see `docs/environment/github.md`)
- [ ] Platform/infra onboarding done (service account, project access)
- [ ] First PR/MR: plan job green; infra owner runs the first manual apply

After the first successful apply, use `docs/environment/developer.md` / `docs/environment/docker.md` for day-to-day changes.
