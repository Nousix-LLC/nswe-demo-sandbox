# _BRIEF.md — NSWE overseer step I249 (persona swe-lead) — ACT: fork scope-limited ferric-ssr-r1 code DAG

**Depends on**: I248
**Task Kind**: act — load `appfiles/WORK_SESSION.md`, `appfiles/DELIVERABLES_GIT.md`.

## Context from I248 (EVALUATE: file #133 sub-issues + assess product work readiness)

- **#133 sub-issues filed** (all 4 work items now have issues):
  - #223 — Server-side HTML rendering and per-request scope isolation (BAR-003) — Not blocked on #130
  - #224 — Client hydration without re-render — must-have (BAR-004) — Not blocked on #130
  - #225 — State carry and async resource resume across the SSR seam (BAR-005) — **Blocked on #130**
  - #226 — Hydration mismatch detection and Axum server integration (BAR-006) — Not blocked on #130
- **SSR independence analysis**: BAR-003, BAR-004, BAR-006 are independent of #130. Only BAR-005 (async resource resume) explicitly depends on the async resource primitive from #130. The design confirms the view layer is already server-compilable, event wiring on hydrate extends automatically without change, and mismatch detection + Axum integration have no #130 dependency.
- **Decision: Option A** — a coherent, valuable subset (BAR-003 + BAR-004 + BAR-006) can proceed now. This subset delivers the ferric 1.0 gating must-have (BAR-004: hydration without re-render).
- **Product work**: #35 (Logged-out reading) is now unblocked — its only dependency (#56 durable persistence) is Done. However, the SSR ferric framework work is higher strategic priority: it delivers the ferric 1.0 gating must-have and unblocks the full #133 → #134 → #135 → #136 chain once #130 resolves. #35 is next after ferric-ssr lands.
- **Escalation**: `escalation_ferric_async_forms_budget_exhausted` STILL ACTIVE — no user response on PR #193.
- **Config**: `landing_authority: delegated`, `auto_land: true`, `headless: true`
- **Repo**: `Nousix-LLC/nswe-demo`, `main` SHA: `945fade38abd6b053268501f3801734756f02502`
- **STATE**: `taskflow/overseer/I248/project_state.json`

## Work for this step

### 1. Load governing files

Load `appfiles/WORK_SESSION.md` and `appfiles/DELIVERABLES_GIT.md`.

### 2. Confirm DAG slot available

Check `dags_in_flight` from I248 STATE. If a slot is free (expect 1 free slot), proceed. If none, record waiting and pass on; the next board check picks it up.

### 3. Write the brief for the ferric-ssr-r1 code DAG

Write `taskflow/dags/ferric-ssr-r1/_BRIEF.md` for a scope-limited SSR code DAG covering only the independent subset of #133 (BAR-003 + BAR-004 + BAR-006: issues #223, #224, #226).

The brief must describe:

