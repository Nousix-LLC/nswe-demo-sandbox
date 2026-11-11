# _BRIEF.md — synthesis-gate

**Goal slug**: `synthesis-gate`
**Kind**: code + verification + PR (atomic)
**Repo**: Nousix-LLC/nswe-demo
**Branch**: `work/ferric-router-r1`
**Workspace**: `taskflow/dags/ferric-router-r1/SUBTASK_synthesis_gate/`

---

## Objective

Verify the complete `work/ferric-router-r1` branch against all contracts in
`taskflow/dags/ferric-router-r1/contracts/`, update the example app to demonstrate nested routes
and active-link awareness, ensure CI passes, create the PR, and author the root `SYNTHESIS.md`
at `taskflow/dags/ferric-router-r1/SYNTHESIS.md`.

This is the final gate: it closes #131, #146, and #147 by landing a correct, CI-green PR.

---

## Inputs

- Working branch: `work/ferric-router-r1` (after `nested-routes` spoke)
- Contracts: `taskflow/dags/ferric-router-r1/contracts/ferric_router_r1_api.md`
- Design spec: `design/ferric/router-and-http.md` (read-only)
- Issues to close: #131, #146, #147 in `Nousix-LLC/nswe-demo`
- CI: six jobs on GitHub Actions (`fmt`, `clippy`, `test`, `wasm`, `doc`, `image`)

---

## Declared output

### Verification pass (before the PR)

Walk through every identity in `contracts/_MANIFEST.yaml` and confirm it is met on the branch:

1. **`frozen_surface_preserved`**: Read `src/lib.rs`, `src/router.rs`, `src/matcher.rs`,
   `src/link.rs`. Confirm every frozen #5 item is present with its original signature.
2. **`navigate_replace_added`**: Confirm `navigate_replace` exists in `router.rs` and is in
   the prelude.
3. **`active_link_awareness`**: Confirm `Link::build()` calls `current_path()` and conditionally
   adds `aria-current="page"`.
4. **`nested_routes_added`**: Confirm `RoutePattern::match_prefix` exists in `matcher.rs` and
   `Router::nest` exists in `router.rs`; confirm `Router::outlet()` tries nested routes first.
5. **`prelude_union`**: Confirm prelude exports exactly
   `{link, Params, RoutePattern, current_path, navigate, navigate_replace, Router}`.
6. **`test_coverage`**: Run `cargo test -p ferric-router` and confirm all tests pass.

### Example update

Update `crates/ferric-router/examples/app.rs` to demonstrate:
- A nested route (`/settings` layout with `/settings/` index and `/settings/profile` child)
- The nav bar uses `link()` helpers that now show `aria-current="page"` on the active link
- One `navigate_replace` call (e.g., a redirect button that replaces instead of pushes)

The existing three routes (`/`, `/about`, `/user/:id`) must still be present and working.

### README update

Update `crates/ferric-router/README.md` to document:
- `navigate_replace` (push vs. replace, when to use each — satisfies REQ-RT-003 doc criterion)
- Nested routes with `Router::nest()` and example (satisfies REQ-RT-005 doc criterion)
- Active-link `aria-current` and how to style the active link (satisfies REQ-RT-007 doc criterion)

### CHANGELOG

Create `crates/ferric-router/CHANGELOG.md` (new file) documenting the r1 additions as additive:
- `navigate_replace(path)` — additive
- `Link`/`link` active-route awareness via `aria-current="page"` — additive
- `RoutePattern::match_prefix` — additive
- `Router::nest(prefix, layout, child_builder)` — additive

### CI verification

Run the following checks locally (they mirror what CI runs):
```bash
cargo fmt --check -p ferric-router
cargo clippy -p ferric-router -- -D warnings
cargo test -p ferric-router
cargo build -p ferric-router --target wasm32-unknown-unknown
cargo build -p ferric-router --example app --target wasm32-unknown-unknown
cargo doc -p ferric-router --no-deps
```

If any check fails, fix the failure before creating the PR.

### PR creation

Create a pull request from `work/ferric-router-r1` → `main` on `Nousix-LLC/nswe-demo` with:

**Title**: `feat(ferric-router): nested routes, replace navigation, active links (Ferric 1.0 router r1)`

**Body** (written for the repository's readers; no host paths, no taskflow internals):
- What changed: enumerate the four additions (navigate_replace, active-link aria-current,
  RoutePattern::match_prefix, Router::nest)
- How it was verified: cargo test, wasm build, CI
- Closes #131, Closes #146, Closes #147

End the PR body with:
```
🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

Do NOT merge the PR. The overseer's review gate does that.

### SYNTHESIS.md

Author `taskflow/dags/ferric-router-r1/SYNTHESIS.md` with:
- For each issue (#131, #146, #147): whether it is met and why (map each acceptance criterion
  to the code or test that satisfies it)
- PR URL
- CI status
- Any deviations from the contracts (there should be none)

---

## Success criteria

1. All five contract identities in `_MANIFEST.yaml` are verified met.
2. `cargo test -p ferric-router` passes (all spokes' tests + frozen baseline).
3. `cargo build -p ferric-router --target wasm32-unknown-unknown` succeeds.
4. `cargo build -p ferric-router --example app --target wasm32-unknown-unknown` succeeds.
5. `cargo clippy -- -D warnings` and `cargo fmt --check` clean.
6. PR created on `work/ferric-router-r1` → `main` with correct `Closes #131, #146, #147`.
7. `SYNTHESIS.md` authored at `taskflow/dags/ferric-router-r1/SYNTHESIS.md`.

---

## Constraints

- Do not merge the PR.
- The PR description must NOT include the host server address, SSH key path, user name, or
  local paths.
- The PR description must NOT reference taskflow-internal paths.
- Closes #131, #146, #147 in `Nousix-LLC/nswe-demo` via the PR description magic keywords.
- Do not touch `design/`.
- Do not change any frozen #5 item in the process of updating docs/examples.
