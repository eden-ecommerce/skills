# App developer (this repo)

You own the **application** and **how it is containerized**; you also update deploy-facing fields in **`terraform/service.yaml`** (image, port, `env`, optional `secrets`). You do not need to be a dedicated Terraform contributor.

## Day to day

1. Change app code and **`Dockerfile`** as needed.
2. Build/push image (local `docker push` or CI `build:image` on MR/main).
3. Set **`terraform/service.yaml`** `image` to the URI you pushed; align `port` with `$PORT` in the container.
4. Open MR → review Terraform **plan** artifact → merge → **Infrastructure team** runs **Apply terraform:dev**.

## New app checklist

See `docs/environment/terraform.md` § First-time setup. If CI fails before plan, that's usually incomplete platform/infra onboarding, not an app bug.

## Do not

- Commit SA JSON keys or app secrets to git.
- Edit `terraform/main.tf` / `backend.tf` without Infrastructure team approval.
- Run `terraform apply` locally unless debugging with the Infrastructure team.
