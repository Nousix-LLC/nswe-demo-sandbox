# COMPLETE — SUBTASK_accessibility

**Task**: Measure the accessibility cluster (`manual_user_check`) against the live chirp product at `c805525`.
**Evaluation**: Atomic (one accessibility measurement pass, one verdict table, one responsibility).

## What was done

Exercised the live `Nousix-LLC/nswe-demo` **chirp** product read-only and measured all 18 owned
accessibility `BAR-*` criteria. The UI is a client-side WASM SPA (`crates/chirp-frontend`) whose
rendered DOM — the surface a keyboard and screen reader meet — is produced entirely by Rust source, so
each criterion was grounded in that source at `c805525` together with the live served shell (`lang`,
viewport, the 20-line inline stylesheet) and the live API (`/api/timeline` returns a typed 401; health
endpoints return 200). The deployed revision is a docs/design/deploy-hygiene descendant of `c805525`
with no product-code change, so the running product realizes `c805525`.

## Output produced

- `outputs/accessibility-measurement.md` — access-note header + verdict table conforming to the inherited
  `verdict_row_schema` (`bar_id, live_status, observation`), one row per owned `BAR-*`, keyed by `bar_id`.

## Verdicts (18/18)

- **met** (4): BAR-218 (focus indicator — no CSS suppresses the UA ring), BAR-286 (zoom/reflow — single
  flowing column, zoom unblocked), BAR-288 (no flashing content), BAR-289 (reduce-motion — no motion to reduce).
- **partial** (12): BAR-031, BAR-277, BAR-278, BAR-280, BAR-281, BAR-282, BAR-283, BAR-284, BAR-287,
  BAR-290, BAR-291, BAR-292.
- **missing** (2): BAR-276 (keyboard-only cannot complete the action set; nav links are pointer-only
  `<span role=link>` with Click-only handlers), BAR-279 (no skip-to-content control and no `<main>` landmark).

## Cross-cutting findings feeding the partials

- Router nav links are `<span role="link" tabindex="0">` with a Click-only handler (no keydown) —
  keyboard-inoperable navigation (`ferric-router/src/link.rs`, `chirp-frontend/src/app.rs`).
- No `<main>` landmark, no skip link, no `aria-current` on the current nav destination, no `aria-pressed`
  on like/follow toggles, no `aria-invalid`/`aria-describedby` on form fields, no `aria-busy`.
- No route-change or dialog focus management (no `.focus()` anywhere); no modal dialogs exist.
- Static `<title>chirp</title>` never matches the per-screen `<h1>`.
- Strengths: `role="alert"` error banners and a `role="status"` success banner; `<label for>`-associated
  fields; native `<button>`s; a `<ul>`/`<li>` feed; one `<h1>` per screen; zoomable single-column layout.

## Success criteria

- [x] Every owned `BAR-*` has exactly one `live_status` and a grounded observation; none omitted; no out-of-cluster `BAR-*`.
- [x] Each observation grounded in the live product or an actual `c805525` source artifact; conservatively judged where only a rendered pass could fully confirm, with the basis stated.
- [x] `live_status` values from the inherited vocab; `bar_id`s verbatim.
- [x] Read-only on the live product; output references repository identity + commit + repo-relative paths only; no host/system/taskflow detail.

## Dependents

`SUBTASK_journeys_fold` unions this cluster's table with the other eight into `outputs/live-journeys-measurement.md`.
