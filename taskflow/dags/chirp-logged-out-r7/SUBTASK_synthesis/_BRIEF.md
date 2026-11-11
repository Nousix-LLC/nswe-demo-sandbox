# Task: Synthesis — PR Creation and AC Verification

## Task Specification

**Slug**: SUBTASK_synthesis  
**Task Kind**: synthesis  
**Depends on**: SUBTASK_frontend-ui  
**Status**: Pending  
**Assigned To**: swe-coder

### Objective

This task is a **verification gate**. It verifies that the combined implementation from SUBTASK_explore-codebase, SUBTASK_backend-api, and SUBTASK_frontend-ui collectively satisfies all five acceptance criteria from issue #35. It then creates a GitHub PR closing issue #35, and authors the root `SYNTHESIS.md` accounting for each AC as "met" or "not met and why".

The gate either PASSES (all ACs met, PR created, SYNTHESIS.md authored) or FAILs (one or more ACs not met, documented with remediation path in SYNTHESIS.md).

### Context

This task is part of Chirp Logged-Out Visitor Experience r7 (see `../_GLOBAL.md` for full context, ACs, and constraints).

**Dependencies**: SUBTASK_frontend-ui (which depends on the full chain: explore → backend → frontend)  
**Dependents**: none (this is the final task)

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Parent hub | `../_GLOBAL.md` | ACs, constraints, PR requirements |
| Analysis | `../SUBTASK_explore-codebase/analysis.md` | Original gap analysis (baseline) |
| Backend impl | `../SUBTASK_backend-api/backend-impl.md` | Endpoints implemented, test coverage |
| Frontend impl | `../SUBTASK_frontend-ui/frontend-impl.md` | UI states implemented, test coverage |
| Contracts | `../contracts/_MANIFEST.yaml`, `../contracts/public_api_contract.md` | Identities to verify |
| Repository | branch `work/chirp-logged-out` | Live code to inspect if needed |

---

## Verification Gate: Four Checks

This task MUST run these four checks in order:

**Check 1 — Behavioral Contract Verification**: For each AC (AC-1 through AC-5), verify the implementation satisfies it. Use backend-impl.md and frontend-impl.md as evidence. Mark each AC as PASS or FAIL with supporting rationale.

**Check 2 — Wiring Verification**: Verify that:
- The frontend calls only the endpoints declared in backend-impl.md (identity: api_coverage)
- Every AC is covered by at least one implementation artifact (identity: ac_coverage)
- No AC is addressed by the analysis.md alone without a corresponding implementation

**Check 3 — Duplication Detection**: Check for any duplicated concerns — e.g., a public endpoint added in both a new and existing route family, or state handling logic duplicated across components.

**Check 4 — Code Review**: Verify that code quality gates pass: `cargo fmt --check`, `cargo clippy`, `cargo test`, WASM build. These are the CI checks the PR must pass.

**Gate Decision**: If all four checks PASS, create the PR and author SYNTHESIS.md with status "completed". If any check FAILS, document the failure in SYNTHESIS.md and do not create the PR until remediation is possible (or document what cannot be remediated in this scope).

---

## Output Specification

### Primary Output: `SYNTHESIS.md` at the parent workspace root

| Attribute | Value |
|-----------|-------|
| Filename | `SYNTHESIS.md` |
| Location | `../` (parent workspace: `taskflow/dags/chirp-logged-out-r7/`) |

`SYNTHESIS.md` MUST include:

1. **Per-AC Verdict**: For each of AC-1 through AC-5, a verdict of "met" (with evidence) or "not met" (with explanation)
2. **Four-Check Results**: Summary of each check's pass/fail
3. **PR URL**: The GitHub PR URL, or "PR not created — see failures below" if the gate did not pass
4. **Contract Identity Verification**: Explicit statement on api_coverage, ac_coverage, ci_pass identities
5. **Remediation Items** (if any): Any ACs not met, with specific remediation steps

### Secondary Output: GitHub PR

A PR on `Nousix-LLC/nswe-demo` from `work/chirp-logged-out` into `main`:
- Title: descriptive, under 70 characters
- Body: summary of changes, closes issue, plus `Closes #35` as plain text
- Body ends with: `🤖 Generated with [Claude Code](https://claude.com/claude-code)`

---

## Success Criteria (Gate PASS conditions)

- [ ] All five ACs verified as met with evidence from backend-impl.md and frontend-impl.md
- [ ] api_coverage identity: every frontend API call maps to a declared backend endpoint
- [ ] ac_coverage identity: every AC has an implementation artifact
- [ ] ci_pass identity: CI checks pass (or documentation of a known failure with remediation plan)
- [ ] PR created with `Closes #35` in the plain-text description body
- [ ] `SYNTHESIS.md` at `taskflow/dags/chirp-logged-out-r7/SYNTHESIS.md` exists and covers every AC

---

## Suggested Methodology Files

**Task-type row matched**: "Synthesizing / verifying a hub-and-spoke decomposition" → Synthesis; "PR creation and management via gh CLI" → Operations

**Primary files to load**:
- `synthesis/Synthesis_Overview_Methodology.md` — rationale: anchor file for all synthesis tasks; defines the four-check model, gate pass/fail decision, and SYNTHESIS.md schema this task MUST follow
- `synthesis/Synthesis_Contract_Verification_Methodology.md` — rationale: the _MANIFEST.yaml declares three identities (api_coverage, ac_coverage, ci_pass) that must be verified against the combined output
- `synthesis/Synthesis_Wiring_Verification_Methodology.md` — rationale: verifying that the frontend's API calls wire to the backend's declared endpoints
- `operations/GitWorkflow_PR_Lifecycle_Methodology.md` — rationale: PR creation via `gh pr create`, proper description format, `Closes #35` syntax

**Supporting files** (load if the approach reveals a need):
- `synthesis/Synthesis_Code_Review_Methodology.md` — if code quality review beyond CI gates is warranted
- `synthesis/Synthesis_Remediation_Methodology.md` — if any check fails and remediation sub-tasks need to be scheduled

These are the parent's flagged methodologies. The child agent SHOULD load these as a starting point but is the final judge of what its work requires.

## Inherited Constraints

- Branch: `work/chirp-logged-out`; PR: `work/chirp-logged-out` → `main`
- Repository: `Nousix-LLC/nswe-demo`
- PR description MUST contain `Closes #35` as plain text in the body
- PR description MUST NOT contain host paths, internal addresses, or taskflow references
- PR description MUST end with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`
- `SYNTHESIS.md` MUST be at `taskflow/dags/chirp-logged-out-r7/SYNTHESIS.md` (the parent workspace root, not this task's workspace)
- No force-push to `main`
- Gate decision is binary: either all ACs are met and PR is created, or the SYNTHESIS.md documents what is not met and why

## Out-of-Scope Methodologies

- Writing new Rust code — all implementation is owned by SUBTASK_backend-api and SUBTASK_frontend-ui
- Decomposition methodologies — synthesis is the reassembly, not the split
