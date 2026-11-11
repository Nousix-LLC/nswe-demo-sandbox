# ferric-foundation — Cargo workspace + `ferric` framework core (issue #4, EPIC #1)

Subtree hub (narrative + shared context). The tool-consumable structure lives in `contracts/`.

## Project Context

**Status**: Active

### Objective
Establish the Cargo **virtual workspace** at the root of `Nousix-LLC/nswe-demo` and implement the
**core of `ferric`** — a small client-side web-application framework in Rust compiled to
WebAssembly. This is the foundation the rest of the engagement builds on; prioritize a clean,
well-tested, documented, extensible core over breadth. Delivered as a PR into `main` from branch
`work/ferric-foundation`, closing #4.

### Scope
**In scope:** virtual workspace + `crates/ferric` member crate; reactive signals (`Signal`/`Memo`,
effects, batching, sound subscriber cleanup); a component model producing a view tree; DOM
rendering via `wasm-bindgen` + `web-sys` with a minimal keyed diff/patch and click+input events;
wasm build for `wasm32-unknown-unknown`; a counter example; native unit tests + wasm-bindgen-test
where the toolchain allows; quality gates (fmt/clippy/rustdoc/README); PR into `main`.

**Out of scope:** the Twitter-style SPA itself; the later crates (`ferric-router`, `ferric-http`,
`chirp-types`, `chirp-server`, `chirp-frontend`) — only lay the workspace out so they slot in.

### Success criteria (the gate asserts these — see `contracts/_MANIFEST.yaml` identities)
- [ ] Virtual workspace builds; `crates/ferric` builds for `wasm32-unknown-unknown`.
- [ ] Reactive core: `Signal`/`Memo` get/set/update, subscriber registration, change
      notification, derived/computed values, batched updates, **no stale-subscriber leaks**.
- [ ] Component model producing a view tree; `mount(root, component)` renders into a DOM element.
- [ ] DOM rendering via wasm-bindgen/web-sys; minimal **keyed** diff/patch on signal change;
      click + input event binding.
- [ ] Counter example builds to wasm.
- [ ] Native `cargo test` passes without a browser; `wasm-bindgen-test` if the toolchain installs
      cleanly (else documented in SYNTHESIS.md; native tests remain the gate).
- [ ] `cargo fmt --check` clean; `cargo clippy --all-targets -- -D warnings` clean; rustdoc on all
      public items; `crates/ferric/README.md` with the counter example + an architecture note.
- [ ] PR opened into `main` from `work/ferric-foundation`; body ends with `Closes #4`.

## Input / working state
- **Repo**: `Nousix-LLC/nswe-demo` (GitHub; `gh` authenticated; `git`, `cargo`, `rustup` present).
- **Shared working tree**: a single git clone at `checkout/` **under this subtree root**
  (`/home/user/nousix-runtime/nswe-demo/taskflow/dags/ferric-foundation/checkout/`), created by
  `SUBTASK_scaffold`. Every downstream child operates on THIS clone via its absolute path. Do NOT
  reuse `~/nousix-runtime/nswe-demo/repo` (another process may touch it). Base branch `main`; all
  work commits to branch `work/ferric-foundation`. **Never** commit to or force-push `main`.
- **Contract** (read-only): `contracts/ferric_api.rs` (frozen public API) + `contracts/_MANIFEST.yaml`
  (ownership + identities). Descendants IMPORT/MATCH these; they do not redefine them.

## Chosen decomposition — layered serial spine + synthesis gate (rationale)
This is ONE crate split into layers that share a public surface. Three candidate cuts were
considered; the layered serial spine was chosen:
- **Why not a parallel feature fan-out**: the layers carry a real compile-and-test dependency —
  the view layer's tests exercise the *real* `Signal`, and the DOM runtime renders *real* `VNode`s
  and subscribes to *real* signals. Mocking `Signal`/`VNode` to parallelize would be L3 mock depth
  (a sibling re-implementing a sibling) — forbidden. So the signal→view and view→dom seams are
  **SERIALIZED** (each consumer reads its predecessor's real output), not frozen-and-mocked.
- **What is frozen anyway**: the crate's **public API surface** (`contracts/ferric_api.rs`,
  kind `rust_trait`), because it is the shared `lib.rs`/prelude mount surface *and* the stable
  surface the later engagement crates depend on. Mock depth **L0**.
- **Walking skeleton**: `SUBTASK_scaffold` owns the shared composition root — the two `Cargo.toml`s,
  `src/lib.rs` (module decls + prelude re-exports), and compiling `todo!()` stubs for each module —
  so `cargo build` (native + wasm) is green before any layer is implemented. Each spoke then fills
  in the body of exactly its own module file (disjoint ownership; no concurrent writers).

