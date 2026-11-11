spoke: foundation-buildability
concern_ids: [4]

findings:

  - id: FB-001
    severity: non-blocking
    concern: 4
    location: "ssr-hydration.md §render_to_string / §hydrate (REQ-SSR-005 area)"
    statement: >
      The design specifies that `hydrate` must adopt the server-rendered DOM without
      destroying and rebuilding it — correctly identifying that `mount()` empties the
      root first, making it unsuitable. However, the design does not state what `hydrate`
      does when the server-rendered DOM and the client's initial VNode tree disagree at a
      path (a hydration mismatch). The Ferric diff/patch model addresses nodes by
      `path: Vec<usize>` (child indices from the tree root, as confirmed in `vdom.rs`
      lines 78–143); a mismatch in tree shape means a path that resolves to a different
      DOM node than expected, producing silent corruption or a runtime panic rather than a
      recoverable failure. Neither `ssr-hydration.md` nor `release-bar.md` states the
      required behavior for mismatches (warn and re-render at the divergence point, panic,
      or silently adopt regardless). Every peer SSR framework (Leptos, Dioxus, React)
      defines explicit mismatch behavior; Ferric 1.0 is silent on it.
    recommendation: >
      Add a paragraph to `ssr-hydration.md` under the `hydrate` specification naming the
      mismatch behavior Ferric 1.0 commits to — for example: "on a path that cannot be
      resolved against the existing DOM, log a warning in debug builds and fall back to a
      full re-render at the divergence subtree." Add the corresponding acceptance criterion
      to `release-bar.md` under the SSR bar so it is mechanically checkable.

  - id: FB-002
    severity: non-blocking
    concern: 4
    location: "router-and-http.md §REQ-RT-007 (active-route awareness)"
    statement: >
      The design adds active-route awareness (`REQ-RT-007`) so that the `Link` component
      sets `aria-current="page"` on the link to the currently active route. The design
      does not specify how the `Link` determines whether it is active at render time.
      The existing `ferric-router/src/router.rs` (confirmed at `276138f`) exposes
      `current_path()`, which reads a thread-local `Signal<String>` and subscribes the
      enclosing reactive effect to path changes. If `Link::build()` calls `current_path()`
      during a component render, every link re-renders on every navigation — potentially
      producing O(n) DOM patches for a nav bar with n links when only one link's active
      state changed. The design does not rule this out, nor does it specify an alternative
      (e.g., comparing the link's `to` path against the current path lazily, or computing
      `aria-current` only inside a scoped `create_memo`). The subscription model for
      active-route detection is implementation-critical but left unspecified.
    recommendation: >
      Add a note to the `REQ-RT-007` section of `router-and-http.md` specifying the
      intended subscription model: either (a) each `Link` renders a closure that reads
      `current_path()` reactively so only that link's subtree re-evaluates, or (b) a
      single `Memo<HashSet<String>>` of active paths is computed once and links subscribe
      to it. State the choice as a design constraint so the implementation can be verified
      against it in the release bar.

summary:
  blocking_count: 0
  non_blocking_count: 2
  notes: >
    All design claims about the existing foundation at baseline commit 276138f were
    verified against the actual source. The frozen prelude surfaces for ferric, ferric-router,
    and ferric-http are correctly described. The SSR architecture's technical assumptions
    (no web-sys in vdom/component, path-based patch addressing, mount emptying the root,
    reactive values stored as Box<dyn Any>, closures not serializable) are all accurate.
    Every 1.0 addition — render_to_string, hydrate, view! macro, #[component], Children,
    nested routes, replace-navigation, active-route awareness, Method::Patch, per-request
    timeout — is additive over the frozen surfaces: no existing export is removed or
    redefined. The VElement builder methods and vdom::text() relied on by the view! macro
    lowering table already exist at baseline (vdom.rs lines 146-205, labeled "Ergonomic
    builders additive to the frozen surface"). No design assumption is demonstrably wrong
    about the existing foundation. The two non-blocking findings are unspecified behaviors
    (hydration mismatch handling; active-route subscription model) that need to be stated
    for the release bar to be mechanically checkable.
