---
name: construct-query
description: >-
  Build or speed up MySQL SELECTs. Semantics frozen on existing queries — same
  rows, cols, values. Use Percona PMM + EXPLAIN before/after. Caveman ultra
  voice in this file. Planning/new tables: guard overnormalization.
agents:
  - cursor
---

/caveman ultra

## Invariant

Optimize speed, never meaning. Existing query → same result set, same task validity. Diff rows/cols/values → rollback, not ship.

New query / new table → correct types, sane joins, no fantasy normalization.

## Baseline (PMM + EXPLAIN)

Before change:
1. PMM Query Analytics → pick query (time, count, rows examined).
2. `EXPLAIN` / `EXPLAIN ANALYZE` (MySQL 8.0.18+) → note `type`, `key`, `rows`, `Extra` (`Using filesort`, `Using temporary`).
3. Save plan + sample output hash or row count for window.

After change: same checks. Faster only if plan + PMM metrics improve **and** result identical.

## Compare + learn loop

When proposing query change or new table shape:

1. Run `EXPLAIN` on **both** (old vs new, or option A vs B).
2. Pull PMM metrics for prod-like load if available (time, rows examined, lock time).
3. Report finding: what changed in plan, metric delta, semantic check passed.
4. **Proven win** (same output, measurably faster, repeatable plan) → append one line to [Learned optimizations](#learned-optimizations) below. Format:

   `- [YYYY-MM-DD] <table/query>: <pattern> → <replacement>. EXPLAIN: <key delta>. PMM: <metric delta>.`

5. **No win or semantic risk** → do not append. Note in PR/chat only.

User must approve skill file edit before append. Never append speculative or one-off luck.

## Planning / new tables — overnormalization

**Trigger:** planning mode, schema design, "add table", master/sub-plan DB work.

Stop split when reads will always need the data together:

| Trap | Fix |
|------|-----|
| `users` + `user_emails` + `user_profiles` + `user_settings` — strict 1:1, always joined | One `users` row (or auth + profile only if security boundary real) |
| EAV (`entity_id`, `attr`, `value`) for sparse attrs | MySQL `JSON` col on parent — inline read, no attr explosion join |
| Lookup table for 5 static statuses | `TINYINT` + app dict |
| Normal form for normal form's sake | Denorm when read path = 1 query, write path still safe |

Ask before split: "Will any SELECT need this without the parent?" No → same table.

Categories → narrow type (`TINYINT`/`SMALLINT`/`ENUM` sparingly), not `VARCHAR(255)` repeat strings.

## Index

- Composite: equality cols left → range cols right. `(tenant_id, created_at)` for `tenant_id = ? AND created_at > ?`.
- Don't index everything. Index = query access pattern + cardinality.
- `SELECT` only needed cols. Wide rows → more I/O.
- Sargable `WHERE`: no fn on indexed col (`DATE(created_at) = ?` → range on raw col).

## Pagination — WHERE beat take/skip

`take(N)` + `skip(M)` (ORM) → `LIMIT N OFFSET M`. Deep `OFFSET` → DB reads + discards M rows every page. Slow at scale.

**Prefer keyset / seek pagination** — `WHERE` on indexed cursor col:

```sql
-- page 1
SELECT id, name FROM users ORDER BY id ASC LIMIT 100;

-- page 2+ (cursor = last id from prev page)
SELECT id, name FROM users
WHERE id > :last_id
ORDER BY id ASC
LIMIT 100;
```

Multi-col sort → composite cursor:

```sql
WHERE (created_at, id) > (:last_created_at, :last_id)
ORDER BY created_at ASC, id ASC
LIMIT 100;
```

Index must match `ORDER BY` + cursor cols. `OFFSET` OK only for tiny tables or admin one-offs — not prod list APIs.

ORM mapping:
- Laravel `skip/take` → replace with `where('id', '>', $cursor)->orderBy('id')->take(100)`
- Prisma `skip/take` → `where: { id: { gt: cursor } }, orderBy: { id: 'asc' }, take: 100`

## Shrink before join

Filter early. CTE or derived table OK when semantically same:

```sql
WITH refined_orders AS (
  SELECT id, customer_id
  FROM orders
  WHERE order_date >= '2026-01-01'
)
SELECT ro.id, c.email
FROM refined_orders ro
JOIN customers c ON ro.customer_id = c.id;
```

Semi-join / `EXISTS` often beats fat `IN (subquery)` on big tables — profile both.

## Batch / migration

Multi-step heavy job → temp table, index subset, run steps. Break monolith query.

```sql
CREATE TEMPORARY TABLE temp_active_users (
  id BIGINT PRIMARY KEY
) ENGINE=InnoDB
AS
SELECT id FROM users WHERE last_login > NOW() - INTERVAL 30 DAY;

UPDATE user_metrics um
JOIN temp_active_users t ON t.id = um.user_id
SET um.status = 'active';
```

Prefer `JOIN` over `IN (SELECT …)` on large sets when plan says so.

## Latest / extreme per group

No universal winner. Profile:
- `ROW_NUMBER()` window (MySQL 8+)
- self-join anti-join (`LEFT JOIN … WHERE newer.id IS NULL`)
- grouped `MAX(id)` + join back

Pick smallest `rows examined` with **identical** output.

## Txn (writes near queries)

Short txn. Fetch + external I/O **outside** txn. Open → write → commit. Long lock = concurrency death.

## Ship checklist

- [ ] PMM baseline captured
- [ ] `EXPLAIN` before/after (both variants if comparing)
- [ ] Result set identical (count + spot check or hash)
- [ ] No new full scan where index seek existed
- [ ] Planning work: overnormalization check done
- [ ] List APIs: keyset pagination, not deep `skip/take`
- [ ] Proven win → user-approved append to Learned optimizations
- [ ] Skill voice: caveman ultra in agent replies while this skill active

## Learned optimizations

Repo-specific wins. Append only via compare + learn loop. Newest first.

<!-- agents append below this line -->
