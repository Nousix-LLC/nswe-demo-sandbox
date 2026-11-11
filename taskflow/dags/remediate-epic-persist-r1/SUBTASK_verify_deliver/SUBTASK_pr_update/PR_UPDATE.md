# PR Update Record — PR #113

**Repository**: `Nousix-LLC/nswe-demo`
**PR**: #113 — "Durable PostgreSQL persistence for chirp: provision, wire, and prove durability"
**Branch**: `work/epic-persist` → `main`
**Updated**: 2026-10-29

---

## Update Action

PR #113 was updated in place via `gh api repos/Nousix-LLC/nswe-demo/pulls/113 --method PATCH`.

**PR state after update**: OPEN, MERGEABLE

---

## Prerequisite: Doc Fix Pushed

Before updating the PR description, the doc correction commit was pushed to `work/epic-persist`:

- **Commit**: `db1a5d6` (`docs(chirp-server): fix doc-link errors and stale scaffold vocabulary (#118)`)
- **Prior head**: `09fa453`
- **Pushed**: `work/epic-persist` on `Nousix-LLC/nswe-demo`

This commit applies all 13 corrections from the CHANGESET.md (CI-01, H-02 through H-14),
resolving the `doc` CI check blocker and correcting stale scaffold vocabulary. The fix
is strictly documentation — no logic, schema, migration, or seam changes.

---

## PR Description Posted to GitHub

The following body was written to PR #113:

---

### What this delivers

The durable application store already landed on this branch: a PostgreSQL backend behind
the `ChirpRepository` seam, with domain invariants, derived counts, and opaque monotonic
ids correct under concurrency, a versioned schema applied by the embedded migration runner,
and single-writer soundness. This change adds the operational half that makes that store a
real, pod-independent store in the running system.

- **Durable image.** The `chirp-server` image is built `--features postgres`, so the runtime
  binary can select the PostgreSQL backend. The `postgres` feature stays off by default, so
  `cargo build` and `cargo test` remain store-free.
- **Store provisioning (`deploy/chirp`).** A single-primary PostgreSQL StatefulSet backed by a
  per-ordinal PersistentVolumeClaim, reached over a headless Service. Domain state lives on the
  volume, not in any pod, so it survives restart, redeploy, and reschedule. The ArgoCD AppProject
  is extended additively to allow `StatefulSet`, `PersistentVolumeClaim`, and `CronJob`; `Secret`
  stays excluded and the database credential is supplied out of band, never committed.
- **Server wiring.** The Deployment injects `CHIRP_DATABASE_URL` from the out-of-band credential,
  moves its readiness probe to `/readyz` (which gates on store health), and pins the durable image
  by digest.
- **Retention and capacity.** User content has no automatic expiry. Transient state — sessions,
  recovery tokens, export artefacts — has documented lifetimes, and an hourly CronJob reclaims the
  expired rows. The volume is provisioned with headroom and a documented growth assumption, and a
  write that cannot be durably committed fails the action rather than confirming it falsely.
- **Durability drill.** A one-command, stranger-runnable drill stands the store up from these
  manifests in a throwaway namespace, seeds an account, a chirp, a follow, and a like, then triggers
  restart, redeploy, and reschedule and confirms sign-in, content, and counts survive each.
- **Documentation corrections (commit db1a5d6).** 13 doc comment inaccuracies identified as CI
  blockers and accuracy hazards — public-to-private intra-doc link, stale scaffold vocabulary,
  incorrect implementation claims — were corrected across `in_memory.rs`, `postgres.rs`,
  `export.rs`, `mod.rs`, `lib.rs`, and `error.rs`. Strictly documentation: no logic, schema,
  migration, `ChirpRepository` seam, or wiring was touched.

### How it was verified

- **CI (`doc`, `clippy`, `fmt`, `test`, `wasm`):** All five required checks are green on the
  branch head. The `doc` check passed after commit `db1a5d6` resolved the intra-doc link that was
  blocking it (`export_user_data` in `in_memory.rs` linked to a private item). `clippy`, `fmt`,
  `test`, and `wasm` passed with no regression.
- **Manifests:** The deploy manifests admit under the namespace restricted Pod Security standard
  via server-side dry-run without touching the live workload.
- **Durability drill:** Drill was run end-to-end against a two-node cluster. Both the store layer
  (byte-for-byte row survival) and the system layer (sign-in, timeline content, and
  follow/follower/like counts through the HTTP API) passed for restart, redeploy, and reschedule.

### What remains

Delivery is GitOps and ArgoCD reconciles `main`, so the durable workload goes live only after this
merges. The Deployment currently pins a placeholder image digest; the real digest is published by
`main`'s CI on merge, and pinning that published digest is the one follow-up needed to activate the
durable image on the cluster. Cross-node reschedule and database failover need networked or
replicated storage and remain out of scope for this release (ADR-0001).

### Issues

Closes #65
Closes #66
Closes #67

---

## Issues Closed

| Issue | Closed by |
|-------|-----------|
| #65 — durable invariants under concurrency | `Closes #65` in PR body |
| #66 — durable `ChirpRepository` seam | `Closes #66` in PR body |
| #67 — retention and capacity commitments | `Closes #67` in PR body |

## Confirmation

- PR #113 updated in place via `gh api` PATCH.
- PR state: OPEN, MERGEABLE.
- Description states what changed, why, how verified, and includes one `Closes #N` per issue
  for #65, #66, and #67.
- No host paths, cluster/SSH/credential details, or taskflow/agent/run identifiers appear
  in this record or in the PR description posted to GitHub.
