# Task: Threat model + assembly + verification gate for identity-security.md

## Task Specification
**Slug**: SUBTASK_synthesis
**Task Kind**: synthesis
**Status**: Pending

### Objective
Integrate the four identity/security requirement clusters into the single releasable deliverable
`design/identity-security.md`: author the **threat model** (derived from the four areas), assemble all six
required sections and the consolidated `REQ-ID-*` register, **verify the subtree contract identities with
recorded evidence**, and fold the result up into `SUBTASK_identity_trust`. This is the subtree's verification
gate — it reconciles the combined output and does not silently plug a failing identity.

### Context
Part of `SUBTASK_identity_trust` (see `../_GLOBAL.md` and `../contracts/`). You read the four sibling partials,
own the `threat_model` section and any threat-driven `REQ-ID-100..119`, and produce the assembled deliverable
plus the fold record. You own the final `identity-security.md`; the four spokes own their section partials.

**Dependencies**: `SUBTASK_accounts_lifecycle`, `SUBTASK_auth_sessions`, `SUBTASK_authorization`,
`SUBTASK_abuse_privacy` (all four COMPLETED, partials present).
**Dependents**: folds the parent `SUBTASK_identity_trust`.

### What this gate must do (obligations, not a fixed runbook)
- **Threat model** (`threat_model` section): walk chirp's public, internet-facing surface STRIDE-style
  (spoofing an identity, tampering with content/attribution, repudiation, information disclosure of private
  fields, denial of service, elevation beyond one's own account), derived from the four areas. For each threat,
  name what the design answers (the `REQ-ID-*` that mitigates it) or record the residual risk and why it is
  acceptable for the bar. Mint `REQ-ID-100..119` only for threat-driven requirements not already covered by a
  spoke (e.g. transport confidentiality, anti-automation/bot resistance, auditability of operator actions).
- **Assemble** the single `identity-security.md` with the six required sections in `design_artifact_map.yaml`
  order (accounts_and_lifecycle, authentication_and_sessions, authorization, abuse_and_privacy_basics,
  threat_model, requirements_and_acceptance_criteria), the last being the consolidated register of every
  `REQ-ID-*` from the four partials plus your threat-driven ids, each with its full fields.
- **Verify the identities** in `../contracts/_MANIFEST.yaml` with recorded evidence: unique ids each within their
  owner's range; every `REQ-ID-*` testable + release_gating + traces to ≥1 existing `REQ-PROD-*`; gating ids name
  a verification method from the vocabulary; all six sections present; every `REQ-PROD-*` identity need
  (008–014, 016–024, identity aspects of 025–028) answered or explicitly carried by a sibling area with a reason;
  threat model answers each named threat; no schema redefinition; deliverable hygiene; writing-voice pass.
- **Remediate by decomposing**, not by a silent plug: if an identity fails (a gap, a collision, an untraceable
  requirement), decompose a remediation subtree or report the failure — never paper over it.
- **Fold**: author `SYNTHESIS.md` at the fold location (`../SYNTHESIS.md`, i.e. the SUSPENDED parent's directory)
  recording the identity evidence and the `REQ-ID ↔ REQ-PROD` trace list; then resume the suspended parent.

## Inputs
| Input | Source (absolute) | Purpose |
|-------|-------------------|---------|
| Subtree hub | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-chirp-r1/SUBTASK_identity_trust/_GLOBAL.md` | Shared context, success criteria, writing voice |
| Subtree contract | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-chirp-r1/SUBTASK_identity_trust/contracts/` (read-only) | Identities to assert, id partition, section map, partial format |
| Parent contract | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-chirp-r1/contracts/` (read-only) | REQ-ID format, required fields, verification vocab, design-artifact map |
| Accounts partial | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-chirp-r1/SUBTASK_identity_trust/SUBTASK_accounts_lifecycle/outputs/accounts-lifecycle.md` | `accounts_and_lifecycle` section + REQ-ID-001..029 |
| Auth/sessions partial | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-chirp-r1/SUBTASK_identity_trust/SUBTASK_auth_sessions/outputs/auth-sessions.md` | `authentication_and_sessions` section + REQ-ID-030..059 |
| Authorization partial | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-chirp-r1/SUBTASK_identity_trust/SUBTASK_authorization/outputs/authorization.md` | `authorization` section + REQ-ID-060..079 |
| Abuse/privacy partial | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-chirp-r1/SUBTASK_identity_trust/SUBTASK_abuse_privacy/outputs/abuse-privacy.md` | `abuse_and_privacy_basics` section + REQ-ID-080..099 |
| Product requirements | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-chirp-r1/SUBTASK_product_requirements/outputs/product-requirements.md` | The `REQ-PROD-*` register every trace must resolve into |

## Methodology
Bundle IDs (Domain Mapping): **Identity and Trust** (primary — threat model, coverage); **Release Definition**
(CompletenessAndGapReview). The synthesis-gate method (how to run a verification gate + fold) is engineering
practice in the `software` domain's `synthesis` bundle, reached by prose.

## Output
- `SUBTASK_identity_trust/outputs/identity-security.md` — the assembled, repository-ready deliverable (six
  sections + consolidated `REQ-ID-*` register). This is the parent node's declared output.
- `SUBTASK_identity_trust/SYNTHESIS.md` — the fold record: identity evidence (each identity asserted with its
  result), the `REQ-ID ↔ REQ-PROD` trace list, and any gap/remediation note.

## Success criteria
- [ ] All six required sections present, in `design_artifact_map.yaml` order; consolidated register complete.
- [ ] Every subtree identity in `../contracts/_MANIFEST.yaml` asserted with recorded evidence; no silent plug.
- [ ] Every `REQ-ID-*` unique and in range; testable + gating + traces to ≥1 existing `REQ-PROD-*`.
- [ ] Threat model names each threat and what the design answers (REQ-ID or recorded residual risk).
- [ ] `identity-security.md` carries no host/system/taskflow detail or attribution trailer; writing-voice pass run.
- [ ] Parent folded via `SYNTHESIS.md` at `../SYNTHESIS.md`.

## Constraints
- Requirements/threat-model only — no implementation. Do not redefine the id scheme or section map.
- Mint `REQ-ID-*` only within `100..119` and only for threat-driven requirements not already covered by a spoke.
- A failing identity is remediated by decomposition or reported — never silently reconciled.
