# COMPLETE — SUBTASK_safety_notifications

## What this task was
Design the safety, notifications, and public-explanatory surfaces of the `screens_and_flows`
section-part owned by this spoke, each a designed screen (layout, content, primary action, and
empty/error/loading states) composed against the frozen screen inventory and component library, and
mint `REQ-UX-078..085`.

## Decompose-evaluation
`Atomic`. The brief enumerates seven surfaces, but they are leaf screens of one design area (safety/
notifications) designed with one methodology from one frozen component library against one journey
cluster (J7 + the J9 entry) into one 8-id range — one kind of change producing one kind of output.
The Single-Responsibility and conjunction tests pass; the token, tool-call, and output-size triggers
clear; the Distinct Concerns Test does not fire (splitting the tightly-coupled report→rules and
block→blocked-&-muted surfaces would manufacture seams, not separate genuine concerns). Runtime
confirmed the call: the work stayed one responsibility, the output is 342 lines, and the invocation
used well under the atomic tool-call envelope. No falsification signal fired.

## What was produced
- `outputs/screens-safety-notifications.md` — the `safety_notifications` part of `screens_and_flows`,
  wireframe-level detail for seven surfaces, plus the `REQ-UX-078..085` register.

### Surfaces designed (each with layout, content, primary action, empty/error/loading states)
1. **Notifications** (`/notifications`, feed/list) — activity surface; unseen indicator + cleared
   state; J7 / REQ-PROD-029.
2. **Report** (modal/dialog) — report a chirp or account against a stated rule, with a receipt
   acknowledgement; J7 / REQ-PROD-025, 026.
3. **Block / mute** (confirmation) — stops unwanted interaction with the effect stated; J7 /
   REQ-PROD-027.
4. **Blocked & muted** (`/settings/blocks`, settings) — manage blocked/muted accounts; J7 /
   REQ-PROD-027.
5. **Help & support** (`/help`, empty/landing) — user-facing entry to recovery, reporting, and
   contacting the operator (entry only); J9 entry / REQ-PROD-028, 013.
6. **Rules & terms** (`/rules`, empty/landing) — the stated rules a report references; J7 /
   REQ-PROD-026.
7. **Not found** (any unresolved path, empty/landing) — explains an absent/removed resource and routes
   back; REQ-PROD-033.

### REQ-UX register
`REQ-UX-078..085` (8 ids), each with a `statement`, a stranger-testable `acceptance_criteria`, a
`release_gating` flag, and ≥1 `REQ-PROD-*` reference. Non-gating staging honoured where the
implemented product requirement is non-gating: 078 (REQ-PROD-029), 080 and 081 (REQ-PROD-027) carry
`release_gating: false` with reasons; 079, 082, 083, 084, 085 are gating.

## How it composes with the parent
Written as the `safety_notifications` part of `screens_and_flows`, the one section-part this spoke
owns in `../contracts/`. All seven surfaces refer to screen-inventory screens by name and are built
from component-library components by name; nothing in the frozen vocabularies is redefined, and no new
screen or component is introduced (the notifications row is the "row kind the screen needs" that
ListView provides for). Sibling-owned surfaces — the notification preferences sub-section, the
Settings hub, and Recover access — are cross-referenced, not redesigned. Per-screen empty/error/
loading states compose the component library's named states and the product-wide patterns owned by
`SUBTASK_considered_states`; the subtree synthesis asserts STATES_CONSISTENT across the assembled
whole.

## Limitation recorded
The `design` methodology loader is unavailable in the reconstructed environment (`agent_domain_unset`);
per the brief and hub, the surfaces were designed from the named bundle intent (Experience Design
primary; Identity & Trust and Product Strategy in support) and product-design competence, and the
limitation is noted in the deliverable.

## Checks
- Composes against `../contracts/`, the screen inventory, and the component library; nothing redefined.
- All seven required surfaces designed with their empty/error/loading states (or a state recorded
  not-applicable with a reason).
- Each screen specifies layout, content, and a primary action — not a bare route name.
- Every `REQ-UX-078..085` is testable, `release_gating`-flagged, unique, in-range, and traces to ≥1
  `REQ-PROD-*`.
- Repository-ready hygiene verified: no host/system/taskflow detail, no workspace paths, no
  agent/DAG/run ids, no attribution trailers in the deliverable.
- avoid-ai-writing pass run by hand (P0/P1); flagged tells removed.
