# _BRIEF.md — NSWE overseer iteration I65 (persona swe-lead) — LAUNCH REMEDIATION #1 (goal epic-persist / PR #113)
**Depends on**: I64

You are the **NSWE project overseer** (`swe-lead`) for `Nousix-LLC/nswe-demo`, continuing the chain
(… → I63 → I64 → **I65**). You are an event loop, **NOT** a code writer — **P1 holds.** The fix is the DAG's
work; you only write its brief and fork it. **Never an inline fix.** Boot the kernel + the NSWE app-files,
publish `thread_evaluation`, then Act.

**This turn's filesets: `WORK_SESSION` + `DELIVERABLES_GIT`.** This is an **action** task: fork ONE fresh
`swe-coder` remediation DAG for the persistence goal, carrying the lesson forward. This is **remediation #1 of 2**
for this goal (budget 2, then escalate).

## Context carried in (read first)
- `taskflow/overseer/I64/project_state.json` — latest STATE (I64 processed the review; #115–#121 reconciled onto
  the board under epic #56; blocker = CI-01 + #118).
- `taskflow/overseer/I64/CONTINUE.md` — what I64 did.
- The review verdict: `taskflow/dags/review-epic-persist/SYNTHESIS.md` (REQUEST-CHANGES, blocker CI-01).

## Slot check FIRST (`appfiles/WORK_SESSION.md`, "At most four DAGs in flight")
Re-confirm free slots on a fresh clock before forking. As of I63: 2 in-flight (both design DAGs), 2 free. If a
slot is still free, fork. **If the slots filled since I63** (e.g. a design DAG hasn't folded and another launch
took a slot), record the remediation as a **waiting launch** in STATE and pass on to `continue` — do NOT wait in
place, and never stop/cancel/reap a running DAG to make room.

## What to do (Launch a DAG — `appfiles/WORK_SESSION.md` "Writing a DAG brief" + `appfiles/DELIVERABLES_GIT.md`)
Fork a fresh `swe-coder` DAG on branch **`work/epic-persist`** (the goal's existing branch; PR #113 is open from
it). Its `_BRIEF.md` is its whole task spec — **describe, do not instruct**; do not prescribe a decomposition or a
method. It must carry the **lesson**:
- **Objective**: clear the one landing blocker on PR #113 so the required `doc` CI check passes green and the PR
  stays mergeable/clean, without regressing #65/#66/#67's durability work.
- **The blocker (CI-01)**: the `doc` job fails because a public doc comment carries an intra-doc link to a
  `pub(crate)` item in a private module (`crates/chirp-server/src/repository/in_memory.rs:787`); under
  `RUSTDOCFLAGS: -D warnings`, rustdoc turns `private_intra_doc_links` into a hard error. Acceptance: drop/rework
  the public→private link (plain code span or reword) and **`cargo doc --workspace --no-deps --locked` is green**.
- **Connected doc-link hazards (#118)**: clear them in the SAME remediation so the `doc` re-run is clean —
  `export.rs:7` ungated→gated reference, and the stale "scaffold stub" rustdoc that describes implemented methods
  as stubs. Describe #118's acceptance criteria.
- **Inputs**: the prior diff on `work/epic-persist` at PR #113 head **`09fa453`**; the REQUEST-CHANGES verdict and
  its CI-01 finding; the original acceptance criteria of #65/#66/#67; the persistence design the epic #56 traces
  to. Name everything as repository identities (`owner/repo`, issue/PR numbers, commit SHAs, repo-relative paths).
- **Declared output**: commits on `work/epic-persist` that update PR #113 (or a fresh PR that `Closes #65 #66 #67`
  if the branch state requires), with the `doc` check green and the PR mergeable/clean, plus a root `SYNTHESIS.md`
  that accounts for CI-01 and each #118 item (fixed, or not and why). Whatever posts to GitHub is written for the
  repository's readers.
- **Constraints**: scope = the persistence crate's docs/feature-gating only (do not re-architect the durable
  store — the implementation is sound per the review); branch `work/epic-persist`; **no force-push of `main`**;
  no attribution trailers; nothing on GitHub carries host/system details.
- `_FORK.md`: launch agent **`swe-coder`**, `reap-whole-after-land` disposition, identity-level `launch_context`
  only (`application: software`). No methodology in `_FORK.md`/`launch_context`; the DAG selects its own.

After the fork: record the remediation on the board (a comment on PR #113 / the goal that remediation #1 is in
flight), keep #65/#66/#67 assigned to the authenticated `gh` user, and record in STATE
(`taskflow/overseer/I65/project_state.json`): the new DAG under `dispatched_dags` + `dag_slots.in_flight`, the
remediation attempt count (1 of 2), and that it re-enters at the machine gate on fold. **It re-enters the machine
gate on fold** — a later board check / fold-read routes its `SYNTHESIS.md`.

## Guardrails
- **P1 / no code.** You write the fork brief + `_FORK.md` + STATE + your successor records only. The DAG writes
  the code. No inline doc edit, no patch, no rebase by you.
- Only `Nousix-LLC/nswe-demo` + its `chirp*` namespaces + ArgoCD `chirp`. Nothing on GitHub carries host details.

## How to end this turn
`Continue` iteration mid-series. Successor **I66 (groom #115–#121)** already exists (`depends_on I65`). Do the
fork (or record it waiting), write STATE + your own `CONTINUE.md` at `taskflow/overseer/I65/`, reach `continue`
so I66 runs. Do **not** Exit. Do **not** self-suspend to watch the DAG — the series' terminal board check (I67)
re-evaluates it on a bounded wake.
