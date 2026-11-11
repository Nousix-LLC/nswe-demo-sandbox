# _BRIEF.md — NSWE overseer step I293 (persona swe-lead) — ACT: process review fold (review-ferric-async-forms-r3 APPROVE)

**Depends on**: I292
**Task Kind**: act — load `appfiles/REVIEW_GATE.md` and `appfiles/BOARD.md`.

## Context from I292

I292 woke from the +15-minute timer and found review-ferric-async-forms-r3 has completed with **APPROVE**.
- review-ferric-async-forms-r3: **APPROVE** — SYNTHESIS.md present at `taskflow/dags/review-ferric-async-forms-r3/SYNTHESIS.md`
- chirp-logged-out: still in flight (SYNTHESIS.md not present)

STATE at: `taskflow/overseer/I292/project_state.json`
Config seam: `taskflow/overseer/_CONFIG.yaml`

## Work for this step

### 1. Load governing files

Load `appfiles/REVIEW_GATE.md` and `appfiles/BOARD.md`.

### 2. Confirm review is posted on PR #193

The SYNTHESIS.md states: "Review posted to PR #193 via `gh pr review 193 --repo Nousix-LLC/nswe-demo --approve`."
Verify via `gh pr view 193 --repo Nousix-LLC/nswe-demo --json reviews` that the APPROVE review is on the PR.

### 3. Add non-blockers #248–#253 to the GitHub project board

The review DAG filed six non-blocker issues on GitHub:
- #248: REQ-ASYNC-016 concurrent stale-discard test gap (`async_resource.rs`)
- #249: `#[allow(clippy::type_complexity)]` on EventHandler enum — use type alias instead
- #250: Inaccurate closure.forget() comment in form.rs WASM test
- #251: `dom.rs` event_name()/stash_key() return String — use `Cow<'static, str>`
- #252: `Bind::on_input_handler()` / `on_input_event_handler()` return type not in prelude
- #253: `ResourceState` and `EventHandler` missing `#[non_exhaustive]`

For each of #248–#253:
- Run `gh project item-add 1 --owner Nousix-LLC --url https://github.com/Nousix-LLC/nswe-demo/issues/<N>`
  to add to project board (project number 1 = PVT_kwDOEB9jls4BlZH4).
- Record the returned project item ID.
- After adding all six, update `taskflow/overseer/_CONFIG.yaml` to add `issue_248` through `issue_253`
  with their project item IDs under `project_item_ids`.
- Set each to status "Todo" (option id `f75ad846`) via `gh api` mutation.

### 4. Update STATE

Write updated STATE at `taskflow/overseer/I293/project_state.json` reflecting:
- review-ferric-async-forms-r3: FOLDED (APPROVE)
- Non-blockers #248–#253 added to board as Todo
- ferric_async_forms_goal: review_verdict updated to APPROVE, landing pipeline scheduled

### 5. Proceed

Schedule I294 (land PR #193) as the next step.

## Notes

- Landing authority is **delegated** (`auto_land: true`, `headless: true` from _CONFIG.yaml).
  Land on machine PASS + review APPROVE without a human gate.
- PR #193 is on branch `work/ferric-async-forms-r2`, head SHA `838239e`, epic #130.
- CI: all 6 jobs green (run https://github.com/Nousix-LLC/nswe-demo/actions/runs/42126720006).
- Review non-blockers from review-ferric-async-forms-r2 (#196–#201 or similar) may already be on the board;
  only #248–#253 (from this new review round) need adding.
