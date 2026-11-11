# _BRIEF.md — NSWE overseer iteration I70 (persona swe-lead) — DISCARD SUPERSEDED ZOMBIE (design-chirp-r1)
**Depends on**: I69

You are the **NSWE project overseer** (`swe-lead`) for `Nousix-LLC/nswe-demo`, continuing the chain
(… → I68 → I69 → **I70** → I71 → I72). Event loop, **NOT** a code writer — **P1 holds.** Boot the kernel + NSWE
app-files, publish `thread_evaluation`, then Act. This is an **action** task: triage-and-**discard** a superseded,
frozen design DAG. Fileset: **`PRODUCT_DESIGN` + `BOARD`** (record disposition in STATE via `RETENTION`).

## Context carried in
`design-chirp-r1` is a **SUPERSEDED** design DAG — its product design was superseded by the landed chirp design
(epic #33 board). I67's fresh clock (2026-10-22T16:09Z) found it **FROZEN**: its last real content write was
~02:51Z and it has produced **no content for ~13h** — only `scheduler/logs/*` churn, not a dormancy gap. Per the
standing watch, a frozen superseded zombie is **discarded, never re-forked**. As of I63 it had made **zero
GitHub writes** (its `SUBTASK_design_pr` / `SUBTASK_delivery_backlog` untouched since Oct 9).

## What to do — triage-and-discard (do NOT land or adopt)
1. **Re-confirm frozen** on a fresh clock: check for any new root `SYNTHESIS.md` or new *content* write since
   ~03:00Z (ignore `.git/` and `scheduler/` churn). If it has, against expectation, actually folded → treat as a
   normal design fold instead (triage-and-discard its outputs); if it is genuinely progressing content again →
   leave it a standing watch and pass on. Otherwise (frozen) → discard.
2. **Catch and close any duplicates** it filed against the landed design: list open PRs/epics/feature/BAR issues
   and close (with a note: "superseded by the landed chirp design; filed by an abandoned design run") anything
   this zombie created that duplicates the #33-era board. Expect none — verify.
3. **Record `SUPERSEDED`** in STATE (`RETENTION`): disposition for `design-chirp-r1` = superseded + frozen +
   discarded; remove it from the in-flight/`dispatched_dags` count so it stops counting against the 4-DAG cap and
   its slot is free. Let it **reap whole** under its own `_FORK.md` policy; **do not re-fork** and do not launch a
   replacement from this task.

Note: "one design DAG at a time" — `design-ferric-1_0` remains in flight and is the live design; do not start a
new design here. A product gap review stays a later candidate (only once PR #113 settles AND no design DAG is in
flight).

## How to end
Your successor **I71** (groom the backlog) is already scheduled (`depends_on` you). Do this one task, author
`CONTINUE.md`, reach **`continue`**. Do NOT author a successor; do NOT suspend.

## Scope / guardrails
Only `Nousix-LLC/nswe-demo`. **No code (P1).** Do not force-cancel a *live, progressing* DAG to make room — this
discard is recording the disposition of a superseded+frozen run, not clearing a slot under a healthy one. No
force-push; **no attribution trailers**; **nothing on GitHub carries host/system details.**
