# SUBTASK_mismatch_synthesis — Synthesis Gate: Mismatch Detection + Axum Integration Findings

## Task Specification

**Slug**: SUBTASK_mismatch_synthesis
**Task Kind**: synthesis
**Depends on**: SUBTASK_mismatch_detect, SUBTASK_axum_server
**Status**: Pending

### Objective

This task is the **verification gate** for the SUBTASK_axum_mismatch subtree. It does NOT summarize
the spokes — it verifies that their outputs satisfy the structural contract (`../_MANIFEST.yaml` and
`../../_GLOBAL.md` §Contract), cross-checks the client/server marker format identity, and assembles
the verified findings into `axum_mismatch_findings.md` at the parent workspace (`../`).

If the gate passes: produce `axum_mismatch_findings.md` and `SYNTHESIS.md`, report
`status="completed"`, then fold the SUSPENDED parent (`SUBTASK_axum_mismatch`) via
`engine_resume_suspended`.

If the gate fails (a contract identity is violated, e.g., marker format mismatch): inject a
remediation fix-task via `engine_amend_plan { add_task }`, record the violations in `SYNTHESIS.md`,
and suspend on the fix-task.

### Context

This task is the synthesis gate for `SUBTASK_axum_mismatch`. It inherits the subtree hub at `../_GLOBAL.md`
and the contract at `../contracts/_MANIFEST.yaml`. It reads the two spoke outputs, verifies the identities,
and produces the final combined findings file that `SUBTASK_correctness_synthesis` (parent DAG) will consume.

**Depends on**: `SUBTASK_mismatch_detect` (output: `mismatch_detect_findings.md`),
`SUBTASK_axum_server` (output: `axum_server_findings.md`)
**Dependents**: none within this subtree; `SUBTASK_axum_mismatch` becomes COMPLETED on fold;
`SUBTASK_correctness_synthesis` reads `../axum_mismatch_findings.md`

---

## Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree context | `../_GLOBAL.md` | Scope, success criteria, identity assertions |
| Contract | `../contracts/_MANIFEST.yaml` | Ownership declaration, identity assertions |
| Mismatch detect findings | `../SUBTASK_mismatch_detect/mismatch_detect_findings.md` | REQ-SSR-006 verdict + client-side marker format |
| Axum server findings | `../SUBTASK_axum_server/axum_server_findings.md` | REQ-MIS-001, REQ-MIS-002 verdicts + server-side marker format + REQ-SSR-007 non-goal |

---

## Gate Checks (Four-Check Model)

Run these checks in order. A failure in any check is a gate failure.

### Check 1 — All criteria present

Verify every criterion listed in `../_GLOBAL.md` §Success Criteria has a named verdict in the spoke
outputs:
- REQ-SSR-006 verdict in `mismatch_detect_findings.md`
- REQ-MIS-001 verdict in `axum_server_findings.md`
- REQ-MIS-002 verdict in `axum_server_findings.md`
- REQ-SSR-007 non-goal confirmation in `axum_server_findings.md`

No criterion may be silently omitted. Missing entry = gate failure.

### Check 2 — Marker format cross-check (identity assertion)

The client-side marker format in `mismatch_detect_findings.md` (what the mismatch detection logic
reads from the DOM) MUST agree with the server-side marker format in `axum_server_findings.md`
(what `render_to_string` / the Axum handler writes into the HTML).

If they disagree: this is a FINDING in its own right — the client and server use different marker
schemas, which means hydration would fail on a real mismatch. Record this as a FINDING (BLOCKER) in
`axum_mismatch_findings.md` under a "Cross-check" section.

### Check 3 — Evidence standard

Verify no evidence citation in either spoke uses a host path, taskflow path, or test assertion as a
proxy for behavior. All evidence must be `file:line` in `Nousix-LLC/nswe-demo`.

### Check 4 — Non-goal boundary

Verify REQ-SSR-007 is confirmed as non-goal in `axum_server_findings.md` (not evaluated as deficient).

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| Primary output file | `axum_mismatch_findings.md` |
| Primary output location | parent workspace (`../`, i.e., `SUBTASK_axum_mismatch/`) |
| Terminal record (fold record) | `SYNTHESIS.md` |
| Terminal record location | parent workspace (`../`, i.e., `SUBTASK_axum_mismatch/`) |

**Important**: Both `axum_mismatch_findings.md` and `SYNTHESIS.md` MUST be written at `../` (the
parent workspace, `SUBTASK_axum_mismatch/`), not at this task's workspace. This is the fold-record
pattern: the synthesis task writes to the SUSPENDED parent's directory.

