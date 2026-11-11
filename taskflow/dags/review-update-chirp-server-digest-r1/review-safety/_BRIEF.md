# _BRIEF.md — review-digest-r1-safety

**Kind**: review concern (atomic)  
**Concern**: Deployment Safety  
**Parent DAG**: review-update-chirp-server-digest-r1

---

## Objective

Assess whether PR #209's manifest change is safe to deploy: the change is minimal (image field only,
no config drift), the manifest is valid Kubernetes YAML, and there are no blocking rollout concerns
from schema migrations in the commits between the previous digest (`adaa4c26`) and the new one
(`f845ca8c`).

---

## Scope

**Changed file**: `deploy/chirp/10-deployment.yaml`  
**Branch**: `deploy/update-chirp-server-digest-d8230fea` → `main`  
**Repo**: `Nousix-LLC/nswe-demo`

What to establish:
1. **Config drift**: The only lines that changed are the image comment and the image reference.
   No replica count, resource limit, env var, volume mount, probe, securityContext, or any other
   field was modified.
2. **Manifest validity**: The resulting YAML is valid Kubernetes syntax and the deployment spec
   remains well-formed.
3. **Migration concerns**: Identify any database schema migrations merged to `main` between commit
   `0d5917dc` (previous image, run 41687555341) and commit `d8230fea917dc1228fbb5ccd72bcb7ea79d0bed3`
   (new image). For each migration found, determine whether it requires a coordinated rollout
   (e.g., a backward-incompatible schema change that would break the previous binary during a
   rolling update).

Evidence sources:
- PR #209 diff: `gh pr diff 209 --repo Nousix-LLC/nswe-demo`
- Full manifest on the PR branch via GitHub API or `gh api`
- Merged PRs on `main` between the two commits (look for migrations/ directories, SQL files, or
  migration-related commit messages): `gh pr list --repo Nousix-LLC/nswe-demo --state merged` and
  the commit log between `0d5917dc` and `d8230fea`

---

## Declared Output

`taskflow/dags/review-update-chirp-server-digest-r1/review-safety/FINDINGS.md`

Format: per `taskflow/dags/review-update-chirp-server-digest-r1/contracts/_MANIFEST.yaml`
- `## Verdict` — PASS or FAIL
- `## Evidence` — what was read; which fields were compared; which migrations (if any) were found
  and their assessment
- `## Findings` — None, or a list (blocker if config drift found or if a migration requires
  coordinated rollout that this rolling-update strategy does not satisfy)

---

## Success Criteria

The concern is satisfied (PASS) when: the diff touches only the image field (3 lines: comment × 2
+ image reference); the manifest is valid YAML; and no migration in the gap requires a coordinated
rollout that the current RollingUpdate (`maxUnavailable: 0`, `maxSurge: 1`) strategy cannot provide.
