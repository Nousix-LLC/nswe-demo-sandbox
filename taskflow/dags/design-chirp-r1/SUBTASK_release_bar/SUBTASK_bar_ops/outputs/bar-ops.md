# Release bar — operational-readiness area (`BAR-400..499`)

This fragment holds the `BAR-*` criteria that enforce the release-gating operational requirements of the
operational-readiness design (`REQ-OPS-*`). Each criterion is a concrete, testable release condition — something a
person who was not in the room can check against the live product and reach the same verdict — not a restatement of
the requirement. A single criterion may enforce several related requirements; it references every `REQ-OPS-*` it
holds. Every criterion carries one `verification_method` from the frozen vocabulary (`manual_user_check`,
`automated_test`, `inspection`, `operational_check`) and a `proposed_stage` (`usable_early` | `releasable`); the
synthesis hub owns the final cross-cutting staging line.

The operational-readiness design marks 59 of its 75 requirements release-gating. All 59 are covered here; the coverage
note at the end lists each gating `REQ-OPS-*` and the `BAR-*` that holds it. The 16 non-gating requirements
(`REQ-OPS-047, 048, 067, 070, 071, 073, 074, 076, 078, 082, 084, 087, 089, 091, 094, 095`) are deliberately not minted
into bar criteria; they are quality and depth the product should grow into, not conditions the release turns on.

Most operational criteria are proven by an `operational_check` — observing a property of the running product
(data survives a restart, a backup restores, a limit is enforced) — because that is what "beyond it runs" means for
operations. Where the condition is a written posture or a configured property rather than a behaviour, the method is
`inspection`; where a person exercises the product and reads the result, `manual_user_check`; where a repository test
can assert it, `automated_test`.

---

## Durable data (`BAR-400..412`)

#### BAR-400
- **statement**: The deployment runs the product's authoritative state in a durable store that is a separate,
  persistent component from the serving process, with its own lifecycle; stopping or replacing the serving process
  does not stop or reset the store, and no deployment configuration keeps authoritative state only in serving-process
  memory. The in-memory backing of the `ChirpRepository` seam at `Nousix-LLC/nswe-demo @ c805525` does not meet this;
  closing it is the blocker this bar turns on.
- **references**: REQ-OPS-002, REQ-OPS-009
- **verification_method**: operational_check
- **proposed_stage**: usable_early

#### BAR-401
- **statement**: On a populated deployment, each of a serving-process restart, a redeploy, and a replacement of the
  serving process with a fresh instance leaves every Account and its Chirps, Follows, and Likes present and unchanged,
  with no manual step to recover them — demonstrating the authoritative state did not live in the process that was
  replaced.
- **references**: REQ-OPS-001, REQ-OPS-003
- **verification_method**: operational_check
- **proposed_stage**: usable_early

#### BAR-402
- **statement**: A create or change the product has confirmed to a person — a posted Chirp, a Follow or unfollow, a
  Like or unlike, a profile edit, an account deletion — is present after a restart or process replacement that happens
  immediately after the success response, with no further action taken. No acknowledged write is lost in the window
  right after its acknowledgement.
- **references**: REQ-OPS-005
- **verification_method**: operational_check
- **proposed_stage**: usable_early

#### BAR-403
- **statement**: After the serving process is restarted or replaced, the durable data still satisfies the domain
  invariants: every reference resolves, ids are unchanged and never reused, each Account's follower/following counts
  and each Chirp's like count equal their current edges, and any applied account deletion stays applied. Adding and
  removing a Follow and a Like after the restart moves the counts by exactly one each way.
- **references**: REQ-OPS-006
- **verification_method**: operational_check
- **proposed_stage**: usable_early

#### BAR-404
- **statement**: A restart, crash, or process replacement during a write leaves the durable data consistent: after
  recovery each interrupted operation — posting a Chirp, following, deleting an account that has Chirps, Follows, and
  Likes — is observably either fully applied or fully absent, with no half-applied state (a Chirp with no resolvable
  author, a half-deleted Account with dangling references, a count out of step with its edges).
