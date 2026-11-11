# _BRIEF.md — active-link

**Goal slug**: `active-link`
**Kind**: code (atomic)
**Repo**: Nousix-LLC/nswe-demo
**Branch**: `work/ferric-router-r1`
**Workspace**: `taskflow/dags/ferric-router-r1/SUBTASK_active_link/`

---

## Objective

Extend `Link::build()` in `crates/ferric-router/src/link.rs` to emit `aria-current="page"` on
the navigation element when the link's target matches the current path. The frozen
`link(to, label)` signature and the `Link` builder API are unchanged; this is a purely additive
behavioral extension.

This closes the active-route awareness requirement (REQ-RT-007) for issue #147.

---

## Inputs

- Working branch: `work/ferric-router-r1` (after `navigate-replace` spoke)
- Source file to extend: `crates/ferric-router/src/link.rs`
- Existing frozen `Link::build()` implementation in that file
- `crate::router::current_path()` already exists and is importable
- Contract: `taskflow/dags/ferric-router-r1/contracts/ferric_router_r1_api.md`
  (identity: `active_link_awareness`)

---

## Declared output

Commits on `work/ferric-router-r1`:

- `crates/ferric-router/src/link.rs` extended:
  - `use crate::router::{current_path, navigate};` — add `current_path` to the existing
    import
  - `Link::build()` updated: before constructing the element, call `current_path()` to get
    the current path; if `self.to == current_path()`, add `aria-current="page"` as an
    attribute to the emitted element; otherwise, the element is structurally identical to
    the frozen surface (no `aria-current`, no class change)
  - The frozen `link(to, label) -> VNode` function and `Link` builder signatures are
    unchanged

- Native tests in `src/link.rs` (in the existing `tests` module):
  - `active_link_emits_aria_current_when_path_matches`: call `navigate("/active")` then
    build `Link::new("/active", "Active").build()`; assert element has `aria-current="page"`
  - `inactive_link_has_no_aria_current`: call `navigate("/other")` then build
    `Link::new("/active", "Active").build()`; assert element has NO `aria-current` attribute
  - `aria_current_toggles_on_navigation`: build a link once at "/about", verify no
    aria-current; call `navigate("/about")`, build again, verify aria-current present

---

## Success criteria

1. `cargo test -p ferric-router` passes all tests (new + pre-existing frozen tests,
   including all frozen link tests which must still pass unchanged).
2. `cargo build -p ferric-router --target wasm32-unknown-unknown` succeeds.
3. `cargo clippy -p ferric-router -- -D warnings` clean.
4. `cargo fmt --check -p ferric-router` clean.
5. Contract identity `active_link_awareness` is met.
6. All frozen link tests pass without modification.

---

## Constraints

- Only touch `crates/ferric-router/src/link.rs`. No other source files.
- The frozen `link(to, label)` function signature is unchanged.
- When the link's `to` does NOT match `current_path()`, the emitted element MUST be
  structurally identical to the frozen surface — no `aria-current`, no extra attributes,
  no class changes.
- Do not change the `LINK_CLASS` constant or the `class()` builder behavior.
- Do not create a PR; leave that to the synthesis gate.
- Commit messages must NOT include the host server address, SSH key path, user name, or
  local paths.
