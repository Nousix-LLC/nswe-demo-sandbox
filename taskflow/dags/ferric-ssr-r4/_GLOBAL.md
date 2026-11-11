# ferric-ssr-r4 — Code Remediation: SSR + Hydration Blockers B1 and B2

## Project Context

**Status**: Active  
**Branch**: `work/ferric-ssr-r1`  
**PR**: [#228](https://github.com/Nousix-LLC/nswe-demo/pull/228)  
**Repo local path**: `/home/user/nswe-demo`

### Objective

Remediate the two blocking findings from review-ferric-ssr-r1 on PR #228 so the PR can land:

- **B1 — REQ-HYD-003**: `hydrate()` never called from the WASM entry point. `crates/chirp-frontend/src/app.rs::start()` calls `ferric::dom::mount()` instead of `ferric::hydrate()`.
- **B2 — REQ-SSR-006 / Area E**: `hydrate.rs` has no `wasm-bindgen-test` coverage (3 tests required by issues #224 and #226).

### Scope

**In Scope:**
- Modify `crates/chirp-frontend/src/app.rs::start()` to call `ferric::hydrate(root, app)` when `#app` has server-rendered children; fall back to `ferric::dom::mount()` otherwise.
- Correct the `crates/chirp-server/src/ssr.rs` docstring (around line 71, item 4) that describes WASM hydration wiring.
- Add a `#[cfg(test)]` module to `crates/ferric/src/hydrate.rs` (or `crates/ferric/tests/hydrate_wasm.rs`) with 3 `#[wasm_bindgen_test]` tests: adopt-walk, event-wiring, mismatch-detection.
- Update the PR identity table to add `wasm-tests-pass: ✅`.

**Out of Scope:**
- The 14 non-blocker issues (#229–#242) tracked in the PR review.
- Any other functional changes.

### Success Criteria

- [ ] `ferric::hydrate(root, app)` is called from the WASM entry point when `#app` has server-rendered children.
- [ ] `crates/chirp-server/src/ssr.rs` docstring accurately reflects the conditional hydration call.
- [ ] Three `wasm-bindgen-test` tests (adopt-walk, event-wiring, mismatch-detection) pass under `wasm-pack test --headless`.
- [ ] All 6 CI checks pass: fmt, clippy, doc, build, native-tests, wasm-tests.
- [ ] PR #228 updated with `wasm-tests-pass: ✅` in identity table.

---

## Technical Context

### Key Files

| File | Role |
|---|---|
| `/home/user/nswe-demo/crates/chirp-frontend/src/app.rs` | WASM entry point — currently calls `mount()` at line 150 |
| `/home/user/nswe-demo/crates/chirp-server/src/ssr.rs` | Axum SSR handler; docstring at ~line 71 incorrectly asserts hydrate is called |
| `/home/user/nswe-demo/crates/ferric/src/hydrate.rs` | Full 466-line hydration implementation; no tests |
| `/home/user/nswe-demo/crates/ferric/Cargo.toml` | `wasm-bindgen-test` already in dev-dependencies |

### How to Run CI Locally (via SSH to build server)

```bash
SSH_CMD='ssh -i ~/.ssh/nousix_server_ed25519 -o IdentitiesOnly=yes -o BatchMode=yes mattm@100.90.75.93'

# Format check
$SSH_CMD 'bash -lc "cd /home/user/nswe-demo && git checkout work/ferric-ssr-r1 && cargo fmt --all -- --check"'

# Clippy
$SSH_CMD 'bash -lc "cd /home/user/nswe-demo && cargo clippy --all-targets --all-features -- -D warnings"'

# Native tests (ferric)
$SSH_CMD 'bash -lc "cd /home/user/nswe-demo && cargo test -p ferric"'

# WASM tests (ferric)
$SSH_CMD 'bash -lc "cd /home/user/nswe-demo && wasm-pack test crates/ferric --headless --chrome"'

# Full build
$SSH_CMD 'bash -lc "cd /home/user/nswe-demo && cargo build --workspace"'
```

### hydrate() vs mount() signature

Both take `(root: web_sys::Element, f: F)` where `F: Fn() -> VNode + 'static`.  
`hydrate` is `#[cfg(target_arch = "wasm32")]` only (and re-exported from `ferric::hydrate`).  
Detection: check `root.has_child_nodes()` or `root.child_element_count() > 0`.

---

## Task Structure

```
_GLOBAL.md (this document)
├── SUBTASK_b1_hydrate_fix/   — Fix app.rs entry point + correct ssr.rs docstring
├── SUBTASK_b2_wasm_tests/    — Add 3 wasm_bindgen_test tests to hydrate.rs
└── SUBTASK_synthesis_report/ — Verify CI, update PR identity table, produce SYNTHESIS.md
```

### Task Summary

| Task id | Depends on | Description | Output |
|---|---|---|---|
| `SUBTASK_b1_hydrate_fix` | none | Fix app.rs to call ferric::hydrate() + correct ssr.rs docstring | `b1_resolution.md` |
| `SUBTASK_b2_wasm_tests` | `SUBTASK_b1_hydrate_fix` | Add 3 wasm_bindgen_test tests to hydrate.rs | `b2_resolution.md` |
| `SUBTASK_synthesis_report` | `SUBTASK_b2_wasm_tests` | Verify CI + update PR identity table + write SYNTHESIS.md | `SYNTHESIS.md` |

### Dependency Graph

```
SUBTASK_b1_hydrate_fix → SUBTASK_b2_wasm_tests → SUBTASK_synthesis_report
```

---

## Contract

**Contract location**: N/A (thin seam — B1 and B2 are independent file changes on the same branch; they compose by sequential git commits, not by shared types or interfaces)

**Ownership:**

| Artifact | Owning subtask |
|---|---|
| Changes to `crates/chirp-frontend/src/app.rs` | `SUBTASK_b1_hydrate_fix` |
| Changes to `crates/chirp-server/src/ssr.rs` | `SUBTASK_b1_hydrate_fix` |
| Test code added to `crates/ferric/src/hydrate.rs` or `crates/ferric/tests/` | `SUBTASK_b2_wasm_tests` |
| `SYNTHESIS.md` at `taskflow/dags/ferric-ssr-r4/SYNTHESIS.md` | `SUBTASK_synthesis_report` |

**Identity:**
- Both B1 and B2 commits MUST be on branch `work/ferric-ssr-r1`.
- All 6 CI checks MUST pass after both fixes are committed.

---

## Output Specifications

| Deliverable | Format | Location |
|---|---|---|
| B1 resolution record | Markdown | `SUBTASK_b1_hydrate_fix/b1_resolution.md` |
| B2 resolution record | Markdown | `SUBTASK_b2_wasm_tests/b2_resolution.md` |
| Final synthesis | Markdown | `ferric-ssr-r4/SYNTHESIS.md` |
