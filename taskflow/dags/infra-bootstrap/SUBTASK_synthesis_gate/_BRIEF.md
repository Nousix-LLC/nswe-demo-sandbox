# Task: Synthesis gate — verify, assemble, and land the infra-bootstrap PR

## Task Specification
**Slug**: SUBTASK_synthesis_gate
**Task Kind**: synthesis
**Status**: Pending

### Objective
Act as the **verification gate** for the infra-bootstrap (#10) subtree: verify the three spokes'
combined output against the frozen contract, assemble the unified bootstrap runbook, land the result
as commits on `work/infra-bootstrap` + a PR into `main` that **Closes #10**, and author the root
`SYNTHESIS.md` verdict at the DAG root. This is a gate, **not** a prose summary.

### Context
Final task of infra-bootstrap (#10) — see `../_GLOBAL.md` and `../contracts/`. You run after all
three spokes complete and read their COMPLETED outputs.

**Dependencies**: `SUBTASK_cluster_k3s`, `SUBTASK_wasm_toolchain`, `SUBTASK_gitops_argocd`.
**Dependents**: none (this folds the subtree into the parent result at the observation seam).

## Inputs
- `../_GLOBAL.md` (objective, constraints, env facts) and `../contracts/` (`_MANIFEST.yaml` identities
  I1–I6 + ownership; `result_record.schema.md`).
- Each spoke's COMPLETED outputs: `../SUBTASK_cluster_k3s/{staged/**,RESULT.md}`,
  `../SUBTASK_wasm_toolchain/{staged/**,RESULT.md}`, `../SUBTASK_gitops_argocd/{staged/**,RESULT.md}`.
- A checkout of `Nousix-LLC/nswe-demo` at `origin/main` for the git/PR work (establish `checkout/`
  under the DAG root; see `../_GLOBAL.md §Environment facts`).

## Scope / what to deliver (named as distinct concerns)
1. **Verification gate (run the four-check model over the COMBINED output)**:
   - *Contract/identities*: enumerate `_MANIFEST.yaml` identities I1–I6 and run each
     (criteria coverage; **no committed secrets** — grep staged trees + the diff; reproducibility
     headers + runbook wiring; versions recorded; honest blockers for any BLOCKED criterion;
     infra-only scope — no #12/#13 artifacts). Do not silently plug a failing identity.
   - *Wiring*: every spoke's staged files are laid into the repo under their owned paths and
     referenced by the unified runbook (no detached/dead script).
   - *Duplication*: no duplicated install logic across spokes; one producer per owned path.
   - *Combined review*: the staged scripts/manifests are coherent and safe to re-run.
2. **Assemble the unified runbook** `deploy/bootstrap/README.md` from the three spoke fragments
   (prereqs, run order across cluster → argocd and the independent wasm path, verification, access).
3. **Land it**: create branch `work/infra-bootstrap` off `main`, commit the laid-in `deploy/bootstrap/**`
   tree (and any `scripts/**` a spoke owned), push the branch, and open a **PR into `main`** whose body
   summarizes what was installed/verified, the kubeconfig + ArgoCD access runbook, toolchain versions,
   and (if applicable) the exact blocker(s) + remediation. **Do NOT merge the PR; do NOT push to `main`.**
   **No attribution trailers** on commits.
4. **Root verdict**: author `SYNTHESIS.md` at the DAG root (`../SYNTHESIS.md` — i.e. this DAG's root
   workspace `taskflow/dags/infra-bootstrap/SYNTHESIS.md`) carrying the machine-gate verdict
   (PASS, or honest PASS-with-documented-blocker), the per-criterion results, the decision record, and
   the PR link.

### Gate outcome & honesty
A criterion legitimately BLOCKED by a host/sandbox constraint (with an exact blocker + remediation in
the owning spoke's RESULT) is an **honest PASS-with-documented-blocker**, not a gate failure to hide —
surface it verbatim in the PR body and `SYNTHESIS.md`, and mark the criterion BLOCKED. A genuine gate
violation (missing owned artifact, a committed secret, a fabricated green, an out-of-scope #12/#13
artifact) is a **FAIL**: schedule remediation as additive fix-task(s) via `engine_amend_plan`
(remediation-as-decomposition) and re-verify — do not reconcile inline and do not launder it to PASS.

## Success Criteria
- [ ] All six contract identities (I1–I6) evaluated with recorded pass/fail; no identity silently plugged.
- [ ] `deploy/bootstrap/README.md` assembled and references every staged script with run order + verification.
- [ ] Branch `work/infra-bootstrap` exists off `main` with the committed bootstrap tree; PR into `main` opened that Closes #10, with the required body. PR NOT merged; `main` NOT pushed; no attribution trailers.
- [ ] No secret/live-kubeconfig/token in any commit (I2 verified over the actual diff).
- [ ] Root `SYNTHESIS.md` carries the verdict, per-criterion results (PASS / BLOCKED+blocker+remediation), decision record, and PR link.

## Suggested Methodology Files — SYNTHESIS gate (verification-gate posture is MANDATORY)
You are a verification gate; author and run accordingly. Primary **Synthesis**, supporting
**Operations** (git/PR), **Code Review** (PR authoring). Load on-demand:
- `synthesis` — `synthesis/Synthesis_Overview_Methodology.md` (anchor — the four-check model + gate
  pass/fail + `SYNTHESIS.md` schema; always, first), `synthesis/Synthesis_Contract_Verification_Methodology.md`
  (enumerate + run the `_MANIFEST.yaml` identities — this subtree HAS a contract),
  `synthesis/Synthesis_Wiring_Verification_Methodology.md` (staged files laid in + runbook-referenced),
  `synthesis/Synthesis_Duplication_Detection_Methodology.md` (no duplicated install logic), and
  `synthesis/Synthesis_Remediation_Methodology.md` (schedule fix-tasks on a real FAIL).
- `operations` — `operations/GitWorkflow_PR_Lifecycle_Methodology.md`,
  `operations/GitWorkflow_Syscall_PR_Review_Methodology.md`,
  `operations/CodeManagement_Branching_Strategy_Methodology.md`. Rationale: branch/commit/PR into main,
  closing #10, without merging or pushing main.
- `code-review` — `code-review/CodeReview_PR_Authoring_Methodology.md`. Rationale: the PR body.

*Gate posture is prescribed; coverage DEPTH is your judgment — run `Synthesis_Overview` first, then
load the sibling checks your reading of the subtree requires.*

## Inherited Constraints
All of `../_GLOBAL.md §Subtree-Wide Constraints` bind you (infra-only; no secrets; reproducible;
honest reporting; repo scope `Nousix-LLC/nswe-demo`; branch `work/infra-bootstrap`; PR into main
Closes #10; never force-push/rewrite main; **no attribution trailers**; do NOT merge the PR or push
main — the overseer lands, P1). You are the ONLY task that performs git operations.

## Out-of-Scope Methodologies
`decomposition/*` (decomposer-side only; synthesis is the reassembly, not the split). Do not author
app containerization (#12) or an ArgoCD `Application`/app deploy manifests (#13) while landing #10.
