# COMPLETE — SUBTASK_social_actions

## What was done
Designed the two in-place social-action behaviors of the core loop — like/unlike and follow/unfollow —
as designed controls (where they sit, content, primary action, and their default/active, error, and
loading states), and minted `REQ-UX-059..060`. Delivered one output:
`outputs/screens-social-actions.md`.

## Decompose evaluation
Atomic. The brief is one responsibility — specify the in-place social-action controls (two cohesive
controls sharing one state model: optimistic flip, revert-on-error with `InlineFeedback` danger,
busy-while-in-flight), one kind of output into one file. Token/scope/output triggers and both concern
tests cleared; the two controls are one concern, not two distinct analyses. Evaluated independently of
the parent's split.

## How it composes (nothing redefined)
- Like control = the like `IconButton` on every `ChirpCard`; liked state = `color.like` + filled heart
  + "Liked" label (never colour alone), per the `ChirpCard`/`IconButton` definitions.
- Follow control = `PrimaryButton` "Follow" / `SecondaryButton` "Following" on `ProfileHeader` and on
  the person rows the discovery/list screens present; own-profile action is "Edit profile".
- Error = optimistic change reverted + `InlineFeedback` danger at the control; loading = each control's
  own busy treatment. Success is carried by the control's own state change (no redundant `Toast`), per
  the product's transient-feedback convention.
- The host surfaces (cards, headers, person rows, the people lists) are owned by the timeline,
  posting/conversation, and profiles/discovery spokes and are not designed here. No screen or component
  was invented; no additive contract amendment was needed.

## Requirements
- `REQ-UX-059` (like) → `REQ-PROD-005`; `REQ-UX-060` (follow) → `REQ-PROD-006`. Both in sub-range
  059..060, unique, `release_gating: true`, each with stranger-testable live-product acceptance criteria
  covering idempotency, accurate count, cannot-follow-self, and error/loading behavior.

## Success criteria
- [x] Composes against the subtree contract and the frozen component library; nothing redefined.
- [x] Like/unlike and follow/unfollow each designed with default/active, error, and loading states,
      including idempotency, accurate count, and cannot-follow-self.
- [x] Each behavior states where it sits, its content, and its primary action — not a bare name.
- [x] Every `REQ-UX-059..060` is testable, `release_gating`-flagged, unique, in-range, and traces to a
      `REQ-PROD-*`.
- [x] Plain, checkable voice; avoid-ai-writing checklist run over the narrative before finalizing.

## Methodology limitation (recorded, non-blocking)
The `design` methodology loader was unavailable in this reconstructed environment (the loader syscall
reports the agent domain unset). Per the subtree hub's recorded posture, the design was produced from
the named bundle intent — Experience Design (primary), Product Strategy (support) — and product-design
competence. This limitation did not reduce coverage of the brief.

## Output
- `outputs/screens-social-actions.md`
