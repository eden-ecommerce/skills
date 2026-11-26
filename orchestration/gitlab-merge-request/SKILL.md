---
name: gitlab-merge-request
description: "Open a GitLab merge request, set its description, or change its target branch, with `glab` or with git push options when `glab` is not installed. Use whenever a skill or the user needs to open or update a merge request on a GitLab remote."
agents:
  - cursor
---

# GitLab merge request

The caller decides the source branch, the target branch, the title, and the body. This skill only puts them on GitLab. It does not merge.

## Gates

- `git remote get-url origin` is a GitLab URL. A `github.com` URL is a pull request, not this skill.
- Read `git branch --show-current`. When it is `main`, `master`, or `develop`, stop. Push only the source branch. Never push a refspec of `main`, `master`, or `develop`, and never push the `production` remote.
- Do not `glab mr merge`. A person merges.
- Do not install `glab`, do not call the GitLab API with a token, and do not change git config.

## Write the body to a file

Write the description as normal Markdown in a file, for example `/tmp/<branch>.md`. Both paths below read it from that file.

Do not build the body with a heredoc inside `$(...)`. macOS ships bash 3.2, which fails on an apostrophe inside that heredoc. Write the file with the file tool, or use `read -r -d '' body <<'EOF'` without `$(...)`.

## Pick the path

Run `command -v glab`. When it prints a path and `glab auth status` succeeds, use **With `glab`**. Otherwise use **Without `glab`**.

## With `glab`

Open:

```bash
git push -u origin HEAD
glab mr create --source-branch <source> --target-branch <target> --title "<title>" --draft --yes --description-file <body-file>
```

Drop `--draft` when the caller wants the merge request ready for review.

Set the description: `glab mr update <id> --description-file <body-file> --yes`

Change the target: `glab mr update <id> --target-branch <target> --yes`

## Without `glab`

GitLab reads merge request settings from push options on the push itself. Git refuses a push option that contains a newline, so replace each newline with the two characters `\n`. GitLab 15.0 and later turn them back into newlines.

Open:

```bash
desc=$(< <body-file>)
desc=${desc//$'\n'/\\n}
git push -u origin HEAD \
  -o merge_request.create \
  -o merge_request.target=<target> \
  -o "merge_request.title=Draft: <title>" \
  -o "merge_request.description=$desc"
```

The `Draft:` title prefix stands in for `--draft`. Leave it off when the caller wants the merge request ready for review.

Set the description or change the target: add `-o "merge_request.description=$desc"` or `-o merge_request.target=<target>` to the next push of this branch, for example the `git push --force-with-lease` after a rebase.

Push options travel only with a push that sends commits. When the branch is already up to date, git prints `Everything up-to-date`, sends nothing, and drops the options. When no push is due, ask a person to make the change in the GitLab UI. Do not add an empty commit to carry the options.

## Check

The push or `glab` prints the merge request URL. Open it and check the title, the target, and the description.

When the description shows a literal `\n`, the server is older than GitLab 15.0. Use `<br>` in place of `\n` from then on, and ask a person to fix that description in the GitLab UI.

## Report

Return the merge request URL, its target branch, and whether it is a draft. Say so when a description or a target change is still waiting for the next push or for a person.