- **references**: REQ-OPS-008
- **verification_method**: operational_check
- **proposed_stage**: usable_early

#### BAR-405
- **statement**: An upgrade performed in production that changes how the data is shaped preserves the user data that
  existed before it: afterward the Accounts, Chirps, Follows, and Likes created before the upgrade are all present and
  their references still resolve, with none lost or corrupted by the upgrade.
- **references**: REQ-OPS-004
- **verification_method**: operational_check
- **proposed_stage**: releasable

#### BAR-406
- **statement**: While an account exists, its data — the Account and profile, its Chirps, its Follows, its Likes —
  remains present and complete over a sustained operating period with ordinary restarts and redeploys, without the
  holder re-creating it. Any age-out the product applies to a live account's content is found stated in the retention
  posture, not met as an unexplained loss.
- **references**: REQ-OPS-010
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

#### BAR-407
- **statement**: When an account is deleted, the stated deletion outcome holds immediately (the account cannot sign
  in and no dangling reference remains), and after the product's stated, bounded retention window the deleted
  account's data is no longer present in the live durable store. The observed behaviour matches the stated window.
- **references**: REQ-OPS-011
- **verification_method**: operational_check
- **proposed_stage**: releasable

#### BAR-408
- **statement**: The product states a maximum backup-retention bound that limits how long a deleted account's data
  can remain recoverable in backups, and that bound is consistent with the deleted-account retention posture; no
  backup older than the bound is retained, so deleted-account data cannot be recovered from backups indefinitely.
- **references**: REQ-OPS-012
- **verification_method**: inspection
- **proposed_stage**: releasable

#### BAR-409
- **statement**: An active Session survives a restart or redeploy — a request carrying its token is still accepted as
  the same account afterward — while a Session that has ended (sign-out) or passed its lifetime is refused after a
  restart and after a restore from a backup taken while it was active, never revived.
- **references**: REQ-OPS-014
- **verification_method**: operational_check
- **proposed_stage**: usable_early

#### BAR-410
- **statement**: The account's Credential and Verified contact are retained durably — a person can still sign in and
  the recovery path still recognises the contact after a restart and a restore — never appear in any public response,
  and are no longer retained in the live durable store once the account is deleted and its retention window elapses.
- **references**: REQ-OPS-015
- **verification_method**: operational_check
- **proposed_stage**: usable_early

#### BAR-411
- **statement**: For a signed-in account with Chirps and Follows, the data the product retains and the data a
  self-service export yields are the same set — the account's profile, its complete Chirps, and its complete followed
  Accounts — matching the committed durable state. No retained category of a person's own data is missing from what
  they can export.
- **references**: REQ-OPS-013
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

#### BAR-412
- **statement**: The product's data-retention and deletion posture is published where a user and an operator can find
  it, and it names what is retained, the live-account retention, the deleted-account retention window, the
  backup-retention bound, and session and private-identity-data handling. The stated posture matches the behaviour the
  retention and deletion criteria verify; a discrepancy is a defect.
- **references**: REQ-OPS-016
- **verification_method**: inspection
- **proposed_stage**: releasable

---

## Backups and recovery (`BAR-420..432`)

#### BAR-420
- **statement**: An operated deployment with user data produces a backup of its durable data (Accounts, Chirps,
  Follows, Likes) on the product's stated, regular cadence without an operator remembering to take it, and each
  produced backup is recorded where an operator can see it was taken. Observed over several cadence intervals, a
  backup appears each interval, not ad hoc.
- **references**: REQ-OPS-020
- **verification_method**: operational_check
- **proposed_stage**: releasable

#### BAR-421
- **statement**: Backups are kept for the product's stated, bounded retention period and no longer: a backup within
  the period is available to restore from, a backup older than the period is no longer retained, and the period is
  consistent with the deleted-account backup bound (BAR-408). The oldest available backup is no older than the stated
  period.
