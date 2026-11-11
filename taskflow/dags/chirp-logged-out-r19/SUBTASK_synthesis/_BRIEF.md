# _BRIEF.md — SUBTASK_synthesis

## Task Specification

**Slug**: SUBTASK_synthesis  
**Task Kind**: synthesis  
**Depends on**: SUBTASK_ac-verify-remediate  
**Status**: Pending

### Objective

This task is the **verification gate** for the chirp-logged-out-r19 DAG. Read the AC verdicts
produced by SUBTASK_ac-verify-remediate, verify the four contract identities hold, then write
`SYNTHESIS.md` at the DAG root path (`taskflow/dags/chirp-logged-out-r19/SYNTHESIS.md`), and
fold the SUSPENDED parent DAG via `engine_resume_suspended`.

### Context

This synthesis task integrates the verification output of its sole sibling spoke. It runs
the four-check model: ownership coverage, ownership respect, identity assertions, and overall
verdict. See `../_GLOBAL.md` for full project context.

The DAG root (this invocation's parent) is SUSPENDED waiting for this synthesis fold. The
`SYNTHESIS.md` written by this task at the parent's workspace IS the fold record —
both this task's terminal record AND the record `engine_resume_suspended` consumes.

---

## Gate: Four-Check Model

This task MUST run as a verification gate, not a prose summary:

1. **Ownership coverage**: `ac-verdicts.yaml` exists at `../SUBTASK_ac-verify-remediate/ac-verdicts.yaml` and was produced by the correct owner. `SYNTHESIS.md` will be authored by this task.
2. **Ownership respect**: No task wrote to an artifact it doesn't own.
3. **Identity assertions** (from `../contracts/_MANIFEST.yaml`):
   - ac-verdicts.yaml contains all five AC entries (AC-1 through AC-5)
   - Each entry has `verdict: MET | NOT-MET`
   - SYNTHESIS.md will reference each verdict and produce an overall PASS/FAIL
4. **Overall verdict**: PASS if all 5 ACs are MET; FAIL if any AC is NOT-MET (with remediation path noted).

If any identity fails, this task MUST report the failure in SYNTHESIS.md rather than silently plug it.

---

## Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Hub document | `../_GLOBAL.md` | Project context, constraint list |
| Contract manifest | `../contracts/_MANIFEST.yaml` | Ownership + identities to assert |
| Contract schema | `../contracts/ac_verdict_schema.yaml` | Expected ac-verdicts.yaml shape |
| AC verdicts | `../SUBTASK_ac-verify-remediate/ac-verdicts.yaml` | Per-AC verdicts + evidence |

---

## Output Specification

**Primary output**: `SYNTHESIS.md` written at **`taskflow/dags/chirp-logged-out-r19/SYNTHESIS.md`**  
(the DAG ROOT directory, i.e., `../SYNTHESIS.md` relative to this workspace)

This is NOT written to this task's own workspace — it is written to the parent's workspace
so it serves as both the fold record and the overseer's confirmation artifact.

### SYNTHESIS.md Structure

```markdown
# SYNTHESIS.md — chirp-logged-out-r19

**Verdict: PASS | FAIL**

[One-paragraph executive summary]

## Per-AC Status

### AC-1 — [Description]
**Status: MET | NOT-MET**
Evidence: [from ac-verdicts.yaml]

### AC-2 — ...
...

## CI Status

[CI status from ac-verdicts.yaml]

## Commits on Branch

[Any new commits added during gap remediation]

## Disposition

[No code gaps found / gaps fixed and pushed / unresolved gaps blocking merge]
```

---

## Fold Mechanic

After writing `../SYNTHESIS.md`, this task MUST call:
```
engine_resume_suspended(
  target_task_id = <parent DAG root task ID>,
  synthesized_task_id = <this task's ID>,
  seam_path = "<absolute path to ../SYNTHESIS.md>"
)
```

The parent DAG root's task ID can be found in the _FORK.md at `../_FORK.md` field
`owner_id`. The synthesized_task_id is this task's own process ID (available from the
engine's boot confirmation).

Then report terminal: `status=completed, outputs=[../SYNTHESIS.md], artifact_path=../SYNTHESIS.md`.

---

## Success Criteria

- [ ] `../SYNTHESIS.md` exists and contains verdicts for all 5 ACs
- [ ] Overall verdict is PASS or FAIL (not ambiguous)
- [ ] All four contract identity assertions checked; no silent plugs
- [ ] `engine_resume_suspended` called successfully to fold the parent
- [ ] Terminal `status=completed` reported

---

## Suggested Methodology Files

Task-type row matched: "Synthesizing / verifying a hub-and-spoke decomposition" → primary
bundle `synthesis`, supporting `code-review`, `code-quality`.

Suggested files:
- `synthesis/Synthesis_Overview_Methodology.md` — the four-check gate model (always load first)
- `synthesis/Synthesis_Contract_Verification_Methodology.md` — verify contract identities
- `synthesis/Synthesis_Code_Review_Methodology.md` — optional: review combined output quality

The above are the parent's flagged methodologies. The child agent SHOULD load these as a
starting point but is the final judge of what its work requires.

## Inherited Constraints

- Write `SYNTHESIS.md` at the DAG root path (`../SYNTHESIS.md`), not in this workspace
- Do NOT modify `contracts/` or `mocks/` (read-only)
- After writing SYNTHESIS.md, call `engine_resume_suspended` to fold the SUSPENDED parent
