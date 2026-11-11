# Task: Synthesis — Compile Review Verdict and Post to PR #193

## Task Specification

**Slug**: SUBTASK_synthesis  
**Task Kind**: synthesis  
**Depends on**: SUBTASK_correctness_concurrency, SUBTASK_quality_tests_idiom, SUBTASK_security  
**Status**: Pending  
**Assigned To**: swe-reviewer

### Objective

This task is the **verification gate** for the review-ferric-async-forms-r3 DAG. Read the three spoke findings files, verify contract identities (all requirements covered, no contradictions), compile a final verdict (APPROVE or REQUEST-CHANGES), write `SYNTHESIS.md` at the DAG root (`../SYNTHESIS.md` relative to this workspace), and post the review findings to PR #193 as a GitHub review comment.

---

## Context

See `../_GLOBAL.md` for full project context, acceptance criteria, ownership manifest, and identities.

**Spoke findings files (inputs to this task):**
- `../SUBTASK_correctness_concurrency/findings.md`
- `../SUBTASK_quality_tests_idiom/findings.md`
- `../SUBTASK_security/findings.md`

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Project context | `../_GLOBAL.md` | Acceptance criteria, identities, scope |
| Contract manifest | `../contracts/_MANIFEST.yaml` | Ownership and identities to verify |
| Correctness/concurrency findings | `../SUBTASK_correctness_concurrency/findings.md` | B1/B2/B3 correctness + async hazard results |
| Quality/tests/idiom findings | `../SUBTASK_quality_tests_idiom/findings.md` | Code quality, test depth, idiom, API stability results |
| Security findings | `../SUBTASK_security/findings.md` | Security pass results |

---

## Synthesis Process

This task runs the **four-check verification gate** over the combined spoke outputs:

1. **Contract verification**: Confirm every requirement in scope (REQ-ASYNC-001, 003, 005, 016, 023, 042) appears in at least one spoke's findings. No requirement may be silently uncovered.

2. **Wiring verification**: Confirm the three spoke findings are mutually consistent. Flag any contradiction (e.g., one spoke says B2 is clean, another says it's broken) and resolve it by re-reading the source code if needed.

3. **Duplication detection**: Check whether the same finding is raised by multiple spokes. Consolidate duplicates into a single finding with the most precise location.

4. **Code review compilation**: Compile the final verdict:
   - If ANY spoke finding has `severity: blocker` → verdict is `REQUEST-CHANGES`; list each blocker with its requirement ID, location, and what would satisfy it
   - If NO blocker findings → verdict is `APPROVE`; confirm B1, B2, B3 are resolved and all acceptance criteria satisfied
   - For non-blocker findings: file each as a new GitHub issue (do NOT re-file issues #196–#201); list the new issue numbers in SYNTHESIS.md

**Posting the review to PR #193:**
- Use `gh pr review 193 --repo Nousix-LLC/nswe-demo` to post a review
- If APPROVE: `--approve` with a body summarizing the findings
- If REQUEST-CHANGES: `--request-changes` with a body listing each blocker
- The review body must use repository-relative file paths only; no internal host paths, taskflow paths, or infrastructure addresses
- Do not reference the escalation comment from overseer I220

---

## Output Specification

**Primary Output:** `SYNTHESIS.md` at the DAG root — `../SYNTHESIS.md` relative to this task workspace (absolute: `/home/user/nousix-runtime/nswe-demo/taskflow/dags/review-ferric-async-forms-r3/SYNTHESIS.md`)

The SYNTHESIS.md MUST contain:
- Verdict: `APPROVE` or `REQUEST-CHANGES`
- If APPROVE: confirmation that B1, B2, B3 are resolved; all acceptance criteria satisfied; CI green; PR #193 ready to land; any new non-blocker issues filed (with numbers)
- If REQUEST-CHANGES: each remaining blocker named against its REQ-ASYNC-NNN requirement ID; severity and blocking status for every finding; non-blockers filed as new issues (with numbers)
- Summary of what each spoke examined and found (or did not find)
- Confirmation that the review was posted to PR #193 (with PR review URL/ID if available)

**Complete the terminal lifecycle:**
After writing SYNTHESIS.md at `../SYNTHESIS.md`, call:
- `engine_report_status { status: "completed", decompose_evaluation: "Atomic", outputs: ["../SYNTHESIS.md"], artifact_path: "../SYNTHESIS.md" }`
- Then `engine_resume_suspended` to fold the SUSPENDED parent (this DAG's root task) to COMPLETED

---

## Suggested Methodology Files

Task type row (Domain Mapping): **Synthesizing / verifying a hub-and-spoke decomposition** → Primary: `synthesis`, Supporting: `code-review`, `code-quality`

Specific files to load:
- `synthesis/Synthesis_Overview_Methodology.md` — the four-check model (anchor; always load first)
- `synthesis/Synthesis_Code_Review_Methodology.md` — how to compile a code review verdict from spoke findings
- `synthesis/Synthesis_Contract_Verification_Methodology.md` — verify requirements coverage identities
- `synthesis/Synthesis_Wiring_Verification_Methodology.md` — verify consistency across spoke outputs
- `code-review/CodeReview_Feedback_Guidelines_Methodology.md` — writing constructive, actionable review text
- `operations/GitWorkflow_Syscall_PR_Review_Methodology.md` — posting a review via `gh pr review`

These are SUGGESTIONS. Load fewer if some are clearly inapplicable.

## Inherited Constraints

- `SYNTHESIS.md` must be authored at the DAG ROOT (`../SYNTHESIS.md`), not at this task's workspace — this is the fold location
- Repository-relative paths only in posted review text
- Do not re-raise issues #196–#201; file new issues for any new non-blockers
- Do not reference or re-raise the escalation comment from overseer I220 (PR #193 comment 6624409600)
- The review text posted to GitHub must read as the repository's own (plain voice, no AI-writing tells)

## Out-of-Scope Methodologies

- `synthesis/Synthesis_Duplication_Detection_Methodology.md` — not needed; the three spokes cover distinct concern areas with minimal overlap
- `synthesis/Synthesis_Remediation_Methodology.md` — only needed if blocker findings require decomposed fix-tasks; load if blockers are found

## Success Criteria

- Contract identities verified (all REQ-ASYNC-NNN requirements covered)
- Wiring consistency confirmed (no contradictions across spokes)
- Verdict determined and justified with evidence from spoke findings
- `SYNTHESIS.md` authored at the DAG root with complete content
- Review posted to PR #193 via `gh pr review`
- Terminal lifecycle complete (engine_report_status + engine_resume_suspended)
