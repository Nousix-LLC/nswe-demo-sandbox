### Sessions & devices

**Screen**: Sessions & devices — **Route**: `/settings/sessions` — **Archetype**: settings — **Auth**:
signed-in. **Journey**: J6 (managing the account). **Serves**: REQ-PROD-017 (the account settings
surface must let a person view and end active sessions), REQ-PROD-014 (sign-out that ends the session
server-side).

This is where a signed-in person sees every place their account is currently signed in, ends a session
on a device that is not the one in front of them, and signs out. It is a sub-section of **Settings**:
reached from the Settings hub, opened directly at its own URL, and offering a labelled way back to the
hub (the settings-as-secondary-nav convention, REQ-UX-017). It is built as a list of **SettingRow**s
inside the signed-in **NavShell** — the settings archetype — against the 600px reading measure
(`space.measure`).

#### What the person can see and do

- **See their active sessions.** Each session the account currently holds is listed, with enough to
  recognise it: the device and browser (for example "Chrome on macOS"), an approximate location, and
  when it was last active. The session the person is using right now is marked as the current one.
- **End a session on another device.** Any session other than the current one can be ended. This is a
  destructive action, so it is confirmed through the **Dialog** confirmation variant that names the
  effect before it proceeds (the destructive-confirmation convention, REQ-UX-011). Once ended, that
  session can no longer be used on its device.
- **Sign out.** The person can sign out of the current session. Sign-out ends the session server-side
  and leads into the product's sign-out transition — back to the signed-out Landing, with no protected
  screen reachable afterwards (the sign-out transition, REQ-UX-016).

It designs what the person sees and does. How a session or token is represented, validated, or
invalidated is the identity design's concern (`REQ-ID-*`), not this screen's.

#### Layout and content

Top to bottom, inside the signed-in NavShell with the screen's main heading "Sessions & devices"
(`type.title`) and a labelled back control to the Settings hub:

1. **Intro line** — one `type.body` line in `color.text.secondary` explaining the screen in plain words:
   "These are the places you're signed in to chirp. End any you don't recognise, or sign out below."
2. **This device** — a single **SettingRow** for the current session, marked "This device · current
   session" with a label and a marker (a mark and words, never colour alone). Its content: the device
   and browser, the approximate location, and "signed in <relative time>" / "active now". This row has
   **no End session control** — the way to end the current session is Sign out, below — so the row's
   control slot carries only the current-session marker, keeping the one destructive per-row action
   ("End session") reserved for other devices.
