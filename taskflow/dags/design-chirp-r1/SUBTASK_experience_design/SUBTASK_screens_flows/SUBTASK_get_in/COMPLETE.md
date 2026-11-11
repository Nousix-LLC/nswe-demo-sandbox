# COMPLETE — SUBTASK_get_in

## Decompose evaluation
`Atomic`. Applied the decomposition triggers to this brief at the evaluation point: Token clears
(inputs read, well under context; one output document); Single-Responsibility clears ("design the
entry & auth screens" — one verb, one kind of output: designed screens + their states + a contiguous
REQ-UX range); Distinct-Concerns clears (six instances of one concern — the signed-out↔signed-in
boundary — over one shell, one component vocabulary, one archetype family, interlinked transitions, a
contiguous id range, not distinct kinds needing separate specialists); enumerated-concerns weighed and
cleared (the genuinely-distinct concerns were separated one level up). Output-size fired (~400-700
lines) but is the weakest signal and is subordinated by the fixed precedence rule to the passing
Single-Responsibility and Distinct-Concerns tests. Tool-call envelope well within atomic range; no
"draw the rest of the owl" gap (full component library, screen inventory, and requirements in hand).
Evaluated fresh against my own brief, not against the parent's split.

## What was done
Designed the `get_in` part of the screens-and-flows section — the entry and authentication screens a
releasable chirp needs — and minted the `REQ-UX-040..050` register.

Surfaces designed, each with layout, content, one primary action, and its empty/error/loading states:
- **Landing** (`/` no session) — explains chirp, offers Sign up / Sign in without an account, shows a
  public sample where available; never dead-ends.
- **Sign up** (`/signup`) — handle / display name / optional bio / credential / verified contact;
  live handle format + uniqueness feedback; lands on Onboarding.
- **Sign in** (`/signin`) — proves ownership (credential beyond the handle); distinct no-such-account
  vs wrong-credential signals.
- **Recover access** (`/recover`) — self-service recovery through the verified contact, non-disclosing
  response.
- **Set new credential** (`/recover/confirm`) — completes recovery, handles an expired link, returns
  to Sign in.
- **Sign out** (confirmation Dialog) — ends the session server-side, optionally all devices; a failed
  sign-out leaves the session intact.
- **The transitions** between them, composed against the IA interaction model.

## Output produced
- `outputs/screens-get-in.md` — the designed screens + the `REQ-UX-040..050` entries
  (`statement`, `acceptance_criteria`, `release_gating`, `references` ≥1 `REQ-PROD-*`).

## How it composes with the parent
Feeds `SUBTASK_synthesis`, which assembles the `screens_and_flows` section (this is its `get_in` part,
first in the assembled order) and consolidates the `REQ-UX-040..089` register. Composes against the
frozen screen inventory and component library by name, and against the parent/subtree contracts for the
`REQ-UX` format, the `040..050` sub-range, the required surfaces, the shared-vocabulary rule, and the
trace rule. Nothing upstream was redefined; no screen or component was invented outside the frozen
vocabularies, so no additive contract amendment was required. Transition conventions
(REQ-UX-007/008/014/015/016) and the global empty/error/loading patterns (owned by
`SUBTASK_considered_states`) are composed against, not restated.

## Identities self-checked (final assertion is SUBTASK_synthesis's)
SURFACE_COVERAGE, NOT_SKELETAL, ID_UNIQUE_IN_RANGE (11 contiguous ids 040..050),
UX_TESTABLE_AND_GATED, UX_TRACES_TO_PROD, COMPOSES_AGAINST_VOCAB, STATES_CONSISTENT, HYGIENE — all hold
for this part.

## Methodology limitation (recorded per brief and subtree posture)
The Phase-B `design` methodology loader was unavailable in the current reconstructed environment (the
loader syscall reported the agent domain unset). Per the brief's fallback and the subtree hub's
recorded posture, these screens were designed from the named bundle intent — Experience Design
(primary), Identity & Trust and Product Strategy (support, so the auth/account screens align with the
identity requirements) — and principal-product-design competence. This did not block the work; it is
recorded here rather than in the repository-ready deliverable to keep that deliverable hygienic.
