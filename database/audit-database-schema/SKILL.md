---
name: audit-database-schema
description: >-
  Audits schema.sql or a user-exported .sql dump against codebase database queries.
  Identifies column bloat, missing optimizations, and redundant/missing indexes.
  Generates a strict db_audit_report.md. Use when auditing schema, reviewing a
  mysqldump/pg_dump/phpMyAdmin export, or optimizing indexes from an attached .sql file.
  Caveman ultra voice: terse, highly analytical, zero fluff.
agents:
  - cursor
---

/caveman ultra

## Invariant

Optimize structure, align with actual access patterns. Schema exists to serve queries.
No guessing—prove missing indexes or bloated columns by mapping ingested DDL directly to codebase ORM/SQL calls.
End state: Generate `db_audit_report.md` with actionable, measurable fixes.

## Phase 0: Ingest SQL source

Resolve **one** schema source, in this order:

1. User-attached / mentioned `.sql` (dump or schema export).
2. Workspace `schema.sql`.
3. Other workspace `*.sql` the user points at (`dump.sql`, `database.sql`, `backup.sql`).

Ambiguous → ask. None → stop. Record the chosen path; cite it in the report.

Normalize to DDL. Full dumps are data + schema — **schema only** for this audit.

*   **Keep:** `CREATE TABLE`, `ALTER TABLE`, `CREATE INDEX` / `UNIQUE INDEX`, `PRIMARY KEY`, `FOREIGN KEY`, `CONSTRAINT`, `CREATE VIEW`.
*   **Drop:** `INSERT` / `UPDATE` / `DELETE`, `LOCK`/`UNLOCK TABLES`, dump session `SET`/`USE`, `COPY` data, mysqldump/pg_dump headers.
*   **Large dump:** do not read the whole file. Extract DDL with `rg` (`CREATE TABLE|ALTER TABLE|CREATE (UNIQUE )?INDEX|CONSTRAINT|FOREIGN KEY|PRIMARY KEY`). Skip INSERT blobs.

Treat extracted DDL as the schema. Same proof bar as a dedicated `schema.sql`.

## Phase 1: Schema X-Ray (Analyze DDL)

Read the ingested DDL. Scan for structural waste:

*   **Column Bloat:** Flag `VARCHAR(255)` used for ENUMs/statuses. Demand `TINYINT` or explicit `ENUM`.
*   **NULL Abuse:** Flag nullable columns that logically require data. `NULL` defeats index efficiency.
*   **Orphaned Foreign Keys:** Flag relational columns (`user_id`, `company_id`) lacking strict `FOREIGN KEY` constraints or supporting indexes.
*   **Zombie Columns:** Identify columns in schema never referenced in codebase.
*   **Over-normalization:** Flag 1:1 tables that share the same exact read lifecycle (e.g., `users` + `user_prefs` always joined).

## Phase 2: Codebase Query Hunt

Search workspace for DB interactions (Raw SQL, Prisma, TypeORM, Eloquent, Hibernate, etc.).
Map every discovered query to the ingested DDL.

Extract:
1.  **Filters:** Every `WHERE` clause.
2.  **Sorts:** Every `ORDER BY` clause.
3.  **Joins:** Every `JOIN` condition.
4.  **Selects:** Check for `SELECT *` vs explicit column projection.

## Phase 3: The Match-Up (Indexes & Constraints)

Cross-reference Phase 1 (Schema) with Phase 2 (Queries).

*   **Missing Composite Indexes:** If query does `WHERE tenant_id = ? AND status = ? ORDER BY created_at`, demand index `(tenant_id, status, created_at)`.
*   **Left-to-Right Rule:** Equality columns first, range columns (`>`, `<`, `BETWEEN`) last. Flag indexes violating this.
*   **Redundant Indexes:** Flag index `(user_id)` if `(user_id, created_at)` already exists.
*   **Sargability Traps:** Flag queries using functions on indexed columns (e.g., `WHERE DATE(created_at) = ?`). Index is bypassed.
*   **Pagination:** Flag deep `OFFSET` or ORM `skip/take`. Demand keyset/cursor pagination mapped to a sequenced index.

## Phase 4: Generate Audit Report

Do not output findings in chat. Write exactly to `db_audit_report.md` using this exact structure:

```md
# Database Optimization & Scalability Audit

Source: `[path to schema.sql or exported .sql]`

## 1. Executive Summary
[High-level impact: X unused columns, Y missing critical indexes, Z high-risk queries.]

## 2. Schema Bloat & Type Optimizations
- **[Table Name]**: `[column_name]` -> Change `VARCHAR(255)` to `TINYINT` (Only stores 4 distinct statuses).
- **[Table Name]**: `[column_name]` -> Remove (Never queried in codebase).

## 3. Index & Key Review
- **Missing Index**: `[Table Name]` needs `(col1, col2)` for query found in `[filepath:line]`.
- **Redundant Index**: Drop `idx_name` on `[Table Name]` (Covered by `idx_larger_name`).

## 4. Query Anti-Patterns (Codebase fixes)
- **Non-Sargable Query**: `[filepath:line]` -> `WHERE YEAR(date) = 2026`. Fix: `WHERE date >= '2026-01-01' AND date < '2027-01-01'`.
- **Pagination Risk**: `[filepath:line]` -> Uses deep offset. Convert to cursor pagination on `(id)`.
- **Over-fetching**: `[filepath:line]` -> Selects all columns but only uses `id` and `name`.

## 5. Action Plan (Execution Order)
1. [Highest impact / lowest effort schema change]
2. [Critical missing index creation]
3. [Codebase query rewrite]
```
