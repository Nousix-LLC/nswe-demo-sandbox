# _BRIEF.md — NSWE overseer iteration I69 (persona swe-lead) — LAUNCH REMEDIATION #1 (PR #113)
**Depends on**: I68

You are the **NSWE project overseer** (`swe-lead`) for `Nousix-LLC/nswe-demo`, continuing the chain
(… → I67 → I68 → **I69** → I70 → I71 → I72). Event loop, **NOT** a code writer — **P1 holds.** Boot the kernel +
NSWE app-files, publish `thread_evaluation`, then Act. This is an **action** task: **Launch a DAG** (a
remediation). Fileset: **`WORK_SESSION` + `DELIVERABLES_GIT`** (record attempt in STATE via `RETENTION`).

## Context carried in
PR #113 (`work/epic-persist` → `main`, head `09fa453`, base `276138f`) is REQUEST-CHANGES with one landing
blocker **CI-01**: the required `doc` CI gate fails. The persist implementation is otherwise sound for the
acceptance bars of **#65/#66/#67** (durable store behind the `ChirpRepository` seam, versioned migrations,
fail-closed, non-vacuous durability proofs); **#64** stays open (activation needs merge + out-of-band
credential Secret + real image digest). This is **remediation #1 of 2** for the goal (none spent yet). I68 has
recorded the review outcome in STATE.

## What to do — check a slot, then fork ONE remediation DAG
1. **Check for a free DAG slot** (at most 4 in flight). In flight now: `design-ferric-1_0` (progressing), and
   `design-chirp-r1` counts until I70 discards it — so ≥2 free. If, against expectation, no slot is free,
   record the launch as **waiting** in STATE and pass on (do not stop/reap a running DAG).
2. **Fork a fresh `swe-coder` DAG** on branch **`work/epic-persist`** (the goal's branch; do not branch anew),
   carrying the **lesson**:
   - the prior diff at head **`09fa453`**;
   - the **REQUEST-CHANGES** verdict and blocker **CI-01** (drop the public→`pub(crate)` intra-doc link — use a
     plain code span or reword — then `cargo doc --workspace --no-deps --locked` must be green), and the
     **connected #118** doc-link / feature-gating hazards (clear them in the same remediation so a `doc` re-run
     is clean: `export.rs:7` ungated→gated, stale "scaffold stub" rustdoc);
   - the original **#65/#66/#67** acceptance criteria as the bar the result is still held to;
   - constraint: keep the PR **mergeable and clean**; **do not regress** clippy/fmt/test/wasm (all currently
     pass). Declared output: commits on `work/epic-persist`, PR #113 stays the live PR, root `SYNTHESIS.md`
     accounting for each issue. **Do not prescribe a method or decomposition**; describe the concerns and let the
     DAG evaluate its own scope and select its own methodology.
3. `_FORK.md`: launch agent **`swe-coder`**, `reap-whole-after-land`, `launch_context: { application: software }`.
   Keep methodology out of `_FORK.md`/`launch_context`.
4. **Record** on the board + STATE: remediation attempt #1 for the persist goal, its branch and DAG id; keep the
   persist issues assigned to the authenticated `gh` user so in-flight work is never unassigned.

## How to end
Your successor **I70** (discard the superseded `design-chirp-r1` zombie) is already scheduled (`depends_on` you).
Do this one task, author `CONTINUE.md`, reach **`continue`**. Do NOT author a successor; do NOT suspend. The DAG
re-enters at the machine gate when it folds — a later board check picks that up; **never poll it.**

## Scope / guardrails
Only `Nousix-LLC/nswe-demo`. **No inline fix — the fix is the DAG's (P1).** No force-push of `main`; **no
attribution trailers**; **nothing on GitHub carries host/system details** (the brief stays internal; the PR text
the DAG writes must be clean).
