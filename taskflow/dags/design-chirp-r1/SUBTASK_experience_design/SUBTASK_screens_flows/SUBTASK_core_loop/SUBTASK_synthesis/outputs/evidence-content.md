# Content evidence: core-loop screens

Four content-quality identities checked against the core-loop screens document. Overall result: three PASS (UX_TESTABLE_AND_GATED, UX_TRACES_TO_PROD, COMPOSES_AGAINST_VOCAB) and one FAIL (STATES_CONSISTENT, three gaps). Verification only; nothing was edited. Limitation: STATES_CONSISTENT used the considered-states patterns that were present; no identity was verified without its reference source.

---

# UX_TESTABLE_AND_GATED

**Verdict: PASS**

## Checks performed
Read the "Requirements register — REQ-UX-051..064" section of `screens-core-loop.md` (lines 649–846). For each id: (1) a statement exists; (2) acceptance criteria exist and name actions and observable results a stranger can run on the live product; (3) a `release_gating` flag exists; (4) every `false` flag carries a one-line reason. Nothing was edited.

## Findings (one row per id)
| REQ-UX | Line | Statement | Acceptance criteria checkable | release_gating | Reason when false |
|---|---|---|---|---|---|
| 051 | 655 | present | yes (open `/`, order, load-older) | true | n/a |
| 052 | 667 | present | yes (second account posts, catch-up control, back keeps position) | true | n/a |
| 053 | 679 | present | yes (empty, forced first-page fail, load-older fail, slow connection) | true | n/a |
| 054 | 695 | present | yes (counter, warning, over-limit, empty, disabled Post) | true | n/a |
| 055 | 709 | present | yes (busy state, offline failure keeps draft, no duplicate) | true | n/a |
| 056 | 724 | present | yes (three placements, labels, disabled empty state, dialog draft kept) | true | n/a |
| 057 | 740 | present | yes (Replying to relation, order, reply count, load older) | false | present (rides REQ-PROD-004, not gated; parent reference covered by REQ-UX-058) |
| 058 | 755 | present | yes (reply, deleted-chirp not-found, signed-out sign-in path) | true | n/a |
| 059 | 769 | present | yes (liked state not colour alone, idempotence, forced failure, consistency across three screens) | true | n/a |
| 060 | 786 | present | yes (follow, repeat, unfollow, own profile, forced failure, consistency) | true | n/a |
| 061 | 804 | present | yes (signed-out and signed-in profile) | true | n/a |
| 062 | 815 | present | yes (own profile, Edit profile, no follow control) | true | n/a |
| 063 | 825 | present | yes (followers/following by count, direct URL, per-row follow) | true | n/a |
| 064 | 837 | present | yes (search, follow in place, no-results vs before-search) | false | present (Explore implements REQ-PROD-042, not gated) |

All 14 ids (051–064) are present; none missing or duplicated. 12 are gating, 2 are not (057, 064), both with a stated reason.

## Citations
REQ-UX-051..064 headings at lines 655, 667, 679, 695, 709, 724, 740, 755, 769, 786, 804, 815, 825, 837; false-flag reasons at lines 749–752 and 843–845.

## Observations (non-failing)
- REQ-UX-054 and 060 statements include behaviour "by any means" / "any attempt is refused" (direct submit, forced self-follow) that the criteria only partly exercise through the UI. The UI-visible parts are checkable, so this is not a gap.
- The reasons for 057 and 064 run to several lines, longer than "one line"; the content is a reason, so it is recorded as present.

## Gaps
None.

---

# UX_TRACES_TO_PROD

**Verdict: PASS**

## Checks performed
- Listed every `### REQ-UX-` heading in the core-loop screens deliverable (register REQ-UX-051..064): 14 requirements.
- Confirmed each has a `references` line (14 of 14 found) naming at least one REQ-PROD id.
- Looked up each cited id as a `#### REQ-PROD-NNN` heading in the product requirements. All 8 distinct ids cited exist (REQ-PROD-001..007 and 042).

## Trace table

