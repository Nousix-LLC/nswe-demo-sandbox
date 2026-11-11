# SUBTASK_synthesis: PR Creation and Synthesis Verification Gate

## Task Specification

**Slug**: SUBTASK_synthesis  
**Task Kind**: synthesis  
**Depends on**: SUBTASK_frontend  
**Status**: Pending  
**Assigned To**: swe-coder

### Objective

Verify all five acceptance criteria are met by the combined work of SUBTASK_backend and SUBTASK_frontend, then create one GitHub pull request from `work/chirp-logged-out` into `main` closing issue #35, and produce `SYNTHESIS.md` accounting for each acceptance criterion (met, or not met and why). This is the verification gate for the entire decomposition.

### Context

This task is part of the Chirp Logged-Out Visitor Experience (r8) (see `../_GLOBAL.md`). It is the synthesis gate: it reads the outputs of all prior tasks, verifies the deliverables meet the acceptance criteria, creates the PR, and authors the fold record.

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Project context | `../_GLOBAL.md` | Acceptance criteria, PR requirements |
| Codebase analysis | `../SUBTASK_explore/analysis.md` | What was designed |
| Backend summary | `../SUBTASK_backend/backend_summary.md` | What backend routes were implemented |
| Frontend summary | `../SUBTASK_frontend/frontend_summary.md` | What frontend components and states were implemented |
| Repository | `/home/user/nousix-runtime/nswe-demo` | Actual code to verify |

---

## Process: Verification Gate (Four-Check Model)

This is a verification gate, not a prose summary. Run the four checks over the combined output:

### Check 1: Behavioral Contract Verification
Verify each acceptance criterion against the implemented code:

- **AC-1**: Confirm the public timeline and user profile routes exist and do not require auth tokens.
- **AC-2**: Confirm the empty state shows a "what chirp is" statement + sign-up/sign-in links (not a blank page).
- **AC-3**: Confirm the error state shows a recoverable message (not a broken screen).
- **AC-4**: Confirm "create an account" is visible from the landing and from the sign-in screen and leads to sign-up.
- **AC-5**: Confirm loading, empty, error, and end-of-list states are each visually distinct and never blank/stale.

For each AC: PASS (evidence) or FAIL (what is missing).

### Check 2: Wiring Verification
Verify the backend and frontend are wired to each other:
- The frontend fetch URLs match the backend route URLs
- The response shapes the frontend deserializes match the response shapes the backend serves
- No dead code: every added backend route is used by the frontend (or by tests)

### Check 3: Duplication Detection
Check for any duplicated code or shared dependencies that should be consolidated:
- Chirp/User type definitions: are they in a shared crate or duplicated?
- Serialization/deserialization logic: consistent?

### Check 4: Code Review Gate
Review the combined diff for:
- `cargo fmt --check` clean
- `cargo clippy` clean
- `cargo test` passes (run via SSH if needed)
- `cargo wasm` passes (run via SSH if needed)
- `cargo doc` clean
- `docker build` / image check passes

If any check fails, do NOT open the PR. Instead, record the failure in `SYNTHESIS.md` and report failed status.

### PR Creation (only if all checks PASS)

Create the PR with:
- Title: "feat: logged-out visitor experience (public timeline, profiles, landing states)"
- Body: Must include `Closes #35` as plain text
- Body: Summary of what was implemented covering each AC
- No host paths, internal addresses, or taskflow references

Command: `gh pr create --title "..." --body "..."`

---

## Output Specification

### Primary Output

`SYNTHESIS.md` at the PARENT workspace (`../_GLOBAL.md`'s directory, i.e., `taskflow/dags/chirp-logged-out-r8/SYNTHESIS.md`).

The `SYNTHESIS.md` documents:
```markdown
# SYNTHESIS.md — Chirp Logged-Out Visitor Experience (r8)

## Acceptance Criteria Verification

### AC-1 (REQ-PROD-013): Public timeline and user profiles without auth
Status: PASS / FAIL
Evidence: ...

### AC-2 (REQ-PROD-014): Empty-state landing
Status: PASS / FAIL
Evidence: ...

### AC-3 (REQ-PROD-014): Error state
Status: PASS / FAIL
Evidence: ...

### AC-4 (REQ-PROD-015): Sign-up navigation
Status: PASS / FAIL
Evidence: ...

### AC-5 (REQ-UX-002/030-032): Distinct states
Status: PASS / FAIL
Evidence: ...

## CI Status
- cargo fmt: PASS / FAIL
- cargo clippy: PASS / FAIL
- cargo test: PASS / FAIL
- cargo wasm: PASS / FAIL
- cargo doc: PASS / FAIL
- image build: PASS / FAIL

## PR
- URL: (GitHub PR URL or "not created: [reason]")

## Remediation Required
(List any criteria not met and what would be needed to meet them)
```

---

## Success Criteria

This gate PASSES when:
- [ ] All five ACs verified with evidence
- [ ] Backend/frontend wiring verified (URLs match, shapes match)
- [ ] All CI checks pass
- [ ] PR created with `Closes #35` in the description body
- [ ] `SYNTHESIS.md` written at the parent workspace root with PASS/FAIL for each AC

This gate FAILS when any AC is not met or any CI check fails. In that case:
- [ ] `SYNTHESIS.md` documents exactly what failed and what would need to change
- [ ] The task reports `status: failed` with the gap description

---

## Suggested Methodology Files

**Task-type row matched**: "Synthesizing / verifying a hub-and-spoke decomposition (contract + wiring + dedup + review gate)" → Primary: `synthesis`, Supporting: `code-review`, `code-quality`

Specific files:
- `synthesis/Synthesis_Overview_Methodology.md` — the four-check model, gate pass/fail decision, SYNTHESIS.md schema; rationale: this task IS the verification gate
- `synthesis/Synthesis_Contract_Verification_Methodology.md` — verifying behavioral contracts (ACs) are met; rationale: AC-1 through AC-5 are the contracts this gate checks
- `synthesis/Synthesis_Wiring_Verification_Methodology.md` — verifying backend/frontend are wired (URL/shape alignment); rationale: a core correctness check for this feature
- `synthesis/Synthesis_Code_Review_Methodology.md` — combined output code review including CI gate; rationale: CI must pass before the PR is opened
- `operations/GitWorkflow_PR_Lifecycle_Methodology.md` — gh CLI PR creation; rationale: this task creates the PR

The above are the parent's flagged methodologies. The child agent SHOULD load these as a starting point but is the final judge of what its work requires.

## Inherited Constraints

- `SYNTHESIS.md` must be written at `taskflow/dags/chirp-logged-out-r8/SYNTHESIS.md` (the parent workspace root, NOT in this task's own directory)
- PR description must include `Closes #35` as plain text
- Do NOT open a PR if any AC or CI check fails
- No host paths, internal addresses, or taskflow references in the PR or in SYNTHESIS.md
- The PR is from `work/chirp-logged-out` into `main`
