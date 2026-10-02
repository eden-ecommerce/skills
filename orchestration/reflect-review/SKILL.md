---
name: reflect-review
description: Turn pull request review comments into guards in the repo's Cursor rules, so the agent stops repeating the patterns reviewers flag. Uses this chat when /review-comments already ran; otherwise fetches every review comment on the open pull request and compares each thread's diff with the current file. Proposes each guard, writes only the approved ones to `.cursor/rules/`, and reports the detected patterns in plain prose. Use when the user says /reflect-review, after /review-comments, or when they want reviewer comments turned into rules.
---

# reflect-review

Propose first. Write rule files only after the user approves. Do not implement the review comments.

## 1. Collect the comments

This pull request only.

**`/review-comments` already ran in this chat.** Use its comments and the edits made for them. For each, keep the file and line, the reviewer, the quoted comment, the outcome (**Suggested change** or **Need more information**), and what was actually changed. Do not fetch them again.

**It has not run.** Fetch them yourself. Do not ask the user to run `/review-comments`.

1. Read `.git/HEAD` for the branch (`ref: refs/heads/...`) and `.git/config` for `remote "origin"`, then derive `owner/repo`. Prefer file reads over shell `git`. If the user gave a pull request URL or number, use that.
2. Call `GetDynamicTools` with pattern `github`. Discover tool names at runtime. If no GitHub namespace is listed, or its status is `needsAuth` or `error`, stop and tell the user to connect GitHub MCP in Cursor Settings. Do not fall back to `gh`. If auth is needed, call `mcp_auth` for that namespace, then retry.
3. Find the open pull request whose head branch matches the current branch. If none exists, stop and say the branch may not be pushed or has no open pull request.
4. Fetch every review comment on it, resolved and unresolved. Skip authors whose login ends with `[bot]`, and the author's own replies that only acknowledge a thread.
5. For each comment, read the diff hunk on the review thread, then the current file at those lines. The hunk is what the reviewer saw. Where the current file differs from that hunk, that difference is the change the comment caused. Where they still match, no change was made yet. Keep the comment anyway, because its wording can still be a pattern.

## 2. Find the patterns

For each comment, ask: "If a rule had said this, would the agent have written the code correctly first time?"

Keep a comment as a pattern when the fix generalises beyond this line. A comment with no code change yet still counts when its wording states a rule that would have stopped the flagged code. Typical examples: naming, import paths, file placement, design tokens, translation strings, accessibility, type safety, React Query or InstantSearch usage.

Discard it, and say why in one line, when it is:

- A one-off bug or typo.
- A product, design, or architecture decision specific to this feature.
- **Need more information** with no answer from the reviewer yet.
- Something a linter, formatter, or type check already catches.

Group comments that point at the same pattern into one guard. Note how many comments it covers; repeats are the strongest signal.

## 3. Check existing rules

In the repo the pull request belongs to, read `.cursor/rules/*.mdc`, `.cursorrules`, and `AGENTS.md` if present. Search them for the pattern's topic.

- **Not covered.** Propose a new guard.
- **Covered but missed.** The rule exists and the agent still broke it. Propose making that rule more concrete (add a bad and good example, or move it higher), not a duplicate.
- **Covered and the reviewer disagrees with it.** Do not propose a guard. Flag it as a conflict for the user to settle with the reviewer.

## 4. Pick the destination

Append to the closest existing rule file by topic. Create a new `.cursor/rules/<topic>.mdc` only when nothing fits, using kebab-case and this frontmatter:

```markdown
---
description: <one line, what the rule guards against>
alwaysApply: true
---
```

Use `globs:` instead of `alwaysApply: true` when the pattern only applies to certain files (for example `**/*.tsx`).

## 5. Write a good guard

A guard is short and tells the agent what to do, with code where code helps:

````markdown
## <Short imperative name>

<One sentence: what to do, or what not to do.>

```tsx
// Bad
<code the reviewer flagged, trimmed>

// Good
<code after the fix, trimmed>
```

<One sentence on why, only if the reason is not obvious from the example.>
````

Rules for the guard text:

- One pattern per guard. Under 15 lines.
- Use code from this pull request, trimmed to the essentials. No invented examples. The bad block comes from the review hunk. The good block comes from the current file, and only when that file actually differs.
- State the rule, not its history. No pull request numbers, reviewer names, or dates in the rule file.
- Match the tone, headings, and RFC 2119 words (MUST, SHOULD) the target file already uses.
- Do not restate what a linter, the type checker, or an existing rule already enforces.

## 6. Present the proposals

Before showing anything, run the plain-writing check (below) on the summary, the cards, and every guard text.

Summary first; its count must match the number of cards:

```markdown
## Review patterns found

**Summary:** 3 patterns from 5 comments. 2 new guards, 1 strengthened rule.
```

Then one card per pattern, separated by `---`:

```markdown
### 1. Import design components from their own file
**From:** 2 comments by @reviewer (`blocks/Basket/ItemList.tsx:12`, `components/search/SearchPills.tsx:4`)
**Destination:** new guard in `.cursor/rules/no-barrels.mdc`
**Why:** The reviewer flagged barrel imports twice; the existing rule has no example.

<guard text from step 5>
```

Then list what was discarded and any conflicts from step 3, one line each.

No tables or HTML in the output.

## 7. Get approval

Use `AskQuestion` with **allow_multiple: true**: one option per card, plus **Skip all**. Do not write anything until the user chooses.

## 8. Apply

For each approved card:

1. Re-read the destination file and check nobody has added the same guard meanwhile.
2. Add the guard where it fits the file's structure. Do not reorder or reword the rest of the file.
3. Keep each rule file under about 50 lines. If a file would grow past that, ask before splitting it.

Write only to `.cursor/rules/`, `.cursorrules`, or `AGENTS.md` in the pull request's repo.

## 9. Report

Run the plain-writing check on this report too. End with:

```markdown
## Guards added

- `.cursor/rules/no-barrels.mdc`: import design components from their own file.

## Patterns detected but not added

- <pattern>: <one line why, for example skipped by you, or needs a decision from @reviewer>.
```

The second list tells the user which detected patterns could still become guards later.

## Plain-writing check

If `/unslop` is available, apply it. If not, check the text against these instead:

- No em dashes. Use a full stop or a comma.
- Plain words: "use" not "leverage" or "utilise". Drop "crucial", "ensure", "robust", "seamless".
- Active voice: name who does what.
- Whole sentences with their articles and verbs. No arrows or symbol shorthand.
- Sentence-case headings.
- No chatbot phrases ("Great question", "I hope this helps").

## Do not

- Implement review comments or edit application code.
- Commit, push, or post anything to GitHub.
- Write guards for skipped cards or unanswered **Need more information** comments.
- Edit rules in repos other than the pull request's repo.
