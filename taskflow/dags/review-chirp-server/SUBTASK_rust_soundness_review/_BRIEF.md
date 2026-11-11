# Task: Rust idiom & soundness review of chirp-server (PR #19)

## Task Specification
**Slug**: SUBTASK_rust_soundness_review
**Task Kind**: standard
**Status**: Pending

### Objective
Review the `chirp-server` feature diff (PR #19, head `714d50f`) through the **single lens of Rust
idiom and soundness**, and emit `findings_rust_soundness.md` conforming to the findings contract.
You review; you do NOT edit, fix, or push.

### Context
Part of the review-chirp-server review DAG (see `../_GLOBAL.md`). Sibling spokes own architecture/
contract, test adequacy, and code-review quality; a synthesis gate folds the verdict. Do not
duplicate their lenses — stay on Rust soundness. The round-0 gate FAIL is superseded history; the
code DAG's cold machine gate (`chirp-server/SYNTHESIS.md`) is PASS (build/clippy/fmt green).

**Dependencies**: none. **Dependents**: `SUBTASK_synthesis_verdict`.

## Input Specification
| Input | Source | Purpose |
|-------|--------|---------|
| Hub | `../_GLOBAL.md` | Shared context, input set, discipline |
| Findings contract | `../contracts/findings_schema.md`, `../contracts/_MANIFEST.yaml` | Output shape, severity vocabulary, your owned items (AC6; co-review AC3 enum/IntoResponse idiom) |
| PR diff | `gh pr diff 19 -R Nousix-LLC/nswe-demo` | The change under review |
| Checkout | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/chirp-server/checkout/crates/chirp-server/src/` | Full files for context (`api/*.rs`, `error.rs`, `lib.rs`, `main.rs`, `repository/*.rs`) |
| Contract crate | `.../checkout/crates/chirp-types/` | What the server composes |
| Code DAG verdict | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/chirp-server/SYNTHESIS.md` | Context only |

## Review Concern (one responsibility: Rust soundness)
Examine, and record findings on:
- **Ownership / borrowing / lifetimes**: needless clones, `Arc`/`Clone` usage on the
  `Arc<dyn ChirpRepository>` seam and handler state, borrow correctness, no accidental `'static`
  leaks.
- **Error handling idiom**: `ServerError` enum design, `From`/`?` propagation (incl. the F1
  `From<JsonRejection> for ServerError`), `thiserror`/manual impl soundness, no error swallowing.
- **No runtime panic / no `unsafe` on request paths (AC6)**: audit `unwrap`/`expect`/`panic!`/
  indexing/`unsafe` on request-handling paths; confirm any `expect` is a documented thin-entry
  `main`/bootstrap exception. This is your **primary owned acceptance criterion** — render an
  explicit verdict.
- **Trait design & async idiom**: the `ChirpRepository` trait (object safety, `async_trait` or
  native async, `Send + Sync` bounds), extractor impls (`ValidatedJson<T>: FromRequest`), axum
  handler signatures, `IntoResponse` impl correctness.
- **Type-system usage**: newtypes/value objects from `chirp-types`, `#[serde(try_from)]` boundary
  behavior, enum exhaustiveness, avoidance of stringly-typed logic.
- **F1 soundness angle**: is the `ValidatedJson` extractor + `From<JsonRejection>` mapping a sound,
  idiomatic Rust construction (no panic, correct trait bounds, no orphan-rule abuse)?

A panic/`unsafe`/soundness defect on a request path is a `block`. Non-idiomatic-but-correct code is
`minor`/`nit`.

## Methodology (load on demand — IDs only; you are the executing agent)
### Suggested Methodology Files
Matched Domain-Mapping row: **"Rust code review" → Rust / Code Review, Core**.
- `rust` bundle — primary. Flag `Rust_Ownership_Borrowing_Methodology.md` (seam/clone review),
  `Rust_Error_Handling_Methodology.md` (ServerError/`?`/From idiom), `Rust_Trait_Design_Methodology.md`
  (ChirpRepository object safety, FromRequest), `Rust_Type_System_Methodology.md` (newtypes,
  try_from), `Rust_Async_Tokio_Methodology.md` (async-trait/axum handler idiom).
- `core` — error-handling & coding-standard baseline.
- `code-review` — `CodeReview_Checklist_Methodology.md` for severity discipline.
Load via `engine_load_methodology { name: "rust" }` etc., on demand. **Suggestions, not an exclusive
list** — you are the final judge of what you load.

### Inherited Constraints
- Rust async runtime is Tokio; axum is the web framework; persistence seam is `Arc<dyn ChirpRepository>`.
- Reviewer discipline (P1): read-only; no edits/push/rebase; never touch `main`; only `Nousix-LLC/nswe-demo`.
- Rely on the code DAG's cold gate for build/clippy PASS; corroborate specific findings with
  read-only inspection, do not reproduce the full build.

### Out-of-Scope Methodologies
- Testing bundle (that is `SUBTASK_test_adequacy_review`). Architecture/contract-conformance
  mapping correctness beyond the enum→status *idiom* belongs to `SUBTASK_architecture_contract_review`.

## Output Specification
**Primary output**: `findings_rust_soundness.md` in this task's workspace, conforming to
`../contracts/findings_schema.md` (header, finding records, the owned-items verdict ledger — at
minimum AC6, plus the F1 soundness angle and any co-review note on AC3's enum/IntoResponse idiom).

## Success Criteria
- [ ] Rust-soundness lens applied across all src files in the diff.
- [ ] AC6 (no panic/unsafe on request paths) rendered with an explicit verdict + evidence.
- [ ] F1 extractor/mapping soundness assessed.
- [ ] Every finding uses the fixed severity vocabulary and cites `file:line`.
- [ ] Verdict ledger present for owned items; `findings_rust_soundness.md` written.
