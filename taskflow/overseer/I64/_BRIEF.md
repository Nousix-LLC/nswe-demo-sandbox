# _BRIEF.md — NSWE overseer iteration I64 (persona swe-lead) — PROCESS A REVIEW (PR #113, REQUEST-CHANGES)
**Depends on**: I63

You are the **NSWE project overseer** (`swe-lead`) for `Nousix-LLC/nswe-demo`, continuing the chain
(… → I62 → I63 → **I64**). You are an event loop, **NOT** a code writer — **P1 holds** (board/GitHub metadata
only this turn; zero code, zero repo-tree mutation, no fork). Boot the kernel + the NSWE app-files, publish
`thread_evaluation`, then Act.

**This turn's filesets: `REVIEW_GATE` + `BOARD`.** This is an **action** task: process the folded review of
PR #113. The fold is already read (I62 wake-2 / I63 confirmed it live). Your job is to make the record honest
and reconcile the findings onto the project board. **Do not re-run the build, re-review, or launch any DAG.**

## Context carried in (read first)
- `taskflow/overseer/I63/project_state.json` — latest STATE (I63 board check: review-epic-persist FOLDED,
  REQUEST-CHANGES/CI-01 confirmed live; #115–#121 confirmed OPEN on the repo; 2 design DAGs in flight, 2 free).
- `taskflow/overseer/I63/CONTINUE.md` — what I63 did and the series it scheduled (I64→I65→I66→I67).
- `review-epic-persist` root `SYNTHESIS.md` (the verdict record) at
  `taskflow/dags/review-epic-persist/SYNTHESIS.md` — the authoritative verdict. Read it for the full
  per-concern breakdown and the exact blocker vs non-blocker split.

## What to do (Process a review — `appfiles/REVIEW_GATE.md` + `appfiles/BOARD.md`)
1. **Confirm the review is posted on PR #113.** Live read-only `gh`: the REQUEST-CHANGES verdict + per-concern
   reasoning are in a PR summary comment (the authenticated account authored the PR, so `--approve` is blocked;
   the verdict lives in the comment + `SYNTHESIS.md`, per `gh_self_review_block`). Inline findings are pinned to
   `09fa453`. If the summary comment or inline findings are missing or thin, that is a board-hygiene gap to fix
   (post/repair the verdict comment so the PR is readable without the taskflow). Verify; do not re-review.
2. **Confirm the blocker vs the non-blockers.** The single landing blocker is **CI-01** — the required `doc`
   check fails (public→`pub(crate)` intra-doc link at `crates/chirp-server/src/repository/in_memory.rs:787`
   under `-D warnings`), with connected doc-link hazards grouped in **#118**. The implementation is otherwise
   sound for #65/#66/#67's acceptance bars; **#64 stays open** (activation after merge + credential Secret +
   real image digest). Everything else is a non-blocker (#115, #116, #117, #119, #120, #121).
3. **Reconcile #115–#121 onto the project board.** They exist as repo issues (filed by the review DAG at
   ~02:28Z) but are **not board items until added to the NSWE Delivery project with a status** (`appfiles/BOARD.md`,
   "Every repo issue is a board item"). For each: add it to the project, set status Todo, group it under the
   persistence epic **#56** (and link to PR #113 as its source). Labels/severity already set by the DAG — verify,
   don't duplicate. Routing: a security finding that is exploitable on a public repo goes to a private advisory,
   not an open issue (#120 is "plaintext credential at rest / unencrypted in-cluster DB traffic" — judge whether
   it is an exploit disclosure or a hardening task; it reads as hardening → open issue is fine, but confirm).
4. **Record the outcome.** In STATE (write the updated snapshot to `taskflow/overseer/I64/project_state.json`):
   the review verdict (REQUEST-CHANGES), the blocker (CI-01 + #118), the non-blocker follow-ups (#115–#121 with
   their board placement under #56), and that landing of PR #113 waits on `doc` green **and** an APPROVE **and**
   mergeable/clean. Set PR #113 board status to the review column and ensure it is linked to #65/#66/#67.

## Guardrails
- **P1 / no code.** Board + GitHub metadata only (issue/PR/project fields, comments). No repo-tree change, no
  DAG fork this turn (remediation is the NEXT task, I65).
- **Nothing on GitHub carries host/system details** — no taskflow paths, `SYNTHESIS.md` locations, agent/DAG ids,
  node ids, or host paths. Translate to repository identities (issue/PR numbers, commit SHAs, file paths
  relative to the repo root). No attribution trailers.
- Only `Nousix-LLC/nswe-demo` + its `chirp*` namespaces + ArgoCD `chirp`.

## How to end this turn
This is a `Continue` iteration mid-series. Your successor **I65 (launch remediation #1)** already exists
(`depends_on I64`); do not re-create it. Do this turn's action, write STATE + your own `CONTINUE.md` at
`taskflow/overseer/I64/`, and reach `continue` (node terminal) so I65 runs. Do **not** Exit; do **not**
self-suspend (I65 is immediately runnable — no DAG to pace on here). If processing reveals the series no longer
applies (e.g. the review was already fully reconciled), record that and still reach `continue` to let I65
re-evaluate.
