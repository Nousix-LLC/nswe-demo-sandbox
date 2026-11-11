## Social actions — the in-place like and follow controls

Liking a chirp and following a person are the two reactions in the core loop. Neither is a screen:
each is a control that lives on another screen's component — the like control on every **ChirpCard**,
the follow control on a **ProfileHeader** and on the person rows the discovery and list screens
present. This part specifies how those two controls read and behave wherever they appear, built from
the frozen component library and composed against the per-screen states its components already carry.
It does not redefine **ChirpCard**, **ProfileHeader**, **IconButton**, **PrimaryButton**,
**SecondaryButton**, or **InlineFeedback**, and it does not design the cards, headers, or lists the
controls sit on — those are the timeline, conversation, profile, and discovery surfaces.

### The behavior both controls share

Both controls act in place — the person stays on the screen they are on, and nothing navigates.
Both are **idempotent**: the control holds exactly two mutually exclusive states (liked / not-liked;
Following / not-following), so repeating the same intent cannot stack. The value the control shows is
the resolved result, not a client-side tally — a like count is the server's count for that chirp, and
a follow is either on or off, never counted twice.

The response is immediate and optimistic, then reconciled:

- On activation the control flips to the target state at once (the heart fills and the count moves;
  the button becomes "Following") and shows its own in-flight **loading** treatment while the change
  settles.
- On success the optimistic state stands; the state change is itself the confirmation, so no extra
  toast is raised for a result that already shows on the control (per the product's transient-feedback
  convention, a result that belongs against a specific control is shown at that control, not in a
  **Toast**).
- On failure the optimistic change is reverted — the control returns to the state it held before, and
  any count returns to its prior value — and an **InlineFeedback** in the danger role appears at the
  control, in plain words, with the action still available to retry. The control never shows a like or
  a follow that did not take.

Meaning is never carried by colour alone: every active state is a colour together with an icon or a
label, matching the library's rule for its components.

---

### Like / unlike

**Where it sits.** The like control is the like **IconButton** in the action row of every **ChirpCard**
— the same control wherever a ChirpCard is drawn: the Home timeline, the Chirp / conversation screen,
a profile's chirps, and search and notification results. It reads and behaves identically in all of
them.

**Content.** The heart **IconButton** and, beside it, the chirp's like count in tabular numerals so a
changing count does not shift the row. The control exposes a text label to assistive technology in both
states ("Like" / "Liked").

**Primary action.** Toggle this chirp's like for the signed-in person: like it when not liked, unlike
it when liked.

**States.**

- **default / active.** Two states. *Not liked* — the outline heart at rest, the current like count.
  *Liked* — the active treatment the **ChirpCard** defines: `color.like`, a filled heart, and a "Liked"
  label together (never colour alone), with the count raised by this person's like. The two states are
  mutually exclusive, which is what makes a second "like" impossible — activating an already-liked
  control unlikes it rather than liking again, so the count cannot double-count.
- **error.** A like or unlike that fails: the optimistic flip is reverted (the heart returns to its
  prior fill, the count returns to its prior value) and the like **IconButton** shows **InlineFeedback**
  in the danger role at the control with a plain reason and a retry. The count shown always matches the
  result that actually happened.
- **loading.** The request is in flight: the like **IconButton** shows its own busy treatment (a
  bounded spinner in place of the heart) and is not re-triggerable until it resolves, so a rapid double
  activation cannot post two conflicting changes.

---

### Follow / unfollow

**Where it sits.** The follow control is the context action on a **ProfileHeader** and the follow
action on each person row the Explore / find-people, Followers, and Following screens present (those
rows are the discovery-and-lists surface; this part specifies only the control that sits on them). It
is the same control in every place.

**Content.** A single context action: a **PrimaryButton** labelled "Follow" when the person is not
followed, a **SecondaryButton** labelled "Following" when they are (the calmer weight signals the
already-done state and carries the unfollow affordance). On a **ProfileHeader**, the follower and
following counts sit beside it in tabular numerals so the layout holds as a count changes.

