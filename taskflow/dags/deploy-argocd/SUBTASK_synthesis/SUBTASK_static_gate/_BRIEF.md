# Task: Static verification gate over the combined deploy manifests (pre-cluster go/no-go)

## Task Specification

**Slug**: SUBTASK_static_gate
**Task Kind**: synthesis / verification (static)
**Status**: Pending

### Objective

Run the **static** half of the deploy-argocd verification gate over the *combined* sibling outputs,
**before anything touches the cluster**. Assert every statically-checkable parent contract identity,
confirm wiring (no dead manifest) and duplication (disjoint producers), and give a focused k3s/ArgoCD +
security review — ending in a clear static **GO / NO-GO** for the downstream deploy. You READ the
combined manifests; you do not modify them and you do not touch the cluster or git.

### Context

You are the first stage of the `SUBTASK_synthesis` sub-subtree (hub `../_GLOBAL.md`, contract
`../contracts/`). The two authoring spokes are COMPLETED: `../../SUBTASK_app_manifests` produced
`deploy/chirp/*` and `../../SUBTASK_argocd_gitops` produced `deploy/argocd/*`. The parent identities you
assert live in `../../contracts/_MANIFEST.yaml`; the frozen shared values in
`../../contracts/deploy_contract.yaml`; the resolved facts (digest, ports, health path, ingress class,
pull-secret need) in `../../SUBTASK_discovery/outputs/ground_truth.md`.

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| App workload manifests | `/home/user/nswe-demo/deploy/chirp/*` (also mirrored at `../../SUBTASK_app_manifests/outputs/deploy/chirp/`) | The objects to assert statically |
| GitOps config | `/home/user/nswe-demo/deploy/argocd/*` | Application + AppProject to assert |
| Parent contract + identities | `../../contracts/_MANIFEST.yaml`, `../../contracts/deploy_contract.yaml` | The assertion set |
| Ground-truth facts | `../../SUBTASK_discovery/outputs/ground_truth.md` | Digest/port/health-path/ingress-class to compare against |
| Sub-subtree contract | `../contracts/_MANIFEST.yaml`, `../contracts/synthesis_gate_contract.yaml` | Your identity-coverage assignment + the required report shape |

## Scope (what this task covers — you decide the method)

- The **statically-checkable** identities assigned to you in `../contracts/_MANIFEST.yaml`
  `identity_coverage` (`image-pinned-by-digest`, `resources-and-probes`, `appproject-least-privilege`,
  `namespace-isolation-no-secrets`), each asserted against the real manifest text with recorded evidence.
- The **static halves** of the three runtime identities (`service-selector-matches-pods`,
  `ingress-wires-service`, `argocd-application-wired`): the label/port, backend/class, and path/project
  diffs that can be checked without a cluster (the runtime halves belong to `SUBTASK_deploy_reach`).
- **Wiring**: every object is referenced/mounted (Service→pods via selector, Ingress→Service, Application→
  path + project); no dead/orphan manifest.
- **Duplication**: exactly one producer per owned path; `deploy/chirp` and `deploy/argocd` disjoint.
- **Review**: a focused read for k3s/Traefik + ArgoCD idiom and the security posture.
- If a static identity FAILs, record it precisely; routing it to a remediation fix-task
  (`engine_amend_plan { add_task }`) is an available response — do not silently edit the sibling manifests.

Out of scope: any cluster mutation, any git mutation, and the runtime identity proofs (those are
`SUBTASK_deploy_reach`). Do not re-author the sibling manifests.

## Output Specification

| Attribute | Value |
|-----------|-------|
| File | `outputs/static_gate_report.md` (under this task's workspace) |
| Content | Per the `static_gate_report` schema in `../contracts/synthesis_gate_contract.yaml`: per-identity PASS/FAIL table with evidence, the static halves of the runtime identities, wiring + duplication results, review note, overall static GO/NO-GO |

## Success Criteria

- [ ] Every assigned static identity has a recorded PASS/FAIL with concrete evidence (file:line / compared value) — no silent plug.
- [ ] Static halves of the runtime identities recorded; wiring and duplication checks recorded.
- [ ] A focused review note and an unambiguous overall static GO/NO-GO are present.
- [ ] No cluster or git side effects; sibling manifests unmodified.

## Suggested Methodology Files

Task-type rows: *"Synthesizing / verifying a hub-and-spoke decomposition (contract + wiring + dedup +
review gate)"* (primary `synthesis`; supporting `code-review`, `code-quality`); *"Kubernetes
configuration & secrets"* and *"enforce pod security / admission"* (`kubernetes`, `kubernetes-security`,
for the static posture read). Load `synthesis` first; these are SUGGESTIONS — you judge coverage depth.

- `synthesis/Synthesis_Overview_Methodology.md` — anchor; the four-check gate model and the
  mechanical-then-review discipline (run the deterministic checks, then review).
- `synthesis/Synthesis_Contract_Verification_Methodology.md` — the gate-time inverse of the frozen
  contract: enumerate every identity and run its check; coverage is total, not sampled.
- `synthesis/Synthesis_Wiring_Verification_Methodology.md` — no detached/dead manifest.
- `synthesis/Synthesis_Duplication_Detection_Methodology.md` — one producer per owned path.
- `synthesis/Synthesis_Code_Review_Methodology.md` — the focused review of the combined manifests.
- `synthesis/Synthesis_Remediation_Methodology.md` — only if a static check FAILs (inject fix-tasks).
- `kubernetes` / `kubernetes-security` — confirm the k3s/Traefik idiom and least-privilege/supply-chain posture statically.

These are the parent's flagged methodologies for this task type. Load them as a starting point but you are
the final judge of what your work requires — load fewer if clearly inapplicable, more if your reading reveals
additional surface. Synthesis never loads `decomposition/` content.

## Inherited Constraints

- Read-only over the sibling manifests; do NOT edit them (remediation is injected fix-tasks, not inline edits).
- No cluster access and no git mutation in this task.
- Assert, do not re-author: least-privilege AppProject (no `*/*/*`) and `@sha256:` digest pinning are
  already in the manifests; your job is to verify them against `ground_truth.md` and the contract.
- No secrets read into or written to the report.

## Out-of-Scope Methodologies

- `decomposition/` content — this is reassembly/verification, not a split.
- `operations`/git methodologies — landing is `SUBTASK_land_pr`'s concern, not yours.
- Runtime/cluster methodologies beyond what you need to read the manifests statically — the live proof is `SUBTASK_deploy_reach`.
