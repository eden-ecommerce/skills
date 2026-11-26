---
name: merge-request-description
description: "Write a merge request or pull request description for the current branch against its parent, from the repo's own template: `.gitlab/merge_request_templates/Default.md` on GitLab, `pull_request_template.md` on GitHub. Use when the user asks for a description, or when gitlab-merge-request or a GitHub pull request needs a body."
agents:
  - cursor
---

# Merge request description

Fill the repo's template from what the branch actually does. Short, factual, British English.

Read the host from `git remote get-url origin`. A `github.com` URL is GitHub. Anything else is GitLab. If the host is unclear, ask.

## Pick the base

Describe the current branch against its parent, unless the user or the calling skill names the branches. Named branches are used as given, without asking.

Git does not record a parent. Take the closest remote branch: the one the current branch is fewest commits ahead of. Skip branches that already contain the current branch.

```bash
cur=$(git branch --show-current)
default=$(git symbolic-ref --short refs/remotes/origin/HEAD)
git fetch origin
git for-each-ref --sort=-committerdate --count=100 --format='%(refname:lstrip=2)' refs/remotes/origin | grep -v -e '/HEAD$' -e "^origin/$cur$" |
  while read -r b; do
    git merge-base --is-ancestor HEAD "$b" && continue
    echo "$(git rev-list --count "$b"..HEAD) $b"
  done | sort -n | head -3
```

- The closest is `$default`, or ties with it: use `$default`.
- The closest is another branch: ask the user whether to base the description on that branch or on `$default`. Do not guess.

## Gather

Read the change first, then the reasons for it.

```bash
git diff --stat <base>...HEAD
git diff <base>...HEAD
git log --reverse --format='%h %s%n%b' <base>..HEAD
```

- The diff is the source of truth. `<base>...HEAD` diffs from the merge base, which is what GitLab and GitHub show. Commit messages explain why. When they disagree, follow the diff and say so.
- `git log` takes two dots. Three dots would also list the base branch's own new commits.
- List generated files (lockfiles, `vendor/`, generated code) in one line. Do not read them.
- Tests, checks, and deploy notes from this conversation: what ran, the command, the result.
- Related merge requests, issues, and other repos that must deploy first.

The merge request holds only pushed commits. Check `git status --porcelain` and `git rev-list --count origin/$cur..HEAD`. When `origin/$cur` does not exist, nothing is pushed yet. Unpushed commits are expected when the caller is about to push. Otherwise tell the user they are not in the merge request yet. For anything uncommitted:

- When its intent is clear from the branch and this conversation, follow it. Describe the work that finishes this branch and leave out what is clearly unrelated. Say which you did.
- Otherwise ask the user whether it belongs in this merge request.

## Find the template

Read templates from `$default`, not from the working tree. Both hosts use only the copy on the default branch.

### GitLab

```bash
git ls-tree --name-only "$default" .gitlab/merge_request_templates/
git show "$default":.gitlab/merge_request_templates/<file>.md
```

1. The template the user names.
2. `Default.md`, matched case-insensitively (`default.md` counts). GitLab applies it to every new merge request.
3. Another template in that folder that matches the change. Say which one you picked.
4. None in the repo: use the fallback and say so. A default in the project settings, or a group or instance `Default.md`, can still apply in the UI. Git cannot see those, so ask the user when they mention one.

### GitHub

```bash
git ls-tree -r --name-only "$default" | grep -i -E '^(\.github/|docs/)?pull_request_template(\.md$|/)'
git show "$default":<path>
```

1. The template the user names.
2. `pull_request_template.md`, matched case-insensitively: `.github/` first, then the root, then `docs/`.
3. A `PULL_REQUEST_TEMPLATE/` folder in any of those: none applies by default. Pick the one that matches the change and say which.
4. None in the repo: the owner's public `.github` repository can supply one, in the same places and order. Check with `gh api repos/<owner>/.github/contents/<path>` when `gh` is available. Otherwise use the fallback and say so.

`gh pr create --body-file` replaces the template, so fill the template here.

The repo template wins over a template from a calling skill. Put the caller's content under the repo's headings.

## Fill it

- Keep every heading, in the template's order. Write `None` or `Not applicable` under a heading that does not apply. Do not delete it.
- Delete the `<!-- -->` guidance comments once the section under them is filled. Keep any other comment, such as a link to the team's code review page.
- Tick a checkbox only for what was done or verified. A step a person still has to do stays unticked.
- Facts only. A test that did not run says `Not run`. Do not invent a URL, a result, or a reviewer step.
- Name files, classes, commands, and merge requests in backticks or as links.
- Plain sentences. No filler, no em dashes, no marketing tone.

## Fallback

```markdown
## Summary

## Testing

## Deployment

## Rollback
```

## Output

Reply with the description as Markdown in one fenced `markdown` block, ready to paste. Write a file only when the user asks for one.

When another skill called this one, hand the text back to it for its body file. Do not print it as well.
