# Task: Error Safety + Rust Idiom Analysis — PR #263

## Task Specification

**Slug**: spoke-safety-idiom
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective

Assess error message safety and Rust/WASM idiom correctness in PR #263 on `Nousix-LLC/nswe-demo`,
covering concerns 8 and 10 from the parent spoke brief.

### Context

This task is part of the code-quality review decomposition. See `../_GLOBAL.md` for PR details,
the full concern assignment table, and `../contracts/` for the FINDINGS.md output schema.

**Concerns assigned to this spoke:**

8. **Error message safety** (`AppError` / `user_message()`):
   Verify that error messages surfaced in the UI (e.g., via `error_banner`) do not expose
   internal details — stack traces, internal server paths, raw database errors, SQL query text,
   or any detail that aids an attacker or leaks implementation.

   Specifically: read `AppError`'s `user_message()` implementation. For each error variant,
   what string does it return? Could any variant surface a database error message, a file path,
   or a raw exception message that the UI would display? If a handler returns
   `AppError::InternalServerError` or similar, does the message string contain the original
   error? Does the error_banner component display the full message string?

9. *(Not assigned to this spoke — handled by `spoke-prose`.)*

10. **Rust idiom** (`ferric/src/hydrate.rs` and broader):
    Assess whether the following patterns are idiomatic for Rust/WASM and whether any create
    leak or panic risks:

    - `spawn_local` for async effects: is this the idiomatic way to trigger async side-effects
      in a Leptos/WASM context? Does misuse create leaked futures?
    - `thread_local!` + `RefCell` for reactive state: is this the standard Leptos pattern for
      mutable reactive signals, or is there a type-safe alternative?
    - `Cell<bool>` for the started guard: appropriate for a single-threaded WASM context?
      Could it be replaced with something that provides better compile-time guarantees?
    - `Closure::forget()` in `hydrate.rs`: is this intentional leak-prevention, or does it
      risk a real memory leak? Under what conditions is `Closure::forget()` correct vs. a bug?

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Hub context | `../_GLOBAL.md` | Concern assignments, pin commit, output schema |
| Contract schema | `../contracts/findings_schema.md` | FINDINGS.md structure |
| `AppError` definition | Likely `crates/chirp-server/src/` or `crates/chirp-types/` at HEAD | `user_message()` impl |
| Error banner usage | Frontend component(s) that display `error_banner` at HEAD | What is displayed to the user |
| `hydrate.rs` | `crates/ferric/src/hydrate.rs` at HEAD | Rust/WASM idiom patterns |
| Other callers | Any file using `spawn_local`, `thread_local!`, `Cell<bool>`, `Closure::forget()` in this PR | Context for the idiom patterns |

Access files via:
```bash
gh api "repos/Nousix-LLC/nswe-demo/contents/PATH?ref=decb6196c2c1e6ed421d393a642f0c844cc333ba" \
  --jq '.content' | base64 -d
```

To find the AppError type and its user_message():
```bash
gh api "repos/Nousix-LLC/nswe-demo/git/trees/decb6196c2c1e6ed421d393a642f0c844cc333ba?recursive=1" \
  --jq '.tree[] | select(.path | contains("error")) | .path'
```

---

## Process Specification

For concern 8 (error safety):
- Locate `AppError` and its `user_message()` or equivalent method
- For each variant, determine whether the returned message could contain user-hostile or
  security-sensitive detail
- Trace the error display path: handler → AppError → user_message() → error_banner → HTML
- Determine whether raw database errors, internal paths, or query text can reach the UI

For concern 10 (Rust idiom):
- Read `hydrate.rs` for the four patterns listed
- For `spawn_local`: check whether the future is properly driven to completion or could be dropped
- For `thread_local! + RefCell`: assess whether the approach is the Leptos idiomatic pattern
  or whether a `Signal`/`RwSignal` would be safer and more idiomatic
- For `Cell<bool>`: valid in single-threaded WASM; note whether the invariant is documented
- For `Closure::forget()`: this deliberately leaks the closure to extend its lifetime; correct
  for event handlers that must outlive the calling function, but verify that the use site
  actually requires a persistent callback (not a one-shot)

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| Filename | `FINDINGS.md` |
| Format | Markdown |
| Location | `spoke-safety-idiom/` (this workspace) |

Structure: per `../contracts/findings_schema.md`.

---

## Success Criteria

- Concerns 8 and 10 each appear in the Clean Account
- For concern 8: each `AppError` variant's user-facing message examined; verdict on whether
  any variant can surface internal detail to the UI
- For concern 10: each of the four patterns assessed for idiomatic correctness and leak/panic risk
- Severity assigned and justified for each finding
- No internal infrastructure details in any finding

---

## Suggested Methodology Files

Domain Mapping match (concern 8): **Security review** → Primary: `Security`, Supporting: `Code Review`
Domain Mapping match (concern 10): **Rust code review** → Primary: `Rust`, Supporting: `Code Review`, `Core`

Specific files:
- `security/Security_Secure_Coding_Methodology.md` — information leakage through error messages;
  the principle that user-facing errors must not expose internal state
- `code-review/CodeReview_Checklist_Methodology.md` — security rows and idiom rows
- `rust/Rust_Async_Tokio_Methodology.md` — async Rust patterns; use for `spawn_local` assessment
- `rust/Rust_Ownership_Borrowing_Methodology.md` — `Closure::forget()` and lifetime management

These are suggested starting points; load fewer if inapplicable, more if needed.

## Out-of-Scope Methodologies

- `testing/` bundle — test depth is handled by `spoke-tests`
- Prose quality — handled by `spoke-prose`
- `synthesis/` bundle — belongs to `spoke-synthesis`

## Inherited Constraints

- Findings point at repository file paths and line numbers at pinned commit
  `decb6196c2c1e6ed421d393a642f0c844cc333ba`; no host paths, private IPs, or infrastructure details
- Do not post to the PR
- Prose in FINDINGS.md must pass the plain-voice bar in `../contracts/findings_schema.md`
- Repository: `Nousix-LLC/nswe-demo` only
