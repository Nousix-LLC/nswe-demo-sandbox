# _BRIEF.md — NSWE overseer step I233 (persona swe-lead) — ACT: launch review DAG for PR #209 (devops: chirp-server image digest)

**Depends on**: I232
**Task Kind**: act — load `appfiles/REVIEW_GATE.md`, `appfiles/WORK_SESSION.md`, `appfiles/DEPLOYMENT.md`.

## Context from I232 (EVALUATE: devops DAG folded, machine gate PASS)

- **Devops DAG update-chirp-server-digest-r1**: FOLDED — COMPLETED
  - PR #209 created: `deploy/update-chirp-server-digest-d8230fea` → `main`
  - Change: `deploy/chirp/10-deployment.yaml` image updated sha256:adaa4c26 → sha256:f845ca8c (d8230fea build, CI run 41803200262 on main merge commit)
  - CI on PR #209: all 6 PASS (run 41806003677) — fmt, clippy, test, wasm, doc, image — all SUCCESS
  - PR #209 MERGEABLE
  - **Machine gate: PASS**
- **Issue #206**: chirp-server image digest update — board item `PVTI_lADOEB9jls4BlZH4zhF7WNw`
- **STATE**: `taskflow/overseer/I232/project_state.json`
- **Config seam**: `taskflow/overseer/_CONFIG.yaml`
- Escalation ferric-async-forms STILL ACTIVE — do NOT launch ferric-async-forms-r3

## Work for this step

### 1. Load governing files

Load `appfiles/REVIEW_GATE.md`, `appfiles/WORK_SESSION.md`, `appfiles/DEPLOYMENT.md`. Read `_CONFIG.yaml` and `taskflow/overseer/I232/project_state.json`.

### 2. Launch review DAG for PR #209

Write `taskflow/dags/review-update-chirp-server-digest-r1/_BRIEF.md` and `taskflow/dags/review-update-chirp-server-digest-r1/_FORK.md`, then fork as `swe-reviewer` (launch_agent).

**Review brief must describe:**

- **Target**: PR #209 (`deploy/update-chirp-server-digest-d8230fea` → `main`, repo `Nousix-LLC/nswe-demo`), issue #206 (chirp-server image digest update to d8230fea build)
- **Change**: `deploy/chirp/10-deployment.yaml` — chirp-server image updated from `ghcr.io/nousix-llc/chirp-server@sha256:adaa4c26...` to `ghcr.io/nousix-llc/chirp-server@sha256:f845ca8c29408fd27d0fc3a6ff3f0f0d661d17ffd63b6427dcceb5b6845f044f`
- **Code DAG SYNTHESIS**: `taskflow/dags/update-chirp-server-digest-r1/SYNTHESIS.md` — confirms digest from CI run 41803200262 for commit d8230fea
- **CI on PR #209**: all 6 PASS (run 41806003677 — fmt, clippy, test, wasm, doc, image)
- **Review concerns** (devops PR — include deployment/ops concerns per REVIEW_GATE):
  - *Correctness*: Does the pinned digest (`sha256:f845ca8c...`) match the image produced by CI run 41803200262 for commit d8230fea917dc1228fbb5ccd72bcb7ea79d0bed3? Is the image reference format correct?
  - *Deployment safety*: Is this a minimal, safe manifest change — no unintended resource changes, replica count drift, env var changes, or other config drift beyond the image field?
  - *Ops*: Are the commit message, PR description, and closing reference (#206) appropriate? Does the change follow the project's digest-pinning convention?
  - *Security*: Does the diff contain any host paths, tailnet/LAN addresses, internal infrastructure details, internal server URLs (100.x addresses), or secrets? None should appear in committed files.
- **Declared output**: Posted review (or comment if platform self-approval blocks), root `SYNTHESIS.md` with APPROVE or REQUEST-CHANGES verdict, any non-blocking findings filed as board issues

### 3. Update board: issue #206 → In Progress

Update board item `PVTI_lADOEB9jls4BlZH4zhF7WNw` to status "In Progress":

```
gh api graphql -f query='mutation { updateProjectV2ItemFieldValue(input: { projectId: "PVT_kwDOEB9jls4BlZH4" itemId: "PVTI_lADOEB9jls4BlZH4zhF7WNw" fieldId: "PVTSSF_lADOEB9jls4BlZH4zhkGLsc" value: { singleSelectOptionId: "47fc9ee4" } }) { projectV2Item { id } } }'
```

### 4. Update STATE

Write `taskflow/overseer/I233/project_state.json`:
- Move `update-chirp-server-digest-r1` from `dags_in_flight` to `dags_folded` (verdict: COMPLETED, machine_gate: PASS, pr: 209, ci_run: 41806003677)
- Add `review-update-chirp-server-digest-r1` to `dags_in_flight` (kind: review, goal: review PR #209 devops chirp-server image digest update, issues: ["#206"], launch_agent: swe-reviewer, forked_in: overseer/I233)
- Add PR #209 to `prs` (status: OPEN, branch: `deploy/update-chirp-server-digest-d8230fea`, machine_gate: PASS, ci_run: 41806003677, all 6 PASS, issues: ["#206"])
- Update board note
- Update forward_series entry for I233: "ACT — DONE. review-update-chirp-server-digest-r1 forked (swe-reviewer). Board #206 → In Progress."

### 5. Schedule I234

I234: EVALUATE — load `appfiles/REVIEW_GATE.md`, `appfiles/WORK_SESSION.md`, `appfiles/DELIVERABLES_GIT.md`.
Fold review DAG `review-update-chirp-server-digest-r1` result for PR #209.
- If review APPROVE: land PR #209, update board #206 → Done, record work_item in STATE, check deployment, then assess next code goal #132 HTTP Client.
- If review REQUEST_CHANGES: assess blockers, remediate within budget (attempt 1 of 2), or escalate.

Self-suspend after forking the review DAG, waiting on forked-thread-completion (review-update-chirp-server-digest-r1) + 20-minute timer.

## Notes

- Config: `landing_authority: delegated`, `auto_land: true`, `headless: true` → land on APPROVE without human gate
- Do NOT launch ferric-async-forms-r3 (escalation ACTIVE)
- After PR #209 lands: deployment check will confirm ArgoCD syncs and pod restarts on new image
- Next code goal after #206 Done: #132 HTTP Client (Ferric 1.0) — depends on #131 (LANDED ✓) and #129 (LANDED ✓)
- issue_206 board item: `PVTI_lADOEB9jls4BlZH4zhF7WNw`
- PR #209: https://github.com/Nousix-LLC/nswe-demo/pull/209
