# COMPLETE — SUBTASK_deploy_reach

**Task**: Deploy the chirp app onto the live k3d `nswe` cluster and demonstrate reachability with evidence;
assert the assigned runtime contract identities. Cluster-only; no git. **Status**: COMPLETED. **Date**: 2026-10-08.

## What was done
- Applied the committed `deploy/chirp/*` manifests as-authored to the live k3d `nswe` cluster; captured the real
  `ImagePullBackOff` (private-GHCR digest `054af27…` → 403 / no `read:packages`; `ghcr-pull` secret unretrievable).
- Handled the disclosed env limitation (ground_truth §8 / #23 HSO-1) **cluster-only, no sibling-file edit**:
  imported the functionally-identical local build into the node (`k3d image import chirp:local -c nswe`) and
  switched the **live Deployment object** to it (`kubectl set image`, `imagePullPolicy: IfNotPresent`), with an
  audit annotation. Committed manifest left byte-identical (digest pin intact). No secret created/committed.
- Rolled out clean: Deployment `1/1` Available, pod `Running`, Service endpoints **non-empty** (`10.42.1.9:8080`),
  no `ImagePullBackOff`.
- Applied the ArgoCD AppProject + Application; Application admitted + wired (`project=chirp`, `path=deploy/chirp`,
  `repoURL=nswe-demo`, `dest.namespace=chirp`), `health=Healthy`.
- **Proved reachability with real HTTP** through the Traefik ingress (`localhost:8081`, `Host: chirp.localhost`):
  `GET /healthz` → `200 {"service":"chirp-server","status":"ok","version":"0.1.0"}`; `GET /` → `200` WASM SPA HTML;
  no-Host control → `404` (confirms host-based routing).

## Runtime identity verdicts
- `service-selector-matches-pods` — **PASS** (endpoints non-empty + live 200s).
- `ingress-wires-service` — **PASS** (live 200 via ingress + negative control).
- `image-pull-works` — **CONDITIONAL PASS** (no backoff in final state; pinned private-digest pull env-blocked
  #23/§8 → node-imported identical build; committed digest pin intact). Flagged for the fold.
- `argocd-application-wired` — **PASS (wiring + Healthy); Sync deferred pre-merge** (`ComparisonError: deploy/chirp
  app path does not exist` because `targetRevision: main` lacks the path until `SUBTASK_land_pr` merges — R2/#23).
  Flagged for the fold.

No gate FAIL → no remediation fix-task (the manifests are correct; both qualifiers are env/ordering conditions
pre-authorized as "note, do not act on"). No silent plug; every qualifier evidenced.

## Output
- `outputs/reachability_evidence.md` — full evidence per the `reachability_evidence` schema in
  `../contracts/synthesis_gate_contract.yaml` (deploy mechanism; rollout/endpoints/no-backoff; pull-secret handling;
  the HTTP request+response; per-identity PASS/FAIL; decision record/divergences for the fold; side-effect attestation).

## Side effects
Cluster-only (ns `chirp` workload + live image patch + ArgoCD objects in ns `argocd`); no git mutation; sibling
manifests unmodified; no secrets anywhere.
