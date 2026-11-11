# COMPLETE — `SUBTASK_folded_minors` (concern 5)

**Task**: Review the non-CI changes folded into PR #21 (ci-actions, issue #11) at head `c8123376` — the ~79 rustdoc intra-doc-link fixes and the chirp-server README validation-error correction. Read-only review spoke of the PR #21 review DAG.

**Output produced**: `findings.md` (this workspace), conformant to `../contracts/findings_schema.md`, id prefix `DOC-`, header states head `c8123376`.

## What was done

Gathered evidence read-only via `gh` (GET only — no push, no review, no merge):
- `gh pr view 21 --json ...` — confirmed head `c8123376`, 22 files, +286/−92 (21 non-CI files = +92/−92).
- `gh pr diff 21` — inspected every non-CI hunk (ci.yml excluded; owned by other spokes).
- `gh api .../contents/...?ref=c8123376` for `src/api/json.rs` and `src/error.rs` — confirmed the real validation-error response path.

## Conclusions (per concern-5 facet)

1. **Doc-only verification — confirmed.** All 20 changed `.rs` files edit only `//!`/`///` doc-comment lines (broken intra-doc links → plain code spans). Zero runtime code changed. +92/−92 symmetry corroborates in-place doc-line replacement. No non-doc hunk found.
2. **README 422→400 / `VALIDATION_ERROR` correction — accurate.** Verified against actual source: `ValidatedJson` extractor → `ServerError::InvalidBody` → `ErrorCode::ValidationError` → `StatusCode::BAD_REQUEST` (400). The correction matches real behavior. One cosmetic variant-name imprecision (prose says `ServerError::Validation`; code path is `InvalidBody`) raised as a nit.
3. **Scope-folding judgment — acceptable.** The rustdoc fixes are coupled to this PR's own new `doc` job (`RUSTDOCFLAGS: -D warnings`): they are the debt resolution that keeps that new gate green. Folding is correct scope. Mixed-concern/reviewability raised as an advisory `minor`.

## Roll-up

**block: 0 | major: 0 | minor: 1 | nit: 1** → this spoke contributes no verdict-forcing findings (0 block, 0 major).

## Constraints honored

- Read-only throughout (no write to the repo/branch; `gh` GET only).
- Confirmed doc-only scope from the actual diff rather than assuming it from the machine-PASS gate (used the green gate only as corroboration).
- Emitted in the frozen findings schema; no amendment needed (schema was adequate).