- **references**: REQ-OPS-021
- **verification_method**: inspection
- **proposed_stage**: releasable

#### BAR-422
- **statement**: A backup taken while the product is serving restores to a state in which the model's invariants hold
  — every reference resolves, ids are unchanged and unreused, counts equal their edges — with no partially captured
  write visible. A backup that restores to an invariant-violating state is treated as unusable, not accepted.
- **references**: REQ-OPS-022
- **verification_method**: operational_check
- **proposed_stage**: releasable

#### BAR-423
- **statement**: Backups are held so that losing the primary durable store does not also lose them: the two do not
  share a single point of failure, and with the primary store made unavailable a retained backup is still reachable to
  restore from.
- **references**: REQ-OPS-023
- **verification_method**: inspection
- **proposed_stage**: releasable

#### BAR-424
- **statement**: The product states a recovery-point objective — a bounded quantity of recent durable data a recovery
  may lose, no tighter than the backup cadence can achieve — and a recovery-time objective — a bounded duration the
  product may be unavailable during recovery, consistent with its availability commitment. Both name a bounded figure,
  not "none" without a mechanism to achieve it.
- **references**: REQ-OPS-024, REQ-OPS-025
- **verification_method**: inspection
- **proposed_stage**: releasable

#### BAR-425
- **statement**: The restore procedure is written down and followable by an operator who did not build the system:
  following it, that operator restores a deployment from a retained backup and returns it to service without knowledge
  that is not in the procedure, and the procedure names what is restored (Accounts, Chirps, Follows, Likes) and how the
  product is returned to serving.
- **references**: REQ-OPS-026
- **verification_method**: inspection
- **proposed_stage**: releasable

#### BAR-426
- **statement**: A restore from a retained backup returns the Accounts, Chirps, Follows, and Likes present at the
  backup point intact and consistent — references resolve, ids are unchanged and unreused, counts equal their edges,
  and an account deleted before the backup stays deleted with no dangling reference. A failing invariant is reported as
  an unsuccessful restore, never silently accepted.
- **references**: REQ-OPS-027, REQ-OPS-007
- **verification_method**: operational_check
- **proposed_stage**: releasable

#### BAR-427
- **statement**: A timed restore from a backup on a representative deployment recovers the product within the stated
  recovery-time objective and loses no more than the stated recovery-point objective, both measured rather than
  asserted. A drill that exceeds either objective is reported as a defect in the objective or the procedure, not
  ignored.
- **references**: REQ-OPS-028
- **verification_method**: operational_check
- **proposed_stage**: releasable

#### BAR-428
- **statement**: A deploy can be rolled back to the last working version as a routine operator operation with no
  user-data loss: after the rollback the product serves on the prior version and every Account, Chirp, Follow, and Like
  that existed before the deploy is present and unchanged, with no manual reconstruction.
- **references**: REQ-OPS-029
- **verification_method**: operational_check
- **proposed_stage**: releasable

#### BAR-429
- **statement**: A deploy that damages or loses durable data can be recovered from by restoring from a pre-deploy
  backup following the restore procedure, returning the durable data to an intact and consistent state (as BAR-426)
  within the stated objectives. The product does not depend on the damaging deploy being reversible in place.
- **references**: REQ-OPS-030
- **verification_method**: operational_check
- **proposed_stage**: releasable

#### BAR-430
- **statement**: A restore from a recent backup is exercised on the product's stated recurring drill cadence against a
  store where its correctness can be checked; the drill verifies the restored data's invariants and timing, and a
  failed drill is recorded and acted on rather than passed over. The drill is recurring, not a one-time pre-release
  event.
- **references**: REQ-OPS-031
- **verification_method**: operational_check
- **proposed_stage**: releasable

#### BAR-431
- **statement**: A scheduled backup that fails or does not run is surfaced to operators as a visible failure state or
  alert, not absorbed silently, so a deployment cannot drift into having no recent usable backup unnoticed. A run of
  successful backups and a failed backup are distinguishable to an operator.