### axum_mismatch_findings.md Structure

Follows the template from the parent brief (`../../_BRIEF.md`):

```markdown
# Mismatch Detection + Axum Integration Findings (REQ-SSR-006, REQ-MIS-001–002)

## Summary
<one paragraph: overall verdict on mismatch detection and Axum integration>

## Findings by Criterion

### REQ-SSR-006 — Mismatch detection
**Status**: CLEAN | FINDING (BLOCKER) | FINDING (NON-BLOCKER)
**What was checked**: ...
**Evidence**: `<file:line>`
**Finding** (if any): ...

### REQ-MIS-001 — Axum handler pattern
**Status**: CLEAN | FINDING (BLOCKER) | FINDING (NON-BLOCKER)
**What was checked**: ...
**Evidence**: `<file:line>`
**Finding** (if any): ...

### REQ-MIS-002 — HTML well-formedness and markers
**Status**: CLEAN | FINDING (BLOCKER) | FINDING (NON-BLOCKER)
**What was checked**: ...
**Evidence**: `<file:line>`
**Finding** (if any): ...

## Non-goal Boundary
### REQ-SSR-007 / #225 — Async resource state (non-goal)
**Status**: CONFIRMED NON-GOAL
**What was checked**: ...
**Evidence**: `<file:line>`

## Cross-check: Marker Format Agreement
**Client-side format** (from SUBTASK_mismatch_detect): <format>
**Server-side format** (from SUBTASK_axum_server): <format>
**Agreement**: MATCHES | MISMATCH (see Finding above)
```

### SYNTHESIS.md Structure

```markdown
# SYNTHESIS — SUBTASK_axum_mismatch Fold Record

## Gate Outcome: PASS | FAIL

## Checks Run

### Check 1 — All criteria present: PASS | FAIL
<what was verified>

### Check 2 — Marker format cross-check: PASS | FAIL
Client: <format>
Server: <format>
Result: MATCHES | MISMATCH

### Check 3 — Evidence standard: PASS | FAIL
<what was verified>

### Check 4 — Non-goal boundary: PASS | FAIL
<what was verified>

## Outputs Produced
- `../axum_mismatch_findings.md` — combined findings for SUBTASK_correctness_synthesis
```

---

## Success Criteria

- [ ] All four gate checks run and recorded in `SYNTHESIS.md`
- [ ] `axum_mismatch_findings.md` written at `../` with all criteria, non-goal, and cross-check
- [ ] `SYNTHESIS.md` written at `../` before terminal `report_status`
- [ ] If gate PASSES: `engine_resume_suspended` called with `target_task_id=SUBTASK_axum_mismatch`,
  `synthesized_task_id=SUBTASK_mismatch_synthesis`, `seam_path=../SYNTHESIS.md`
- [ ] If gate FAILS: a remediation fix-task injected via `engine_amend_plan { add_task }` before
  suspending

---

## Suggested Methodology Files

**Task-type row matched**: "Synthesizing / verifying a hub-and-spoke decomposition" → Primary: `Synthesis`;
Supporting: `Code Review`, `Code Quality`

Specific files:
- `synthesis/Synthesis_Overview_Methodology.md` — the four-check gate model, pass/fail decision, SYNTHESIS.md schema
- `synthesis/Synthesis_Contract_Verification_Methodology.md` — verifying criteria coverage against the contract
- `synthesis/Synthesis_Code_Review_Methodology.md` — code review of the combined output
- `synthesis/Synthesis_Remediation_Methodology.md` — how to inject remediation fix-tasks when the gate fails

The above are the parent's flagged methodologies. The child agent SHOULD load these as a starting point but
is the final judge — load fewer if some are clearly inapplicable; load more if the brief reveals additional
surface.

---

## Inherited Constraints

- **Gate posture**: This task is a verification gate. It runs checks; it does not rewrite the spoke findings.
  When a check fails, it records the failure and injects a fix-task — it does NOT silently plug the failure.
- **Fold obligation**: On gate PASS, MUST call `engine_resume_suspended` to fold the SUSPENDED parent.
  `axum_mismatch_findings.md` exists and is complete before that call.
- **Non-goal**: REQ-SSR-007 is confirmed as non-goal, not remediated
- **Evidence standard**: All findings cite `Nousix-LLC/nswe-demo` file:line, never host/taskflow paths
- **Output location**: Both `axum_mismatch_findings.md` and `SYNTHESIS.md` MUST be written at `../`
  (the SUSPENDED parent's workspace), not in this task's workspace
