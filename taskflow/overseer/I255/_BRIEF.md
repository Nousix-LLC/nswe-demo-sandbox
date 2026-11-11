# _BRIEF.md — NSWE overseer step I255 (persona swe-lead) — EVALUATE: read fold ferric-ssr-r1

**Depends on**: I254
**Task Kind**: evaluate — load `appfiles/WORK_SESSION.md`, `appfiles/REVIEW_GATE.md`.

## Context from I254 (board check)

### ferric-ssr-r1 DAG: FOLDED — FAIL

- SYNTHESIS.md at `taskflow/dags/ferric-ssr-r1/SYNTHESIS.md`
- Verdict: **FAIL** — client-hydrate spoke (`ferric-ssr-r1-client-hydrate`) never ran
  - BAR-003 / #223: **MET** — `render_to_string` implemented in `crates/ferric/src/ssr.rs`; 14 SSR tests pass; on `work/ferric-ssr-r1`
  - BAR-004 / #224: **NOT MET** — `crates/ferric/src/hydrate.rs` remains `todo!()` stub; `work/ferric-ssr-r1-client` branch never created
  - BAR-005 / #225: out of scope (blocked on #130, correctly excluded)
  - BAR-006 / #226: **PARTIALLY MET** — axum integration (REQ-SSR-011) done and merged into `work/ferric-ssr-r1` via PR #227; mismatch detection NOT done
  - Identity assertion `marker-format-agreement` FAILED (marker in `ssr.rs`, absent from `hydrate.rs` stub)
  - No PR to main was created
- **Remediation budget**: 0 of 2 used
- **PR #227** (`work/ferric-ssr-r1-axum` → `work/ferric-ssr-r1`): MERGED (2026-11-05T00:01:39Z). This PR merged the axum spoke into the goal branch, **not into main**. Main SHA is unchanged at `945fade38abd6b053268501f3801734756f02502`. Issues #223, #224, #226 all remain OPEN.
- **Branch `work/ferric-ssr-r1`**: has server-render + axum-integration commits; no client-hydrate work. No rebase needed (main is unchanged).

### Escalation ferric-async-forms: ACTIVE

- PR #193 last updated 2026-11-04T06:38:30Z (escalation comment). No user response since.
- Clearing condition NOT met. No action.

### Operating config

- `landing_authority: delegated`, `auto_land: true`, `headless: true`
- STATE last written: `taskflow/overseer/I249/project_state.json`

## Work for this step

### 1. Load governing files

Load `appfiles/WORK_SESSION.md` and `appfiles/REVIEW_GATE.md`.

### 2. Read the fold

Re-read `taskflow/dags/ferric-ssr-r1/SYNTHESIS.md` for full detail if needed.
Assess:
- Verdict: FAIL (client-hydrate spoke never ran)
- Budget: 0/2 remediation attempts used → within budget, remediate
- BAR-003 work is done and on the branch; needs to carry forward
- BAR-004 / #224: implement `hydrate` — DOM walk/adopt pass, event handler wiring (REQ-SSR-004, REQ-SSR-005); mismatch detection and recovery (REQ-SSR-009)
- BAR-006 mismatch portion: same as above — mismatch detection is the BAR-004 implementation concern
- Contracts at `work/ferric-ssr-r1` root: `contracts/ferric_ssr_contract.rs` (or the brief's declared contract)

### 3. Decide and schedule

Verdict FAIL, within budget → remediate with ferric-ssr-r2.

Remediation goal (ferric-ssr-r2):
- Branch: `work/ferric-ssr-r1` (continue on the existing branch; no rebase needed as main is unchanged)
- Implement BAR-004 / #224: `crates/ferric/src/hydrate.rs` — full hydration implementation
- Implement BAR-006 mismatch detection (REQ-SSR-009): integrated with BAR-004 implementation
- Open a PR to main closing #223, #224, #226 (server-render + axum + hydration all in one PR)

Schedule the following series:
1. **I256** — Launch remediation DAG ferric-ssr-r2 (act, loads `appfiles/WORK_SESSION.md`, `appfiles/DELIVERABLES_GIT.md`): write the ferric-ssr-r2 brief and fork it; update STATE (move ferric-ssr-r1 from dags_in_flight to dags_folded:FAIL, record remediation attempt 1 for ferric-ssr)
2. **I257** — Board check (evaluate, loads `appfiles/WORK_SESSION.md`, `appfiles/BOARD.md`)

### 4. Write CONTINUE.md

## Notes

- ferric-ssr-r1 is confirmed FOLDED FAIL — dags_in_flight should be updated to 0 when the launch task runs
- ferric-ssr-r2 will be attempt 1 of 2 remediation budget
- #35 (logged-out reading): still deferred — dispatch after ferric-ssr lands
- After ferric-ssr-r2 lands: machine gate → review launch → process review → landing decision → land → then dispatch #35
- ferric-async-forms escalation: ACTIVE, no action this iteration
- main SHA: `945fade38abd6b053268501f3801734756f02502` (unchanged — PR #227 merged only into the goal branch)
