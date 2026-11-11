## Verdict

FINDINGS

---

## Findings

### Finding 1: `public_timeline` doc comment claims ISO 8601; the server type is `i64`

- **Location**: `crates/chirp-frontend/src/api.rs`, line 217 at commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- **Principle at stake**: A public method's documentation must describe the wire contract it actually implements. When the doc says one format and the server enforces another, any new caller following the doc gets a 422.
- **Why it matters**: The method doc at line 217 reads "Query params: `before` (ISO 8601 cursor), `limit` (1-50, default 20)." The server's `PublicTimelineQuery.before` is `Option<i64>` (lines 151–155 of `crates/chirp-types/src/api.rs`), which serde deserializes from a decimal integer query string. If a caller reads the doc and passes an ISO 8601 string such as `"2024-01-15T10:30:00Z"`, the server returns a 422 — the string is not parseable as `i64`. Both current callers work correctly: `landing.rs` line 201 and `public_profile.rs` line 244 each extract an `i64` timestamp from the response and call `.to_string()`, producing a decimal integer string (e.g., `"1700000000000"`) that the server parses without error. The runtime type contract is consistent; the documentation is not.
- **Severity**: non-blocking
- **Satisfying condition**: The sentence at `crates/chirp-frontend/src/api.rs` line 217 must replace "before (ISO 8601 cursor)" with wording that matches the actual wire format, e.g., "before (Unix timestamp in milliseconds as a decimal integer string)." The same correction should be applied to the module-level pagination notes in `crates/chirp-frontend/src/landing.rs` line 19 and `crates/chirp-frontend/src/public_profile.rs` line 15, both of which describe the cursor as "ISO 8601" when the stored and transmitted value is an `i64` millisecond timestamp.

---

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

  No semantic gaps found across all seven checks: syntax, before-filter operator,
  null-cursor handling, ordering and tiebreaker, soft-removed exclusion, two-query join
  safety, and case-insensitive username lookup.

- **Concern 4 — Spec deviation (`before` milliseconds vs ISO 8601)**: Checked
  `PublicTimelineQuery.before` in `crates/chirp-types/src/api.rs` lines 142–155 at the
  pinned commit: the type is `Option<i64>`, the deviation from the external ISO 8601 spec
  is acknowledged in the struct doc comment with a stated rationale (consistency with the
  domain `Timestamp` type). Traced both callers of `public_timeline` and
  `public_user_profile` in `crates/chirp-frontend/src/landing.rs` (line 201) and
  `crates/chirp-frontend/src/public_profile.rs` (line 244): both extract an `i64`
  timestamp from the most recent response item, convert with `.to_string()`, and pass the
  resulting decimal string. The server parses this as `i64` without error — no live type
  mismatch exists. The spec deviation is bounded: server documentation is accurate, callers
  are correct. The finding is the wrong format claim in the client method doc at
  `crates/chirp-frontend/src/api.rs` line 217, which would cause any new caller following
  the doc to pass an ISO 8601 string and receive a 422. → Finding 1 (non-blocking).
