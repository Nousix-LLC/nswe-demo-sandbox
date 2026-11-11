# SUBTASK_correctness: Signature Correctness Verification

## Task Specification

**Slug**: SUBTASK_correctness  
**Task Kind**: standard  
**Depends on**: none  
**Status**: Pending

### Objective

Verify that the ferric-http-r2 remediation commit (`0436218`) has resolved the original blockers B1 and B2, and the should-fix items SF3, SF4, and SF5, by reading the actual Rust source files and comparing every documented signature in CHANGELOG.md against them.

### Context

This is a spoke task in review-ferric-http-r2. See `../_GLOBAL.md` for full background, blocker/should-fix definitions, and subtree constraints.

**Depends on**: none — reads source files directly  
**Dependents**: `SUBTASK_verdict` reads `correctness_findings.md`

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Project context | `../_GLOBAL.md` | Blocker/SF definitions, constraints |
| Findings schema | `../contracts/findings_schema.yaml` | Required output structure |
| request.rs | `crates/ferric-http/src/request.rs` | Ground truth for RequestBuilder, query(), header(), body_string() |
| response.rs | `crates/ferric-http/src/response.rs` | Ground truth for Response::text(), status_text(), headers(), body() |
| client.rs | `crates/ferric-http/src/client.rs` | Ground truth for Client API |
| error.rs | `crates/ferric-http/src/error.rs` | Ground truth for Error::is_network(), is_status(), status() |
| lib.rs | `crates/ferric-http/src/lib.rs` | Ground truth for pub re-exports and Method |
| CHANGELOG.md | repo root | Documented API surface to verify |
| PR #210 diff | `gh pr diff 210 --repo Nousix-LLC/nswe-demo` | Exact lines added/changed |

---

## Process Specification

For each of the 5 items (B1, B2, SF3, SF4, SF5), read the relevant source file(s) first, then read the corresponding CHANGELOG.md entry, then compare. Record each item's status (RESOLVED / UNRESOLVED / PARTIAL) with explicit source-file evidence (filename, function/type name as it appears in source).

Specifically:

- **B1**: Find `query()` on RequestBuilder in request.rs. Check the CHANGELOG documents it as `(self, params: &[(&str, &str)]) -> Self` (not `(self, key: &str, value: &str) -> Self`).
- **B2**: Find `text()` on Response in response.rs. Check the CHANGELOG documents it as `(self) -> String` (not `(&self) -> &str`).
- **SF3**: Find `header()` and `default_header()` in request.rs or client.rs. Check the CHANGELOG documents their `&str` parameters (not `impl Into<String>`).
- **SF4**: Check the CHANGELOG documents all of: `Error::is_network()`, `Error::is_status()`, `Error::status()`, `Method::as_str()`, `Method`'s `Display` impl, `RequestBuilder::body_string()`, `Response::status_text()`, `Response::headers()`, `Response::body()`. Verify each against its source file.
- **SF5**: Find `Method` in lib.rs or its definition. Check whether CHANGELOG adds a note about `#[non_exhaustive]` being deferred, referencing issue #149.

Also check: are there any public items exported from the crate root (via lib.rs pub re-exports) that are NOT documented in the CHANGELOG? If so, record as a finding.

Are there any items documented in CHANGELOG that cannot be found in the source? If so, record as a blocker.

---

## Output Specification

**File**: `correctness_findings.md`  
**Location**: `SUBTASK_correctness/`  
**Schema**: `../contracts/findings_schema.yaml`

Required sections (per schema):
- `## Summary` — what was checked, overall result
- `## Findings` — per-item (B1, B2, SF3, SF4, SF5), plus any new findings. Each CLEAN finding explicitly states what was verified and found sound.
- `## Verdict contribution` — APPROVE or REQUEST-CHANGES from this concern area

---

## Success Criteria

- [ ] B1 status: RESOLVED or UNRESOLVED with source-file evidence
- [ ] B2 status: RESOLVED or UNRESOLVED with source-file evidence
- [ ] SF3 status: RESOLVED or UNRESOLVED or PARTIAL with source-file evidence
- [ ] SF4 status: RESOLVED or UNRESOLVED or PARTIAL with source-file evidence
- [ ] SF5 status: RESOLVED or UNRESOLVED or PARTIAL with source-file evidence
- [ ] Any newly discovered finding recorded with severity classification
- [ ] `correctness_findings.md` written following the schema

---

## Suggested Methodology Files

**Task-type row (from Domain Mapping):** "Ferric PR review (Rust library)" — Primary: Code Review; Supporting: Rust, Framework Design

Suggested files:
- `code-review/CodeReview_Checklist_Methodology.md` — the standard review checklist; correctness is its first concern. Rationale: grounds the per-item verification pass in an explicit discipline rather than ad hoc comparison.
- `code-review/CodeReview_Process_Methodology.md` — review process; "read the source as the ground truth" discipline. Rationale: the whole task is a correctness check on CHANGELOG against source.
- `rust/Rust_Library_API_And_Stability_Methodology.md` — Rust library public API conventions; signature shapes (self vs &self, Into<> vs concrete types). Rationale: B1/B2/SF3 are specifically about API signature shape.
- `framework-design/FrameworkDesign_Library_API_Design_Methodology.md` — library API design; what makes a signature doc correct vs incorrect. Rationale: SF4 requires checking completeness of the documented public surface.

These are suggestions. Load fewer if some are clearly inapplicable; load more if your reading of the source reveals additional methodology surface.

## Inherited Constraints

- Ground truth is the Rust source, not prior review notes or the PR description
- Head commit under review: `0436218`
- Repo: `Nousix-LLC/nswe-demo` — use `gh` CLI for all GitHub operations
- Output file must follow `../contracts/findings_schema.yaml`

## Out-of-Scope Methodologies

- Testing methodology — this task reads source for correctness, not for test quality
- Security methodology — handled by SUBTASK_security
- Code quality / structure methodology — handled by SUBTASK_code_quality
