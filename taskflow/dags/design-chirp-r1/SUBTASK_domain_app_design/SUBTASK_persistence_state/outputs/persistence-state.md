<!--
This file is the `persistence_requirement` section of design/domain-application-design.md.
SUBTASK_dad_synthesis assembles it, with the sibling parts, into the consolidated design file and folds
every REQ-DOM-* below into that file's requirements_and_acceptance_criteria register.
Owns: the `persistence_requirement` section and REQ-DOM-100..149.
References entities only by the canonical vocabulary in domain-model.md. Held to the current
chirp-server ChirpRepository seam and its in-memory backing at Nousix-LLC/nswe-demo @ c805525.
-->

# Persistence requirement

## What this section fixes

This section states the **durable-persistence requirement** for chirp: what of the product's state must
survive the serving process going away and coming back, where that state has to live for the survival to
hold, and the backup, recovery, and data-integrity posture a release depends on. It states all of this as
requirements the release bar can be checked against — what must be true from the operator's and the user's
side — and it leaves the engineering *how* to the `software` domain's later code work.

It says nothing about which database, which schema, which migration tool, or how connections are pooled.
Those are real decisions, but they are decisions about *how* to meet a requirement, not the requirement
itself. Wherever one is tempting below, it is written as the property the product must have and the choice is
handed, by prose, to the `software` domain. The one place the current implementation is named is the place it
is the problem: chirp at `c805525` keeps its state in process memory behind the `ChirpRepository` seam in the
`chirp-server` crate, so a restart, update, or redeploy empties the product. The product requirements call
this out as a release **blocker**, not a baseline (`product-requirements.md`, REQ-PROD-037), and every
requirement here exists to close it.

The vocabulary is the domain model's. "Account," "Chirp," "Follow," "Like," "Session," "Timeline,"
"Credential," and "Verified contact" are used below exactly as `domain-model.md` defines them
(`REQ-DOM-001..049`); this section introduces no entity the model does not name. Where persistence has a
consequence the model already fixed — referential integrity (`REQ-DOM-036`), ids never reused
(`REQ-DOM-007`), counts that match their edges (`REQ-DOM-021`, `REQ-DOM-024`), a defined deletion outcome
(`REQ-DOM-037`) — the requirement here is that the fixed property keeps holding across a restart and a
restore, not a restatement of the property.

### Scope of this section

- **In this section**: the concrete set of state that must survive a restart and redeploy; the requirement
  that the product's authoritative state lives in a durable store distinct from the serving process; the
  durability property that an acknowledged write is not lost; the integrity properties that must hold after a
  restart and after a restore; and the requirement that the durable data can be backed up and recovered and
  is enumerable for a person's own export.
- **Referenced, owned elsewhere**: the operational *mechanics* of durability — backup cadence and retention,
  the restore runbook, a recovery-point / recovery-time target, and the availability target — are the
  operational-readiness design's (`REQ-OPS-*`); this section states the capability the bar needs and hands
  the operational targets to that design, which consumes this section as its `durable_data` input. The
  structure and handling of the account **Credential** and **Verified contact** are the identity/security
  design's (`REQ-ID-*`); this section requires only that they persist durably and stay non-public. The
  **how** — database engine, schema, migrations, connection handling, serialization — is the `software`
  domain's.
- **Not required to be durable** (recorded so the absence is a decision): the **Timeline**. The domain model
  fixes the timeline as a *derived* view, not stored state (`REQ-DOM-025`, `REQ-DOM-028`); it therefore does
  not need to survive a restart as stored data. What must survive is the data it is derived from — the
  viewer's chirps and the follow graph — so that the same timeline is reconstructable after a restart
  (`REQ-DOM-108`). Durably materializing a timeline is neither required nor prohibited here; it is a `how`
  left to the `software` domain, constrained only by the derived-view invariants the model already fixed.

---

## The requirement in prose

**What must survive.** A person who creates an account, posts, follows, and likes must find all of it still
there the next time they visit, and an operator must be able to restart, update, and redeploy the service as
normal operations without losing any of it. Concretely, the state that MUST survive a restart and a redeploy
is: every **Account** (its profile fields, its server-assigned **Account id**, its creation **Timestamp**,
and its follower/following counts); the account-associated **Credential** and **Verified contact** that the
identity area owns but that live on the account record; every **Chirp** (its body, its author, its creation
time, its reply linkage, and its like count); the entire **Follow** graph; every **Like**; and every active
**Session**. This set is named by `REQ-PROD-037`, which lists accounts, chirps, follows, likes, and sessions
explicitly; the account's private identity data is added here because the model places it on the account
(`REQ-DOM-033`, `REQ-DOM-034`).

