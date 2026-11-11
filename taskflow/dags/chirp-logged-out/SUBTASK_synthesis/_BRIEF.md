# _BRIEF.md — SUBTASK_synthesis

**Parent:** chirp-logged-out  
**Global hub:** `taskflow/dags/chirp-logged-out/_GLOBAL.md`

## Objective

Verify that the work on `work/chirp-logged-out` is complete, CI-clean, and correctly implements every acceptance criterion from issue #35, then open the one pull request into `main` that closes the issue. Author a `SYNTHESIS.md` that accounts for each acceptance criterion.

## Background

By the time this spoke runs, `SUBTASK_server_public_timeline` and `SUBTASK_frontend_logged_out` will have committed their changes to `work/chirp-logged-out`. This spoke's job is the gate and the delivery:

- Confirm the branch is green (all CI checks pass).
- Confirm each acceptance criterion is met by inspecting the branch's code.
- Open the PR.
- Write `SYNTHESIS.md`.

## Scope

**1. CI verification**  
Push the branch if it has unpushed commits. Confirm all GitHub Actions checks pass: `fmt`, `clippy`, `test`, `wasm`, `doc`, `image`. If any check fails, diagnose and fix it on the branch before opening the PR — do not open a PR on a failing branch.

**2. Acceptance-criterion review**  
For each criterion, determine from the branch's code whether it is met:

- **AC-1:** `GET /api/public/timeline` exists and is unauthenticated; frontend calls it for logged-out session; `GET /api/users/{id}` is unauthenticated.
- **AC-2:** Empty-timeline state renders a "what Chirp is" message and sign-up/sign-in links — not blank.
- **AC-3:** Error state renders a recoverable message with a Retry affordance — not a broken screen.
- **AC-4:** "Create an account" link is visible from the landing and from the sign-in screen and leads to the sign-up flow.
- **AC-5:** Each of loading, empty, error, end-of-list is a visually distinct screen — four distinct renders, never blank or stale.

**3. Pull request**  
Open exactly one PR from `work/chirp-logged-out` into `main` with:
- Title that summarizes the feature (under 70 characters).
- Body that lists the acceptance criteria met, references the design requirements (REQ-PROD-013/014/015, REQ-UX-002/030-032, BAR-011), and contains `Closes #35` as plain text.
- Body ends with the standard attribution line: `🤖 Generated with [Claude Code](https://claude.com/claude-code)`

**4. Post-PR check**  
After opening the PR, confirm the PR URL is recorded and that `Closes #35` appears in the description (view the PR with `gh pr view`).

## Declared outputs

- One open PR from `work/chirp-logged-out` into `main` with `Closes #35` in the description.
- `taskflow/dags/chirp-logged-out/SYNTHESIS.md` — accounts for each acceptance criterion (met / not met and why).
- `COMPLETE.md` in this workspace on completion.

## Success criteria

- The PR is open and links to issue #35 in its description.
- All five acceptance criteria are assessed in `SYNTHESIS.md`.
- All CI checks pass on the branch at the time the PR is opened (or confirmed passing after opening).

## Constraints

- Repository: `Nousix-LLC/nswe-demo`
- Branch: `work/chirp-logged-out`
- Do not force-push to `main`.
- Do not merge the PR — leave it open for review.
- Written for the repository's readers: no host paths, no internal addresses, no taskflow references in anything committed or posted to GitHub.
- The PR description must contain `Closes #35` as plain text in the body.
