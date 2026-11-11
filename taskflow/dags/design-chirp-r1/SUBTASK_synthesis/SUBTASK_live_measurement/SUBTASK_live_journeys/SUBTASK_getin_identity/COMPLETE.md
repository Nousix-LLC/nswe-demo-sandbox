# COMPLETE — SUBTASK_getin_identity

## What was done
Exercised the chirp product's get-in & identity journeys at `Nousix-LLC/nswe-demo` commit `c805525` and judged
the 22 `manual_user_check` `BAR-*` assigned to this cluster, each to one `live_status` and a grounded
observation. The live SPA and JSON API were both reachable and were exercised read-only with a single
throwaway test account (one sign-up, one handle-only login, one probe chirp); surfaces that the running UI
left thin or ambiguous were settled against the SPA/API source at `c805525`.

## Output produced
- `outputs/getin-identity-measurement.md` — a verdict table conforming to the inherited `verdict_row_schema`
  (columns `bar_id, live_status, observation`), one row per owned `BAR-*`, keyed by `bar_id`, with an
  access-note preamble recording only that the product was reached, by repository/commit identity.

## Verdict summary (22 owned criteria, each exactly one verdict)
- **met (2):** BAR-116, BAR-338 — a public/other-account response returns only public profile fields; no
  credential, contact, or session data leaks (credential and contact do not exist at this commit; the session
  token is returned only to the authenticating caller).
- **partial (4):** BAR-112 (single-account attribution and bearer presentation hold, but the token value
  encodes the account id as `tok-<n>-<id>`, so it is not truly opaque); BAR-303 (handle format and uniqueness
  enforced at the API, but no sign-up screen and the validation error is scoped to `body`); BAR-304
  (unknown-handle distinguishable via 404, but no wrong-secret failure path because no secret exists); BAR-316
  (refusals leak no owner-only data on the surfaces that exist, but the authority model has little surface to
  exercise at this commit).
- **missing (16):** BAR-014, BAR-015, BAR-113, BAR-114, BAR-115, BAR-200, BAR-206, BAR-207, BAR-213, BAR-230,
  BAR-231, BAR-236, BAR-300, BAR-321, BAR-322, BAR-323 — the credential, verified-contact, recovery,
  session-lifecycle (sign-out/expiry), and signed-out/get-in screen surfaces (landing, sign-up, sign-in,
  recover access, set-new-credential, sign-out) are architecturally absent at `c805525`. Sign-in is
  handle-only; account creation has no SPA surface; the only session-establishing affordance is a handle-only
  "Log in" in `/compose`.

## How it composes with the parent
Feeds `SUBTASK_journeys_fold`, which unions the nine cluster tables into
`../outputs/live-journeys-measurement.md` and asserts totality (139 `manual_user_check` `BAR-*`). This table
is disjoint from the other eight clusters and carries exactly its 22 owned `bar_id`s.

## Success criteria
- [x] Every owned `BAR-*` has exactly one `live_status` and a grounded observation; none omitted; none outside cluster.
- [x] Each observation grounded in an actual exercise of the live product or an actual `c805525` source artifact.
- [x] `live_status` values from the inherited vocab; `bar_id`s verbatim.
- [x] Read-only on the live product; output touches only `Nousix-LLC/nswe-demo` and the project's own deployment; no host/system/taskflow detail in the output.

## Notes / limitations
- The Phase-B `design` methodology loader was unavailable run-wide (`agent_domain_unset`); recorded and proceeded per the subtree hub.
- The product at `c805525` uses an in-memory store; the throwaway account and probe chirp do not persist across a restart. No deletion endpoint exists, so the test account was left as-is (read-only beyond its own normal actions).
