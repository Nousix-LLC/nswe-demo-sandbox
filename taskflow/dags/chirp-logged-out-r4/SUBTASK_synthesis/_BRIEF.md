# Task: Synthesis Gate — Commit, PR, CI Verification, SYNTHESIS.md

## Task Specification

**Slug**: SUBTASK_synthesis
**Task Kind**: synthesis
**Depends on**: SUBTASK_backend, SUBTASK_frontend
**Status**: Pending
**Assigned To**: swe-coder

### Objective

This is the **verification gate** for the chirp-logged-out-r4 subtree. It does NOT simply
summarize — it verifies that the combined output of SUBTASK_backend and SUBTASK_frontend
satisfies all five acceptance criteria, checks that CI-equivalent quality gates pass, creates
the git commit(s) on `work/chirp-logged-out`, opens the GitHub PR closing issue #35, and
authors `SYNTHESIS.md` as a fold record for the subtree parent.

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `taskflow/dags/chirp-logged-out-r4/_GLOBAL.md` | Acceptance criteria and constraints |
| Ownership manifest | `taskflow/dags/chirp-logged-out-r4/contracts/_MANIFEST.yaml` | Identity assertions to verify |
| API spec | `taskflow/dags/chirp-logged-out-r4/contracts/public_api_spec.md` | Contract to verify was followed |
| Backend completion record | `taskflow/dags/chirp-logged-out-r4/SUBTASK_backend/COMPLETE.md` | Backend output summary |
| Frontend completion record | `taskflow/dags/chirp-logged-out-r4/SUBTASK_frontend/COMPLETE.md` | Frontend output summary |
| Exploration analysis | `taskflow/dags/chirp-logged-out-r4/SUBTASK_explore_and_setup/analysis.md` | Branch status, context |

### Input Verification

Before processing:
- [ ] `SUBTASK_backend/COMPLETE.md` exists
- [ ] `SUBTASK_frontend/COMPLETE.md` exists
- [ ] `crates/chirp-server/` has the new route files
- [ ] `crates/chirp-frontend/` has the new component files

---

## Process Specification

### Check 1 — Wiring Verification

Verify the backend and frontend are correctly connected per the ownership manifest:
- [ ] `GET /api/chirps` route exists in chirp-server without an auth requirement
- [ ] `GET /api/users/:username/chirps` route exists in chirp-server without an auth requirement
- [ ] The home/landing route is registered in chirp-frontend's router
- [ ] The user profile route is registered in chirp-frontend's router
- [ ] Sign-in and sign-up navigation links are present in the landing component

If a wiring violation is found: inject a fix-task via `engine_amend_plan { add_task }`, record
the violation in SYNTHESIS.md, and do NOT silently reconcile it inline.

### Check 2 — Contract Verification

Verify both spokes composed against `contracts/public_api_spec.md`:
- [ ] Backend response shape matches the spec (Rust structs or serde serialization matches)
- [ ] Frontend deserialization structs match the spec shapes
- [ ] The five frontend states (loading, empty, error, loaded, end-of-list) each have a distinct implementation

If a contract violation is found: inject a fix-task, record in SYNTHESIS.md.

### Check 3 — Acceptance Criteria Verification

For each AC from the _GLOBAL.md:
- [ ] **AC-1**: The public timeline and user profile routes require no authentication — verify by reading the route handler code (no auth extractor that returns 401, or uses optional auth)
- [ ] **AC-2**: The empty state renders a "what is chirp" statement AND sign-up/sign-in links
- [ ] **AC-3**: The error state renders a recoverable message (not blank)
- [ ] **AC-4**: "Create an account" link is reachable from landing and sign-in screen
- [ ] **AC-5**: Loading, empty, error, and end-of-list states are each visually distinct

Record each as PASS or FAIL with evidence.

### Check 4 — CI Quality Gates

Run the following checks via SSH to the build server (see CLAUDE.md for the SSH pattern):

```bash
# From the build server, on branch work/chirp-logged-out
cargo fmt --check
cargo clippy -- -D warnings
cargo test
# If WASM tests exist:
# wasm-pack test --headless crates/chirp-frontend
```

**SSH command pattern** (from CLAUDE.md):
```bash
ssh -i ~/.ssh/nousix_server_ed25519 -o IdentitiesOnly=yes -o BatchMode=yes mattm@100.90.75.93 \
  'bash -lc "cd <repo-path> && git checkout work/chirp-logged-out && cargo fmt --check"'
```

The repo path on the build server may differ — check the existing CI configuration or the
server's filesystem if the path is not obvious. If the CI checks cannot be run (server
unavailable, path unknown), document this in SYNTHESIS.md and proceed.

Record the result of each check: PASS / FAIL / SKIPPED (with reason).

### Git and PR Operations

After all checks pass (or are documented):

1. Stage all modified files in `crates/chirp-server/` and `crates/chirp-frontend/`:
   ```bash
   git add crates/chirp-server/ crates/chirp-frontend/
   ```
2. Commit with a clear message (do NOT include host paths, internal addresses, or taskflow refs):
   ```
   feat: add logged-out public timeline and user profile
   
   Implements the logged-out visitor experience per issue #35:
   - Public GET /api/chirps endpoint (no auth required)
   - Public GET /api/users/:username/chirps endpoint (no auth required)  
   - Home/landing route with loading, empty, error, end-of-list states
   - Public user profile view
   - Sign-up and sign-in navigation from the landing
   
   Closes #35
   
   Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
   ```
3. Push to origin:
   ```bash
   git push origin work/chirp-logged-out
   ```
