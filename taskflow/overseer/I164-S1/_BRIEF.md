# _BRIEF.md — NSWE overseer step I164-S1 (persona swe-lead) — REVIEW LAUNCH: security-persist-r1

**Depends on**: I164
**Task Kind**: act — load REVIEW_GATE + WORK_SESSION + DELIVERABLES_GIT; fork review DAG for PR #182; move #120 to "In Review"; update project_state.json.

## Context from I164 evaluation

- **security-persist-r1**: FOLDED with PASS. SYNTHESIS.md at `taskflow/dags/security-persist-r1/SYNTHESIS.md`.
  - PR #182 open: `work/security-persist-r1` → `main`. Closes #120.
  - Both spokes: SUBTASK_credential_hashing (commit `282707f`) and SUBTASK_ssl_manifest (commit `d5e865b`) complete.
  - All four gate checks passed.
  - CI PENDING (triggered by PR #182 open).
- **sweep-seam-r1**: Still pre-decomposition. No action needed.
- **CronJob**: Only one failure (chirp-transient-sweep-29895480, Failed). No new run yet. No bug filed.
- **ArgoCD**: OutOfSync/Healthy (annotation drift; non-blocking).
- **free_dag_slots**: 0 → rises to 1 (security-persist-r1 coder slot freed) → drops back to 0 (review slot taken).
- **Config**: landing_authority=delegated, auto_land=true, headless=true.
- **main_sha**: `9a24c281f1380644801e246b79b85f13a11cb33d`

## Work for this step

### 1. Load governing files
Load `appfiles/REVIEW_GATE.md`, `appfiles/WORK_SESSION.md`, `appfiles/DELIVERABLES_GIT.md` before forking.

### 2. Fork review DAG

Fork a **swe-reviewer** DAG at `taskflow/dags/review-security-persist-r1/` to review PR #182.

**Brief for the review DAG** — the fork's `_FORK.md` and the DAG's `_BRIEF.md` must describe:

- **Target**: PR #182 (`work/security-persist-r1` → `main`). Closes issue #120 (persistence security hardening: KDF credential storage + CronJob TLS).
- **Issue #120 acceptance criteria**:
  - Passwords/credentials hashed with argon2id (per-password fresh salt via `SaltString::generate`; `PasswordHasher::hash_password` for storage; `PasswordVerifier::verify_password` for constant-time compare — no direct `==`).
  - All credential-verify paths use `PasswordVerifier::verify_password` (not `==`).
  - CronJob `deploy/chirp/50-transient-sweep-cronjob.yaml` sets `PGSSLMODE: require` (TLS enforced).
  - No secrets or plaintext credentials in the diff.
  - All existing tests pass; new tests (if any) cover the hash/verify round-trip.
- **Code DAG SYNTHESIS.md**: `taskflow/dags/security-persist-r1/SYNTHESIS.md` — read it for the gate checks already performed.
- **Review concerns** (distinct, as REVIEW_GATE requires):
  1. *Correctness*: argon2id implementation correct — fresh salt per credential, correct use of `PasswordHasher`/`PasswordVerifier`, constant-time compare, `complete_account_recovery` updated in both `postgres.rs` and `in_memory.rs`; all acceptance criteria met.
  2. *Security*: trust-boundary review — argon2id is used everywhere a credential is stored/verified; no plaintext fallback; no hardcoded salts; `PGSSLMODE: require` enforced; no secrets in diff; no host paths, Tailscale IPs, or internal addresses committed; TLS requirement is correct and complete for the CronJob.
  3. *Code quality and design*: responsibilities clear; no duplication introduced; naming and error handling appropriate; migration script correct and idempotent-safe.
  4. *Test coverage*: existing tests exercise hash/verify round-trip; no regressions.
  5. *Rust idiom*: argon2 usage idiomatic; error handling pattern fits project style.
- **Declared output**: A posted review comment on PR #182 (verdict + findings per concern); `SYNTHESIS.md` at the review DAG root with APPROVE or REQUEST-CHANGES verdict; non-blocking findings filed as board backlog issues.
- **Config**: landing_authority=delegated, auto_land=true, headless=true. On APPROVE: land PR #182 automatically (merge to main, close #120).
- **Repo**: `Nousix-LLC/nswe-demo`. No attribution trailers on GitHub posts.

### 3. Move issue #120 to "In Review"

After forking the review DAG, move #120 to "In Progress" on the GitHub project board (no dedicated "In Review" status; use "In Progress"):
```
gh api graphql -f query='mutation { updateProjectV2ItemFieldValue(input: { projectId: "PVT_kwDOEB9jls4BlZH4" itemId: "<#120-item-id>" fieldId: "PVTSSF_lADOEB9jls4BlZH4zhkGLsc" value: { singleSelectOptionId: "47fc9ee4" } }) { projectV2Item { id } } }'
```
Find #120's project item ID first via `gh api graphql -f query='{ repository(owner: "Nousix-LLC", name: "nswe-demo") { issue(number: 120) { projectItems(first: 5) { nodes { id } } } } }'`.

### 4. Update project_state.json

Write updated project_state.json at `taskflow/overseer/I164-S1/project_state.json`:
- Move security-persist-r1 from `dags_in_flight` to a completed entry (or remove from in_flight).
- Add `review-security-persist-r1` to `dags_in_flight` (kind: review, state: RUNNING).
- Update #120 board status to "In Progress" (in review).
- free_dag_slots: 0 (one review DAG slot occupied).
- Append to `forward_series` for I165.

### 5. Write CONTINUE.md and report

Write `I164-S1/CONTINUE.md` and report terminal `status: completed, thread_evaluation: Continue, artifact_path: taskflow/overseer/I164-S1/CONTINUE.md`.

## Important notes

- No attribution trailers on anything posted to GitHub.
- The config seam is authoritative for landing_authority/auto_land/headless — re-read `_CONFIG.yaml` each iteration.
- If CI fails on PR #182 when the review folds, that is a remediation, not a re-review.
- Ferric 1.0 epics (#129–#136) are next candidate after both security/sweep issues clear.
- sweep-seam-r1 still very early; no action unless SYNTHESIS.md appears.
- CronJob: still 1 failure. File a bug referencing #117 only if a 2nd failure appears.

## Schedule

- **I165** (depends_on I164-S1): next evaluating iteration.
