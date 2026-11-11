# Release bar — screens & flows: safety, help, rules, not-found & cross-screen state patterns

Chapter sub-fragment of the screens-&-flows UX release bar. Owns `BAR-256..263` (8 ids) enforcing the nine
release-gating experience requirements of this chapter: the safety/help/rules/not-found surfaces
(`REQ-UX-079, 082, 083, 084`) and the product-wide cross-screen state patterns
(`REQ-UX-085, 086, 087, 088, 089`). Each criterion is a release condition a stranger can check against the
live product, stated in the user's terms — not a restatement of the requirement and not an implementation.

The id budget is tight (8 ids, 9 gating requirements), so the considered-states umbrella (`REQ-UX-085`) and
the empty-treatment specific (`REQ-UX-086`) are clustered into one checkable condition (`BAR-260`). Non-gating
requirements in this band — `REQ-UX-078` (notifications surface), `REQ-UX-080` (block/mute), `REQ-UX-081`
(managing blocked/muted) — are not covered here; where one is named in a statement it is context, never the
basis of a criterion.

---

## BAR-256 — Reporting a chirp or an account is acknowledged, and a reasonless report cannot be sent

- **id**: BAR-256
- **statement**: Signed in, a person can open the report action from both a chirp's and an account's
  more-actions menu, choose a reason, add optional detail, and submit, and sees an in-product confirmation
  that the report was received; and when no reason is chosen the submit control does not send the report.
  No report path ends in a silent no-op.
- **references**: REQ-UX-079 (serves REQ-PROD-025, REQ-PROD-026)
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

## BAR-257 — The product's rules are stated as named categories reachable from both shells, and a report's reasons map to them

- **id**: BAR-257
- **statement**: From both the signed-out and the signed-in shell, a person can reach a Rules & terms screen
  that lists the product's rules as named categories; and the reasons offered in the report action correspond
  to those same named categories, so a submitted report points at a stated rule rather than an unlabelled
  choice.
- **references**: REQ-UX-083 (serves REQ-PROD-026)
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

## BAR-258 — Help & support is reachable from both shells and leads to recovery and to a person

- **id**: BAR-258
- **statement**: A Help & support entry is reachable with no session from the signed-out shell and, signed in,
  from the account menu; from it a person can reach the recover-access path ("Can't get in?") and a way to
  contact the operator ("Contact support") for what self-service does not cover.
- **references**: REQ-UX-082 (serves REQ-PROD-028, REQ-PROD-013)
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

## BAR-259 — An unresolved or removed address lands on a not-found screen that explains, protects privacy, and offers a way back

- **id**: BAR-259
- **statement**: Opening an address that does not resolve — a mistyped path, a deleted chirp, an unavailable
  account — shows a not-found screen that states the resource is missing (consistent with the in-place
  tombstone used elsewhere), reveals no private detail about a removed or restricted resource, and offers a
  route to a known place (the home timeline when signed in, the landing when signed out) rather than a broken
  page.
- **references**: REQ-UX-084 (serves REQ-PROD-033)
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

## BAR-260 — Every surface in this area shows a considered empty, error, and loading state, and an explained-empty surface is told apart from a failed one

- **id**: BAR-260
- **statement**: On each surface in this area a person can force an empty result, a failed load, and a first
  load and sees, respectively, an explained empty treatment carrying at least one next step (never a blank
  region), a distinct "couldn't load — try again" treatment with a retry, and a loading treatment — with the
  empty treatment and the failed treatment visibly different from each other; a surface to which one of these
  states does not apply says so rather than showing nothing. Checked across, for example, Notifications, the
  report and block/mute dialogs on a failed submit (the dialog stays open with its input preserved and an
  inline error), the blocked & muted screen when empty, a brand-new home timeline, and an empty followers
  list.
- **references**: REQ-UX-085, REQ-UX-086 (serve REQ-PROD-033, REQ-PROD-034)
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

## BAR-261 — Loading shows the shape of what is coming, keeps the navigation frame, and never spins forever

