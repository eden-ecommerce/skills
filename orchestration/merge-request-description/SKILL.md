---
name: merge-request-description
description: "Write a GitLab merge request description for the current branch against its parent, from the repo's own template, usually `.gitlab/merge_request_templates/Default.md`. Use when the user asks for a merge request description, or when gitlab-merge-request needs a body."
agents:
  - cursor
---

# Merge request description

Fill the repo's template from what the branch actually does. Short, factual, British English.

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

- `git log --oneline <base>..HEAD` and `git diff --stat <base>...HEAD`. Read the diff where the stat is not enough.
- Tests, checks, and deploy notes from this conversation: what ran, the command, the result.
- Related merge requests, issues, and other repos that must deploy first.

## Find the template

GitLab reads templates only from `.gitlab/merge_request_templates/*.md` on the project's default branch. Read them from `$default`, not from the working tree:

```bash
git ls-tree --name-only "$default" .gitlab/merge_request_templates/
git show "$default":.gitlab/merge_request_templates/<file>.md
```

Use the first that applies:

1. The template the user names.
2. `Default.md`, matched case-insensitively (`default.md` counts). GitLab applies it to every new merge request.
3. Another template in that folder that matches the change. Say which one you picked.
4. No template in the repo. Use the fallback below and say no repo template was found. A default in the GitLab project settings, or a group or instance `Default.md`, can still apply in the UI. Git cannot see those, so ask the user when they mention one.

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

When gitlab-merge-request called this skill, hand the text back to it for its body file. Do not print it as well.
