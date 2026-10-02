---
name: review-comments
description: Fetch unresolved review comments on the current branch's pull request via GitHub MCP, explain each with a suggested change or a question, then after the user picks comments, implement them and post a reply on each thread plus one top-level comment of the user's decisions. Use when the user says /review-comments or asks for PR comments on this branch.
---

# review-comments

Report first. Edit files only for comments the user selects in step 8. After the edits, ask whether the user is happy with the changes. Do not draft or post GitHub replies, or the context comment, until they say yes. Then show drafts and wait again before posting.

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

## 3. Find the open PR

Using GitHub MCP, find the **open** pull request whose head branch matches the current branch (same repo). If none exists, stop and say the branch may not be pushed or has no open PR.

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

For each inline comment with a file path and line (or range), read that file locally at those lines before writing **What I think it does**. Do not guess from the comment alone.

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

**What I think it does:** Plain-English link between the reviewer's point and the current code.

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

## 9. Implement, then confirm, then reply

Only after the user selects comments in step 8:

1. Implement only the selected comments, following the repo's rules. Keep each change minimal and targeted.
2. Run the repo's checks that apply to the touched files, and report any failures.
3. Summarise what changed, in a short list. Use `AskQuestion` to ask whether the user is happy with the changes. Options: happy, proceed to reply drafts; not happy, they will say what to change. **Stop here.** Do not draft or post any GitHub reply or context comment until they say they are happy.
4. If they are not happy, change the code they name and return to step 3. Do not draft replies for a comment whose change fails checks or that they have rejected.
5. Once they are happy, discover the reply tool via `GetDynamicTools` on the GitHub namespace. Look for a tool that replies to a pull request review thread or comment. Do not hard-code its name. Reply using the thread node id or latest comment id kept in step 4.
6. Draft one reply per implemented comment and show all drafts to the user in one block. Wait for approval before posting anything.
7. Post each approved reply. Never resolve a thread. Never reply to a **Need more information** comment unless the user explicitly asks.
8. Report which threads got a reply, with links.

Reply format. Short, plain, British English, no emojis:

```markdown
Done: <one-line summary of the change>.
Changed: `path/to/file.tsx` (<what, in a few words>).
```

Mention the commit only if the user has already committed. Do not push or commit for them.

## 10. Record context

Only after the user has said they are happy with the changes (step 9) and the thread replies are posted:

1. Collect only the decisions and instructions the user gave in this chat about how to implement the selected comments (answers to `AskQuestion`, explicit directions such as a chosen name or library). Leave out reasoning, chatter, and anything about unselected comments.
2. If the user gave no such guidance, skip this step and say so.
3. Draft one top-level pull request comment (not a thread reply) and show it to the user. Wait for approval before posting.
4. Post it with the GitHub MCP tool for adding a pull request or issue comment, discovered at runtime via `GetDynamicTools`. Do not hard-code its name.
5. Never include secrets, tokens, local file paths outside the repo, or content from unrelated chats.

Comment format:

```markdown
Context for the changes in this round:
- <decision or instruction, one line each, tagged with the comment it relates to, e.g. "debounce.ts: use lodash.debounce">
```

## 11. Hand over to reflect-review

After step 10, use `AskQuestion` to ask whether to run `/reflect-review` now, so repeated reviewer patterns become guards in the repo's Cursor rules. If the user says yes, read `../reflect-review/SKILL.md` and follow it with the comments from this run.

## Do not

- Push, merge, or open PRs.
- Resolve review threads (the reviewer does this).
- Use `gh` or REST when GitHub MCP is unavailable (stop and ask to connect MCP instead).
- Draft or post any GitHub reply or comment before the user has said they are happy with the code changes.
- Post any reply or comment without showing the draft first.
- Reply to comments classified **Need more information** unless the user explicitly asks.
