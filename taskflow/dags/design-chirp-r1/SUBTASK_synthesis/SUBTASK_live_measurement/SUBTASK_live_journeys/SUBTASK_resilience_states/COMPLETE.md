# COMPLETE — SUBTASK_resilience_states

**Task**: Measure the 12 `manual_user_check` `BAR-*` of the resilience & feedback-states cluster
against the deployed chirp product at `Nousix-LLC/nswe-demo` commit `c805525`.

**Evaluation**: Atomic — one coherent measurement responsibility (exercise one journey/surface
cluster read-only, one verdict per criterion, one consolidated table). Every decomposition trigger
cleared and both concern tests passed; the work ran well within the atomic tool-call envelope.

## Output

- `outputs/resilience-states-measurement.md` — access-note preamble (repository/commit identity only)
  + a `verdict_row_schema`-conforming table (`bar_id, live_status, observation`), one row per owned
  `BAR-*`, keyed by `bar_id`.

## Result

12 criteria judged: 0 met · 8 partial · 4 missing · 0 not_applicable.

- **missing**: BAR-026, BAR-027, BAR-248, BAR-260 — the first-use / cross-surface features they
  describe (landing, sign-up, onboarding; Notifications/dialogs/blocked-&-muted/followers) are absent
  from the three-route walking skeleton shipped at `c805525`.
- **partial**: BAR-028, BAR-029, BAR-226, BAR-240, BAR-259, BAR-261, BAR-262, BAR-263 — error/retry,
  inline-error-at-control, and draft-preservation patterns are present and sound, but empty states
  carry no next step, loading is plain text (not skeletons sized to real content), and expired
  sessions are not detected or routed to sign-in.

## Grounding & method

- Live product reached read-only and exercised through one throwaway account (register → login → post
  one chirp). Live API responses observed directly: timeline auth gate (401), user not-found (404),
  failed like (404), self-follow (403), authed empty vs post-populated timeline, SPA route-serving.
- Where rendered UI states cannot be captured outside a browser (WebAssembly bundle), grounded in the
  SPA/API source at `c805525` (`crates/chirp-frontend` views + shared error type, `crates/chirp-server`,
  `crates/chirp-types`) at repo-relative paths cited in each observation. No verdict assumed or
  confabulated; absent surfaces judged conservatively with the reason stated.

## Constraints honoured

- Read-only on the live product (only a throwaway account's own normal actions); no product code written;
  only `Nousix-LLC/nswe-demo` and the project's own deployment touched.
- Output carries no host/system/taskflow detail — repository identity, commit SHA, repo-relative paths,
  product API/route paths, and `BAR-*` ids only.
- Phase-B `design` methodology loader unavailable run-wide (`agent_domain_unset`); recorded, proceeded
  on the persona + release-bar statements per the brief.

## Dependents

`SUBTASK_journeys_fold` unions this table with the other eight clusters.
