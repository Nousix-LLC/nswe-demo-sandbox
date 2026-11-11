owner_id: chirp-logged-out-r6
observation_seam: taskflow/dags/chirp-logged-out-r6/SYNTHESIS.md
launch_agent: swe-coder
thread_type: dag
disposition: retain
reap: whole-after-land

# _BRIEF.md — SUBTASK_synthesis (chirp-logged-out-r6)

**Owner**: chirp-logged-out-r6
**Kind**: synthesis
**Task Kind**: synthesis
**Depends on**: none

## Objective

Verify each of the five acceptance criteria for issue #35 against the existing implementation
on branch `work/chirp-logged-out` in repository `Nousix-LLC/nswe-demo`, produce the root
`SYNTHESIS.md` at the observation seam, and complete the DAG fold so the parent task reaches
its terminal state.

## Parent task ID

The task that is SUSPENDED waiting for this synthesis to complete is:
`proc-43de7e9f-cfbc-4dfc-aa75-734b6b18740c`

After writing `SYNTHESIS.md` and your own `COMPLETE.md`, you MUST call
`engine_resume_suspended` with:
- `target_task_id`: `proc-43de7e9f-cfbc-4dfc-aa75-734b6b18740c`
- `synthesized_task_id`: your own process ID (from your boot_complete response)
- `seam_path`: absolute path to `taskflow/dags/chirp-logged-out-r6/SYNTHESIS.md`

This fold call flips the parent from SUSPENDED → COMPLETED and is the terminal action of this
synthesis task. Without it, the DAG cannot advance.

## Inputs

- Branch: `work/chirp-logged-out` in `Nousix-LLC/nswe-demo`
- PR: https://github.com/Nousix-LLC/nswe-demo/pull/263 (`feat: logged-out public timeline and user profiles (#35)`)
- CI status at prior discovery: all six checks (fmt, clippy, test, wasm, doc, image) COMPLETED SUCCESS
- Parent global context: `taskflow/dags/chirp-logged-out-r6/_GLOBAL.md`
- Existing SYNTHESIS.md: `taskflow/dags/chirp-logged-out-r6/SYNTHESIS.md` — verify its accuracy

## Acceptance criteria to assess

- **AC-1 (REQ-PROD-013 / BAR-011):** A logged-out visitor can load the home/public timeline
  and open a user profile and read chirps without being forced to sign up or sign in.
- **AC-2 (REQ-PROD-014 / BAR-011):** On arrival with no content, the visitor sees a clear
  statement of what Chirp is plus an obvious way to sign up or sign in — never a blank page.
- **AC-3 (REQ-PROD-014 / BAR-011):** If the timeline fails to load, a clear, recoverable
  message is shown instead of a broken screen.
- **AC-4 (REQ-PROD-015 / BAR-011):** A "create an account" route is visible on the landing
  and on the sign-in screen, and following it reaches sign-up.
- **AC-5 (REQ-UX-002 / REQ-UX-030–032 / BAR-011):** The logged-out landing/timeline renders
  its loading, empty, error, and end-of-list states accurately and distinctly — each is a
  visually distinct screen, never a blank page or a stale view.

## Declared output

`taskflow/dags/chirp-logged-out-r6/SYNTHESIS.md` — an assessment of each AC (met or not met
and why), the PR URL, the CI status, and any residual concerns worth noting.

## Process

1. **Verify the existing SYNTHESIS.md.** A SYNTHESIS.md already exists at the observation
   seam path. Read it and spot-check its claims against the actual codebase on branch
   `work/chirp-logged-out` (use SSH to the build server or `gh` CLI). If the existing content
   is accurate and complete, it may be re-used as-is or updated minimally.

2. **Re-verify CI.** Run `gh pr checks 263 --repo Nousix-LLC/nswe-demo` to confirm all six CI
   checks (fmt, clippy, test, wasm, doc, image) still pass. Record the current state.

3. **Confirm PR fields.** `Closes #35` must appear in the PR description. The branch must be
   `work/chirp-logged-out`. The PR must be OPEN.

4. **Write (or overwrite) SYNTHESIS.md** at the absolute path
   `/home/user/nousix-runtime/nswe-demo/taskflow/dags/chirp-logged-out-r6/SYNTHESIS.md`
   with final verified content.

5. **Write COMPLETE.md** at your own workspace (`taskflow/dags/chirp-logged-out-r6/SUBTASK_synthesis/COMPLETE.md`)
   summarising what was verified.

6. **Call `engine_resume_suspended`** (the fold) with the parent task ID and seam path as
   specified above under "Parent task ID". This is the LAST action before your terminal
   `report_status { status: "completed" }`.

## Success criteria

- Each AC is assessed with evidence from the actual code on the branch.
- The SYNTHESIS.md is written at the exact path
  `taskflow/dags/chirp-logged-out-r6/SYNTHESIS.md`.
- CI status and PR URL are recorded accurately.
- `engine_resume_suspended` is called with the correct parent task ID and seam path.
- The file contains no host paths, internal addresses, or taskflow-internal references.

## Constraints

- Read evidence from `work/chirp-logged-out` on the remote server (via SSH) or the local
  workspace — do not rely on the summary alone.
- Do not commit or push anything; this is a verification-and-synthesis task only.
- Written for the repository's readers: no host paths, no internal addresses, no taskflow
  references in anything committed or posted to GitHub (SYNTHESIS.md itself is a taskflow
  artifact and is not committed to the repo).

## Suggested Methodology Files

Task type: "Synthesizing / verifying a hub-and-spoke decomposition (contract + wiring + dedup + review gate)"
Primary bundle: Synthesis
Supporting: Code Review, Code Quality

The parent's flagged methodologies based on the task type:
- `synthesis/Synthesis_Overview_Methodology.md` — the four-check model, gate behavior,
  `SYNTHESIS.md` schema, and the fold (engine_resume_suspended) obligation for synthesis tasks.
  **This is mandatory for all synthesis tasks.**
- `synthesis/Synthesis_Contract_Verification_Methodology.md` — verify behavioral contracts.
- `synthesis/Synthesis_Wiring_Verification_Methodology.md` — verify components are wired.

The above are the parent's flagged methodologies based on the task type. The child agent SHOULD
load these as a starting point but is the final judge of what its work requires.

## Inherited Constraints

- Repository: `Nousix-LLC/nswe-demo`
- Branch: `work/chirp-logged-out`
- PR #263 must be OPEN with `Closes #35` and all six CI checks passing
- No commits or pushes — this task is verification only
- No host paths or internal addresses in committed/posted content
