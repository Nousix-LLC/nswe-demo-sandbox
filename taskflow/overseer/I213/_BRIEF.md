# _BRIEF.md — NSWE overseer step I213 (persona swe-lead) — ACT: launch review for ferric-router-r1

**Depends on**: I212
**Task Kind**: act — load `REVIEW_GATE`, `WORK_SESSION`. Write review brief and fork review DAG for PR #192.

## Context from I212

- ferric-router-r1 machine gate: **PASS** (confirmed in I212 fold-read).
  SYNTHESIS.md at `taskflow/dags/ferric-router-r1/SYNTHESIS.md`.
  Head commit: 2bf76698c474fb60ca663f6cd074845600caea93 (CI run 41778305739, all 6 SUCCESS).
  PR #192: OPEN/MERGEABLE, `work/ferric-router-r1` → `main`.
  Issues: #131 (navigate_replace / REQ-RT-003), #146 (active-link awareness / REQ-RT-007), #147 (nested routes / REQ-RT-005).
- Design source: `design/ferric/router-and-http.md` (Part 1, REQ-RT-001..008). Already on main (merged with PR #128).
- free_dag_slots: 4 (both prior code slots freed; no reviews launched yet).
- STATE: `taskflow/overseer/I212/project_state.json`.
- Config seam: `taskflow/overseer/_CONFIG.yaml`.

## Work for this step

### 1. Load governing files
Load `appfiles/REVIEW_GATE.md` and `appfiles/WORK_SESSION.md`. Read `_CONFIG.yaml` and
`taskflow/overseer/I212/project_state.json`.

### 2. Write the review brief

Write `taskflow/dags/review-ferric-router-r1/_BRIEF.md` per REVIEW_GATE guidance. Include:

- **Objective**: Review PR #192 (`feat(ferric-router): nested routes, replace navigation, active links`)
  for correctness, code quality, test coverage, security, Rust idioms, and API/contract stability.
- **PR**: https://github.com/Nousix-LLC/nswe-demo/pull/192, branch `work/ferric-router-r1`,
  head commit `2bf76698c474fb60ca663f6cd074845600caea93`.
- **Issues and acceptance criteria**:
  - #131: `navigate_replace(path)` exported from prelude; uses `history.replaceState` on wasm32
    (no history growth); updates `current_path()` reactively; both native and wasm32 tests present.
  - #146: `Link::build()` reads `current_path()` and conditionally emits `aria-current="page"`;
    inactive link has no `aria-current`; frozen `link()` signature unchanged.
  - #147: `RoutePattern::match_prefix` exists with correct semantics; `Router::nest(prefix, layout, child_builder)`
    exists; `Router::outlet()` tries nested routes first; per-level fallback; flat-route behavior preserved.
- **Design reference**: `design/ferric/router-and-http.md` (REQ-RT-001..008) in `Nousix-LLC/nswe-demo` (on main).
- **Concerns**: correctness (all 3 ACs vs design), code quality (idiomatic Rust, error paths),
  test coverage (native + wasm32 for all 3 issues), security (no unsafe, event handling safety),
  Rust idioms (lifetimes, trait impls), API/contract stability (frozen surface from #5 not broken).
- **Declared output**: review verdict (APPROVE/REQUEST-CHANGES), posted GitHub review on PR #192,
  non-blocking findings filed as backlog issues, root `SYNTHESIS.md`.

### 3. Fork the review DAG

Fork `taskflow/dags/review-ferric-router-r1` as `swe-reviewer`.

Write `_FORK.md` at the new root carrying:
- `forked_by`: this thread (swe-lead overseer)
- `thread_type`: dag
- `launch_agent`: swe-reviewer
- `reap_policy`: reap-whole-after-land
- `launch_context`: application: software

### 4. Update board and STATE

- Assign issues #131, #146, #147 status "In review" on board (they already show In Progress from DAG launch).
  Actually they remain In Progress / or move to In Review per board semantics — confirm with REVIEW_GATE.
- Update `taskflow/overseer/I213/project_state.json`:
  - Add review-ferric-router-r1 to `dags_in_flight`.
  - Decrement free_dag_slots by 1 (4 → 3).
  - Record forward_series entry for I213.

## Notes

- I214 follows: fold-read ferric-async-forms-r2 (loads WORK_SESSION + REVIEW_GATE).
