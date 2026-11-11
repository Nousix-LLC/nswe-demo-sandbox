# Task: Spec Deviation Analysis — Concern 4

## Task Specification

**Slug**: SUBTASK_spec-deviation
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective

Verify client-server type consistency for the `before` pagination cursor and assess
whether the documented deviation from the external spec is a blocker.

### Context

This task covers concern 4 from the spoke-correctness brief. See `../_GLOBAL.md` for PR
details. The pinned commit is `decb6196c2c1e6ed421d393a642f0c844cc333ba`.

The concern: `PublicTimelineQuery.before` is `Option<i64>` (milliseconds since epoch), and
a code comment in `chirp-types/src/api.rs` explicitly acknowledges the deviation from the
external spec, which describes `before` as an ISO 8601 string. The question is whether the
client and server are consistent with each other and whether the deviation needs to be
resolved before merge.

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Hub context | `../_GLOBAL.md` | Concern assignment, output schema, constraints |
| Output schema | `../../contracts/findings_schema.md` | FINDINGS.md structure |
| `api.rs` (types) | `crates/chirp-types/src/api.rs` at HEAD | Server-side `PublicTimelineQuery.before` type |
| `api.rs` (frontend) | `crates/chirp-frontend/src/api.rs` at HEAD | Frontend `public_timeline` method |

Access files via:
```bash
gh api "repos/Nousix-LLC/nswe-demo/contents/PATH?ref=decb6196c2c1e6ed421d393a642f0c844cc333ba" \
  --jq '.content' | base64 -d
```

### Key locations to read

**`crates/chirp-types/src/api.rs`** (server-side type, approximately lines 144–155):
```rust
/// `before` is a pagination cursor expressed as a Unix timestamp in milliseconds (the `created_at`
/// Note: the external spec describes `before` as an ISO 8601 string; this implementation uses
/// milliseconds-since-epoch for consistency with the domain Timestamp
pub struct PublicTimelineQuery {
    /// Pagination cursor — return items with `created_at` strictly before this timestamp
    /// (milliseconds since the Unix epoch).
    pub before: Option<i64>,
```
The server-side type is `Option<i64>` — deserializes from an integer query parameter.

**`crates/chirp-frontend/src/api.rs`** (client-side method and helpers, approximately
lines 217–220 and 340–343):
```rust
/// Query params: `before` (ISO 8601 cursor), `limit` (1-50, default 20).
pub async fn public_timeline(&self, before: Option<&str>, ...) -> ...

fn public_chirps_query_params(before: Option<&str>, limit: Option<u32>) -> Vec<(String, String)> {
    if let Some(b) = before {
        params.push(("before".to_string(), b.to_string()));
```

The frontend method signature accepts `Option<&str>` and passes the string value directly
to the HTTP query parameter. The doc comment says "ISO 8601 cursor" — inconsistent with the
server's `Option<i64>`.

---

## Process Specification

1. **Read both files** at the key locations above. Confirm that the types are as described.

2. **Determine runtime consistency**: When `public_timeline` is called with a `before` value,
   what string does it send? The server's `axum` deserialization of `PublicTimelineQuery`
   will attempt to parse `before` as `i64`. If the caller passes an ISO 8601 string like
   `"2024-01-15T10:30:00Z"`, the server receives a string it cannot parse as `i64` and will
   return a 422 / 400. If the caller passes a millisecond integer as a string (e.g., `"1705318200000"`),
   parsing succeeds.

3. **Trace actual call sites**: Does any code currently call `public_timeline` with a
   `before` value? Search `crates/chirp-frontend/` for callers of `public_timeline`. If
   no current caller passes a non-None `before`, the type mismatch is a documentation issue
   and latent runtime risk. If a caller does pass a value, determine what it passes.

4. **Assess severity**: Apply these criteria:
   - Is this a *current* runtime failure (a caller today passes an ISO 8601 string → server
     returns 4xx)? → blocker
   - Is this a *latent* failure (the type contract is wrong; a future caller following the
     doc comment would fail)? → evaluate based on whether spec alignment is a merge
     requirement for this PR
   - Is the acknowledged deviation clearly bounded (the comment states it, the type enforces
     it, callers must use milliseconds, and callers currently do)? → non-blocking
   - Is the frontend doc comment misleading enough that it would cause the next author to
     pass an ISO 8601 string? → blocker or non-blocking depending on severity judgment

5. **Check the acknowledgment quality**: The comment in `chirp-types/src/api.rs` notes the
   deviation. Does it tell the reader what to do? Does the frontend doc comment contradict it?

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| Filename | `FINDINGS.md` |
| Format | Markdown |
| Location | `SUBTASK_spec-deviation/` (this workspace) |

Structure: per `../../contracts/findings_schema.md`. This is a partial findings file
covering concern 4 only. The synthesis child reads it to build the final FINDINGS.md.

The `## Clean Account` section MUST have exactly one entry:
- **Concern 4 — Spec deviation (`before` milliseconds vs ISO 8601)**: ...

---

## Success Criteria

- Both `chirp-types/src/api.rs` and `chirp-frontend/src/api.rs` read at pinned commit
- Current callers of `public_timeline` traced to determine whether a live type mismatch exists
- Severity of the frontend doc comment inconsistency assessed and justified
- Findings conform to `../../contracts/findings_schema.md`
- Concern 4 has exactly one entry in `## Clean Account`

---

## Suggested Methodology Files

Domain Mapping match: **Code review** → Primary: `Code Review`, Supporting: `Core`
Also applicable: **Rust code review** → `Rust` bundle for type contract analysis

Specific files:
- `code-review/CodeReview_Checklist_Methodology.md` — API contract rows: does the
  documented interface match the actual runtime behavior?
- `core/BestPractices_Error_Handling_Methodology.md` — what happens when the type
  contract is violated? Parse failure path, error surfaced to caller
- `code-review/CodeReview_Feedback_Guidelines_Methodology.md` — severity calibration:
  documentation inconsistency that causes latent parse failure vs current failure

These are suggested starting points; load fewer if inapplicable, more if needed.

## Inherited Constraints

- Findings point at repository file paths and line numbers at pinned commit
  `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- Do not post to the PR
- Prose in FINDINGS.md must pass the plain-voice bar in `../../contracts/findings_schema.md`
- Repository: `Nousix-LLC/nswe-demo` only

## Out-of-Scope

- Concern 3 (SQL correctness) — belongs to `SUBTASK_sql-correctness`
- SQL query analysis — not applicable to this concern
- Testing depth — belongs to `spoke-tests`
- Synthesis — belongs to `SUBTASK_synthesis`
