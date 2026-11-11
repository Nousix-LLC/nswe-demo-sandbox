# Review verdict — PR #113 "Durable PostgreSQL persistence for chirp" @ 09fa453

**Target**: `Nousix-LLC/nswe-demo#113` — `work/epic-persist` → `main`, pinned head
`09fa453c3c40e39a9b4647e0de6e00dcf50ecb21`, +11,851 / −77 across 28 files. Owner-authored. Closes #65, #66,
#67 (children of epic #56); #64 stays open.

This record folds seven concern reviews into one verdict. It is authoritative and independent of whether the
platform accepts a formal approval on an owner-authored PR. All locations pin to the commit above.

---

## Verdict: REQUEST-CHANGES

One finding blocks landing:

- **CI-01 — the required `doc` check fails.** `cargo doc --workspace --no-deps --locked` runs with
  `RUSTDOCFLAGS: -D warnings`; the public doc comment on `export_user_data`
  (`crates/chirp-server/src/repository/in_memory.rs:787`) carries an intra-doc link
  `` [`ExportDocument`](super::export::ExportDocument) `` to a `pub(crate)` item in a private module, which
  `rustdoc::private_intra_doc_links` turns into a hard error, so the crate fails to document and the check is
  red. Merge state is `UNSTABLE` solely because of this required check.

**Landing is gated on the `doc` check going green AND the PR being mergeable and clean**, even though every
code concern is otherwise non-blocking. A green `doc` run after the fix is the bar; because rustdoc reports
only the first crate that fails, the remediator must re-run `doc` to confirm no further `-D warnings` error
surfaces behind this one (see the documentation/feature-gating backlog item, which names two more public→
private / ungated→gated doc links that can surface next).

The implementation underneath the blocker is sound for its acceptance bars: the #66 capability set is fully
delivered behind the `ChirpRepository` seam with versioned migrations and a documented single-writer posture;
#67 fails writes closed, keeps user content un-expired, and enforces transient lifetimes; the #65 store is
well-built, with non-vacuous, stranger-runnable durability proofs. The blocker is a documentation-link lint in
a required check, not a defect in the durable store.

---

## Contract identity evaluation

All ten identities were evaluated as assertions over the seven findings documents. None was silently plugged.
One cross-concern severity divergence was adjudicated (recorded under "Cross-concern adjudications" below);
that is a reconciliation ID-SEVERITY anticipates, not an identity failure.

| Identity | Result | Basis |
|---|---|---|
| ID-SCHEMA | PASS | All seven concern documents conform to `finding_schema.md`: each states what it checked and what it found clean, and every finding carries the per-finding field set. |
| ID-PIN | PASS | Every finding pins a repo-relative file + line range @ 09fa453, or is explicitly whole-PR / design-level with its rationale (e.g. the activation-framing finding). |
| ID-SEVERITY | PASS | Every finding carries a severity and a `blocks_landing` boolean. The rubric is applied honestly: no blocker is downgraded to backlog to ease approval, no preference is inflated. The one inter-concern severity conflict is adjudicated openly below. |
| ID-ACTIONABLE | PASS | The blocker names a concrete change: drop the public→private intra-doc link at `in_memory.rs:787` (plain code span, or reword), then confirm `doc` is green. |
| ID-DOC-GATE | PASS | The failing required `doc` check is represented as the landing blocker, and the verdict states landing is gated on `doc` going green and the PR being mergeable and clean. |
| ID-VERDICT | PASS | REQUEST-CHANGES, because a `blocks_landing: true` finding exists (CI-01). |
| ID-BACKLOG | PASS | The blocker is named in the verdict, not filed as backlog. Non-blocking findings are grouped into seven backlog issues, de-duplicated against open issues, each linked to PR #113 and epic #56 / its originating issue. |
| ID-NO-HOST | PASS | No posted artifact and no content of this record carries host paths, cluster/SSH/credential details, or review-process internals; all references point at repo files, lines, issues, and design paths. |
| ID-PLAIN-VOICE | PASS | The verdict, the PR comment, every inline comment, and every filed issue went through the plain-voice finishing pass before posting. |
| ID-64-OPEN | PASS | #64 is confirmed OPEN; its "stays open" framing is accurate (below). It is neither closed nor filed as backlog. |

