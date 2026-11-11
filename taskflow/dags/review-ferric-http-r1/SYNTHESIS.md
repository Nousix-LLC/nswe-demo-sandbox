# Review Synthesis — PR #210 ferric-http usable_early surface

**Node**: review-ferric-http-r1  
**PR**: https://github.com/Nousix-LLC/nswe-demo/pull/210  
**Review comment**: https://github.com/Nousix-LLC/nswe-demo/pull/210#issuecomment-6639957464  
**Verdict**: REQUEST CHANGES

---

## What this PR does

Adds `crates/ferric-http/CHANGELOG.md` (142 lines added, 0 deleted). No implementation
changes. The CHANGELOG formally closes issues #148 (HTTP methods, JSON bodies, error
handling) and #132 (the ferric-http 1.0 epic) by declaring the frozen public API surface
for the `usable_early` scope.

---

## Findings

### Blockers

**1. `query()` signature wrong**  
CHANGELOG: `pub fn query(self, key: &str, value: &str) -> Self`  
Actual (`src/request.rs`): `pub fn query(mut self, params: &[(&str, &str)]) -> Self`  
The actual API takes a slice of key-value pairs. The declared signature does not compile
against any real call site.

**2. `Response::text()` signature wrong**  
CHANGELOG: `pub fn text(&self) -> &str`  
Actual (`src/response.rs`): `pub fn text(self) -> String`  
`text()` consumes the response and returns an owned `String`. The declared form borrows and
returns a slice — a different ownership model that cannot be substituted for the real one.

### Should-fix

**3. `header()` / `default_header()` declared with `impl Into<String>`, actual `&str`**  
The CHANGELOG claims callers can pass a `String` directly; the actual API requires a `&str`.

**4. Several public API members absent from frozen surface declaration**  
- `Error::is_network()`, `Error::is_status()`, `Error::status() -> Option<u16>`
- `Method::as_str() -> &'static str`, `impl Display for Method`
- `RequestBuilder::body_string(self, body: impl Into<String>) -> Self`
- `Response::status_text() -> &str`, `Response::headers() -> &[(String, String)]`, `Response::body() -> &str`

**5. `Method` not `#[non_exhaustive]`, issue #149 adds PATCH**  
Adding `Patch` without `#[non_exhaustive]` is a semver-major breaking change. The deferred
items note should state the chosen approach explicitly.

---

## What was clean

- `Error::Status.body: Option<String>` typed correctly in both CHANGELOG and code
- `#[non_exhaustive]` on `Error` correctly applied and documented
- Code quality: URL resolution is pure and well-tested; `has_header()` guard in `json()` correct; `pub(crate)` on internal constructors correct
- Test coverage: each module tests behavior at meaningful boundary conditions
- `std::error::Error` source chain correct for `Serialize`/`Deserialize` variants
- Acceptance criteria table accurate for every criterion verified

---

## Disposition

PR should not merge in current form. The CHANGELOG has two signatures that do not match
the compiled API, overstates parameter types on two methods, and omits several public
members from the frozen surface it exists to declare. The blockers are straightforward
fixes; the should-fix items complete the declaration.
