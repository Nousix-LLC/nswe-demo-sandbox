# COMPLETE — SUBTASK_ops_status_incident

## What was done
Authored the `status_and_incident` section fragment of the chirp operational-readiness design as
`outputs/status-incident.md`: section prose plus the `REQ-OPS-080..095` requirements (within the owned
`REQ-OPS-080..099` range), each with `statement`, testable `acceptance_criteria`, a `verification_method`
from the contract vocabulary, a `release_gating` flag, and `traces_to`. The fragment states how operators
and users learn when chirp is not serving and what the product owes a user while impaired, built on the
observability signals the dependency fragment defines.

## How it composes with the parent
- **Owns only its seam.** Section `status_and_incident`; `REQ-OPS-080..095` only (no number used outside
  the assigned `080..099` range; gaps `096..099` left free). The ancestor `id_and_traceability_schema.yaml`
  and this subtree's `reqs_ops_partition.yaml` are composed against, not redefined.
- **Builds on the dependency.** Incident detection references the observability serving/availability signal
  `REQ-OPS-075` and the metrics `REQ-OPS-072/074/076` from the COMPLETED `SUBTASK_ops_observability`
  fragment, rather than defining new signals.
- **References boundaries it does not own.** The user-facing degraded/error states are referenced as the
  experience design's (`REQ-UX-*`, `REQ-PROD-033`, `REQ-PROD-034`) — `REQ-OPS-090` states only the
  operational join. The data recovery-time objective is left to backups/recovery (`REQ-OPS-020..039`);
  `REQ-OPS-095` is time-to-restore-serving, stated as distinct.
- The synthesis gate (`SUBTASK_ops_synthesis`) reads this fragment, concatenates the section in
  `design_artifact_map` order, and folds the requirements into the consolidated register and traceability
  table.

## Requirement set (REQ-OPS-080..095)
- Incident detection and response: 080 (detect, don't wait), 081 (driven by observability signals), 082
  (proportionate severity), 083 (responsible operator — J9), 084 (defined response path; runbooks deferred).
- User-facing status/maintenance communication: 085 (users can learn of outage), 086 (status surface
  independent of the failed product), 087 (advance maintenance notice), 088 (no private/secret data —
  `REQ-DOM-035`), 089 (recovery communicated).
- Degraded-state experience boundary (referenced, not owned): 090 (fail into designed states —
  `REQ-PROD-033/034`), 091 (partial-failure containment — `REQ-DOM-115`).
- Availability as an operated commitment: 092 (stated proportionate target → `REQ-PROD-040`), 093 (measured
  from the serving signal, not asserted), 094 (announced maintenance accounted for), 095 (time-to-restore
  objective).

## Verification against success criteria
- [x] Composes against `../contracts/`; uses only `REQ-OPS-080..099`; schema not redefined; each requirement
      carries all contract fields; every `verification_method` is from the closed vocabulary
      (`manual_user_check`, `inspection`, `operational_check` used).
- [x] Incident detection/response, user-facing outage and maintenance communication, and a stated
      availability expectation are each testable requirements that build on the observability signals.
- [x] Each requirement `traces_to` a real `REQ-PROD-*`/`REQ-DOM-*` (`REQ-PROD-040`, `REQ-PROD-033/034`,
      `REQ-DOM-035`, `REQ-DOM-115`); the degraded-state boundary with `REQ-UX-*` is referenced, not owned.
- [x] Requirements only — status-page tooling, paging/alerting setup, and runbooks deferred to code DAGs.
- [x] Proportionate to a small hosted product; no enterprise incident programme.
- [x] Repository hygiene — no host/cluster/taskflow detail, no attribution trailer; operations described by
      product/repository identity.
- [x] avoid-ai-writing pass run over the fragment (P0/P1 tells); no flagged patterns remain.

## Environment note
The Phase-B `design` methodology loader is unavailable here (`engine_methodology_glob` returns
`agent_domain_unset`), as the subtree hub records. The product-design persona and the relayed bundle
guidance (Release Readiness primary; Release Definition, Product Strategy supporting) were applied; the
unavailability is recorded rather than blocked on.

## Output
- `outputs/status-incident.md`
