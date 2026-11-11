# SYNTHESIS — review-ferric-http-r2

**PR**: #210 (`work/ferric-http-r1` → `main`)  
**Head commit**: `0436218`  
**Reviewed by**: review-ferric-http-r2 DAG (correctness, code_quality, security spokes)

---

## Verdict: APPROVE

No BLOCKER findings in any concern area. All five carry-over items (B1, B2, SF3, SF4, SF5) are resolved with direct source-file evidence. Nine new non-blocking findings were filed; none prevent merge.

Review comment posted: https://github.com/Nousix-LLC/nswe-demo/pull/210#pullrequestreview-5775620356

---

## Original Blockers

**B1 — `query()` signature: RESOLVED**  
Source (`crates/ferric-http/src/request.rs`): `pub fn query(mut self, params: &[(&str, &str)]) -> Self`.  
CHANGELOG: `pub fn query(self, params: &[(&str, &str)]) -> Self;`.  
`mut` on `self` is an implementation detail not visible to callers; parameter type and return match. The original wrong signature `(self, key: &str, value: &str) -> Self` is gone.

**B2 — `Response::text()` signature: RESOLVED**  
Source (`crates/ferric-http/src/response.rs`): `pub fn text(self) -> String`.  
CHANGELOG: `pub fn text(self) -> String;`. Exact match.  
The original wrong signature `(&self) -> &str` is gone.

---

## Should-Fix Items

**SF3 — `header()` / `default_header()` parameter types: RESOLVED**  
Both `RequestBuilder::header` and `ClientBuilder::default_header` read `&str` in source and CHANGELOG. Neither uses `impl Into<String>`. Verified against `request.rs` and `client.rs`.

**SF4 — Missing public API members: RESOLVED**  
All nine members verified against source: `Error::is_network(&self) -> bool`, `Error::is_status(&self) -> bool`, `Error::status(&self) -> Option<u16>`, `Method::as_str(&self) -> &'static str`, `impl Display for Method`, `RequestBuilder::body_string(self, impl Into<String>) -> Self`, `Response::status_text(&self) -> &str`, `Response::headers(&self) -> &[(String, String)]`, `Response::body(&self) -> &str`. Each matches source.

