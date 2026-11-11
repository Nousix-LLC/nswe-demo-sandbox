## Findings

### 1. HTML injection / escaping gap

- **severity**: clean
- **concern**: security
- **location**: `crates/ferric/src/form.rs` (new), `crates/ferric/src/dom.rs` (modified)
- **description**: `Bind<T>::on_input_event_handler()` writes `HtmlInputElement::value()` into a `Signal<String>` via `raw.set(input_el.value())`. When that signal triggers a reactive re-render, the value enters the DOM only through the library's established rendering path. Inspection of the full `dom.rs` at head `838239e` shows every DOM write uses safe browser APIs: text content is set via `document.create_text_node(content)` (dom.rs:106) and `node.set_text_content(Some(value))` (dom.rs:143); attributes are set via `element.set_attribute(name, value)` (dom.rs:112, 147). `set_inner_html` is entirely absent from `dom.rs` and from the entire PR diff. None of these APIs parse their argument as HTML markup, so no injection gap exists. The PR does not introduce a new escaping hole; it stays within the library's pre-existing safe rendering contract.

---

### 2. Secrets and infrastructure data

- **severity**: clean
- **concern**: security
- **location**: `crates/ferric/src/async_resource.rs`, `crates/ferric/src/form.rs`, `crates/ferric/src/dom.rs`, `crates/ferric/src/vdom.rs`
- **description**: A full-text scan of all added lines in the diff found no hardcoded IP addresses (no `100.`, `192.168.`, `10.`, `172.` patterns), no hostnames, no passwords, secrets, API keys, tokens, or SSH key material. WASM tests in `async_resource.rs` and `form.rs` are configured via `wasm_bindgen_test_configure!(run_in_browser)` with no embedded server addresses. The new `Cargo.toml` entries add only the `wasm-bindgen-futures = "0.4"` dependency and new `web-sys` feature flags (`KeyboardEvent`, `FocusEvent`, `PointerEvent`, etc.); no registry mirrors or private registries introduced.

---

### 3. Unsafe code

- **severity**: clean
- **concern**: security
- **location**: `crates/ferric/src/async_resource.rs`, `crates/ferric/src/form.rs`, `crates/ferric/src/dom.rs`, `crates/ferric/src/vdom.rs`
- **description**: A scan of all added lines (`^+` prefix) across the entire PR diff for the `unsafe` keyword returned zero results. No unsafe blocks were introduced by any of the three remediation commits (`9fedad9`, `9557f0c`, `838239e`). The `Closure::wrap`, `unchecked_ref()`, and `JsCast::dyn_into()` calls in `dom.rs` and `form.rs` are safe (non-`unsafe`) WASM interop APIs from `wasm-bindgen` and `web-sys`; they do not require unsafe blocks.

---

### 4. Event handler downcast — remote panic surface

- **severity**: clean
- **concern**: security
- **location**: `crates/ferric/src/form.rs:1587` (production `on_input_event_handler`), `crates/ferric/src/dom.rs:272–275` (production `set_events`)
- **description**: The `WithEvent` variant passes `&event as &dyn std::any::Any` to the handler closure, where `event: web_sys::Event` — the concrete type is established by the `wasm-bindgen` Closure type bound. The only new production downcast is in `on_input_event_handler`: `any.downcast_ref::<Event>()` uses an `if let Some(event) = ...` guard (form.rs:1587), which silently returns unit on a bad cast — no panic. The WASM test at dom.rs (`event_carrying_handler_can_call_prevent_default`) uses `.expect()` on the downcast, but that is test-only code where a type mismatch is a test bug, not a remotely triggerable condition. No crafted event can reach a production panic path via `downcast_ref`.

---

### 5. `closure.forget()` scope

- **severity**: clean
- **concern**: security
- **location**: `crates/ferric/src/dom.rs:287` (pre-existing production), `crates/ferric/src/form.rs:1883` (new test)
- **description**: The only `closure.forget()` call **added by this PR** is in `form.rs`'s `wasm_tests` module (line 1883, inside `#[cfg(all(test, target_arch = "wasm32"))]`), which is test-only. The comment at line 1881–1882 correctly explains the rationale: test scope, element removed at end of test. The pre-existing `closure.forget()` in production `dom.rs:287` was not introduced by this PR (it appears as unchanged context in the diff). It is the correct WASM event listener pattern: the closure is stash-rooted on the DOM element via `Reflect::set(target, stash_key, closure.as_ref())` immediately before the `forget()`, making it GC-reachable, and the existing detachment pass removes it on re-bind. This is not a new security concern.

---

## What was examined

| Area | Files / diff sections examined | Outcome |
|------|-------------------------------|---------|
| HTML injection / rendering path | `crates/ferric/src/form.rs` new file (full WASM handler), `crates/ferric/src/dom.rs` at head `838239e` (full rendering path: `create_node`, `apply_patches`) | No `set_inner_html`; all DOM writes use `create_text_node`, `set_text_content`, `set_attribute` — clean |
| Secrets / infrastructure data | Full PR diff, all added lines (`^+`) — `async_resource.rs`, `vdom.rs`, `dom.rs`, `form.rs`, `Cargo.toml` | No IP addresses, credentials, tokens, hostnames — clean |
| Unsafe code | Full PR diff, all added lines for `unsafe` keyword | Zero results — clean |
| Downcast panic surface | `form.rs:1587` (production handler), `dom.rs:272–275` (production `set_events`), `dom.rs` WASM tests | `if let` guard in production; `.expect()` only in test code — clean |
| `closure.forget()` scope | Full PR diff for `forget()` calls, context read for each | New `forget()` is test-only; pre-existing production `forget()` is a stash-rooted WASM pattern, not new to this PR — clean |
| Acceptance criteria coverage | REQ-ASYNC-042 (the only req with security-touching surface: `on_input_event_handler`) | Rendering path confirmed safe; criterion's security implication is clean |

**Verdict for security spoke**: No blockers. All four security questions answered with evidence. No HTML injection gap introduced, no secrets committed, no unsafe code, no remote panic surface.