**Durability is a correctness property, not only a presence one.** It is not enough that data *tends* to be
there after a restart. A write the product has acknowledged to a person — a posted chirp, a new follow, a
like, a profile edit — must not be lost by a restart that happens immediately afterward; once the product
tells someone "done," that fact is durable (`REQ-DOM-109`). And the invariants the domain model fixes must
still hold after the process comes back and after a restore from backup: every reference still resolves
(`REQ-DOM-110`), ids are still unique and still never reused (`REQ-DOM-111`), the counts still equal their
edges (`REQ-DOM-107`), and an applied account deletion stays applied (`REQ-DOM-112`). Recovery that brings the
rows back but breaks these invariants has not recovered the product.

**Where state lives.** For any of the above to hold, the product's authoritative state cannot live in the
serving process. The requirement is that it lives in a **durable store distinct from the serving process**,
so that replacing, restarting, or redeploying the process does not touch the data (`REQ-DOM-113`). The
`ChirpRepository` seam in `chirp-server` is the right place for this to resolve: today that seam is backed by
an in-memory store, which is exactly the blocker; the requirement is that the seam (or its equivalent) be
backed by the durable store instead (`REQ-DOM-114`). Which store, and how it is reached, is the `software`
domain's to decide. Because serving now depends on that store, the product's readiness signal must reflect
whether the store is reachable — a process that cannot reach its durable state is not ready to serve, even
though it is running (`REQ-DOM-115`), which is the persistence-side half of the readiness requirement the
operational-readiness design owns (`REQ-PROD-039`).

**Backup, recovery, and a person's own copy.** Once data is durable there is something to protect, and the
product must be able to protect it: the durable data can be backed up and restored, and a restore brings the
accounts, chirps, follows, and likes back intact and consistent (`REQ-DOM-116`). The operational shape of
this — how often a backup is taken, how long it is kept, how much data loss is tolerable, and the restore
procedure — is the operational-readiness design's (`REQ-OPS-*`), which consumes this requirement; this
section fixes only that the capability exists and recovers a correct product. Separately, a person must be
able to obtain their own data, so the durable store must be enumerable per account — a person's profile,
their full set of chirps, and the accounts they follow can all be read out for export (`REQ-DOM-117`),
feeding the export surface the experience and identity designs own.

**Change over time.** Redeploys are named alongside restarts in the product requirement, and a redeploy may
carry a change to how data is shaped. The requirement is that evolving the product does not lose or corrupt
existing durable data: after an upgrade that changes the data's shape, the accounts, chirps, follows, and
likes that existed before are still present and still satisfy their invariants (`REQ-DOM-118`). The mechanics
of schema and data migration are the `software` domain's; the property that an upgrade preserves existing
data is the bar's.

---

## Requirements and acceptance criteria (`REQ-DOM-100..149`)

Each requirement carries an `id`, a `statement` (what must be true), `acceptance_criteria` a person who never
met the author can check, a `release_gating` flag (`true` when a releasable product depends on it), and
`traces_to` the product requirement it refines where one applies. Durability criteria prefer an
**operational_check** — observe the property on the running product across a real restart, redeploy, or
restore — because that is the only check that actually proves durability; a few criteria that fix a boundary
or name the current blocker are checkable by **inspection** of the repository at `c805525`.

### What must survive a restart

#### REQ-DOM-100 — The product's user state survives restart, update, and redeploy
- **statement**: The product's user-visible state — every Account, Chirp, Follow, Like, and active Session — survives the serving process being restarted, updated, and redeployed; a person's account and content are still present and unchanged on their next visit, for any deployment of chirp.
- **acceptance_criteria**: On a running deployment, create an Account, post Chirps, follow accounts, and like Chirps; restart (and separately, redeploy) the serving process; sign in again — the Account exists and its Chirps, Follows, and Likes are all present and unchanged. Observed as an operational_check across a real process restart and a real redeploy.
- **release_gating**: true — the in-memory store at `c805525` loses everything on restart; this is the release blocker, not a style choice.
- **traces_to**: REQ-PROD-037

#### REQ-DOM-101 — Accounts persist in full
- **statement**: An Account survives a restart carrying all of its state: its opaque Account id, its Handle, its Display name, its Bio (absent or present, preserved as given), its creation Timestamp, and its follower/following counts.
- **acceptance_criteria**: Register an Account with a Handle, Display name, and Bio; restart the service; fetch the Account — the same Account id, Handle, Display name, Bio, and creation Timestamp are returned, and the counts are unchanged. An Account registered with no Bio still reads back with its Bio absent (not an empty string).
- **release_gating**: true
- **traces_to**: REQ-PROD-037, REQ-DOM-001