| REQ-UX | Deliverable line (references) | REQ-PROD cited | Exists in product requirements |
|---|---|---|---|
| REQ-UX-051 | 665 | REQ-PROD-002 | yes (Read the home timeline) |
| REQ-UX-052 | 677 | REQ-PROD-002 | yes |
| REQ-UX-053 | 693 | REQ-PROD-002 | yes |
| REQ-UX-054 | 707 | REQ-PROD-001 | yes (Post a chirp) |
| REQ-UX-055 | 722 | REQ-PROD-001 | yes |
| REQ-UX-056 | 738 | REQ-PROD-001, REQ-PROD-003 | yes, yes (Reply to a chirp) |
| REQ-UX-057 | 753 | REQ-PROD-004 | yes (Read a reply in the conversation it belongs to) |
| REQ-UX-058 | 767 | REQ-PROD-003 | yes |
| REQ-UX-059 | 784 | REQ-PROD-005 | yes (Like and unlike) |
| REQ-UX-060 | 802 | REQ-PROD-006 | yes (Follow and unfollow) |
| REQ-UX-061 | 813 | REQ-PROD-007 | yes (View a user's public profile) |
| REQ-UX-062 | 823 | REQ-PROD-007 | yes |
| REQ-UX-063 | 835 | REQ-PROD-007, REQ-PROD-006 | yes, yes |
| REQ-UX-064 | 846 | REQ-PROD-042 | yes (A way to find people and content to follow) |

## Gaps
None. No cited REQ-PROD id is missing, and no REQ-UX lacks a trace.

Nothing was edited.

---

# COMPOSES_AGAINST_VOCAB

**Verdict: PASS**

Every screen in the core-loop deliverable matches a name in the frozen screen inventory, and every component it uses matches a name in the frozen component library. The deliverable defines no new screen and no new component. Nothing was edited.

## Checks performed

1. **Screen names against the inventory.** I listed each screen the deliverable designs or refers to and matched it to the first column of the screen inventory (IA section, "Screen inventory"), including route, archetype and auth state where the deliverable restates them.
2. **Component names against the library.** I listed each bolded or code-formatted component in the deliverable and matched it to a `####` component heading in the component library (visual-system section, "Component library").
3. **Redefinition.** I checked whether the deliverable restates a component's built-from, behaviour or states in a way that differs from the library, or adds a component or screen. The deliverable composes the components' own named states (default, empty, error, loading, disabled) and defers counter, limit and keep-the-draft behaviour to the library and ComposeBox.
4. **Tokens.** As a secondary check, every `color.*`, `type.*`, `space.*` and `avatar.*` token named in the deliverable exists in the token tables. This is outside the strict brief but supports "nothing redefined".

## Screens (deliverable name → inventory entry)

| Screen named in the deliverable | Inventory match | Route and auth as restated |
|---|---|---|
| Home timeline | Home timeline | `/` with a session, signed-in, feed/list. Matches. |
| Compose (`/compose` and the overlay dialog) | Compose | Matches the inventory route and archetype (modal/dialog). |
| Chirp / conversation | Chirp / conversation | `/@:handle/chirp/:id`, feed/list, both. Matches. |
| Public profile | Public profile | `/@:handle`, profile, both. Matches. |
| Own profile | Own profile | `/@:handle` for the owner, profile, signed-in. Matches. |
| Followers | Followers | `/@:handle/followers`, feed/list. Matches. |
| Following | Following | `/@:handle/following`, feed/list. Matches. |
| Explore / find people | Explore / find people | `/explore`, feed/list, signed-in. Matches. |

Screens the deliverable refers to but does not design, all present in the inventory: Sign in, Sign up, Not found, Onboarding (`/welcome`), Edit profile (`/settings/profile`), Notifications. The delete-chirp confirmation Dialog corresponds to the inventory's Delete chirp dialog.

## Components (deliverable name → library entry)

| Component named | Library match |
|---|---|
| NavShell (signed-in and signed-out variants) | NavShell, which defines both shells |
| ListView | ListView |
| ChirpCard | ChirpCard |
| ComposeBox | ComposeBox, which lists the inline, Compose-dialog and reply-position placements |
| ProfileHeader | ProfileHeader |
| Avatar | Avatar |
| IconButton | IconButton |
| PrimaryButton | PrimaryButton |
| SecondaryButton | SecondaryButton |
| TextField | TextField |
| Dialog (modal variant, confirmation variant) | Dialog |
| Toast | Toast |
| InlineFeedback | InlineFeedback |
| InlineError | InlineError |
| EmptyState (including its error variant) | EmptyState, and ProfileHeader's error state is defined there as an EmptyState error variant |
| LoadingState | LoadingState |

Named states used (default, empty, error, loading, disabled, ChirpCard tombstone, ListView catch-up and load-older, ComposeBox "composing not permitted") are each stated in the library entry for that component.

## Citations

- Deliverable: preamble (the intro paragraphs), Home timeline, "Compose and post a chirp", "The Chirp / conversation screen", "Social actions", "Profiles, followers/following, and discovery". The requirements register lists REQ-UX-051..064.
- Screen inventory: signed-out and public table, signed-in table, dialogs table.
- Component library: component headings Avatar, ChirpCard, ProfileHeader, ComposeBox, TextField, Toggle, PrimaryButton, SecondaryButton, IconButton, NavShell, ListView, SettingRow, Dialog, Toast, InlineFeedback, InlineError, EmptyState, LoadingState. The library's ListView entry carries the catch-up control, load-older and scroll-keeping behaviour that the deliverable composes.

## Gaps

No screen or component is missing from the frozen vocabularies. Two observations, neither a failure:

1. **"Person row"** (Explore, Followers, Following) is used as a name but is not a library component. The deliverable describes it as an arrangement of Avatar, text, and the follow control inside a ListView, with no states or behaviour of its own, so it is a composition and not a new component. If the component-library owner wants it named for reuse, it would need to be added there.
2. **"Text control"** for the load-older affordance ("a SecondaryButton or text control") is not a library component. The ListView entry in the library uses the same phrase, so the deliverable matches the library.

## Result

Unmatched screens: none. Unmatched components: none.

---

# STATES_CONSISTENT

**Verdict: FAIL**

Most per-screen states match the product-wide patterns and the components' named states. Three gaps remain: one direct conflict with a library requirement and two places where a product-wide pattern is not carried into the core-loop screens. Nothing was edited.

## Reference sources
- Global empty/error/loading patterns: the considered-states output was present and was used (four patterns: empty, loading, error by level, expired session and transient error; REQ-UX-086..089).
- Components' named states: the component library (ListView, ChirpCard, ProfileHeader, ComposeBox, Avatar, IconButton, PrimaryButton, SecondaryButton, Dialog, Toast, InlineFeedback, InlineError, EmptyState, LoadingState, NavShell), plus REQ-UX-031, 036 and 039 from the visual system.
- Screen inventory: used to confirm "Not found" exists as a screen.

## Checks performed
For each of the seven surfaces (Home timeline, Compose, Chirp / conversation, Social actions, Public/Own profile, Followers/Following, Explore), I read its empty, error and loading text in the core-loop deliverable and checked three things: (1) it names the component state the library defines, (2) it matches the global pattern for that condition and error level, (3) it does not contradict a library requirement. I also checked whether the expired-session pattern is carried where a session-bound request can fail.

## Per-surface results

| Surface (deliverable lines) | Empty | Error | Loading | Result |
|---|---|---|---|---|
| Home timeline (90-129) | ListView *empty* + EmptyState pointing to Explore and compose; matches global empty pattern | First page: ListView *error* (InlineError + retry); load-older at boundary keeping items; expiry routed to sign-in, not shown as a retry error; matches | LoadingState skeleton at ChirpCard size, bounded spinner for load-older, NavShell never blanks, static under reduced motion; matches | Consistent. Note 1 |
| Compose (224-260) | ComposeBox *empty* + PrimaryButton *disabled*, nothing marked red | Over-limit (ComposeBox *error*) and failed publish (InlineError, draft kept); Dialog error inside panel; expiry keeps the draft; matches | PrimaryButton busy state, field locks briefly; matches | Consistent |
| Chirp / conversation (367-396) | ListView *empty* as EmptyState with the reply slot as next step | Removed chirp: ChirpCard tombstone; reply to a gone parent: InlineError at ComposeBox; replies fail: ListView *error*; unresolved id: Not found screen | LoadingState skeletons for focused chirp, parent and replies; reply slot renders at once | Consistent with one gap. Gap 2 |
| Social actions: like, follow (413-498) | Not stated (the library marks *empty* as not applying to these controls) | InlineFeedback in the danger role, optimistic change reverted, retry; matches the global control-level pattern | IconButton / PrimaryButton / SecondaryButton busy state, not re-triggerable; matches | Conflicts on success feedback and expiry. Gaps 1 and 3 |
| Public and own profile (541-556, 573-581) | ProfileHeader *empty* (labelled zeros) and EmptyState for chirps; owner-voiced variant; matches | Header load failure: EmptyState error variant with retry; blocked/suspended/missing account stated in place; chirp page failure: ListView *error*; matches | ProfileHeader skeleton over ListView skeleton; matches | Consistent. Note 2 |
| Followers / Following (604-613) | Worded per list; own empty following list points to Explore; matches | ListView *error*, load-older failure keeps rows; matches | ListView skeleton at person-row size, bounded spinner; matches | Consistent. Gap 3 (expiry) applies to signed-in rows |
| Explore (636-645) | No-query prompt and no-results block read differently; matches global "suggest broadening the query" | ListView *error* with the query preserved; matches | ListView skeleton while search resolves; matches | Consistent. Gap 3 |

## Gaps

1. **Success feedback for like and follow conflicts with a library requirement.** The social-actions part says that on success "no extra toast is raised" and the control's state change is the confirmation (deliverable lines 426-428). REQ-UX-039 in the visual system requires that a completed action "is confirmed with a brief, non-blocking toast or inline feedback" and its acceptance criterion says to "follow an account" and see "brief, non-blocking confirmation". The Toast component's purpose also lists "a follow" as a confirmed action. The social-actions text may be right that a changed control is enough, but as written the two sources disagree and a tester following REQ-UX-039 would mark follow as failing. Resolution is for the designers: either narrow REQ-UX-039 / the Toast purpose to exclude actions whose result shows on the control, or add a brief InlineFeedback success confirmation to follow.
2. **A failed load of the focused chirp is not specified.** The conversation error state names three cases (removed chirp, reply to a gone parent, replies fail to load). A network or server failure while fetching the focused chirp itself, with the chirp still existing, is none of them. The global surface-level pattern (EmptyState error variant with retry) would apply, but the screen does not say so, and the tombstone ("This chirp isn't available") would mislabel a retryable failure as a removal.
3. **The expired-session pattern is not carried to session-bound actions outside the timeline, compose, conversation and own profile.** The global pattern (REQ-UX-089) requires an expiry to route to sign-in with a stated reason and return the person, and says an expiry must never be dressed as a retryable error. Like, unlike, follow and unfollow (lines 429-432, 493-496), the Explore search (642-643) and the follower/following rows describe only a retryable danger-role failure. A request that fails because the session lapsed would show "retry" and keep failing. The deliverable should say these controls and Explore follow the expiry pattern.

## Notes (not failures)
1. The timeline's failed catch-up is shown "on the catch-up control with a retry" (line 114) without naming the component. The global control-level pattern is InlineFeedback in the danger role; naming it would remove ambiguity.
2. A missing chirp id goes to the generic Not found screen (line 378-379), while a missing account is stated in place and explicitly "not the generic Not-found screen" (line 550-551). Both match their own component rules (ChirpCard tombstone, ProfileHeader error), and the global patterns do not rule between them, so this is a difference to confirm, not a conflict.
3. The social-actions part does not state that the *empty* state does not apply to the like and follow controls. The library already says it does not apply, so nothing is missing from behavior, only from the sentence.

## Frozen-vocabulary names not found
None. Every component and state named in the surveyed state text (ListView, ChirpCard, ComposeBox, ProfileHeader, Avatar, IconButton, PrimaryButton, SecondaryButton, Dialog, Toast, InlineFeedback, InlineError, EmptyState, LoadingState, NavShell) exists in the component library, and "Not found" exists in the screen inventory.
