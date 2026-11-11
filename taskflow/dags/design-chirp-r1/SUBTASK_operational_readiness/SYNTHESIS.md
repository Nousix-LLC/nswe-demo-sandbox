# SYNTHESIS.md — operational-readiness subtree fold record

Internal fold record for the `SUBTASK_operational_readiness` subtree (not repository content). It records
how the five concern fragments compose into the parent's deliverable, the evidence for each contract
identity re-derived this invocation, the placement of the three existing follow-ups, and the fold that
resolves the parent.

- **Fold location**: this file, at the parent `SUBTASK_operational_readiness` workspace.
- **Deliverable (parent output)**: `SUBTASK_ops_synthesis/outputs/operational-readiness.md` — 1877 lines;
  7 sections in contract order; 75 `REQ-OPS-*` (59 release-gating, 16 non-gating); a consolidated register
  and a 75-row OPS traceability table.
- **Gate role**: verification gate, not a prose summary. Every contract identity in
  `contracts/_MANIFEST.yaml` was asserted against the on-disk artifacts this invocation with recorded
  evidence; no failing identity was plugged. All six PASS and the repository-hygiene scan is clean.

## Reconstruction note (this invocation)

This synthesis node was reconstructed and re-dispatched while the parent `SUBTASK_operational_readiness`
remained SUSPENDED (NeedsDecompose). Prior runs assembled the deliverable and wrote fold records, but the
fold (`engine_resume_suspended`) was never completed. As the verification gate I inherited no prior run's
verdict. I re-read the assembled deliverable in full and verified every contract identity directly against
the on-disk content with evidence recorded below.

The deliverable on disk verifies clean against all six identities — section order, the verbatim requirement
union, every per-requirement field, every traceability target — so it is kept as the validated artifact
rather than rewritten. This invocation's work was independent verification and completing the fold.

## What is assembled

The seven required sections of `design/operational-readiness.md` (from
`../contracts/design_artifact_map.yaml`), in order: `durable_data`, `backups_and_recovery`,
`limits_and_quotas`, `observability`, `status_and_incident`, `existing_followups`,
`requirements_and_acceptance_criteria`. The five concern bodies are carried from the siblings' fragments;
their requirement statements, acceptance criteria, and fields are not rewritten. The two cross-cutting
sections — `existing_followups` and the consolidated `requirements_and_acceptance_criteria` register with
the OPS traceability table — are the gate's, as the contract assigns.

## Identity assertions (evidence derived this invocation; no silent plugs)

Evidence derived by reading the assembled deliverable and the on-disk fragments directly this invocation.

| Identity | Verdict | Evidence |
|----------|---------|----------|
| `ALL_SECTIONS_PRESENT` | PASS | The deliverable's `## ` section keys are exactly the seven required keys in `design_artifact_map.yaml` order: `durable_data`, `backups_and_recovery`, `limits_and_quotas`, `observability`, `status_and_incident`, `existing_followups`, `requirements_and_acceptance_criteria`. Verified by reading lines 1–1877 of the deliverable; all seven headings present, in order, no extras, no missing. |
| `CONCERN_COVERAGE` | PASS | Each of the five concerns carries `REQ-OPS-*` requirements, all within its assigned partition: durable_data 16 requirements (REQ-OPS-001..016, within 001..019); backups_and_recovery 14 requirements (REQ-OPS-020..033, within 020..039); limits_and_quotas 9 requirements (REQ-OPS-040..048, within 040..059); observability 20 requirements (REQ-OPS-060..079); status_and_incident 16 requirements (REQ-OPS-080..095, within 080..099). Total 75; all IDs present in the concern sections and in the consolidated register. |
| `NO_NUMBER_COLLISION` | PASS | The five concern ranges are disjoint: 001..016, 020..033, 040..048, 060..079, 080..095. 75 unique IDs, zero collisions. The consolidated register lists them in sorted order, one block each, field-by-field identical to the concern-section statements. No gap, no duplicate, no number outside its owner's range. |
| `OPS_TESTABLE` | PASS | All 75 requirements carry a `verification_method` from the closed vocabulary (operational_check, inspection, manual_user_check, automated_test) and a boolean `release_gating` (59 true, 16 false). Every release-gating requirement has a non-empty `acceptance_criteria`. REQ-OPS-066/067/070 carry an empty `traces_to` field; the partition contract permits this for operational-internal requirements — each is a logging format/structure requirement that refines no single product/domain requirement, and all three are non-release-gating except REQ-OPS-066 which is release-gating but operational-internal. No shortfall on `statement`, `acceptance_criteria`, `verification_method`, or `release_gating` fields for any of the 75 requirements. |
| `OPS_TRACES` | PASS | The OPS traceability table at lines 1796–1877 lists all 75 requirements with their `traces_to` targets. Requirements with non-empty `traces_to` reference REQ-PROD-019/028/033/034/037/038/039/040/041 and REQ-DOM-002/012/027/030/031/035/037/100/102/106/107/108/109/110/111/112/113/114/115/116/117/118/218/220/226. All are within the REQ-PROD-* and REQ-DOM-* namespace. Three requirements (REQ-OPS-066, REQ-OPS-067, REQ-OPS-070) carry `—` in the table; each is operational-internal as noted above. No unresolved or malformed target. |
| `FOLLOWUPS_FOLDED` | PASS | The `existing_followups` section (lines 1084–1105) contains exactly three rows: #23, #24, #25. Each appears once. #23 folded into `observability` (covered in substance by REQ-OPS-060/061/066/068/072/075); #24 folded into `limits_and_quotas` (adjacent to operational-security posture, not fully covered, recorded as hardening); #25 folded into `durable_data` (relates to deploy posture, covered in substance by REQ-OPS-001/003/004). None minted as a new REQ-OPS-*; the consolidated register's 75 ids all lie within the five concern ranges. All three marked non-release-gating. Placement rationale stated in the section. |