- **references**: REQ-OPS-032
- **verification_method**: operational_check
- **proposed_stage**: releasable

#### BAR-432
- **statement**: The product's backup-and-recovery posture is published where an operator can find it, naming the
  backup cadence and retention, the recovery-point and recovery-time objectives, and the restore and rollback
  procedures; the stated posture matches the behaviour the backup-and-recovery criteria verify. A discrepancy is a
  defect.
- **references**: REQ-OPS-033
- **verification_method**: inspection
- **proposed_stage**: releasable

---

## Limits and quotas (`BAR-440..445`)

#### BAR-440
- **statement**: The product bounds the request rate it accepts from a single client, applied on both the
  authenticated surface and the unauthenticated surface (landing, sign-up, sign-in) and identified by client rather
  than only by account. A client issuing requests far faster than a person would is refused or slowed past a point —
  and cannot escape the bound by not signing in — while other clients continue to be served normally.
- **references**: REQ-OPS-040, REQ-OPS-046
- **verification_method**: operational_check
- **proposed_stage**: releasable

#### BAR-441
- **statement**: State-creating actions — posting a Chirp, following, liking — are held to their own, tighter rate
  limit than reads: performing one repeatedly far faster than a person would is refused or throttled past a point,
  while reading remains possible within its own limit meanwhile.
- **references**: REQ-OPS-041
- **verification_method**: operational_check
- **proposed_stage**: releasable

#### BAR-442
- **statement**: The volume of content one account can create over a longer rolling window is bounded: creating
  content continuously at or just under the per-action rate limit for a sustained period is eventually bounded for that
  window rather than accumulating without limit, and resumes in a later window.
- **references**: REQ-OPS-042
- **verification_method**: operational_check
- **proposed_stage**: releasable

#### BAR-443
- **statement**: A request whose body is far larger than any valid chirp or form submission (for example a
  multi-megabyte body to a write endpoint) is refused with an error before the body is processed, while a normal,
  within-bounds request to the same endpoint succeeds.
- **references**: REQ-OPS-043
- **verification_method**: automated_test
- **proposed_stage**: usable_early

#### BAR-444
- **statement**: Every endpoint that returns a list serves at most the server's maximum page size: a request with no
  page size and a request with a page size well above the maximum both return at most the maximum number of items, with
  a continuation cursor when more remain, rather than the full result set.
- **references**: REQ-OPS-044
- **verification_method**: automated_test
- **proposed_stage**: usable_early

#### BAR-445
- **statement**: Exceeding any limit above refuses or throttles the excess rather than serving it, and returns a
  typed, machine-readable error whose category identifies it as a limit being hit — distinct from a validation error or
  a not-found — so a caller can tell it was limited and back off. The error is the typed contract category, not an
  ad-hoc string.
- **references**: REQ-OPS-045
- **verification_method**: operational_check
- **proposed_stage**: releasable

---

## Observability (`BAR-460..468`)

#### BAR-460
- **statement**: The product exposes a readiness signal, distinct from liveness, whose meaning is that it can serve
  users: it reports ready when the durable store is reachable and the product can serve, reports not-ready when the
  store is unreachable from the serving process, carries a machine-distinguishable ready/not-ready indication an
  orchestrator can branch on without reading prose, and returns to ready on its own — without a restart or redeploy —
  once the condition that made it not-ready clears.
- **references**: REQ-OPS-060, REQ-OPS-061, REQ-OPS-064, REQ-OPS-065
- **verification_method**: operational_check
- **proposed_stage**: usable_early

#### BAR-461
- **statement**: The liveness signal reports the serving process's own health only: with the durable store
  unreachable but the process otherwise healthy, liveness reports alive while readiness reports not-ready, so an
  orchestrator restarts a genuinely crashed process but does not kill one that is alive and waiting on its store.
  Liveness reports not-alive only when the process itself cannot make progress.
- **references**: REQ-OPS-062
- **verification_method**: operational_check
- **proposed_stage**: usable_early

