# Task: Abuse-resistance & privacy/data-rights basics for chirp (as REQ-ID requirements)

## Task Specification
**Slug**: SUBTASK_abuse_privacy
**Task Kind**: standard
**Status**: Pending

### Objective
Design the **minimum abuse-resistance and privacy/data-rights surface** a public social product needs, as
testable `REQ-ID-*` requirements, to the bar of a releasable public product that strangers can post at each
other on. Requirements only; defer enforcement and data-handling "how" to code DAGs by prose.

### Context
Part of `SUBTASK_identity_trust` (see `../_GLOBAL.md`). You own the `abuse_and_privacy_basics` section of
`design/identity-security.md` and `REQ-ID-080..099`. The authority/visibility boundary (who may read/write which
fields) is the sibling `SUBTASK_authorization`; you own **data-protection** (what is collected, how it is kept
private, retained, and erased) and the **abuse controls** (report, rules, block/mute, limits). Coordinate the
public-vs-private field split with `SUBTASK_authorization` by prose. Rate/volume limits are also an operational
concern: state the limit as an identity/trust requirement, trace to `REQ-PROD-041`, and name the `REQ-OPS-*` area
for the enforcement detail — do not mint `REQ-OPS-*`.
**Dependencies**: none (read the already-COMPLETED product-requirements output directly).
**Dependents**: `SUBTASK_synthesis`.

### Distinct concerns to weigh in your own evaluation
Facets of one requirements cluster (abuse + privacy basics); decompose only if genuinely separable:
- Abuse controls: report a chirp/account (acknowledged as received), stated rules/terms a report references,
  block and mute to stop unwanted interaction, and rate/volume limits as a first line against abuse.
- Privacy/data-rights: data minimization (collect only what the account needs); private-field protection
  (contact, credential, session data never exposed to other users or in public responses); retention and
  erasure-on-deletion consistent with the account-deletion outcome; and a data-rights baseline (access, export,
  erasure) proportionate to a public microblog — stated as product requirements, not legal advice.

## Inputs
| Input | Source (absolute) | Purpose |
|-------|-------------------|---------|
| Subtree hub | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-chirp-r1/SUBTASK_identity_trust/_GLOBAL.md` | Shared context, constraints, writing voice |
| Subtree contract | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-chirp-r1/SUBTASK_identity_trust/contracts/` (read-only) | Your REQ-ID range, section, partial format |
| Parent contract | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-chirp-r1/contracts/` (read-only) | REQ-ID format, required fields, verification vocab — compose against, do not redefine |
| Product requirements | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-chirp-r1/SUBTASK_product_requirements/outputs/product-requirements.md` | REQ-PROD-024/025/026/027/041/021 and journeys J7/J8 — user-side needs + trace targets |
| Repo + live product | `Nousix-LLC/nswe-demo` @ `c805525`; live deployment (read-only) | Current state: no report/rules/block/mute, no limits, no stated privacy/retention posture |

## Methodology
Bundle IDs (Domain Mapping): **Identity and Trust** (primary — privacy/data-rights & compliance, abuse);
**Product Strategy**, **Product Surfaces**, **Release Definition** (supporting).

## Output
- `SUBTASK_abuse_privacy/outputs/abuse-privacy.md` — the `abuse_and_privacy_basics` section partial in the format
  fixed by `../contracts/req_id_partition.yaml` (section prose + `REQ-ID-080..099` entries + notes for synthesis).
  Repository-ready content.

## Success criteria
- [ ] Composes against both contracts; `REQ-ID-*` ids only within `080..099`; schema not redefined.
- [ ] Abuse controls (report, stated rules, block/mute, limits) and privacy basics (minimization, private-field
      protection, retention/erasure, data-rights baseline) are each specified as testable requirements.
- [ ] Every `REQ-ID-*` has a statement, testable acceptance_criteria, a release_gating flag, a verification method
      where it would anchor a bar, and traces to ≥1 existing `REQ-PROD-*`.
- [ ] Rate/volume limits are traced to `REQ-PROD-041` with the `REQ-OPS-*` area named for enforcement (not minted
      here); the public/private field split is coordinated with `SUBTASK_authorization` by prose.

## Constraints
- Requirements only — no implementation of filters, limiters, or data-handling mechanics.
- Do not mint any id outside `REQ-ID-080..099`; do not mint other areas' ids or `BAR-*`.
- Note (for the synthesis's threat model) which disclosure/abuse/DoS threats each requirement answers.
- Repository-ready hygiene and the hub's writing-voice rule bind your prose.
