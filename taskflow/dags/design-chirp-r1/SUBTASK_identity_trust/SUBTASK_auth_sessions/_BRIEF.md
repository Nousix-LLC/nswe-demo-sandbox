# Task: Authentication & sessions design for chirp (as REQ-ID requirements)

## Task Specification
**Slug**: SUBTASK_auth_sessions
**Task Kind**: standard
**Status**: Pending

### Objective
Design **real authentication and sessions safe to expose on the public internet** for chirp, as testable
`REQ-ID-*` requirements — closing the critical handle-only-sign-in gap — to the bar **real auth, not a stub;
sessions safe to expose publicly**. Requirements only; defer the authentication-protocol and session-store
"how" to code DAGs by prose.

### Context
Part of `SUBTASK_identity_trust` (see `../_GLOBAL.md`). You own the `authentication_and_sessions` section of
`design/identity-security.md` and `REQ-ID-030..059`. The account object and lifecycle events (sign-up, recovery)
belong to the sibling `SUBTASK_accounts_lifecycle`; you own the **mechanism requirements** (what proving identity
and holding a safe session must guarantee) and reference that sibling where sign-up/recovery establish or reset
the credential.
**Dependencies**: none (read the already-COMPLETED product-requirements output directly).
**Dependents**: `SUBTASK_synthesis`.

### Distinct concerns to weigh in your own evaluation
Facets of one requirements cluster (authentication and sessions); decompose only if your reading finds genuinely
separable responsibilities:
- What "real authentication" must mean: a secret only the owner holds; owner-only sign-in; a not-found vs
  failed-credential signal that does not leak which accounts exist beyond what is already public; credential
  strength / anti-guessing expectations (stated as requirements, not crypto-how).
- Safe public sessions: issuance, bounded lifetime/expiry, server-side invalidation and reliable sign-out,
  protection of the session token in transit and against theft/fixation/replay.
- Stay-signed-in on a trusted device as an explicit, bounded convenience.
- An explicit **in/out-of-scope decision for MFA and third-party/social login for the release bar**, each with a
  stated reason (chirp is a single public product of individual accounts — no enterprise tenancy/SSO obligation).

## Inputs
| Input | Source (absolute) | Purpose |
|-------|-------------------|---------|
| Subtree hub | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-chirp-r1/SUBTASK_identity_trust/_GLOBAL.md` | Shared context, constraints, writing voice |
| Subtree contract | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-chirp-r1/SUBTASK_identity_trust/contracts/` (read-only) | Your REQ-ID range, section, partial format |
| Parent contract | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-chirp-r1/contracts/` (read-only) | REQ-ID format, required fields, verification vocab — compose against, do not redefine |
| Product requirements | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-chirp-r1/SUBTASK_product_requirements/outputs/product-requirements.md` | REQ-PROD-008/010/011/014/015 and journeys J3/J3b/J5 — user-side needs + trace targets |
| Repo + live product | `Nousix-LLC/nswe-demo` @ `c805525`; live deployment (read-only) | Current state: handle-only sign-in issues a session token; no expiry/invalidation/sign-out story |

## Methodology
Bundle IDs (Domain Mapping): **Identity and Trust** (primary — authentication incl. MFA/social-login scope,
sessions); **Product Strategy**, **Release Definition** (supporting).

## Output
- `SUBTASK_auth_sessions/outputs/auth-sessions.md` — the `authentication_and_sessions` section partial in the
  format fixed by `../contracts/req_id_partition.yaml` (section prose + `REQ-ID-030..059` entries + notes for
  synthesis). Repository-ready content.

## Success criteria
- [ ] Composes against both contracts; `REQ-ID-*` ids only within `030..059`; schema not redefined.
- [ ] Real authentication (owner-only sign-in replacing handle-only) and publicly-safe sessions (expiry,
      server-side invalidation/sign-out, token protection) are specified as requirements, not stubs.
- [ ] The MFA and social-login scope decision for the bar is stated explicitly, each with a reason.
- [ ] Every `REQ-ID-*` has a statement, testable acceptance_criteria, a release_gating flag, a verification method
      where it would anchor a bar, and traces to ≥1 existing `REQ-PROD-*`.
- [ ] No implementation of auth protocols, token formats, or session storage — deferred to code DAGs by prose.

## Constraints
- Requirements only. Do not mint any id outside `REQ-ID-030..059`; do not mint other areas' ids or `BAR-*`.
- Note (for the synthesis's threat model) which threats each session requirement answers.
- Repository-ready hygiene and the hub's writing-voice rule bind your prose.
