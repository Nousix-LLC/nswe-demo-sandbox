# _GLOBAL.md — ferric-router-r1 subtree hub (pass 2: CI fix)

**Subtree root**: `ferric-router-r1`  
**Observation seam**: `taskflow/dags/ferric-router-r1/SYNTHESIS.md`  
**Branch**: `work/ferric-router-r1` → `Nousix-LLC/nswe-demo`  
**Epic**: #131 — EPIC: Ferric 1.0 — Client-side Router (closes #131, #146, #147)

---

## Context

The original four sequential spokes (`navigate-replace`, `active-link`, `nested-routes`,
`synthesis-gate`) all completed. PR #192 (`work/ferric-router-r1` → `main`) was created by the
synthesis gate. All five API contract identities are met.

**One CI check is still failing**: `clippy` (GitHub Actions `cargo clippy --workspace
--all-targets --locked -- -D warnings`) reports:

```
error: unused import: `VNode`
  --> crates/ferric-router/src/router.rs:436:46
   |
   | use ferric::vdom::{VElement, VNode};
   |                              ^^^^
```

The synthesis gate ran `cargo clippy -p ferric-router -- -D warnings` (single-crate, no
`--all-targets`), which does not lint test code. The CI command includes `--all-targets` and
therefore catches the unused import inside a test closure.

---

## Pass-2 decomposition

Two sequential tasks close the remaining gap:

| Task ID | Description | Depends on |
|---|---|---|
| `clippy-fix` | Remove unused `VNode` import from `router.rs:436`; run full workspace clippy; commit + push | — |
| `synthesis-verify` | Verify all 6 CI checks pass on the updated head; write final SYNTHESIS.md; fold root | `clippy-fix` |

---

## Contract identities (unchanged from pass 1)

All five identities defined in `contracts/ferric_router_r1_api.md` remain binding:

| Identity | Status |
|---|---|
| `frozen_surface_preserved` | ✅ Met (all frozen #5 items present, signatures unchanged) |
| `navigate_replace_added` | ✅ Met (`navigate_replace` exported from prelude) |
| `active_link_awareness` | ✅ Met (`Link::build()` emits `aria-current="page"` on match) |
| `nested_routes_added` | ✅ Met (`Router::nest`, `RoutePattern::match_prefix` present) |
| `prelude_union` | ✅ Met (prelude exports all frozen items plus `navigate_replace`) |

**Additional CI constraint**: the final SYNTHESIS.md must report all 6 CI checks passing on
the PR head commit that includes the clippy fix.

---

## Binding constraints for all children

- **Repo**: `Nousix-LLC/nswe-demo`; scope `crates/ferric-router` only.
- **Branch**: `work/ferric-router-r1`. Never force-push.
- **Additive only**: do not remove or redefine any frozen #5 prelude item.
- **Do not touch**: `design/` directory (read-only design inputs).
- **Do not merge the PR**: the overseer's review gate merges.
- **Security**: never commit secrets, tokens, or credentials. Never put the host's server
  address, SSH key path, user name, or local paths into GitHub issues, PRs, or commits.
- **CI gate**: all six jobs (`fmt`, `clippy`, `test`, `wasm`, `doc`, `image`/`SKIPPED`) must
  PASS on the PR head.
