# Task: ferric-router route matcher (pure logic)

## Task Specification
**Slug**: SUBTASK_matcher
**Task Kind**: standard
**Status**: Pending

### Objective
Implement the pure, browser-free route matcher in `src/matcher.rs`: compile path patterns, match a
concrete path, and extract named parameters — fully covered by native unit tests.

### Context
Part of the `ferric-router` work-item (see `../_GLOBAL.md`, `../contracts/`). Second task in the serial
pipeline: the scaffold's compiling skeleton exists; you replace the body of `src/matcher.rs` only. The
navigation layer (next) will call your real `RoutePattern`/`Params` — no mock.

**Dependencies**: `SUBTASK_scaffold`. **Dependents**: `SUBTASK_navigation` (and downstream).

## Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Hub | `../_GLOBAL.md` | context + constraints |
| Frozen contract | `../contracts/ferric_router_api.rs` (matcher module), `../contracts/_MANIFEST.yaml` (identity `matcher_param_extraction`) | the exact `Params` / `RoutePattern` signatures you MATCH and the param-extraction identity you MUST satisfy |
| Shared clone | `<subtree_root>/checkout/` on branch `work/ferric-router` | the tree you edit + commit in (`<subtree_root>` = `/home/user/nousix-runtime/nswe-demo/taskflow/dags/ferric-router/`) |

## What to do (approach — your design, not a script)
Implement `src/matcher.rs` to the frozen contract: `Params` (`get`, `is_empty`, `len`) and
`RoutePattern` (`new`, `match_path`). Support static segments, `:name` params, and the root `/`;
matching is exact over segments. Internal representation (how segments/params are stored) is yours.
Write native `#[test]`s covering: exact match, param extraction (`/user/:id` + `/user/42` → `id=42`),
non-match on extra/missing segments, the root, multi-param patterns, and edge cases you judge relevant
(trailing slash, empty param). Keep it `no_std`-of-the-browser: **no `web-sys`/DOM** here. Commit on
`work/ferric-router` when `cargo test -p ferric-router` passes for your module.

## Outputs (you own)
- `checkout/crates/ferric-router/src/matcher.rs` (final implementation + its `#[cfg(test)] mod tests`)
- a commit; `COMPLETE.md` recording the design + `cargo test` result for the matcher.

## Success Criteria
- [ ] `Params` + `RoutePattern` match the frozen signatures exactly (compiler-checked); rustdoc on all public items.
- [ ] Identity `matcher_param_extraction` holds (see `_MANIFEST.yaml`): `/user/:id` vs `/user/42` → `id="42"`; `/user/42/extra` and `/user` → `None`; `/` matches `/`.
- [ ] `cargo test -p ferric-router` passes for the matcher tests; `cargo fmt` clean; no clippy warnings in this module.
- [ ] No `web-sys`/browser dependency introduced by this module.

## Constraints
- `../contracts/` is READ-ONLY; MATCH signatures, do not alter the contract or other modules' files.
- Compose only within your owned file; do not implement router/link.
- NEVER touch `main`; no commit-attribution trailers.

## Suggested Methodology Files (parent's flags — you are the final judge)
Task type: **Writing new code** (pure algorithm) → primary **Core**/**Rust**, supporting **Testing**.
- `rust` — `rust/Rust_Ownership_Borrowing_Methodology.md` (borrow-clean matcher, `&str` lifetimes for `get`),
  `rust/Rust_Type_System_Methodology.md` (modeling segments/params), `rust/Rust_Testing_Methodology.md`.
- `core` — `core/BestPractices_Coding_Standards_Methodology.md`, `core/BestPractices_Error_Handling_Methodology.md`.
- `testing` — `testing/Testing_Unit_Testing_Methodology.md` (table-driven matcher cases).

## Inherited Constraints
Pure logic only (no browser APIs) so it is natively testable; edition 2021/stable; rustdoc required
(workspace `missing_docs=warn`); lean deps.

## Out-of-Scope Methodologies
Do NOT load `synthesis`/`decomposition`; do NOT load E2E/integration testing — this module is unit-tested
pure logic.
