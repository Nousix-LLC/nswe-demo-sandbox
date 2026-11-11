# Task: Entry & authentication screens for chirp (with empty / error / loading states)

## Task Specification
**Slug**: SUBTASK_get_in
**Task Kind**: standard
**Status**: Pending

### Objective
Design the **entry and authentication screens and flows** a releasable chirp needs — the first-visit
landing, sign-up, sign-in, account recovery (and setting a new credential), and sign-out — each a
designed screen with its layout, content, and primary action, and **each with its empty, error, and
loading states**, to the bar of *designed screens, not a skeleton*.

### Context
Part of the screens-&-flows subtree (see `../_GLOBAL.md`, `../contracts/`). You own the **get_in** part of
the `screens_and_flows` section and `REQ-UX-040..050`. You compose against the frozen **screen inventory**
and **component library**; you do not invent screens or components outside those vocabularies without an
additive amendment to `../contracts/`. These screens are where a stranger decides whether chirp is a
product they can trust with an account, and they are the signed-out↔signed-in boundary — so align them
with the identity requirements (owner-only sign-in, a verified recovery contact, server-side sign-out).

**Dependencies**: none (within this subtree). **Dependents**: `SUBTASK_synthesis`.

### Scope — distinct surfaces to weigh in your own evaluation
This brief covers **several distinct screens/flows**; evaluate your own scope against the decomposition
triggers and decompose if warranted. Each surface is designed with its happy path **and** its empty /
error / loading states, and each maps to its journey and `REQ-PROD-*`:
- **First-visit landing** — the signed-out Landing that explains chirp and leads to sign-up/sign-in
  without an account and never dead-ends at an auth wall (J1 / REQ-PROD-030, 031).
- **Sign-up** — create an account with handle, display name, optional bio, the credential, and the
  verified contact; handle format/uniqueness feedback against the field (J2 / REQ-PROD-008, 009, 031;
  contact 012).
- **Sign-in** — return to an account by proving ownership; a clear not-found vs failed-credential signal
  (J3 / REQ-PROD-010, 011).
- **Account recovery** — Recover access and Set new credential: self-service recovery through the
  verified contact (J3a / REQ-PROD-012, 013).
- **Sign-out** — the sign-out confirmation that ends the session, incl. ending sessions on other devices
  (J3b / REQ-PROD-014).
- **The transitions between them** — sign-up → onboarding, the interlinks between sign-in/sign-up/
  recovery, sign-out → signed-out landing with no back-leak — as the IA interaction model already fixes
  them (compose against `REQ-UX-007/008/014/015/016`, do not redefine).

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints, hygiene, methodology posture. |
| Internal contract | `../contracts/` (read-only) | Your section-part + id range, the surface map, the shared-vocab rule, the trace rule, identities. |
| Screen inventory | `../../SUBTASK_ia_interaction/outputs/ia-interaction.md` | The screens/routes/archetypes and the signed-out shell + auth-transition conventions you design into. |
| Component library | `../../SUBTASK_visual_system/outputs/visual-system.md` | The components (TextField, InlineError, PrimaryButton, Dialog, EmptyState, NavShell, …) you assemble these screens from. |
| Product requirements | `../../../SUBTASK_product_requirements/outputs/product-requirements.md` | Journeys J1–J3b and the `REQ-PROD-*` each screen serves and traces to. |

### Output
- `outputs/screens-get-in.md` — the **get_in** screens/flows at wireframe-level detail (each screen's
  layout, content, primary action, and empty/error/loading states), and `REQ-UX-040..050` entries
  (`statement`, testable `acceptance_criteria`, `release_gating`, ≥1 `REQ-PROD-*`). Repository-ready; no
  host/system/taskflow detail, no workspace paths, no attribution.

### Success criteria
- [ ] Composes against `../contracts/`, the screen inventory, and the component library; nothing redefined.
- [ ] Landing, sign-up, sign-in, recovery (both screens), and sign-out are each designed with their
      empty/error/loading states — or recorded out-of-scope with a reason.
- [ ] Each screen specifies layout, content, and a primary action — not a bare route name.
- [ ] Every `REQ-UX-040..050` is testable, `release_gating`-flagged, unique, in-range, and traces to ≥1
      `REQ-PROD-*`.

### Constraints
- Design only — no front-end code. Repository-ready hygiene on all output content.
- Methodology: Experience Design (primary); Identity & Trust, Product Strategy (support). Load bundle
  bodies on demand; if the `design` loader is unavailable, design from the bundle intent and competence
  and record the limitation (do not block).
- Write in a plain, checkable human voice; run the avoid-ai-writing checklist over the narrative before
  finalizing.
