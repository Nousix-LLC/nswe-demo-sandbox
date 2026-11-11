# SYNTHESIS — ferric-http-r2

**Task**: Remediation: fix CHANGELOG.md API signatures (blockers from review-ferric-http-r1)  
**Branch**: `work/ferric-http-r1`  
**PR**: #210 (open — `work/ferric-http-r1` → `main`)  
**Commit**: `0436218` — `fix(ferric-http): correct API signatures in CHANGELOG.md (review-ferric-http-r1 blockers)`

---

## Verdict: PASS

All blockers resolved. All should-fix items addressed in the same edit.

---

## Blocker Resolution

### B1 — `query()` signature

**Status**: ✅ RESOLVED

| | Signature |
|---|---|
| Was (incorrect) | `pub fn query(self, key: &str, value: &str) -> Self` |
| Now (correct) | `pub fn query(self, params: &[(&str, &str)]) -> Self` |

Verified against `crates/ferric-http/src/request.rs` line 120:
`pub fn query(mut self, params: &[(&str, &str)]) -> Self`
(The `mut` on `self` is an implementation detail; the public declaration correctly omits it.)

### B2 — `Response::text()` signature

**Status**: ✅ RESOLVED

| | Signature |
|---|---|
| Was (incorrect) | `pub fn text(&self) -> &str` |
| Now (correct) | `pub fn text(self) -> String` |

Verified against `crates/ferric-http/src/response.rs` line 94:
`pub fn text(self) -> String`

---

## Should-Fix Items (all addressed)

### SF3 — `header()` / `default_header()` declared with `impl Into<String>`

**Status**: ✅ FIXED

Both methods actually take `&str`, not `impl Into<String>`:
- `RequestBuilder::header(self, name: &str, value: &str) -> Self` — fixed from `impl Into<String>`
- `ClientBuilder::default_header(self, name: &str, value: &str) -> Self` — fixed from `impl Into<String>`

Verified against `src/request.rs` line 112 and `src/client.rs` line 115.

### SF4 — Missing public API members

**Status**: ✅ ADDED

The following members exist in the compiled crate but were absent from the frozen surface declaration. All have been added:

**`Error` impl block** (new):
- `pub fn is_network(&self) -> bool`
- `pub fn is_status(&self) -> bool`
- `pub fn status(&self) -> Option<u16>`

**`Method` impl and Display** (new):
- `pub fn as_str(&self) -> &'static str`
- `impl std::fmt::Display for Method`

**`RequestBuilder`** (added):
- `pub fn body_string(self, body: impl Into<String>) -> Self`

**`Response`** (added):
- `pub fn status_text(&self) -> &str`
- `pub fn headers(&self) -> &[(String, String)]`
- `pub fn body(&self) -> &str`

All verified against source files.

### SF5 — `Method` not `#[non_exhaustive]`; deferred note

**Status**: ✅ NOTED

The deferred items note now reads:
> `PATCH` method (REQ-HTTP-009); when added in #149, `Method` will gain `#[non_exhaustive]`

This records the chosen approach: `Method` will become `#[non_exhaustive]` at the same time `PATCH` is added in issue #149. The current source does not yet have `#[non_exhaustive]` on `Method`, so it was not added to the surface declaration.

---

## Verification

- Source files read and all signatures cross-checked: `src/request.rs`, `src/response.rs`, `src/error.rs`, `src/client.rs`
- `crates/ferric-http/CHANGELOG.md` updated on branch `work/ferric-http-r1`
- Commit `0436218` pushed to `origin/work/ferric-http-r1`
- PR #210 remains OPEN: https://github.com/Nousix-LLC/nswe-demo/pull/210
- No source code was modified; only `CHANGELOG.md` was changed
