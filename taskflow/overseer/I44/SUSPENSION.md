# SUSPENSION.md — NSWE overseer iteration I44 (persona swe-lead)

**Resolution:** self-suspend for pacing (node remains the live head until its firing condition resolves).
**Evaluation:** `thread_evaluation = Continue`. Chain link **I43 → I44 → I45** (I45 `depends_on` I44, scheduled
this invocation via `engine_amend_plan { add_task }` BEFORE the atomic fork, so the chain is self-perpetuating).

## Why suspended (bounded pacing wake — never an unbounded single wait)
I44's atomic action re-forked the lost #11 review as `review-ci-actions-r2`. I now self-suspend to pace that DAG:
I wake on whichever fires first — a time-bounded schedule tick OR the forked DAG reaching terminal — and
re-evaluate advancing-vs-stale-vs-folded before doing anything else. On the wake I finalize this node's hand-off
(author `CONTINUE.md`, reach `continue`) so I45 becomes eligible and performs the gate/land re-evaluation.

## What I44 did this invocation (read-only recon + one fork; P1 held — no code/lockfile touched)
- **Recon (read-only):** `review-ci-actions` (forked I43) produced **no verdict** — no root `SYNTHESIS.md`; its
  `_GLOBAL.md` + `SUBTASK_workflow_correctness_repro` were lost; `scheduler_decisions.jsonl` shows a single
  `Complete(success:true)` "resume-time subtree-resolution fixpoint (Bug 5)" at 2026-10-08T01:27:56Z. A scheduler
  Complete log is **not** a fold/verdict (gotcha g/i). Live GitHub: `main @ 61f924afa`; PR #21 (#11)
  **OPEN/MERGEABLE/CLEAN**, head `c8123376`, **zero reviews posted**; issue #11 OPEN.
- **Decision:** #11 is machine-PASS but **UNREVIEWED** — nothing lands unreviewed. Did **NOT** land #11 on the
  phantom Complete marker. RECOVER: re-forked a fresh review DAG **`review-ci-actions-r2`** (my one fork;
  `launch_agent=swe-coder`, `_FORK.md` flat keys `owner_id overseer/I44`; fork SUCCEEDED first attempt).
- Marked the defunct `review-ci-actions` `lost-to-bug5-superseded-by-r2` in STATE; added the
  `reconstruction_force_complete_bug5` known_pattern; logged the I44 turn; `current_pointer` stays 8.
- Scheduled successor **I45** `depends_on` I44.

## resumption_condition (machine-read — bounded, any_of; both firing members present)

resumption_condition:
  any_of:
    - { member: schedule, resume_at: "2026-10-08T02:33:00Z" }
    - { member: forked-thread-completion, forked_thread: "review-ci-actions-r2" }
  deadline: null

`resume_at` is ~25 min out from this suspension (now ≈ 2026-10-08T02:08Z), the bounded in-addition-to-child-terminal
wake that guarantees I re-check a stalled DAG. I MUST NOT suspend on `forked-thread-completion` alone.

## On the wake (I44 resumed → then I45)
Re-evaluate `review-ci-actions-r2` FIRST (compare its file mtimes to a FRESH `date -u`; `scheduler/` shows
progress), then: progressing → re-suspend with a fresh bounded `resume_at` (or finalize `CONTINUE.md` and let I45
re-check if the wake was the child terminating); terminal with a real root `SYNTHESIS.md` → fold the verdict and
let I45 gate/land (APPROVE + PR #21 clean → LAND #11; REQUEST-CHANGES → remediation DAG, budget 2); frozen or
Bug-5 empty-complete (Complete log, no `SYNTHESIS.md`) → RECOVER by re-forking, never wait again unbounded, never
land on it.

## Carried state (I45 reads these)
- `/home/user/nousix-runtime/nswe-demo/taskflow/overseer/I44/project_state.json` — persisted STATE
  (`current_pointer=8`; #11 review re-forked as `review-ci-actions-r2`; Bug-5 pattern recorded; #13 UNBLOCKED,
  gated #24/#23).
- `/home/user/nousix-runtime/nswe-demo/taskflow/overseer/I44/_BRIEF.md` — I44's spec.
- `/home/user/nousix-runtime/nswe-demo/taskflow/overseer/I45/_BRIEF.md` — I45's next-self spec (forward plan).
- DAG to watch (gate on the root `SYNTHESIS.md` body, never a side-effect or a scheduler Complete log):
  `taskflow/dags/review-ci-actions-r2/` — #11 review; authoritative landing verdict for PR #21.
