# COMPLETE — SUBTASK_scaffold (walking skeleton)

**Task**: Scaffold the shared working tree + a compiling `ferric` crate skeleton.
**Status**: COMPLETED (Atomic).
**Branch**: `work/ferric-foundation` (cut from `main`); **not pushed** — the synthesis child pushes and opens the PR.
**Scaffold commit**: `eb1d192` ("Scaffold Cargo workspace + ferric crate skeleton (walking skeleton)"), parent `51cfc70` (`main` HEAD, untouched).

## What was scaffolded

Working tree: a fresh `gh repo clone Nousix-LLC/nswe-demo` at the subtree root's `checkout/`
(`/home/user/nousix-runtime/nswe-demo/taskflow/dags/ferric-foundation/checkout/`), on a new branch
`work/ferric-foundation`. `rustup target add wasm32-unknown-unknown` was performed (host toolchain:
`cargo 1.97.0`, stable).

Files authored (per `contracts/_MANIFEST.yaml` → `SUBTASK_scaffold` ownership):

| Path (under `checkout/`) | Role |
|---|---|
| `Cargo.toml` | Virtual workspace root — `resolver = "2"`, `members = ["crates/*"]`, `[workspace.package]` (version/edition 2021/rust-version 1.82/repository), lean `[workspace.dependencies]` (`wasm-bindgen`, `js-sys`, `web-sys`, `wasm-bindgen-test`), shared `[workspace.lints]`, size-tuned `[profile.release]`. Laid out so `crates/ferric-router`, `crates/ferric-http`, `crates/chirp-types`, `crates/chirp-server`, `crates/chirp-frontend` slot in later. |
| `crates/ferric/Cargo.toml` | `ferric` member crate; inherits workspace package/lints; `web-sys` feature set the DOM layer needs (Window/Document/Element/HtmlElement/HtmlInputElement/Node/Text/Comment/CharacterData/Event/EventTarget/InputEvent/MouseEvent/console/NodeList/DomTokenList/NamedNodeMap/Attr); `wasm-bindgen-test` dev-dependency. |
| `crates/ferric/src/lib.rs` | Module decls (`signal`, `vdom`, `component`, `dom`) + `pub mod prelude` re-exporting the frozen surface (`Signal, create_signal, Memo, create_memo, create_effect, batch, VNode, VElement, EventKind, Component, mount`). |
| `crates/ferric/src/signal.rs` | STUB — `Signal`/`Memo` (Copy handles), `create_signal`, `create_memo`, `create_effect`, `batch`; `todo!()` bodies. Owned impl → `SUBTASK_reactive_core`. |
| `crates/ferric/src/vdom.rs` | STUB — `VNode`, `VElement`, `Key`, `EventKind`, `EventHandler`, `Patch`, `diff`; `todo!()` body. Owned impl → `SUBTASK_view_and_diff`. |
| `crates/ferric/src/component.rs` | STUB — `Component` trait + the frozen `Fn() -> VNode` blanket impl (complete as frozen). Owned impl → `SUBTASK_view_and_diff`. |
| `crates/ferric/src/dom.rs` | STUB — `mount`; `todo!()` body. Owned impl → `SUBTASK_dom_runtime`. |
| `.gitignore` | `/target` (build-artifact hygiene for the shared tree). |

`Cargo.lock` is committed (workspace-level reproducibility). Stub public signatures were transcribed
verbatim from the read-only `contracts/ferric_api.rs`, including its doc comments (the subtree enforces
rustdoc on public items via `missing_docs = "warn"`); `contracts/` was not modified.

## Build / identity results (run inside `checkout/`)

| Manifest identity | Command | Result |
|---|---|---|
| `workspace_builds` | `cargo build --workspace` | ✅ pass |
| `ferric_wasm_builds` | `cargo build -p ferric --target wasm32-unknown-unknown` | ✅ pass |
| `fmt_clean` | `cargo fmt --all --check` | ✅ pass |
| `clippy_clean` | `cargo clippy --all-targets -- -D warnings` | ✅ pass (zero warnings) |
| `native_tests_pass` | `cargo test --workspace` | ✅ pass (0 tests yet; crate-doc example marked `ignore`) |
| `public_api_surface` | prelude re-exports resolve during compilation | ✅ importable (frozen set present) |

The remaining manifest identities belong downstream: `no_stale_subscriber_leak` →
`SUBTASK_reactive_core`; `counter_example_wasm_builds` → `SUBTASK_dom_runtime`. The scaffold proves the
walking skeleton compiles native + wasm before any layer logic exists.

## Flags for downstream owners (no deviation taken; recorded, not acted on)

1. **`mount` root parameter.** `contracts/ferric_api.rs` carries a commented-out
   `root: web_sys::Element` on `mount`, and `_GLOBAL.md` success criteria say `mount(root, component)`.
   The *active* frozen signature omits `root`, so the stub transcribes it exactly as
   `mount(component: impl Component + 'static)` ("match these signatures; do not redefine them").
   `SUBTASK_dom_runtime` will likely need the `root` parameter — the `web-sys` `Element` feature is
   already enabled; adding it is an owner-latitude refinement / additive contract amendment, not a
   scaffold change.
2. **`EventHandler` payload.** The frozen alias is `Rc<dyn Fn()>` with a `/* web_sys::Event */` hint;
   the concrete wrapper is owner-designed. `SUBTASK_view_and_diff` may refine it (e.g.
   `Rc<dyn Fn(web_sys::Event)>`) — the `Event`/`InputEvent`/`MouseEvent` features are enabled.
3. **Lints.** `unsafe_code = "warn"` (not `forbid`) so the web-sys layer can `#[allow(unsafe_code)]`
   locally if it genuinely needs `unsafe`; `clippy::all` + `missing_docs` are workspace-wide and are
   run under `-D warnings`, so every new public item must carry rustdoc and stay clippy-clean.

## For the synthesis gate
`main` is untouched (HEAD `51cfc70`); `work/ferric-foundation` is `main` + exactly one scaffold commit
(`eb1d192`), local-only. Push + PR (`Closes #4`) are `SUBTASK_synthesis`'s responsibility.