#### REQ-DOM-102 — Account private identity data persists durably and stays non-public
- **statement**: The account-associated Credential and Verified contact persist durably as part of the Account across a restart, so a person can still sign in and still recover their account after a restart; this data is never returned in any public response. Its structure and handling are the identity/security design's; this requirement is that it is durable and non-public.
- **acceptance_criteria**: Register an Account and establish its Credential and Verified contact; restart the service; the person can still sign in with their Credential, and the recovery path still recognises the Verified contact. Fetch the Account's public profile before and after the restart with another account's Session and with no Session — the Credential, Verified contact, and Session data never appear.
- **release_gating**: true
- **traces_to**: REQ-PROD-037, REQ-DOM-033, REQ-DOM-034, REQ-DOM-035

#### REQ-DOM-103 — Chirps persist in full
- **statement**: A Chirp survives a restart carrying its Chirp id, its author's Account id, its Chirp text, its creation Timestamp, its like count, and its reply target when it is a Reply.
- **acceptance_criteria**: Post a Chirp and a Reply to it; restart the service; fetch both — each returns with the same id, author, text, and creation time; the Reply still records the id of the Chirp it answers; the like counts are unchanged.
- **release_gating**: true
- **traces_to**: REQ-PROD-037, REQ-DOM-011, REQ-DOM-015

#### REQ-DOM-104 — The follow graph persists
- **statement**: Every Follow edge survives a restart with its follower and followee Account ids intact, so who follows whom is unchanged across a restart.
- **acceptance_criteria**: Have one Account follow another; restart the service; the follow relationship is still recorded in the same direction, the followee's chirps still enter the follower's Timeline, and both accounts' follower/following counts are unchanged.
- **release_gating**: true
- **traces_to**: REQ-PROD-037, REQ-DOM-017

#### REQ-DOM-105 — Likes persist
- **statement**: Every Like survives a restart with its Account id and Chirp id intact, so what each person has liked is unchanged across a restart.
- **acceptance_criteria**: Like a Chirp; restart the service; the Like is still recorded from the same Account to the same Chirp, and the Chirp's like count is unchanged.
- **release_gating**: true
- **traces_to**: REQ-PROD-037, REQ-DOM-022

#### REQ-DOM-106 — Active sessions survive a restart, and ended sessions stay ended
- **statement**: An active Session remains valid across a restart so a signed-in person is not silently signed out by a redeploy; a Session that has been ended (sign-out) or has passed its lifetime stays unusable across a restart and is never revived by one.
- **acceptance_criteria**: Sign in to obtain a Session; restart the service; a request carrying that Session's token is still accepted and still acts as the same Account. Separately, end a Session (sign out) and then restart; a request carrying the ended Session's token is refused, not revived.
- **release_gating**: true
- **traces_to**: REQ-PROD-037, REQ-DOM-029, REQ-DOM-030, REQ-DOM-031

#### REQ-DOM-107 — Server-maintained counts are correct after a restart
- **statement**: After a restart, each Account's follower and following counts still equal its current Follow edges and each Chirp's like count still equals the distinct Accounts that like it — whether the counts are stored durably or recomputed from the durable edges, the result observed by a client is consistent with the edges.
- **acceptance_criteria**: Record an Account's follower count and a Chirp's like count; restart the service; both counts read back equal to the number of current edges (add and remove a Follow and a Like after the restart and confirm the counts track the edges by exactly one each way).
- **release_gating**: true
- **traces_to**: REQ-DOM-021, REQ-DOM-024

#### REQ-DOM-108 — The timeline is reconstructable from durable data after a restart
- **statement**: Because the Timeline is a derived view and not stored state, it need not itself be durable; the data it is derived from — the viewer's Chirps and the current Follow graph — must be durable, so the same Timeline is produced after a restart as before it.
- **acceptance_criteria**: Build a Timeline for a viewer who follows several accounts; note its contents and order; restart the service; read the Timeline again with no further writes — it returns the same Chirps in the same newest-first order. No separate stored Timeline is required for this to hold.
- **release_gating**: true
- **traces_to**: REQ-PROD-002, REQ-DOM-025, REQ-DOM-028

### Durability as a correctness property

