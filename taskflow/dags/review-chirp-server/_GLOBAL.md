# _GLOBAL.md — review-chirp-server review DAG (subtree hub)

## Project Context

**Status**: Active

### Objective

Render the **authoritative human-landing verdict** — `APPROVE` or `REQUEST-CHANGES` — on
**PR #19** (`chirp-server`, `work/chirp-server` → `main`, `Closes #8`, head `714d50f`) into this
review DAG's **root `SYNTHESIS.md`**. This DAG **reviews; it does NOT re-implement.** Blocking
defects → `REQUEST-CHANGES` with precise, actionable findings; remediation is a separate forked
code DAG the overseer dispatches, never this DAG.

The root `SYNTHESIS.md` at this workspace is the **observation seam** the overseer gates the land
on — not the gh review state (self-review posts COMMENTED) and not the code DAG's machine gate
alone.

### Scope

**In scope** — review the feature diff (`main...HEAD`, +3437/−4 across 16 files) of
`crates/chirp-server` (axum REST backend) composing the frozen `crates/chirp-types` contract:
- Rust idiom & soundness
- Architecture / layering / frozen-contract conformance
- Test adequacy
- Code-review quality (incl. the F1 remediation and fmt/clippy/rustdoc/README)

**Out of scope (do NOT flag):**
- PR #19's CONFLICTING/DIRTY mergeability — it is a pure `Cargo.lock` restale (branch cut on
  `main @ 25e90c0`; `main` now `92661d8` after the #9 land). The overseer clears it mechanically
  with a forked relock DAG before landing. Review `main...HEAD`, not mergeability.
- Re-running the full cold build to re-derive the machine PASS. The code DAG already did this cold;
  rely on its gate and review for design/correctness/quality.
- Any source edit, push, rebase, relock, force-push, or touching `main`. Reviewer discipline (P1).

### Success Criteria

- [ ] All four review lenses executed, each emitting a findings file conforming to the contract.
- [ ] The F1 remediation (validation → 400 `ApiError{VALIDATION_ERROR,details}`) examined through
      every applicable lens (reachability/wiring, flipped test, `details` limitation judgment).
- [ ] Synthesis gate folds a single root `SYNTHESIS.md` carrying an explicit `verdict:`, the
      per-severity finding list, an acceptance-criteria checklist (N/N), an explicit F1 line and
      `details`-limitation ruling, F2 triage, and whether any block/major finding is open.
- [ ] gh PR review posted (expected COMMENTED due to self-review platform block); authoritative
      verdict lives in `SYNTHESIS.md`, not the gh review state.

---

## Input Specifications

Every spoke reads these shared inputs (read-only; do not mutate the checkout).

