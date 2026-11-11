# Task: SQL Correctness + Spec Deviation Analysis — PR #263

## Task Specification

**Slug**: spoke-correctness
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective

Assess SQL correctness and spec conformance in PR #263 on `Nousix-LLC/nswe-demo`, covering
concerns 3 and 4 from the parent spoke brief.

### Context

This task is part of the code-quality review decomposition. See `../_GLOBAL.md` for PR details,
the full concern assignment table, and `../contracts/` for the FINDINGS.md output schema.

**Concerns assigned to this spoke:**

3. **SQL formatting and semantic correctness** (`crates/chirp-server/src/repository/postgres.rs`):
   The PostgreSQL implementations of `public_chirps_with_authors` and `get_user_chirps_by_username`
   embed SQL as single-line strings with mangled whitespace (spaces instead of `\` line
   continuations), unlike the multi-line format used elsewhere. Verify:
   - Is the SQL syntactically correct despite the formatting?
   - Does the SQL match the semantics specified in the trait docstrings in `mod.rs`?
   - Specifically for `public_chirps_with_authors`: does the JOIN correctly embed the author
     in each chirp? Does the `before`/cursor filtering match what the trait specifies?
   - Specifically for `get_user_chirps_by_username`: does the WHERE clause match the username
     filter semantics? Are results ordered as the trait requires?

4. **Spec deviation: `before` as milliseconds** (`crates/chirp-types/src/api.rs`,
   `crates/chirp-frontend/src/api.rs`):
   `PublicTimelineQuery.before` is documented in the type as milliseconds since epoch; the
   external spec describes it as ISO 8601. The deviation is acknowledged in a code comment.
   Verify:
   - Is client-side usage consistent with the server-side expectation? Does the frontend pass
     a millisecond integer (or integer string) where the server expects a millisecond integer?
   - Is the type system enforcing the right contract, or could a caller pass an ISO 8601 string
     and have it silently accepted or rejected with a confusing error?
   - Is the acknowledged deviation a blocker (needs spec or code alignment before merge) or
     non-blocking (acceptable under a known-deviation policy)?

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Hub context | `../_GLOBAL.md` | Concern assignments, pin commit, output schema |
| Contract schema | `../contracts/findings_schema.md` | FINDINGS.md structure |
| `postgres.rs` | `crates/chirp-server/src/repository/postgres.rs` at HEAD | SQL queries under review |
| `mod.rs` | `crates/chirp-server/src/repository/mod.rs` at HEAD | Trait docstrings (specification) |
| `in_memory.rs` | `crates/chirp-server/src/repository/in_memory.rs` at HEAD | Reference implementation semantics |
| `api.rs` (types) | `crates/chirp-types/src/api.rs` at HEAD | `PublicTimelineQuery.before` type + comment |
| `api.rs` (frontend) | `crates/chirp-frontend/src/api.rs` at HEAD | Frontend usage of `before` field |

Access files via:
```bash
gh api "repos/Nousix-LLC/nswe-demo/contents/PATH?ref=decb6196c2c1e6ed421d393a642f0c844cc333ba" \
  --jq '.content' | base64 -d
```

For SQL analysis: read the query string carefully. The single-line format makes visual scanning
hard, but the SQL is still parseable. Check JOIN conditions, WHERE clauses, ORDER BY, and
parameter binding ($1, $2, etc.) against the trait docstring semantics. Do not assume correctness
from formatting — verify against the in-memory implementation as a semantic reference.

---

## Process Specification

For concern 3 (SQL):
- Read `mod.rs` trait docstrings to establish the semantic contract for each method
- Read the `postgres.rs` SQL queries and parse them mentally (or note them out for analysis)
- Cross-check: does the SQL return the same shape and filtering semantics the trait specifies?
- Compare against `in_memory.rs` as a reference for intended behavior
- Note any semantic differences (not just formatting) as findings

For concern 4 (spec deviation):
- Read `api.rs` type definition for `PublicTimelineQuery.before` and its comment
- Read the frontend `api.rs` to find how `before` is passed when calling the public timeline
- Determine if the runtime types are consistent (integer vs string) on both sides
- Assess whether the acknowledged deviation is documented clearly enough that future callers
  won't be surprised

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| Filename | `FINDINGS.md` |
| Format | Markdown |
| Location | `spoke-correctness/` (this workspace) |

Structure: per `../contracts/findings_schema.md`.

---

## Success Criteria

- Concerns 3 and 4 each appear in the Clean Account
- For concern 3: SQL syntax and JOIN/filter semantics verified against trait docstrings — not
  assumed correct from formatting alone
- For concern 4: client-server type consistency determined and severity assigned
- Each finding includes a verifiable satisfying condition
- No internal infrastructure details in any finding

---

## Suggested Methodology Files

Domain Mapping match: **Code review** → Primary: `Code Review`, Supporting: `Core`
Also applicable: **Rust code review** → `Rust` bundle for type-level analysis

Specific files:
- `code-review/CodeReview_Checklist_Methodology.md` — correctness rows: does the code do
  what it says it does?
- `core/BestPractices_Error_Handling_Methodology.md` — relevant for concern 4: what happens
  when the type contract is violated at runtime?
- `code-review/CodeReview_Process_Methodology.md` — verify the SQL against the spec; green
  compiles are not a correctness proof

These are suggested starting points; load fewer if inapplicable, more if needed.

## Out-of-Scope Methodologies

- `testing/` bundle — test depth is handled by `spoke-tests`
- `synthesis/` bundle — belongs to `spoke-synthesis`

## Inherited Constraints

- Findings point at repository file paths and line numbers at pinned commit
  `decb6196c2c1e6ed421d393a642f0c844cc333ba`; no host paths, private IPs, or infrastructure details
- Do not post to the PR
- SQL correctness verdict must be based on reading the actual query, not on assuming the formatter
  would not introduce bugs
- Prose in FINDINGS.md must pass the plain-voice bar in `../contracts/findings_schema.md`
- Repository: `Nousix-LLC/nswe-demo` only
