## Summary

[1-2 sentences: what this slice changes and why]

## Scope

- **In this slice:** [files and behaviour from the diff]
- **Later slice:** [what this slice does not do]
- **Package pin:** [none | the package and version this slice changes]
- **Safe to deploy alone:** [yes | no, and the flag, dormant route, or additive change that makes it safe]
- **Deploy type:** [filled from the file checks below]

## Dev test plan

Numbered checks for this branch only. Name the command, the URL, and the click path that exist in this repo. Write `none` for a step this repo does not have. Mark what this slice cannot show yet.

1. [ ] [local command from package.json, composer.json, or the repo rules]
2. [ ] [local URL or page]
3. [ ] [what this slice cannot show until a later slice]

## Deployment plan

Run the file checks in the repo this slice belongs to. Keep every matching section. Delete every section that did not match. A repo can match more than one. Write the matched file paths on the Deploy type line in Scope. Do not invent a host, a command, or a URL.

**File checks**

| Keep this section | When this file check matches |
|-------------------|------------------------------|
| Cloud Run | Any `*.tf` file |
| PHP manual | `composer.json` exists and `vercel.json` does not |
| GitLab Vercel | `.gitlab-ci.yml` contains `vercel` |
| GitHub Vercel | `git remote get-url origin` contains `github.com`, and `vercel.json` exists or a file in `.github/workflows/` contains `vercel` |
| Worker route | GitHub Vercel matched, a `next.config.*` file exists, and this slice adds or changes a public path |
| Changesets | A `.changeset/` directory exists |

### Cloud Run

Keep when any `*.tf` file exists. Name the `.tf` files this slice touches. If it touches none, write `no terraform changes`.

- [ ] The workflow that plans terraform is green. Name the workflow file under `.github/workflows/`.
- [ ] No secrets in the diff
- [ ] Image and service come from the `.tf` files, not from memory
- [ ] Merge this slice only. Prod deploy is the workflow on the base branch. Do not run `terraform apply`

When the diff also contains a migration, name the migration file and the workflow that runs it. One migrate, then the test, then merge.

### PHP manual

Keep when `composer.json` exists and `vercel.json` does not. This is a hard human gate.

The agent opens the merge request into `develop` and stops. The agent does not merge. The agent does not push `develop`, `master`, or the `production` remote.

A person does this, in this order, after the slice is reviewed:

1. [ ] Merge the slice into `develop`
2. [ ] Test on the result of that merge
3. [ ] Merge `develop` into `master`
4. [ ] `git push origin master`
5. [ ] `git push production master` — the remote named `production` in `git remote -v`. If that remote is missing, stop and write `production remote not found`

GitLab CI on the merge request is not the production deploy.

### GitLab Vercel

Keep when `.gitlab-ci.yml` contains `vercel`.

- [ ] Merge this slice only
- [ ] The GitLab pipeline deploys the Vercel project. Name the job from `.gitlab-ci.yml`
- [ ] Run the dev test plan on the deployed URL
- [ ] Do not merge the next slice until this one is deployed and tested

### GitHub Vercel

Keep when the origin remote contains `github.com`, and `vercel.json` exists or a file in `.github/workflows/` contains `vercel`.

Day-to-day commands, only when `package.json` has the script:

- [ ] `pnpm run pull:env`
- [ ] `pnpm run dev`
- [ ] `pnpm run predeploy` before push

Deploy:

- [ ] Merge this slice only. Name the workflow file that deploys to Vercel
- [ ] Confirm the deployment in that workflow
- [ ] Run the dev test plan on the deployed URL
- [ ] Do not merge the next slice until this one is deployed and tested

### Worker route

Keep when GitHub Vercel matched, a `next.config.*` file exists, and this slice adds or changes a public path. The proxy is the worker in the manage repo:

`httpdocs/automatedqueries/nextEden/cloudflare-worker-router-2`

Read `src/routing.ts` and `src/mvt/actions/rewritePagesForPagesWithMVT.ts`. If that directory is not in the workspace, say so. Do not invent a route.

**Path already in `src/routing.ts`**

- [ ] Update `src/routing.ts` and `src/mvt/actions/rewritePagesForPagesWithMVT.ts` only if this public path changed
- [ ] Update the test under `src/tests/`
- [ ] A person runs `worker-test`
- [ ] A person runs `worker-deploy`. The agent does not
- [ ] The manage repo merge to `master` is the PHP manual gate. The agent does not push it

**Path not in `src/routing.ts` (new site)**

A person does the hookup. The agent lists the steps and does not perform them.

1. [ ] Namespace matches `NEXT_PUBLIC_NAMESPACE`. Use `pnpm run setup` when that script exists
2. [ ] Vercel project name and the GitHub repo name match
3. [ ] Vercel domain is the `eden.co.uk` subdomain
4. [ ] Cloudflare DNS for `eden.co.uk`: the CNAME and the TXT record from Vercel. Proxy status off
5. [ ] `NEXT_PUBLIC_PRODUCTION_ORIGIN` or `VITE_PRODUCTION_ORIGIN` is `https://<subdomain>.eden.co.uk`
6. [ ] Add the path to `src/routing.ts` and `src/mvt/actions/rewritePagesForPagesWithMVT.ts`, plus a test
7. [ ] A person runs `worker-test`, then `worker-deploy`
8. [ ] Assets load on the subdomain, and the beacon is the first network request

### Changesets

Keep when `.changeset/` exists.

- [ ] This slice publishes with Changesets
- [ ] The tag is `design-v*` or `lib-v*`
- [ ] A consumer pins that exact version. Do not invent a host

## Reversion plan

Keep the block that matches the deploy type. Delete the rest. Say how to undo this slice without undoing a later slice.

### Cloud Run

- [ ] Shift traffic to the previous revision, or re-apply the previous image in the `.tf` file this slice changed
- [ ] A migration in the diff is forward-only. Name the recovery, or write `additive only`

### PHP manual

- [ ] A person reverts on `develop` and then on `master`, and pushes `origin` then the `production` remote
- [ ] The agent does not run that push
- [ ] Schema change: code revert is not enough. Name the recovery, or write `no schema change`

### GitLab Vercel

- [ ] Revert the merge and let the GitLab pipeline redeploy
- [ ] Or roll back the deployment in Vercel

### GitHub Vercel

- [ ] Revert the merge and let the Vercel workflow redeploy
- [ ] A worker change reverts in the manage repo through the PHP manual gate. The agent does not push it

### Changesets

- [ ] Publish the previous version and pin that version in the consumer
