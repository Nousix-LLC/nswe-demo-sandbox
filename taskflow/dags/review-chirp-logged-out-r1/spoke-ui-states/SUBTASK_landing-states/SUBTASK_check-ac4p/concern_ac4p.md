## Concern: AC-4 (partial) — header_nav() in every rendered state

**Status**: clean

---

## Checked

**File**: `crates/chirp-frontend/src/landing.rs`  
**Pinned commit**: `decb6196c2c1e6ed421d393a642f0c844cc333ba`  
**Scope**: `view_tree` function (lines 238–267) — the pure, unit-testable dispatch function called by `landing_view` (line 162). `header_nav()` function definition (lines 270–277).

**Criterion applied**: Is `header_nav()` present in EVERY rendered state of `landing_view`, including loading, error, empty/populated, and any other branch?

**Method**: Read the full `view_tree` function body, enumerated each branch arm, confirmed the placement of the `header_nav()` call relative to the branch dispatch logic, and read the `header_nav()` definition to confirm it is not itself conditional.

---

## Branch Inventory

The dispatch logic in `view_tree` (lines 238–267) uses a two-level if/else to compute a `body` node
(lines 243–260), then unconditionally wraps it with `header_nav()` in the outer `VElement::new("section")` at line 264.

The key structural observation: `header_nav()` is called **outside and after** all branching — it is a sibling of `body` in the outer container, not an element inside any branch arm. This means no branch can accidentally omit it; the guarantee is structural.

| Branch | Condition | `header_nav()` present? | Line reference |
|--------|-----------|------------------------|----------------|
| Loading state (initial, no error yet) | `!model.loaded && model.error == None` → `loading_view()` | Yes | Line 264 (outer wrapper) |
| Initial error state (error before first successful load) | `!model.loaded && model.error == Some(err)` → error div | Yes | Line 264 (outer wrapper) |
| Empty state (loaded, zero chirps) | `model.loaded && model.chirps.is_empty()` → `empty_view()` | Yes | Line 264 (outer wrapper) |
| Populated state (loaded, chirps present) | `model.loaded && !model.chirps.is_empty()` → chirp-list div | Yes | Line 264 (outer wrapper) |

**Note on `footer()` sub-branches**: The populated state renders `footer(model, on_load_more)` (line 258), which itself dispatches on `model.error`, `model.loading_more`, `model.has_more`, and end-of-list (lines 352–375). These sub-branches affect only the footer area inside `body`; they do not affect `header_nav()`, which is outside `body` entirely.

**Note on `empty_view()` CTA links**: `empty_view()` (lines 287–306) contains its own sign-up/sign-in links at line 301–303. These are AC-2 content (the empty-state explanation and CTAs), not AC-4 navigation. `header_nav()` and those links are distinct elements appearing side-by-side in the empty-state render.

---

## Findings

None.

---

## Clean Notes

**Structural guarantee at line 264**: The author chose a "hoist before branch" pattern — compute `body` via the if/else (lines 243–260), then build the outer `section` unconditionally with `.child(header_nav()).child(body)` (lines 262–266). This is the right architectural choice for a component that must appear in every state: it makes omission impossible without touching the wrapper. The pattern is sound and matches the documented intent (function comment at line 139: "always shows sign-up and sign-in navigation (AC-4)").

**`header_nav()` definition (lines 270–277)**: The function is non-conditional — it always returns a `div.chirp-landing-nav` containing both the `/signup` ("Create account") and `/signin` ("Sign in") links. No internal branching.

**Test at line 509** (`every_state_includes_header_nav_links`): This test exercises the loading state (fresh `LandingModel::new()` has `loaded: false`, no error) and asserts both `chirp-landing-nav` class presence and nav link text. Because the guarantee is structural (outer wrapper, not per-branch), one state is sufficient to prove coverage. The test checks the right thing — the class attribute of the div produced by `header_nav()` — and the assertion is behavioral, not vacuous.