#### REQ-DOM-109 — An acknowledged write is durable before it is acknowledged
- **statement**: Any create or change the product confirms to a person — posting a Chirp, following or unfollowing, liking or unliking, editing a profile, deleting an account — is durable at the moment it is acknowledged, so a restart immediately after the acknowledgement does not lose it.
- **acceptance_criteria**: Perform a write and receive the product's success response; without any further action, restart the service; the written state is present after the restart. Observed as an operational_check: the window between acknowledgement and the next restart does not lose acknowledged writes.
- **release_gating**: true
- **traces_to**: REQ-PROD-037

#### REQ-DOM-110 — Referential integrity holds across restart and restore
- **statement**: After a restart and after a restore from backup, every reference in the model still resolves — each Chirp's author, each Reply's target, each Follow's two endpoints, and each Like's Account and Chirp name entities that exist — with no dangling reference introduced by stopping, restarting, or recovering the product.
- **acceptance_criteria**: On a populated deployment, restart (and separately, restore from a backup); then traverse chirps, replies, follows, and likes — every referenced Account and Chirp resolves, and no Chirp, Follow, or Like references an entity that is absent.
- **release_gating**: true
- **traces_to**: REQ-DOM-036

#### REQ-DOM-111 — Ids stay unique and are never reused across a restart
- **statement**: Account id and Chirp id assignment survives a restart such that ids already issued are never reassigned to a different entity after a restart; id generation does not reset to a point that would collide with existing ids.
- **acceptance_criteria**: Record several existing Account ids and Chirp ids; restart the service; create new Accounts and Chirps — the newly assigned ids collide with none of the recorded ids, and no existing entity's id has changed. Over the deployment's life, no id is ever observed on two entities.
- **release_gating**: true
- **traces_to**: REQ-DOM-006, REQ-DOM-007

#### REQ-DOM-112 — An applied account deletion is durable and leaves no half-applied state
- **statement**: Once an account deletion has been applied, its defined outcome (what becomes of the account's Chirps, Follows, and Likes, and whether the freed Handle may be re-registered) survives a restart; a restart during a deletion leaves the product in a consistent state — the deletion is either fully applied or not applied, never half-applied with dangling references.
- **acceptance_criteria**: Delete an Account that has Chirps (some replied-to and liked), Follows, and Likes; restart the service; the Account still cannot sign in, the stated deletion outcome is still reflected, and the freed-Handle policy still holds. Across restarts the product's state matches the stated outcome and never shows a partially deleted Account with dangling references.
- **release_gating**: true
- **traces_to**: REQ-PROD-020, REQ-PROD-021, REQ-DOM-037

### Where state lives

#### REQ-DOM-113 — Authoritative state lives in a durable store distinct from the serving process
- **statement**: The product's authoritative state lives in a durable store that is distinct from the serving process, so that stopping, restarting, replacing, or redeploying the serving process does not alter or lose any of the state in REQ-DOM-100. The serving process holds no authoritative state that only exists in its memory.
- **acceptance_criteria**: Replace the serving process entirely (for example, roll it to a fresh instance with no shared memory) without touching the data store; all Accounts, Chirps, Follows, Likes, and active Sessions are intact afterward — demonstrating the authoritative state did not live in the replaced process. Observed as an operational_check.
- **release_gating**: true
- **traces_to**: REQ-PROD-037

#### REQ-DOM-114 — The repository seam is backed by the durable store; the in-memory backing is the blocker this closes
- **statement**: The persistence seam the product reads and writes through — the `ChirpRepository` in the `chirp-server` crate, or its equivalent — is backed by the durable store of REQ-DOM-113 rather than by process memory. The in-memory backing at `c805525` is named as the release blocker this requirement closes. The choice of store engine, the schema, migrations, and connection handling are deferred to the `software` domain.
- **acceptance_criteria**: Inspect `crates/chirp-server` at `Nousix-LLC/nswe-demo @ c805525`; the `ChirpRepository` is backed by an in-memory store (the blocker). On the released product, the same seam is backed by a durable store, confirmed by REQ-DOM-100 holding across a restart. No requirement here names a specific engine.
- **release_gating**: true
- **traces_to**: REQ-PROD-037

#### REQ-DOM-115 — Readiness reflects durable-store availability
- **statement**: The product reports itself ready to serve only when its durable store is reachable; a serving process that is running but cannot reach its durable state reports not-ready rather than ready.
- **acceptance_criteria**: Query the readiness signal while the durable store is unavailable to the serving process; it reports not-ready. Query it while the store is reachable and the product can serve; it reports ready. (The readiness signal's shape and the liveness-vs-readiness distinction are the operational-readiness design's; this requirement is that readiness depends on store reachability.)
- **release_gating**: true
- **traces_to**: REQ-PROD-039

### Backup, recovery, and a person's own copy

#### REQ-DOM-116 — Durable data can be backed up and restored intact
- **statement**: The durable user data can be backed up and restored, and a restore brings back the Accounts, Chirps, Follows, and Likes consistent with every model invariant (REQ-DOM-110, REQ-DOM-111, REQ-DOM-107). The backup cadence, retention, recovery-point/recovery-time targets, and restore procedure are the operational-readiness design's; this requirement is that the capability exists and recovers a correct product.
- **acceptance_criteria**: On a populated deployment, produce a backup of the user data; then, on a store restored from that backup, the Accounts, Chirps, Follows, and Likes are present and the invariants hold (references resolve, ids are unchanged, counts match edges). Observed as an operational_check (backup then restore).
- **release_gating**: true
- **traces_to**: REQ-PROD-038

#### REQ-DOM-117 — Durable data is enumerable per account for export
- **statement**: The durable store is enumerable per Account so a person's own data — their profile, the full set of their Chirps, and the full set of Accounts they follow — can be read out for a self-service export, reflecting the committed durable state at the time of the request.
- **acceptance_criteria**: For a signed-in Account with Chirps and Follows, the product can produce that Account's profile, its complete set of Chirps, and its complete set of followed Accounts, matching what is in the durable store. (The export surface and portable format are the experience/identity designs'; this requirement is that the durable data is enumerable per Account.)
- **release_gating**: true
- **traces_to**: REQ-PROD-019, REQ-DOM-038

