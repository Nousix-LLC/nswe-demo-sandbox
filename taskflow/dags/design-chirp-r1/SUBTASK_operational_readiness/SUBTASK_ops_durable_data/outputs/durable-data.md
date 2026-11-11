# Durable data in production

This is the `durable_data` section of `design/operational-readiness.md`: the **operational posture**
around chirp's persistence model, stated as testable `REQ-OPS-*` requirements. The domain design already
fixed the persistence *model* — authoritative state in a durable store distinct from the serving process,
acknowledged writes survive, invariants hold across restart/redeploy/restore, readiness reflects store
reachability, upgrades preserve data (`REQ-DOM-100..118`). This section does not restate that model. It
states what an **operator and a user are owed in production** once that model is in place: that the
product's authoritative state lives durably as a standing property of an operated deployment, survives the
normal operations of running a service, and is **retained for as long as the product promises and no
longer**. The backups-and-recovery section (`REQ-OPS-020..039`) builds its backup, restore, and
recovery-target requirements on the durability posture fixed here; the readiness *signal* itself is the
observability section's (`REQ-OPS-060..079`) — this section states only that durability requires the store
to be run as a reachable, persistent component.

## What this section fixes, and what it defers

- **In this section**: the production durability expectation (a running deployment loses no user data to a
  restart, update, or redeploy); acknowledged-write durability as an operated property; the integrity
  properties that must still hold after an operational restart and after a restore; the requirement that the
  durable store be operated as a reachable, persistent component distinct from the serving process; and a
  stated **data-retention posture** — how long live user data, deleted-account data, sessions, and private
  identity data are kept, consistent with the defined deletion outcome (`REQ-DOM-037`, `REQ-DOM-112`) and
  with export (`REQ-DOM-117`).
- **Referenced, owned elsewhere**: the persistence *model* and its invariants (`REQ-DOM-100..118`, domain
  design) — consumed here by reference, not restated; the backup cadence, retention schedule,
  recovery-point / recovery-time targets, and the restore procedure (`REQ-OPS-020..039`,
  backups-and-recovery), which build on this section; the readiness *signal*, the health-vs-readiness
  distinction, and the audit trail (`REQ-OPS-060..079`, observability); the structure and handling of the
  account **Credential** and **Verified contact** (`REQ-ID-*`, identity/security); and the user-facing
  export surface and portable format (`REQ-UX-*` / `REQ-ID-*`).
- **Deferred to the code work (the "how")**: which store engine, replication or snapshot mechanism, schema,
  migrations, connection handling, and serialization. Every requirement below is a property the operated
  product must have, not a mechanism; where a mechanism is tempting it is stated as the property and the
  choice handed to the engineering code DAGs.

Entities are named by the domain model's canonical vocabulary (Account, Chirp, Follow, Like, Session,
Credential, Verified contact); this section introduces none the model does not define. The product and the
in-memory backing it closes are named by repository identity — `Nousix-LLC/nswe-demo @ c805525`, the
`ChirpRepository` seam in the `chirp-server` crate — never by any host, cluster, or deployment address.

## The posture in prose

**Durability is a standing property of an operated deployment, not a one-time property of a fresh start.**
The domain design requires that authoritative state survives a restart (`REQ-DOM-100`). The operational
requirement is stronger in a different direction: a deployment that an operator runs — restarting it,
updating it, redeploying it, rolling the serving process to a fresh instance — loses no user data in the
course of those routine operations, every time, for the life of the deployment. The operator does not have
to treat a restart as a risky event; it is a normal one. This is the operational face of `REQ-DOM-113/114`
(authoritative state in a durable store distinct from the serving process) and `REQ-DOM-118` (an upgrade
preserves existing data).

**The store is a component the deployment runs, not a convenience of the process.** For durability to be a
standing property, the durable store named by `REQ-DOM-113` must be operated as a persistent component
whose lifecycle is independent of any single serving process. An operator can replace the serving process
without touching the store, and the store outlives the process. A deployment that keeps authoritative state
only in the serving process's memory — the `c805525` blocker — does not meet this posture no matter how
rarely it restarts.

