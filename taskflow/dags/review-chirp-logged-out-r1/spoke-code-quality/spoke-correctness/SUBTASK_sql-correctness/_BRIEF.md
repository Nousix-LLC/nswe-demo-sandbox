# Task: SQL Semantic Correctness — Concern 3

## Task Specification

**Slug**: SUBTASK_sql-correctness
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective

Verify SQL formatting and semantic correctness for the two new methods added in PR #263:
`public_chirps_with_authors` and `get_user_chirps_by_username` in
`crates/chirp-server/src/repository/postgres.rs`.

### Context

This task covers concern 3 from the spoke-correctness brief. See `../_GLOBAL.md` for PR
details. The pinned commit is `decb6196c2c1e6ed421d393a642f0c844cc333ba`.

The concern: both methods embed SQL as single-line strings with mangled whitespace, unlike
the multi-line format used elsewhere in the file. The question is whether the SQL is
syntactically correct and semantically faithful to the trait specification.

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Hub context | `../_GLOBAL.md` | Concern assignment, output schema, constraints |
| Output schema | `../../contracts/findings_schema.md` | FINDINGS.md structure |
| `postgres.rs` | `crates/chirp-server/src/repository/postgres.rs` at HEAD | SQL under review |
| `mod.rs` | `crates/chirp-server/src/repository/mod.rs` at HEAD | Trait docstrings (the specification) |
| `in_memory.rs` | `crates/chirp-server/src/repository/in_memory.rs` at HEAD | Reference implementation |

Access files via:
```bash
gh api "repos/Nousix-LLC/nswe-demo/contents/PATH?ref=decb6196c2c1e6ed421d393a642f0c844cc333ba" \
  --jq '.content' | base64 -d
```

### Key locations to read

**postgres.rs** — the two methods under review:

- `public_chirps_with_authors` starts at approximately line 614.
  - Chirp-fetch SQL at approximately line 625 (single-line string)
  - User-batch-fetch SQL at approximately line 652
  - Rust-level pair assembly follows

- `get_user_chirps_by_username` starts at approximately line 694.
  - User lookup SQL at approximately line 707
  - Chirp count query at approximately line 724
  - Chirp page SQL at approximately line 737

**mod.rs** — trait docstrings for the specification:

- `public_chirps_with_authors` docstring: "Returns one reverse-chronological page of
  public chirps joined with their authors. Each item is `(chirp, author_user)`.
  Soft-removed chirps are excluded. The `before` cursor, when present, is a millisecond
  timestamp — only chirps with `created_at` strictly before that value are returned.
  `limit` is clamped to `1..=50`, defaulting to 20 when 0."

- `get_user_chirps_by_username` docstring: "Returns the user's profile and a page of their
  chirps, looked up by username (case-insensitive). Also returns the user's total chirp
  count and whether more chirps follow the page. Soft-removed chirps are excluded. The
  `before` cursor is a millisecond timestamp."

**in_memory.rs** — reference implementation at approximately line 446 and 488:
- `public_chirps_with_authors`: filters `before.is_none_or(|b| chirp.created_at.as_millis() < b)` — strictly less than
- `get_user_chirps_by_username`: same filter at approximately line 523

---

## Process Specification

For each method (`public_chirps_with_authors` and `get_user_chirps_by_username`):

1. **Read the trait docstring** in `mod.rs` to establish the semantic contract.
2. **Read the SQL** in `postgres.rs`. The single-line format makes visual scanning hard;
   parse it mentally or extract it for analysis. Extra whitespace in SQL is ignored by
   Postgres — do not assume correctness from formatting or assume error from formatting.
3. **Verify syntax**: Is the SQL well-formed? Check for unmatched parentheses, correct
   parameter binding ($1, $2, $3), correct column references.
4. **Verify `before` filter semantics**: The trait says "strictly before that value."
   Does the SQL use `<` (strictly less than) or `<=`? Does `$1::BIGINT IS NULL` correctly
   handle the absent-cursor case?
5. **Verify ordering**: The trait says "reverse-chronological." Does the SQL have
   `ORDER BY created_at DESC`? Is there a stable tiebreaker (e.g., `id DESC`)?
6. **Verify soft-removed filter**: Does `WHERE removed = FALSE` appear in every chirp query?
7. **For `public_chirps_with_authors` specifically**: The docstring says "joined with
   their authors." The implementation fetches chirps and authors in two separate SQL
   queries and assembles pairs in Rust. Is this application-level join semantically
   equivalent to a SQL JOIN? Could a chirp appear without its author in the result?
   (Read the assembly code around line 661–685.)
8. **For `get_user_chirps_by_username` specifically**: Does the username lookup use
   case-insensitive comparison (`LOWER(username) = LOWER($1)`)? Does the `has_more`
   calculation match the in-memory reference (fetch limit+1, check len > limit)?
9. **Compare against in_memory.rs**: Do the postgres filter semantics match the
   in-memory reference at lines 458 and 523? Do the has_more patterns match?

Do not declare findings from formatting alone. A finding requires a semantic gap.

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| Filename | `FINDINGS.md` |
| Format | Markdown |
| Location | `SUBTASK_sql-correctness/` (this workspace) |

Structure: per `../../contracts/findings_schema.md`. This is a partial findings file
covering concern 3 only. The synthesis child reads it to build the final FINDINGS.md.

The `## Clean Account` section MUST have exactly one entry:
- **Concern 3 — SQL formatting and semantic correctness**: ...

---

## Success Criteria

- SQL syntax verified against the actual query string, not assumed from formatting
- `before` filter semantics verified (strict `<` vs `<=`)
- Ordering verified (reverse-chronological with stable tiebreaker)
- Soft-removed filter verified
- Two-query approach in `public_chirps_with_authors` assessed for semantic correctness
- Case-insensitive username lookup in `get_user_chirps_by_username` verified
- Findings conform to `../../contracts/findings_schema.md`
- Concern 3 has exactly one entry in `## Clean Account`

---

## Suggested Methodology Files

Domain Mapping match: **Code review** → Primary: `Code Review`, Supporting: `Core`
Also applicable: **Rust code review** → `Rust` bundle for query binding and type analysis

Specific files:
- `code-review/CodeReview_Process_Methodology.md` — verify the SQL against the spec;
  green compilation is not a correctness proof; read the query, not just its shape
- `code-review/CodeReview_Checklist_Methodology.md` — correctness rows: does the code
  do what it says it does?
- `code-review/CodeReview_Feedback_Guidelines_Methodology.md` — severity calibration:
  formatting-only issues are nits, not blockers; semantic gaps are blockers

These are suggested starting points; load fewer if inapplicable, more if needed.

## Inherited Constraints

- Findings point at repository file paths and line numbers at pinned commit
  `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- Do not post to the PR
- SQL correctness verdict must be based on reading the actual query, not on assuming
  the formatter would not introduce bugs
- Prose in FINDINGS.md must pass the plain-voice bar in `../../contracts/findings_schema.md`
- Repository: `Nousix-LLC/nswe-demo` only

## Out-of-Scope Methodologies

- `testing/` bundle — test depth is handled by `spoke-tests`
- `synthesis/` bundle — belongs to `SUBTASK_synthesis`
- Concern 4 (spec deviation) — belongs to `SUBTASK_spec-deviation`
