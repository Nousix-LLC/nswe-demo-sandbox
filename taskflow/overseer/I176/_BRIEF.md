# _BRIEF.md — NSWE overseer step I176 (persona swe-lead) — ACT: launch review for PR #183

**Depends on**: I175
**Task Kind**: act — load REVIEW_GATE + WORK_SESSION; fork swe-reviewer DAG for PR #183.

## Context from I175

- **sweep-seam-r1-r1** (remediation DAG, swe-coder): FOLDED PASS. COMPLETE.md at `taskflow/dags/sweep-seam-r1-r1/COMPLETE.md`.
- **PR #183** (`work/sweep-seam-r1`): all CI checks SUCCESS (fmt ✓, clippy ✓, test ✓, wasm ✓, doc ✓, image ✓). mergeStateStatus: CLEAN. mergeable: MERGEABLE.
  - Machine gate: **PASS** — PR #183 is ready for review.
- **free_dag_slots**: 1 (sweep-seam-r1-r1 folded).
- **ArgoCD**: OutOfSync/Healthy at `c3f9f558` — cosmetic postgres StatefulSet drift, non-blocking.
- **project_state.json**: `taskflow/overseer/I164-S1/project_state.json`
- **_CONFIG.yaml**: `taskflow/overseer/_CONFIG.yaml`
- **main_sha**: `c3f9f558fc7b254c2b0d431c31a7fc9a095fe0d5`
- **landing_authority**: delegated, auto_land: true, headless: true

## Work for this step

### 1. Load governing files
Load `appfiles/REVIEW_GATE.md` and `appfiles/WORK_SESSION.md` before acting.

### 2. Read the config seam
Read `taskflow/overseer/_CONFIG.yaml`.

### 3. Launch the review DAG for PR #183
Per REVIEW_GATE: write the review brief and fork a `swe-reviewer` DAG.

**What to cover in the review brief**:
- PR: #183 (`work/sweep-seam-r1`) — "fix(#117): replace psql sweep CronJob with chirp-server sweep subcommand"
- Issue closed: #117 "Replace psql-based sweep CronJob with Rust-implemented sweep endpoint/subcommand"
- Branch: `work/sweep-seam-r1` (rebased onto `c3f9f558`, commit `5dcb72f`)
- Code DAG verdict: PASS (all 6 functional ACs met per sweep-seam-r1 SYNTHESIS.md)
- Remediation verdict: PASS (fmt + rebase fixed, all CI green per sweep-seam-r1-r1 COMPLETE.md)
- Goals of review: correctness, test coverage, code quality, design conformance (does the implementation match the stated approach of invoking the Rust sweep subcommand rather than raw psql?), security (no credentials in manifests, TLS requirements met in connection string), manifest hygiene (CronJob updated correctly).

DAG workspace: `taskflow/dags/review-sweep-seam-r1/`
Launch agent: `swe-reviewer`

### 4. Update STATE and write CONTINUE.md

After fork:
- Update project_state.json: add review DAG to dags_in_flight, update PR #183 to include review_dag slug.
- Schedule I177 (board check) to watch for review fold.

Dispatch logic for I177 (the board check that follows):
- If review DAG folded APPROVE + no blockers: schedule "process review + land" tasks.
- If review DAG folded REQUEST-CHANGES: schedule remediation.
- If still running: bounded wake (5–10 min or DAG fold), re-check.

## Important notes

- landing_authority: delegated, auto_land: true, headless: true (from _CONFIG.yaml).
- After review APPROVE + machine PASS: land PR #183 automatically (no human gate needed).
- The review brief must name the PR by number and the branch by name, with the commit SHA. It must NOT include host paths, internal addresses, or taskflow internals.
- After merge, a deployment check is needed (ArgoCD will sync new image to k3s cluster).
- Remediation budget: 2 total attempts; 1 used. Budget remaining: 1 (if review finds blockers).