#### BAR-462
- **statement**: The health/readiness endpoint responds when queried with no account or session, and its response
  carries no credential, session token, verified-contact value, or other private account data, and no secret such as a
  connection string — it conveys serving status, not the contents of the system.
- **references**: REQ-OPS-063
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

#### BAR-463
- **statement**: The product records its operational events as structured, machine-parseable records with consistent,
  named fields (such as timestamp, severity, event category, and outcome) that a log tool can parse and filter, not as
  free-form prose.
- **references**: REQ-OPS-066
- **verification_method**: inspection
- **proposed_stage**: usable_early

#### BAR-464
- **statement**: The product's logs cover the operational events needed to explain operation and failure: request
  handling and its outcome, errors and failures with a cause category, process start and stop, changes in
  durable-store connectivity, and successful and failed authentication outcomes. Provoking each in a running product
  produces a distinct, categorized log event with enough context to tell what happened.
- **references**: REQ-OPS-068
- **verification_method**: operational_check
- **proposed_stage**: releasable

#### BAR-465
- **statement**: No credential, session token, verified-contact value, or other private account data appears in the
  product's logs or its audit trail, in any field at any severity: exercising sign-up, sign-in, recovery, session use,
  and representative administrative actions and then inspecting the logs and audit entries shows accounts referenced by
  non-secret identifier only, with no private data or secret present.
- **references**: REQ-OPS-069, REQ-OPS-079
- **verification_method**: inspection
- **proposed_stage**: usable_early

#### BAR-466
- **statement**: The product exposes serving metrics that report the rate of requests handled and the rate failing,
  broken down enough to see which class of surface is affected (for example reads versus writes, or by outcome
  category); the metric labels carry no handle-linked private data, credential, or contact value.
- **references**: REQ-OPS-072
- **verification_method**: operational_check
- **proposed_stage**: releasable

#### BAR-467
- **statement**: The product exposes a serving/availability signal that makes "the product is not serving its core
  loop" an observable fact: put into a degraded state in which the core loop does not work for users, the signal
  reflects the degradation; returned to serving, it reflects recovery. The signal is suitable to drive automated
  detection.
- **references**: REQ-OPS-075
- **verification_method**: operational_check
- **proposed_stage**: releasable

#### BAR-468
- **statement**: Every action taken through the supported administrative surface — assisting a user's recovery,
  removing content, disabling or actioning an account — produces an audit entry naming the acting operator identity,
  the action taken, the target account or content, and the time. An administrative action that reaches accounts or
  content leaves no untraced path.
- **references**: REQ-OPS-077
- **verification_method**: operational_check
- **proposed_stage**: releasable

---

## Status and incident (`BAR-480..487`)

#### BAR-480
- **statement**: A serving degradation — the product not serving its core loop, or serving it with elevated errors —
  is detected from the observability signals (the serving/availability signal, request- and error-rate metrics,
  saturation/headroom, durable-store interaction health) and raises a notification to the responsible operator within a
  bounded time, without a user having to report it first. Each alerting condition names an observability signal and a
  threshold or state on it; returning the product to serving raises no further alert for that incident.
- **references**: REQ-OPS-080, REQ-OPS-081
- **verification_method**: operational_check
- **proposed_stage**: releasable

#### BAR-481
- **statement**: There is a stated role accountable for acknowledging and acting on a detected incident, so a fired
  alert has an owner; a detected major incident has a defined responder and no detected incident is left with no one
  responsible for it.
- **references**: REQ-OPS-083
- **verification_method**: inspection
- **proposed_stage**: releasable

#### BAR-482
- **statement**: When the product is unavailable or degraded, a person consulting a status surface or in-product
  notice sees that chirp itself is affected rather than being left to infer it from a failed action or a spinner; when
  the product is serving normally, the surface shows normal operation.
- **references**: REQ-OPS-085
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

