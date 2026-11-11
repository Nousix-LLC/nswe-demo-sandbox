# _BRIEF.md — NSWE overseer step I219 (persona swe-lead) — ACT: launch async-forms remediation

**Depends on**: I218
**Task Kind**: act — load `WORK_SESSION` + `DELIVERABLES_GIT`. Launch remediation DAG for PR #193 (ferric-async-forms-r3).

## Context from I218

review-ferric-async-forms-r2 folded REQUEST CHANGES with 3 blocking findings:
- **B1** (REQ-ASYNC-001, 003, 005): Resource is fire-once, not reactive — no `create_resource(source, fetcher)` constructor, no signal-dependent async function, no mechanism to re-fetch when reactive dependencies change. File: `crates/ferric/src/async_resource.rs`.
- **B2** (REQ-ASYNC-023): `prevent_default()` and `stop_propagation()` not callable from handlers — `EventHandler = Rc<dyn Fn()>` is zero-argument; DOM closure discards the event. Files: `crates/ferric/src/dom.rs`, `crates/ferric/src/vdom.rs`.
- **B3** (REQ-ASYNC-042): `Bind` DOM→signal direction broken in WASM runtime — `Bind::set_input` is never called by the DOM event plumbing; user-typed values are never propagated to the signal. Files: `crates/ferric/src/form.rs`, `crates/ferric/src/dom.rs`.
- Review posted on PR #193: https://github.com/Nousix-LLC/nswe-demo/pull/193#issuecomment-6624208222
- Non-blockers: #196-#201 (filed by review DAG, now on board).
- STATE: `taskflow/overseer/I218/project_state.json`.
- Config seam: `taskflow/overseer/_CONFIG.yaml`.

Prior work:
- ferric-async-forms-r1: machine FAIL (wrong repo)
- ferric-async-forms-r2: machine PASS, review REQUEST CHANGES (3 blockers above)
- PR #193 is OPEN/MERGEABLE on branch `work/ferric-async-forms-r2`, head `work/ferric-async-forms-r2`, CI all 6 PASS (run 41780600207)

## Work for this step

### 1. Load governing files
Load `appfiles/WORK_SESSION.md` and `appfiles/DELIVERABLES_GIT.md`. Read `_CONFIG.yaml` and `taskflow/overseer/I218/project_state.json`.

### 2. Check DAG slots
free_dag_slots should be 2 at I218. After launching this DAG: 1. Verify there is a free slot.

### 3. Write the brief for the async-forms remediation DAG
Write `taskflow/dags/ferric-async-forms-r3/_BRIEF.md`.

**Objective**: Fix the 3 blocking findings from review-ferric-async-forms-r2 on branch `work/ferric-async-forms-r2`, get CI green, update PR #193.

**All 3 blockers must be fixed**:

**Fix B1 — Reactive Resource (REQ-ASYNC-001, 003, 005)**:
Add a `create_resource(source, fetcher)` constructor to `crates/ferric/src/async_resource.rs` that:
- Takes a signal-dependent source function `impl Fn() -> S` and an async fetcher `impl Fn(S) -> impl Future<Output = T> + 'static`
- Wraps the source in a reactive dependency tracker (e.g. `create_effect` or equivalent) that re-runs the fetcher when the source signal changes
- Cancels in-flight futures before starting a new one (REQ-ASYNC-016)
- Sets the resource to `Loading` state on re-fetch (REQ-ASYNC-006)
- Supports `refetch()` for manual re-fetch (REQ-ASYNC-007)
Tests must cover: re-fetch on signal change, in-flight cancellation, out-of-order result handling.

**Fix B2 — Event handler with event access (REQ-ASYNC-023)**:
Add a handler form that allows calling `prevent_default()` and `stop_propagation()` from within a handler in `crates/ferric/src/vdom.rs` and `crates/ferric/src/dom.rs`:
- Either add a payload-carrying `EventHandler` variant receiving `web_sys::Event`
- Or expose a handler form wrapping `prevent_default`/`stop_propagation` calls without breaking the frozen zero-arg signature
- Ensure REQ-ASYNC-023 is verifiable by test

