# Area C: Error Handling — PR #228

## Task Specification

**Slug**: SUBTASK_C_error_handling
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective

Examine the error handling in PR #228 (`work/ferric-ssr-r1`, repo `Nousix-LLC/nswe-demo`) for correctness, panic-safety, and idiomatic Rust error propagation. Identify any path where errors are suppressed, panics can be triggered at runtime by external input, or callers are denied the ability to recover. Produce one area finding file at the declared output path.

---

## Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Hub | `../_GLOBAL.md` | PR coordinates, citation constraints, non-goal boundary |
| Findings schema | `../contracts/findings_schema.yaml` | Required output structure |
| PR diff | `gh pr diff 228 --repo Nousix-LLC/nswe-demo` | The change under review |
| ferric crate source | `crates/ferric/` on branch `work/ferric-ssr-r1` | Full file content for touched files |

---

## Review Scope

This area covers error handling on new code paths introduced by the PR:
- Whether `render_to_string` returns a `Result` or propagates errors, or panics on bad/unexpected input
- Whether `hydrate()` on a mismatched tree is recoverable — can the caller handle the mismatch without panicking?
- `unwrap()` and `expect()` calls in new code paths: are any called on values that could plausibly be `None`/`Err` at runtime (not just in tests)?
- Idiomatic Rust error types: are errors typed appropriately so callers can match on them?

The boundary: test-only code may use `unwrap()` for brevity; that is not a finding. The concern is `unwrap()`/`expect()` in production code paths that handle real inputs. Naming of error types belongs in Area A.

---

## Output

| Attribute | Value |
|-----------|-------|
| File | `area_c_error_handling.md` |
| Location | this workspace (`SUBTASK_C_error_handling/`) |
| Must conform to | `../contracts/findings_schema.yaml` |

One verdict (CLEAN, FINDING (NON-BLOCKER), or FINDING (BLOCKER)). FINDING includes at least one citation with a repository-relative file path and line number.

---

## Success Criteria

- `area_c_error_handling.md` exists before this task reports completed
- One verdict explicitly stated
- "What was checked" names the specific functions and code paths examined for panic-safety
- Each finding specifies what would satisfy it (e.g., "return Result instead of panicking")
- No finding cites #225 / REQ-SSR-007 (inherited non-goal)

## Inherited Constraints

- Read-only: do not modify source code
- Citations use repository-relative paths in `Nousix-LLC/nswe-demo`, not host paths
- #225 / REQ-SSR-007 is not a code quality finding for this PR
- Non-blockers: flag as FINDING (NON-BLOCKER); the outer synthesis will track them