3. **Other sessions** — a **ListView** of **SettingRow**s, one per other active session. Each row's
   label is the device and browser; its description (`type.meta`, `color.text.secondary`) carries the
   approximate location, the relative "last active" time, and a short session identifier set in
   `type.family.mono` so a person can tell two similar sessions apart by reading it exactly. Each row's
   control slot holds an **End session** **SecondaryButton** (or an **IconButton** carrying the "End
   session" label where the row is tight). The ListView owns the list-level empty, loading, and error
   treatments (below) and loads in bounded pages if the list is long (the pagination convention,
   REQ-UX-010).
4. **Sign out** — the screen's primary action (below), presented as a prominent entry beneath the list.

#### Primary action

The screen's primary action is **Sign out**. It is the decisive action a person comes here to take on
their own session, and it is the action the release bar gates (REQ-PROD-014). Ending another device's
session is the row-level destructive action within the Other sessions list; it is confirmed the same
way but is not the screen's single primary action.

#### Ending a session on another device (the confirmed, destructive flow)

1. The person activates **End session** on another session's row.
2. A **Dialog** confirmation variant opens over the `color.bg.scrim`. Title: "End this session?" Body
   names the effect plainly: "The session on <device>, <approximate location>, will be signed out.
   Whoever is using chirp there will have to sign in again." The action pair is a destructive confirm —
   a `color.danger` **PrimaryButton** labelled "End session" — and a **SecondaryButton** "Cancel", the
   calm way out. Cancel closes the dialog and changes nothing.
3. On confirm, the dialog shows its loading state (the confirm button is busy and the dialog stays open
   until the action resolves). The end is server-side, so the ended session can no longer be used on its
   device.
4. On success, the dialog closes, the row leaves the list, and the result is shown — **InlineFeedback**
   in the success role at the list, or a **Toast** confirming "Session ended" (the result-of-every-action
   convention, REQ-UX-012). On failure, an **InlineError** appears inside the dialog in plain words and
   the dialog stays open so the person can retry; nothing is ended until it succeeds.

#### Signing out (into the sign-out transition)

1. The person activates **Sign out**.
2. A **Dialog** confirmation variant opens. Title: "Sign out?" Body: "You'll be signed out on this
   device and returned to the chirp landing." When the account is signed in elsewhere, the dialog also
   offers "Also sign out of my other N sessions" (a **Toggle** within the dialog) — this is the
   inventory's Sign out dialog "confirm when ending sessions on other devices too", composed here, not a
   new pattern. The confirm is a **PrimaryButton** "Sign out" (destructive styling when "also end
   others" is on); Cancel is a **SecondaryButton**.
3. On confirm, the current session ends server-side and the screen leads into the product's existing
   sign-out transition: the person lands on the signed-out Landing, and the browser back control does
   not re-expose this settings screen (REQ-UX-016). This screen designs the sign-out entry *into* that
   transition; it does not redesign the transition.
4. The server-side end means the session that was in use is rejected afterward, and the next person at
   that device is not signed in as this account (REQ-PROD-014). A failed sign-out shows an
   **InlineError** in the dialog with a retry; the person is not left in a half-signed-out state.

#### Empty, error, and loading states

| State | Treatment |
|---|---|
| **Loading** | First load of the sessions list shows the **ListView** / **LoadingState** skeleton rows at the rows' real dimensions, not a spinner on a blank screen, so the layout does not jump when the sessions arrive; the skeleton honours `motion.reduced`. The **NavShell** and the screen heading render immediately (the shell has no loading state), and the **This device** row renders as soon as the current session is known, while the other sessions resolve. |
| **Empty** (the "only this session" case) | When the account is signed in only on the current device, the Other sessions list has no items, so the **ListView** shows its **EmptyState**: a calm, explanatory block — "You're only signed in here. When you sign in on another device, it'll show up in this list." — never a blank area and never an apology. The **This device** row and **Sign out** remain present and usable. |
| **Error** | If the sessions list fails to load, the **ListView** shows its error treatment — an **EmptyState** error variant (or **InlineError**) with a retry: "We couldn't load your sessions — try again." The **This device** row still renders if the current session is known, so the person can still sign out. A failed End session or Sign out is shown as an **InlineError** inside the open **Dialog** (its error state), with the action retryable and nothing changed until it succeeds. An action attempted on an expired or invalid session follows the product-wide session-expiry convention (REQ-UX-008): the person is routed to **Sign in** with the reason stated and returned afterwards — that pattern is composed here, owned by the product-wide considered-states work, not redefined on this screen. |

Each state above is one of the composed components' own named states; this screen invents no per-screen
state treatment of its own, and stays consistent with the product-wide empty / loading / error patterns.

#### Out of scope for this screen

The session, token, and verification **mechanism** (identity design, `REQ-ID-*`); the sign-out
**transition** itself (composed here, owned by the IA/interaction model and the screens-and-flows
sign-out design); and the other settings sub-sections the Settings hub links to. Those are referenced
by name and designed elsewhere.

---

#### Requirements

##### REQ-UX-073 — See active sessions and end another device's session
- **statement**: A signed-in person can open Sessions & devices and see each place the account is
  currently signed in — each with enough to recognise it (device and browser, approximate location,
  last-active time) and the current session clearly marked — and can end any other session through a
  confirmation that names the effect, after which that session can no longer be used on its device.
- **acceptance_criteria**: Signed in on two devices, open `/settings/sessions`; both sessions are
  listed, the one you are using is marked as the current device, and each other session shows its
  device, an approximate location, and a last-active time. Choose End session on the other device; a
  confirmation states what will happen and offers a cancel. Confirm it: the session leaves the list, the
  result is shown, and on the other device the next action on that session is rejected and requires a
  fresh sign-in.
- **release_gating**: true
- **references**: REQ-PROD-017, REQ-PROD-014

##### REQ-UX-074 — Sign out ends the session server-side and does not leak back
- **statement**: A signed-in person can sign out from Sessions & devices; sign-out ends the current
  session server-side so it can no longer be used, returns the person to the signed-out landing, and
  leaves no protected screen reachable with the browser back control. Where the account is signed in
  elsewhere, the sign-out confirmation offers to end those other sessions too.
- **acceptance_criteria**: Signed in, open `/settings/sessions` and choose Sign out; a confirmation
  states you will be signed out and, when other sessions exist, offers to end them too. Confirm it: you
  land on the signed-out landing; pressing browser back does not re-expose the settings screen; and
  replaying the request from the session that was in use is rejected, so the next person at that device
  is not signed in as you.
- **release_gating**: true
- **references**: REQ-PROD-014
