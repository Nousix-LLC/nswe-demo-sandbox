# Duplication Analysis — CHANGELOG.md (PR #210)

## Concern Covered

Concern 3 (duplication)

## Findings

**[CLEAN] Intra-section uniqueness (within `## Unreleased — usable_early surface (#148)`)**: Each
public API type is documented exactly once in the frozen-surface block: `Client`, `ClientBuilder`,
`RequestBuilder`, `Response`, `Error`, `Method`. The same method name appearing on two distinct
types (`header()` on RequestBuilder and Response; `json()` on RequestBuilder and Response) is
expected Rust API design — different receivers, not duplicated entries. The acceptance criteria
table and the API surface declarations cover different facts (behavior assertions vs. signatures)
and do not duplicate each other.
- Principle: Each entry in a CHANGELOG section should appear once; same names on different types
  are not duplicates.
- Evidence: Diff lines +31–+128 (the full `## Unreleased` block); no type block repeated.
- Resolution: N/A — clean.

**[CLEAN] Intra-section uniqueness (within `## Initial implementation (#6)`)**: Each source file
(`src/error.rs`, `src/request.rs`, `src/response.rs`, `src/client.rs`, `src/lib.rs`) and each
dependency (`web-sys`, `js-sys`, `wasm-bindgen`, `wasm-bindgen-futures`, `serde`, `serde_json`)
appears exactly once.
- Principle: No copy-paste items within a single CHANGELOG entry.
- Evidence: Diff lines +147–+160 (the `## Initial implementation` block); six source files,
  six dependencies, each listed once.
- Resolution: N/A — clean.

**[CLEAN] Cross-section mention of the same types**: Both `## Unreleased` and
`## Initial implementation (#6)` name the same types (Client, ClientBuilder, etc.). This is not
duplication: the two sections record distinct events separated in time — commit d6a9b6e
(2026-11-04T10:12) introduced the code; the `## Unreleased` entry records the formal API freeze
and acceptance-criteria verification. Keep a Changelog conventions assign each section to one
release point; mentioning the same types across sections at different levels of description
(brief source-file attribution vs. full signature specification) is correct structure.
- Principle: Different CHANGELOG entries describe different events; cross-section mentions of
  the same type name are not duplicates when the entries describe different events.
- Evidence: `## Initial implementation` names `Error` as "Error enum + Result type alias";
  `## Unreleased` gives the full `#[non_exhaustive]` enum definition and helper methods. The
  two descriptions are complementary, not copies.
- Resolution: N/A — clean.

**[CLEAN] Cross-commit duplication and contradiction (commit d6a9b6e vs 0436218)**: The
remediation commit (0436218) made targeted in-place corrections — it replaced incorrect
signatures (B1: `query` parameter type, B2: `Response::text` self/return type, SF3:
`header`/`default_header` parameter types) and added members that were entirely absent (SF4:
`Error::is_network()`, `Error::is_status()`, `Error::status()`, `Method::as_str()`,
`impl Display for Method`, `RequestBuilder::body_string()`, `Response::status_text()`,
`Response::headers()`, `Response::body()`). No entry exists in both its pre-correction and
post-correction form. The final document does not contain the original incorrect `query(key: &str,
value: &str)` signature alongside the corrected `query(params: &[(&str, &str)])` — only the
corrected form is present. No contradiction exists between the two commits' contributions to
the final file.
- Principle: A remediation commit that corrects existing entries in place does not create
  duplication; only if both old and new forms remain would duplication exist.
- Evidence: PR commit list (oid d6a9b6e, then 0436218); final diff shows single occurrence of
  each corrected method with the accurate signature.
- Resolution: N/A — clean.

**[CLEAN] Near-duplicate entries**: No near-duplicate entries found. The acceptance criteria
reference `Error::{Network,Status,Deserialize,...}` (enum variant names) while the API surface
spec documents `Error::is_network()`, `Error::is_status()`, `Error::status()` (helper methods).
These describe different aspects (variant identity vs. method accessors). RFC-3986 URL resolution
is noted as an implementation detail in `## Initial implementation (#6)` and as a verified
acceptance criterion in `## Unreleased`; different sections, different events, different
specificity. No entry appears under more than one version section with the same content.
- Principle: Same fact stated at different levels of abstraction in different sections for
  different purposes is not near-duplication.
- Evidence: "RFC-3986 URL resolution + percent-encoding" at diff +152 (source file attribution);
  "RequestBuilder chains URL resolution per RFC 3986" at diff +122 (acceptance criterion). These
  are in separate sections serving separate roles.
- Resolution: N/A — clean.
