# _GLOBAL.md — Hub: `ferric-router` (issue #5, EPIC #1)

## Project Context

**Status**: Active (decomposed subtree; parent `ferric-router` DAG node is SUSPENDED pending this subtree)

### Objective
Deliver **`crates/ferric-router`** — a client-side router for the landed `ferric` WASM framework —
as a PR into `Nousix-LLC/nswe-demo:main`, `Closes #5`. The router provides: a declarative route
table with path params (`/user/:id`), a path→route matcher with param extraction, History API
navigation (`pushState`/`popstate` via `web-sys`), a programmatic `navigate(path)` API, a `<Link>`-style
navigation helper, and a reactive router-outlet that re-renders on navigation — composing with
`ferric`'s signals/component model (NOT re-implementing reactivity).

### Scope
**In scope:** new workspace member crate `crates/ferric-router` (path-dep on `crates/ferric`); route
matcher + param extraction; `Router`, `navigate`, `current_path`, outlet, `link`; a 2–3 route wasm
example; native unit tests + a `wasm-bindgen-test` where the toolchain installs; fmt/clippy/rustdoc/README;
branch `work/ferric-router`; PR into `main`.

**Out of scope:** any application built *on* the router (the Twitter-style SPA comes later); forking or
re-implementing `ferric`'s reactivity/DOM layer; touching `main` directly; commit-attribution trailers.

### Success Criteria (inherited from the work-item brief; the synthesis gate asserts these)
- [ ] `crates/ferric-router` is a workspace member, path-dep on `crates/ferric`, builds in the virtual workspace.
- [ ] Route table + matcher resolves patterns with params; param extraction correct (`/user/:id` → `id`).
- [ ] History API navigation works (`pushState`/`popstate`); `navigate(path)` + `<Link>` helper present.
- [ ] Reactive outlet renders the matched route's view and re-renders on navigation (via `ferric` signals).
- [ ] `cargo build -p ferric-router --target wasm32-unknown-unknown` succeeds; a 2–3 route example builds to wasm.
- [ ] Native `cargo test` covers matcher + param extraction; a `wasm-bindgen-test` if the runner installs (else documented).
- [ ] `cargo fmt --check` clean; `cargo clippy --all-targets -- -D warnings` clean; rustdoc on all public items; `README.md` present.
- [ ] PR opened into `main` with `Closes #5`; `SYNTHESIS.md` carries a PASS/FAIL verdict + the PR URL.

---

## Decomposition decision & chosen cut (rationale)

The work-item fired multiple decomposition triggers (distinct components: pure matcher / web-sys
History integration / reactive view; enumerated concerns; output > 400 lines; serial pipeline of
distinct responsibilities). `decompose_evaluation = NeedsDecompose`.

**Cut chosen: a contract-first SERIAL pipeline**, mirroring the proven sibling `ferric-foundation`
decomposition (scaffold → layers → synthesis over a frozen public-API contract). The router's modules
form a genuine dependency chain — matcher (pure) → router/history (stateful, depends on matcher) →
view (outlet + link, depends on router). Per the contract-scoping stability heuristic: the **public
API surface is stable/forced** (we design it; later crates — `ferric-router`'s example and the future
`chirp-frontend` — depend on it) → **FREEZE it** as the one contract (`contracts/ferric_router_api.rs`,
kind `rust_trait`). The **internal layer seams are discovery-dependent and strictly serial** →
**SERIALIZE them** as task dependencies at **mock depth L0** (each layer reads its predecessor's REAL
output in the shared clone; no mocks).

Candidate cuts considered and rejected:
- *By layer with parallel spokes + mocked internal seams*: rejected — the internal matcher↔router↔view
  seams are discovery-dependent, so freezing them would be guessing; mock overhead + drift risk for no
  real parallelism gain (the chain is serial anyway).
- *One atomic task*: rejected by the kernel evaluation (triggers fired).

Ownership is **disjoint per source file** (hard gate satisfied); and because the pipeline is serial,
each file additionally has a single writer at the time it runs — no concurrent writers to the shared clone.

---

## Shared working tree
A single git clone at **`<subtree_root>/checkout/`** (created by `SUBTASK_scaffold`), on branch
**`work/ferric-router`** off `main`. `<subtree_root>` = this directory
(`/home/user/nousix-runtime/nswe-demo/taskflow/dags/ferric-router/`). Every child operates on that
clone via its absolute path; no child reuses any other process's clone. The pipeline is serial, so
each child commits its own owned files in turn.

---

## Contract (the frozen seam)
**Location:** `contracts/` (read-only for every descendant). **Kind:** `rust_trait` (an in-process Rust
public-API surface; enforcement tool = the compiler + rustdoc). **Mock depth:** **L0** — serialized
pipeline, every consumer reads its predecessor's REAL output.

- `contracts/ferric_router_api.rs` — the FROZEN public surface (module layout, public items + signatures,
  prelude re-exports). Implementers MATCH these signatures; additions are additive-only (request a plan
  amendment to change a frozen signature). Private/internal representation is owner latitude.
