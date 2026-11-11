## Code review — ferric-router (issue #5) — **APPROVE**

Principal-level human-review-equivalent pass on top of the green machine gate. Reviewed the full
~1205-line additive diff (8 files) against issue #5's acceptance criteria and the `code-review` /
`rust` / `core` methodologies. **No block- or major-severity findings. Acceptance criteria
substantively met. Approving.**

### What I verified (independently of the machine gate)
- **Composition, not re-implementation.** `ferric-router` composes `ferric`'s `create_signal`/`Signal`,
  `VElement`/`text`/`EventKind`, `Component`, and `mount`; it re-implements none of the reactivity/DOM
  layer. Confirmed against `crates/ferric` source. The duplication/ownership check holds.
- **The `preventDefault` constraint (F2) is real, not an excuse.** `ferric::vdom` defines
  `pub type EventHandler = Rc<dyn Fn()>` and `VElement::on(.., impl Fn() + 'static)` — the click
  handler genuinely receives no `web_sys::Event`, so `preventDefault()` is unreachable through the
  public API. The `<span role="link" tabindex="0">` + click→`navigate` workaround in `link.rs` is the
  correct composition given the frozen surface, is `data-to`/`role`/`tabindex`-annotated for a11y, and
  is documented in code + README. A true `<a href>` variant can be added additively later.
- **Matcher correctness** (`src/matcher.rs`): exact-over-segments matching with empty-segment
  normalization gives root `/`, trailing-slash, and doubled-slash handling for free; param extraction
  is correct; 18 unit tests cover extra/missing segments, root, multi-param, mixed static/param,
  no-percent-decode, and segment-count exactness. No `unwrap`/panic in non-test code.
- **Navigation soundness** (`src/router.rs`): History `pushState` + `popstate` are correctly behind
  `cfg(target_arch = "wasm32")` so the crate unit-tests natively; fallible JS calls use `let _ =`;
  the `popstate` closure is intentionally `forget`-ed for the app-lifetime router (same trade-off
  `ferric::dom` documents). `path_signal()` keeps no `RefCell` borrow across `create_signal`, avoiding
  the classic already-borrowed panic.
- **Public API surface**: the frozen prelude (`Params`, `RoutePattern`, `Router`, `navigate`,
  `current_path`, `link`) matches `contracts/ferric_router_api.rs`; additive extras (`Params::iter`,
  `Link` builder, `LINK_CLASS`) are additive-only — nothing frozen was removed or changed in place.
  Ergonomic enough to build a Twitter-style SPA on later.

### Findings (all minor / non-blocking)
| # | Severity | Location | Finding |
|---|----------|----------|---------|
| F1 | minor (by-design) | `src/router.rs` thread-local `CURRENT_PATH` | Routing state is a single thread-local `Signal<String>`. Correct and idiomatic for a single-root client-side wasm SPA (the stated scope) and thoroughly documented; a future multi-root/SSR scenario would need a per-runtime handle. Acceptable documented choice, not a defect. |
| F2 | minor (by-design) | `src/link.rs` / README | `<span role="link">` instead of `<a href>` due to `ferric`'s zero-arg `Fn()` click handler (see above). Correct composition, well documented. |
| M1 | nit | `src/router.rs` `path_signal()` | The lazy-create-outside-effects invariant is upheld by `outlet()`/`mount_history()` pre-creating the signal. If `current_path()` were ever the *first* router call from inside a reactive effect, the signal would be created inside that effect and risk disposal on re-run. Normal API usage avoids this and it's documented; a hardening opportunity only. |
| M2 | nit | `src/router.rs` route resolution | First-match-wins is an O(routes) linear scan per navigation — fine at SPA scale and documented; register specific patterns before general ones. |
| M3 | nit | `examples/app.rs` `main()` | `.expect()` on `window`/`document`/mount-root is acceptable for an example binary; no change needed. |

None of F1/F2/M1–M3 block. The design is clean, documented, test-covered, and extensibility-aware.

### Acceptance criteria (issue #5 + work-item brief)
All met: workspace member crate (path-dep on `ferric`) ✓; route table + param matcher ✓; History API
`pushState`/`popstate` + `navigate()` + `link` helper ✓; reactive outlet ✓; wasm build + 3-route
example ✓; native matcher/param tests + compile-only `wasm-bindgen-test` (no headless runner —
documented, not a FAIL) ✓; fmt/clippy clean + rustdoc + README ✓; PR into `main` with `Closes #5` ✓.

**Verdict: APPROVE.** (Note: GitHub may record this as COMMENTED rather than APPROVED because the
authenticated account authored the PR — a platform self-review block. The authoritative verdict is the
APPROVE recorded in this review DAG's `SYNTHESIS.md`.)
