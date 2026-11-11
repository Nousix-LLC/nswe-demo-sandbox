# Task: Accounts & lifecycle design for chirp (as REQ-ID requirements)

## Task Specification
**Slug**: SUBTASK_accounts_lifecycle
**Task Kind**: standard
**Status**: Pending

### Objective
Design the chirp **account object and its full lifecycle** as testable `REQ-ID-*` requirements — how a person
gets an account, manages it, and ends it, and how they and their data leave — to the bar of a releasable,
publicly-exposed, account-based consumer product. Requirements only; defer every implementation "how" to code
DAGs by prose.

### Context
Part of `SUBTASK_identity_trust` (see `../_GLOBAL.md`) within `design-chirp-r1`. You own the
`accounts_and_lifecycle` section of `design/identity-security.md` and `REQ-ID-001..029`. The authentication,
session, and credential **mechanisms** belong to the sibling `SUBTASK_auth_sessions` — you state the lifecycle
events that depend on them from the account's side (sign-up establishes a credential; recovery re-establishes
access) and name that sibling, without specifying the auth mechanism yourself.
**Dependencies**: none (read the already-COMPLETED product-requirements output directly).
**Dependents**: `SUBTASK_synthesis` consolidates your partial and REQ-ID cluster.

### Distinct concerns to weigh in your own evaluation
These are facets of one requirements cluster (the account lifecycle); weigh them and decompose only if your own
reading finds genuinely separable responsibilities:
- Sign-up that establishes a real credential and a verified point of contact (what is collected, kept minimal).
- Profile edit and the account-settings surface (contact, active sessions/devices, notification prefs).
- A stated handle-change policy (handles are the identifier others follow by).
- Self-service account recovery through the verified contact.
- Data export (portable form) and account deletion with a defined, confirmed outcome for content and handle.

## Inputs
| Input | Source (absolute) | Purpose |
|-------|-------------------|---------|
| Subtree hub | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-chirp-r1/SUBTASK_identity_trust/_GLOBAL.md` | Shared context, constraints, writing voice |
| Subtree contract | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-chirp-r1/SUBTASK_identity_trust/contracts/` (read-only) | Your REQ-ID range, section, partial format |
| Parent contract | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-chirp-r1/contracts/` (read-only) | REQ-ID format, required fields, verification vocab — compose against, do not redefine |
| Product requirements | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-chirp-r1/SUBTASK_product_requirements/outputs/product-requirements.md` | REQ-PROD-008/009/012/013/016–022 and journeys J2/J3a/J6/J8 — the user-side needs + trace targets |
| Repo + live product | `Nousix-LLC/nswe-demo` @ `c805525`; live deployment (read-only) | Current state: handle-only sign-up, no recovery/settings/edit/deletion/export |

## Methodology
Bundle IDs (Domain Mapping): **Identity and Trust** (primary — accounts & the lifecycle, privacy/data-rights for
deletion/export); **Product Strategy**, **Release Definition**, **Product Surfaces** (supporting).

## Output
- `SUBTASK_accounts_lifecycle/outputs/accounts-lifecycle.md` — the `accounts_and_lifecycle` section partial in the
  format fixed by `../contracts/req_id_partition.yaml` (section prose + `REQ-ID-001..029` entries + notes for
  synthesis). Repository-ready content (no host/system/taskflow detail).

## Success criteria
- [ ] Composes against both contracts; `REQ-ID-*` ids only within `001..029`; schema not redefined.
- [ ] Sign-up (real credential + verified contact), recovery, profile edit, settings surface, handle-change
      policy, data export, and account deletion with a defined+confirmed outcome are each specified as
      requirements — not stubs — from the user's side.
- [ ] Every `REQ-ID-*` has a statement, testable acceptance_criteria, a release_gating flag, a verification method
      where it would anchor a bar, and traces to ≥1 existing `REQ-PROD-*`.
- [ ] Implementation "how" (hashing, token/credential internals, export format internals) is deferred to code
      DAGs by prose; the sibling `SUBTASK_auth_sessions` is named for the credential/session mechanism.

## Constraints
- Requirements only — no implementation of credentials, sessions, crypto, or storage.
- Do not mint any id outside `REQ-ID-001..029`; do not mint `REQ-PROD-*`/`REQ-DOM-*`/`REQ-UX-*`/`REQ-OPS-*`/`BAR-*`.
- Repository-ready hygiene and the hub's writing-voice rule bind your prose.