**Objective**: Implement the scope-limited SSR and hydration foundation for Ferric, covering server-side HTML rendering, per-request isolation, client hydration without re-render, hydration mismatch detection, and the Axum server integration path. The state carry and async resource resume work (BAR-005 / #225) is **explicitly out of scope** (blocked on #130).

**Issues and acceptance criteria**:
- #223 (BAR-003): `render_to_string`, off-wasm compilation, text-boundary markers, per-request reactive isolation, HTML escaping, additive surface
- #224 (BAR-004): `hydrate` entry point, zero structural mutations during hydration (observable via `MutationObserver` or node-identity), event handler wiring onto adopted elements, reactive effect establishment
- #226 (BAR-006): Hydration mismatch detection (detect at adoption path, actionable dev-build diagnostic, subtree recovery), Axum integration (document assembly library surface, composing with existing `chirp-server`/`build_router`)

**Inputs**:
- Repository: `Nousix-LLC/nswe-demo` at `945fade38abd6b053268501f3801734756f02502` on `main`
- Design specs: `design/ferric/ssr-hydration.md` and `design/ferric/scope-and-requirements.md` in the repo (merged via PR #128) — the authoritative source for the SSR architecture and requirements register `REQ-SSR-*`
- Current ferric crate surface (`crates/ferric`): `signal`, `vdom`, `component`, `dom`, the frozen `ferric` prelude including `mount`, and the existing Axum server in `crates/chirp-server`
- Authoring model landed in PR #188 (commit `aa2468771`): `view!` macro, component system, context — now in `main`
- Router landed in PR #203 (commit `d8230fea`): client-side router — now in `main`
- HTTP client landed in PR #210 (commit `945fade3`): fetch/JSON HTTP client — now in `main`

**Declared output**:
- Commits on branch `work/ferric-ssr-r1`
- One PR closing #223, #224, #226 (BAR-003, BAR-004, BAR-006)
- Root `SYNTHESIS.md` accounting for each issue (met, or not and why)
- Note explicitly on the PR: BAR-005 / #225 (state carry + async resource resume) is a follow-up issue dependent on #130 and is NOT part of this goal

**Concerns to cover**:
- *Server render correctness*: `render_to_string` produces valid, well-formed HTML; text-boundary markers are unambiguous; HTML escaping holds for all injection-risky characters; the view layer builds natively off-wasm with no browser APIs; `REQ-SSR-001`, `REQ-SSR-002`, `REQ-SSR-003`, `REQ-SSR-010`, `REQ-SSR-012`
- *Per-request isolation*: each server render runs in its own reactive context; no signal subscription leaks across requests; testable by concurrent render of two requests with different seeded state; `REQ-SSR-003`
- *Hydration without re-render*: `hydrate` adopts the server DOM with zero structural mutations under the hydration root; this is the observable gating bar (zero create/replace/move/remove, verifiable by `MutationObserver` or node-identity in a headless `wasm-bindgen-test`); `REQ-SSR-004`, `REQ-SSR-005`
- *Event wiring on adopt*: existing `Click` and `Input` handlers wire onto adopted elements; subsequent signal updates patch via the existing keyed-patch path; `REQ-SSR-005`
- *Mismatch detection and recovery*: the hydration walk detects tag/text divergence at any path; dev-build diagnostic names path + expected/found; mismatched subtree is recovered by client-rendering; the rest of the document remains adopted; `REQ-SSR-009`
- *Axum integration*: `render_to_string` + document assembly library surface callable from an Axum handler; composing with `chirp-server`'s existing `build_router`; documented usage; `REQ-SSR-011`
- *Additive surface*: `mount` and the frozen prelude are unchanged; `hydrate` and `render_to_string` are new surface; existing apps compile and run without modification; `REQ-SSR-012`
- *Test coverage*: server-render path covered by native tests (not wasm); hydration path covered by headless `wasm-bindgen-test`; mismatch detection covered by a headless test with a deliberately mismatched DOM; Axum integration covered by an example or integration test

**Constraints**:
- Branch: `work/ferric-ssr-r1`; no force-push to `main`
- Scope: `crates/ferric` and `crates/chirp-server` only; do not touch other crates except additive entries in Cargo.toml/workspace
- BAR-005 (#225) is out of scope; do not attempt async resource serialisation or state island implementation
- The frozen `ferric` prelude surface (including `mount`, `Signal`, `create_effect`, router, HTTP client) must remain unchanged; all additions are additive

### 4. Write `_FORK.md` for the ferric-ssr-r1 DAG

Write `taskflow/dags/ferric-ssr-r1/_FORK.md` with:
- `launch_agent: swe-coder`
- `reap: whole-after-land`
- `launch_context: { application: software }`

### 5. Fork the ferric-ssr-r1 DAG

Fork it via `engine_fork`. Assign issues #223, #224, #226 to the authenticated `gh` user. Move those issues to "In Progress" on the project board. Record the goal in STATE (goal_slug: `ferric-ssr-r1`, issues: [223, 224, 226], branch: `work/ferric-ssr-r1`).

### 6. Update STATE

Write `taskflow/overseer/I249/project_state.json` with:
- `dags_in_flight`: the forked ferric-ssr-r1 DAG
- Escalation status (still ACTIVE)
- #35 unblocked (noted, not dispatched — waiting for ferric-ssr to land)
- Forward plan

### 7. Write CONTINUE.md

Write `taskflow/overseer/I249/CONTINUE.md` after completing the step.

## Notes

- Config: `landing_authority: delegated`, `auto_land: true`, `headless: true`
- main_sha: `945fade38abd6b053268501f3801734756f02502`
- ferric-async-forms escalation: ACTIVE, clearing condition NOT met
- #133 sub-issues filed: #223 (BAR-003), #224 (BAR-004), #225 (BAR-005, blocked), #226 (BAR-006)
- #35 unblocked: its only dependency (#56 durable persistence) is Done
- After ferric-ssr-r1 lands: next is a board check (which will see #35 ready and check the escalation)
