# Task: Identity, security & trust design for chirp (as requirements)

## Task Specification
**Slug**: SUBTASK_identity_trust
**Task Kind**: standard
**Status**: Pending

### Objective
Design the identity, security and trust surface a releasable, publicly-exposed product needs — accounts and
their full lifecycle, real authentication and safe sessions, authorization, abuse/privacy basics, and the
threat model this surface implies — to the bar of **real auth, not a stub; sessions safe to expose publicly**.

### Context
Part of design-chirp-r1 (see `../_GLOBAL.md`, `../contracts/`). You own `design/identity-security.md` and
`REQ-ID-*`. State requirements and the threat model; defer the implementation of auth/sessions/SSO to code DAGs
(reach to the `software` domain by prose where a "how" is tempting).
**Dependencies**: `SUBTASK_product_requirements`. **Dependents**: `SUBTASK_release_bar` consolidates `REQ-ID-*`.

## Distinct concerns in this task
Evaluate your own scope against these and decompose if warranted:
- **Accounts & lifecycle** — sign-up, sign-in, credential recovery, account deletion, and data export (the
  unglamorous surfaces users assume: how they get in, and how they and their data leave).
- **Authentication & sessions** — real authentication and sessions that are safe to expose on the public
  internet; what "real auth" must mean for this product (and whether SSO/MFA are in-scope for the bar).
- **Authorization** — what each user may see and change; the authority model.
- **Abuse & privacy basics** — the minimum abuse-resistance and privacy/data-rights surface for a public
  social product.
- **Threat model** — the threats this product's surface implies and what the design must answer for.

## Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context/constraints |
| Contract | `../contracts/` (read-only) | `REQ-ID-*` scheme; your file + required sections |
| Product requirements | `../SUBTASK_product_requirements/outputs/product-requirements.md` | Users/journeys that imply identity needs |
| Repo + live product | `Nousix-LLC/nswe-demo` @ `c805525`; live deployment (read-only) | The current auth/session surface |

## Methodology
Bundle IDs (Domain Mapping): **Identity and Trust** (primary — accounts & authentication incl. SSO/MFA,
authorization & multi-tenancy, privacy/data-rights & compliance); **Product Strategy**, **Release Definition**,
**Product Surfaces** (supporting).

## Output
- `SUBTASK_identity_trust/outputs/identity-security.md` with the required sections in
  `../contracts/design_artifact_map.yaml` and `REQ-ID-*` ids. Repository-ready content.

## Success criteria
- [ ] Composes against `../contracts/`; `REQ-ID-*` used; schema not redefined.
- [ ] Real authentication, safe public sessions, and an authorization model are specified as requirements
      (not stubs); account lifecycle incl. recovery, deletion, and data export is covered.
- [ ] A threat model and abuse/privacy basics are stated.
- [ ] Every `REQ-ID-*` has testable acceptance criteria and a release-gating flag; traces to `REQ-PROD-*`.

## Constraints
- Requirements/threat model only — no implementation of auth, sessions, or crypto; defer to code DAGs.
- Repository-ready hygiene (no host/system/taskflow detail, no attribution trailers, no secrets).
