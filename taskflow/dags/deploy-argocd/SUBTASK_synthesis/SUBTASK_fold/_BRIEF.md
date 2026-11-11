# Task: Fold synthesis — author the root SYNTHESIS.md verdict and fold the deploy-argocd subtree

## Task Specification

**Slug**: SUBTASK_fold
**Task Kind**: synthesis (verification gate — final verdict + fold)
**Status**: Pending

### Objective

Be the deploy-argocd subtree's **final verification gate and fold point**: consolidate the three upstream
outputs into a single PASS/FAIL verdict over the *entire* parent contract-identity set (static + runtime,
**no silent plug**), author the root `SYNTHESIS.md` fold record, and **fold the deploy-argocd subtree to
COMPLETED**. This is a verification gate, NOT a prose summary — it asserts total identity coverage and that
any FAIL was remediated, or it schedules remediation and re-verifies.

### Context

Final stage of the `SUBTASK_synthesis` sub-subtree (hub `../_GLOBAL.md`, contract `../contracts/`). Your
declared dependencies are COMPLETED: `SUBTASK_static_gate` (static verdict), `SUBTASK_deploy_reach`
(reachability evidence + runtime verdict), `SUBTASK_land_pr` (PR record). You read their real outputs; you
produce the authoritative verdict and perform the kernel fold.

This sub-subtree exists because `SUBTASK_synthesis` decomposed. Therefore the root `SYNTHESIS.md` that the
`SUBTASK_synthesis` brief owed to the deploy-argocd subtree root is YOURS to author, and the fold that
resolves the subtree is yours to perform.

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Static gate report | `../SUBTASK_static_gate/outputs/static_gate_report.md` | Static per-identity results, wiring, duplication, review, GO/NO-GO |
| Reachability evidence | `../SUBTASK_deploy_reach/outputs/reachability_evidence.md` | Runtime per-identity results + the HTTP request/response evidence |
| PR record | `../SUBTASK_land_pr/outputs/pr_record.md` | PR URL/number, commit SHA(s), CI status, no-trailers/no-merge confirmations |
| Parent identities | `../../contracts/_MANIFEST.yaml`, `../../contracts/deploy_contract.yaml` | The full identity set the verdict must cover |
| Sub-subtree contract | `../contracts/_MANIFEST.yaml`, `../contracts/synthesis_gate_contract.yaml` | Identity-coverage map, the `fold_output` schema, and the fold obligation |
| Ground truth | `../../SUBTASK_discovery/outputs/ground_truth.md` | Decision-record facts (digest, ingress, pull-secret, #23 divergences) |

## Scope (what this task covers — you decide the method)

- Confirm **every** parent identity in `../../contracts/_MANIFEST.yaml` is covered by exactly one upstream
  result (per `../contracts/_MANIFEST.yaml` `identity_coverage`), with both the static and runtime halves
  recorded where applicable. A missing or unresolved identity is a gate FAIL — not a silent pass.
- Decide the machine-gate **PASS/FAIL** verdict. On FAIL, schedule remediation via
  `engine_amend_plan { add_task }` (Inject a fix-task + a re-verification) rather than plugging — do not
  edit the sibling manifests or fabricate a PASS.
- Assemble the **decision record**: ingress mechanism, AppProject scoping, imagePullSecret handling, and the
  native-cluster divergences noted for #23 (HSO-1).
- Author the root `SYNTHESIS.md` fold record at the deploy-argocd subtree root:
  `/home/user/nousix-runtime/nswe-demo/taskflow/dags/deploy-argocd/SYNTHESIS.md` (per the `fold_output`
  schema in `../contracts/synthesis_gate_contract.yaml`): verdict, per-identity results, reachability
  evidence, decision record, PR link.
- **Perform the fold** (kernel `engine_resume_suspended`). Both the `SUBTASK_synthesis` node (this
  sub-subtree's root, task id `SUBTASK_synthesis`) and the `deploy-argocd` root (task id `deploy-argocd`)
  are SUSPENDED/NeedsDecompose and MUST be resumed to COMPLETED, with the root `SYNTHESIS.md` as the seam
  record and this task (`SUBTASK_fold`) as the synthesized (COMPLETED) task. Neither ancestor may be left
  dangling SUSPENDED.

Out of scope: re-running the static checks, the deploy, or the PR (consume the upstream outputs); editing
the sibling manifests.

## Output Specification

| Attribute | Value |
|-----------|-------|
| File | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/deploy-argocd/SYNTHESIS.md` (the deploy-argocd subtree root — the fold location) |
| Role | This task's terminal record AND the fold seam that resolves the deploy-argocd subtree |
| Content | Per the `fold_output` schema: PASS/FAIL verdict; per-identity results (static + runtime); reachability evidence; decision record; PR link |

## Success Criteria

- [ ] Every parent contract identity has a recorded PASS/FAIL sourced from an upstream output — no silent plug, no unresolved identity passed off as PASS.
- [ ] The four-check posture is honored: contract identities + wiring + duplication + review all reflected in the verdict; any FAIL handled by injected remediation + re-verification, not inline repair.
- [ ] `SYNTHESIS.md` present at the deploy-argocd subtree root with verdict, per-identity results, reachability evidence, decision record, and the PR link.
- [ ] The fold is performed: both `SUBTASK_synthesis` and `deploy-argocd` are resumed to COMPLETED via `engine_resume_suspended` with `SYNTHESIS.md` as the seam; neither is left SUSPENDED.

## Suggested Methodology Files

This child is a **verification gate** (deployment obligation). Load `synthesis` first, then the sibling
check/remediation files your reading reveals you need. SUGGESTIONS — you judge coverage depth.

Task-type rows: *"Synthesizing / verifying a hub-and-spoke decomposition (contract + wiring + dedup +
review gate)"* (primary `synthesis`; supporting `code-review`, `code-quality`); *"Remediating
synthesis-gate violations as decomposed fix-tasks"* (`synthesis`).

- `synthesis/Synthesis_Overview_Methodology.md` — anchor (always first): the four-check gate model, the
  PASS/FAIL decision, and the structured `SYNTHESIS.md` schema.
- `synthesis/Synthesis_Contract_Verification_Methodology.md` — total (not sampled) enumeration of the
  contract identities; the gate-time inverse of the frozen contract.
- `synthesis/Synthesis_Wiring_Verification_Methodology.md`, `synthesis/Synthesis_Duplication_Detection_Methodology.md` — reflect the upstream wiring/dedup results into the verdict.
- `synthesis/Synthesis_Code_Review_Methodology.md` — the combined-output review dimension of the verdict.
- `synthesis/Synthesis_Remediation_Methodology.md` — if the verdict is FAIL, inject fix-tasks + re-verify.

Parent-flagged for this task type; load as a starting point, you are the final judge of coverage depth.
Synthesis never loads `decomposition/` content.

## Inherited Constraints

- No silent plug: every identity's verdict is traceable to an upstream evidence line; remediation is injected fix-tasks, never inline edits.
- The PR must already be open (not merged) and `main` not pushed — record the PR link; do not alter the PR or push `main`.
- Reachability is evidence-backed (carry the captured request/response into `SYNTHESIS.md`).
- Note, but do not act on, native-cluster divergences (#23 HSO-1).
- The fold uses `SYNTHESIS.md` as the seam; resume both `SUBTASK_synthesis` and `deploy-argocd`.

## Out-of-Scope Methodologies

- `decomposition/` content — this is the reassembly/fold, not a split (injected remediation fix-tasks are gate-driven correction, not re-cutting).
- Kubernetes/GitOps/operations deploy+PR methodologies — those tasks are done; you consume their outputs.
