# Task: Authorization model design for chirp (as REQ-ID requirements)

## Task Specification
**Slug**: SUBTASK_authorization
**Task Kind**: standard
**Status**: Pending

### Objective
Design chirp's **authority model** — what each actor may see and change — as testable `REQ-ID-*` requirements,
to the bar of a releasable public product where a person acts only as themselves. Requirements only; defer the
enforcement "how" to code DAGs by prose.

### Context
Part of `SUBTASK_identity_trust` (see `../_GLOBAL.md`). You own the `authorization` section of
`design/identity-security.md` and `REQ-ID-060..079`. Authentication (proving who the actor is) is the sibling
`SUBTASK_auth_sessions`; you take identity as established and specify what that identity is **authorized** to do.
The privacy-field *data-protection* requirements (minimization, retention, erasure) are the sibling
`SUBTASK_abuse_privacy`; you own the **authority/visibility boundary** (who may read/write which fields), and you
coordinate the public-vs-private field split with that sibling by prose rather than duplicating it.
**Dependencies**: none (read the already-COMPLETED product-requirements output directly).
**Dependents**: `SUBTASK_synthesis`.

### Distinct concerns to weigh in your own evaluation
Facets of one requirements cluster (the authority model); decompose only if genuinely separable:
- Actor-scoped action authority: a signed-in person may post/reply/like/follow as themselves only, and may edit
  or delete only their own account and content; acting as another account is refused.
- The read boundary: unauthenticated read scope (public profiles/chirps, counts) vs authenticated actions vs the
  owner-only fields; which fields any viewer may read and which are the owner's alone.
- Operator/admin/support authority: who is authorized to assist recovery, remove content, and action an abusive
  account — under what principle (least privilege; operator authority separated from ordinary-user authority;
  auditable). This is the authorization aspect of the supported admin surface (REQ-PROD-028); the surface's
  existence/shape is a product/ops concern you reference, not redesign.

## Inputs
| Input | Source (absolute) | Purpose |
|-------|-------------------|---------|
| Subtree hub | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-chirp-r1/SUBTASK_identity_trust/_GLOBAL.md` | Shared context, constraints, writing voice |
| Subtree contract | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-chirp-r1/SUBTASK_identity_trust/contracts/` (read-only) | Your REQ-ID range, section, partial format |
| Parent contract | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-chirp-r1/contracts/` (read-only) | REQ-ID format, required fields, verification vocab — compose against, do not redefine |
| Product requirements | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-chirp-r1/SUBTASK_product_requirements/outputs/product-requirements.md` | REQ-PROD-023/024/028/007 — user-side authority needs + trace targets |
| Repo + live product | `Nousix-LLC/nswe-demo` @ `c805525`; live deployment (read-only) | Current state: session identifies an actor; public profile served unauthenticated; no admin/authority model |

## Methodology
Bundle IDs (Domain Mapping): **Identity and Trust** (primary — authorization & the authority model);
**Product Strategy**, **Release Definition** (supporting).

## Output
- `SUBTASK_authorization/outputs/authorization.md` — the `authorization` section partial in the format fixed by
  `../contracts/req_id_partition.yaml` (section prose + `REQ-ID-060..079` entries + notes for synthesis).
  Repository-ready content.

## Success criteria
- [ ] Composes against both contracts; `REQ-ID-*` ids only within `060..079`; schema not redefined.
- [ ] Actor-scoped action authority, the read/visibility boundary, and the operator/admin authority model are
      each specified as testable requirements.
- [ ] Every `REQ-ID-*` has a statement, testable acceptance_criteria, a release_gating flag, a verification method
      where it would anchor a bar, and traces to ≥1 existing `REQ-PROD-*`.
- [ ] The public-vs-private field split is coordinated with `SUBTASK_abuse_privacy` by prose (no duplication of
      its data-protection requirements); enforcement "how" is deferred to code DAGs.

## Constraints
- Requirements only. Do not mint any id outside `REQ-ID-060..079`; do not mint other areas' ids or `BAR-*`.
- Note (for the synthesis's threat model) which elevation/impersonation threats each requirement answers.
- Repository-ready hygiene and the hub's writing-voice rule bind your prose.
