task_id: chirp-logged-out-r5-synthesis
parent: chirp-logged-out-r5
group: 1
dependencies: [chirp-logged-out-r5-discovery]
launch_agent: swe-coder

# _BRIEF.md — SUBTASK_synthesis

## Objective

Consume the discovery review, resolve any implementation gaps, verify the PR is correct, and write the
parent's `SYNTHESIS.md`. Then fold the suspended parent (`chirp-logged-out-r5`) via `engine_resume_suspended`.

## Context

SUBTASK_discovery has completed and written its review document at:
`taskflow/dags/chirp-logged-out-r5/SUBTASK_discovery/review.md`

That review assesses AC-1 through AC-5 against the implementation on branch `work/chirp-logged-out` and
lists any gaps. The local clone is at `/home/user/nswe-demo/`.

Observed at hub creation time:
- PR #263 OPEN: "feat: logged-out public timeline and user profiles (#35)"
- PR body contains "Closes #35"
- CI checks: fmt ✓, clippy ✓, test ✓, wasm ✓, doc ✓, image ✓

## Scope of this task

1. **Read** `taskflow/dags/chirp-logged-out-r5/SUBTASK_discovery/review.md`
2. **If the review records implementation gaps**: implement the minimum code changes on `work/chirp-logged-out`
   to close each gap, then push and confirm CI still passes. All changes must meet the branch constraints
   (no host paths, no internal addresses, no taskflow references in committed code or PR text).
3. **If the review records no gaps**: no code changes are needed.
4. **Verify the PR**: confirm PR #263 exists, body contains "Closes #35", and all 6 CI checks pass.
5. **Write SYNTHESIS.md** at the declared output path (the parent's workspace root).
6. **Fold the parent**: call `engine_resume_suspended` with:
   - `target_task_id`: `chirp-logged-out-r5`
   - `synthesized_task_id`: `chirp-logged-out-r5-synthesis`
   - `seam_path`: the `SYNTHESIS.md` path you authored

## Declared output

`taskflow/dags/chirp-logged-out-r5/SYNTHESIS.md`

The file must conform to the synthesis_md_identity constraints in
`taskflow/dags/chirp-logged-out-r5/contracts/_MANIFEST.yaml`:
- Address each of AC-1 through AC-5 (met / not met and why)
- Record the final PR URL and confirm "Closes #35" in body
- Record final CI check results (all 6 checks by name)
- Reference the branch name and HEAD commit SHA at time of synthesis

## Success criteria

- `taskflow/dags/chirp-logged-out-r5/SYNTHESIS.md` exists and is complete
- The parent (`chirp-logged-out-r5`) is folded via `engine_resume_suspended`
- PR #263 is mergeable (CI green, "Closes #35" in body, no blocking review comments)