---

## Per-concern findings

Severities: **blocker** (blocks landing), **major** / **minor** / **nit** (backlog). Finding ids are the
spokes' own.

### Correctness vs acceptance criteria & design — sub-verdict: HAS-BLOCKERS (adjudicated to non-blocking; see below)
- **Checked**: #65 invariants / derived counts / opaque monotonic ids under concurrency (schema sequences,
  count columns + `CHECK (>=0)`, composite PKs, the store's `with_transaction` and count helpers, the
  concurrency suite); #66 full capability set behind the seam (all 24 trait methods have real durable bodies,
  stub/weakening scan, single-writer topology, the embedded migration runner); #67 retention / fail-closed
  (no user-content expiry, transient lifetimes, the reclaim path, capacity fail-safe); the durable-persistence
  requirement and the #64 framing.
- **Clean**: ids are opaque, server-assigned, monotonic, durable; counts move in lockstep with edges inside one
  transaction; handle uniqueness resolves via the unique-index violation; timeline paging is exactly-once;
  rows are re-validated on the way out; all capabilities are implemented behind (not around) the seam; writes
  are confirmed-durable; migrations are forward-only, versioned, and fail startup on error; user content has no
  expiry path; fail-closed holds end to end at the substrate; the #64 "stays open" framing is accurate.
