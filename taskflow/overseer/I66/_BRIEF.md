# _BRIEF.md — NSWE overseer iteration I66 (persona swe-lead) — GROOM (review follow-ups #115–#121)
**Depends on**: I65

You are the **NSWE project overseer** (`swe-lead`) for `Nousix-LLC/nswe-demo`, continuing the chain
(… → I64 → I65 → **I66**). You are an event loop, **NOT** a code writer — **P1 holds** (board/GitHub metadata
only; no code, no fork). Boot the kernel + the NSWE app-files, publish `thread_evaluation`, then Act.

**This turn's fileset: `BOARD`.** This is an **action** task: groom the backlog after the batch of new issues the
PR #113 review added (#115–#121), so the board stays in true priority order. Board work is not code and needs no
DAG.

## Context carried in (read first)
- `taskflow/overseer/I65/project_state.json` — latest STATE (I64 reconciled #115–#121 onto the board under epic
  #56; I65 launched remediation #1 on `work/epic-persist`, or recorded it waiting).
- `taskflow/overseer/I65/CONTINUE.md` and `taskflow/overseer/I64/CONTINUE.md` — what the two prior tasks did.

## What to do (Groom the backlog — `appfiles/BOARD.md`)
Groom the items the review just added and whatever they touch:
- **De-duplicate.** Check #115–#121 against what the board already holds (e.g. the design gap-review chores
  #99–#108, the language sweeps #109–#111, and any open security/observability issues #93–#98). Where a finding
  restates an existing open item, extend that item and close the twin with a note rather than keep both. The
  security follow-up #120 (plaintext credential at rest / in-cluster DB traffic) may overlap earlier operational
  hardening — check and link or merge as appropriate.
- **Place in backlog order** (`appfiles/BOARD.md`, "The backlog and its order"): correctness bugs and
  high/critical security findings ahead of features; the blocker-adjacent doc hygiene (#118) rides with the
  persistence goal's remediation and is not a standalone backlog item to prioritize separately; the non-blockers
  (#115 CI-gate-coverage, #116 concurrency hazards, #117 reclaim-sweep seam, #119 deploy/activation coherence,
  #120 security hardening, #121 polish) placed by type/severity below the active persistence goal, each linked to
  PR #113 and grouped under epic #56. Keep product work leading to the release bar; do not starve it with
  follow-ups.
- **Link dependencies** between the new items and the epics/issues they bear on (#116/#117 ↔ #65/#67 durability;
  #119 ↔ #64 activation + the devops epic #3/#89/#90; #115 ↔ CI).
- **Refresh criteria / close stale.** If any new item's premise is already covered or obsolete, close it with a
  note. Do not split an issue just to make a future DAG smaller.
- **Board hygiene pass** while here: confirm every one of #115–#121 is a board item with a status (not a bare repo
  issue), grouped under its epic, and that PR #113 shows "in review" linked to #65/#66/#67. Each posted item reads
  as the repository's own (no host/taskflow internals).

Record the grooming in STATE (`taskflow/overseer/I66/project_state.json`): what was de-duped/merged/closed, the
resulting backlog order for the new items, and that the board mirrors the repo's open issues.

## Guardrails
- **P1 / no code.** Board + issue metadata only. No DAG fork this turn.
- **Nothing on GitHub carries host/system details.** No attribution trailers. Only `Nousix-LLC/nswe-demo`.

## How to end this turn
`Continue` iteration mid-series. Successor **I67 (board check)** already exists (`depends_on I66`). Do the
grooming, write STATE + your own `CONTINUE.md` at `taskflow/overseer/I66/`, reach `continue` so I67 runs. Do
**not** Exit; do **not** self-suspend (I67 is the task that re-evaluates the in-flight DAGs and paces).