4. Create a GitHub PR:
   ```bash
   gh pr create \
     --title "feat: logged-out public timeline and user profiles (#35)" \
     --body "$(cat <<'EOF'
   ## Summary
   
   Implements the logged-out visitor experience for Chirp (issue #35):
   
   - **Public timeline** (`GET /api/chirps`): unauthenticated access to the public feed with loading, empty, error, and end-of-list states
   - **Public user profiles** (`GET /api/users/:username/chirps`): unauthenticated user chirp feeds
   - **Frontend landing**: home route with accurate state handling, sign-up/sign-in navigation always visible
   - **Tests**: unit and integration tests for API endpoints; component tests for each distinct UI state
   
   Closes #35
   
   ## Test plan
   - [ ] `cargo fmt --check` passes
   - [ ] `cargo clippy -- -D warnings` passes
   - [ ] `cargo test` passes (server and frontend unit tests)
   - [ ] Wasm tests pass for frontend state components
   - [ ] Visiting `/` without auth shows public timeline (or empty state with sign-up prompt)
   - [ ] Visiting `/users/:username` without auth shows public profile
   - [ ] Error state shows recoverable message
   - [ ] Sign-up link visible from landing
   
   🤖 Generated with [Claude Code](https://claude.com/claude-code)
   EOF
   )" \
     --base main \
     --head work/chirp-logged-out
   ```

### Duplicate Detection

Scan for any shared logic that was implemented twice (once in backend, once in frontend) that
should instead be a shared type or utility. Record any significant duplications in SYNTHESIS.md.

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| Filename | `SYNTHESIS.md` |
| Location | `taskflow/dags/chirp-logged-out-r4/` |

The SYNTHESIS.md MUST contain:

```markdown
# SYNTHESIS — Chirp Logged-Out Experience

## Verification Gate Results

### Check 1 — Wiring Verification
- GET /api/chirps: PASS/FAIL
- GET /api/users/:username/chirps: PASS/FAIL
- Home route registered: PASS/FAIL
- User profile route registered: PASS/FAIL
- Sign-up/sign-in navigation: PASS/FAIL

### Check 2 — Contract Verification
- Backend matches spec: PASS/FAIL
- Frontend matches spec: PASS/FAIL
- Five states implemented distinctly: PASS/FAIL

### Check 3 — Acceptance Criteria
- AC-1 (no auth required): PASS/FAIL
- AC-2 (empty state with sign-up): PASS/FAIL
- AC-3 (error state recoverable): PASS/FAIL
- AC-4 (create account visible): PASS/FAIL
- AC-5 (states visually distinct): PASS/FAIL

### Check 4 — CI Quality Gates
- cargo fmt --check: PASS/FAIL/SKIPPED
- cargo clippy: PASS/FAIL/SKIPPED
- cargo test: PASS/FAIL/SKIPPED
- wasm tests: PASS/FAIL/SKIPPED

## Gate Verdict: PASS / FAIL

## PR URL
<URL>

## Injected Fix-Tasks (if any)
<List of fix tasks added, or "none">

## Duplications Detected
<Any significant shared logic duplication, or "none">
```

---

## Success Criteria

This gate task is complete when:
- [ ] All four checks have been run and results documented
- [ ] Gate verdict is PASS (or fix-tasks have been injected for FAIL items)
- [ ] Git commit(s) pushed to `work/chirp-logged-out`
- [ ] PR is open on GitHub closing issue #35
- [ ] SYNTHESIS.md is written at `taskflow/dags/chirp-logged-out-r4/SYNTHESIS.md`
- [ ] `engine_resume_suspended` called to fold the parent (the r4 root task)

---

## Suggested Methodology Files

**Task-type rows matched:**
- "Synthesizing / verifying a hub-and-spoke decomposition" — Primary: `synthesis`, Supporting: `code-review`, `code-quality`
- "PR creation and management via gh CLI" — Primary: `operations`, Supporting: `code-review`
- "Git workflow / branch management" — Primary: `operations`, Supporting: `code-review`

**Specific files:**
- `synthesis/Synthesis_Overview_Methodology.md` — Rationale: this IS a synthesis/verification gate task. Load first.
- `synthesis/Synthesis_Contract_Verification_Methodology.md` — Rationale: verify both spokes composed against the frozen API spec.
- `synthesis/Synthesis_Wiring_Verification_Methodology.md` — Rationale: verify backend routes and frontend components are correctly wired.
- `synthesis/Synthesis_Code_Review_Methodology.md` — Rationale: combined code review of the full output.
- `operations/GitWorkflow_PR_Lifecycle_Methodology.md` — Rationale: committing and creating the PR.

**These are SUGGESTIONS.** The child agent is the final judge.

## Inherited Constraints

- Write `SYNTHESIS.md` at `taskflow/dags/chirp-logged-out-r4/SYNTHESIS.md` (the FOLD LOCATION — the suspended parent's directory)
- After writing SYNTHESIS.md, call `engine_resume_suspended` to fold the parent:
  ```
  target_task_id: <the chirp-logged-out-r4 root process id>
  synthesized_task_id: <this task's id>
  seam_path: taskflow/dags/chirp-logged-out-r4/SYNTHESIS.md
  ```
  The parent process id is in the _FORK.md at `taskflow/dags/chirp-logged-out-r4/_FORK.md`
  (look for `owner_id`).
- Do NOT put host paths, internal addresses, SSH key paths, or taskflow references in anything committed to GitHub
- Do NOT force-push to main
- If a CI check fails and cannot be fixed inline, inject a fix-task and report the FAIL — do not block indefinitely

## Out-of-Scope Methodologies

- `synthesis/Synthesis_Duplication_Detection_Methodology.md` — may load if significant duplication is found, but keep the check lightweight
- `rust/` bundle — the synthesis gate reads and verifies code; it does not write new Rust features
