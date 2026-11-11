# Spoke: Error Safety + Rust Idiom — Subtree Hub

## Context

**Parent spoke**: `spoke-code-quality` of review `review-chirp-logged-out-r1`
**PR under review**: PR #263 on `Nousix-LLC/nswe-demo`
**Pinned commit**: `decb6196c2c1e6ed421d393a642f0c844cc333ba`
**Assigned concerns**: 8 (error message safety) and 10 (Rust/WASM idiom)

This spoke was decomposed because concerns 8 and 10 are distinct analyses from different
methodology domains (security vs. Rust/WASM idiom) that can run in parallel with no
cross-dependency.

## Subtree Objective

Produce one combined `FINDINGS.md` at this workspace root that covers both assigned concerns,
conforming to the findings schema at `../../contracts/findings_schema.md`.

## Cut Rationale

Concern 8 reads `AppError`/`user_message()` and the error display path in `crates/chirp-server/`
and the frontend error banner. Concern 10 reads `crates/ferric/src/hydrate.rs` and broader
WASM idiom patterns. These are disjoint file sets and disjoint methodology domains:

- Security methodology → concern 8
- Rust/WASM methodology → concern 10

They require no shared write targets during analysis. The synthesis child combines their partial
findings into the final FINDINGS.md.

## Subtree Methodology Posture

- **Dominant task types**: Security review (concern 8), Rust code review (concern 10)
- **Primary bundles**: `security`, `rust`, `code-review`
- **Cross-cutting binding**: The `../../../contracts/findings_schema.md` FINDINGS.md structure
  binds every leaf and the synthesis — partial findings must be mergeable into the combined schema

## Subtree-Wide Constraints

- All findings point at repository file paths and line numbers at pinned commit
  `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- No host paths, private IPs, or infrastructure details in any output
- Do not post to the PR
- Prose in all findings must pass the plain-voice bar defined in
  `../../contracts/findings_schema.md`
- Repository: `Nousix-LLC/nswe-demo` only
- Access files via:
  ```bash
  gh api "repos/Nousix-LLC/nswe-demo/contents/PATH?ref=decb6196c2c1e6ed421d393a642f0c844cc333ba" \
    --jq '.content' | base64 -d
  ```

## Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `spoke-error-safety` | none | Concern 8: AppError / user_message() error message safety | `spoke-error-safety/error_safety_findings.md` |
| `spoke-rust-idiom` | none | Concern 10: Rust/WASM idiom patterns in hydrate.rs | `spoke-rust-idiom/rust_idiom_findings.md` |
| `spoke-safety-synthesis` | `spoke-error-safety`, `spoke-rust-idiom` | Merge partial findings into combined FINDINGS.md | `FINDINGS.md`, `SYNTHESIS.md` |

## Dependency Graph

```
spoke-error-safety  ──┐
                       ├── spoke-safety-synthesis
spoke-rust-idiom    ──┘
```

## Contract

**Contract location**: `contracts/`
**Contract kind**: `yaml_schema` (thin — ownership + identities; structural schema inherited from ancestor)

The ancestor findings schema at `../../contracts/findings_schema.md` already declares the
structural format every analysis spoke must produce. This level's contract is thin: it declares
per-child output ownership and the identities that must hold at synthesis.

See `contracts/_MANIFEST.yaml`.
