# _BRIEF.md — NSWE overseer step I418 (persona swe-lead) — ACT: process review-chirp-logged-out-r1 + launch chirp-logged-out-r27

**Depends on**: I417

**Task Kind**: act — load `appfiles/REVIEW_GATE.md`, `appfiles/BOARD.md`, `appfiles/WORK_SESSION.md`, `appfiles/DELIVERABLES_GIT.md`.

## Context from I417

I417: stall check 3/4 performed. `review-chirp-logged-out-r1` **FOLDED REQUEST-CHANGES** (confirmed I417, ~15:20Z).

- **Review DAG**: `review-chirp-logged-out-r1` — FOLDED, verdict: REQUEST-CHANGES
- **Review synthesis**: `taskflow/dags/review-chirp-logged-out-r1/SYNTHESIS.md`
- **PR #263**: OPEN/MERGEABLE, head `decb6196c2c1e6ed421d393a642f0c844cc333ba`, CI ALL 6 PASS
- **Branch**: `work/chirp-logged-out`
- **Issue**: #35 ("Logged-out reading and a useful landing with accurate states")
- **Code verdict**: PASS — `chirp-logged-out-r26` folded PASS (I413), all 5 ACs met

### Two blockers (both single-line regressions, not new-feature gaps):

**Blocker 1 — `crates/chirp-frontend/src/timeline.rs:218`**
```rust
let result = ctx.client().pub_timeline(&query).await;   // ← was timeline()
```
`pub_timeline()` constructs an unauthenticated HTTP client. Authenticated users on `/timeline` now see the global public feed instead of their personalized following feed. Fix: revert to `ctx.client().timeline(&query).await`.

**Blocker 2 — `crates/chirp-frontend/src/compose.rs:519`**
```rust
link("/compose", "Log in →")   // ← should be /signin
```
The "Log in →" CTA on the sign-up page routes to `/compose` instead of `/signin`. Fix: `link("/signin", "Log in →")`.

### Non-blockers flagged ⚑ for issue filing (6 findings):
- **CQ-C** (`api.rs:434`): `pub_timeline_url_has_correct_path_and_no_auth` test never calls `pub_timeline()`; reproduces method inline — a path change would not fail it. File as test-gap issue.
- **CQ-D** (`api.rs:217`, `landing.rs:19`, `public_profile.rs:15`): Method doc says "ISO 8601 cursor"; wire type is `Option<i64>` (Unix milliseconds). A caller following the doc receives a 422. File as docs/bug issue.
- **CQ-E** (`sign_up.rs:23`): `sign_up::sign_up_view` is a public export with no live caller. The `/signup` route binds to `compose::signup_view`. Module doc claims `/signup`, contradicting the route table. File as code-health/refactor issue.
- **CQ-G** (`hydrate.rs:494`, `dom.rs:309`): `static_event_kinds()` is a hand-written array without the compile-time completeness guard that `event_name()` and `stash_key()` have. A missing entry causes silent listener accumulation on re-renders. File as safety/code-health issue.
- **CQ-H** (`ferric-http/src/error.rs:111`, `chirp-frontend/src/error.rs:60`): JSON deserialization failures reach the catch-all arm, surfacing serde_json error text (including expected field names) in the UI banner. Fix: handle `HttpError::Deserialize` before catch-all with a fixed message; log the serde error. File as security/UX issue.
- **CQ-I** (`chirp-frontend/src/error.rs:53–57`): HTTP status errors include the full API endpoint URL in the banner. Fix: emit status code only. File as security/UX issue.

### Additional non-blockers (grouped, may file as a batch or individual issues):
- SM-F1, SM-F2: No view-tree tests for continuation-error and loading-more states in `landing.rs` and `public_profile.rs` mod tests.
- SM-F3: `begin_initial_resets_all_state` does not assert `!m.loading_more`.
- SM-F4: `apply_more_appends_and_updates_cursor` does not cover empty-response guard.
- UI-NB1: Error test checks text but not `role="alert"`.
- UI-NB2: Route annotation at `app.rs:13` has wrong AC reference.
- CQ-A: Handler unit test checks `author.username` but not `author.display_name`.
- CQ-B: Pagination test covers `n > limit` but not `n == limit`.
- CQ-F: `hydrate.rs` EventKind expansion is framework work bundled in an application feature PR (rollback coupling risk — non-blocking, just noted).
- CQ-J: `Closure::forget()` in `hydrate.rs:473` lacks the module-level explanation present in `dom.rs`.
- CQ-K: `Resource::new` and `Resource::new_fallible` call `spawn_local` unconditionally with no API doc noting the `wasm32` restriction.

