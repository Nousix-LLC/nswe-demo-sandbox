## Concern 7 — hydrate.rs Scope and Sync Risk

## Investigation

Three sources were read: `crates/ferric/src/hydrate.rs` at commit `decb6196`, `crates/ferric/src/dom.rs` at the same commit, and the PR #263 diff. The diff lists one ferric crate file changed: `crates/ferric/src/hydrate.rs`. Neither `crates/ferric/src/vdom.rs` nor `crates/ferric/src/dom.rs` appears in the diff.

The `EventKind` enum is defined in `crates/ferric/src/vdom.rs`, which was not changed in PR #263. At the pinned commit it already contained all 47 static variants plus `Custom(String)`. `EventHandler::WithEvent` was also already present in `vdom.rs`. Before this PR, `hydrate.rs::set_events` hardcoded a 2-element detachment array (`[EventKind::Click, EventKind::Input]`), and `event_name` / `stash_key` each had 2 match arms. The PR expanded all three to cover all 47 static variants, matching the pre-existing pattern in `crates/ferric/src/dom.rs` (which already had `static_event_kinds() -> [EventKind; 47]` and exhaustive matches at the pinned commit, at line 309 and surrounding). The vdom.rs doc comment on `EventKind` reads: "The full set is frozen by the walking skeleton; feature spokes consume these variants but do not add new ones."

The hydrate.rs changes sit in `crates/ferric/` (the framework crate), not in `crates/chirp-frontend/` (the application crate). No variant was added to `EventKind` by this PR — the PR completed the hydrate.rs implementation to cover variants the enum already contained. The correctness gap being closed: before this PR, re-rendering an SSR-adopted element that used any event kind other than `Click` or `Input` would fail to detach the old listener, accumulating handlers with each render cycle.

For the sync risk: `static_event_kinds()` at line 494 of `hydrate.rs` returns `[EventKind; 47]`, a hand-written array literal. The companion functions `event_name()` (line 562) and `stash_key()` (line 633) use exhaustive match arms with no wildcard — a new variant added to `EventKind` without a corresponding arm causes a compile error in both. `static_event_kinds()` has no equivalent guard: its return type `[EventKind; 47]` continues to typecheck at 47 entries even after a 48th variant is added to the enum. The doc comment at lines 491–493 says "Must be kept in sync" but enforces nothing. There is no test or assertion verifying that the array covers all static variants. The same gap exists at `crates/ferric/src/dom.rs`, line 309, with an identical advisory comment. The runtime failure mode if a 48th variant is added to `EventKind`, its match arms in `event_name()` and `stash_key()` are updated (forced by the compiler), but it is omitted from `static_event_kinds()`: the detachment pass in `set_events()` skips that variant's stash slot on each re-render, the old listener is never removed before the new one is added, and listeners accumulate silently. No panic; no compile error from `static_event_kinds()`.

## Verdict

The `hydrate.rs` EventKind expansion corrects a pre-existing implementation gap in the framework — the enum was already full-sized in `vdom.rs` before this PR — bringing `hydrate.rs` into alignment with the existing `dom.rs` pattern. It is framework-level work bundled with an application feature PR. `static_event_kinds()` is a hand-written list that must track `EventKind` manually; the companion matches (`event_name`, `stash_key`) are compiler-enforced but `static_event_kinds()` is not, leaving a latent silent-failure path if a new variant is ever added.

## Finding

### Finding: Framework fix bundled in application feature PR

- **Location**: `crates/ferric/src/hydrate.rs`, lines 417–490 at commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- **Principle at stake**: PR scope discipline — framework changes belong in framework PRs
- **Why it matters**: The hydrate.rs changes correct a pre-existing framework bug (the detachment pass covered 2 of 47 event kinds) and are located in `crates/ferric/`, not `crates/chirp-frontend/`. Mixing framework-layer correctness work with an application feature PR couples a framework fix to a feature review, complicates bisect and rollback, and obscures the blast radius if either part needs reverting independently. The vdom.rs doc comment explicitly states feature spokes should not add EventKind variants, reinforcing the expectation that changes to ferric have their own PRs.
- **Severity**: non-blocking
- **Satisfying condition**: Accept the bundled change as-is (the fix is correct and matches the dom.rs pattern), or extract the ferric changes into a preceding framework PR and rebase this PR onto it. No code correction is required if the team accepts the scope.

### Finding: `static_event_kinds()` lacks a compile-time completeness guard

- **Location**: `crates/ferric/src/hydrate.rs`, line 494 at commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- **Principle at stake**: Compile-time enforcement over advisory comments for enum-to-table mappings
- **Why it matters**: `event_name()` and `stash_key()` enforce their own completeness through exhaustive match arms — the compiler rejects the build if either is out of sync with `EventKind`. `static_event_kinds()` enforces only that it returns exactly 47 elements, not that those 47 elements cover all static variants. A developer forced by the compiler to update `event_name()` and `stash_key()` has no compiler signal to also update `static_event_kinds()`. If the omission is not caught in review, re-renders of elements carrying that event kind silently accumulate listeners with each render cycle. The same gap exists at `crates/ferric/src/dom.rs`, line 309. The vdom.rs "frozen" declaration reduces the probability but is not enforced.
- **Severity**: non-blocking
- **Satisfying condition**: Add a guard that makes omission from `static_event_kinds()` a build or test failure. Three options: (a) a `#[cfg(test)]` function that iterates `static_event_kinds()` and calls `event_name()` and `stash_key()` on each element, then asserts a known count — this will fail to compile when a new variant is added to `event_name` / `stash_key` but absent from the array; (b) replace the hand-written array with a derived iterator using `strum::IntoEnumIterator` filtered to skip `Custom`; (c) add a `strum::EnumCount` derive and assert `static_event_kinds().len() + 1 == EventKind::COUNT` (the +1 accounts for `Custom`). The fix must be applied to both `hydrate.rs` and `dom.rs`.
