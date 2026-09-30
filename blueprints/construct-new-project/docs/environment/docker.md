# Dockerfile (required for Cloud Run)

This app runs on **Google Cloud Run**, which starts a **container image** built from a `Dockerfile` (or equivalent build config).

## Rules

- Keep **`Dockerfile`** at repo root. CI and `pnpm build:docker` use `--file Dockerfile` (context is repo root). Ignore SSOT is `.dockerignore`, loaded via `Dockerfile.dockerignore`.
- The process must listen on **`$PORT`** (integer). Cloud Run injects `PORT`; `terraform/service.yaml` `port` must match what the container binds to (scaffold default: **8080**).
- After changing the Dockerfile or application entrypoint, rebuild the image and update **`terraform/service.yaml`** `image` if the tag or registry path changed.
- Do not put secrets in the image; use Secret Manager via `service.yaml` `secrets` (the Infrastructure team can help wire refs).

## Scaffold

New repos from `setup-new-app.sh` include a minimal **Python hello world** (`main.py` + `Dockerfile`). Replace with your stack when ready; update the Dockerfile and dependencies together.

## Local check

```bash
./scripts/docker/run-local-docker.sh
```

Copies from platform kit via `setup-new-app.sh`. Optional `.env` at repo root is passed through when present.
