# COMPLETE — failure-handler callback for `deploy-ghcr-auth`

**Handler task: COMPLETED.** The `TaskFailed` of DAG `deploy-ghcr-auth` (F1 of #29) was diagnosed and a
handling disposition produced.

- **Evaluation:** Atomic (one responsibility — diagnose the failure and decide the disposition).
- **Disposition:** **ESCALATE — not autonomously recoverable.** No remediation task was amended into the
  plan, because the sole blocker is a non-schedulable external/human action (provision a `read:packages`
  credential for `nousix-llc/chirp-server`, or an org-admin package-visibility flip). A scheduled in-sandbox
  task could not fix it: it would re-tread the documented dead ends, and the only in-sandbox alternative
  (GitOps-managed secret) is out of scope (#24). The fork design (`_FORK.md`: `reap-whole-after-land`) routes
  recovery through the overseer re-forking a fresh DAG once the credential exists.
- **Failed node:** remains TERMINAL and IMMUTABLE (not revived). No dependents to reroute — `deploy-ghcr-auth`
  is a scratch forked-root DAG the overseer observes only via its `SYNTHESIS.md` seam.

**Deliverable:** `ESCALATION.md` (this workspace) — full diagnosis, the recoverability test, the one
unblocking action, and the recommended overseer/human recovery path (supply credential → re-fork fresh DAG
→ verify AC1–4 via PR #30 runbook → land PR #30 → close #29).

**Action required of overseer/human:** supply a least-privilege `read:packages` credential (or flip the GHCR
package public), then re-fork `deploy-ghcr-auth`. Until then, **#29 stays open**.