| Input | Location | Purpose |
|-------|----------|---------|
| Acceptance rubric + F1 detail | `../review-chirp-server/_BRIEF.md` (this DAG's root brief, ancestor) | The review rubric and the F1 sub-questions |
| This hub | `_GLOBAL.md` (parent of each SUBTASK dir) | Shared context, contract pointer |
| Findings contract | `contracts/_MANIFEST.yaml`, `contracts/findings_schema.md` | The shared finding-record shape + severity vocabulary + coverage map |
| PR #19 feature diff | `gh pr diff 19 -R Nousix-LLC/nswe-demo` | The change under review (`main...HEAD`) |
| Live working tree | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/chirp-server/checkout/` (on `work/chirp-server` @ `714d50f`) | Read full files for context around diff hunks |
| chirp-server crate | `.../checkout/crates/chirp-server/src/` (`api/{auth,handlers,json,mod,router,state}.rs`, `error.rs`, `lib.rs`, `main.rs`, `repository/{in_memory,mod}.rs`) | The code under review |
| Frozen contract crate | `.../checkout/crates/chirp-types/` | The wire contract the server MUST compose, never redefine |
| Integration tests | `.../checkout/crates/chirp-server/tests/` | The test suite (44 tests: 24 unit + 20 integration, no DB) |
| Code DAG machine verdict | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/chirp-server/SYNTHESIS.md` | Context INPUT: gate=PASS round 1; F1 resolved; tracked minor F2. Treat round-0 FAIL as superseded history. |

**Reviewer discipline (P1):** read only; `gh pr diff` / `gh pr view` are fine; `gh pr review` is
posted ONLY by the synthesis gate. Never push/edit/rebase/relock; never touch `main`; only
`Nousix-LLC/nswe-demo`.

---

## Methodology

Bundle IDs are **propagated** to each child (IDs only — children load full bundles on demand). This
hub does not load full bundle bodies.

### Subtree Methodology Posture

- **Dominant task type**: code review (Rust). Most leaves map to Domain-Mapping rows "Rust code
  review" (Rust / Code Review, Core) and "Code review" (Code Review / Core, Testing).
- **Primary bundles across the subtree**: `code-review` binds every spoke; `rust` binds the Rust
  lenses; `architecture` the layering/contract lens; `testing` the test lens; `synthesis` the gate.
- **Cross-cutting binding**: every spoke emits findings in the **contract's** finding-record shape
  and severity vocabulary so the gate integrates mechanically. The F1 remediation is a cross-cutting
  focus named in each applicable spoke's brief.
- Suggestion-not-prescription: each child is the final judge of what methodology surface it loads.

---

## Task Structure

### Overview

```
_GLOBAL.md (this hub)
├── contracts/
│   ├── _MANIFEST.yaml              (ownership, identities, coverage map)
│   └── findings_schema.md          (finding-record shape + severity vocabulary + F1 checklist)
├── SUBTASK_rust_soundness_review/_BRIEF.md
├── SUBTASK_architecture_contract_review/_BRIEF.md
├── SUBTASK_test_adequacy_review/_BRIEF.md
├── SUBTASK_code_review_quality_review/_BRIEF.md
└── SUBTASK_synthesis_verdict/_BRIEF.md     (verification gate → writes ../SYNTHESIS.md, folds root)
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_rust_soundness_review` | none | Rust idiom, ownership/borrowing, error discipline, no runtime panic/`unsafe` on request paths, trait-object seam soundness | `findings_rust_soundness.md` |
| `SUBTASK_architecture_contract_review` | none | Layering (transport→service→repository), `Arc<dyn ChirpRepository>` seam, in-memory repo semantics, frozen `chirp-types` contract conformance (routes, base `/api`, camelCase, Bearer, `ErrorCode` mapping, no DTO redefinition), F1 reachability/400-routing + `details` contract-satisfaction | `findings_architecture_contract.md` |
| `SUBTASK_test_adequacy_review` | none | Suite drives real app via `lib.rs` against in-memory repo (no DB); error-row coverage (400/401/403/404/409); timeline limit-clamp; F1 flipped characterization test asserts 400/`ValidationError`/`!details.is_empty()` and no `422` pin remains | `findings_test_adequacy.md` |
| `SUBTASK_code_review_quality_review` | none | General code-review-quality lens; F1 `json.rs`/`error.rs` change quality + minimal-dependency trade-off; fmt/clippy/rustdoc(`missing_docs`)/README; F2 triage (intra-doc-link nits under `RUSTDOCFLAGS=-D warnings`, not in gate set) | `findings_code_review_quality.md` |
| `SUBTASK_synthesis_verdict` | `SUBTASK_rust_soundness_review`, `SUBTASK_architecture_contract_review`, `SUBTASK_test_adequacy_review`, `SUBTASK_code_review_quality_review` | **Verification gate**: integrate the four findings files against the contract coverage map + identities, render the authoritative verdict, post the gh review, write root `SYNTHESIS.md` at the fold location and fold | `../SYNTHESIS.md` (fold record) |

### Dependency Graph

```
SUBTASK_rust_soundness_review      ──┐
SUBTASK_architecture_contract_review ─┤
SUBTASK_test_adequacy_review         ─┼── SUBTASK_synthesis_verdict ── ../SYNTHESIS.md (fold → root COMPLETED)
SUBTASK_code_review_quality_review   ─┘
```

---

## Contract

**Contract location**: `contracts/` (read-only for every descendant)
**Contract kind**: `yaml_schema` + markdown finding-record spec (a thin seam — see the Thin-Seam note).

### Structural Declarations

The four spokes are parts of ONE review and share a seam: every spoke emits findings in a **single
finding-record shape** using a **fixed severity vocabulary**, each finding tagged with the
acceptance-criterion id(s) it bears on, so the synthesis gate integrates them mechanically and
derives the verdict without reconciling divergent structures.

| Artifact | Kind | Declares |
|---|---|---|
| `contracts/findings_schema.md` | markdown spec | The finding-record fields, the severity vocabulary (`block`/`major`/`minor`/`nit`), the acceptance-criterion id set (AC1..ACn), the F1 sub-question checklist (F1.1–F1.4), and the per-spoke output filename |
| `contracts/_MANIFEST.yaml` | yaml_schema | Per-spoke ownership, the acceptance-criteria coverage map (which spoke owns which AC), and the identities the gate asserts |

### Ownership

| Artifact | Owning subtask |
|---|---|
| `findings_rust_soundness.md` | `SUBTASK_rust_soundness_review` |
| `findings_architecture_contract.md` | `SUBTASK_architecture_contract_review` |
| `findings_test_adequacy.md` | `SUBTASK_test_adequacy_review` |
| `findings_code_review_quality.md` | `SUBTASK_code_review_quality_review` |
| `../SYNTHESIS.md` (fold record) + gh review post | `SUBTASK_synthesis_verdict` |

### Identities (the gate asserts these; MUST NOT silently plug a failure)

- [ ] **Coverage**: every acceptance criterion AC1..ACn is addressed by ≥1 spoke finding or an
      explicit "conforms, no finding" statement from the owning spoke.
- [ ] **F1 completeness**: each F1 sub-question F1.1–F1.4 is answered by the owning spoke.
- [ ] **Severity vocabulary**: every finding uses exactly one of `block`/`major`/`minor`/`nit`.
- [ ] **Verdict derivation**: `verdict = REQUEST-CHANGES` iff any `block` finding is open (and the
      gate must decide, with reasoning, whether any `major` also forces REQUEST-CHANGES); otherwise
      `APPROVE`. The `details`-limitation ruling (acceptable vs blocking weakening of the wire
      contract) is an explicit gate decision, not a spoke's unilateral call.
- [ ] **F2 disposition**: the code DAG's tracked minor F2 is confirmed non-gating and carried as a
      tracked issue recommendation for the CI work-items (#10–#13), or escalated with reasoning.

### Thin-Seam Note

These children share little beyond the finding-record shape and the input set — so the contract is
small: a `_MANIFEST.yaml` (ownership + coverage map + identities) plus one finding-schema spec.
Small is correct here; absent would not be.

---

## Output Specifications

| Deliverable | Format | Location | Description |
|-------------|--------|----------|-------------|
| Four findings files | Markdown (per schema) | each `SUBTASK_*/findings_*.md` | One per review lens |
| Root verdict | Markdown | `SYNTHESIS.md` (this workspace root = observation seam) | Authoritative APPROVE / REQUEST-CHANGES fold record |
