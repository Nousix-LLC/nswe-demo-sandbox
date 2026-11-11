# _BRIEF.md — ferric-ssr-r2 (SSR + Hydration remediation DAG)

**Goal**: Complete the SSR + hydration goal by implementing `crates/ferric/src/hydrate.rs` (BAR-004 / #224) and mismatch detection/recovery (the remaining BAR-006 / #226 portion), then open a PR to main closing #223, #224, and #226.

**Repo**: `Nousix-LLC/nswe-demo`  
**Branch**: `work/ferric-ssr-r1` (continue on the existing branch; no rebase needed — main SHA `945fade38abd6b053268501f3801734756f02502` unchanged)  
**Remediation attempt**: 1 of 2

---

## Context from prior DAG (ferric-ssr-r1)

Prior synthesis: `taskflow/dags/ferric-ssr-r1/SYNTHESIS.md` — read it for the full record of what was done and what is missing.

**What is done on `work/ferric-ssr-r1`** (do not redo; do not modify):

- **BAR-003 / #223**: FULLY MET — `render_to_string` implemented in `crates/ferric/src/ssr.rs`; 56 unit tests pass; TEXT_OPEN_MARKER / TEXT_CLOSE_MARKER correct; HTML escaping complete; ReactiveScope isolation verified.
- **Axum integration (REQ-SSR-011, part of BAR-006 / #226)**: DONE — PR #227 was merged into the goal branch; `crates/chirp-server/src/ssr.rs` fully wired.
- Build state: `cargo test -p ferric` passes (56+7 tests), `cargo build -p chirp-server` exits 0, all compile checks pass.

**What is missing** (this DAG's work):

- **BAR-004 / #224**: `crates/ferric/src/hydrate.rs` remains a `todo!()` stub. The client-hydrate spoke never ran in ferric-ssr-r1.
- **Mismatch detection/recovery (REQ-SSR-009, the remaining BAR-006 / #226 concern)**: not yet implemented; depends on the hydration implementation above.
- **PR to main**: not created (blocked on the above); must be opened as part of this DAG.

---

## Acceptance criteria

### #223 / BAR-003 (already MET — must remain correct and passing)

`render_to_string` in `crates/ferric/src/ssr.rs` is complete and must stay correct. No modification required or permitted.

### #224 / BAR-004 — full hydration implementation

`crates/ferric/src/hydrate.rs` must be fully implemented per the contract at `taskflow/dags/ferric-ssr-r1/contracts/ferric_ssr_contract.rs`:

- **Function signature** (exact):
  ```rust
  #[cfg(target_arch = "wasm32")]
  pub fn hydrate<F>(root: web_sys::Element, f: F)
  where
      F: Fn() -> VNode + 'static;
  ```
  Note: the original contract had `FnOnce`; the corrected signature is `Fn` (the effect loop needs to call it on subsequent renders). Use `Fn`.

- **cfg gating**: The entire implementation must be `#[cfg(target_arch = "wasm32")]` so `cargo check --lib -p ferric` on a native host continues to pass with zero errors.

- **REQ-SSR-004 — Zero structural mutations adopt pass**: The DOM walk MUST NOT create, replace, move, or remove any DOM node under `root`. The walk maps VNode children to existing DOM nodes by index without touching the DOM structure.

- **REQ-SSR-005 — Event handler wiring**: Click and Input event handlers present in the VNode tree must be wired onto the adopted DOM elements using the same Reflect-based approach as `crates/ferric/src/dom.rs` uses. No new event-wiring mechanism; reuse the existing one.

- **Comment sentinel handling (from contract)**: During the adopt walk, `Comment` nodes whose `data == TEXT_OPEN_MARKER` or `data == TEXT_CLOSE_MARKER` are recognized as text-boundary sentinels. They are NOT counted as VNode children when advancing the child index. VNode::Text at a given index maps to the DOM Text node between its pair of sentinel Comment nodes.

- **REQ-SSR-009 — Mismatch detection (debug builds only)**:
  ```rust
  #[cfg(debug_assertions)]
  web_sys::console::warn_1(&format!(
      "ferric hydration mismatch at [{}]: expected {:?}, found {:?}",
      path_string, expected, found
  ).into());
  ```
  Trigger: when the DOM node at a child-index path has a different tag or text content than the VNode at that path.

- **REQ-SSR-009 — Mismatch recovery**: The mismatched subtree is recovered by client-rendering it (as `dom::mount` would on that node alone). Successfully adopted sibling and ancestor nodes MUST NOT be disturbed.

- **Reactive effects**: After adoption, a reactive effect is established with the first adopted tree as the "previous" VNode for the diff/patch cycle. Subsequent signal updates invoke the existing keyed-patch path exactly as `dom::mount` does. The hydration entry point is functionally equivalent to `dom::mount` for all subsequent renders; only the first pass is an adopt walk.

- **TEXT_OPEN_MARKER / TEXT_CLOSE_MARKER usage**: The hydration implementation MUST import and use these constants from `crate::ssr` (not redefine them). The literal string `<!--$t-->` must appear in `hydrate.rs` indirectly through the constant, satisfying the `marker-format-agreement` identity assertion.

### #226 / BAR-006 (complete the remaining portion)

Mismatch detection/recovery (REQ-SSR-009) is now part of the BAR-004 implementation above. When BAR-004 is fully implemented, BAR-006 is fully covered (axum done + mismatch done).

---

## Identity assertions — all must pass

| Assertion | Command | Required result |
|---|---|---|
| `native-compile` | `cargo check --lib -p ferric` | Exit 0 — hydrate.rs is `cfg(wasm32)` only; must not break native compile |
| `wasm-compile` | `cargo check --target wasm32-unknown-unknown -p ferric` | Exit 0 |
| `native-tests-pass` | `cargo test -p ferric` | All existing tests pass + any new hydration tests pass (0 failures) |
| `chirp-server-compile` | `cargo build -p chirp-server` | Exit 0 |
| `frozen-prelude-unchanged` | `git diff HEAD -- crates/ferric/src/lib.rs crates/ferric/src/signal.rs crates/ferric/src/dom.rs crates/ferric/src/router.rs` | Empty diff — no frozen file modified |
| `marker-format-agreement` | presence of `crate::ssr::TEXT_OPEN_MARKER` (or the literal `<!--$t-->`) in `hydrate.rs` | Present — the hydration implementation uses the imported constant |
| `issues-closed` | PR body content | Includes `Closes #223`, `Closes #224`, `Closes #226`; includes the BAR-005 exclusion sentence below |

**BAR-005 exclusion sentence** (required verbatim in PR body):
> BAR-005 / #225 (state carry + async resource resume) is a follow-up issue dependent on #130 and is NOT part of this goal.

---

## Non-goals / scope constraints

- **BAR-005 / #225**: out of scope; blocked on #130. Include the exclusion sentence in the PR body but do not implement.
- **Frozen files**: do not modify `crates/ferric/src/lib.rs`, `crates/ferric/src/signal.rs`, `crates/ferric/src/dom.rs` (public API), or `crates/ferric/src/router.rs` (public API).
- **No force-push**: do not force-push any branch.
- **PR #227** (`work/ferric-ssr-r1-axum` → `work/ferric-ssr-r1`): already merged into the goal branch. It may be closed/deleted as superseded but must not be undone.
- Do not merge the PR. The overseer does that after the review gate.

---

## Inputs

- Prior DAG synthesis: `taskflow/dags/ferric-ssr-r1/SYNTHESIS.md`
- Contract (marker constants + signatures): `taskflow/dags/ferric-ssr-r1/contracts/ferric_ssr_contract.rs`
- Existing implementation on branch `work/ferric-ssr-r1` in `Nousix-LLC/nswe-demo`
- Existing `crates/ferric/src/dom.rs` for the Reflect-based event wiring approach (read it; replicate the pattern)
- Existing `crates/ferric/src/ssr.rs` for the TEXT_OPEN_MARKER / TEXT_CLOSE_MARKER constants

---

## Declared output

- Commits on `work/ferric-ssr-r1` implementing `hydrate.rs` per the contract
- A PR from `work/ferric-ssr-r1` to `main` in `Nousix-LLC/nswe-demo` closing #223, #224, #226 (not #225), with the BAR-005 exclusion sentence in the body
- Root `SYNTHESIS.md` at `taskflow/dags/ferric-ssr-r2/SYNTHESIS.md` accounting for each acceptance criterion (MET / NOT MET and why) and each identity assertion result

---

## What to evaluate / concerns

1. **Correctness of the DOM adopt pass**: the hydration walk correctly maps VNode children to DOM children, skips TEXT_OPEN_MARKER and TEXT_CLOSE_MARKER comment sentinels (they are not VNode children), and wires Click/Input events without any structural DOM mutation. The walk terminates correctly on deep/nested trees.

2. **Mismatch detection and recovery**: debug-build warnings are emitted with the correct format when a tag/text mismatch is detected; recovery renders the mismatched subtree client-side without disturbing successfully adopted neighbors.

3. **cfg gating**: `hydrate.rs` is fully gated on `cfg(target_arch = "wasm32")` so native `cargo check` passes without errors or dead-code warnings from the stub.

4. **Marker constant import**: `hydrate.rs` imports `TEXT_OPEN_MARKER` and `TEXT_CLOSE_MARKER` from `crate::ssr` (or re-exports) rather than redefining them. The `marker-format-agreement` assertion passes.

5. **Reactive effects**: after the adopt walk, signal updates drive the diff/patch cycle exactly as `dom::mount` does. The hydration entry point is functionally equivalent to mount for all subsequent renders.

6. **All identity assertions pass**: compile checks, test suite (all existing + new), frozen-file diff, marker agreement, issues-closed syntax.

7. **PR quality**: title, body (outcome and what changed, issues closed, BAR-005 exclusion sentence), no host paths or taskflow internals in the PR text.
