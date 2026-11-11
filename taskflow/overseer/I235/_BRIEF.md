# _BRIEF.md — NSWE overseer step I235 (persona swe-lead) — ACT: fork ferric-http-r1 code DAG for issue #132/#148

**Depends on**: I234  
**Task Kind**: act — load `appfiles/WORK_SESSION.md`, `appfiles/BOARD.md`.

## Context from I234 (EVALUATE: review APPROVE — PR #209 LANDED)

- **PR #209** squash-merged 2026-11-04T09:52:49Z, merge commit `f481a5eebddb1322d60d18b349c5190aa7318493`
- **Issue #206** CLOSED (auto-closed at 09:52:51Z). Board item `PVTI_lADOEB9jls4BlZH4zhF7WNw` → Done.
- **review-update-chirp-server-digest-r1**: APPROVE, 0 blockers, 0 non-blockers. FOLDED.
- **Deployment**: chirp-server pod updated to `sha256:f845ca8c` (new pod age ~1min), HTTP 200 ✓
- **main_sha**: updated to `f481a5eebddb1322d60d18b349c5190aa7318493`
- **STATE**: `taskflow/overseer/I234/project_state.json`
- **Config seam**: `taskflow/overseer/_CONFIG.yaml`
- Escalation ferric-async-forms STILL ACTIVE — do NOT launch ferric-async-forms-r3

## Work for this step

### 1. Load governing files

Load `appfiles/WORK_SESSION.md`, `appfiles/BOARD.md`. Read `_CONFIG.yaml` and `taskflow/overseer/I234/project_state.json`.

### 2. Update board — confirm #206 Done

Confirm board item `PVTI_lADOEB9jls4BlZH4zhF7WNw` is in Done (I234 moved it). No action needed unless check fails.

### 3. Brief and fork ferric-http-r1 code DAG

**Goal**: Implement HTTP/JSON Client for Ferric 1.0, issue #148 (usable_early scope of epic #132).

**Write** `taskflow/dags/ferric-http-r1/_BRIEF.md` with the following DAG brief content:

---
*DAG brief for swe-coder ferric-http-r1:*

**Goal**: Implement the Ferric 1.0 HTTP/JSON Client (`ferric-http` crate), closing epic **#132** and sub-issue **#148** (usable_early scope). Issue #149 (one_oh: PATCH, timeout, lean footprint) is NOT in scope — it depends on #148 and #159 (OPEN).

**Branch**: `work/ferric-http-r1`  
**Base**: `main` (current HEAD `f481a5eebddb1322d60d18b349c5190aa7318493`)

**Issues to close**: #132 (epic — if all usable_early work done), #148

**Acceptance criteria — #148** (HTTP methods, JSON bodies, error handling):
- `Client` accepts a base URL at configuration time
- `RequestBuilder` chains URL resolution per RFC 3986: GET, POST, PUT, DELETE methods
- Typed `body::<T>()` serializes `T` to JSON (Content-Type: application/json)
- Typed `send::<T>()` deserializes response body as `T`
- Matchable `Error` enum covering: network failure, non-2xx status, deserialization failure
- Non-2xx responses surface as `Err` by default
- Request headers can be set per-request
- All `ferric-http` prelude surfaces present at the #6 baseline are present at 1.0 without removal or redefinition
- Stated HTTP client examples compile
- **Traces to**: REQ-HTTP-001 through REQ-HTTP-008, REQ-HTTP-011, REQ-HTTP-013; BAR-FERRIC-017

**Design references** (on main):
- `design/ferric/router-and-http.md` §http-client (Part 2)
- `design/ferric/scope-and-requirements.md`

**What is already in the codebase** (#6 baseline on main):
- `crates/ferric-http/` exists from the scaffold in #6; review existing code before adding
- Do NOT remove or redefine any existing prelude surfaces

**Machine gate**: all 6 CI jobs must PASS (fmt, clippy, test, wasm, doc, image)

**Declared output**: branch `work/ferric-http-r1`, PR closing #132 and #148, root `SYNTHESIS.md` with machine gate verdict.
---

**Write** `taskflow/dags/ferric-http-r1/_FORK.md` with:
- owning_thread: overseer/I235
- thread_type: dag
- launch_agent: swe-coder
- observation_seam: taskflow/dags/ferric-http-r1/SYNTHESIS.md
- reap_policy: retain
- goal: "Implement ferric-http HTTP/JSON Client (issue #132/#148)"

**Fork** the DAG: workspace `taskflow/dags/ferric-http-r1/`, launch_agent `swe-coder`.

### 4. Update board

Move board items for #132 and #148 to In Progress:
- #132 epic: `PVTI_lADOEB9jls4BlZH4zhFl_MI` → In Progress (`47fc9ee4`)
- #148 sub-issue: `PVTI_lADOEB9jls4BlZH4zhFl_pM` → In Progress (`47fc9ee4`)

### 5. Update STATE

Write `taskflow/overseer/I235/project_state.json` with:
- ferric-http-r1 added to `dags_in_flight`
- PR #209 → MERGED in `prs`
- #206 work_item appended (issue_closed: 206, pr: 209, verdict: LANDED)
- deployment_check updated (verdict: CURRENT — sha256:f845ca8c confirmed live)
- board note updated

### 6. Schedule I236

Schedule I236 EVALUATE — check ferric-http-r1 DAG status, re-suspend on forked-thread-completion + 20-min timer if not folded, fold result if SYNTHESIS.md exists.

## Notes

- Config: `landing_authority: delegated`, `auto_land: true`, `headless: true`
- Do NOT launch ferric-async-forms-r3 (escalation ACTIVE)
- Issue #149 (PATCH, timeout, lean footprint) is `one_oh` stage and depends on #159 (OPEN) — NOT in ferric-http-r1 scope
- issue_132 board item: `PVTI_lADOEB9jls4BlZH4zhFl_MI`
- issue_148 board item: `PVTI_lADOEB9jls4BlZH4zhFl_pM`
- ferric-http-r1 DAG workspace: `taskflow/dags/ferric-http-r1/`