### Dependency graph
```
SUBTASK_scaffold ─> SUBTASK_reactive_core ─> SUBTASK_view_and_diff ─> SUBTASK_dom_runtime ─┐
       └───────────────────────────────────────────────────────────────────────────────> SUBTASK_synthesis
```

### Task Summary (authoritative DAG)
| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_scaffold` | none | Clone repo into `checkout/`; branch `work/ferric-foundation`; virtual-workspace root `Cargo.toml`; `crates/ferric/Cargo.toml` (lean deps); `src/lib.rs` (module decls + prelude); compiling `todo!()` stubs for every module; commit. Walking skeleton — proves `cargo build` (native + wasm) green. | the prepared clone + crate skeleton (`COMPLETE.md`) |
| `SUBTASK_reactive_core` | `SUBTASK_scaffold` | Implement `src/signal.rs`: `Signal`/`Memo`, effects, batching, sound subscriber cleanup; native unit tests incl. a stale-subscriber-leak test. | `src/signal.rs` (`COMPLETE.md`) |
| `SUBTASK_view_and_diff` | `SUBTASK_reactive_core` | Implement `src/vdom.rs` + `src/component.rs`: view tree, `Component` trait + function components, keyed `diff`→`Patch`; native unit tests for the diff. | `src/vdom.rs`, `src/component.rs` (`COMPLETE.md`) |
| `SUBTASK_dom_runtime` | `SUBTASK_view_and_diff` | Implement `src/dom.rs`: `mount`, web-sys patch application, click+input binding; `examples/counter.rs`; `crates/ferric/README.md`; wasm-bindgen-test if available. | `src/dom.rs`, `examples/counter.rs`, `README.md` (`COMPLETE.md`) |
| `SUBTASK_synthesis` | `SUBTASK_scaffold`, `SUBTASK_reactive_core`, `SUBTASK_view_and_diff`, `SUBTASK_dom_runtime` | **Verification gate**: run the manifest identities (build/wasm/test/fmt/clippy/api/example); push the branch; open the PR into `main`; author `SYNTHESIS.md` with verdicts + diff manifest + PR URL + PASS/FAIL. | `SYNTHESIS.md` + PR (fold record) |

## Contract
**Contract location**: `contracts/` (read-only for every descendant).
**Contract kind**: `rust_trait` (the `ferric` public API surface).
- **Structural declarations**: `contracts/ferric_api.rs` — frozen public items per module.
- **Ownership**: `contracts/_MANIFEST.yaml` — every owned path → exactly one child.
- **Identities**: the 8 build/test/quality/soundness invariants in the manifest; the synthesis
  gate enumerates and runs each.
- **Derived artifacts / mocks**: none (L0 — serialized pipeline reads real outputs).
- **Amendment**: additive-only. A child that finds the frozen API inadequate requests a plan
  amendment; it MUST NOT edit `contracts/` or deviate silently.

## Subtree Methodology Posture
- **Dominant task type**: *Writing new code* in **Rust** (a reactive Rust/WASM framework). The DOM
  layer is Rust FFI over `web-sys`; the synthesis child is a verification gate + git/PR delivery.
- **Primary bundles** children should assume in scope without re-justifying: **`rust`** (primary),
  **`core`**, **`code-quality`**, **`testing`**. The synthesis child additionally loads
  **`synthesis`** and **`operations`** (GitWorkflow PR lifecycle).
- **Cross-cutting bindings over the whole subtree**: the frozen `contracts/ferric_api.rs` surface
  binds every layer; `Rust_Error_Handling`, `Rust_Ownership_Borrowing`, and the Core coding
  standards bind every leaf. Public items carry rustdoc (quality identity). These are inherited
  constraints, not per-leaf choices.
- **Suggestion, not prescription**: each child is the final judge of what it loads — fewer if a
  suggested file is clearly inapplicable, more if its own reading reveals additional surface (e.g.
  `architecture` for a design note on the component/render boundary; `Rust_Unsafe_FFI` for the
  web-sys layer).

## Subtree-Wide Constraints (decided upstream — conform, do not re-litigate)
- Framework crate is **`ferric`** at `crates/ferric`. Lay the workspace out so
  `crates/ferric-router`, `crates/ferric-http`, `crates/chirp-types`, `crates/chirp-server`,
  `crates/chirp-frontend` slot in cleanly later.
- Rust **edition 2021+**, **stable** toolchain. Framework deps stay lean: `wasm-bindgen`,
  `web-sys`, `js-sys` — avoid heavy frameworks (we are building one).
- Public API must be ergonomic enough that a Twitter-style SPA (timeline, compose, profile,
  follow/like) can later be built on it. Build only the foundation now.
- Work in the `checkout/` clone only; branch `work/ferric-foundation`; **never** touch `main`.
  No commit-attribution trailers.
- `rustup target add wasm32-unknown-unknown` is performed within this DAG (scaffold does it).
