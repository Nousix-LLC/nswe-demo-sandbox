# Task: SSL Manifest Hardening — CronJob PGSSLMODE: require

## Task Specification

**Slug**: SUBTASK_ssl_manifest  
**Task Kind**: standard  
**Depends on**: SUBTASK_credential_hashing  
**Status**: Pending  
**Assigned To**: swe-coder

### Objective

Change `PGSSLMODE: disable` to `PGSSLMODE: require` in the chirp sweep CronJob manifest
(`deploy/chirp/50-transient-sweep-cronjob.yaml`), update the now-stale comment that called TLS
"a documented hardening follow-up", commit to `work/security-persist-r1`, and push.

### Context

This is spoke 2 of 3 in the `security-persist-r1` subtree (see parent `_GLOBAL.md`). Issue #120
(PR #113 review follow-up) identifies that the sweep CronJob sends the DB password over the pod
network in plaintext because `PGSSLMODE: disable` is set explicitly. This spoke owns the manifest
fix. The dependency on `SUBTASK_credential_hashing` is for **git sequencing only** (both spokes
commit to the same branch; running them concurrently would create push conflicts).

**Dependencies**: `SUBTASK_credential_hashing` (git ordering — branch must exist)  
**Dependents**: `SUBTASK_synthesis`

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Repository facts, branch name, constraints |
| SUBTASK_credential_hashing COMPLETE.md | `../SUBTASK_credential_hashing/COMPLETE.md` | Confirms branch exists; git SHA to base the commit on |
| CronJob manifest | `deploy/chirp/50-transient-sweep-cronjob.yaml` | File to modify (PGSSLMODE at line ~103) |
| Issue #120 | GitHub issue (read via gh CLI) | Acceptance criteria for this fix |

All inputs are on the build server at `~/nswe-demo`. Access via:
```bash
ssh -i ~/.ssh/nousix_server_ed25519 -o IdentitiesOnly=yes -o BatchMode=yes mattm@100.90.75.93 'bash -lc "..."'
```

---

## Process

1. **Confirm branch exists** — read `../SUBTASK_credential_hashing/COMPLETE.md` for the pushed SHA.
2. **Pull latest** from `origin/work/security-persist-r1` to ensure the commit is local on the build server.
3. **Edit the manifest** `deploy/chirp/50-transient-sweep-cronjob.yaml`:
   - Change `value: disable` under `PGSSLMODE` → `value: require`
   - Update the adjacent comment that says "TLS in transit is a documented hardening follow-up" — this IS that follow-up; update the comment to say TLS is now required.
4. **Commit** with message `fix(security): require TLS for CronJob DB connection — PGSSLMODE require (#120)`
5. **Push** to `origin/work/security-persist-r1`

### Quality criteria

- `PGSSLMODE: disable` must not appear anywhere in `deploy/` after this change
- The updated comment must be accurate (no longer a "follow-up", now implemented)
- Commit message references `#120`
- Manifest must still apply cleanly (dry-run is optional but encouraged)

---

## Output Specification

### Primary Output

| Attribute | Value |
|-----------|-------|
| File | `COMPLETE.md` |
| Location | `SUBTASK_ssl_manifest/` |

### COMPLETE.md contents

Record:
- Exact diff applied (file, lines changed)
- Git commit SHA pushed
- Any validation performed (e.g. kubectl dry-run)

---

## Success Criteria

- [ ] `PGSSLMODE: disable` absent from the CronJob manifest
- [ ] `PGSSLMODE: require` present in its place
- [ ] Stale comment updated to reflect the change is live
- [ ] Commit pushed to `origin/work/security-persist-r1`
- [ ] `COMPLETE.md` authored at this task's workspace

---

## Suggested Methodology Files

**Task type match**: "Kubernetes configuration & secrets (ConfigMaps/Secrets, Helm vs Kustomize)" → primary: `kubernetes`, supporting: `security`; also "Security review" → primary: `security`, supporting: `code-review`

**Specific files to load**:
- `kubernetes/K8s_Configuration_Management_Methodology.md` — ConfigMap/Secret patterns, environment variable injection in Pods, and manifest hygiene. **Rationale**: the fix is a Kubernetes manifest env-var change; methodology covers how to structure env vars in a CronJob spec and what to watch for in Secret references.
- `security/Security_Secure_Coding_Methodology.md` — transport layer TLS posture. **Rationale**: this fix closes the plaintext-DB-password-in-transit finding; the methodology covers TLS-in-transit requirements for internal service-to-service connections.

*These are the parent's flagged methodologies based on the task type. The child agent SHOULD load these as a starting point but is the final judge of what its work requires — load fewer if some are clearly inapplicable; load more if the child's own reading of the brief reveals additional methodology surface the parent did not anticipate.*

## Inherited Constraints

- Do NOT modify any other manifest file or application code.
- Branch is `work/security-persist-r1` — do not create a new branch.
- Commit message convention: `fix(security): ...` prefix; reference `#120`.
- Never force-push to `main`.
- The DB credential is out-of-band and not in the repository; do not commit it.

## Out-of-Scope Methodologies

- `K8s_Storage_And_Stateful_Workloads_Methodology.md` — the PostgreSQL StatefulSet storage is not being touched.
- `K8s_Operators_And_CRDs_Methodology.md` — no CRD or operator work.
- The server-leg SSL posture (`CHIRP_DATABASE_URL`) is out of scope — it is an out-of-band secret not in the tree.