#### BAR-483
- **statement**: The surface users consult to learn of an outage is reachable when the serving product and its
  durable store are fully offline: with the product taken fully down, the status surface is still reachable and reports
  the product as unavailable. Its availability does not require the product's serving path, store, or process to be up.
- **references**: REQ-OPS-086
- **verification_method**: operational_check
- **proposed_stage**: releasable

#### BAR-484
- **statement**: Nothing published on the status surface, in an in-product outage notice, or in a maintenance
  announcement contains private account data or secret material — no credential, session token, verified-contact value,
  connection string, or raw internal error detail that discloses them. Inspected for a representative outage and a
  maintenance notice, the content describes product status in the terms a user needs and nothing more.
- **references**: REQ-OPS-088
- **verification_method**: inspection
- **proposed_stage**: releasable

#### BAR-485
- **statement**: With the durable store made unreachable while the serving process stays up, a user exercising the
  core loop meets the explained degraded or error experience the experience design specifies — an explained error, a
  preserved in-progress draft, a routed-to-sign-in on an expired session — not a blank page or a crashed process.
- **references**: REQ-OPS-090
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

#### BAR-486
- **statement**: The product states an availability target that defines what "reasonably available" means for it — a
  specific figure over a stated window (for example a monthly serving-availability target), proportionate to a small
  hosted service rather than an enterprise commitment — written down, not left implicit.
- **references**: REQ-OPS-092
- **verification_method**: inspection
- **proposed_stage**: releasable

#### BAR-487
- **statement**: Availability is computed in production from the serving/availability signal over the stated window,
  counting the product as unavailable when the signal shows it not serving its core loop, so whether the target was met
  is a measured fact rather than a claim. Over a window that includes at least one serving interruption, the measured
  result reflects the interruption and can be compared against the stated target.
- **references**: REQ-OPS-093
- **verification_method**: operational_check
- **proposed_stage**: releasable

---

## Coverage note — every release-gating `REQ-OPS-*` and the `BAR-*` that covers it

This lets the synthesis gate assert `GATING_REQ_COVERAGE` for the operations area without re-deriving the gating set.
The gating set is the 59 `REQ-OPS-*` whose `release_gating` field is `true` in the operational-readiness design
(`operational-readiness.md`, OPS traceability table). Each is referenced by at least one `BAR-*` in this fragment.

