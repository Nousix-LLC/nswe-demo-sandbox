# Findings: B1 and B2 Fix Verification

**PR**: #263 (`work/chirp-logged-out`)  
**HEAD reviewed**: 7f4b684671cab7eb778f5ad7f54dfdc82d57b3c4  
**Diff reviewed**: decb6196..7f4b684

---

## Fix verdicts

| Fix | Verdict | Evidence |
|-----|---------|----------|
| B1 (timeline.rs) | PASS | `timeline.rs:218` reads `ctx.client().timeline(&query).await`; no `pub_timeline` call remains in `timeline.rs`; `timeline()` uses `self.token` and routes to `/api/timeline`. |
| B2 (compose.rs) | PASS | `compose.rs:519` reads `link("/signin", "Log in →")`; `/signin` resolves to `sign_in_view` in the route table. |

---

## Code quality: PASS

The remediation is a single commit (`7f4b684`) with the message "fix(chirp-frontend): revert auth timeline to personalized feed, fix signup Log-in link". Two files changed, one line each.

- **`timeline.rs:218`**: one identifier replaced (`pub_timeline` → `timeline`), no whitespace or formatting drift, surrounding `spawn_local` block untouched.
- **`compose.rs:519`**: one string literal replaced (`"/compose"` → `"/signin"`), surrounding `render_signup` builder chain untouched.

Both changes follow codebase naming and style conventions. Commit message is accurate and correctly scoped.

---

## Test coverage: FLAG

**B1**: No automated test was added in the remediation verifying that `timeline_view` calls `ctx.client().timeline()` rather than `ctx.client().pub_timeline()`. The r1 B1 finding stated "the fix needs a frontend test or manual verification confirming `timeline_view` calls `timeline()`, not `pub_timeline()`." Manual verification is complete — direct inspection of `timeline.rs:218` at HEAD confirms the fix — but no regression guard was added. If this line were accidentally reverted, the existing test suite would not catch it.

The `pub_timeline_url_has_correct_path_and_no_auth` test in `api.rs:434` (non-blocker CQ-C, issue already filed from r1) tests the `pub_timeline()` method itself; it does not cover the call site in `timeline_view`.

**B2**: No test explicitly verifies that `render_signup` renders "Log in →" pointing to `/signin`. A regression reintroducing `"/compose"` at `compose.rs:519` would not be caught by the existing suite.

Both gaps are non-blocking — the fixes themselves are correct and confirmed. See non-blocking findings TC-B1 and TC-B2 below.

---

## Security: PASS

- **B1**: `ChirpApiClient::timeline()` (`api.rs:176–188`) builds an authenticated HTTP client using `self.token` and calls `GET /timeline`. The substitution at `timeline.rs:218` restores authenticated users to their personalized feed with no new credential handling or token-exposure surface.
- **B2**: A routing-string change in a rendered hyperlink. No input, no processing, no exploitable surface.
- Remediation diff contains no host paths, internal network addresses, unsafe blocks, or new dependencies.

---

## Regression: PASS

The remediation diff `decb6196..7f4b684` consists of exactly the two targeted single-line fixes and nothing more: one commit, two files, 1 addition and 1 deletion each. No new files, no dependency changes, no reformatting of neighboring code.

---

## Non-blocking findings

| ID | Location | Severity | Description |
|----|----------|----------|-------------|
| TC-B1 | `crates/chirp-frontend/src/timeline.rs` | Non-blocking | No frontend test verifies that `timeline_view` calls `ctx.client().timeline()` rather than `pub_timeline()`. Add a test to `timeline.rs`'s `mod tests` asserting that the authenticated call is made. This was flagged as a requirement in the r1 B1 finding ("a frontend test or manual verification"); the manual bar has been met but the automated regression guard remains absent. |
| TC-B2 | `crates/chirp-frontend/src/compose.rs:519` | Non-blocking | No test verifies that `render_signup` renders "Log in →" pointing to `/signin`. Add a test to `compose.rs`'s `mod tests` asserting that the link target is `/signin`, so a regression to `/compose` would be caught. |

Non-blockers from r1 (issues #264–#271) already tracked; not re-filed here.

---

## Clean items

- **B1 call site** (`timeline.rs:218`): `ctx.client().timeline(&query).await` confirmed at the exact line cited in r1. No other call to `pub_timeline` exists in `timeline.rs`. The module-level doc at `timeline.rs:4` documents `ctx.client().timeline(..)` as the correct call — the fix is now consistent with its own specification.
- **B2 link destination** (`compose.rs:519`): `link("/signin", "Log in →")` confirmed at the exact line cited in r1, inside `render_signup` (the sign-up form renderer). The route entry `/signin` → `sign_in_view` is present in the route table, so the destination resolves correctly.
- **B1 method contract** (`api.rs:176–209`): `timeline()` and `pub_timeline()` differ only in auth header and endpoint path. The fix at `timeline.rs:218` unambiguously restores authenticated users to the personalized feed (`GET /api/timeline`) and away from the global unauthenticated feed (`GET /api/public/timeline`).
- **Diff scope**: The remediation is minimal — exactly the two lines requested, in one focused commit. No collateral changes found.
