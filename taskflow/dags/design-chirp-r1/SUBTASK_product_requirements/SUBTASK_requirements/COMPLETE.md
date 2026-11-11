# COMPLETE — SUBTASK_requirements

**Task**: Mint the testable `REQ-PROD-*` register and the consolidated in-scope/out-of-scope
statement for chirp (`Nousix-LLC/nswe-demo` @ `c805525`).

**Decompose evaluation**: Atomic — one responsibility (formalize already-surfaced needs into the
product-level requirement register plus the scope consolidation), one kind of output, drawn from
two already-complete precursor fragments. Output Size was the only leaning trigger and, per the
kernel's fixed Trigger Precedence, does not drive decomposition when no scope/concern/
responsibility trigger has fired.

## What was produced

`SUBTASK_requirements/outputs/requirements.md` — repository-ready design content carrying the two
sections this task owns:

- **`requirements_and_acceptance_criteria`** — 42 requirements, `REQ-PROD-001` … `REQ-PROD-042`,
  each with `id`, `statement`, a stranger-exercisable `acceptance_criteria`, and a `release_gating`
  flag. Organized by theme: core loop (001–007); accounts & identity lifecycle (008–015); account
  management (016–018); leaving — export & deletion (019–022); authorization & privacy (023–024);
  safety, moderation & support (025–028); notifications (029); experience quality (030–036);
  durability & operational readiness (037–041); finding people (042). A traceability section maps
  every product-kind implication and every journey (J1–J10) to the ids.
- **`in_scope_out_of_scope`** — consolidates the product-definition kind-lens scope draft with what
  the register settles; every out-of-scope concern carries a reason.

## Success criteria — met

- Every `REQ-PROD-*` carries id / statement / stranger-testable acceptance_criteria / release_gating.
- Every end-to-end journey (incl. first visit, daily use, and leaving: deletion & export) traces to
  ≥1 `REQ-PROD-*` (traceability table).
- Each product-kind implication is reflected in a requirement or recorded out-of-scope with a reason.
- `in_scope_out_of_scope` stated; out-of-scope concerns carry reasons.
- Composes against the inherited `../../contracts/id_and_traceability_schema.yaml` (uses
  `REQ-PROD-NNN`, the four `each_requirement_has` fields) and the subtree section-ownership map;
  redefines no inherited schema; mints no other area's ids (sibling areas `REQ-DOM/UX/ID/OPS-*` and
  `BAR-*` are referenced as pointers only). Repository hygiene holds (no host/system/taskflow detail,
  no attribution trailer; repository-identity naming).

## Judgment recorded for the synthesis gate

- **Release-gating calls.** `release_gating: false` on REQ-PROD-004, 015, 018, 027, 029, 031, 042 —
  each in scope and expected but staged as non-blocking for a first release, with a stated reason.
  The two findings that break a basic releasable-product assumption are gated `true`: owner-only
  sign-in (REQ-PROD-010, the handle-only-auth finding) and durable data (REQ-PROD-037, the in-memory
  store blocker). The final MVP-vs-releasable staging of the non-gating items is the release-bar
  design's (`BAR-*`) to settle; this register hands it the requirements and the flags.
- **Self-hosting (J10/P5).** Durability (037) and the account-lifecycle requirements are written to
  hold for any deployment, so an instance someone runs inherits them; chirp as a *supported
  self-hosting product* is recorded out of scope, consistent with the product-definition fragment's
  closed-demonstration kind call. J10 therefore traces to REQ-PROD-037 for the in-scope part.

## Assumption / limitation

The `design` methodology surface was unreachable from this reconstructed node (the methodology
syscalls returned `agent_domain_unset`; the domain binding was not restored on reconstruction).
The brief mapped this task to Product Strategy (primary), Release Definition, and Delivery
(supporting). The work proceeded on the principal-product-designer persona (which embodies that
judgment), the brief, the read-only contracts, and the two complete precursor fragments, which had
already done the analytic work and supplied a journey→need table and a kind-lens scope draft. No
methodology-specific claim was fabricated; the register is grounded in those inputs and the product
as it exists at `c805525`. If a later pass restores methodology access, the register should be
re-checked against the Release Definition bundle's gating conventions, but the content above is a
sound, self-contained requirement register as it stands.

**Output**: `SUBTASK_requirements/outputs/requirements.md`
