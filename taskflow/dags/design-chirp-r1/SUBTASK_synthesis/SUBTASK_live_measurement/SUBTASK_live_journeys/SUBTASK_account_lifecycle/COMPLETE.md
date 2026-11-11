# COMPLETE — SUBTASK_account_lifecycle

## Task
Measure the 20 `manual_user_check` `BAR-*` of the account-management & lifecycle cluster against the live
chirp product at `Nousix-LLC/nswe-demo` commit `c805525`, one `live_status` + grounded observation each.

## Output produced
- `outputs/account-lifecycle-measurement.md` — a `bar_id`-keyed verdict table conforming to the inherited
  `verdict_row_schema` (columns `bar_id, live_status, observation`), with an access-note header and a shared
  finding. One row per owned `BAR-*`.

## Result
All 20 owned criteria are judged **`missing`**. Every account-lifecycle release surface the cluster measures —
settings hub, edit profile / profile update, account & contact (verified contact), sessions & devices
management, data export, account deletion, and a stated data-rights baseline — does not exist at `c805525`.

Grounded two ways that agree:
- **Live exercise** of the running product (read-only, one throwaway account): `PUT`/`PATCH`/`DELETE
  /api/users/{id}` → 405; `GET`/`DELETE /api/sessions` → 405; `/api/export`, `/api/users/{id}/export`,
  `/api/users/{id}/contact` → SPA index fallback; every settings/account/export/delete client route → the
  index shell ("Not found" in the SPA, whose only routes are `/`, `/compose`, `/user/:id`).
- **Source at `c805525`**: the complete server route table and handler set, the complete wire DTO set, and the
  frontend route table and module list contain none of these surfaces; the `User` model has no contact field.

No criterion is `not_applicable` (all are in release scope) or `partial` (none of the required behaviour is
present). Conservative where the WASM SPA could not be driven headlessly, settled against `c805525` source.

## Verification performed
- Totality: all 20 owned `BAR-*` present, each exactly once; no `BAR-*` outside the cluster.
- Vocabulary: every `live_status` ∈ {met, partial, missing, not_applicable}; every `bar_id` verbatim.
- Grounding: every observation cites a live probe result and/or a `c805525` source artifact; none assumed.
- Hygiene: output carries no host/system/taskflow detail — repository identity (`Nousix-LLC/nswe-demo`,
  `c805525`, repo-relative paths, `BAR-*`/`REQ-*` ids) only. Verified by scan.

## Notes
- Phase-B `design` methodology loader unavailable run-wide (`agent_domain_unset`); limitation recorded,
  proceeded per brief using the principal-product-designer persona and the relayed ReleaseBar guidance.
- The throwaway test account could not be removed afterward — there is no account-deletion surface, which is
  itself part of the finding. The `c805525` deployment uses an in-memory store that resets on restart.
