# _FORK.md — ferric-http-r2 DAG fork record

owner_id: overseer/I239
owning_thread: overseer/I239
thread_type: dag
launch_agent: swe-coder
observation_seam: taskflow/dags/ferric-http-r2/SYNTHESIS.md
reap_policy: retain
disposition: retain
goal: "Remediation: fix ferric-http CHANGELOG.md API signatures (blockers from review-ferric-http-r1, PR #210)"

---

# ferric-http-r2 — Remediation: fix CHANGELOG.md API signatures (blockers from review-ferric-http-r1)

**Goal**: Fix `crates/ferric-http/CHANGELOG.md` on branch `work/ferric-http-r1` to correct two API signatures that do not match the compiled code, so PR #210 can pass re-review and land.

**Repo**: `Nousix-LLC/nswe-demo`  
**Branch**: `work/ferric-http-r1` (amend or add commits to this branch; do not create a new branch)  
**PR**: #210 (already open — `work/ferric-http-r1` → `main`)  
**Issues closed by PR #210**: #132 (ferric-http 1.0 usable_early epic), #148 (HTTP methods, JSON bodies, error handling)

---

## Blockers to fix (from review-ferric-http-r1)

### B1 — `query()` signature wrong

**CHANGELOG declares**:
```rust
pub fn query(self, key: &str, value: &str) -> Self
```

**Actual (`crates/ferric-http/src/request.rs`)**:
```rust
pub fn query(mut self, params: &[(&str, &str)]) -> Self
```

The actual API takes a **slice of key-value pairs**, not two individual `&str` arguments. Fix the CHANGELOG to show the correct signature: `pub fn query(self, params: &[(&str, &str)]) -> Self` (use `self`, not `mut self`, in the public API declaration — `mut` is an implementation detail).

### B2 — `Response::text()` signature wrong

**CHANGELOG declares**:
```rust
pub fn text(&self) -> &str
```

**Actual (`crates/ferric-http/src/response.rs`)**:
```rust
pub fn text(self) -> String
```

`text()` **consumes the response** and returns an owned `String`. Fix the CHANGELOG to show the correct signature: `pub fn text(self) -> String`.

---

## Context: should-fix items (non-blockers — address if feasible while editing CHANGELOG.md)

These were non-blocking review findings from review-ferric-http-r1. They are already filed as backlog issues (#211, #212, #213). Addressing them in this remediation is not required to unblock the re-review, but would be a clean and efficient use of the edit.

- **SF3** (#211): `header()` and `default_header()` are declared with `impl Into<String>` parameter type, but the actual implementation takes `&str`.
- **SF4** (#212): Several public API members are absent from the frozen surface declaration:
  - `Error::is_network() -> bool`, `Error::is_status() -> bool`, `Error::status() -> Option<u16>`
  - `Method::as_str() -> &'static str`, `impl Display for Method`
  - `RequestBuilder::body_string(self, body: impl Into<String>) -> Self`
  - `Response::status_text() -> &str`, `Response::headers() -> &[(String, String)]`, `Response::body() -> &str`
- **SF5** (#213): `Method` enum is not `#[non_exhaustive]`; issue #149 adds `PATCH`. The deferred items note should state the chosen approach.

**Verify all API members against the actual source** before committing — read `src/request.rs`, `src/response.rs`, `src/error.rs`, `src/method.rs` to ensure the CHANGELOG matches the compiled code on all points.

---

## Acceptance criteria

A re-review of PR #210 by `swe-reviewer` must find:

1. `query()` signature in CHANGELOG matches the actual compiled API signature  
2. `Response::text()` ownership and return type in CHANGELOG matches the actual compiled API  
3. CI on `work/ferric-http-r1` passes all 6 checks  
4. PR #210 is still open and updated

---

## Declared output

- Updated `crates/ferric-http/CHANGELOG.md` committed to `work/ferric-http-r1`
- Root `SYNTHESIS.md` at `taskflow/dags/ferric-http-r2/SYNTHESIS.md` with verdict (PASS / FAIL), listing each blocker and whether it was resolved

## Notes

- Read the actual source files (`src/request.rs`, `src/response.rs`, etc.) to verify every signature before committing — do not guess
- Branch `work/ferric-http-r1` already has the original CHANGELOG.md commit `d6a9b6e`; amend or add a new commit on top of it
- Do not modify source code; fix only the CHANGELOG documentation
- Commit message: `fix(ferric-http): correct API signatures in CHANGELOG.md (review-ferric-http-r1 blockers)`
