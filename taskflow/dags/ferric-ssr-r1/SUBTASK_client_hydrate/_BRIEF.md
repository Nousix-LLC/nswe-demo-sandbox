# _BRIEF.md — ferric-ssr-r1-client-hydrate

## Objective

Implement `hydrate` fully in `crates/ferric/src/hydrate.rs`, addressing Issue #224 (BAR-004)
(client hydration without re-render) and the mismatch detection and recovery portion of Issue
#226 (BAR-006). The implementation runs on branch `work/ferric-ssr-r1-client`, branched from
`work/ferric-ssr-r1` after the skeleton task has committed.

## Inputs

- **Branch**: `work/ferric-ssr-r1` after the skeleton task has committed (use as base for
  `work/ferric-ssr-r1-client`).
- **Owned file to implement**: `crates/ferric/src/hydrate.rs` (the skeleton left a stub here).
- **Contract** (read-only): `contracts/ferric_ssr_contract.rs` — the `hydrate` signature,
  `TEXT_OPEN_MARKER` / `TEXT_CLOSE_MARKER` constants, and the full constraint list (zero
  structural mutations, comment-node handling, event wiring, mismatch detection format).
- **Source references** (read-only):
  - `crates/ferric/src/dom.rs` — DOM walk, event wiring via Reflect, keyed-patch cycle,
    child-index path addressing via `resolve` / `child_nodes().item(i)`.
  - `crates/ferric/src/vdom.rs` — `VNode`, `VElement`, `diff`, `Patch`.
  - `crates/ferric/src/signal.rs` — `create_effect`, `ReactiveScope`.
  - `design/ferric/ssr-hydration.md` — hydration walk spec, mismatch detection spec.

## Declared Output

Commits on branch `work/ferric-ssr-r1-client` with:

1. `crates/ferric/src/hydrate.rs` fully implemented — `hydrate` replaces the `todo!()` stub
   with the complete adopt-pass, event-wiring, reactive-effect, mismatch-detection, and
   mismatch-recovery logic.

2. Headless `wasm-bindgen-test` tests covering at minimum:
   - **Zero structural mutations** (the gating bar): a server-rendered DOM is passed to
     `hydrate`; a MutationObserver or node-identity comparison confirms no create/replace/
     move/remove occurs under the hydration root during the adopt pass.
   - **Event handler wiring**: a Click or Input handler is wired during hydration and fires
     correctly on the adopted element.
   - **Mismatch detection**: a deliberately mismatched DOM (a `<span>` where a `<div>` is
     expected, or wrong text content) triggers the dev-build diagnostic at the correct path.
   - **Mismatch recovery**: the mismatched subtree is client-rendered; surrounding adopted
     nodes retain their original identity.

## Success Criteria

- Zero structural DOM mutations during the adopt pass: no DOM node is created, replaced,
  moved, or removed under the hydration root. This is the gating observable bar.
- Event handlers wired onto adopted elements function correctly.
- Reactive effects established; subsequent signal updates patch via the existing keyed-patch
  path in `dom.rs` (or an equivalent local path — see dom.rs for the pattern).
- Mismatch detection fires for tag/text divergence at any path in the tree.
- `#[cfg(debug_assertions)]` diagnostic names the child-index path, the expected tag/text,
  and what was found — following the format in `contracts/ferric_ssr_contract.rs`.
- Mismatched subtree is client-rendered; the rest of the document is not disturbed.
- `TEXT_OPEN_MARKER` and `TEXT_CLOSE_MARKER` comment nodes are skipped (not counted as VNode
  children) during the child-index walk.
- Requirements REQ-SSR-004, REQ-SSR-005, REQ-SSR-009 are addressed.
- The frozen files (`src/dom.rs`, `src/signal.rs`, `src/vdom.rs`, `src/component.rs`) are
  unmodified.

## Constraints

- **Owns**: `crates/ferric/src/hydrate.rs` (and sub-files if split into `src/hydrate/`
  subdirectory). Do not modify any other file.
- **Do not modify `src/dom.rs`**: event-wiring patterns are read from `dom.rs` and replicated
  or adapted within `src/hydrate.rs`. If a refactor would help, note it in a code comment
  for a follow-up — do not restructure `dom.rs` in this task.
- **Marker constants**: use `TEXT_OPEN_MARKER` and `TEXT_CLOSE_MARKER` exactly as declared
  in the contract. Import from `crate::ssr` or redeclare as `pub(crate) const` matching the
  same literal bytes — never use independent inline strings.
- **Frozen files** must not be touched.
- **BAR-005 (#225)** is out of scope; do not implement state deserialization or async
  resource resume.
- Branch: `work/ferric-ssr-r1-client`. Do not force-push to `main`.
- Commit attribution: end commit messages with `Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>`.
