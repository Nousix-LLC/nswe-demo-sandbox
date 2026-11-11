# _BRIEF.md — SUBTASK_synthesis

## Objective

This task is a **verification gate**. Its job is NOT to write a prose summary — it is to
verify that the combined output of SUBTASK_server and SUBTASK_frontend satisfies all five
acceptance criteria for GitHub issue #35, check that all CI quality gates pass, create the
pull request into `main` closing issue #35, and author the root `SYNTHESIS.md` recording
the gate verdict.

## Context

**Repository:** `Nousix-LLC/nswe-demo`  
**Branch:** `work/chirp-logged-out` (commits from both SUBTASK_server and SUBTASK_frontend)  
**Issue:** #35 — "Logged-out reading and a useful landing with accurate states"  
**CI checks required to pass:** `fmt`, `clippy`, `test`, `wasm`, `doc`, `image`

## Declared outputs

- Root `SYNTHESIS.md` at `taskflow/dags/chirp-logged-out-r2/SYNTHESIS.md` — gate verdict recording each AC as met/not-met
- One PR into `main` with `Closes #35` as plain text in the description body
- If any AC is not met: specific failure recorded in `SYNTHESIS.md`; fix-task injected if remediable

## Process — four-check verification gate

Run these four checks over the combined output of both spokes before creating the PR:

**Check 1 — Behavioral contract / AC verification**  
For each acceptance criterion, verify the code satisfies it:

- AC-1 (REQ-PROD-013): `GET /api/public/timeline` exists and returns HTTP 200 without auth. Confirm the route is registered in `router.rs`, the handler has no `AuthUser` extractor, and an integration test covers this.
- AC-2 (REQ-PROD-014): `empty_view()` in `timeline.rs` shows a "what Chirp is" statement AND Sign up and Sign in controls — not a blank page or "No chirps yet." only.
- AC-3 (REQ-PROD-014): The timeline error path in `timeline.rs` renders a human-readable recoverable error message rather than a blank page. Verify the error state arm of the state machine displays something.
- AC-4 (REQ-PROD-015): "Create account" / Sign up control is visible in the nav bar (in `app.rs`) and in the empty state (in `timeline.rs`). Verify both surfaces.
- AC-5 (REQ-UX-002/030-032): The state machine has distinct arms for loading, empty, error, and end-of-list — none silently collapses to a blank page or stale view.

**Check 2 — Wiring verification**  
Verify the composition is correctly wired end-to-end:

- `timeline_view` calls `pub_timeline` (not `timeline`) for both initial load and load-more
- `pub_timeline` on `ApiClient` calls `GET /public/timeline` (no `/api/` prefix — the base URL already includes `/api`)
- The route in `router.rs` maps to the correct handler (`public_timeline_handler`)
- `chirp_item` renders the author as a link to `/user/{author_id}` (not plain text)
- Sign up / Sign in nav links are present in `nav_bar()` in `app.rs`

**Check 3 — CI gates**  
Run the CI checks over `work/chirp-logged-out` via SSH. All of the following must pass:
- `cargo fmt --check` (workspace)
- `cargo clippy -- -D warnings` (workspace)
- `cargo test` (workspace, including chirp-server integration tests)
- `cargo build --target wasm32-unknown-unknown -p chirp-frontend` (the `wasm` check)
- `cargo doc --no-deps` (the `doc` check)
- Docker image build if the CI `image` check runs a local build

If any check fails: record the failure in `SYNTHESIS.md` and do NOT create the PR until it
is fixed. Fix formatting/clippy issues directly; for deeper issues, record and report.

**Check 4 — Code review**  
Scan the combined diff for:
- Security: no host addresses, SSH key paths, internal addresses, or taskflow references in committed files
- No unintended changes to authenticated endpoints or session management
- No dead code introduced (unused imports, unused methods)
- The public timeline implementation does not accidentally expose private/deleted chirps if the data model has such a concept (verify the SQL or in-memory query scope is correct)

## Success criteria (gate pass conditions)

The gate PASSES when ALL of the following hold:

- [ ] All five ACs verified as met by code inspection
- [ ] Wiring verified end-to-end (all five wiring checks above pass)
- [ ] All CI checks pass (fmt, clippy, test, wasm, doc, image)
- [ ] Code review finds no security, correctness, or dead-code violations
- [ ] PR created into `main` with `Closes #35` in the description body
- [ ] Root `SYNTHESIS.md` authored recording each AC as met

The gate FAILS (and fixes must be applied before the PR is created) when:
- Any AC is not met by the current code
- Any CI check fails
- Security content found in committed files

## Constraints (inherited from parent hub)

- **Security**: The PR description MUST NOT contain any host address, SSH key path, username, or host path. Only repository-level content in the PR.
- **PR attribution**: End the PR description body with:
  ```
  🤖 Generated with [Claude Code](https://claude.com/claude-code)
  ```
- **Commit attribution**: Confirm that all commits on `work/chirp-logged-out` end with:
  ```
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
  ```
- **No force-push to main**: Use `gh pr create` to target `main`; do not push directly to main.
- **SSH for cluster commands**: kubectl / helm commands use SSH pattern from CLAUDE.md; do not embed SSH details in any committed artifact.

## Suggested Methodology Files

Domain mapping row matched: **"Synthesizing / verifying a hub-and-spoke decomposition"** →
primary bundle `Synthesis`, supporting bundles `Code Review`, `Code Quality`.

**Primary (gate posture — load first):**
- `synthesis/Synthesis_Overview_Methodology.md` — the four-check model, gate pass/fail decision, `SYNTHESIS.md` schema. This is the anchor for this task's execution.
- `synthesis/Synthesis_Contract_Verification_Methodology.md` — verifying the five ACs against the contracts/_MANIFEST.yaml identities.
- `synthesis/Synthesis_Wiring_Verification_Methodology.md` — verifying that every spoke output is correctly wired (pub_timeline called, route registered, nav links present).
- `synthesis/Synthesis_Code_Review_Methodology.md` — combined code review over the full diff (security, correctness, dead code, fmt/clippy mechanical floor).

**Supporting:**
- `code-review/CodeReview_PR_Authoring_Methodology.md` — PR description format, `Closes #35` placement, description quality for a small focused PR.

The above are the parent's flagged methodologies based on the task type. The child agent SHOULD load these as a starting point but is the final judge of what its work requires.

## Out-of-Scope Methodologies

- `rust/Rust_Web_Services_Axum_Methodology.md` — server implementation is complete; this task only verifies it
- `decomposition/` bundle — decomposition is the parent's concern; synthesis is the reassembly