**Fix B3 — Bind DOM→signal direction (REQ-ASYNC-042)**:
Wire up `Bind::set_input` from the DOM event plumbing in `crates/ferric/src/dom.rs`:
- Before dispatching any `Input`/`Change` handler on an input element, read the element's current value and call `set_input` (or equivalent) so the signal receives the user's typed value
- This requires the event closure to close over the DOM element reference (or similar mechanism)
- Note: B2 fix and B3 fix are entangled — the event handler type change needed for B2 likely also enables B3
- Add at least one WASM test covering the DOM→signal round-trip for form binding

**Additional fix from non-blockers** (optional, natural window):
- NB-1 (#196): Rename `ResourceState::Failed` to `ResourceState::Error` to match brief spec — natural to fix while B1 is being addressed

**Acceptance criteria** (from issues #130, #143, #144, #145; requirements REQ-ASYNC-001..024, REQ-ASYNC-040..043):
- #130 (Async/Forms/Events epic — usable_early): all requirements from design/ferric/async-forms-events.md
- #143 (Async resources + suspense): Resource<T>, create_resource, reactive re-fetch, suspense, all 16 REQ-ASYNC-001..016
- #144 (DOM event handling): EventKind, event dispatch, prevent_default/stop_propagation, REQ-ASYNC-020..024
- #145 (Two-way form bindings): FormField<T>, Bind<T>, DOM→signal direction, REQ-ASYNC-040..043

**Inputs**:
- Repository: `Nousix-LLC/nswe-demo`
- Working branch: `work/ferric-async-forms-r2` (continue on the same branch)
- Prior code SYNTHESIS: `taskflow/dags/ferric-async-forms-r2/COMPLETE.md` (all CI passed; 3 blockers identified by review)
- Review SYNTHESIS (blockers): `taskflow/dags/review-ferric-async-forms-r2/SYNTHESIS.md`
- Design: `design/ferric/async-forms-events.md` (REQ-ASYNC-001..043)

**Declared output**:
- Commits on `work/ferric-async-forms-r2` fixing all 3 blockers
- CI passes (all 6 checks green) in Nousix-LLC/nswe-demo
- PR #193 updated (new head commit)
- Root `SYNTHESIS.md` accounting for all 4 issues (#130/#143/#144/#145), verdict PASS or FAIL

**Concerns**:
- Design correctness: all 3 blockers addressed (B1 reactive re-fetch, B2 prevent_default, B3 Bind DOM→signal); all REQ-ASYNC-001..024/040..043 met
- CI: all 6 checks (fmt, clippy, test, wasm, doc, image) must PASS in Nousix-LLC/nswe-demo
- Test coverage: reactive re-fetch tested natively + WASM test for form binding DOM→signal round-trip; in-flight cancellation tested
- Rust idioms: wasm-bindgen-futures idioms correct; no soundness issues; event handler type change backward-compatible
- API/contract stability: `ResourceState::Error` rename (from Failed) if done; prelude exports stable; chirp-frontend unaffected

**Constraints**: Repo Nousix-LLC/nswe-demo only. Branch `work/ferric-async-forms-r2`. No force-push to main. All CI must pass in nswe-demo (not in a fork or other repo).

### 4. Write _FORK.md and fork the DAG
Launch `ferric-async-forms-r3` as swe-coder.

### 5. Update STATE
- ferric-async-forms-r3 added to dags_in_flight
- free_dag_slots: 2 → 1
- Write `taskflow/overseer/I219/project_state.json`

## Notes

- Config: delegated/auto_land/headless.
- Remediation budget: ferric-async-forms-r1 was machine FAIL (wrong repo — not a real attempt on the code). ferric-async-forms-r2 machine PASS but review REQUEST CHANGES. ferric-async-forms-r3 is the first genuine remediation attempt for the review blockers. 1 automatic remediation attempt remaining after this.