### Change over time

#### REQ-DOM-118 — Upgrading the product preserves existing durable data
- **statement**: Evolving the product — including a redeploy that changes how the data is shaped — preserves the durable data that existed before: after an upgrade, the prior Accounts, Chirps, Follows, and Likes are still present and still satisfy their invariants. The mechanics of schema and data migration are the `software` domain's; the preservation property is the bar's.
- **acceptance_criteria**: On a populated deployment, perform an upgrade that changes the data's shape (a redeploy with a data-model change); afterward the Accounts, Chirps, Follows, and Likes created before the upgrade are all present and their references still resolve. Observed as an operational_check across an upgrade.
- **release_gating**: true
- **traces_to**: REQ-PROD-037

<!--
Range note: this part owns REQ-DOM-100..149 and uses 100..118. The unused 119..149 are reserved,
not padding; a later amendment to the persistence requirement takes ids from there without disturbing
the domain-model (001..049) or module (200..249) ranges.
-->

---

## Traceability

Every `REQ-DOM-*` above that refines a product requirement or builds on a domain-model requirement cites it.
The map below is the checkable summary, folded into the consolidated traceability matrix.

| REQ-DOM | Traces to REQ-PROD | Builds on REQ-DOM | release_gating |
|---|---|---|---|
| 100 | 037 | — | true |
| 101 | 037 | 001 | true |
| 102 | 037 | 033, 034, 035 | true |
| 103 | 037 | 011, 015 | true |
| 104 | 037 | 017 | true |
| 105 | 037 | 022 | true |
| 106 | 037 | 029, 030, 031 | true |
| 107 | — | 021, 024 | true |
| 108 | 002 | 025, 028 | true |
| 109 | 037 | — | true |
| 110 | — | 036 | true |
| 111 | — | 006, 007 | true |
| 112 | 020, 021 | 037 | true |
| 113 | 037 | — | true |
| 114 | 037 | — | true |
| 115 | 039 | — | true |
| 116 | 038 | — | true |
| 117 | 019 | 038 | true |
| 118 | 037 | — | true |

**What the rest of the design consumes from this section.** The operational-readiness design (`REQ-OPS-*`)
consumes this section as its `durable_data` input and owns the operational targets this section defers to it:
the backup cadence and retention, the recovery-point and recovery-time objectives, the restore runbook, and
the availability target — all building on REQ-DOM-116 and REQ-DOM-115. The release bar (`BAR-*`) turns the
`release_gating: true` requirements here into testable gate criteria: REQ-DOM-100, REQ-DOM-109, and
REQ-DOM-113 are the core durability gate (state survives a real restart and redeploy, acknowledged writes are
not lost, no authoritative state lives in the process), REQ-DOM-116 is the backup/restore gate, and
REQ-DOM-115 is the readiness-reflects-the-store gate. The identity/security design (`REQ-ID-*`) owns the
structure of the Credential and Verified contact whose durability REQ-DOM-102 requires, and the `software`
domain owns every `how` this section deferred — the store engine, schema, migrations, connection handling,
and the migration mechanics behind REQ-DOM-114 and REQ-DOM-118.
