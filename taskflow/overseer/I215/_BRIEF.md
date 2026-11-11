# _BRIEF.md — NSWE overseer step I215 (persona swe-lead) — ACT: launch review for PR #193

**Depends on**: I214
**Task Kind**: act — load `REVIEW_GATE` + `WORK_SESSION`. Write review brief and fork review-ferric-async-forms-r2.

## Context from I214

- ferric-async-forms-r2 machine gate: PASS confirmed.
  - All 6 CI PASS (run 41780600207, PR #193).
  - PR #193: OPEN/MERGEABLE, `work/ferric-async-forms-r2` → `main`, repo Nousix-LLC/nswe-demo.
  - Issues #130 (EPIC), #143 (DOM events), #144 (form bindings), #145 (further async concerns) — all closed.
  - Deliverables: async_resource.rs, form.rs, dom.rs/vdom.rs (all as designed).
- review-ferric-router-r1 still IN_FLIGHT (forked I213).
- free_dag_slots: 2 (review-ferric-router-r1 in flight, now adding review-ferric-async-forms-r2 → 1 after launch).
- STATE: `taskflow/overseer/I214/project_state.json`.
- Config seam: `taskflow/overseer/_CONFIG.yaml`.

## Work for this step

### 1. Load governing files
Load `appfiles/REVIEW_GATE.md` and `appfiles/WORK_SESSION.md`. Read `_CONFIG.yaml` and
`taskflow/overseer/I214/project_state.json`.

### 2. Write review brief
Write `taskflow/dags/review-ferric-async-forms-r2/_BRIEF.md`.

The review brief must cover:
- **Target**: PR #193 (`work/ferric-async-forms-r2` → `main`), implementing issues #130 (async resources +
  suspense, REQ-ASYNC-001..016), #143 (DOM events, REQ-ASYNC-020..024), #144 (form bindings, REQ-ASYNC-040..043),
  #145 (further async concerns). Design reference: `design/ferric/async-forms-events.md`.
  Code DAG COMPLETE.md: `taskflow/dags/ferric-async-forms-r2/COMPLETE.md`.
- **Concerns** (distinct, each with its goal and bar):
  - Correctness: does the change implement REQ-ASYNC-001..024, REQ-ASYNC-040..043 correctly, including
    edge cases (error paths in async resources, event binding teardown, form binding two-way sync),
    async hazards (resource lifecycle, signal/reactive invalidation), and concurrency correctness?
  - Code quality and design: responsibilities, abstraction boundaries (async_resource / form / dom split),
    naming, function size, error-handling style, and whether the change leaves ferric simpler to extend.
  - Test coverage and depth: do native + WASM tests exercise each acceptance criterion? Are edge and error
    paths tested? Do tests assert real behavior rather than pass vacuously?
  - Security: input handling (custom event data, form binding data), trust boundaries (web-sys/wasm bridge),
    and no host-specific or internal-infrastructure detail committed (host paths, tailnet IPs, etc.).
  - Rust idioms: one concern among these; DAG already wrote to it. Check for soundness, lifetime correctness,
    and idiomatic async/WASM patterns.
  - API/contract stability: does the public API (prelude re-exports, `Resource`, `Bind`, `FormField`,
    `suspense()`) align with what downstream crates (chirp-frontend) would depend on?
- **Declared output**: posted review on PR #193, root `SYNTHESIS.md` at
  `taskflow/dags/review-ferric-async-forms-r2/SYNTHESIS.md` with APPROVE or REQUEST-CHANGES verdict,
  findings per concern with severity and blocker status, non-blocking findings filed as backlog issues.
- **Constraint**: repo Nousix-LLC/nswe-demo only; no host paths, no internal IPs in findings.

### 3. Fork the review DAG
Fork review-ferric-async-forms-r2 as swe-reviewer.

### 4. Update STATE
Write `taskflow/overseer/I215/project_state.json`:
- Move review-ferric-async-forms-r2 to dags_in_flight.
- Update free_dag_slots: 2 → 1.
- Update forward_series with I215 entry.

## Notes

- I216 follows: EVALUATE — board check / watch review folds: review-ferric-router-r1 and
  review-ferric-async-forms-r2.
- Config: delegated/auto_land/headless. On APPROVE for PR #193, land without human gate.
