# Task: Code-review-quality review of chirp-server (PR #19)

## Task Specification
**Slug**: SUBTASK_code_review_quality_review
**Task Kind**: standard
**Status**: Pending

### Objective
Review the `chirp-server` feature diff (PR #19, head `714d50f`) through the **single lens of
code-review quality** — readability, maintainability, hygiene, documentation, and the quality of the
F1 remediation change itself — and emit `findings_code_review_quality.md` conforming to the findings
contract. You review; you do NOT edit, fix, or push.

### Context
Part of the review-chirp-server review DAG (`../_GLOBAL.md`). You own AC7 (fmt/clippy/rustdoc/README)
and the F2 triage. Sibling spokes own Rust soundness, architecture/contract, and test adequacy —
defer the soundness/contract/test *verdicts* to them; your lens is craft quality and the F1 change
quality + minimal-dependency trade-off.

**Dependencies**: none. **Dependents**: `SUBTASK_synthesis_verdict`.

## Input Specification
| Input | Source | Purpose |
|-------|--------|---------|
| Hub | `../_GLOBAL.md` | Shared context, input set, discipline |
| Findings contract | `../contracts/findings_schema.md`, `../contracts/_MANIFEST.yaml` | Output shape; owned AC7, F2 triage |
| PR diff | `gh pr diff 19 -R Nousix-LLC/nswe-demo` | The change under review |
| Checkout | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/chirp-server/checkout/` | Source (`crates/chirp-server/src/`, esp. `api/json.rs`, `error.rs`), `README.md` |
| Code DAG verdict | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/chirp-server/SYNTHESIS.md` | Context: fmt/clippy PASS cold; tracked minor **F2** (rustdoc intra-doc-link nits that only fire under `RUSTDOCFLAGS=-D warnings`, which is NOT in the gate set; `missing_docs` satisfied) |

## Review Concern (one responsibility: code-review quality)
- **AC7 — hygiene & docs**: confirm fmt `--check` clean, clippy `--all-targets -- -D warnings` clean
  (rely on the code DAG's cold gate; corroborate with read-only inspection, do not reproduce the
  full build), rustdoc on public items (`missing_docs` satisfied), README present and adequate.
- **F1 change quality (`json.rs` + `error.rs`)**: is the `ValidatedJson<T>` extractor + the
  `JsonRejection → ServerError::InvalidBody → ErrorCode::ValidationError → 400` + `into_api_error()`
  lifting **well-written, readable, documented, and minimal**? Judge the **minimal-dependency
  trade-off** (declining `serde_path_to_error` to recover the field name, accepting a generic
  `FieldError{field:"body"}`): is that trade-off well-reasoned and clearly documented in-code, or an
  under-documented shortcut? (The *contract-satisfaction* ruling is the architecture spoke's + gate's;
  you judge the **craft and documentation** of the trade-off.)
- **General craft**: naming, module boundaries, comment quality (explains *why*, not *what*), dead
  code, duplication, TODOs, consistent error-construction patterns, handler readability.
- **F2 triage (owned)**: confirm F2 is genuinely **non-gating** (fires only under
  `RUSTDOCFLAGS=-D warnings`, which is not in the gate assertion set; `missing_docs` satisfied), and
  recommend whether it should be carried as a **tracked issue** for the CI work-items (#10–#13).
  Record this as an explicit finding (`minor`, with the tracked-issue recommendation).

Quality issues here are generally `minor`/`nit`; a genuinely unreadable/undocumented critical path
or a hygiene failure contradicting AC7 is `major`.

## Methodology (load on demand — IDs only)
### Suggested Methodology Files
Matched row: **"Code review" → Code Review / Core, Testing**.
- `code-review` — primary. Flag `CodeReview_Checklist_Methodology.md`, `CodeReview_Process_Methodology.md`,
  `CodeReview_Feedback_Guidelines_Methodology.md` (actionable, specific, kind findings).
- `core` — `BestPractices_Coding_Standards_Methodology.md`, `BestPractices_Error_Handling_Methodology.md`.
- `code-quality` (optional) — `Framework_Clean_Code_Methodology.md` if craft depth is warranted.
Load on demand. **Suggestions, not exclusive** — you are the final judge.

### Inherited Constraints
- Reviewer discipline (P1): read-only; no edits/push/rebase; never touch `main`; only `Nousix-LLC/nswe-demo`.
- Rely on the code DAG's cold gate for fmt/clippy PASS; do not reproduce the full build.
- Do NOT flag the CONFLICTING/DIRTY mergeability (known `Cargo.lock` restale).

### Out-of-Scope Methodologies
- Rust soundness *verdict* (that is `SUBTASK_rust_soundness_review`), contract conformance (arch spoke),
  test adequacy (test spoke). You may note craft issues you see in those areas but route the
  authoritative verdict to the owning spoke.

## Output Specification
**Primary output**: `findings_code_review_quality.md` conforming to `../contracts/findings_schema.md`,
with the owned-items verdict ledger covering AC7 and the F2 disposition.

## Success Criteria
- [ ] AC7 (fmt/clippy/rustdoc/README) rendered with explicit verdict + evidence.
- [ ] F1 change craft + minimal-dependency trade-off documentation judged.
- [ ] F2 triage rendered: non-gating confirmed (or escalated) + tracked-issue recommendation for #10–#13.
- [ ] Every finding uses the fixed severity vocabulary and cites evidence; ledger present; file written.