**Integrity survives the events of operating the product.** Recovery that brings the rows back but breaks
the model's invariants has not recovered the product (`REQ-DOM-110`). The operational posture is that after
an operational restart *and* after a restore from backup, every reference still resolves, ids are still
unique and never reused, counts still equal their edges, and an applied account deletion stays applied —
and that an interrupted write (a crash or restart mid-operation) never leaves half-applied state visible.
The backups-and-recovery section inherits this: a restore is "correct" only when these properties hold, and
that is the bar its restore-verification requirements are written against.

**Retention is a promise with a stated length, in both directions.** A releasable product owes its users a
plain answer to two questions: *how long do you keep my data?* and *when I delete my account, when is my
data actually gone?* The posture here is that live user data is retained for as long as the account exists —
no silent expiry, no background deletion of a live account's content — and that deleted-account data is
removed or de-identified per the stated deletion outcome (`REQ-DOM-037`, `REQ-DOM-112`) within a stated,
bounded window rather than lingering indefinitely, including in backups. Retention and export name the same
set: while an account exists, the data the product keeps for it is the data it can hand back (`REQ-DOM-117`).
The product states this posture where a user and an operator can find it.

The formal requirements are **REQ-OPS-001..016** in the register below.

## Requirements and acceptance criteria (`REQ-OPS-001..019`)

