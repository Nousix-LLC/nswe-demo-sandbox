# Backups and recovery

This is the `backups_and_recovery` section of `design/operational-readiness.md`: the **backup and
recovery path** a release of chirp requires, stated as testable `REQ-OPS-*` requirements. The domain
design fixed that the capability must exist — the durable user data can be backed up and restored, and a
restore brings the Accounts, Chirps, Follows, and Likes back consistent with every model invariant
(`REQ-DOM-116`), and the product-level need is a release-gating product requirement (`REQ-PROD-038`). The
durable-data section (`REQ-OPS-001..019`) fixed the operational durability posture this path protects:
authoritative state lives in a durable store distinct from the serving process, and the invariants the
model requires after a restart must hold again after a restore (`REQ-OPS-007`). This section does not
restate either. It states what an **operator is owed** so that durable data, once it exists, can actually
be recovered: that it is backed up on a known cadence, kept for a known period, recoverable to stated loss
and downtime targets, restorable by a defined procedure that returns a correct product, recoverable after a
bad deploy, and proven restorable rather than merely produced. This is the operational face of the operator
journey's unmet need — *backup and recovery for durable data* (J9) — which the product requirements record
as a release gap.

## What this section fixes, and what it defers

- **In this section**: that durable user data is backed up on a stated, regular cadence; that backups are
  retained for a stated, bounded period; that each backup is an internally consistent point-in-time image
  held independently of the primary store; a recovery-point target (tolerable data loss) and a
  recovery-time target (tolerable downtime); a defined, operator-performable restore procedure that returns
  the Accounts, Chirps, Follows, and Likes intact and consistent; recovery from a failed or data-damaging
  deploy; and the requirement that backups are periodically proven restorable, that backup failures are
  surfaced rather than silent, and that the whole posture is written where an operator can find it.
- **Referenced, owned elsewhere**: the durability posture these requirements protect and the
  invariants-after-restore bar they are written against (`REQ-OPS-001..019`, especially `REQ-OPS-007`;
  durable-data) — consumed here by reference, not restated; the backup-retention bound as it constrains
  **deleted-account** data (`REQ-OPS-012`, durable-data), which this section's retention requirement builds
  on rather than redefines; the persistence model and its invariants (`REQ-DOM-100..118`, domain design);
  the alerting *signal* that carries a backup failure to an operator, which is the observability section's
  (`REQ-OPS-060..079`) — this section states that a failure must be surfaced, not how it is signalled.
- **Deferred to the code work (the "how")**: which backup tool or mechanism, which storage target, the
  snapshot or replication method, the restore scripting, and the deploy/rollback machinery. Every
  requirement below is a property the operated product must have, not a mechanism; where a mechanism is
  tempting it is stated as the property and the choice is handed to the engineering code DAGs.

Entities are named by the domain model's canonical vocabulary (Account, Chirp, Follow, Like, Session); this
section introduces none the model does not define. The product and the durable store are named by
repository identity — `Nousix-LLC/nswe-demo @ c805525`, the `ChirpRepository` seam in the `chirp-server`
crate — never by any host, cluster, or deployment address.

## The posture in prose

**A backup is only real once it has brought a correct product back.** The domain design already requires
that the capability exists (`REQ-DOM-116`); the operational requirement is that the capability is run as a
standing part of operating the service and is trusted because it has been exercised. A deployment that
produces backups it has never restored from has a file, not a recovery path. The bar this section is
written to is that an operator who has lost the durable store can, following a written procedure, bring the
product back to a known-good point within a stated time, and that what comes back satisfies the same
invariants a restart must satisfy (`REQ-OPS-007`, `REQ-DOM-110/111/107`): references resolve, ids are
unchanged and never reused, counts equal their edges, and applied account deletions stay applied.

**Cadence and retention set the two numbers a person's recovery depends on.** How often a backup is taken
bounds how much a person can lose — the work done since the last good backup. How long backups are kept
bounds how far back an operator can reach, and, in the other direction, how long a deleted account's data
can still be recovered from a backup. The durable-data section already fixed that a maximum backup-retention
bound exists and is consistent with the deletion posture (`REQ-OPS-012`); this section states the cadence
and the retention period themselves, and keeps them consistent with that bound rather than redefining it.

**Loss and downtime are commitments, not hopes.** A releasable product that can be operated states how much
data it is willing to lose in a disaster (a recovery-point objective) and how long it is willing to be down
while recovering (a recovery-time objective), and it sets them so they can be met — the recovery-point
objective no tighter than the backup cadence allows, the recovery-time objective no tighter than a
rehearsed restore achieves. A target nobody has measured a restore against is an aspiration; the restore
drill is what turns it into a commitment.

