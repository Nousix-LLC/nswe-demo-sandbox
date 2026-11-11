# _BRIEF.md — Review DAG: PR #113 "Durable PostgreSQL persistence for chirp"

You are a code-review DAG for `Nousix-LLC/nswe-demo`. Your unit of work is **one review of one pull
request as a whole change**: PR **#113**, held issue by issue to the acceptance criteria of each issue it
closes and traced to the product's design of record. You read and judge; you do **not** change the
repository, push, comment edits into the code, or fix anything you find. Decompose your own review as your
evaluation of the diff's size and surface warrants; select and load the review methodology (and the
methodology for each concern) yourself from what this brief describes — nothing here tells you which to load.

## The target

- **PR**: `Nousix-LLC/nswe-demo#113` — "Durable PostgreSQL persistence for chirp: provision, wire, and prove
  durability". Head branch `work/epic-persist`, base `main`. Author `mattsmcknight`. State OPEN, not draft.
- **Review the change as a whole**, one review however many issues it closes. Read the full diff of
  `work/epic-persist` against its merge base with `main`, the PR description, and the branch's commits
  (read-only `git`/`gh`).
- **This PR was authored directly by the repository owner, not produced by a code DAG**, so there is **no
  code-DAG `SYNTHESIS.md`** for it. The machine signal for this change is therefore the **live CI rollup on
  the PR**, not a DAG verdict — see the CI concern below.

### What it closes, and the acceptance criteria to hold it to

The PR declares, as plain-text closing keywords, `Closes #65`, `Closes #66`, `Closes #67`. All three are
children of **epic #56 — Durable persistence & data integrity**. Trace the change against each issue's own
acceptance criteria (read each issue on GitHub):

- **#65** — domain invariants, derived counts (follower/following/like counts), and opaque monotonic ids
  hold in the durable store **under concurrency**. Evaluate whether the change actually proves this, not just
  asserts it.
- **#66** — durable storage plugs into the **`ChirpRepository` seam** soundly: the full capability set is
  implemented behind the existing seam, single-writer safety holds, and the schema is versioned and applied
  by a migration runner. Evaluate the seam fidelity and that no capability was dropped or weakened.
- **#67** — retention and capacity commitments are honoured (documented lifetimes for transient state, the
  reclaim job, the no-automatic-expiry rule for user content, fail-closed on a non-durable write) and
  durability is proven by a **repeatable, stranger-runnable drill** (restart, redeploy, reschedule).

- **#64 stays open by the PR's own account** — the durable store, its wiring, and the drill are delivered,
  but the *running system* becomes durable only after merge plus a follow-up digest-pin. Confirm whether that
  framing is accurate and whether anything the PR claims as "delivered" for #64 is in fact incomplete or
  belongs in this change. Note, do not close, #64.

### The design of record to trace to

The design landed in the repo at `design/` (read on `main`): `design/domain-application-design.md` carries
the **durable-persistence requirement**; `design/release-bar.md` carries the release bar (`BAR-*` / `REQ-*`).
`design/operational-readiness.md` is relevant to the provisioning/ops half of this change. The change must
satisfy the durable-persistence requirement and the applicable `BAR-*` items; a change that passes its tests
but misses a `BAR-*` the design requires is a finding.

## The review concerns — evaluate each as a distinct concern, each with its bar

Decide the final concern set from what the diff actually touches; the set below is what this change calls
for. For each, say what you checked, what you found, each finding's severity, and whether it **blocks
landing**.

- **Correctness against the acceptance criteria and the design.** Does the change do what #65/#66/#67 and the
  durable-persistence requirement say — including edge cases, error paths, the domain invariants and derived
  counts, opaque-id monotonicity, **concurrency and single-writer hazards**, migration/versioning behavior,
  and the fail-closed-on-non-durable-write rule? Bar: a behavior the criteria or design require that the
  change does not actually deliver, or delivers incorrectly, is a blocking finding.
