# SYNTHESIS — core-loop screens subtree (SUBTASK_core_loop)

## What this fold does

This is the verification gate and fold for the core-loop screens subtree. It assembles the four spoke
outputs into the single deliverable `outputs/screens-core-loop.md` — the `core_loop` part of the parent
`screens_and_flows` section — in the order the seam fixes (timeline_reading → posting_conversation →
social_actions → profiles_discovery), consolidates the `REQ-UX-051..064` register, asserts the eight
contract identities with recorded evidence, and folds `SUBTASK_core_loop` to COMPLETED.

The gate does not redesign any screen. It reads the four COMPLETED spoke outputs, composes them, checks
the identities declared in `contracts/_MANIFEST.yaml`, and records the evidence below.

## Inputs read (all four spokes COMPLETED)

| Spoke | Output read | Surfaces | REQ-UX |
|---|---|---|---|
| `SUBTASK_timeline_reading` | `SUBTASK_timeline_reading/outputs/screens-timeline-reading.md` | Home timeline (reading, bounded pages, catch-up) | 051–053 |
| `SUBTASK_posting_conversation` | `SUBTASK_posting_conversation/outputs/screens-posting-conversation.md` | Compose & post; Chirp / conversation | 054–058 |
| `SUBTASK_social_actions` | `SUBTASK_social_actions/outputs/screens-social-actions.md` | Like/unlike; follow/unfollow (in-place) | 059–060 |
| `SUBTASK_profiles_discovery` | `SUBTASK_profiles_discovery/outputs/screens-profiles-discovery.md` | Public/Own profile; Followers/Following; Explore | 061–064 |

Internal seam read: `contracts/_MANIFEST.yaml`, `contracts/core_loop_seam.yaml` (read-only). Frozen
upstream vocabularies composed against by name: the Screen inventory (IA/interaction output) and the
Component library (visual-system output); the product requirements (journey J4, `REQ-PROD-001..007, 042`)
are the trace target.

## Assembly

`outputs/screens-core-loop.md` carries, in the seam's order (reading → writing → reacting → identity and
finding):

1. **Home timeline** — from `SUBTASK_timeline_reading`.
2. **Posting and conversation** (Compose & post; the Chirp / conversation screen) — from
   `SUBTASK_posting_conversation`.
3. **Social actions** (like/unlike; follow/unfollow) — from `SUBTASK_social_actions`.
4. **Profiles, followers/following, and discovery** — from `SUBTASK_profiles_discovery`.

followed by the consolidated `REQ-UX-051..064` register (14 entries). Each surface is reproduced with its
layout, content, primary action, and empty/error/loading states; nothing is redesigned.

## Identity assertions (recorded evidence; no silent plugs)

### 1. SURFACE_COVERAGE — PASS

Each of the seven core-loop surfaces is designed with its empty/error/loading states by exactly one
owning spoke; no hole, no double-write.

| Surface | Owner (per `core_loop_seam.yaml`) | Designed in the deliverable | States |
|---|---|---|---|
| home_timeline | `SUBTASK_timeline_reading` | Home timeline (`/`) | empty / error / loading |
| compose_and_post | `SUBTASK_posting_conversation` | Compose & post (ComposeBox, 3 placements) | empty / error (over-limit, failed-publish keep-draft) / loading |
| reply_and_conversation | `SUBTASK_posting_conversation` | Chirp / conversation (`/@:handle/chirp/:id`) | empty / error (tombstone, reply-to-gone, replies-fail) / loading |
| like_unlike | `SUBTASK_social_actions` | like control on every ChirpCard | default/active / error / loading |
| follow_unfollow | `SUBTASK_social_actions` | follow control on ProfileHeader + person rows | default/active / error (incl. self-follow refusal) / loading |
| view_profile | `SUBTASK_profiles_discovery` | Public profile, Own profile, Followers, Following | empty / error / loading each |
| discovery_find_people | `SUBTASK_profiles_discovery` | Explore (`/explore`) | empty (no-query vs no-results) / error / loading |

Every surface in the parent `required_surfaces` checklist maps to exactly one spoke; the ownership map in
`contracts/core_loop_seam.yaml` is fully covered.

### 2. ID_UNIQUE_IN_RANGE — PASS

The 14 ids `REQ-UX-051..064` each appear exactly once, in the owning spoke's sub-range, with no gaps,
collisions, or out-of-range ids (confirmed by a mechanical pass over the register):

- `051–053` → `SUBTASK_timeline_reading` (3 ids)
- `054–058` → `SUBTASK_posting_conversation` (5 ids)
- `059–060` → `SUBTASK_social_actions` (2 ids)
- `061–064` → `SUBTASK_profiles_discovery` (4 ids)

### 3. NOT_SKELETAL — PASS

Each designed screen specifies layout, content, and a primary action, plus its empty, error, and loading
states — none is a bare route name. The two social-action surfaces are in-place controls rather than
screens, and each is specified with where it sits, its content, its primary action, and its
default/active, error, and loading states, which meets the not-skeletal bar for a control.

### 4. UX_TESTABLE_AND_GATED — PASS

Every `REQ-UX-*` carries a `statement`, an `acceptance_criteria` a stranger could run on the live product,
and a `release_gating` flag. 12 are `release_gating: true`; the two `false` entries each carry a one-line
reason:

