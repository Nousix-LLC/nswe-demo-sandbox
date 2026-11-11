# Release bar — entry & auth chapter (BAR-230..237)

The release conditions for the surfaces a person meets before and during getting into chirp:
the Landing, sign-up, sign-in, recover access, set new credential, and sign-out, their empty/
error/loading states, and where each flow lands the person. Each `BAR-*` enforces one or more
release-gating `REQ-UX-040..050` from `design/experience-design.md`; it states a condition a
person who was not in the room can check against the live product, not a restatement of the
requirement and not an implementation. The id budget is tight by design, so related gating
requirements are clustered into one condition where they are checked in the same pass.

Fields per block: `id`, `statement`, `references` (the `REQ-*` it enforces), `verification_method`
(one of `manual_user_check`, `automated_test`, `inspection`, `operational_check`), `proposed_stage`
(`usable_early` | `releasable` — this chapter's proposal; the screens synthesis finalizes one stage
per criterion).

---

### BAR-230
- **statement**: With no session, opening the site root reaches a Landing that says what chirp is
  and shows both a Sign up and a Sign in action, each reachable without first signing in. Where a
  public sample is served it shows real public chirps; where none is served the Landing still
  explains chirp and offers both actions rather than a blank area.
- **references**: REQ-UX-040 (REQ-PROD-030, REQ-PROD-031)
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

### BAR-231
- **statement**: The Sign up screen collects a handle, a display name, an optional bio marked
  optional, a credential, and a point of contact — and no fields beyond these — and on submit with
  valid values creates the account and signs the person in. The contact is shown as pending
  verification and is not treated as confirmed until it is verified.
- **references**: REQ-UX-041, REQ-UX-043 (REQ-PROD-008, REQ-PROD-012, REQ-PROD-031)
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

### BAR-232
- **statement**: On the Sign up screen a handle that is already taken, or that breaks the rule (more
  than 15 characters, or anything other than letters, numbers, or underscores), is reported inline
  against the handle field so the person can fix it before submitting, and a valid unused handle
  resolves to accepted. The check does not disclose which other handles exist beyond the conflict it
  reports.
- **references**: REQ-UX-042 (REQ-PROD-009)
- **verification_method**: automated_test
- **proposed_stage**: usable_early

### BAR-233
- **statement**: Signing in requires the credential set at sign-up or recovery — a known handle
  alone never grants a session. A handle that matches no account returns a not-found result with a
  path to Sign up; a real handle with a wrong credential returns a failed sign-in the person can
  retry or recover from, with a path to Recover access. Neither result reveals account existence
  beyond what a public profile already shows, and neither shows a system code.
- **references**: REQ-UX-044, REQ-UX-045 (REQ-PROD-010, REQ-PROD-011)
- **verification_method**: automated_test
- **proposed_stage**: usable_early

### BAR-234
- **statement**: A person who cannot sign in can start recovery themselves from a Recover access
  screen that runs through the account's verified contact. Submitting a contact returns the same
  neutral acknowledgement whether or not it matches an account, so the response discloses no account
  existence. Following a valid recovery step opens a Set new credential screen, and after setting a
  new credential the person is routed to Sign in and can sign in with it. An expired or already-used
  recovery link is explained with a path back to Recover access rather than a dead end.
- **references**: REQ-UX-046, REQ-UX-047 (REQ-PROD-013, REQ-PROD-012)
- **verification_method**: automated_test
- **proposed_stage**: releasable

### BAR-235
- **statement**: Signing out is confirmed before it proceeds; the confirmation names the consequence
  and offers both a cancel and an option to end sessions on all other devices. Confirming ends the
  current session on the server — the prior session can no longer be used — and lands the person on
  the signed-out Landing. Cancelling changes nothing. A sign-out that fails is reported and leaves
  the person signed in rather than appearing to succeed.
- **references**: REQ-UX-048 (REQ-PROD-014)
- **verification_method**: automated_test
- **proposed_stage**: usable_early

### BAR-236
- **statement**: Each of the Landing, Sign up, Sign in, Recover access, Set new credential, and Sign
  out surfaces presents a designed state for empty, loading, and error — a field-level message, a
  busy control, a skeleton, or an explained error with a next step — rather than a blank area, a
  hang, or a silent failure. Where a state does not apply to a surface, that is stated rather than
  left undesigned.
- **references**: REQ-UX-049 (REQ-PROD-033, REQ-PROD-034)
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

### BAR-237
- **statement**: A completed sign-up lands the person on the onboarding screen, not a sign-in prompt
  or a blank page. A person routed from a signed-in-only screen to Sign in lands back on the screen
  they asked for after signing in. After signing out, pressing back does not show the protected
  screen's content. (The three-way links among Sign in, Sign up, and Recover access ride the
  non-gating REQ-UX-015 and are not part of this release condition; a first release may omit them
  provided Recover access stays reachable from Help & support.)
- **references**: REQ-UX-050 (REQ-PROD-032, REQ-PROD-014)
- **verification_method**: automated_test
- **proposed_stage**: releasable

---

## Coverage note — entry & auth chapter

Every release-gating `REQ-UX-*` in `040..050` (11 total) and the `BAR-*` that covers it. All eight
ids fall within this chapter's assigned sub-range `BAR-230..237`.

| REQ-UX | Gating surface | Covered by |
|--------|----------------|-----------|
| REQ-UX-040 | Landing explains chirp, reachable with no session | BAR-230 |
| REQ-UX-041 | Sign-up creates an account from only what it needs | BAR-231 |
| REQ-UX-042 | Handle format and uniqueness reported against the field | BAR-232 |
| REQ-UX-043 | Sign-up captures a contact marked to-be-verified | BAR-231 |
| REQ-UX-044 | Sign-in requires the person's own credential | BAR-233 |
| REQ-UX-045 | Sign-in distinguishes no-account from wrong-credential, no existence leak | BAR-233 |
| REQ-UX-046 | Self-service recovery through the verified contact, neutral no-leak | BAR-234 |
| REQ-UX-047 | Set new credential completes recovery, returns to sign-in, no dead end | BAR-234 |
| REQ-UX-048 | Sign-out confirmed, ends the session, offers all devices | BAR-235 |
| REQ-UX-049 | Each entry/auth surface has designed empty/error/loading states | BAR-236 |
| REQ-UX-050 | Land on the right place; no back-leak (gating basis only) | BAR-237 |

All 11 release-gating requirements are covered. No non-gating `REQ-UX-*` fall in `040..050`, so no
criterion here rests on a non-gating requirement. `REQ-UX-050` is covered against its gating basis
(the sign-up→onboarding landing and the sign-out no-leak, REQ-PROD-032 and REQ-PROD-014); its
three-way interlinks are non-gating and are not used to justify BAR-237.
