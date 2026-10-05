---
name: review-comments
description: Fetch unresolved review comments on the current branch's pull request via GitHub MCP, explain each with a suggested change or a question, then after the user picks comments, implement them. Once they say they are happy, commit and push, then post a reply on each thread plus one top-level comment of the user's decisions, building up across stacked pull requests and flagging slices above that need restacking. Use when the user says /review-comments or asks for PR comments on this branch. When they ask to go through the whole lot of threads at once, switch to Plan mode first.
---

# review-comments

Report first. Edit files only for comments the user selects in step 8. After the edits, ask whether the user is happy with the changes. Once they say yes, commit and push those changes, then show reply drafts and wait again before posting. Do not draft or post GitHub replies, or the context comment, until the push has succeeded.

## Whole queue

When the user asks to go through the whole lot of threads at once (every open review, a stack of pull requests, or the rest of the threads), switch to Plan mode before any edit, commit, or push. Call SwitchMode with target `plan`. If you are already in Plan mode, stay there.

Do not leave Plan mode to implement until the user accepts the current thread. Commit and push still wait until they say they are happy with that diff.

In that plan:

- Show only the current thread, in the step 7 format, and include its GitHub link.
- Put each review the user has already agreed into the plan todos. Mark it completed only after it is pushed. Leave it pending when the change is still local, so a change they have not reviewed cannot be skipped.
- List every later thread, from the next one through the last, as a bullet: link, a concise version of the comment, then the login of who left the thread.

## 1. Resolve repo and branch

From the working directory the user cares about (or repo root):

- Read `.git/HEAD` for the branch name (`ref: refs/heads/...`).
- Read `.git/config` for `remote "origin"` URL and derive `owner/repo` (e.g. `https://github.com/eden-ecommerce/design.git` → `eden-ecommerce/design`).

Prefer file reads over shell `git` when the environment is slow.

If the user gave a PR URL or number, use that instead of branch lookup.

## 2. GitHub MCP (required)

Call `GetDynamicTools` with pattern `github` (or the connected GitHub namespace id). Discover tool names at runtime; do not hard-code tool names in this skill.

- If no GitHub namespace is listed, or status is `needsAuth` / `error`: **stop**. Tell the user to connect or authenticate the GitHub MCP in Cursor Settings. **Do not fall back to `gh` CLI.**
- If auth is needed, use `CallDynamicTool` with `mcp_auth` for that namespace, then retry.

**Who posts.** GitHub MCP comments appear as whichever account is authenticated in Cursor (check with `get_me`). There is no “post as bot” switch in the skill. To use a machine user or GitHub App bot, connect MCP with that token or post from CI; tell the user before posting if they expected a bot identity.

## 3. Find the open PR

Using GitHub MCP, find the **open** pull request whose head branch matches the current branch (same repo). If none exists, stop and say the branch may not be pushed or has no open PR.

### Check the slices below before editing

Do this as soon as the pull request is found, before step 9. A shallow clone can make the ancestor check fail: deepen with `git fetch --deepen` before trusting it.

1. Note this pull request's base branch, and whether the pull request it stacks on is still open or already merged.
2. Fetch that base. If `git merge-base --is-ancestor origin/<base> HEAD` is false, this branch is missing commits from below. Stop. Tell the user, and name the conflicting files from `git merge-tree --write-tree --name-only origin/<base> HEAD`. Do not edit until they say to restack.
3. If the pull request below has merged, run the same check against the branch it merged into (usually `main`). Missing those commits means this branch still contains the pre-merge copy.

## 4. Fetch comments (unresolved scope)

Using GitHub MCP, fetch:

- Unresolved inline review threads (exclude outdated lines where the API marks them outdated).
- Top-level review and issue comments on the PR that still need a response.

**Exclude** unless they contain an open question to the author:

- Authors whose login ends with `[bot]`.
- The PR author's own replies that only acknowledge or resolve.

Sort for reading: file path, then line number, then thread creation time.

Keep, for every thread, the thread node id and the id of its latest comment. Step 9 replies using those ids.

## 5. Ground each inline comment in local code

For each inline comment with a file path and line (or range), read that file locally at those lines before writing **What it does**. Do not guess from the comment alone. Put how sure you are of that reading in the heading, as a percentage (for example `99% confident`). Lower the percentage when the comment or the local code leaves the reading uncertain.

## 6. Classify each comment

Use exactly one outcome per comment:

| Outcome | When |
|--------|------|
| **Suggested change** | Reviewer's intent is clear; the fix is local to the referenced code and aligns with repo rules. |
| **Need more information** | Ambiguous wording; conflicts with a repo rule; design or visual change without explicit approval; needs a product or architecture decision; or you cannot tell what to change. Name who to ask (usually `@reviewer`). |

When design or styling is in question and the user has not approved a change, prefer **Need more information**.

## 7. Output format

One block per comment, separated by `---`. Number comments sequentially.

```markdown
### 1. `path/to/file.tsx:42` — @reviewer
> quoted comment (trimmed; preserve meaning)

**What it does (99% confident):** Plain-English link between the reviewer's point and the current code. Replace `99%` with how sure you are of that reading.

**Suggested change:** Concrete edit — use a code citation for existing code or a short fenced block for the proposed fix.

---
```

Or, instead of **Suggested change**:

```markdown
**Need more information:** What is unclear and who to ask (e.g. @reviewer).
```

After all blocks, one summary line:

`Summary: N suggested change(s), M need more information.`

## 8. Next step for the user

Use `AskQuestion` with **allow_multiple: true**: list each comment by number and short label; ask which ones to apply. Do not implement until they choose.

Do not apply comments classified **Need more information** unless the user explicitly asks.

