# COMPLETE — SUBTASK_abuse_privacy

## What this task was
Design the minimum abuse-resistance and privacy/data-rights surface for chirp (a public microblog)
as testable `REQ-ID-*` requirements in the `abuse_and_privacy_basics` section, to a releasable bar.
Requirements only; enforcement and data-handling "how" deferred to code / operational areas by prose.

## What was produced
- `outputs/abuse-privacy.md` — the `abuse_and_privacy_basics` section partial in the format fixed by
  `../contracts/req_id_partition.yaml`: section prose, eleven `REQ-ID-080..090` entries, and a
  "Notes for synthesis" block (cross-area seams + the threat each requirement answers). Repository-
  ready: no host/system/taskflow detail, no attribution trailer, plain checkable voice.

## The requirements (REQ-ID-080..090), within the owned range 080..099
- Abuse controls: 080 report a chirp/account (acknowledged), 081 stated rules a report references,
  082 a report is captured and routed to the operator surface, 083 block, 084 mute, 085 rate/volume
  limits as a first line against abuse.
- Privacy / data rights: 086 data minimization, 087 private-field protection (contact, credential,
  session never leak to other users / public responses / the report surface), 088 erasure on account
  deletion + session invalidation, 089 a stated retention posture, 090 a data-rights baseline
  (access, export, erasure).

## How it composes with the parent (SUBTASK_identity_trust)
- Composes against the parent id/traceability schema and the subtree `req_id_partition.yaml`: ids are
  `REQ-ID-<NNN>` only within 080..099; required fields (statement, acceptance_criteria,
  release_gating) present on every entry; verification_method drawn only from the inherited
  vocabulary (manual_user_check, automated_test, inspection, operational_check); schema not redefined.
- Every `REQ-ID-*` traces to ≥1 existing `REQ-PROD-*` (019, 021, 024, 025, 026, 027, 041 — all
  present in the product-requirements register).
- Release-gating: gated — 080, 081, 082, 085, 086, 087, 088, 090 (the reporting floor, limits, and
  the core privacy guarantees); ungated with stated reasons — 083, 084 (block/mute, per REQ-PROD-027
  the bar decides which gate v1) and 089 (a stated retention posture expected; bar sets the minimum).

## Seams handed to the synthesis (recorded in the output's Notes for synthesis)
- Public/private field boundary coordinated with `SUBTASK_authorization` (it owns *who may read
  which field*; this area owns the guarantee that private fields never leak).
- Acting on reports belongs to `SUBTASK_authorization` (REQ-PROD-028); this area only requires capture
  and routing (082). No `REQ-OPS-*` and no operator-action id minted here.
- Deletion outcome belongs to `SUBTASK_accounts_lifecycle`; session invalidation to
  `SUBTASK_auth_sessions`; 088 states the privacy outcome against both.
- Data export belongs to `SUBTASK_accounts_lifecycle` (REQ-PROD-019); 090 references it, does not
  redefine it.
- Rate-limit enforcement belongs to the operational-readiness limits-and-quotas area (REQ-OPS-*);
  085 states the requirement and traces REQ-PROD-041, naming that area so the synthesis coverage
  check records REQ-PROD-041's enforcement as carried there rather than as a hole.
- Threats answered (for the threat-model synthesis): harassment/unwanted interaction (080–084),
  denial of service/flooding (085), information disclosure (086/087/088/089), repudiation-partial
  (082), and the data-rights trust property (090). A cross-cutting transport-confidentiality
  requirement is flagged as a candidate for the synthesis's own range (100..119).

## Verification performed
- Field completeness: 11 headers + 55 field lines = 66 (11 × 6), every entry carries statement,
  acceptance_criteria, release_gating, verification_method, traces_to.
- Range: all ids within 080..099; no id outside range, no `REQ-OPS-*`, no `BAR-*`.
- Trace targets confirmed present in the product-requirements register.
- Writing-voice pass run over the prose; no machine-writing tells found.