Each requirement carries an `id` (within this section's assigned range `REQ-OPS-001..019`), a `statement`
(what must be true in production, from the operator's or user's side), testable `acceptance_criteria`, a
`verification_method` from the contract vocabulary (`manual_user_check`, `automated_test`, `inspection`,
`operational_check`), a `release_gating` flag, and `traces_to` the product/domain requirement it builds on.
The range is generous; it is not filled, and the gaps are deliberate.

### Production durability as an operated property

#### REQ-OPS-001 — A running deployment loses no user data to restart, update, or redeploy
- **statement**: An operated chirp deployment does not lose any user data — Accounts, Chirps, Follows, Likes, Sessions — to the normal operations of running the service: restarting the serving process, updating it, and redeploying it are routine operations after which all user data is present and unchanged. This is the operational standing of the domain model's survival requirement, held as a property of the operated service rather than of a single fresh start.
- **acceptance_criteria**: On an operated deployment, create Accounts and post Chirps, Follows, and Likes; perform each of a process restart, a redeploy, and an update as an operator would; after each, every Account and its Chirps, Follows, and Likes are present and unchanged, with no manual intervention to recover them.
- **verification_method**: operational_check
- **release_gating**: true
- **traces_to**: REQ-PROD-037, REQ-DOM-100

#### REQ-OPS-002 — Authoritative state is operated in a durable store distinct from the serving process
- **statement**: The deployment runs the product's authoritative state in a durable store that is a separate, persistent component from the serving process, with its own lifecycle; the serving process holds no authoritative state that exists only in its memory. The in-memory backing of the `ChirpRepository` seam at `Nousix-LLC/nswe-demo @ c805525` does not meet this and is the blocker this posture closes.
- **acceptance_criteria**: Inspect the deployment: the durable store is a component whose lifecycle is independent of the serving process (stopping or replacing the serving process does not stop or reset the store). Confirm `REQ-DOM-113/114` hold against the operated product. No deployment configuration keeps authoritative state solely in serving-process memory.
- **verification_method**: operational_check
- **release_gating**: true
- **traces_to**: REQ-PROD-037, REQ-DOM-113, REQ-DOM-114

#### REQ-OPS-003 — Replacing the serving process is a routine operation that touches no user data
- **statement**: An operator can replace or roll the serving process to a fresh instance, with no shared process memory, as a normal operation; all user data remains intact because it lives in the durable store, not the process.
- **acceptance_criteria**: On a populated deployment, replace the serving process with a fresh instance without touching the durable store; afterward all Accounts, Chirps, Follows, Likes, and active Sessions are intact, demonstrating the authoritative state did not live in the replaced process.
- **verification_method**: operational_check
- **release_gating**: true
- **traces_to**: REQ-PROD-037, REQ-DOM-113

#### REQ-OPS-004 — An operated upgrade preserves existing user data
- **statement**: Performing an upgrade in production — including a redeploy that changes how the data is shaped — preserves the user data that existed before it: afterward the prior Accounts, Chirps, Follows, and Likes are all present and still satisfy their invariants. The migration mechanics are the code work's; the preservation property across an operated upgrade is the bar's.
- **acceptance_criteria**: On a populated deployment, perform an upgrade that changes the data's shape; afterward the Accounts, Chirps, Follows, and Likes created before the upgrade are all present and their references still resolve. No data created before the upgrade is lost or corrupted by it.
- **verification_method**: operational_check
- **release_gating**: true
- **traces_to**: REQ-PROD-037, REQ-DOM-118

### Acknowledged-write durability as an operated property

#### REQ-OPS-005 — An acknowledged write survives an immediate restart in production
- **statement**: In the operated product, any create or change the product has confirmed to a person — a posted Chirp, a Follow or unfollow, a Like or unlike, a profile edit, an account deletion — is durable at the moment it is acknowledged, so a restart or process replacement happening immediately after the success response does not lose it. Durability is a correctness property of the acknowledgement, not a tendency observed over time.
- **acceptance_criteria**: On an operated deployment, perform a write and receive the product's success response; with no further action, restart or replace the serving process; the written state is present afterward. Repeated across each write type, no acknowledged write is lost by a restart in the window immediately following its acknowledgement.
- **verification_method**: operational_check
- **release_gating**: true
- **traces_to**: REQ-PROD-037, REQ-DOM-109

### Integrity across operational events

#### REQ-OPS-006 — Domain invariants hold after an operational restart
- **statement**: After the serving process is restarted or replaced in production, the domain model's invariants still hold against the durable data: every reference resolves, ids are unique and never reused, each Account's follower/following counts and each Chirp's like count equal their current edges, and any applied account deletion stays applied. A restart never introduces a dangling reference, a reused id, or a count that disagrees with its edges.
- **acceptance_criteria**: On a populated deployment, record a sample of references, ids, and counts; restart the serving process; traverse Chirps, Replies, Follows, and Likes — every referenced Account and Chirp resolves, no recorded id has moved or been reused, and the counts equal the current edges (add and remove a Follow and a Like after the restart and confirm the counts track by exactly one each way).
- **verification_method**: operational_check
- **release_gating**: true
- **traces_to**: REQ-DOM-107, REQ-DOM-110, REQ-DOM-111, REQ-DOM-112

#### REQ-OPS-007 — Domain invariants hold after a restore from backup (the posture backups build on)
- **statement**: After a restore from backup, the durable data satisfies the same invariants required after a restart (`REQ-OPS-006`): references resolve, ids are unchanged and never reused, counts equal their edges, and applied deletions remain applied. A restore that brings rows back but breaks these invariants has not recovered a correct product. This is the durability posture the backups-and-recovery section's restore-correctness requirements (`REQ-OPS-020..039`) are written against.
- **acceptance_criteria**: On a store restored from a backup of a populated deployment, traverse Chirps, Replies, Follows, and Likes — every reference resolves, recorded ids are unchanged and unreused, counts equal their edges, and any account deleted before the backup is still deleted with no dangling reference. A failing invariant is reported as an unsuccessful restore, never silently accepted.
- **verification_method**: operational_check
- **release_gating**: true
- **traces_to**: REQ-DOM-110, REQ-DOM-116

#### REQ-OPS-008 — An interrupted write never leaves half-applied state visible
- **statement**: A restart, crash, or process replacement that happens while a write is in progress leaves the durable data in a consistent state: the operation is observable afterward as either fully applied or not applied, never as a half-applied change with a dangling reference or a count that disagrees with its edges. Account deletion in particular is all-or-nothing across an interruption.
- **acceptance_criteria**: Interrupt the serving process during representative writes (posting a Chirp, following, deleting an account that has Chirps, Follows, and Likes); after recovery, each interrupted operation is observably either fully applied or fully absent, and no partially applied state (a Chirp without a resolvable author, a half-deleted Account with dangling references, a count out of step with its edges) is observable.
- **verification_method**: operational_check
- **release_gating**: true
- **traces_to**: REQ-DOM-110, REQ-DOM-112

### The durable store's reachability as a durability property

#### REQ-OPS-009 — Durability requires the store to be operated as a reachable, persistent component
- **statement**: Because the serving process depends on the durable store to serve, durability in production requires the store to be run as a reachable, persistent component for the life of the deployment: a serving process that cannot reach its durable state cannot serve, and a deployment that does not keep its store reachable and persistent does not meet the durability posture. This section states the dependency as a durability requirement; the readiness *signal* that reports store reachability is the observability section's (`REQ-OPS-060..079`), building on `REQ-DOM-115` / `REQ-PROD-039`.
- **acceptance_criteria**: Confirm the deployment runs the durable store as a persistent, reachable component independent of the serving process. With the store made unreachable to the serving process, the product does not serve user writes or reads from process memory as if durable (it does not silently fall back to a non-durable store). The readiness signal's behaviour under this condition is verified by the observability section.
- **verification_method**: operational_check
- **release_gating**: true
- **traces_to**: REQ-PROD-039, REQ-DOM-115

### Data-retention posture

#### REQ-OPS-010 — Live user data is retained for the life of the account
- **statement**: While an account exists, its user data — the Account and its profile, its Chirps, its Follows, and its Likes — is retained in full: the product does not silently expire, age out, or delete a live account's content as a side effect of operating the service. Any retention limit the product chooses to place on a live account's content is stated, not silent.
- **acceptance_criteria**: Create an account with Chirps, Follows, and Likes; over a sustained operating period with ordinary restarts and redeploys, the account's content remains present and complete without the holder re-creating it. If any component of a live account's data is subject to an age-out, that limit is found stated in the product's retention posture (`REQ-OPS-016`) rather than observed as an unexplained loss.
- **verification_method**: manual_user_check
- **release_gating**: true
- **traces_to**: REQ-PROD-037

#### REQ-OPS-011 — Deleted-account data is removed within a stated, bounded window
- **statement**: When an account is deleted, its data is removed or de-identified per the stated deletion outcome (`REQ-DOM-037`, `REQ-DOM-112`) within a stated, bounded retention window after the deletion is applied, rather than being retained indefinitely. The product states the window; after it elapses, the deleted account's data is not retained in the live durable store.
- **acceptance_criteria**: Find the product's stated deleted-account retention window. Delete an account that has Chirps, Follows, and Likes; after the deletion is applied the stated outcome holds immediately (the account cannot sign in, no dangling reference remains per `REQ-DOM-112`), and after the stated window the deleted account's data is no longer present in the live durable store. The behaviour matches the stated window.
- **verification_method**: operational_check
- **release_gating**: true
- **traces_to**: REQ-DOM-037, REQ-DOM-112

#### REQ-OPS-012 — Backups do not retain deleted-account data beyond a stated bound
- **statement**: Deleted-account data does not persist indefinitely in backups: a stated maximum backup-retention bound limits how long a deleted account's data can remain recoverable in backups, after which the backups holding it have aged out. This section fixes that such a bound exists and is consistent with the deletion posture; the backup cadence, retention schedule, and ageing mechanics are the backups-and-recovery section's (`REQ-OPS-020..039`), which builds on this.
- **acceptance_criteria**: Find the product's stated maximum backup-retention bound and confirm it is consistent with the deleted-account retention posture (`REQ-OPS-011`). Confirm that no backup older than that bound is retained, so deleted-account data cannot be recovered from backups indefinitely. The concrete cadence and schedule are verified against the backups-and-recovery requirements.
- **verification_method**: inspection
- **release_gating**: true
- **traces_to**: REQ-DOM-037, REQ-PROD-038

#### REQ-OPS-013 — Retention and export cover the same per-account set
- **statement**: The data the product retains for a live account is the data it can hand that person back: while an account exists, its retained profile, full set of Chirps, and full set of followed Accounts are enumerable for the holder's own export (`REQ-DOM-117`). A person cannot be told their data is kept while being unable to obtain it, and export reflects the committed durable state at the time of the request.
- **acceptance_criteria**: For a signed-in account with Chirps and Follows, the data the product retains (per `REQ-OPS-010`) and the data a self-service export yields (per `REQ-DOM-117`) are the same set — the account's profile, its complete Chirps, and its complete followed Accounts — matching the committed durable state. No retained category of a person's own data is absent from what they can export.
- **verification_method**: manual_user_check
- **release_gating**: true
- **traces_to**: REQ-DOM-117, REQ-PROD-019

#### REQ-OPS-014 — Sessions are retained only for their bounded lifetime
- **statement**: Active Sessions are retained durably so a signed-in person is not silently signed out by a restart or redeploy (`REQ-DOM-106`), but only until the Session ends (sign-out) or passes its lifetime (`REQ-DOM-030`, `REQ-DOM-031`); an ended or expired Session is not retained as usable and is never revived by a restart or a restore.
- **acceptance_criteria**: Sign in to obtain a Session; restart or redeploy the service — a request carrying that Session's token is still accepted as the same account. Separately, end a Session (or let it pass its lifetime), then restart and restore from a backup taken while it was active — a request carrying that token is refused in both cases, not revived.
- **verification_method**: operational_check
- **release_gating**: true
- **traces_to**: REQ-DOM-106, REQ-DOM-030, REQ-DOM-031

#### REQ-OPS-015 — Private identity data is retained durably, kept non-public, and removed with the account
- **statement**: The account-associated Credential and Verified contact are retained durably as part of the Account for the life of the account so a person can still sign in and still recover after a restart (`REQ-DOM-102`), are never exposed in any public response, and are removed or de-identified with the account under the stated deletion outcome and within the deleted-account retention window (`REQ-OPS-011`). Their structure and handling are the identity/security design's (`REQ-ID-*`); this requirement is that they persist, stay non-public, and are not retained past the account.
- **acceptance_criteria**: After a restart and a restore, a person can still sign in with their Credential and the recovery path still recognises their Verified contact, and neither value ever appears in any public response. After an account is deleted and the retention window elapses, the deleted account's Credential and Verified contact are no longer retained in the live durable store.
- **verification_method**: operational_check
- **release_gating**: true
- **traces_to**: REQ-DOM-102, REQ-DOM-037

#### REQ-OPS-016 — The retention and deletion posture is stated where users and operators can find it
- **statement**: The product states, in a place a user and an operator can find, what user data it keeps, for how long, and what account deletion removes and when — covering live-account retention (`REQ-OPS-010`), the deleted-account window (`REQ-OPS-011`), the backup bound (`REQ-OPS-012`), and session and private-identity-data handling (`REQ-OPS-014`, `REQ-OPS-015`). A releasable product does not leave its retention and deletion promise implicit.
- **acceptance_criteria**: Locate the product's stated data-retention and deletion posture as a user/operator could. It names what is retained, the live-account retention, the deleted-account retention window, the backup-retention bound, and session/private-data handling, and these statements match the behaviour verified by `REQ-OPS-010..015`. A discrepancy between the stated posture and the observed behaviour is a defect.
- **verification_method**: inspection
- **release_gating**: true
- **traces_to**: REQ-PROD-037, REQ-DOM-037

## Methodology note (environment)

The Phase-B `design` methodology loader is unavailable in this environment (the methodology surface returns
`agent_domain_unset`). This section was produced by applying the product-designer persona's release-readiness
judgment and the guidance relayed in the brief and subtree hub — the design bundle IDs its concern maps to
(Release Readiness primary; Release Definition, Product Strategy supporting) — against the domain persistence
model (`REQ-DOM-100..118`) and the product requirements (`REQ-PROD-037..041`, operator journey J9). The
loader unavailability is recorded here rather than treated as a blocker.
