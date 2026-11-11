# _BRIEF.md — NSWE overseer step I414 (persona swe-lead) — ACT: launch review DAG for PR #263

**Depends on**: I413

**Task Kind**: act — load `appfiles/REVIEW_GATE.md` and `appfiles/WORK_SESSION.md`.

## Context from I413

I413: r26 folded PASS. PR #263 is ready for review.

- **r26 verdict**: PASS — all 5 ACs met, CI 6/6 green
- **SYNTHESIS.md**: `taskflow/dags/chirp-logged-out-r26/SYNTHESIS.md` (PASS)
- **PR #263**: OPEN/MERGEABLE, head `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- **Branch**: `work/chirp-logged-out`
- **Issue**: #35 ("Logged-out reading and a useful landing with accurate states")
- **Free DAG slots**: 4

STATE at: `taskflow/overseer/I413/project_state.json`
Config seam: `taskflow/overseer/_CONFIG.yaml`

---

## Work for this step

### 1. Load governing files

Load `appfiles/REVIEW_GATE.md` and `appfiles/WORK_SESSION.md`.

### 2. Read config seam and STATE

Read `taskflow/overseer/_CONFIG.yaml` and `taskflow/overseer/I413/project_state.json`.

### 3. Launch review DAG

Fork a `swe-reviewer` DAG to review PR #263. The review DAG's brief should cover:

**Objective**: Review PR #263 (`work/chirp-logged-out`, head `decb6196c2c1e6ed421d393a642f0c844cc333ba`)
against issue #35's acceptance criteria and the codebase quality bar.

**What to evaluate**:
- AC-1: Public timeline + user profiles accessible without login (no auth extractor on `GET /api/chirps` and `GET /api/users/{username}/chirps`; no redirect from `/` or `/@:handle`)
- AC-2: Clear landing with sign-up prompt on empty state (empty_view in `crates/chirp-frontend/src/landing.rs`)
- AC-3: Clear recoverable error message on timeline load failure (error_banner with role=alert + Retry)
- AC-4: "Create an account" route visible on landing AND sign-in screen (nav_bar, header_nav, sign_in_view)
- AC-5: Loading, empty, error, end-of-list states accurate and distinct (all 7 state branches in view_tree + footer; same for public_profile)
- Code quality: correctness, test coverage, security (no SSRF, no auth bypass), API contracts
- No regressions in existing authenticated flows

**Inputs**:
- PR: `Nousix-LLC/nswe-demo` #263
- Issue: `Nousix-LLC/nswe-demo` #35
- Code machine verdict: PASS (r26, CI 6/6 green, all 5 ACs confirmed by r26 SYNTHESIS.md)
- Branch: `work/chirp-logged-out` at `decb6196c2c1e6ed421d393a642f0c844cc333ba`

**Declared output**: Review verdict (APPROVE or REQUEST-CHANGES), review posted on PR #263, non-blocking findings listed for board filing, `SYNTHESIS.md` at review DAG root.

**Constraints**: Repo `Nousix-LLC/nswe-demo` only. Do not force-push. Post review to PR #263.

### 4. Update STATE

Write updated STATE at `taskflow/overseer/I414/project_state.json` recording:
- Review DAG forked (slug: `review-chirp-logged-out-r1`, workspace: `taskflow/dags/review-chirp-logged-out-r1/`)
- dags_in_flight: [review-chirp-logged-out-r1]
- free_dag_slots: 3

### 5. Schedule next step

Schedule I415 as stall check 1/4 for review-chirp-logged-out-r1 (kind: evaluate; loads WORK_SESSION + BOARD).
Suspend I414 on a bounded wake: `+15 min from now OR review-chirp-logged-out-r1 forked-thread-completion`.

## Notes

- headless: true; landing_authority: delegated — read from `_CONFIG.yaml`.
- DAG slots: 4 free.
- PR #263 is MERGEABLE and CI-green; the review DAG is the next gate before landing.
