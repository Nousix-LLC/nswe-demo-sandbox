# _BRIEF.md — remediate-epic-persist-r1c (remediation #1 of PR #113, re-fork of frozen r1b)

**Task Kind**: code / remediation DAG (you are a `swe-coder` DAG; evaluate your own scope and decompose as you
see fit). Repository: `Nousix-LLC/nswe-demo`.

You are a fresh remediation for one goal. A prior remediation launch for this same goal
(`remediate-epic-persist-r1b`) was forked but its root never dispatched and produced **no verdict and no
commits** — it is abandoned. You carry its intent forward from scratch; nothing it did survives. This re-fork
spends **remediation attempt #1 of 2** for the goal (the frozen launch spent none).

## Objective

Make **PR #113** (`work/epic-persist` → `main`) landable: resolve the code review's blocking finding **and**
keep the goal's acceptance criteria met, so the PR can pass its required CI and earn an APPROVE re-review.

The goal is epic **#56** — durable PostgreSQL persistence for the chirp server (the current store is
in-memory). It covers issues **#65**, **#66**, and **#67**. Issue **#64 stays open and is out of this goal's
scope** — do not attempt to close it. The prior work on this goal is already on the branch: PR #113's head is
commit **`09fa453c3c40e39a9b4647e0de6e00dcf50ecb21`**. Build on that diff; do not restart the goal from zero.

## The blocker to clear (the one thing that makes this a remediation, not new work)

The review on PR #113 is **REQUEST-CHANGES**, and its single blocking finding is a CI failure:

- **The required `doc` CI check is red** while the other required checks — `clippy`, `fmt`, `test`, `wasm` —
  are all green at `09fa453` (the `image` check is skipping, which is expected). The merge is blocked solely
  because `doc` is red.
- **What must hold at the end:** the crate documentation builds cleanly under the repository's `doc` CI job on
  PR #113's branch, with the other required checks staying green (no regression of `clippy`/`fmt`/`test`/`wasm`).
  Describe-what-must-hold, not how: the `doc` job's own configuration (including any warnings-as-errors policy
  it applies) is the authority on what "clean" means — read the job definition in the repository and satisfy it.
- **Context from the prior review (awareness, not a prescription):** the failure was reported as a
  documentation-link / visibility-and-feature-gating hazard in the persistence layer. Non-blocker issue **#118**
  ("persistence-layer docs describe implemented methods as stubs; feature-gating doc hygiene") is the filed
  finding closest to this hazard. Use the live `doc` job output and the current code as your ground truth; the
  review text is a pointer, not a spec.

## Keep the goal's acceptance criteria met

Clearing the `doc` check must not come at the cost of the durable-persistence behavior the goal delivers. Hold
the result to the acceptance criteria of **#65, #66, #67** (read each issue's body on GitHub for its full
criteria):

- **#65** — the durable store preserves domain invariants, derived counts, and opaque monotonic ids under
  concurrency.
- **#66** — durable storage plugs into the `ChirpRepository` seam soundly: full capability set, single-writer
  safety, versioned schema.
- **#67** — retention and capacity commitments are honoured and durability is proven by a repeatable drill.

These issues are the checklist the result is judged against, not a plan for how to divide the work. If the fix
for `doc` touches persistence code, make sure the behavior these criteria describe still holds (and that
`test` stays green).

## Non-blockers — awareness only, not in scope

The review also filed non-blocking follow-ups as backlog issues **#115–#121** (e.g. CI-gating of the durability
drill #115, suspected concurrency hazards #116, a reclaim-sweep duplication #117, doc hygiene #118, deployment
coherence #119, security follow-ups #120, minor polish #121). **Do not take these on.** They are already tracked
on the board. Only if one is *trivially* co-resolved by the `doc` fix itself (for example #118's doc hygiene)
may it come along; otherwise leave them for their own goals.

## Inputs (read these; name everything by repository identity)

- **PR #113** at head `09fa453c3c40e39a9b4647e0de6e00dcf50ecb21` — the diff to build on; its failing `doc`
  check and the passing checks; its posted review.
- **The code review on PR #113** (REQUEST-CHANGES; blocker = the red `doc` check) and the filed non-blocker
  issues **#115–#121**.
- **Issues #65, #66, #67** and their acceptance criteria; the parent epic **#56**.
- The repository's **CI workflow definitions**, so the `doc` job's exact contract is known.

## Declared output

- **Commits on `work/epic-persist`** that update PR #113 so the `doc` check passes and the goal's criteria
  remain met. Do not open a new branch or a new PR; this updates PR #113.
- **A root `SYNTHESIS.md`** that is the machine verdict: state whether the `doc` blocker is resolved (and how
  it was verified — the build/`cargo doc`-equivalent the job runs), and account for each covered issue
  (#65/#66/#67) as met, or not and why. If anything the goal covered could not be finished, say so plainly.

## Constraints

- Scope is **`Nousix-LLC/nswe-demo` only**. Do not touch any other repository, project, cluster namespace, or
  CI outside this repo.
- Work on branch **`work/epic-persist`** only. **No force-push.** Do not push to `main`; never merge your own
  PR.
- **No attribution trailers** on commits.
- **Nothing you post to GitHub** (commit messages, the PR, `SYNTHESIS.md` content that reaches GitHub, any
  comment) may carry host paths, machine addresses, SSH/user details, or taskflow/workspace internals. Write
  for the repository's readers: the outcome, what changed, how it was verified, the issues addressed.

You select and load whatever methodology your concerns call for; this brief names none. Decompose or stay
atomic as your own evaluation decides.