- **Durability proof / test coverage and depth.** Do the tests and the drill exercise each acceptance
  criterion and the failure paths (restart, redeploy, reschedule; concurrency; a write that cannot durably
  commit)? Do they assert real surviving state (byte-for-byte rows AND system-level sign-in/content/counts
  through the HTTP API) rather than passing vacuously? Is the drill genuinely repeatable and runnable by
  someone without hidden local state? Is the `postgres` feature correctly gated so the default build/test
  stays store-free while the durable tests run against a real PostgreSQL? Bar: a criterion with no real proof,
  or a drill/test that proves less than it claims, is a finding (blocking when it leaves an acceptance
  criterion unproven).
- **Code quality and design.** Responsibilities and coupling across the store backend, the `ChirpRepository`
  seam, and the wiring; abstraction boundaries, duplication, naming, error-handling style; whether the
  feature-gated backend leaves the code simpler or harder to extend. Bar: a finding when the change degrades
  maintainability or the seam's clarity.
- **Architecture / contract stability.** The change touches a shared seam (`ChirpRepository`) and the
  deployment contract (manifests, the ArgoCD AppProject, probes moving to `/readyz`). Evaluate whether the
  seam's contract and the public/operational surface stay stable and coherent, and whether the additive
  AppProject changes (`StatefulSet`, `PersistentVolumeClaim`, `CronJob`) are correct and minimal.
- **Security and trust boundaries.** Credential handling for `CHIRP_DATABASE_URL` (supplied out of band,
  `Secret` excluded from the AppProject, nothing committed), SQL/injection and input handling at the store
  boundary, migration safety, the Pod Security `restricted` admission, and anything the diff pulls in
  (dependencies/features). Bar: an exposure or a committed/loggable secret is a blocking finding.
- **Operational readiness.** Provisioning soundness (single-primary StatefulSet + per-ordinal PVC + headless
  Service; volume headroom and the documented growth assumption), the readiness gating on `/readyz`/store
  health, the reclaim CronJob, and the digest-pin follow-up the PR names as the one step to activate the
  durable image. Trace against `design/operational-readiness.md`. Bar: an operational gap that would make the
  store unsafe or unavailable in the running system is a finding.
- **Rust language idiom.** One concern among the others, not the only one: idiomatic error handling,
  ownership/borrowing, async/concurrency constructs, and feature-gating hygiene.

### The failing CI check — diagnose it as its own concern

The **live CI rollup on PR #113** is: `clippy` PASS, `fmt` PASS, `test` PASS, `wasm` PASS, `image` skipping,
and **`doc` FAILING** — so the PR's merge state is UNSTABLE. The `doc` check is a required check: **the PR is
not clean to land while it fails.** Diagnose what the `doc` job is failing on (read the failing job's log via
`gh`), say what change would make it pass, and record it as a **blocker to landing** (the remediation that
clears it is a separate code DAG, not your job). Call this out explicitly in the verdict even if every code
concern is otherwise clean: an APPROVE verdict must still state that landing is gated on the `doc` check going
green and the PR being mergeable and clean.

## Declared output

- A **review posted on PR #113**. `gh pr review --approve` is rejected when the reviewer and author are the
  same org/account (this PR is owner-authored), so **post the review as a PR comment carrying the verdict**
  plus inline/line comments for specific findings. Every reviewed PR must visibly show its review.
- A **root `SYNTHESIS.md`** at this DAG's root with a single **APPROVE** or **REQUEST-CHANGES** verdict, the
  findings grouped **per concern** with each finding's severity and whether it blocks, and an explicit
  statement, per concern, of what was checked and what was found clean. The verdict is authoritative (it is
  what the overseer gates on), independent of whether the platform let the review post as a formal approval.
- **Non-blocking findings filed as backlog issues** on the repo: grouped, de-duplicated against existing
  issues, each linked back to PR #113 and to epic #56 / the issue it came from. Blockers are **not** filed as
  backlog; they are named in the verdict as what must change before landing.

Anything posted to GitHub (the review, inline comments, filed issues) is written for the repository's
readers: point at files and lines in the repository, reference issues and the design by their repo paths, and
include **no** host paths, cluster addresses, SSH/credentials, or taskflow/DAG internals.

## Constraints

- Repo scope: `Nousix-LLC/nswe-demo` only. **Read-only** on the code — review, do not modify, do not push, do
  not merge, do not fix. Filing backlog issues and posting the review/comments are your only GitHub writes.
- No host/system details anywhere on GitHub. No attribution trailers on anything you post.