| Release-gating REQ-OPS | Covered by | Concern |
|------------------------|------------|---------|
| REQ-OPS-001 | BAR-401 | Durable data |
| REQ-OPS-002 | BAR-400 | Durable data |
| REQ-OPS-003 | BAR-401 | Durable data |
| REQ-OPS-004 | BAR-405 | Durable data |
| REQ-OPS-005 | BAR-402 | Durable data |
| REQ-OPS-006 | BAR-403 | Durable data |
| REQ-OPS-007 | BAR-426 | Durable data (restore invariants) |
| REQ-OPS-008 | BAR-404 | Durable data |
| REQ-OPS-009 | BAR-400 | Durable data |
| REQ-OPS-010 | BAR-406 | Durable data (retention) |
| REQ-OPS-011 | BAR-407 | Durable data (retention) |
| REQ-OPS-012 | BAR-408 | Durable data (retention) |
| REQ-OPS-013 | BAR-411 | Durable data (retention/export) |
| REQ-OPS-014 | BAR-409 | Durable data (sessions) |
| REQ-OPS-015 | BAR-410 | Durable data (private identity data) |
| REQ-OPS-016 | BAR-412 | Durable data (stated posture) |
| REQ-OPS-020 | BAR-420 | Backups and recovery |
| REQ-OPS-021 | BAR-421 | Backups and recovery |
| REQ-OPS-022 | BAR-422 | Backups and recovery |
| REQ-OPS-023 | BAR-423 | Backups and recovery |
| REQ-OPS-024 | BAR-424 | Backups and recovery |
| REQ-OPS-025 | BAR-424 | Backups and recovery |
| REQ-OPS-026 | BAR-425 | Backups and recovery |
| REQ-OPS-027 | BAR-426 | Backups and recovery |
| REQ-OPS-028 | BAR-427 | Backups and recovery |
| REQ-OPS-029 | BAR-428 | Backups and recovery |
| REQ-OPS-030 | BAR-429 | Backups and recovery |
| REQ-OPS-031 | BAR-430 | Backups and recovery |
| REQ-OPS-032 | BAR-431 | Backups and recovery |
| REQ-OPS-033 | BAR-432 | Backups and recovery |
| REQ-OPS-040 | BAR-440 | Limits and quotas |
| REQ-OPS-041 | BAR-441 | Limits and quotas |
| REQ-OPS-042 | BAR-442 | Limits and quotas |
| REQ-OPS-043 | BAR-443 | Limits and quotas |
| REQ-OPS-044 | BAR-444 | Limits and quotas |
| REQ-OPS-045 | BAR-445 | Limits and quotas |
| REQ-OPS-046 | BAR-440 | Limits and quotas |
| REQ-OPS-060 | BAR-460 | Observability (readiness) |
| REQ-OPS-061 | BAR-460 | Observability (readiness) |
| REQ-OPS-062 | BAR-461 | Observability (liveness) |
| REQ-OPS-063 | BAR-462 | Observability (health endpoint) |
| REQ-OPS-064 | BAR-460 | Observability (readiness) |
| REQ-OPS-065 | BAR-460 | Observability (readiness) |
| REQ-OPS-066 | BAR-463 | Observability (logging) |
| REQ-OPS-068 | BAR-464 | Observability (logging) |
| REQ-OPS-069 | BAR-465 | Observability (no secrets) |
| REQ-OPS-072 | BAR-466 | Observability (metrics) |
| REQ-OPS-075 | BAR-467 | Observability (serving signal) |
| REQ-OPS-077 | BAR-468 | Observability (audit trail) |
| REQ-OPS-079 | BAR-465 | Observability (no secrets) |
| REQ-OPS-080 | BAR-480 | Status and incident |
| REQ-OPS-081 | BAR-480 | Status and incident |
| REQ-OPS-083 | BAR-481 | Status and incident |
| REQ-OPS-085 | BAR-482 | Status and incident |
| REQ-OPS-086 | BAR-483 | Status and incident |
| REQ-OPS-088 | BAR-484 | Status and incident |
| REQ-OPS-090 | BAR-485 | Status and incident |
| REQ-OPS-092 | BAR-486 | Status and incident |
| REQ-OPS-093 | BAR-487 | Status and incident |

**Count**: 59 release-gating `REQ-OPS-*`, each covered by ≥1 `BAR-*`. Bars minted: `BAR-400..412` (13),
`BAR-420..432` (13), `BAR-440..445` (6), `BAR-460..468` (9), `BAR-480..487` (8) — 49 criteria, all within the
`BAR-400..499` range owned by this spoke.

### Staging note (proposed; the synthesis hub finalizes the cross-cutting line)

The proposed `usable_early` set is the operations floor a first usable version already needs: the product keeps data
across restart and redeploy and never leaves it half-applied (BAR-400..404, 406, 409, 410), refuses obviously abusive
payloads and unbounded list reads (BAR-443, 444), is operable and observable enough to run under an orchestrator and
to diagnose (BAR-460..463), and never writes secrets to its logs or audit trail (BAR-465). Everything the release
requires on top — backups, recovery, drills, and the stated recovery objectives; the full rate- and volume-limiting
posture; metrics, the serving signal, and the audit trail; and the incident, status, and availability apparatus — is
proposed `releasable`. Two criteria that read as foundational are nonetheless proposed `releasable` because they
depend on work owned elsewhere: BAR-405 (upgrade-preserves-data) presumes an upgrade path that a first cut may not yet
have, and BAR-485 (fails into the designed degraded states) depends on the experience area's error and degraded
states existing. The synthesis hub owns the one coherent MVP-vs-releasable line across all five areas and may move any
of these for cross-area coherence.