- `contracts/_MANIFEST.yaml` — ownership (every owned path → exactly one child) + the identities the
  synthesis gate asserts.

See `contracts/_MANIFEST.yaml` for the full ownership map and identity list.

---

## Task Structure

```
ferric-router/ (this hub)
├── contracts/ { _MANIFEST.yaml, ferric_router_api.rs }        READ-ONLY
├── checkout/                                                   shared clone (scaffold creates)
├── SUBTASK_scaffold/_BRIEF.md     walking skeleton + clone + workspace member + stubs
├── SUBTASK_matcher/_BRIEF.md      src/matcher.rs (pure route matcher + param extraction + tests)
├── SUBTASK_navigation/_BRIEF.md   src/router.rs (Router, route table, navigate, History API, outlet)
├── SUBTASK_view/_BRIEF.md         src/link.rs + examples/app.rs + README.md
└── SUBTASK_synthesis/_BRIEF.md    verification GATE + push + PR + SYNTHESIS.md (fold record)
```

### Task Summary (authoritative DAG)

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_scaffold` | none | Clone repo, branch `work/ferric-router`, add `crates/ferric-router` member (Cargo.toml, lib.rs + frozen prelude, `todo!()` stubs for matcher/router/link, a stub example), make `cargo build --workspace` green | crate skeleton in `checkout/`, commit |
| `SUBTASK_matcher` | `SUBTASK_scaffold` | Implement `src/matcher.rs`: `Params`, `RoutePattern::new`/`match_path`, param extraction; native unit tests | `checkout/crates/ferric-router/src/matcher.rs`, commit |
| `SUBTASK_navigation` | `SUBTASK_matcher` | Implement `src/router.rs`: `Router` (route table + reactive current-path), `route`/`fallback`/`mount_history`/`outlet`, `navigate`, `current_path`; History API pushState/popstate via web-sys | `checkout/crates/ferric-router/src/router.rs`, commit |
| `SUBTASK_view` | `SUBTASK_navigation` | Implement `src/link.rs` (`link` helper); 2–3 route wasm `examples/app.rs`; `README.md` (example + architecture note) | `src/link.rs`, `examples/app.rs`, `README.md`, commit |
| `SUBTASK_synthesis` | `SUBTASK_scaffold`, `SUBTASK_matcher`, `SUBTASK_navigation`, `SUBTASK_view` | Verification GATE: workspace+wasm build, native tests, fmt, clippy, contract identities, wiring/dedup/review; push branch; open PR into `main` (`Closes #5`); author `SYNTHESIS.md` | `SYNTHESIS.md` (at this subtree root) |

### Dependency Graph
```
SUBTASK_scaffold ── SUBTASK_matcher ── SUBTASK_navigation ── SUBTASK_view ──┐
      └──────────────────┴────────────────────┴────────────────────────────┴── SUBTASK_synthesis
```

---

## Subtree Methodology Posture
- **Dominant task type**: "Writing Rust code" (plus a Rust wasm/web-sys integration layer and a
  synthesis verification gate). Bundle IDs selected by the overseer and carried into every child:
  **`rust`, `core`, `code-quality`, `testing`** (the synthesis child additionally gets **`synthesis`**,
  and `code-review`/`code-quality` for the gate review).
- **Primary bundles the subtree draws on**: `rust` (ownership/traits/error-handling/type-system/testing),
  `core` (coding standards, error handling, commit practices), `code-quality` (SOLID/Clean Code for the
  public API), `testing` (unit strategy for the matcher + navigation).
- **Cross-cutting bindings (inherited by every leaf)**: compose with `ferric` — do NOT re-implement
  reactivity/DOM; lean deps only (`wasm-bindgen`, `web-sys`, `js-sys`); edition 2021 / stable toolchain;
  workspace lints (`missing_docs=warn`, `unsafe_code=warn`, `clippy::all=warn`) → rustdoc every public item.
- Suggestion-not-prescription: each child loads what its brief names plus whatever its own reading reveals.

## Subtree-Wide Constraints (decided upstream — conform, do not re-litigate)
1. Crate name **`ferric-router`** at `crates/ferric-router`; path-dep on `crates/ferric`; slots into the
   existing virtual workspace (`members = ["crates/*"]`).
2. Compose with the landed `ferric` public surface: `create_signal`/`create_effect`/`Signal`,
   `VNode`/`VElement`/`text`/`EventKind`, `Component` (any `Fn() -> VNode`), `mount`. Read
   `crates/ferric` + its README first.
3. **ferric event constraint (verified):** `ferric`'s click handler is `Fn()` with NO event argument —
   `preventDefault()` is NOT reachable through the public API. The `<Link>` helper MUST therefore use a
   non-`<a>`-navigating element (or an `<a>` whose href the browser will not follow) + a click handler
   calling `navigate()`. This is a known composition constraint, not a defect; the synthesis gate notes it.
4. Work ONLY in `checkout/` on branch `work/ferric-router`; NEVER commit to or force-push `main`; no
   commit-attribution trailers. Push + open the PR only in the synthesis gate.
5. `engine_compute` is not used; builds/tests run via `cargo` in the clone.
