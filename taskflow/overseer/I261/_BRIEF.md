# _BRIEF.md — NSWE overseer step I261 (persona swe-lead) — ACT: launch ferric-ssr-r3 CI-fix remediation DAG

**Depends on**: I260
**Task Kind**: act — load `appfiles/WORK_SESSION.md` and `appfiles/DELIVERABLES_GIT.md`.

## Context from I260 (fold evaluation)

- ferric-ssr-r2 folded with SYNTHESIS.md PASS (all 7 internal identity assertions passing).
- PR #228 (`work/ferric-ssr-r1` → `main`) is OPEN and MERGEABLE but **CI is failing** on 3 checks:
  - **fmt**: `crates/ferric/src/lib.rs:25` — `pub mod ssr;` and the following `#[cfg(target_arch = "wasm32")]` line are not separated by a blank line; `cargo fmt --all --check` fails.
  - **clippy** (3 errors in `crates/ferric/src/ssr.rs`):
    - line 178: `text("<>&\"'").into()` — useless `.into()` on `VNode` (clippy::useless_conversion)
    - line 202: `text("world").into()` — same
    - line 209: `text("").into()` — same
  - **doc**: `crates/ferric/src/ssr.rs` line 16 — module-level doc comment references private item `crate::signal::ReactiveScope` (`rustdoc::private_intra_doc_links`). The fix is to replace the backtick-linked reference `[\`crate::signal::ReactiveScope\`]` with plain text that does not create a private intra-doc link (e.g., "a per-request `ReactiveScope`").
- Machine gate: FAIL (CI failures block landing).
- Escalation on PR #193 (ferric-async-forms): still ACTIVE, no user response — do not start new work on that epic.
- Remediation attempt: this will be attempt 2 of 2 (last attempt). If CI still fails after this attempt, escalate to the user with what was tried.
- Main SHA at last board check: `945fade38abd6b053268501f3801734756f02502`
- STATE at: `taskflow/overseer/I256/project_state.json`

## Work for this step

### 1. Load governing files

Load `appfiles/WORK_SESSION.md` and `appfiles/DELIVERABLES_GIT.md`.

### 2. Read the config seam

Read `taskflow/overseer/_CONFIG.yaml`. Confirm:
- `landing_authority: delegated`, `auto_land: true`, `headless: true`
- Repo: `Nousix-LLC/nswe-demo`

### 3. Launch ferric-ssr-r3 remediation DAG

Write the brief at `taskflow/dags/ferric-ssr-r3/_BRIEF.md` and fork a `swe-coder` DAG to fix the 3 CI failures on branch `work/ferric-ssr-r1`.

**Goal**: Fix the 3 CI failures on PR #228 (`work/ferric-ssr-r1` → `main`) so the PR passes `cargo fmt --all --check`, `cargo clippy --workspace --all-targets --locked -- -D warnings`, and `cargo doc --workspace --no-deps --locked` (with `RUSTDOCFLAGS=-D warnings`). All originally-passing CI checks (test, wasm) must remain passing.

**Branch**: `work/ferric-ssr-r1` (same branch as PR #228)

**Declared output**: 1 commit on `work/ferric-ssr-r1` fixing the 3 issues, pushed to origin; a root `SYNTHESIS.md` accounting for all three fixes and the full CI check results. No new PR — this pushes to the existing branch tracked by PR #228.

**Issues covered**: #223, #224, #226 (unchanged from ferric-ssr-r2 — do not modify the functional implementation).

**What to fix and verify** (each is a distinct concern):

1. **fmt**: Add a blank line in `crates/ferric/src/lib.rs` between `pub mod ssr;` and the `#[cfg(target_arch = "wasm32")] pub mod hydrate;` block. Run `cargo fmt --all --check` to confirm clean.

2. **clippy**: Remove the `.into()` suffix on 3 test-only VNode returns in `crates/ferric/src/ssr.rs` (lines 178, 202, 209). Run `cargo clippy --workspace --all-targets --locked -- -D warnings` to confirm zero errors.

3. **doc**: In `crates/ferric/src/ssr.rs` module-level doc comment (line ~16), replace the backtick-linked reference to the private item `crate::signal::ReactiveScope` with plain text that does not create a private intra-doc link (e.g., use "a per-request reactive scope"). Run `cargo doc --workspace --no-deps --locked` with `RUSTDOCFLAGS=-D warnings` to confirm clean.

4. **Regression guard**: Confirm `cargo test -p ferric`, `cargo check --target wasm32-unknown-unknown -p ferric`, and `cargo build -p chirp-server` all still pass (the full set of originally-passing assertions from ferric-ssr-r2).

**Constraints**:
- Branch: `work/ferric-ssr-r1` only; do not touch `main` or any other branch.
- Do not modify `crates/ferric/src/hydrate.rs`, `crates/ferric/src/ssr.rs` (functional code), or any frozen prelude file (`lib.rs` signal/dom/router/vdom declarations, `signal.rs`, `dom.rs`, `router.rs`) beyond the minimal fmt/clippy/doc fixes stated above.
- No force-push.
- Commit message must not reference host paths or taskflow internals.

### 4. Record goal state and schedule follow-up

After forking the DAG:
- Note in the brief for I262 that ferric-ssr-r3 is in flight (attempt 2 of 2).
- Schedule I262 as a board check (evaluate, loads WORK_SESSION + BOARD) to watch for ferric-ssr-r3 fold.

## Notes

- Do NOT start any new goals while this CI-fix DAG is in flight.
- The ferric-async-forms escalation (PR #193) is still ACTIVE. Do not interpret any board events about it as resolved — wait for explicit user response.
- Remediation budget: attempt 2 of 2. If ferric-ssr-r3 fails CI again, escalate to the user with the two attempts and their outcomes.