**A bad deploy is the disaster most likely to happen.** Hardware loss is rare; a deploy that breaks the
product or damages its data is routine enough that recovering from one is part of operating the service. A
failed deploy must be reversible to the last working version without losing user data, and a deploy that
has already damaged data must be recoverable by restoring from backup — consistent with the domain
requirement that an upgrade preserves existing data (`REQ-DOM-118`). The rollback and restore are the same
recovery path this section defines, applied to the most common cause of needing it.

The formal requirements are **REQ-OPS-020..033** in the register below.

## Requirements and acceptance criteria (`REQ-OPS-020..039`)

Each requirement carries an `id` (within this section's assigned range `REQ-OPS-020..039`), a `statement`
(what must be true in production, from the operator's side), testable `acceptance_criteria`, a
`verification_method` from the contract vocabulary (`manual_user_check`, `automated_test`, `inspection`,
`operational_check`), a `release_gating` flag, and `traces_to` the product/domain requirement it builds on.
The range is generous; it is not filled, and the gaps are deliberate.

### Backup posture: cadence, retention, consistency, independence

#### REQ-OPS-020 — Durable user data is backed up on a stated, regular cadence
- **statement**: An operated chirp deployment backs up its durable user data — Accounts, Chirps, Follows, Likes — on a stated, regular cadence, as a standing part of operating the service rather than as an occasional manual act. The product states what the cadence is; backups are produced on it without an operator having to remember to take them.
- **acceptance_criteria**: Find the product's stated backup cadence. On an operated deployment with user data, observe over a period spanning several cadence intervals that a backup is produced each interval without manual intervention, and that each produced backup is recorded where an operator can see it was taken. Backups appear on the stated cadence, not ad hoc.
- **verification_method**: operational_check
- **release_gating**: true
- **traces_to**: REQ-PROD-038, REQ-DOM-116

#### REQ-OPS-021 — Backups are retained for a stated, bounded period
- **statement**: Backups are kept for a stated retention period that bounds how far back an operator can recover, and that period is bounded above so backups do not accumulate indefinitely. The retention period is consistent with the maximum backup-retention bound the durable-data section fixed for deleted-account data (`REQ-OPS-012`): a backup older than the stated period has aged out and is no longer retained.
- **acceptance_criteria**: Find the product's stated backup-retention period and confirm it is consistent with the deleted-account backup bound (`REQ-OPS-012`). On an operated deployment, confirm that backups within the period are available to restore from and that backups older than the period are no longer retained. The oldest available backup is no older than the stated period.
- **verification_method**: inspection
- **release_gating**: true
- **traces_to**: REQ-PROD-038, REQ-DOM-037

#### REQ-OPS-022 — Each backup is an internally consistent point-in-time image
- **statement**: A single backup captures the durable user data as of one point in time, consistent within itself: restoring it yields a state in which the model's invariants hold, not a smear of rows captured at different moments with references that no longer resolve. A backup taken while the product is serving does not record a Chirp without its author or a count out of step with its edges.
- **acceptance_criteria**: Take a backup of a populated deployment while writes are occurring; restore it to a separate store and traverse Chirps, Replies, Follows, and Likes — every reference resolves, ids are unchanged and unreused, and counts equal their edges, with no partially captured write visible. A backup that restores to a state violating an invariant is treated as an unusable backup, not accepted.
- **verification_method**: operational_check
- **release_gating**: true
- **traces_to**: REQ-DOM-116, REQ-DOM-110

#### REQ-OPS-023 — Backups are stored independently of the primary durable store
- **statement**: Backups are held in a location whose loss is independent of the primary durable store, so that the failure a backup protects against — losing the store — does not also take the backups. A backup kept only alongside the data it backs up does not meet this posture.
- **acceptance_criteria**: Inspect where backups are stored relative to the primary durable store; the two do not share a single point of failure such that losing the primary store also loses its backups. Confirm that, with the primary store made unavailable, a retained backup is still reachable to restore from.
- **verification_method**: inspection
- **release_gating**: true
- **traces_to**: REQ-PROD-038

### Recovery objectives

#### REQ-OPS-024 — A stated recovery-point objective (tolerable data loss)
- **statement**: The product states a recovery-point objective: the maximum amount of recent durable data, measured as a time window of work, that a recovery is permitted to lose in a disaster. The objective is set no tighter than the backup cadence (`REQ-OPS-020`) can actually achieve, so it is a target a recovery can meet rather than an aspiration.
- **acceptance_criteria**: Find the product's stated recovery-point objective and confirm it is consistent with the backup cadence (a recovery-point objective of N cannot be met by a cadence coarser than N). The stated objective names a bounded quantity of tolerable data loss, not "none" without a mechanism that would achieve none.
- **verification_method**: inspection
- **release_gating**: true
- **traces_to**: REQ-PROD-038

#### REQ-OPS-025 — A stated recovery-time objective (tolerable downtime)
- **statement**: The product states a recovery-time objective: the maximum time the product may be unavailable to users while an operator recovers it from backup after a disaster. The objective is a commitment the restore procedure is built and rehearsed to meet, bounding the downtime a person experiences in a recovery.
- **acceptance_criteria**: Find the product's stated recovery-time objective. It names a bounded recovery duration and is consistent with the availability the product commits to (`REQ-PROD-040`). The objective is the one the restore drill (`REQ-OPS-031`) measures the restore against.
- **verification_method**: inspection
- **release_gating**: true
- **traces_to**: REQ-PROD-038, REQ-PROD-040

### Restore procedure

#### REQ-OPS-026 — A restore is a defined, operator-performable procedure
- **statement**: Recovering the product from a backup is a defined procedure an operator can follow, not an improvisation invented during an incident: the steps to restore the durable store from a retained backup and return the product to service are written down and performable by an operator who did not design the system. The scripting and tooling are the code work's; that a defined, followable procedure exists is the bar's.
- **acceptance_criteria**: Locate the product's stated restore procedure. An operator who did not build the system can follow it to restore a deployment from a retained backup and return it to service, without needing knowledge that is not in the procedure. The procedure names what is restored (Accounts, Chirps, Follows, Likes) and how the product is returned to serving.
- **verification_method**: inspection
- **release_gating**: true
- **traces_to**: REQ-PROD-038, REQ-DOM-116

#### REQ-OPS-027 — A restore brings back accounts, chirps, follows, and likes intact and consistent
- **statement**: A restore from a retained backup returns the durable user data intact and consistent: the Accounts, Chirps, Follows, and Likes present at the backup's point in time are all present afterward, and they satisfy the same invariants a restart must satisfy (`REQ-OPS-007`) — references resolve, ids are unchanged and never reused, counts equal their edges, and any account deleted before the backup stays deleted with no dangling reference. A restore that brings rows back but breaks these invariants has not recovered a correct product.
- **acceptance_criteria**: On a store restored from a backup of a populated deployment, every Account, Chirp, Follow, and Like present at the backup point is present; traverse Chirps, Replies, Follows, and Likes — every reference resolves, recorded ids are unchanged and unreused, counts equal their edges, and an account deleted before the backup is still deleted with no dangling reference. A failing invariant is reported as an unsuccessful restore, never silently accepted.
- **verification_method**: operational_check
- **release_gating**: true
- **traces_to**: REQ-DOM-116, REQ-DOM-110, REQ-DOM-111, REQ-DOM-107

#### REQ-OPS-028 — An exercised restore meets the stated recovery-point and recovery-time objectives
- **statement**: When the restore procedure is exercised, it recovers the product within the stated recovery-time objective (`REQ-OPS-025`) and loses no more than the stated recovery-point objective (`REQ-OPS-024`): the downtime and data loss a real recovery incurs are within the commitments the product has made, not merely asserted by them.
- **acceptance_criteria**: Perform a timed restore from a backup on a representative deployment: measure the elapsed time from starting the restore to the product serving users again — it is within the stated recovery-time objective — and measure the data lost relative to the disaster point — it is within the stated recovery-point objective. A drill that exceeds either objective is a defect in the objective or the procedure, reported rather than ignored.
- **verification_method**: operational_check
- **release_gating**: true
- **traces_to**: REQ-PROD-038

### Recovery from a bad deploy

#### REQ-OPS-029 — A failed deploy can be rolled back to the last working version with no user-data loss
- **statement**: A deploy that fails or ships a broken product can be rolled back to the last working version as a routine operation, and the rollback loses no user data: the Accounts, Chirps, Follows, and Likes present before the deploy are all present after the rollback. Rolling back is a recovery operation an operator can perform, not a reason to lose data.
- **acceptance_criteria**: On a populated deployment, perform a deploy and then roll it back to the prior version as an operator would; afterward the product serves on the prior version and every Account, Chirp, Follow, and Like that existed before the deploy is present and unchanged. The rollback requires no manual reconstruction of user data.
- **verification_method**: operational_check
- **release_gating**: true
- **traces_to**: REQ-PROD-037, REQ-DOM-118

#### REQ-OPS-030 — A data-damaging deploy can be recovered from by restore
- **statement**: A deploy that damages durable data — corrupting it or losing part of it despite the preserve-existing-data requirement (`REQ-DOM-118`) — can be recovered from by restoring from a backup taken before the deploy, returning the product to a correct state consistent with `REQ-OPS-027`. The preserve-data property is the first line; a restore path for when it is breached is the second.
- **acceptance_criteria**: Simulate a deploy that damages or loses durable data on a populated deployment; recover by restoring from a pre-deploy backup following the restore procedure (`REQ-OPS-026`); afterward the durable data is intact and consistent per `REQ-OPS-027`, recovered to the pre-deploy point within the stated objectives (`REQ-OPS-028`). The product does not depend on the damaging deploy being reversible in place.
- **verification_method**: operational_check
- **release_gating**: true
- **traces_to**: REQ-DOM-118, REQ-DOM-116

### Backup verifiability

#### REQ-OPS-031 — Backups are periodically proven restorable
- **statement**: Backups are proven restorable on a recurring basis, not merely produced: a restore from a recent backup is exercised periodically against a store where its correctness can be checked, and the exercise verifies the restored data satisfies its invariants (`REQ-OPS-027`) and meets the stated objectives (`REQ-OPS-028`). A backup that has never been restored is not yet known to be a backup.
- **acceptance_criteria**: Find the product's stated restore-drill cadence and the record of its most recent drills. Confirm a restore from a recent backup has been exercised within that cadence, that the drill checked the restored data's invariants and timing, and that a failed drill is recorded and acted on rather than passed over. The drill is recurring, not a one-time pre-release event.
- **verification_method**: operational_check
- **release_gating**: true
- **traces_to**: REQ-PROD-038, REQ-DOM-116

#### REQ-OPS-032 — A failed or missing backup is surfaced, not silent
- **statement**: When a scheduled backup fails or does not run, that fact is surfaced to operators rather than passing silently, so a deployment cannot drift into having no recent usable backup without anyone knowing. This section requires that the failure is detectable and raised; the alerting signal that carries it to an operator is the observability section's (`REQ-OPS-060..079`), building on the same posture.
- **acceptance_criteria**: Induce a backup failure or a missed scheduled backup on an operated deployment; the condition is surfaced to operators (a visible failure state or alert), not absorbed silently. Confirm that a run of successful backups and a failed backup are distinguishable to an operator. The signal's shape is verified against the observability requirements.
- **verification_method**: operational_check
- **release_gating**: true
- **traces_to**: REQ-PROD-038

#### REQ-OPS-033 — The backup and recovery posture is stated where an operator can find it
- **statement**: The product states, in a place an operator can find, its backup cadence and retention (`REQ-OPS-020`, `REQ-OPS-021`), its recovery-point and recovery-time objectives (`REQ-OPS-024`, `REQ-OPS-025`), and the restore and rollback procedures (`REQ-OPS-026`, `REQ-OPS-029`). A releasable product that can be operated does not leave its recovery procedure to be reconstructed under incident pressure.
- **acceptance_criteria**: Locate the product's stated backup-and-recovery posture as an operator could. It names the cadence, the retention period, the recovery-point and recovery-time objectives, and the restore and rollback procedures, and these statements match the behaviour verified by `REQ-OPS-020..032`. A discrepancy between the stated posture and the observed behaviour is a defect.
- **verification_method**: inspection
- **release_gating**: true
- **traces_to**: REQ-PROD-038

## Methodology note (environment)

The Phase-B `design` methodology loader is unavailable in this environment (the methodology surface returns
`agent_domain_unset`). This section was produced by applying the product-designer persona's release-readiness
judgment and the guidance relayed in the brief and subtree hub — the design bundle IDs its concern maps to
(Release Readiness primary; Release Definition supporting) — against the durable-data posture
(`REQ-OPS-001..019`), the domain backup/recovery capability (`REQ-DOM-116`, with invariants
`REQ-DOM-110/111/107` and upgrade-preserves-data `REQ-DOM-118`), and the product requirement and operator
journey it serves (`REQ-PROD-038`, operator journey J9). The loader unavailability is recorded here rather
than treated as a blocker.
