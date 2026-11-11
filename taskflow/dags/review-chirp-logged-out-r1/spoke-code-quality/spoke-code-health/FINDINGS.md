## Verdict

FINDINGS

---

## Findings

### Finding 1: sign_up::sign_up_view is an unreachable public export

- **Location**: `crates/chirp-frontend/src/sign_up.rs`, line 23 at commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- **Principle at stake**: Dead exports. A `pub` function that no caller in the crate can reach through any live code path is dead code, regardless of whether it compiles.
- **Why it matters**: Two functions now share the name concept "signup view" but do different things: `compose::signup_view` is the live handler with full registration logic; `sign_up::sign_up_view` is a disabled stub that was the intended home for that logic but was bypassed when the implementation landed in `compose.rs`. The `lib.rs` module-doc for `sign_up` says it is the "/signup -- sign-up entry point", which contradicts the route table. A contributor reading `sign_up.rs` to understand the signup flow will find a stub rather than the live code, and may not discover `compose::signup_view` without reading the route table. The stub's disabled button ("coming soon") is also misleading — registration is live.
- **Severity**: non-blocking
- **Satisfying condition**: Either remove `sign_up::sign_up_view` and its test module (and correct `lib.rs`'s doc for the `sign_up` module to reflect that `/signup` is now handled by `compose::signup_view`), or — if `sign_up.rs` is intentionally kept as the future home of a richer registration form — add a module-level doc note that the current export is not wired to any route and that `compose::signup_view` is the active handler.

---

### Finding 2: Framework fix bundled in application feature PR

- **Location**: `crates/ferric/src/hydrate.rs`, lines 417–490 at commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- **Principle at stake**: PR scope discipline — framework changes belong in framework PRs
- **Why it matters**: The hydrate.rs changes correct a pre-existing framework bug (the detachment pass covered 2 of 47 event kinds) and are located in `crates/ferric/`, not `crates/chirp-frontend/`. Mixing framework-layer correctness work with an application feature PR couples a framework fix to a feature review, complicates bisect and rollback, and obscures the blast radius if either part needs reverting independently. The vdom.rs doc comment explicitly states feature spokes should not add EventKind variants, reinforcing the expectation that changes to ferric have their own PRs.
- **Severity**: non-blocking
- **Satisfying condition**: Accept the bundled change as-is (the fix is correct and matches the dom.rs pattern), or extract the ferric changes into a preceding framework PR and rebase this PR onto it. No code correction is required if the team accepts the scope.

---

### Finding 3: `static_event_kinds()` lacks a compile-time completeness guard

- **Location**: `crates/ferric/src/hydrate.rs`, line 494 at commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- **Principle at stake**: Compile-time enforcement over advisory comments for enum-to-table mappings
- **Why it matters**: `event_name()` and `stash_key()` enforce their own completeness through exhaustive match arms — the compiler rejects the build if either is out of sync with `EventKind`. `static_event_kinds()` enforces only that it returns exactly 47 elements, not that those 47 elements cover all static variants. A developer forced by the compiler to update `event_name()` and `stash_key()` has no compiler signal to also update `static_event_kinds()`. If the omission is not caught in review, re-renders of elements carrying that event kind silently accumulate listeners with each render cycle. The same gap exists at `crates/ferric/src/dom.rs`, line 309. The vdom.rs "frozen" declaration reduces the probability but is not enforced.
- **Severity**: non-blocking
- **Satisfying condition**: Add a guard that makes omission from `static_event_kinds()` a build or test failure. Options: (a) a `#[cfg(test)]` function that iterates `static_event_kinds()` and calls `event_name()` and `stash_key()` on each element, then asserts a known count — this will fail to compile when a new variant is added to `event_name` / `stash_key` but absent from the array; (b) replace the hand-written array with a derived iterator using `strum::IntoEnumIterator` filtered to skip `Custom`; (c) add a `strum::EnumCount` derive and assert `static_event_kinds().len() + 1 == EventKind::COUNT` (the +1 accounts for `Custom`). The fix must be applied to both `hydrate.rs` and `dom.rs`.

---

## Clean Account

- **Concern 6 — sign_up::sign_up_view reachability**: Checked `app.rs` (route table), `sign_up.rs`, `compose.rs`, `lib.rs`, and the PR diff. The `/signup` route binds to `compose::signup_view`; `sign_up::sign_up_view` has no caller in any live code path. See Finding 1.
- **Concern 7 — hydrate.rs scope and sync risk**: Checked `hydrate.rs`, `dom.rs`, `vdom.rs`, and the PR diff. The EventKind expansion brings `hydrate.rs` into alignment with `dom.rs` by completing coverage of variants already present in the enum before this PR. The changes are framework-layer work bundled with an application feature (Finding 2). `static_event_kinds()` is not compiler-enforced for completeness, leaving a latent silent-failure path if a new variant is added without updating the hand-written array (Finding 3).
