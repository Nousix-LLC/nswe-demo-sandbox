# Correctness Findings — SUBTASK_correctness

**PR**: #210 (`work/ferric-http-r1` → `main`)  
**Head commit under review**: `0436218`  
**Concern area**: Signature correctness — CHANGELOG.md against source (ground truth)

---

## Summary

This review checked all five carry-over items (B1, B2, SF3, SF4, SF5) by reading the actual Rust source files at commit `0436218` and comparing every documented signature in `crates/ferric-http/CHANGELOG.md` against them. Source files read: `request.rs`, `response.rs`, `client.rs`, `error.rs`, and `lib.rs`. Every documented item was found in source. Every source signature for the five carry-over items matches what the CHANGELOG now documents. One public method on `RequestBuilder` (`url()`) is present in source but absent from the CHANGELOG surface inventory; this is recorded as an ADVISORY. No blockers found in this concern area.

---

## Findings

**[CLEAN] B1 — `RequestBuilder::query()` signature**
- File: `crates/ferric-http/src/request.rs`
- Principle: Documented API signatures must match the compiled source (Rust library API stability — the CHANGELOG is the declared frozen surface for issue #132/#148)
- Evidence: Source: `pub fn query(mut self, params: &[(&str, &str)]) -> Self`. CHANGELOG: `pub fn query(self, params: &[(&str, &str)]) -> Self;`. The `mut` binding on `self` is an implementation detail invisible to callers; parameter type `&[(&str, &str)]` and return `-> Self` match exactly. The original blocker was `(self, key: &str, value: &str) -> Self`; that signature is gone.
- Resolution: RESOLVED — no action needed.

**[CLEAN] B2 — `Response::text()` signature**
- File: `crates/ferric-http/src/response.rs`
- Principle: Same as B1 — documented signatures must match source.
- Evidence: Source: `pub fn text(self) -> String`. CHANGELOG: `pub fn text(self) -> String;`. Exact match. The original blocker was `(&self) -> &str`; that signature is gone. The method consumes `self` and returns owned `String` as intended.
- Resolution: RESOLVED — no action needed.

**[CLEAN] SF3 — `header()` and `default_header()` use `&str` parameters**
- Files: `crates/ferric-http/src/request.rs`, `crates/ferric-http/src/client.rs`
- Principle: API documentation must accurately reflect parameter types so callers know the borrowing contract.
- Evidence:
  - `RequestBuilder::header` — source: `pub fn header(mut self, name: &str, value: &str) -> Self`; CHANGELOG: `pub fn header(self, name: &str, value: &str) -> Self;`. Match.
  - `ClientBuilder::default_header` — source: `pub fn default_header(mut self, name: &str, value: &str) -> Self`; CHANGELOG: `pub fn default_header(self, name: &str, value: &str) -> Self;`. Match.
  - Neither uses `impl Into<String>`; both correctly document `&str`.
- Resolution: RESOLVED — no action needed.

**[CLEAN] SF4 — All missing public API members added**
- Files: `error.rs`, `request.rs`, `response.rs`
- Principle: A frozen public surface declaration (issue #132/#148) must enumerate every public member; omissions mislead callers and break discoverability.
- Evidence — each member checked against source and CHANGELOG:
  - `Error::is_network()`: source `pub fn is_network(&self) -> bool`; CHANGELOG `pub fn is_network(&self) -> bool;` ✓
  - `Error::is_status()`: source `pub fn is_status(&self) -> bool`; CHANGELOG `pub fn is_status(&self) -> bool;` ✓
  - `Error::status()`: source `pub fn status(&self) -> Option<u16>`; CHANGELOG `pub fn status(&self) -> Option<u16>;` ✓
  - `Method::as_str()`: source `pub fn as_str(&self) -> &'static str`; CHANGELOG `pub fn as_str(&self) -> &'static str;` ✓
  - `Method Display`: source has `impl std::fmt::Display for Method`; CHANGELOG shows `impl std::fmt::Display for Method { /* delegates to as_str() */ }` ✓
  - `RequestBuilder::body_string()`: source `pub fn body_string(mut self, body: impl Into<String>) -> Self`; CHANGELOG `pub fn body_string(self, body: impl Into<String>) -> Self;` ✓
  - `Response::status_text()`: source `pub fn status_text(&self) -> &str`; CHANGELOG `pub fn status_text(&self) -> &str;` ✓
  - `Response::headers()`: source `pub fn headers(&self) -> &[(String, String)]`; CHANGELOG `pub fn headers(&self) -> &[(String, String)];` ✓
  - `Response::body()`: source `pub fn body(&self) -> &str`; CHANGELOG `pub fn body(&self) -> &str;` ✓
- Resolution: RESOLVED — no action needed.

**[CLEAN] SF5 — `Method` `#[non_exhaustive]` deferral note added, referencing #149**
- File: `crates/ferric-http/CHANGELOG.md`, `crates/ferric-http/src/request.rs`
- Principle: A publicly exported enum without `#[non_exhaustive]` is a semver hazard once new variants are anticipated; the CHANGELOG should state the intent explicitly.
- Evidence: Source confirms `Method` has no `#[non_exhaustive]` attribute (`#[derive(Debug, Clone, Copy, PartialEq, Eq)]` is the only attribute). CHANGELOG documents `Method` without `#[non_exhaustive]`, matching source. The "Not in scope (deferred to issue #149)" block explicitly states: "PATCH method (REQ-HTTP-009); when added in #149, `Method` will gain `#[non_exhaustive]`." This names the deferral, identifies the trigger, and references the tracking issue.
- Resolution: RESOLVED — no action needed.

**[ADVISORY] ADVISORY-1 — `RequestBuilder::url()` is public in source but absent from the CHANGELOG surface inventory**
- File: `crates/ferric-http/src/request.rs`
- Principle: A CHANGELOG that claims to freeze the public surface (issue #132/#148: "this entry records the formal closure of #148 and declares the frozen public surface") should enumerate every public method on every publicly exported type.
- Evidence: Source has `pub fn url(&self) -> String` on `RequestBuilder`, with a doc comment reading "Exposed so callers — and tests — can inspect exactly where the request will go without performing it." The method is intentionally public. The CHANGELOG's `RequestBuilder` section lists six methods (`query`, `header`, `json`, `body_string`, `send`, `send_json`) and omits `url`. Every other public method on every other exported type is accounted for.
- Resolution: Add `pub fn url(&self) -> String;` to the `RequestBuilder` block in the CHANGELOG, with a one-line doc note matching the existing style. This is a documentation gap, not a code defect; the method is correct and the omission does not affect runtime behavior. Does not block merge.

---

## Verdict contribution

**APPROVE**

No blockers found in the correctness concern area. All five carry-over items (B1, B2, SF3, SF4, SF5) are resolved with direct source-file evidence at commit `0436218`. The single new finding (ADVISORY-1) is a documentation completeness gap on one convenience method and does not prevent merge.
