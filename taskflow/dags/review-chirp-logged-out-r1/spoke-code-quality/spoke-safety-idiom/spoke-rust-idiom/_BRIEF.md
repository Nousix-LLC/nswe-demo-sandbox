# Task: Concern 10 — Rust/WASM Idiom Patterns (hydrate.rs and broader)

## Task Specification

**Slug**: spoke-rust-idiom
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective

Assess whether the following patterns in `crates/ferric/src/hydrate.rs` (and any related files)
are idiomatic for Rust/WASM and whether any create leak or panic risks, in PR #263 on
`Nousix-LLC/nswe-demo` at pinned commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`:

- `spawn_local` for async effects
- `thread_local!` + `RefCell` for reactive state
- `Cell<bool>` for the started guard
- `Closure::forget()` in `hydrate.rs`

### Context

This task covers concern 10 from the parent code-quality review. It is part of a decomposition
of `spoke-safety-idiom` (see `../_GLOBAL.md`). The sibling `spoke-error-safety` runs concern 8
concurrently; `spoke-safety-synthesis` depends on both and produces the combined FINDINGS.md.

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Hub context | `../_GLOBAL.md` | Subtree constraints, pinned commit, access instructions |
| Contract manifest | `../contracts/_MANIFEST.yaml` | Output ownership |
| Ancestor schema | `../../../contracts/findings_schema.md` | FINDINGS.md structure |
| `hydrate.rs` | `crates/ferric/src/hydrate.rs` at pinned commit | Four idiom patterns under review |
| Other callers | Any file using `spawn_local`, `thread_local!`, `Cell<bool>`, `Closure::forget()` | Context for each pattern |

Access repository files via:
```bash
gh api "repos/Nousix-LLC/nswe-demo/contents/PATH?ref=decb6196c2c1e6ed421d393a642f0c844cc333ba" \
  --jq '.content' | base64 -d
```

To find `hydrate.rs`:
```bash
gh api "repos/Nousix-LLC/nswe-demo/contents/crates/ferric/src/hydrate.rs?ref=decb6196c2c1e6ed421d393a642f0c844cc333ba" \
  --jq '.content' | base64 -d
```

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| Filename | `rust_idiom_findings.md` |
| Format | Markdown conforming to `../../../contracts/findings_schema.md` |
| Location | `spoke-rust-idiom/` (this workspace) |

The partial findings cover concern 10 only. The synthesis child reads this file and merges it
with `../spoke-error-safety/error_safety_findings.md` to produce the final combined FINDINGS.md.

---

## Assessment Guidance for Each Pattern

**`spawn_local` for async effects**: Is this the idiomatic way to trigger async side-effects in
a Leptos/WASM context? Does misuse create leaked futures (future dropped before completion)?

**`thread_local!` + `RefCell` for reactive state**: Is this the standard Leptos pattern for
mutable reactive signals, or is `Signal`/`RwSignal` a type-safe alternative? Assess whether
`RefCell` panics on borrow are possible at runtime in this context.

**`Cell<bool>` for the started guard**: Valid in single-threaded WASM. Note whether the
single-threaded invariant is documented. Could it be replaced with something that provides
better compile-time guarantees?

**`Closure::forget()` in `hydrate.rs`**: This deliberately leaks the closure to extend its
lifetime beyond the calling function. It is correct for event handlers that must outlive the
caller, but verify the use site actually requires a persistent callback (not a one-shot).

---

## Success Criteria

- All four patterns assessed for idiomatic correctness and leak/panic risk
- Verdict declared: PASS if all patterns are idiomatic and safe; FINDINGS if any concern identified
- For each finding: file path + line number at pinned commit, principle, severity, satisfying condition
- Clean Account covers concern 10 with what was checked and what was found (each pattern separately)
- Output file at `spoke-rust-idiom/rust_idiom_findings.md`
- No internal infrastructure details in any finding or prose

---

## Suggested Methodology Files

Domain Mapping matches:
- **Rust code review** → Primary: `Rust`, Supporting: `Code Review`, `Core`
- For `spawn_local` / async: **Rust async implementation** → `Rust` (Async Tokio sub-bundle)

Specific files to load (starting points — the executing agent is the final judge):

- `rust/Rust_Async_Tokio_Methodology.md` — async Rust patterns; `spawn_local` is the
  WASM-compatible equivalent of `tokio::spawn`; this methodology covers dropped futures and
  the difference between detached tasks and awaited futures.
- `rust/Rust_Ownership_Borrowing_Methodology.md` — `Closure::forget()` is an explicit ownership
  choice (deliberately leaking to extend lifetime); `Cell<bool>` and `RefCell` are interior
  mutability patterns; this methodology provides the vocabulary.
- `code-review/CodeReview_Checklist_Methodology.md` — idiom rows and resource-safety rows.

These are the parent's flagged starting points. Load fewer if some are clearly inapplicable;
load more if the codebase reveals additional methodology surface.

## Out-of-Scope Methodologies

- `security/` bundle (error leakage) — belongs to `spoke-error-safety`
- `testing/` bundle — test depth is handled by `spoke-tests` at the parent review level
- Prose quality — handled by `spoke-prose` at the parent review level

## Inherited Constraints

- Findings point at repository file paths and line numbers at pinned commit
  `decb6196c2c1e6ed421d393a642f0c844cc333ba`; no host paths, private IPs, or infrastructure
  details
- Do not post to the PR
- Prose in `rust_idiom_findings.md` must pass the plain-voice bar in
  `../../../contracts/findings_schema.md`
- Repository: `Nousix-LLC/nswe-demo` only