**Primary action.** Toggle whether the signed-in person follows this account: follow to bring that
account's new chirps into the home timeline, unfollow to remove them.

**Cannot follow yourself.** Your own identity never presents a Follow control. On your own
**ProfileHeader** the context action is "Edit profile" (a **SecondaryButton**), not "Follow", and a
person row that represents you offers no follow affordance. Because no surface draws a Follow control
for your own account, a self-follow cannot be started from the product. If one is nonetheless submitted
(for example from a stale row), it is refused: the control does not enter the Following state, it
returns to "Follow", and **InlineFeedback** in the danger role states plainly that you cannot follow
your own account.

**States.**

- **default / active.** Two states. *Not following* — the "Follow" **PrimaryButton**. *Following* — the
  "Following" **SecondaryButton**. The two are mutually exclusive, so following an account you already
  follow does not stack a second follow; the control simply stays "Following".
- **error.** A follow or unfollow that fails: the optimistic label flip is reverted (back to its prior
  "Follow" or "Following"), any affected follower count returns to its prior value, and the control
  shows **InlineFeedback** in the danger role with a plain reason and a retry. The self-follow refusal
  above uses this same treatment.
- **loading.** The request is in flight: the button shows its busy treatment (a bounded spinner,
  label and width held so the row does not jump) and is not re-triggerable until it resolves.

---

### Requirements and acceptance criteria — REQ-UX-059..060

#### REQ-UX-059 — Like is an in-place, idempotent toggle with an accurate count
- **statement**: The like control on every **ChirpCard** is an in-place toggle with two states —
  not-liked and liked — where the liked state is shown by colour together with a filled heart and a
  "Liked" label (never colour alone); liking is idempotent and the like count shown reflects the
  resolved result; a failed like or unlike reverts the optimistic change and reports at the control,
  and an in-flight change shows the control's busy state.
- **acceptance_criteria**: On any chirp, activate like: the control shows the liked state (filled
  heart, like colour, and a "Liked" label — not colour alone) and the count rises by one. Activate like
  again on the now-liked chirp, or reload the screen: the count does not rise a second time. Unlike it:
  the control returns to not-liked and the count returns to its earlier value. Force a like to fail
  (for example act while offline): the control returns to its prior state, the count is unchanged, and
  a danger message appears at the control with a way to retry — the count never shows a like that did
  not take. Open the same chirp in the timeline, in its conversation, and on the author's profile: the
  like control looks and behaves the same in each.
- **release_gating**: true
- **references**: REQ-PROD-005

#### REQ-UX-060 — Follow is an in-place, idempotent control that cannot follow yourself
- **statement**: The follow control on a **ProfileHeader** and on the person rows of the discovery and
  list screens is an in-place control with two states — "Follow" (a **PrimaryButton**) and "Following"
  (a **SecondaryButton**); following is idempotent; a person's own identity never presents a Follow
  control (the own-profile action is "Edit profile") so a self-follow cannot be started, and any
  attempt is refused and shown at the control; a failed follow or unfollow reverts and reports at the
  control, and an in-flight change shows the control's busy state.
- **acceptance_criteria**: On another person's profile, activate "Follow": the control becomes
  "Following" and that account's new chirps appear in your home timeline. Activate it again, or reload:
  nothing is duplicated — one follow holds and the control stays "Following". Unfollow: the control
  returns to "Follow" and their chirps leave your timeline. Open your own profile: the context action
  is "Edit profile", never "Follow", and no screen offers a control to follow your own account. Force a
  follow to fail: the control returns to its prior label, any follower count is unchanged, and a danger
  message appears at the control with a way to retry. Find the follow control on a profile header and on
  a person row in Explore or a followers/following list: it looks and behaves the same in each.
- **release_gating**: true
- **references**: REQ-PROD-006