- **id**: BAR-261
- **statement**: On a slow connection a first load of a content surface shows skeletons sized to the real
  content — not a spinner on a blank page — while the persistent navigation frame stays visible; an
  incremental load, such as loading older items, shows a bounded indicator at the point of the action while
  the already-loaded content stays on screen; and a load that cannot resolve stops and becomes an error with
  a retry rather than spinning without end.
- **references**: REQ-UX-087 (serves REQ-PROD-033)
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

## BAR-262 — Failures appear where the action was taken, in plain words with no code, and always leave a way forward

- **id**: BAR-262
- **statement**: A person who triggers a field error (for example a taken handle at sign-up), a failed
  in-place action (for example a like or follow that fails), and a failed list page sees in each case a
  plain-language message at the point of the problem — no system or error code, never a silent no-op and
  never a blank — with a way to retry or correct and their input preserved; an optimistic in-place action
  that fails reverts to its prior state rather than showing a result that did not happen.
- **references**: REQ-UX-088 (serves REQ-PROD-033)
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

## BAR-263 — An expired session and a transient error both recover with in-progress work preserved

- **id**: BAR-263
- **statement**: With a session expired, a person who drafts a chirp and tries to post is routed to sign-in
  with the reason stated — not a silent failure — and, after signing in, is returned to where they were with
  the drafted text intact; and a transient server error during the same post can be retried in place and
  succeeds without re-typing the draft. This observes, and does not redefine, the information architecture's
  session-expiry (REQ-UX-008) and auth-gated-return (REQ-UX-007) conventions.
- **references**: REQ-UX-089 (serves REQ-PROD-034)
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

---

## Coverage note — this chapter's release-gating REQ-UX-* → the BAR-* that covers it

Every release-gating requirement in this chapter's set is covered by at least one `BAR-*` above. The set is
read from the experience design's per-requirement `release_gating: true` field; it is restated here as the
mapping the synthesis gate asserts (`SCREENS_GATING_REQ_COVERAGE` for this chapter) without re-deriving it.

| Release-gating REQ-UX-* | Covered by | What the criterion checks |
|---|---|---|
| REQ-UX-079 — report acknowledged as received | BAR-256 | report submitted from chirp and account menus, acknowledged; reasonless submit prevented; never a silent no-op |
| REQ-UX-082 — help & support from both shells | BAR-258 | Help & support reachable from both shells, reaching recovery and operator contact |
| REQ-UX-083 — stated rules a report points to | BAR-257 | rules as named categories reachable from both shells; report reasons correspond to them |
| REQ-UX-084 — not-found screen explains and routes back | BAR-259 | unresolved/removed address → not-found screen; no private leak; route back to a known place |
| REQ-UX-085 — considered empty/error/loading per surface | BAR-260 | each surface shows considered empty/error/loading states (or states N/A) |
| REQ-UX-086 — empty explained, never blank; distinct from failed | BAR-260 | explained empty treatment with a next step; empty visibly distinct from failed |
| REQ-UX-087 — loading shows shape, never forever | BAR-261 | skeletons at real dimensions; nav frame persists; unresolved load → error with retry |
| REQ-UX-088 — failures at the point of action, plain words, way forward | BAR-262 | plain-words failure at the point of action, no code, retry/correct with input preserved, optimistic action reverts |
| REQ-UX-089 — expired session & transient error recover without losing work | BAR-263 | session-expiry re-auth-and-return with draft intact; transient error retryable in place |

**Chapter gating coverage**: 9 / 9 release-gating requirements referenced (`REQ-UX-079, 082, 083, 084, 085,
086, 087, 088, 089`).

**Not covered (non-gating in this band)**: `REQ-UX-078` (notifications surface), `REQ-UX-080` (block/mute),
`REQ-UX-081` (managing blocked/muted) — each `release_gating: false` in the experience design; none is the
sole basis of any `BAR-*` above.

**Ids minted**: BAR-256, BAR-257, BAR-258, BAR-259, BAR-260, BAR-261, BAR-262, BAR-263 — 8 ids, all within
the assigned `BAR-256..263` sub-range.