### Review status:
- Review content is posted to PR #263 as a comment (formal GitHub review not possible from PR author; comment covers full findings with blockers and non-blockers).
- `gh pr review` formal submission may still be needed if the platform permits it from a non-author — check and post if possible.

STATE at: `taskflow/overseer/I417/project_state.json`
Config seam: `taskflow/overseer/_CONFIG.yaml`

---

## Work for this step

### 1. Load governing files

Load `appfiles/REVIEW_GATE.md`, `appfiles/BOARD.md`, `appfiles/WORK_SESSION.md`, `appfiles/DELIVERABLES_GIT.md`.

### 2. Read config seam and STATE

Read `taskflow/overseer/_CONFIG.yaml` and `taskflow/overseer/I417/project_state.json`.

### 3. Confirm review is on PR #263

Check `gh pr view 263 --repo Nousix-LLC/nswe-demo --reviews` and `--comments`. If the review content is not yet on the PR in any form, post it now using the SYNTHESIS.md findings. If a formal review can be submitted, do so; otherwise the comment is sufficient.

### 4. File non-blocker issues on the board

File the 6 ⚑ flagged non-blockers as grouped board issues on `Nousix-LLC/nswe-demo`, linked to PR #263 and issue #35, labelled appropriately:
- Group CQ-H + CQ-I together as one error-message safety issue (both are `chirp-frontend/src/error.rs`, same fix area: expose status code only, log the rest).
- File CQ-C, CQ-D, CQ-E, CQ-G each as individual issues.
- For the remaining non-blockers (SM-F1 through SM-F4, UI-NB1, UI-NB2, CQ-A, CQ-B, CQ-F, CQ-J, CQ-K): group related ones (e.g. SM test gaps together, CQ minor together) and file as 2–3 issues to keep the board clean.
- Add every new issue to the GitHub project board with status Todo.
- Record all new issue numbers in STATE (append to `_CONFIG.yaml` `project_item_ids` section) and in `chirp_logged_out_goal.non_blockers_filed`.

### 5. Launch chirp-logged-out-r27 remediation DAG

Write `taskflow/dags/chirp-logged-out-r27/_FORK.md` and `taskflow/dags/chirp-logged-out-r27/_BRIEF.md`. Fork as `swe-coder`. The brief must carry:
- Both blockers verbatim (exact file + line, the wrong call, the correct call)
- The original AC list from issue #35 (all 5 ACs must still pass)
- The existing PASS verdict from `chirp-logged-out-r26` as prior context (what is already known good; do not regress it)
- Branch: `work/chirp-logged-out`
- Declared output: commits on `work/chirp-logged-out`, updated PR #263 (or new commit on the same branch), root `SYNTHESIS.md` accounting for all 5 ACs
- Constraint: no force-push; squash/fast-forward ok; leave CI green

Assign issue #35 to the authenticated `gh` user and record the DAG in STATE `dags_in_flight`.

### 6. Update STATE

Write updated STATE at `taskflow/overseer/I418/project_state.json` with:
- `review-chirp-logged-out-r1` noted in `dags_folded` (verdict: REQUEST-CHANGES — already there from I417)
- `chirp-logged-out-r27` added to `dags_in_flight`
- `free_dag_slots: 3` (1 DAG in flight)
- `chirp_logged_out_goal.current_dag` updated to `chirp-logged-out-r27 — IN-FLIGHT`
- Non-blocker issue numbers recorded once filed

### 7. Schedule next step

Schedule I419 as an evaluate step (stall check 1/4 for chirp-logged-out-r27): load `appfiles/WORK_SESSION.md` + `appfiles/BOARD.md`. Suspend I418 on a bounded wake: `+15 min from now OR chirp-logged-out-r27 forked-thread-completion`.

## Notes

- headless: true; landing_authority: delegated — read from `_CONFIG.yaml`.
- Both blockers are single-line fixes: B1 reverts a changed call, B2 corrects a URL. This is ordinary remediation; it does not consume a failure budget and does not escalate.
- After chirp-logged-out-r27 folds PASS: re-review (review-chirp-logged-out-r2), then land PR #263 and close issue #35.
- The review loop (code DAG → review DAG → remediation DAG → re-review → land) is successful engineering work throughout.
- DAG slots: 4 free as of I417 → 3 free after launching chirp-logged-out-r27.
