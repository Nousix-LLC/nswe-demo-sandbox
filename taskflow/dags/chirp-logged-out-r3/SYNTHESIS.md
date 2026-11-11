# SYNTHESIS.md — chirp-logged-out-r3

**PR:** https://github.com/Nousix-LLC/nswe-demo/pull/263  
**Branch:** `work/chirp-logged-out` → `main`  
**Issue closed:** #35  
**CI status:** fmt ✓ clippy ✓ test ✓ wasm ✓ doc ✓ image (in progress, build-only on PR)

---

## Work done in this invocation

The branch `work/chirp-logged-out` already carried 6 feature commits from prior r-fork
runs (public_timeline backend + frontend logged-out experience). This invocation:

1. **Diagnosed the wasm CI failure**: PR #193 (async resources + expanded events) landed the new
   `EventHandler` enum (`NoArg` / `WithEvent`) and 47 `EventKind` variants, but `hydrate.rs`
   was never updated — it still called `handler()` as a function and only matched `Click` / `Input`.
   Three compiler errors on `wasm32` target.

2. **Merged main into the branch** (`5982429`) — brings in the full ferric API surface from PR #193.

3. **Fixed `crates/ferric/src/hydrate.rs`** (`2615ba1`) — brings the hydration event-wiring path
   into parity with `dom.rs`:
   - `static_event_kinds()` enumerates all 47 non-Custom variants for detachment
   - `Custom` listener slots tracked in `__ferric_custom_events` and cleaned up
   - Closure dispatches through `EventHandler::NoArg(f) => f()` / `::WithEvent(f) => f(&event)`
   - `event_name` and `stash_key` take `&EventKind`, return `String`, cover all variants

---

## Acceptance criteria

| # | Criterion | Status |
|---|-----------|--------|
| AC-1 | Logged-out visitor can load the home/public timeline and open a user profile without signing up | **MET** — `GET /api/public/timeline` requires no auth; `GET /api/users/{id}` is unauthenticated; frontend uses `ApiClient::public_timeline()` |
| AC-2 | On arrival with no content: statement of what Chirp is + visible sign-up/sign-in route; never blank | **MET** — `empty_view()` renders a description paragraph and "Create account" / "Sign in" links to `/compose` |
| AC-3 | Timeline load failure shows clear, recoverable message | **MET** — `error_banner()` renders an `aria-role=alert` paragraph; initial failure shows full-screen error with retry; inline load-more failure shows error + "Try again" |
| AC-4 | "Create an account" route visible from landing and sign-in screen | **MET** — persistent nav carries "Sign up" and "Sign in" links to `/compose`; empty_view carries "Create account" link |
| AC-5 | Loading, empty, error, and end-of-list states each visually distinct | **MET** — `chirp-loading`, `chirp-empty`, `chirp-error`, `chirp-end` are each distinct CSS-class-labelled elements; never blank or stale |

All 5 acceptance criteria are met.

---

## CI

All required jobs pass on commit `2615ba1`:

| Job | Conclusion |
|-----|-----------|
| fmt | success |
| clippy | success |
| test | success |
| wasm | success |
| doc | success |

The `image` job (container build) has also passed (2m 28s). All six jobs are `pass`.