**SF5 — `Method` `#[non_exhaustive]` deferral note: RESOLVED**  
The "Not in scope (deferred to issue #149)" block in the CHANGELOG names the deferral trigger (`#[non_exhaustive]` when PATCH variant added in #149) and cross-references the tracking issue. Source confirms `Method` currently has no `#[non_exhaustive]` attribute; the CHANGELOG matches.

---

## Concern-by-Concern Account

### Correctness

Examined: every documented signature in `crates/ferric-http/CHANGELOG.md` for the `usable_early` surface against the five source files (`request.rs`, `response.rs`, `client.rs`, `error.rs`, `lib.rs`) at commit `0436218`.

Found: B1, B2, SF3, SF4, SF5 all resolved. All documented signatures match source. The `mut` self binders in source (`query`, `header`, `default_header`, `body_string`) are implementation details invisible to callers and are not surfaced in the CHANGELOG — this is correct.

One new ADVISORY: `RequestBuilder::url()` is intentionally public (doc comment: "Exposed so callers — and tests — can inspect exactly where the request will go without performing it") but absent from the surface inventory. Filed as #215.

### Code Quality

Examined: five concern areas — structural coherence, placement correctness, duplication, formatting consistency, documentation completeness as API contract.

Found clean: heading hierarchy, reverse-chronological ordering, section separators, preamble boilerplate, code-fence language tags, inline formatting, version section placement, intra- and cross-section uniqueness, absence of cross-commit contradictions, and acceptance-criteria mapping.

One SHOULD_FIX found: `Error` does not document `impl Display for Error` or `impl std::error::Error for Error`. Both are part of the public contract; without `impl std::error::Error`, `Error` cannot be used with `Box<dyn std::error::Error>` or `anyhow::Error`. The same CHANGELOG documents `impl Display for Method`, making the gap on `Error` an omission rather than a formatting choice. Filed as #214.

Advisory items:
- `Response::body()` and `Response::text()` have no note explaining whether they return the same content under different ownership — #216
- `ClientBuilder::default_header` does not document its accumulation behavior, unlike `RequestBuilder::header` — #217
- No cross-reference to epic #132 in the `usable_early` section — #218
- H3 subsection naming (`### Verification: all usable_early acceptance criteria met`) diverges from the `### Added` convention in `ferric-router/CHANGELOG.md` — #219
- Uneven doc-comment coverage (two of six type blocks have `///` comments; the others do not) and one C-style block comment in the `Method` block — #220
- `## Initial implementation (#6)` goes directly to prose with no `###` subsection heading, asymmetric with `## Unreleased` — #221

### Security / Information Hygiene

Examined: `crates/ferric-http/CHANGELOG.md` additions (160 lines), commit messages for `d6a9b6e` and `0436218`, and the PR description — against six categories: absolute filesystem paths, IP addresses / private hostnames, taskflow/runtime directory references, SSH key paths or usernames, API keys or credentials, internal tooling references.

Found clean: no absolute host paths, no private IP addresses, no SSH material, no credentials or tokens, no Kubernetes cluster or ArgoCD identifiers. The Co-Authored-By attribution uses public email addresses, not internal credentials. The file reference `chirp-frontend/src/api.rs` in the acceptance-criteria table is a project-relative source path, appropriate for public documentation.

One ADVISORY: commit `0436218`'s message names an internal review orchestration workflow ID (`review-ferric-http-r1`) in both the headline and body. No server address, path, credential, or topology is exposed; the string only reveals that an internal orchestration system exists and uses this naming scheme. The commit is in the git log and cannot be changed. Filed as #222 as a future-practice note.

---

## New Findings Summary

| ID | Severity | Description | Issue |
|----|----------|-------------|-------|
| CQ-1 | SHOULD_FIX | `Error` does not document `impl Display` or `impl std::error::Error` | #214 |
| CO-A1 | ADVISORY | `RequestBuilder::url()` absent from CHANGELOG frozen surface declaration | #215 |
| CQ-A1 | ADVISORY | `Response::body()` / `Response::text()` no behavioral differentiation note | #216 |
| CQ-A2 | ADVISORY | `ClientBuilder::default_header` accumulation behavior not documented | #217 |
| CQ-A3 | ADVISORY | No cross-reference to epic #132 in `usable_early` section | #218 |
| CQ-A4 | ADVISORY | H3 subsection naming diverges from ferric-router convention | #219 |
| CQ-A5 | ADVISORY | Uneven doc-comment coverage and C-style comment in `Method` block | #220 |
| CQ-A6 | ADVISORY | Structural asymmetry between version sections | #221 |
| SEC-A1 | ADVISORY | Commit message names internal review workflow ID | #222 |

---

## Contract Identity Assertions

| Identity | Status |
|----------|--------|
| Every verified item (B1, B2, SF3, SF4, SF5) has explicit RESOLVED/UNRESOLVED/PARTIAL status in correctness_findings.md | HOLDS — all five carry "Resolution: RESOLVED" |
| Every concern area (Correctness, Code Quality, Security) has a verdict contribution | HOLDS — each spoke declares APPROVE |
| The verdict in SYNTHESIS.md matches the verdict posted on PR #210 | HOLDS — both are APPROVE |
| No BLOCKER finding coexists with an APPROVE verdict | HOLDS — no BLOCKERs in any spoke |

---

## Wiring Verification

All three spoke output files present and schema-conformant (all required sections per `contracts/findings_schema.yaml` present in each file):

| File | Present | Has ## Summary | Has ## Findings | Has ## Verdict contribution |
|------|---------|----------------|-----------------|----------------------------|
| SUBTASK_correctness/correctness_findings.md | ✓ | ✓ | ✓ | ✓ |
| SUBTASK_code_quality/code_quality_findings.md | ✓ | ✓ | ✓ | ✓ |
| SUBTASK_security/security_findings.md | ✓ | ✓ | ✓ | ✓ |
