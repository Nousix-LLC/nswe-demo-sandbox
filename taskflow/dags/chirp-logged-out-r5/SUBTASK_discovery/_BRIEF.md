task_id: chirp-logged-out-r5-discovery
parent: chirp-logged-out-r5
group: 0
dependencies: []
launch_agent: swe-coder

# _BRIEF.md — SUBTASK_discovery

## Objective

Verify that the implementation on branch `work/chirp-logged-out` in `Nousix-LLC/nswe-demo` satisfies each of
the five acceptance criteria for issue #35. Produce a written review document at the declared output path.

## Context

Branch `work/chirp-logged-out` has 6 commits beyond `main` (top: `908d703 feat(chirp-frontend): logged-out
visitor experience (AC-1–AC-5)`). PR #263 is OPEN. All CI checks (fmt, clippy, test, wasm, doc, image) were
observed PASSING at the time the parent hub was materialized. This task confirms whether the implementation
satisfies each AC in substance — not just that CI is green.

The local clone is at `/home/user/nswe-demo/` on branch `work/chirp-logged-out`.

## Acceptance criteria to verify (from issue #35 / _FORK.md)

- **AC-1 (REQ-PROD-013 / BAR-011):** A logged-out visitor can load the home/public timeline and open a user
  profile and read chirps without being forced to sign up or sign in first.
- **AC-2 (REQ-PROD-014 / BAR-011):** On arrival with no content, the visitor sees a clear statement of what
  Chirp is plus an obvious way to sign up or sign in — never a blank page or an unexplained error.
- **AC-3 (REQ-PROD-014 / BAR-011):** If the timeline fails to load, a clear, recoverable message is shown
  instead of a broken screen.
- **AC-4 (REQ-PROD-015 / BAR-011):** A "create an account" route is visible on the landing and on the
  sign-in screen, and following it reaches sign-up.
- **AC-5 (REQ-UX-002 / REQ-UX-030–032 / BAR-011 / one-state-model criterion):** The logged-out
  landing/timeline renders its loading, empty, error, and end-of-list states accurately and distinctly —
  each state is a visually distinct screen, never a blank page or a stale view.

## Scope of this task

- Read the relevant source files in `/home/user/nswe-demo/crates/chirp-frontend/` and
  `/home/user/nswe-demo/crates/chirp-server/`
- Read the design documents in `/home/user/nswe-demo/design/` for the specific requirements cited in each AC
- For each AC, identify the specific code that satisfies it (or does not) and cite file + line range
- Note the PR number, confirm "Closes #35" is in the PR body, record all CI check results
- List any implementation gaps that would require code changes before the PR can merge

Do NOT make any code changes. Do NOT push to any branch. This task is read-only.

## Declared output

`taskflow/dags/chirp-logged-out-r5/SUBTASK_discovery/review.md`

The review document must conform to the schema in
`taskflow/dags/chirp-logged-out-r5/contracts/_MANIFEST.yaml` (review_md_identity constraints):
- An AC assessment table: AC-1 through AC-5 with status (MET / PARTIAL / UNMET), evidence (file+line), gap
- A PR status section: PR number, "Closes #35" present, CI check results (all 6)
- An implementation gaps section: enumerated items needing code fixes, or "None — all ACs met"

## Success criteria

The declared output file exists and is complete (all 5 ACs assessed, PR status recorded). The parent
SUBTASK_synthesis can consume it to decide the next action.