- `REQ-UX-057` (read a conversation) — `false`: reading replies as a navigable conversation rides the
  non-gating `REQ-PROD-004`; the gating reply requirement `REQ-UX-058` (`REQ-PROD-003`) already records
  the parent reference, so a first release may ship the reply action without the navigable read.
- `REQ-UX-064` (Explore / find people) — `false`: Explore implements the non-gating `REQ-PROD-042`; a
  first release may ship follow-by-profile and follow-from-a-reply and add discovery as a near-term
  follow-up, with the release bar deciding discovery v1 explicitly.

Both staged flags match the non-gating staging the seam's `trace_rule` note calls out
(`REQ-PROD-042`/`004`).

### 5. UX_TRACES_TO_PROD — PASS

Every `REQ-UX-*` references ≥1 `REQ-PROD-*` (mechanically confirmed):
051→002, 052→002, 053→002, 054→001, 055→001, 056→001+003, 057→004, 058→003, 059→005, 060→006, 061→007,
062→007, 063→007+006, 064→042. The referenced product requirements fall within journey J4's set
(`REQ-PROD-001..007, 042`).

### 6. COMPOSES_AGAINST_VOCAB — PASS

Every screen refers to screen-inventory screens by their inventory name and route (Home timeline `/`,
Compose `/compose` + overlay dialog, Chirp / conversation `/@:handle/chirp/:id`, Explore `/explore`,
Public/Own profile `/@:handle`, Followers `/@:handle/followers`, Following `/@:handle/following`), and is
built from component-library components by name. All 16 library components are used
(`NavShell`, `ListView`, `ChirpCard`, `ComposeBox`, `ProfileHeader`, `Avatar`, `IconButton`,
`PrimaryButton`, `SecondaryButton`, `TextField`, `Dialog`, `Toast`, `InlineFeedback`, `InlineError`,
`EmptyState`, `LoadingState`). Screens owned elsewhere are referenced, not redefined (Sign in, Sign up,
Onboarding `/welcome`, Not found, Edit profile `/settings/profile`). No screen or component outside the
frozen vocabularies is invented; no additive contract amendment was required.

### 7. STATES_CONSISTENT — PASS

Each per-screen empty/error/loading state is a composition of the relevant component's own named states
(`ListView.empty/error/loading`, `ChirpCard.error/loading`, `ComposeBox.empty/error/loading`,
`ProfileHeader.*`, `EmptyState`, `LoadingState`, `InlineError`, `InlineFeedback`, `Toast`) with the
product-wide empty/loading/error patterns and the expired-session / transient-error (keep-the-draft)
recovery owned by the sibling `SUBTASK_considered_states` spoke (the `empty_error_loading_states` section,
outside this subtree). Every spoke states that it composes that global treatment and does not invent a
conflicting per-screen pattern: the timeline routes an expired session to Sign in rather than dressing it
as a load error; compose/reply keep the draft on a failed publish and on a mid-action session expiry; the
social controls show a result at the control (not a Toast) per the transient-feedback convention. The
cross-reference in `core_loop_seam.yaml` is honoured; consistency holds across the assembled whole.

### 8. HYGIENE — PASS

`outputs/screens-core-loop.md` carries no host/system/taskflow detail, no workspace paths, no
agent/DAG/run ids, and no attribution trailer (confirmed by a mechanical scan for server address, SSH,
kubectl, k3d, ArgoCD, workspace-path fragments, `SUBTASK_`/`proc-` tokens, and attribution strings — no
hits). The one process-meta item present in a spoke output — the "methodology loader unavailable in this
environment" note at the end of `screens-profiles-discovery.md` — was kept OUT of the repository-ready
deliverable and the limitation is instead recorded here (see below). This is a transparent hygiene pass,
not a silent plug: the design substance of that spoke is reproduced in full; only the environment/process
note was relocated to this internal record.

## Gaps found and remediation

No failing identity. No surface hole, no id collision, no skeletal screen, no untraceable or ungated
requirement, no redefined or invented vocabulary, no inconsistent state treatment, no hygiene breach in
the deliverable. No remediation subtree was required.

One hygiene relocation (not a gap in the design): a process note about the methodology-loader environment
was excluded from the repository-ready deliverable and recorded here.

## Methodology limitation (recorded, non-blocking)

The Phase-B `design` methodology loader is unavailable in this reconstructed environment (the loader
reports the agent domain unset). Per the ancestor hubs' recorded posture, the spokes designed from the
named bundle intent — Experience Design (primary) and Product Strategy (support) — and product-design
competence, and this gate verified from the bundle intent and the contract identities. The limitation did
not block the assembly or the verification.

## Fold

All eight identities hold with the evidence above. The deliverable `outputs/screens-core-loop.md` carries
all seven core-loop surfaces (each from exactly one spoke, in seam order) and the complete, unique,
in-range, testable, gated, `REQ-PROD`-traced `REQ-UX-051..064` register. `SUBTASK_core_loop` is folded to
COMPLETED. Its consolidated `core_loop` part and the `REQ-UX-051..064` register are ready for the parent
screens-&-flows synthesis to consume when it builds the `screens_and_flows` section and the consolidated
`REQ-UX-040..089` register.
