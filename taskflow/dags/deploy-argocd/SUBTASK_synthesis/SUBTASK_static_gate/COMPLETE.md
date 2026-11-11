# COMPLETE — SUBTASK_static_gate

**Task**: Static verification gate over the combined deploy-argocd manifests (pre-cluster GO/NO-GO).
**Evaluation**: Atomic. **Status**: completed. **Date**: 2026-10-08.

## What was done
Ran the static half of the deploy verification gate, read-only over the COMPLETED sibling outputs
(`deploy/chirp/*` from `SUBTASK_app_manifests`, `deploy/argocd/*` from `SUBTASK_argocd_gitops`), asserting
each statically-checkable parent-contract identity against the real manifest text with concrete evidence,
plus the static halves of the runtime identities, wiring, duplication, and a focused review.

## Result — STATIC GO
- **Assigned static identities (4/4 PASS)**: `image-pinned-by-digest`, `resources-and-probes`,
  `appproject-least-privilege`, `namespace-isolation-no-secrets` — each with file:line / value-compared evidence; no silent plug.
- **Static halves of runtime identities (3/3 consistent/PASS)**: `service-selector-matches-pods` (selector ⊆ pod
  labels; targetPort 8080 == container_listen_port), `ingress-wires-service` (backend → Service name/port 80; class traefik),
  `argocd-application-wired` (path deploy/chirp, repo nswe-demo, dest ns chirp, project chirp ≠ default). Runtime proof → `SUBTASK_deploy_reach`.
- **Wiring**: PASS — connected graph, no dead/orphan manifest.
- **Duplication**: PASS — one producer per owned path; deploy/chirp vs deploy/argocd disjoint; mirror byte-identical to canonical.
- **Review**: k3s/Traefik + ArgoCD idiom correct; security posture strong (PSA restricted, non-root 65532, digest-pinned, least-priv AppProject, no committed secrets).
- **Non-blocking runtime notes carried to deploy_reach/fold**: R1 out-of-band `ghcr-pull` Secret must exist at
  rollout; R2 `targetRevision: main` vs pre-merge test ordering (#23 HSO-1); R3 default SA with token mount disabled.
- **No static FAIL → no remediation fix-task injected.**

## Verification against success criteria
- [x] Every assigned static identity has a recorded PASS/FAIL with concrete evidence — no silent plug.
- [x] Static halves of the runtime identities recorded; wiring + duplication checks recorded.
- [x] Focused review note + unambiguous overall static GO/NO-GO present.
- [x] No cluster or git side effects; sibling manifests unmodified; no secrets in the report.

## Output
- `outputs/static_gate_report.md` — the full per-identity report per the `static_gate_report` schema in
  `../contracts/synthesis_gate_contract.yaml`.
