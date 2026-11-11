# _BRIEF.md — NSWE overseer step I318 (persona swe-lead) — ACT: watch chirp-logged-out-r6 (4th check — STALL CONFIRMATION threshold)

**Depends on**: I317
**Task Kind**: act — load `appfiles/BOARD.md` and `appfiles/DEPLOYMENT.md`.

## Context from I317

chirp-logged-out-r6 3rd check (I317): **STALL CONCERN CONFIRMED** — still only _FORK.md, no child tasks, no SYNTHESIS.md.
- stall_concern: true (3rd check threshold reached)
- Stall progress update comment posted on issue #35: https://github.com/Nousix-LLC/nswe-demo/issues/35#issuecomment-6676638942
- ArgoCD: OutOfSync/Healthy/cb1ced3 — same benign StatefulSet drift only. Unchanged.
- #35 confirmed OPEN/In Progress.
- No PR on work/chirp-logged-out (expected — r6 has not decomposed).

STATE at: `taskflow/overseer/I317/project_state.json`
Config seam: `taskflow/overseer/_CONFIG.yaml`

## Stall schedule for chirp-logged-out-r6

- DAG process: chirp-logged-out-r6
- 1st check (I315 — DONE): no concern.
- 2nd check (I316 — DONE): no concern.
- 3rd check (I317 — DONE): stall_concern: true. Comment posted on #35.
- **4th check (I318 — this iteration): STALL CONFIRMATION — re-fork as r7 if still no child tasks.**

## Work for this step

### 1. Load governing files

Load `appfiles/BOARD.md` and `appfiles/DEPLOYMENT.md`.

### 2. Check chirp-logged-out-r6 DAG (4th check — STALL CONFIRMATION)

Check if `taskflow/dags/chirp-logged-out-r6/SYNTHESIS.md` now exists. Also count the files in
`taskflow/dags/chirp-logged-out-r6/` to see if child tasks exist.
- If SYNTHESIS.md exists: read it, record verdict (PASS or FAIL), plan next step:
  - PASS: check if PR was opened on branch `work/chirp-logged-out` via
    `gh pr list --repo Nousix-LLC/nswe-demo --head work/chirp-logged-out`. If PR exists, dispatch review
    DAG (swe-reviewer). If no PR yet, check for the branch push.
  - FAIL: dispatch chirp-logged-out-r7 (swe-coder) remediation carrying blockers from SYNTHESIS.md.
- If not: check if child tasks have appeared (DAG in progress). Note state.

**4th check — STALL CONFIRMATION threshold.** If still only _FORK.md (no child tasks, no SYNTHESIS.md):
- **STALL CONFIRMED** — read the goal from r6's _FORK.md at `taskflow/dags/chirp-logged-out-r6/_FORK.md`
  to carry the acceptance criteria forward.
- Re-fork as chirp-logged-out-r7 (swe-coder) on branch work/chirp-logged-out, issue #35.
- Post a stall re-fork comment on issue #35:
  `gh issue comment 35 --repo Nousix-LLC/nswe-demo --body "..."` noting work is continuing with a fresh
  implementation attempt. Keep comment factual and product-facing.
- Record stall of r6 and dispatch of r7 in STATE.
- Schedule I319 (+20 min) to begin watching chirp-logged-out-r7 (1st check — no concern).

If child tasks DID appear (DAG has decomposed and is working): record stall_concern: false (concern cleared),
note DAG is progressing, and schedule I319 (+20 min) to continue watching.

### 3. ArgoCD deployment re-check

Re-check ArgoCD sync status:
  `kubectl --context k3d-nswe -n argocd get application chirp -o jsonpath="{.status.sync.status},{.status.health.status},{.status.sync.revision}"`
- If OutOfSync only on chirp-postgres StatefulSet: same benign drift as before — note and continue.
- If new resources OutOfSync: investigate.
- If Synced+Healthy on cb1ced3: record as fully synced.

### 4. Board spot-check

- Confirm #35 still In Progress.
- Check if any PR appeared on `work/chirp-logged-out`: `gh pr list --repo Nousix-LLC/nswe-demo --head work/chirp-logged-out`

### 5. Update STATE

Write updated STATE at `taskflow/overseer/I318/project_state.json`.

### 6. Schedule next step

Schedule I319 (+20 min) to continue watching (either r6 if progressing, or r7 if stall was confirmed and
re-fork was dispatched).

## Notes

- Landing authority: delegated (`auto_land: true`, `headless: true`).
- ArgoCD has auto-sync (selfHeal: true, prune: true). Currently at cb1ced3 (PR #193). OutOfSync status is
  benign StatefulSet drift only.
- chirp-logged-out-r6 was dispatched I314. 1st check I315 (no concern). 2nd check I316 (no concern).
  3rd check I317 (stall_concern: true, comment posted). 4th check I318 (this — STALL CONFIRMATION → re-fork as r7).
- Previous stalls: chirp-logged-out (I298, 6 checks), r2 (I302, 4 checks), r3 (I306, 4 checks), r4 (I310,
  4 checks), r5 (I314, 4 checks).
- r6 DAG process ID: chirp-logged-out-r6
- r7 DAG process ID to use: chirp-logged-out-r7
- When re-forking as r7: read the goal from r6's _FORK.md at `taskflow/dags/chirp-logged-out-r6/_FORK.md`
  to carry the acceptance criteria forward. Issue #35 is the target. Branch: work/chirp-logged-out.
- Stall comment on issue #35: Post at I318 when stall CONFIRMED and re-fork dispatched.
