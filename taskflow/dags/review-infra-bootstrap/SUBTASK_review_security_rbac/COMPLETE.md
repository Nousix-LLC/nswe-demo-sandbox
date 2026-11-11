# COMPLETE — SUBTASK_review_security_rbac

**Task**: Review PR #20 (infra-bootstrap, `deploy/bootstrap/`) through the security / secrets / least-privilege lens.
**Evaluation**: Atomic (one security-review responsibility over one small artifact; two owned concerns are facets of
one lens producing one findings doc — synthesis-of-inputs shape, not two independent analyses).
**Outcome**: completed. Review-only; no repo/branch/checkout/`main` modification performed (R7 upheld).

## What was done
- Read the subtree hub (`../_GLOBAL.md`), the review contract (`../contracts/_MANIFEST.yaml`,
  `../contracts/finding_schema.md`), and the upstream code-DAG `SYNTHESIS.md` (as INPUT context, not authority).
- Read all six bootstrap scripts + all four READMEs + `versions.txt` under the live tree
  `…/infra-bootstrap/checkout/deploy/bootstrap/`.
- Performed an **independent** secret scan (hard-value patterns: private keys, kubeconfig data blobs, inline
  password/token literals, bearer/JWT/AWS keys) over the staged tree **and** over `gh pr diff 20` — zero matches;
  corroborated (did not merely cite) the code DAG's I2.
- Confirmed the landed PR (`gh pr view 20`): OPEN, +912/−0, 11 files under `deploy/bootstrap/`, Closes #10; body
  documents runtime-retrieval access only.
- Judged piped-installer provenance/pinning (k3s `curl|sh`; ArgoCD `kubectl apply -f <raw URL>`) and ArgoCD
  namespace isolation + RBAC/ClusterRole breadth against least-privilege; consulted the suggested
  `kubernetes-security` RBAC and supply-chain methodologies to ground severity calls.

## Result
- Both owned concerns (`security_secrets_posture`, `least_privilege_rbac_cluster_posture`) assessed individually
  with evidence; both **clean** at the control-plane bring-up grain.
- **5 findings, all minor/nit** (no block, no major): SEC-1 (native kubeconfig `0644`), SEC-2 (stock ArgoCD
  application-controller `*/*/*` ClusterRole — defer-to-#13 hardening), SEC-3 (installer pin-by-tag, not
  digest/verify), SEC-4 (nit: `--force-conflicts` re-run reverts out-of-band RBAC narrowing), SEC-5 (nit: k3d
  Docker-group root-equivalence — security consequence only; acceptability deferred to HSO lens).
- AC bearing recorded: AC2_gitops (supports pass; SEC-2/3/4 as hardening follow-ups), AC4_runbook "commit no
  secrets" clause (clean), AC1_cluster (secondary: SEC-1/3/5). Lens disposition: no open block/major.

## Output
- `review_security.md` (this workspace) — per the contract's per-lens document shape (lens summary;
  concern-by-concern assessment for both owned concerns; findings in schema; AC bearing).

## Success criteria
- [x] Both owned concerns assessed individually with evidence.
- [x] Independent secrets scan performed (staged tree + diff) and its result recorded — not merely citing I2.
- [x] Explicit judgment on piped-installer provenance/pinning and on ArgoCD RBAC/namespace least-privilege.
- [x] Every finding well-formed per `finding_schema.md`; `review_security.md` written; no repo modification performed.