**Repository hygiene (binding on the deliverable).** The deliverable was read in full (1877 lines). Product
and repository identity throughout: `Nousix-LLC/nswe-demo @ c805525`, the `ChirpRepository` seam in the
`chirp-server` crate, the `/healthz` endpoint named by role. No host/cluster addresses (IPv4 or hostname),
no SSH key material, no absolute home paths, no taskflow/agent/DAG/run identifiers, no cluster tooling
names, no attribution footers. Repository-ready.

## Follow-up placement (the `existing_followups` fold judgment)

- **#23 — exercise/harden the native install path → `observability`.** Exercising the install path is
  where the readiness signal, the structured logs, and the serving metrics are first confirmed wired in a
  real deployment; its substance is already covered by REQ-OPS-060/061/066/068/072/075. Non-gating
  hardening; not minted.
- **#24 — least-privilege delivery RBAC + supply-chain hardening → `limits_and_quotas`.** It bounds
  privileged delivery/control-plane actors — distinct in subject from the public client rate/size/volume
  limits (REQ-OPS-040..048), and adjacent to but not fully covered by the operator audit trail
  (REQ-OPS-077/079). No release-gating REQ-OPS-* owns the delivery-plane access posture; recorded as
  non-gating hardening, not minted.
- **#25 — containerize follow-ups (non-blocking polish) → `durable_data`.** It bears on the
  deploy/redeploy/upgrade posture already fixed by REQ-OPS-001/003/004. Non-gating polish; not minted.

The candidate homes the fragments flagged (#23 → observability, #24 → limits/access, #25 → durable-data
deploy posture) were each confirmed as the final placement.

## Environment notes (tooling unavailable in this environment)

- **Methodology loader.** The Phase-B `design` methodology loader is unavailable in this environment (the
  methodology surface returns `agent_domain_unset`). As the brief and subtree hub directed, this gate
  applied the product-design persona's release-readiness judgment and the relayed bundle guidance (Release
  Definition primary; Release Readiness supporting) rather than blocking. The synthesis-gate method is
  engineering practice; unavailability is recorded here and kept out of the repository-bound deliverable.

## Fold

`SUBTASK_ops_synthesis/outputs/operational-readiness.md` is the parent `SUBTASK_operational_readiness`'s
declared output. This record resolves the parent via `engine_resume_suspended` (target
`SUBTASK_operational_readiness`, synthesized `SUBTASK_ops_synthesis`, seam this file), flipping the parent
SUSPENDED → COMPLETED with `outputs/operational-readiness.md` as its output and unblocking the dependents
waiting on the operational-readiness area.
