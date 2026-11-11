# SQL Semantic Correctness — Concern 3

Pinned commit: `decb6196c2c1e6ed421d393a642f0c844cc333ba`

## Verdict

PASS

## Clean Account

- **Concern 3 — SQL formatting and semantic correctness**: Checked both new methods in
  `crates/chirp-server/src/repository/postgres.rs`. All SQL query strings were read
  directly; no correctness assumptions were made from formatting.

  **`public_chirps_with_authors` (line 614)**

  *Chirp-fetch SQL (line 625).*
  `WHERE removed = FALSE AND ($1::BIGINT IS NULL OR created_at < $1) ORDER BY created_at DESC, id DESC LIMIT $2`.
  Syntax is well-formed. Parameter bindings: `$1` = `before: Option<i64>` (cast to `BIGINT`),
  `$2` = `i64::from(limit) + 1`. The null-cursor case is handled by `$1::BIGINT IS NULL`,
  which evaluates to `TRUE` when `before` is `None`, leaving all rows eligible — correct.
  The before-filter uses `<` (strictly less than), matching the trait docstring "strictly
  before that value" and the in-memory reference (`chirp.created_at.as_millis() < b`).
  `removed = FALSE` excludes soft-removed chirps. `ORDER BY created_at DESC, id DESC`
  gives reverse-chronological order with a stable tiebreaker on `id DESC`, matching the
  in-memory sort. `LIMIT $2` fetches `limit + 1` rows.

  *User-batch-fetch SQL (line 652).*
  `WHERE id = ANY($1::BIGINT[])`. Syntax is well-formed; `ANY($1::BIGINT[])` is correct
  PostgreSQL array-containment syntax. `$1` is bound to `&author_ids` after the chirp
  page is truncated, so the batch covers only the authors of the final `limit` chirps,
  not the extra sentinel row.

  *has_more (around line 637).* `chirp_rows.len() > limit as usize` before truncation,
  then `.take(limit as usize)` — matches the in-memory pattern exactly.

  *Two-query join assembly (around line 661–685).* The Rust assembly looks up each
  chirp's author in a `HashMap` and propagates `ServerError::Internal` if any author is
  absent. A chirp cannot appear in the result without its author; the method either
  returns all pairs or fails. This is a stricter contract than the in-memory reference,
  which silently drops orphaned chirps via `filter_map`. The difference is a behavioral
  divergence between implementations, not a SQL defect; under normal foreign-key
  constraints the error path is unreachable. Reviewed and found sound for this concern.

  **`get_user_chirps_by_username` (line 694)**

  *User-lookup SQL (line 707).*
  `WHERE LOWER(username) = LOWER($1)`. Syntax is well-formed. Case-insensitive comparison
  is implemented by applying `LOWER()` to both sides, matching the trait's
  "case-insensitive" requirement.

  *Chirp-count SQL (line 725).*
  `WHERE author_id = $1 AND removed = FALSE`. Counts all non-removed chirps by the user.
  Soft-removed chirps are excluded. Correct.

  *Chirp-page SQL (line 737).*
  `WHERE author_id = $1 AND removed = FALSE AND ($2::BIGINT IS NULL OR created_at < $2) ORDER BY created_at DESC, id DESC LIMIT $3`.
  Syntax is well-formed. Parameter bindings: `$1` = `user_id_col`, `$2` = `before:
  Option<i64>`, `$3` = `i64::from(limit) + 1`. Before-filter uses `<` (strictly less
  than), matching the in-memory reference. `removed = FALSE` excludes soft-removed chirps.
  Ordering and tiebreaker match the in-memory reference and `public_chirps_with_authors`.
  Null-cursor handling is identical in structure to the first method.

  *has_more (lines 748–756).* `chirp_rows.len() > limit as usize` before the
  `.take(limit as usize)` iterator, matching the in-memory reference (`page.len() >
  limit_usize` before `truncate`).

  No semantic gaps found across all seven checks: syntax, before-filter operator, null-cursor
  handling, ordering and tiebreaker, soft-removed exclusion, two-query join safety, and
  case-insensitive username lookup.
