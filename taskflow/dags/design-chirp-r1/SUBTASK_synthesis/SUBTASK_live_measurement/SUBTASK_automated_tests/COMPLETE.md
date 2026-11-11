# COMPLETE — SUBTASK_automated_tests

## What was done

Measured every `BAR-*` whose declared `verification_method` is `automated_test` (36 of the 278 release-bar criteria)
against the `Nousix-LLC/nswe-demo` repository test suite at commit `c805525`. Built and ran the workspace's own test
suite (`cargo test`) at `c805525` — all native tests executed and passed (chirp-server 24 unit + 20 integration,
chirp-types 18, chirp-frontend 41 native, plus the ferric framework crates and doc-tests) — and read the sources to
ground each verdict. Each of the 36 criteria was judged `met | partial | missing | not_applicable` with an observation
naming the test(s) and what running or reading them showed.

## Output

- `outputs/automated-test-measurement.md` — verdict table conforming to `verdict_row_schema` in
  `../contracts/_MANIFEST.yaml` (columns `bar_id, live_status, observation`), one row per `automated_test` `BAR-*`,
  keyed by `bar_id`, preceded by a short access/method preamble.

## Verdict distribution

- met: 7 (BAR-001, 002, 003, 004, 005, 006, 008 — the implemented server core loop)
- partial: 10 (BAR-011, 012, 164, 205, 241, 305, 312, 313, 314, 444)
- missing: 19 (BAR-007, 009, 010, 016, 017, 020, 103, 232, 233, 234, 235, 237, 266, 273, 285, 301, 309, 315, 443)
- not_applicable: 0

## Grounding and conservatism

- The suite builds and runs at `c805525`; the server tests exercise the assembled server against a fresh in-memory
  repository (no DB, no network), so a verdict resting on durable persistence does not imply restart survival.
- The frontend `wasm-bindgen-test` browser tests are compile-only and were not executed in a browser. Criteria resting
  on rendered layout, viewport, contrast, or browser navigation (e.g. BAR-266, 273, 285 and parts of 205/241) have no
  executable automated test in the repository and were judged conservatively (`missing`/`partial`), never optimistically.
- `missing` clusters where the release bar expects a surface absent at `c805525`: real credentials and the
  sign-in/recovery/sign-out/account-management flows depending on them, profile editing, and account deletion.

## Success criteria

- [x] Every `automated_test` `BAR-*` (36) has exactly one `live_status` and a grounded observation; none omitted, none
      of another method included (verified: 36 rows == the 36 release-bar rows tagged `automated_test`; `BAR-231`, a
      `manual_user_check`, was correctly excluded).
- [x] Each observation names the repository test artifact at `c805525` it rests on and what running/reading it showed;
      where the browser/visual criteria have no executable test, that is stated and the verdict is conservative.
- [x] `live_status` values from the inherited vocab; `bar_id`s verbatim.
- [x] Output touches only `Nousix-LLC/nswe-demo` by repository/commit identity; no host/system/taskflow detail
      (hygiene scan clean).

## Environment note

The Phase-B `design` methodology loader was unavailable run-wide (`agent_domain_unset`), as recorded in the subtree
hub; this measurement applied the principal-product-designer persona and the relayed ReleaseBar guidance, which the
brief, hub, and contracts fully specified. Recorded for transparency.
