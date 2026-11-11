# COMPLETE — SUBTASK_view (ferric-router: link helper + wasm example + README)

**Status:** COMPLETE
**Branch:** `work/ferric-router`  **Commit:** `0d2dfa8` — "Implement ferric-router view layer: link helper, example app, README"
**Clone:** `<subtree_root>/checkout/` (shared serial-pipeline clone; `main` untouched; no attribution trailers)

## Outputs produced (owned files, per `contracts/_MANIFEST.yaml`)
- `checkout/crates/ferric-router/src/link.rs` — final `link` implementation + additive `Link` builder + native unit tests.
- `checkout/crates/ferric-router/examples/app.rs` — the 3-route wasm example (replaces the scaffold stub).
- `checkout/crates/ferric-router/README.md` — example walk-through + architecture note + wasm build + `preventDefault` constraint.

## Design decisions

### `link` — the `preventDefault` composition constraint (verified, hub §3 / contract note)
`ferric`'s click handler is `Fn()` with **no** `web_sys::Event` argument, so `preventDefault()` is
unreachable through the public API. Rather than edit `ferric` (out of scope), `link` **sidesteps
default navigation by construction**: it emits a **non-anchor element** — a focusable, link-styled
`<span role="link" tabindex="0" class="ferric-router-link" data-to="…">` with **no `href`** for the
browser to follow — carrying a `ferric` `EventKind::Click` handler that moves an owned `String` copy
of `to` and calls `router::navigate(&to)`. No event object is needed and no full-page navigation can
occur. The choice and its rationale are documented in module + item rustdoc.
- **Contract match:** the frozen `pub fn link(to: &str, label: &str) -> VNode` signature is matched
  exactly (compiler-checked; `use ferric_router::prelude::*` resolves `link`).
- **Additive extension (allowed by the contract):** a small `Link` builder (`Link::new(to,label)
  .class(..).build()`) plus a public `LINK_CLASS` const — the frozen `link` is exactly
  `Link::new(to,label).build()`. Nothing frozen was removed or changed.
- **Tests (native, no browser):** assert the element is a `<span>` (NOT `<a>`), shows its label as a
  single text child, records `data-to`/`role`/`tabindex`/`class`, binds exactly one Click handler,
  and that the builder's custom class does not alter the click wiring.

### `examples/app.rs` — end-to-end exercise of the whole router
A 3-route SPA (`/`, `/about`, `/user/:id` + fallback) built with the **real** `Router`
(`route`/`fallback`/`mount_history`), composing the matcher's `/user/:id` param extraction. A single
root component renders a persistent nav bar (three `link`s + a programmatic `navigate("/user/7")`
button) above `router.outlet().render()`; reading the outlet inside the root render subscribes the
mount effect to the reactive current-path signal, so every navigation re-renders the routed view in
place. Root acquisition (`#app` else `<body>`) mirrors the `ferric` counter example. The needed
`web-sys` DOM features (`Document`/`Element`/`HtmlElement`) arrive transitively from `ferric` via
Cargo feature unification, so no `Cargo.toml` edit was required (and `Cargo.toml` is not mine to edit).

### `README.md`
Mirrors the sibling `ferric` crate's house style: an ASCII architecture diagram (matcher → router +
reactive current-path signal → History API → outlet → `link`), the example walk-through, native +
wasm build instructions, browser-run notes, the testing posture, and a dedicated section on the
`<Link>`/`preventDefault` constraint.

## Verification — all contract identities green (run in `checkout/`)
| Identity | Command | Result |
|---|---|---|
| `workspace_builds` | `cargo build --workspace` | exit 0 |
| `native_tests_pass` | `cargo test -p ferric-router` | exit 0 — 28 unit + 5 doctests pass |
| `router_wasm_builds` | `cargo build -p ferric-router --target wasm32-unknown-unknown` | exit 0 |
| **`example_wasm_builds`** | `cargo build -p ferric-router --example app --target wasm32-unknown-unknown` | **exit 0** |
| `fmt_clean` | `cargo fmt --all --check` | exit 0 |
| `clippy_clean` | `cargo clippy --all-targets -- -D warnings` | exit 0 (example compiles on host too) |
| `public_api_surface` | `link` resolves via `ferric_router::prelude::*` | satisfied (crate builds) |

**Example wasm build result:** `cargo build -p ferric-router --example app --target
wasm32-unknown-unknown` → `Finished` / **exit 0**.

## Success criteria (from `_BRIEF.md`) — all met
- [x] `link` matches the frozen signature (compiler-checked); rustdoc explains the non-anchor/`preventDefault` choice.
- [x] `examples/app.rs` uses `Router` + outlet + `link` + `navigate`; the wasm example build exits 0.
- [x] `README.md` present with example + architecture note + wasm build instructions.
- [x] `cargo fmt` clean; no clippy warnings in owned files; all public items documented.
- [x] Committed on `work/ferric-router`; `main` untouched; no attribution trailers.

## Notes for the synthesis gate (`SUBTASK_synthesis`)
- No `#[wasm_bindgen_test]` was added by this task (`wasm_bindgen_test_optional`): the navigation
  spoke already provides the wasm browser test; `link` is pure view-construction fully covered by
  native tests, and the example provides the end-to-end wasm build evidence. Not a FAIL per the
  contract (native tests + wasm builds are the gate).
- `preventDefault` unavailability is handled by design (non-anchor element), documented in code and
  README — a known composition constraint for the gate to note, not a defect.
- `ferric` was not modified; the event-arg limitation is recorded as a possible future additive
  enhancement to `ferric`.
