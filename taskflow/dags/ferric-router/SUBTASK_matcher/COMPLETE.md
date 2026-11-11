# COMPLETE — SUBTASK_matcher (ferric-router route matcher)

**Task**: Implement the pure, browser-free route matcher in `src/matcher.rs` to the frozen contract,
with native unit tests. **Status**: COMPLETED. **Decompose evaluation**: Atomic (one responsibility —
implement one pure module + its tests).

## What was done
Replaced the scaffold's `todo!()` stubs in
`checkout/crates/ferric-router/src/matcher.rs` with the real implementation, matching the frozen
public surface in `../contracts/ferric_router_api.rs` exactly (compiler-checked).

### Design (internal representation is owner latitude; signatures are frozen)
- **`Params`** — ordered `Vec<(String, String)>` of name→value pairs, in pattern order. Linear-scan
  `get` (route patterns carry a handful of params; no hashing/alloc per lookup is the simplest and
  fastest choice). Frozen methods `get(&self, &str) -> Option<&str>`, `is_empty(&self) -> bool`,
  `len(&self) -> usize`. Additive-only extras (allowed by the contract): `iter()` plus derives
  (`Debug, Clone, Default, PartialEq, Eq`) to aid tests/consumers. No frozen item removed or changed.
- **`RoutePattern`** — `Vec<Segment>` where `Segment` is a private enum `Static(String) | Param(String)`.
  `new(&str)` compiles the pattern; `match_path(&self, &str) -> Option<Params>` matches exactly over
  segments, binding each `:name` segment.
- **Matching model** — both pattern and path are split on `/` with **empty segments discarded**. This
  single rule yields, for free: the root `/` ≡ zero segments; trailing slash insignificant; doubled
  slashes collapsed; and exact segment-count matching (no match on extra/missing segments). Param
  values are taken verbatim (no percent-decoding — documented).

### Why this shape
- Filtering empty segments is the one mechanism that makes patterns and paths normalize identically,
  so root / trailing-slash / `//` behavior falls out of one code path rather than special cases.
- `&str`-returning `get` borrows from `&self` (elision Rule 3) — borrow-clean, no lifetime noise,
  per the ownership methodology (prefer borrowing on read APIs).

## Verification (all run inside `checkout/` on branch `work/ferric-router`)
- `cargo test -p ferric-router` → **17 unit tests pass**, 0 failed; module **doctest passes**.
  Cases: exact static match + mismatch; param extraction; extra/missing segment non-match; root
  match + root-vs-nonroot; empty-string ≡ root; multi-param; mixed static+param (incl. wrong static
  prefix); trailing slash; doubled slashes; unknown param name → `None`; empty-param non-match;
  verbatim (undecoded) values; `iter()` order; single-segment exactness.
- Contract identity **`matcher_param_extraction`** holds: `/user/:id` vs `/user/42` → `id="42"`;
  `/user/42/extra` and `/user` → `None`; `/` matches `/`. (Encoded as dedicated tests.)
- `cargo fmt -p ferric-router -- --check` → **clean**.
- `cargo clippy -p ferric-router --all-targets -- -D warnings` → **clean** (no warnings).
- **No `web-sys`/browser dependency** introduced — the module is pure `std`, no imports.
- `cargo build -p ferric-router` (workspace member) remains green; router/link stubs untouched.

## Success criteria — all met
- [x] `Params` + `RoutePattern` match frozen signatures exactly (compiler-checked); rustdoc on all public items.
- [x] Identity `matcher_param_extraction` holds.
- [x] `cargo test -p ferric-router` passes for the matcher; `cargo fmt` clean; no clippy warnings in this module.
- [x] No `web-sys`/browser dependency introduced by this module.

## Ownership & boundaries honored
- Edited only my owned file `checkout/crates/ferric-router/src/matcher.rs`; `contracts/` untouched
  (read-only); did not implement router/link.
- Committed on `work/ferric-router` only; `main` never touched; no commit-attribution trailers.

## Outputs
- `checkout/crates/ferric-router/src/matcher.rs` — final implementation + `#[cfg(test)] mod tests`.
- Commit `443c5f2` on `work/ferric-router` ("Implement ferric-router route matcher (pure logic + tests)"),
  one file changed.

## For the downstream (`SUBTASK_navigation`) and the synthesis gate
- The real `Params`/`RoutePattern` are now available (mock depth L0 — no mock). A route's view builder
  is `Fn(&Params) -> VNode`; `Params::get(name)` returns the captured `&str`.
- Note for the gate: param values are **not** percent-decoded here (verbatim segment capture). If the
  navigation/view layers want decoded values, that is a layer concern, not a matcher defect.
