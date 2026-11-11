# Placement and Duplication Review — CHANGELOG.md, PR #210

Repo: `Nousix-LLC/nswe-demo` — PR #210 (`work/ferric-http-r1` → `main`, head `0436218`)

---

## Concerns Covered

- Concern 2 (placement correctness)
- Concern 3 (duplication)

---

## Summary

PR #210 introduces `crates/ferric-http/CHANGELOG.md` as a new file with two sections: `## Unreleased — usable_early surface (#148)` and `## Initial implementation (#6)`. A remediation commit (`0436218`) followed and corrected API signatures in the Unreleased section. Both placement correctness and duplication were checked across both commits. All 8 items examined are clean: the new entries land in the correct sections, the section order is intact, the remediation commit does not touch any released version block, and no entry is duplicated or contradicted within or across sections.

---

## Findings

**[CLEAN] Unreleased entries under the Unreleased section**: The `usable_early` API surface documentation — all types, methods, acceptance-criteria table, and deferred-items note — is placed under `## Unreleased — usable_early surface (#148)`, the topmost section of the CHANGELOG. This is the correct target for unreleased work. No entry from either commit lands outside this section.

- Principle: Keep a Changelog convention — new entries for unreleased work belong in the `[Unreleased]` block, not in a released version block.
- Evidence: PR diff shows the entire `crates/ferric-http/CHANGELOG.md` created as a new file; the `usable_early` surface entries occupy the first section (`## Unreleased — usable_early surface (#148)`). Commit `d6a9b6eb` authored both sections; commit `0436218` modified only content within the Unreleased section (corrected API signatures for `query()`, `Response::text()`, `header()`/`default_header()`, and added missing API members).
- Resolution: No action required.

**[CLEAN] Remediation commit does not place entries in a released version section**: The remediation commit (`0436218`) makes corrections exclusively within `## Unreleased — usable_early surface (#148)`. It does not introduce or modify any released version block.

- Principle: A remediation fixing documentation errors in an in-flight PR MUST NOT write into released version sections, whose content records historical shipped state.
- Evidence: The CHANGELOG contains no released version blocks (no `## [x.y.z] - YYYY-MM-DD` headers). All changes by both commits are confined to the two sections created by the PR. The remediation commit message explicitly names the Unreleased section as its target ("correct API signatures in CHANGELOG.md").
- Resolution: No action required.

**[CLEAN] Version section ordering intact**: The `## Unreleased` section is at the top; the `## Initial implementation (#6)` section is at the bottom. No ordering inversion is present.

- Principle: Keep a Changelog ordering — `[Unreleased]` first, then released versions from newest to oldest.
- Evidence: Lines 1–155 of the diff (the full file) show `## Unreleased — usable_early surface (#148)` preceding `## Initial implementation (#6)`. No section appears out of order.
- Resolution: No action required.

**[CLEAN] Intra-section uniqueness (within `## Unreleased — usable_early surface (#148)`)**: Each public API type is documented exactly once in the frozen-surface block: `Client`, `ClientBuilder`, `RequestBuilder`, `Response`, `Error`, `Method`. The same method name appearing on two distinct types (`header()` on `RequestBuilder` and `Response`; `json()` on `RequestBuilder` and `Response`) is expected Rust API design — different receivers, not duplicated entries. The acceptance criteria table and the API surface declarations cover different facts (behavior assertions vs. signatures) and do not duplicate each other.

- Principle: Each entry in a CHANGELOG section should appear once; same names on different types are not duplicates.
- Evidence: Diff lines +31–+128 (the full `## Unreleased` block); no type block repeated.
- Resolution: No action required.

**[CLEAN] Intra-section uniqueness (within `## Initial implementation (#6)`)**: Each source file (`src/error.rs`, `src/request.rs`, `src/response.rs`, `src/client.rs`, `src/lib.rs`) and each dependency (`web-sys`, `js-sys`, `wasm-bindgen`, `wasm-bindgen-futures`, `serde`, `serde_json`) appears exactly once.

- Principle: No copy-paste items within a single CHANGELOG entry.
- Evidence: Diff lines +147–+160 (the `## Initial implementation` block); six source files, six dependencies, each listed once.
- Resolution: No action required.

**[CLEAN] Cross-section mention of the same types**: Both `## Unreleased` and `## Initial implementation (#6)` name the same types (`Client`, `ClientBuilder`, etc.). This is not duplication: the two sections record distinct events separated in time — commit `d6a9b6e` (2026-11-04T10:12) introduced the code; the `## Unreleased` entry records the formal API freeze and acceptance-criteria verification. Keep a Changelog conventions assign each section to one release point; mentioning the same types across sections at different levels of description (brief source-file attribution vs. full signature specification) is correct structure.

- Principle: Different CHANGELOG entries describe different events; cross-section mentions of the same type name are not duplicates when the entries describe different events.
- Evidence: `## Initial implementation` names `Error` as "Error enum + Result type alias"; `## Unreleased` gives the full `#[non_exhaustive]` enum definition and helper methods. The two descriptions are complementary, not copies.
- Resolution: No action required.

**[CLEAN] Cross-commit duplication and contradiction (commit `d6a9b6e` vs `0436218`)**: The remediation commit (`0436218`) made targeted in-place corrections — it replaced incorrect signatures (B1: `query` parameter type, B2: `Response::text` self/return type, SF3: `header`/`default_header` parameter types) and added members that were entirely absent (SF4: `Error::is_network()`, `Error::is_status()`, `Error::status()`, `Method::as_str()`, `impl Display for Method`, `RequestBuilder::body_string()`, `Response::status_text()`, `Response::headers()`, `Response::body()`). No entry exists in both its pre-correction and post-correction form. The final document does not contain the original incorrect `query(key: &str, value: &str)` signature alongside the corrected `query(params: &[(&str, &str)])` — only the corrected form is present. No contradiction exists between the two commits' contributions to the final file.

- Principle: A remediation commit that corrects existing entries in place does not create duplication; only if both old and new forms remain would duplication exist.
- Evidence: PR commit list (oid `d6a9b6e`, then `0436218`); final diff shows single occurrence of each corrected method with the accurate signature.
- Resolution: No action required.

**[CLEAN] Near-duplicate entries**: No near-duplicate entries found. The acceptance criteria reference `Error::{Network,Status,Deserialize,...}` (enum variant names) while the API surface spec documents `Error::is_network()`, `Error::is_status()`, `Error::status()` (helper methods). These describe different aspects (variant identity vs. method accessors). RFC-3986 URL resolution is noted as an implementation detail in `## Initial implementation (#6)` and as a verified acceptance criterion in `## Unreleased`; different sections, different events, different specificity. No entry appears under more than one version section with the same content.

- Principle: Same fact stated at different levels of abstraction in different sections for different purposes is not near-duplication.
- Evidence: "RFC-3986 URL resolution + percent-encoding" at diff +152 (source file attribution); "RequestBuilder chains URL resolution per RFC 3986" at diff +122 (acceptance criterion). These are in separate sections serving separate roles.
- Resolution: No action required.
