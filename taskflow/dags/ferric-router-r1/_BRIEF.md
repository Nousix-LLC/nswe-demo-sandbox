# _BRIEF.md — ferric-router-r1

**Goal slug**: `ferric-router-r1`
**Kind**: code DAG
**Launch agent**: swe-coder
**Repo**: Nousix-LLC/nswe-demo
**Branch**: `work/ferric-router-r1`
**Epic**: #131 — EPIC: Ferric 1.0 — Client-side Router (usable_early, extends #5)

---

## Objective

Implement **Ferric 1.0 — Client-side Router** (epic #131) on branch `work/ferric-router-r1`.
This is the third Ferric 1.0 implementation epic, landing on top of the Authoring Model
(PR #188, merge commit `aa2468771eccd9e2ee79c12c79b8943fca18e07a`), and running in parallel with
the Async/Forms/Events epic (#130) on a non-overlapping crate (`crates/ferric-router`).

The goal extends the existing `ferric-router` walking skeleton (from board issue #5, now closed)
**additively** — that crate's frozen prelude surface (`Params`, `RoutePattern`, `Router`,
`navigate`, `current_path`, `link`, `Link`, `LINK_CLASS`) is carried forward unchanged. The 1.0
additions are:

1. **Nested routes with a nested outlet** (#146) — parent routes render a layout with a child
   outlet; a matched child view renders into it. Shared shells (navigation bars, section frames)
   are written once and only the child view swaps on navigation.

2. **Replace-navigation** (#146) — a `replaceState` counterpart to the frozen push-only `navigate`,
   additive over its signature.

3. **Active-route awareness** (#147) — a link that reflects whether its target is the currently
   active route, with an active class and `aria-current="page"`, additive over the frozen `Link`
   builder.

4. **Per-level fallback for nested routes** (#146) — a nested level may declare its own no-match
   view distinct from the app-root fallback.

All of #146's capabilities are stage **usable_early** and release-gating. #147 is stage **one_oh**
and release-gating. Both must be additive over the frozen surface from #5 (REQ-RT-008 / REQ-FW-009).

---

## Issues covered

### #131 — EPIC: Ferric 1.0 — Client-side Router (usable_early, extends #5)

The parent epic. Closed when both sub-issues (#146, #147) are met.

### #146 — Ferric 1.0: Core routing — path parameters, nested routes, navigation, and accessible links

**Acceptance criteria** (from issue body):
- The router matches path patterns with named parameters and renders the matching route's component
  in a reactive `<Outlet>`.
- Nested routes nest their `<Outlet>` inside a parent route's view.
- Each route level can declare a fallback for no-match.
- `navigate(path)` and the History-API push/replace functions change the current path reactively.
- The `<Link>` component is keyboard-focusable and announced by assistive technology as a link.
- All `ferric-router` prelude surfaces present at the #5 baseline are present at 1.0 without
  removal or redefinition.
- Stated router examples compile.

**Design traces**: `design/ferric/router-and-http.md` §client-router (REQ-RT-001, REQ-RT-002,
REQ-RT-003, REQ-RT-004, REQ-RT-005, REQ-RT-006, REQ-RT-008); `design/ferric/scope-and-requirements.md`
(REQ-FW-007, REQ-FW-009); BAR-FERRIC-015.
**Verification**: automated_test.
**Depends on**: #139 (view! macro surface and compile-time diagnostics — delivered by PR #188).

### #147 — Ferric 1.0: Active-route awareness

**Acceptance criteria** (from issue body):
- The `<Link>` component applies `aria-current="page"` when its href matches the current path.
- A test or example demonstrates that navigating to and away from a route toggles the attribute
  correctly.

**Design traces**: `design/ferric/router-and-http.md` §active-link (REQ-RT-007); BAR-FERRIC-016.
**Verification**: automated_test.
**Depends on**: #146 (Core routing — in this epic).

---

## Inputs

### Landed authoring model (the base to build on)

PR #188 merged at `aa2468771eccd9e2ee79c12c79b8943fca18e07a` (branch `main` on
`Nousix-LLC/nswe-demo`) delivers all Ferric 1.0 Authoring Model (epic #129) capabilities —
reactive signals (`create_signal`, `Signal`, `Memo`, `create_effect`, `batch`, `create_memo`),
virtual DOM (`VNode`, `VElement`, `VText`), the `view!` macro, component model (props, children,
named slots, dynamic dispatch), context, and the WASM runtime (`mount`, the event loop). This is
the base; `work/ferric-router-r1` branches from it.

### Frozen ferric-router surface (must remain untouched)

The `crates/ferric-router` prelude shipped by board issue #5 (now closed) is frozen. The following
items must be present at 1.0 with unchanged signatures; no removal or redefinition is permitted
(REQ-RT-008 / REQ-FW-009):

- `matcher::Params` (`get`, `is_empty`, `len`, additive `iter`)
- `matcher::RoutePattern` (`new`, `match_path`)
- `router::Router` (`new`, `route`, `fallback`, `mount_history`, `outlet`)
- `router::navigate(&str)` — push semantics, unchanged
- `router::current_path() -> String` — reactive, unchanged
- `link::link(to, label) -> VNode`, the additive `Link` builder, `LINK_CLASS`

An app written against this baseline prelude must still compile and run at 1.0.

### Design documents

- `design/ferric/router-and-http.md` (commit `ade5bdde424638b9f993c5699219c638d02e0e59`, PR #128
  merged) — the primary design for this epic: Part 1 §client-router (REQ-RT-001 through
  REQ-RT-008). All 8 requirements in this section are the acceptance bar for this goal.
- `design/ferric/scope-and-requirements.md` (same commit) — the full 1.0 requirement index;
  BAR-FERRIC-015 and BAR-FERRIC-016 are the bar entries for this epic.

### Repo

`Nousix-LLC/nswe-demo` — `crates/ferric-router` is the library crate this goal extends.

---

## Declared output

- Commits on branch `work/ferric-router-r1` (never force-pushed).
- One PR into `main` with:
  - `Closes #131`, `Closes #146`, `Closes #147` in the description.
  - Description written for the repository's readers: what changed, how it was verified, what it
    closes. No host paths or taskflow internals.
- Root `SYNTHESIS.md` at the DAG's workspace (`taskflow/dags/ferric-router-r1/SYNTHESIS.md`),
  accounting for each issue: met or not, and why.
- CI all six jobs PASS on the PR head: `fmt`, `clippy`, `test`, `wasm`, `doc`, `image`.

---

## Concerns to evaluate

### C1 — Correctness against the design

Each of the 8 requirements in `design/ferric/router-and-http.md` Part 1 is met:

- **REQ-RT-001**: Route table with named path parameters resolves correctly; `Params::get("id")`
  returns the right value; mismatches do not match.
- **REQ-RT-002**: The outlet re-renders reactively on path change without manual subscription wiring.
- **REQ-RT-003**: Push navigation (`navigate`) and the new replace-navigation both update
  `current_path()` reactively; push grows history length, replace does not; `popstate` restores the
  previous path; the guide documents when to choose each.
- **REQ-RT-004**: In-app links navigate client-side, are keyboard-focusable (`tabindex="0"`), carry
  `role="link"`, and are announced as links by assistive technology.
- **REQ-RT-005**: Nested routes render the parent layout with the child view in the nested outlet;
  navigating between sibling child routes does not tear down the parent layout.
- **REQ-RT-006**: A declared fallback renders for unmatched paths; a nested level can declare its
  own fallback; without a fallback, an empty node renders (baseline preserved).
- **REQ-RT-007**: An active link carries `aria-current="page"` (and an active class) when its
  target matches the current path; the marker is absent otherwise; it toggles correctly on
  navigation.
- **REQ-RT-008**: The additive identity holds — the frozen prelude is unchanged; a baseline app
  still compiles and passes its tests; every 1.0 addition is recorded in the changelog as additive;
  no frozen item is removed or has its signature changed.

### C2 — CI: all six jobs PASS

`fmt`, `clippy`, `test`, `wasm`, `doc`, `image` all pass on the PR head commit (GitHub Actions CI
on `Nousix-LLC/nswe-demo`). No warnings treated as errors by clippy. WASM build succeeds for
`crates/ferric-router` and `crates/chirp-frontend`. Doc builds without broken links or missing
crate references.

### C3 — Test coverage

Automated tests cover:

- Route-matching accuracy: named parameters, extra/missing segments, first-match-wins order.
- Reactive outlet: after `navigate("/a")` then `navigate("/b")`, the outlet renders the `/b` view.
- Push navigation: `navigate` updates `current_path()`; `popstate` restores the prior path; history
  length grows.
- Replace navigation: `replace_navigate` (or equivalent) updates `current_path()` without growing
  history length.
- Nested routing: a two-level config (parent layout + child view) renders parent with child in the
  nested outlet for `/users/7`; `/users` renders the layout with the index/empty child.
- Parent layout preservation: navigating between sibling child routes does not rebuild the parent.
- Per-level fallback: an unmatched child renders the nested level's own fallback while the parent
  layout persists; app-root fallback renders for a fully unmatched path.
- Accessible links: `link(to, label)` emits a non-anchor element with `tabindex="0"` and
  `role="link"`.
- Active-route awareness: when `current_path` matches a link's target the element carries
  `aria-current="page"` (and active class); when it does not, the marker is absent; navigating
  away clears it.
- Baseline backward-compat: the existing `ferric-router` tests (shipped by #5) pass unchanged.

Tests run with `wasm-bindgen-test` where DOM is required; `cargo test` for pure reactive routing
logic.

### C4 — Rust idioms and API surface quality

The new API is idiomatic Rust: clean generics, no unnecessary `Rc<RefCell<>>` sprawl, appropriate
use of `wasm-bindgen` / `web-sys` History API bindings, documentation for all public items. The
router composes `ferric`'s signals and component model (it does not re-implement reactivity or the
DOM diff). The replace-navigation API shape is left to implementation, subject only to being
additive over `navigate`'s signature. The active-link API extends the existing `Link` builder
additively.

### C5 — API surface compatibility with the authoring model on main

Nothing in this PR changes or removes any API item present on `main` at `aa24687`. Code written
against the authoring model (`create_signal`, `Signal`, `view!`, `component`, `context`, `mount`)
and against the frozen `ferric-router` prelude (#5) continues to compile and behave identically.
The additive guarantee in REQ-RT-008 is verified by the baseline router tests passing unchanged.

---

## Constraints

- Repo: `Nousix-LLC/nswe-demo`.
- Branch: `work/ferric-router-r1`. Never force-push.
- Do not modify anything under `design/` (design documents are read-only inputs).
- Do not merge the PR. The overseer's review gate does that.
- Do not prescribe decomposition; choose your own.
