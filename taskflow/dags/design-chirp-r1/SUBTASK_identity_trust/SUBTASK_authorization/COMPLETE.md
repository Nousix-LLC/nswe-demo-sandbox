# COMPLETE — SUBTASK_authorization

## What was done
Designed chirp's **authority model** — what each actor may see and change — as the `authorization`
section partial, authored to the format fixed by `../contracts/req_id_partition.yaml`. Authentication
(proving identity) is taken as established by the sibling `SUBTASK_auth_sessions`; this node specifies
what a proven identity, and an unauthenticated viewer, are authorized to do.

## Output produced
- `SUBTASK_authorization/outputs/authorization.md` — section prose (default-deny premise, a single
  field model: public / owner-only / owner-scoped, and the state-today grounding) plus `REQ-ID-060..074`
  and notes for synthesis.

## Coverage of the three distinct concerns the brief named
- **Actor-scoped action authority** — `REQ-ID-064` (act only as yourself, no impersonation), `065`
  (social write actions as the actor), `066` (change only your own account), `067` (remove only your own
  content/account), `068` (attribution bound to the actor, non-forgeable).
- **Read / visibility boundary** — `REQ-ID-061` (unauthenticated read = public fields only), `062`
  (owner-only fields readable by owner alone), `063` (owner-scoped views served only to their owner),
  `069` (refusals disclose nothing beyond the public surface); `060` sets the default-deny foundation.
- **Operator / admin / support authority** — `REQ-ID-070` (separate provisioned role), `071`
  (least-privilege supported action set), `072` (no impersonation, no credential read), `073`
  (attributable and auditable), `074` (defined, recorded removal/actioning outcome).

## Composition against contracts (verified)
- Ids only within the owned range `REQ-ID-060..079` (used `060..074`; `075..079` left as headroom).
- Only inherited fields and the inherited verification-method vocabulary
  (`manual_user_check | automated_test | inspection | operational_check`) are used; the id format,
  required fields, verification vocabulary, and design-artifact map are composed against, not redefined.
- Every `REQ-ID-*` traces to ≥1 existing `REQ-PROD-*` (traces drawn from `001, 002, 003, 005, 006, 007,
  010, 011, 016, 017, 020, 021, 023, 024, 025, 028`, all present in the product-requirements register).
- Primary `REQ-PROD` targets from the partition (`023, 024, 028, 007`) are all carried.

## Coordinated by prose (no duplication)
- Public-vs-private field split: this section owns the authority boundary (who may read/write);
  `SUBTASK_abuse_privacy` owns the data-protection rules (minimization, retention, erasure) over the
  same owner-only field set.
- Block/mute (`REQ-PROD-027`), session invalidation/sign-out (`REQ-PROD-014`), recovery mechanism, and
  deletion outcome (`REQ-PROD-021`) are referenced and attributed to their owning siblings, not minted
  here.

## Notes left for SUBTASK_synthesis
- Threat hints per requirement (spoofing/elevation, tampering/attribution, repudiation, information
  disclosure) for the STRIDE threat model.
- Candidate cross-cutting requirements (transport confidentiality, anti-automation) flagged as NOT
  covered here, so synthesis can place them in its own `REQ-ID-100..119` range rather than assume owned.

## Checks run
- Writing-voice / avoid-AI-writing pass over the partial (P0/P1 tells): clean.
- Repository hygiene: deliverable carries no host/system/taskflow detail and no attribution trailer;
  state-today grounding named by repository identity (`Nousix-LLC/nswe-demo @ c805525`) only.
- Requirements only; no implementation "how"; no ids outside the owned range; no `BAR-*`.
