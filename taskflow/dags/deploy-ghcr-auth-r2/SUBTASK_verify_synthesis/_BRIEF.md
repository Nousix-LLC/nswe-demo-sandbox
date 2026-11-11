# _BRIEF.md — SUBTASK_verify_synthesis (deploy-ghcr-auth-r2)

## Task Specification
**Slug**: SUBTASK_verify_synthesis
**Task Kind**: synthesis
**Status**: Pending

### Objective
Act as the **verification gate** for the subtree: confirm, with **executed** checks against the fresh live world,
whether Chirp is reachable on its committed digest and reconciled with the committed GitOps desired state — render
the AC1–5 verdict, finalize the issue-#32 disposition, and author the root `SYNTHESIS.md`. This is a gate, **not a
prose summary**: it runs the identity checks and either asserts coverage (PASS) or records a clean FAIL with the
precise external input still required.

### Context
Part of `deploy-ghcr-auth-r2` (see `../_GLOBAL.md`). This is the **judge** stage of diagnose → remediate →
verify/synthesize, and the hub that produces the subtree's single required deliverable. It owns the verdict (the
change/verify split keeps the verdict out of `SUBTASK_remediate`) and the `Closes #32` decision.

**Dependencies**: `SUBTASK_diagnose`, `SUBTASK_remediate`.

## Input Specification
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree context | `../_GLOBAL.md` | Scope, constraints, AC1–5 |
| Contract (identities to assert) | `../contracts/_MANIFEST.yaml` (read-only) | The identity set you MUST enumerate and run — AC1–5 made runnable + supply-chain invariants |
| Diagnosis | `../SUBTASK_diagnose/diagnosis.md` | The branch and the baseline live state |
| Remediation record | `../SUBTASK_remediate/remediation.md` (+ any PR) | What was changed (or why not / why blocked) |
| Host/cluster access | the repo checkout's `CLAUDE.md` | How to reach the cluster to run the live checks |
| Prior verdict | `../../deploy-ghcr-auth/SYNTHESIS.md` | The attempt-#1 FAIL verdict format and ruled-out paths (do not re-tread) |

## Process (approach — not a runbook)
Run the gate as a verification gate: **enumerate every identity in `../contracts/_MANIFEST.yaml` and execute its
`check` against the real, post-remediation live world** — do not sample, do not assert from prose, do not silently
plug a failure. Specifically, verify live (not merely that manifests applied): the committed-digest pod is
`1/1 Ready` and the stale RS is at 0 (I1, I6); ArgoCD `chirp` is Synced **and** Healthy at the integration-branch
head (I2); `GET /healthz` returns 200 from the **digest** pod through the ingress at **both** routes — the owner's
host-less route and `chirp.localhost` (I3); the fix survives a selfHeal/prune reconcile (I4); the supply-chain
posture is intact — digest pin unchanged, no secret in git, AppProject scope unchanged, no broad RBAC (I5); and no
host facts reached GitHub (I7). Record each as a runnable check with its result.

Then set the disposition:
- **PASS (reachability achieved + verified)** — if a PR exists, finalize its body to carry a plain-text `Closes #32`
  line; if no repo change was needed, note that #32 is satisfied by the live reconcile and how the overseer should
  close it. 
- **FAIL / blocked** — leave #32 open, state exactly why, and name the precise external input still required and
  where the system expects it (clean recorded verdict, not an open-ended wait; mirror the attempt-#1 clean-FAIL form).

If any identity FAILS in a way that is remediable within scope (not an external-credential block), prefer scheduling
a remediation fix-task via plan amendment over silently passing — but a credential block is reported as a clean FAIL,
not a defect.

## Output Specification
**Primary output**: `SYNTHESIS.md` authored at the **subtree root** (`../SYNTHESIS.md`, i.e.
`taskflow/dags/deploy-ghcr-auth-r2/SYNTHESIS.md`) — this is the fold location and the overseer's observation seam.
It MUST state: what is deployed at which commit; the AC1–5 results (each with its executed-check evidence); **how it
was verified live** (synced, healthy, the endpoint answering from the digest pod at both routes, a smoke test — not
merely that manifests applied); the issue-#32 disposition and the PR link/line if any; and any external input still
required (what it is and precisely where the system expects to find it). As the synthesis task, author this one
record at the fold location (it is both your terminal record and the fold record) and fold the parent via the
synthesis→resume path; write no separate duplicate.

## Success Criteria
- [ ] Every `../contracts/_MANIFEST.yaml` identity enumerated and **executed** against the live world; results
      recorded with evidence; no silent plugs.
- [ ] Live verification is genuine (endpoint answered from the **digest** pod at both ingress routes; Synced+Healthy
      confirmed) — not "manifests applied".
- [ ] AC1–5 verdict explicit; disposition set (PASS → `Closes #32` on the PR / note for no-PR case; FAIL/blocked →
      #32 left open with the precise external input named).
- [ ] `SYNTHESIS.md` present at the subtree root, self-contained, carrying no host/system facts fit for GitHub where
      it quotes anything PR-bound.
- [ ] On FAIL: clean recorded verdict (not an open-ended wait), external input named precisely.

## Suggested Methodology Files
This child is a **verification gate** (per `../_GLOBAL.md` posture and the loader's SYNTHESIS-task default).
Parent's Domain-Mapping reading: *"Synthesizing / verifying a hub-and-spoke decomposition (contract + wiring + review
gate)"* → **Synthesis** (primary); live-verification support from **GitOps** + **Kubernetes**; PR finalize from
**Operations** / **Code Review**.
- `synthesis/Synthesis_Overview_Methodology.md` — **anchor, read first**: the four-check gate model and the structured `SYNTHESIS.md` schema.
- `synthesis/Synthesis_Contract_Verification_Methodology.md` — enumerate the frozen identities and run each check (the gate-time inverse of this subtree's contract).
- `synthesis/Synthesis_Wiring_Verification_Methodology.md` — confirm the fix is actually wired live (the endpoint really serves from the digest pod), not detached/dead.
- `synthesis/Synthesis_Remediation_Methodology.md` — if a non-blocked identity fails, schedule remediation as a fix-task rather than passing.
- `gitops/GitOps_Reconciliation_And_Drift_Control_Methodology.md` — assert Synced+Healthy and selfHeal survival correctly.
- `kubernetes/K8s_Networking_And_Service_Connectivity_Methodology.md` — verify ingress/endpoint serving at both routes.
- `operations/GitWorkflow_PR_Lifecycle_Methodology.md` — finalize the PR body / `Closes #32` wording.

*The gate posture is mandatory; which sibling check files you load and how deeply you run each check is your
judgment. Read the Overview first, then load the check/remediation files your reading of the subtree reveals you
need.*

## Inherited Constraints
- Run checks; never silently plug a failing identity.
- `Closes #32` only if live reachability is **actually achieved and verified**; otherwise #32 stays open with the reason.
- Scope limited to `chirp*` namespaces and ArgoCD Application `chirp`.
- No host/system facts in anything that reaches GitHub (PR body/comments); translate to repository identities.
- No `main` force-push/history rewrite; no attribution trailers; no secret in git.

## Out-of-Scope Methodologies
- `decomposition/*` — decomposer-side only; a synthesis gate never loads it (synthesis is the reassembly, not the split).