## 9. Implement, confirm, commit, push, then reply

Only after the user selects comments in step 8:

1. Implement only the selected comments, following the repo's rules. Keep each change minimal and targeted.
2. Run the repo's checks that apply to the touched files, and report any failures. Do not commit a repo whose checks failed.
3. Summarise what changed, in a short list. Use `AskQuestion` to ask whether the user is happy with the changes. Options: happy, commit and push; not happy, they will say what to change. **Stop here.** Do not commit, push, draft, or post until they say they are happy.
4. If they are not happy, change the code they name and return to step 3.
5. Once they are happy, commit and push before any GitHub reply:
   - One commit per repo this round changed. Stage only the files from this round. Do not stage secrets (`.env`, credentials).
   - Read `git log -5 --format=%s` in that repo and match that subject style. Pass the message with a HEREDOC. Do not use `--no-verify` or `--no-gpg-sign`.
   - If the branch is `main` or `master`, stop and ask before committing.
   - Push with `git push -u origin HEAD`. Do not force-push. If the push fails, stop and report it. Do not draft replies.
   - If a repo has nothing new to commit, say so and still push when the branch is ahead of the remote.
6. Tell the user the commit subject and the remote branch for each repo.
7. Check the stacked pull requests above this one:
   - Using GitHub MCP, list open pull requests whose base branch is the branch just pushed. Repeat for each of those, so you cover every slice higher up the stack.
   - For each, fetch its head branch and run `git merge-tree --write-tree --name-only HEAD origin/<its head branch>`. Record any conflicting files.
   - Tell the user which pull requests need restacking and which files conflict. Do not rebase, restack, or force-push them without asking.
   - If none exist, say so and skip the downstream comments in step 10.
8. Discover the reply tool via `GetDynamicTools` on the GitHub namespace. Look for a tool that replies to a pull request review thread or comment. Do not hard-code its name. Reply using the thread node id or latest comment id kept in step 4.
9. Draft one reply per implemented comment and show all drafts to the user in one block. Wait for approval before posting anything.
10. Post each approved reply. Never resolve a thread. Never reply to a **Need more information** comment unless the user explicitly asks.
11. Report which threads got a reply, with links.

Reply format. Short, plain, British English, no emojis. If the reviewer asked more than one thing in the thread (for example “split files?” and “add a rule?”), answer **each** in `Done:` or `Changed:` — do not merge them into one vague line.

When the reviewer asked for a rule and `/reflect-review` (step 11) already added or strengthened a guard in this chat, say which rule file and section in `Changed:`. Do not write “we can add a rule if you want” after the rule is already in the repo.

If thread replies are posted **before** reflect-review lands the rule, post a short follow-up on that thread once the guard is committed.

```markdown
Done: <one-line summary of the code change>.
Changed: `path/to/file.tsx` (<what>); `.cursor/rules/<file>.mdc` (<rule topic>, if applicable).
```

Name the commit subject in the reply when it helps the reviewer find the push.

## 10. Record context

Only after the user has said they are happy with the changes (step 9) and the thread replies are posted:

1. Collect only the decisions and instructions the user gave in this chat about how to implement the selected comments (answers to `AskQuestion`, explicit directions such as a chosen name or library). Leave out reasoning, chatter, and anything about unselected comments.
2. If the user gave no such guidance, skip this step and say so.
3. Inherit earlier context. Find the latest top-level comment starting `Context for this stack` on this pull request. If there is none, use the one on the base pull request (the open pull request whose head branch is this one's base). Copy its sections unchanged, then add this round's lines under this pull request's heading.
4. Draft one top-level pull request comment (not a thread reply) for this pull request. For each pull request above it from step 9.7, draft one more with the same sections plus a **Needs restack** list of its conflicting files. Show every draft to the user in one block. Wait for approval before posting.
5. Post each approved comment with the GitHub MCP tool for adding a pull request or issue comment, discovered at runtime via `GetDynamicTools`. Do not hard-code its name.
6. Never include secrets, tokens, local file paths outside the repo, or content from unrelated chats.

Context lives in pull request comments only. Never commit it to a file in the repo.

Comment format:

```markdown
Context for this stack, up to #<this pull request number>:

#<earlier pull request number> (<branch>):
- <inherited line, unchanged>

#<this pull request number> (<branch>), commit <short sha>:
- <decision or instruction, one line each, tagged with the comment it relates to, e.g. "debounce.ts: use lodash.debounce">

**Needs restack** (only on pull requests above this one):
- `<conflicting file path>`
```

## 11. Hand over to reflect-review

After step 10, or as soon as the user skips or postpones the replies or the context comment, use `AskQuestion` to ask whether to run `/reflect-review` now. Do not end the round without asking. Running it turns repeated reviewer patterns into guards in the repo's Cursor rules. If the user says yes, read `../reflect-review/SKILL.md` and follow it with the comments from this run.

When a review thread explicitly asks to “put in rules”, prefer running reflect-review **before** step 9.8 drafts thread replies, so replies can cite the new guard. If replies went out first, use a follow-up reply on that thread after the rule commit.

## Do not

- Merge, or open a new pull request.
- Force-push, or commit onto `main` or `master` without asking.
- Rebase or restack the pull requests above this one without asking.
- Commit context to a file. It lives in pull request comments only.
- Commit or push before the user has said they are happy with the code changes.
- Resolve review threads (the reviewer does this).
- Use `gh` or REST when GitHub MCP is unavailable (stop and ask to connect MCP instead).
- Draft or post any GitHub reply or comment before the user has said they are happy with the code changes.
- Post any reply or comment without showing the draft first.
- Reply to comments classified **Need more information** unless the user explicitly asks.