- **Findings**: COR-01 (#65's under-concurrency proof runs in no CI gate — spoke severity **blocker**,
  adjudicated **major**); COR-02 (delete-vs-concurrent-edge count drift, **major**, suspected); COR-03
  (reciprocal-follow lock-order deadlock surfaced as `Internal`, **major**, suspected); COR-04 (restart-id
  stability proved by a fresh pool, not a real restart, **minor**); COR-20 (seam docs call the implemented
  backend un-implemented stubs, **major**); COR-21 (`remove_chirp` advertises a `Forbidden` it never returns,
  **minor**); COR-22 (single-writer rests on a replica count with no hard guard, **minor**); COR-23 (credential
  stored and compared in plaintext, **minor**); COR-40 (reclaim CronJob SQL is a hand-copy of the tested Rust
  sweep, **major**); COR-41 (`sessions.expires_at` nullable → lifetime by convention, **minor**); COR-42
  (capacity classification not applied to statement-level errors, **nit**); COR-43 (capacity returns 500 not
  503, **nit**); COR-44 (fail-closed / sweep tests skip with no test DB, **minor**); COR-60 (PR's "one
  follow-up" understates what activates durability, **minor**, whole-PR).

### Durability proof (test depth + the drill) — sub-verdict: NON-BLOCKING-ONLY
- **Checked**: the two integration test files, the in-crate durable/live tests, the drill script and procedure,
  the CI wiring and feature gating, the composition root, read against the source issues' acceptance criteria.
- **Clean**: the durable concurrency assertions reconcile stored counts against the real edge set read back
  through the public API (a count regression cannot pass by agreeing with itself); the fresh-pool proxy is
  labelled as the proxy it is; fail-closed substrate proofs read back absence, not just an error, and verify
  non-capacity SQLSTATEs are not misclassified; the fan-out is sized not to become a capacity test; the suite
  is rerunnable; readiness fail-closed is tested on both arms with a double standing in for the boundary;
  startup is fail-closed; the drill is stranger-runnable with disclosed caveats and refuses a movable tag or
  the all-zeros digest.
- **Findings**: DUR-01 (no required check executes any durable-store proof, **major**); DUR-02 (the drill's
  default store-layer run proves a synthetic table but the summary claims user data survived, **major**);
  DUR-03 (reschedule mode degrades to same-node rebind on node-local storage, **nit**); DUR-04 (fail-closed
  proven at the substrate, not end-to-end to the user, **minor**, suspected).

### Code quality, design & Rust idiom — sub-verdict: NON-BLOCKING-ONLY
- **Checked**: the seam's object-safety and additive growth, the ~2,600-line durable backend and its `mapping`
  module, the in-memory backing, `export.rs`, the wiring (`main.rs`, `router.rs`, `error.rs`, `Cargo.toml`),
  Rust idiom (error handling, ownership, async/transactions, SQL parameterization, panic-freedom,
  feature-gating leakage), diff provenance, and a plain-voice scan of shipped comments.
- **Clean**: additive object-safe seam; `with_transaction` enforces confirmed-write-before-success and is
  centralized; one fail-safe error-mapping point with a pure, unit-tested capacity classifier; boundary
  re-validation with panic-free production paths; uniformly parameterized SQL; counts move inside the edge
  transaction; the two backings stay consistent; tidy config-driven wiring.
- **Findings**: CQ-01 (comments describe implemented methods as "scaffold stubs" / "placeholders", **major**);
  CQ-02 (an always-compiled module intra-doc-links into the `postgres`-gated module, **minor**, feature-gating
  hygiene — bears on the `doc` remediation); CQ-03 (`FollowRow`/`LikeRow` and converters unused outside tests,
  **minor**); CQ-04 (internal work-breakdown vocabulary in shipped comments, **minor**); CQ-05 (`error.rs`
  header contradicts its own code, **nit**, pre-existing); CQ-06 (moral-tone adjectives cluster on health
  comments, **nit**, plain-voice — source only, not posted).

### Architecture / contract stability — sub-verdict: NON-BLOCKING-ONLY
- **Checked**: the `ChirpRepository` seam (method set, object-safety, additive release-bar growth), the second
  implementor and the migration/versioning path, the composition root, the public HTTP surface, the error
  surface, the deployment contract (AppProject whitelist, Application binding, probes, StatefulSet, Service,
  CronJob), traced to the design of record, and every sibling path the manifests cite.
- **Clean**: the seam stays stable, additive, object-safe, and is a second implementor rather than a fork;
  capability set complete at the contract level; the public HTTP and error surfaces stayed stable
  (`Unavailable` reuses the frozen 500 cell); readiness gates on store health; AppProject additions are
  additive, minimal, and exclude `Secret`; single-writer posture is correct and documented; schema is
  versioned with a forward migration path.
- **Findings**: ARC-01 (scheduled sweep bypasses the seam and duplicates it as raw SQL, **major**); ARC-02
  (release-bar capabilities live on the seam but not on the `/api/…` surface — a #66 acceptance-criterion
  reading, **major**, suspected; adjudicated below); ARC-03 (committed manifests cite sibling scaffolding paths
  not in the repo, **major**); ARC-04 (deployment set not apply-ready at this commit — placeholder digest,
  **minor**); ARC-05 (seam/contract self-description lags the durable backend it now has, **nit**).

### Security & trust boundaries — sub-verdict: NON-BLOCKING-ONLY
- **Checked**: the whole `CHIRP_DATABASE_URL` supply path and every place it could leak; all 78 query-
  construction sites for injection surface; migration safety; Pod Security `restricted` admission on all three
  workloads; the 147-crate `Cargo.lock` delta and TLS tree; server-detail leakage to clients.
- **Clean**: no committed or logged DB credential (sourced from an out-of-band Secret; AppProject cannot sync a
  Secret); no injection surface (literal SQL + `.bind()` throughout, no `unsafe`); migrations are idempotent,
  forward-only, non-destructive, applied before serving; all three workloads satisfy `restricted`; no
  server-side detail leaks to HTTP clients; dependency pull-ins are the expected registry-sourced,
  checksummed `sqlx` + `rustls` tree with the `postgres` feature off by default.
- **Findings**: SEC-01 (durable store persists the login secret verbatim and verifies with non-constant-time
  `==`, **major** — pre-existing, mirrors the in-memory seam, deferred to the identity/trust work; persistence
  now makes the plaintext secret backup-able); SEC-02 (DB credential crosses the in-cluster network
  unencrypted via `PGSSLMODE: disable` on the sweep job, **minor**, suspected for the server leg).

### Operational readiness — sub-verdict: NON-BLOCKING-ONLY
- **Checked**: provisioning shape (single-primary StatefulSet, per-ordinal PVC, retention policy, access mode,
  StorageClass), restricted-PSA posture of the DB pod, readiness gating, the reclaim CronJob (schedule,
  concurrency, deadlines, the three deletes compared line-for-line to the schema and the repository method),
  capacity commitments, and the image/credential activation path.
- **Clean**: pod-independent storage shape; PVC retention set explicitly to `Retain`/`Retain`; single-writer
  documented as a store property; readiness gates traffic on store health (`/readyz` = `store_health`); the
  CronJob SQL matches the code and schema and leaves user content untouched; CronJob hygiene is sound; capacity
  fails safe and is tested; the placeholder digest fails closed.
- **Findings**: OPS-01 (node-local default storage leaves cross-node reschedule unmet on the target, **major** —
  disclosed, tracked by #64); OPS-02 (the reclaim CronJob re-implements the sweep's delete logic, a second
  source of truth, **major**); OPS-03 (a failing sweep is not observable, **minor** — deferred to
  observability); OPS-04 (activation is a manual, un-gated step and "visibly not-ready" overstates the
  post-merge state, because `maxUnavailable: 0` keeps the previous non-durable pod serving until the digest is
  pinned, and the out-of-band credential Secret is a second prerequisite, **major**).

### CI `doc` check diagnosis — sub-verdict: HAS-BLOCKERS
- **Checked**: the live CI rollup, the failing `doc` job log down to the failing step, the single rustdoc error
  and the crate it failed to document, correlation to the diff, and whether a second link would still fail
  after the first is fixed.
- **Clean**: every other check passes at the pinned commit (`clippy`, `fmt`, `test`, `wasm` green; `image`
  skipping); the failure is one localized, deterministic rustdoc lint error in `chirp-server`, reproducible
  from the change; the PR is otherwise mergeable with no conflict.
- **Findings**: CI-01 (required `doc` check fails: public docs link to a private item under `-D warnings`,
  **blocker**, verified).

---

## Blockers — what must change before landing

1. **Green the required `doc` check (CI-01).** Stop the public doc comment at
   `crates/chirp-server/src/repository/in_memory.rs:787` from linking to the `pub(crate)`
   `super::export::ExportDocument` — replace the intra-doc link with a plain code span `` `ExportDocument` ``
   or reword so public docs no longer link into the private `export` module. Then run
   `cargo doc --workspace --no-deps --locked` with `-D warnings` and confirm it is clean: rustdoc reports only
   the first failing crate, and the documentation backlog item names two further links (`export.rs:7` into the
   `postgres`-gated module, and the stale scaffold rustdoc) that can surface next. Landing also requires the PR
   to be mergeable and clean at merge time.

No other finding blocks landing. Everything below is backlog.

---

## Cross-concern adjudications

The spokes recorded their overlaps rather than reconciling them, by design. The gate reconciles them here.

1. **The durable proof suite executes in no required CI gate — adjudicated major, non-blocking.** Correctness
   rated this a **blocker** for #65 (COR-01: a guarantee the gate never runs is "asserted, not proved"); the
   durability-proof concern — whose dedicated bar is "is it proved?" and which read the tests most closely —
   rated the same gap **major** (DUR-01: the proofs exist, are non-vacuous, and are stranger-runnable from a
   documented command, so no criterion is left unproven; what is missing is enforcement against future
   regression). #67's facet (COR-44) and #66's proof-in-CI note are the same root cause. These are one gap,
   not four. I adjudicate it **major / non-blocking**, because #65's criterion — invariants proved by
   automated tests, checkable by a stranger — is met in substance: the suite exists, its assertions would fail
   on a real regression (verified by the durability concern), and a stranger can provision Postgres and run the
   documented command. The absent required job is a maintainability / rot gap (the rubric's "proves less than
   it claims but the criterion is proven elsewhere" is close; here the criterion is proven, just not gated), so
   it is the top backlog item and carries a real post-merge regression risk, but it is not an unmet acceptance
   criterion. Recorded transparently because the two concerns genuinely diverged; the verdict is REQUEST-CHANGES
   regardless, on the `doc` blocker, so this adjudication eases nothing.
2. **#66 capabilities on the seam but not on `/api/…` (ARC-02) — adjudicated non-blocking.** Two readings of
   #66's "each mapped to the existing `/api/…` surface" are possible: routes required in this PR, or seam-level
   expression with HTTP wiring staged. The correctness concern treats the capability set as delivered behind
   the seam (the #66 bar), consistent with the PR's own framing that #64 stays open because the running system
   becomes durable only after merge plus follow-up. I adopt the staged reading: the seam contract is sound, and
   the deferred HTTP wiring is a recorded, intended stage, not a silent omission. It is captured as a minor
   backlog clarification, not a blocker.
3. **The stale scaffold rustdoc and the `doc` blocker are connected but distinct.** The actual `doc` failure
   (CI-01) is the private-intra-doc link at `in_memory.rs:787`. The stale "scaffold stub" prose
   (COR-20 / CQ-01 / CQ-04) is a separate documentation-integrity defect, and `export.rs:7`'s ungated→gated link
   (CQ-02) is a further `doc` hazard. The remediator of the blocker should clear all of these so a re-run of
   `doc` is clean; they are also filed together as a documentation backlog item.

---

## Non-blocking backlog (grouped) — filed issues

Seven backlog issues, grouped by remediation workstream, de-duplicated against open issues, each linked to PR
#113 and epic #56 / its originating issue. Blockers are not filed.

1. **Durability proof enforcement & drill-summary accuracy** (#115) — COR-01, DUR-01, COR-44, DUR-02, DUR-03.
   The durable suite runs in no required check; the drill's default run overstates what it proved. → #65, #67,
   #56.
2. **Suspected durable-concurrency hazards** (#116) — COR-02 (delete-vs-edge count drift), COR-03
   (reciprocal-follow deadlock → `Internal`). Each would be blocker-class for #65 if reproduced; both are
   currently uncovered. → #65, #56.
3. **Reclaim sweep has two sources of truth** (#117) — COR-40, ARC-01, OPS-02 (CronJob SQL duplicates the
   repository method and bypasses the seam) and OPS-03 (a failing sweep is not observable, deferred to
   observability #90). → #67, #56.
4. **Stale scaffold documentation & feature-gating hygiene** (#118) — COR-20, CQ-01, CQ-04, CQ-02, CQ-03,
   CQ-05, CQ-06, ARC-05. Persistence-layer docs describe implemented methods as stubs; internal build
   vocabulary and two ungated→gated / public→private doc links remain. Voice-only items cross-reference the
   language sweep #110. → #66, #56.
5. **Deployment & activation coherence** (#119) — ARC-03 (manifests cite scaffolding paths absent from the
   tree), OPS-04 and COR-60 (activation understated: digest-pin + out-of-band Secret + a not-ready window where
   the previous non-durable pod keeps serving), ARC-04 (placeholder digest, not apply-ready at this commit). →
   #64, #56.
6. **Security follow-ups, persistence-specific** (#120) — SEC-01 (credential stored plaintext +
   non-constant-time verify; persistence makes it backup-able), SEC-02 (in-cluster DB traffic unencrypted).
   Both pre-exist or are deferred; linked to the identity/trust epic #83 and #47, and to transport item #101. →
   #66, #56.
7. **Minor correctness / schema / idiom polish** (#121) — COR-04, COR-21, COR-22, COR-41, COR-42, COR-43,
   DUR-04, and the ARC-02 clarification. → #65, #66, #67, #56.

---

## #64 status (noted, not closed, not filed as backlog)

#64 is confirmed OPEN, and its "stays open" framing is accurate. The store, the seam wiring
(`deploy/chirp/10-deployment.yaml` injects `CHIRP_DATABASE_URL`, the server selects PostgreSQL when it is set),
the `/readyz` gate, and a repeatable drill are delivered — so #65/#66/#67 close — but the running deployment
becomes durable only after merge (GitOps reconcile), the out-of-band credential Secret being present, and the
real image digest replacing the all-zeros placeholder. That is exactly what BAR-019's operational check against
the live deployment gates on, so #64 legitimately remains open. The cross-node-reschedule limitation (OPS-01)
and the activation sequence (OPS-04, COR-60) are recorded against #64 rather than presented as satisfied.

---

## Plain-voice pass

The verdict, the PR comment, every inline comment, and every filed issue were held to the plain-voice bar
before posting: no moral adjectives glued to artifacts that cannot carry them, no narrated candor, no template
filler, no inflated seamless / robust / comprehensive / leverage. (CQ-06 flags the one such tell inside the
source comments; it is source-only and does not touch posted prose.)
