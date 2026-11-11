# _BRIEF.md — review-ferric-http-r2 (swe-reviewer)

**Task kind**: review  
**Goal**: Re-review PR #210 after ferric-http-r2 remediation — verify all original blockers and should-fix items are resolved

---

## Target

**PR**: #210 — `feat(ferric-http): document frozen API surface and close usable_early acceptance criteria (#132, #148)`  
**Branch**: `work/ferric-http-r1` → `main`  
**PR URL**: https://github.com/Nousix-LLC/nswe-demo/pull/210  
**Head commit**: `0436218` — `fix(ferric-http): correct API signatures in CHANGELOG.md (review-ferric-http-r1 blockers)`  
**CI**: 5/6 checks PASS on 0436218 (fmt, clippy, test, wasm, doc all SUCCESS; image build in progress — CHANGELOG-only change)

**Issues closed by this PR**:
- **#132** — ferric-http: frozen API surface (`usable_early` milestone) — Acceptance: `crates/ferric-http/CHANGELOG.md` documents the complete frozen public API surface; all usable_early API members present and correctly specified
- **#148** — ferric-http: HTTP client and JSON fetch client documentation (`usable_early`) — Acceptance: request builder, response, error, method, client builder all documented; signatures match the compiled crate

**Remediation DAG**: ferric-http-r2 (PASS) — SYNTHESIS at `taskflow/dags/ferric-http-r2/SYNTHESIS.md`

---

## What changed in the remediation commit (0436218)

The remediation fixed the 2 original blockers and all 3 should-fix items in `crates/ferric-http/CHANGELOG.md`:

- **B1 (query signature)**: Changed from `(self, key: &str, value: &str) -> Self` to `(self, params: &[(&str, &str)]) -> Self`
- **B2 (Response::text signature)**: Changed from `(&self) -> &str` to `(self) -> String`
- **SF3 (header/default_header)**: Changed from `impl Into<String>` to `&str` for both `RequestBuilder::header` and `ClientBuilder::default_header`
- **SF4 (missing public members)**: Added `Error::is_network`, `Error::is_status`, `Error::status`, `Method::as_str`, `Display for Method`, `RequestBuilder::body_string`, `Response::status_text`, `Response::headers`, `Response::body`
- **SF5 (non_exhaustive note)**: Added deferred note that `Method` will gain `#[non_exhaustive]` when `PATCH` is added in #149

---

## Review concerns

Review this PR as a whole, against both the acceptance criteria of #132 and #148 and the original blockers/should-fix items. Decide the concerns fresh from what the diff touches.

### Correctness (required)
Verify each changed signature matches the actual compiled API in the source files:
- `crates/ferric-http/src/request.rs`: `query()`, `header()`, `body_string()`
- `crates/ferric-http/src/response.rs`: `text()`, `status_text()`, `headers()`, `body()`
- `crates/ferric-http/src/client.rs`: `ClientBuilder::default_header()`
- `crates/ferric-http/src/error.rs`: `is_network()`, `is_status()`, `status()`
- `crates/ferric-http/src/lib.rs` or enum definition: `Method::as_str()`, `Display for Method`

Verify that every public API member present in the compiled crate (pub items exported from `crates/ferric-http/src/lib.rs`) is documented in `CHANGELOG.md`. Verify no documented member that does not exist in the source. Check that the `#[non_exhaustive]` deferred note correctly reflects the current source state.

### Code quality
Is `CHANGELOG.md` well-structured for its stated purpose (a frozen API surface declaration)? Are the additions coherent and placed correctly? No duplication.

### Security
No absolute host paths, private or internal network addresses, host runtime or taskflow directory references, or internal infrastructure details committed into the repository. This applies to all content in the CHANGELOG and commit messages.

---

## Declared output

1. **Posted review** on PR #210: an inline review comment carrying the verdict (APPROVE or REQUEST-CHANGES) and findings per concern, including what each concern found clean
2. **Root `SYNTHESIS.md`** at `taskflow/dags/review-ferric-http-r2/SYNTHESIS.md` with:
   - Verdict: APPROVE or REQUEST-CHANGES
   - Per-blocker resolution status (B1, B2)
   - Per-should-fix resolution status (SF3: #211, SF4: #212, SF5: #213)
   - Per-concern account of what was checked and what was found
   - Any remaining blockers or new findings with severity
   - Non-blocking findings (if any) for the board
3. **Non-blocking findings** filed as backlog issues (if any new ones found) — referenced from SYNTHESIS.md

**Note**: If the platform will not accept a formal approval (same account as PR author), post the verdict and findings as a review comment on PR #210. The SYNTHESIS.md verdict is authoritative.
