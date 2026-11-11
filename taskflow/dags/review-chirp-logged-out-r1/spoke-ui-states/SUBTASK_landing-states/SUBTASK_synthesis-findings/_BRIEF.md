# _BRIEF.md — SUBTASK_synthesis-findings

## Task Specification

**Slug**: SUBTASK_synthesis-findings
**Task Kind**: synthesis
**Depends on**: SUBTASK_check-ac2, SUBTASK_check-ac3, SUBTASK_check-ac4p
**Status**: Pending

### Objective

This task is the **verification gate** for the SUBTASK_landing-states sub-decomposition.
Read the three concern-findings files produced by the parallel spokes, verify they
collectively satisfy the parent contract's identities, and assemble `FINDINGS.md`
conforming to the parent spoke-ui-states schema (`../../contracts/_MANIFEST.yaml`).

If any identity fails (a concern is missing, a finding lacks a pinned-commit citation,
or the FINDINGS.md schema is not met), schedule a remediation fix-task rather than
silently plugging the gap.

### Context

This task is the synthesis hub in the SUBTASK_landing-states sub-decomposition
(see `../_GLOBAL.md`). It runs after all three concern-checker spokes complete.

**Dependencies**: SUBTASK_check-ac2, SUBTASK_check-ac3, SUBTASK_check-ac4p  
**Dependents**: SUBTASK_synthesis (parent spoke-ui-states synthesis)

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Sub-decomposition hub | `../_GLOBAL.md` | Shared context, task structure |
| Parent hub | `../../_GLOBAL.md` | FINDINGS.md schema and broader context |
| Parent contract | `../../contracts/_MANIFEST.yaml` | FINDINGS.md structural requirements |
| Sub-contract | `../contracts/_MANIFEST.yaml` | Identities to verify |
| AC-2 findings | `../SUBTASK_check-ac2/concern_ac2.md` | AC-2 check output |
| AC-3 findings | `../SUBTASK_check-ac3/concern_ac3.md` | AC-3 check output |
| AC-4p findings | `../SUBTASK_check-ac4p/concern_ac4p.md` | AC-4-partial check output |

---

## Process Specification

This is a **verification gate**, not a prose summary.

### Step 1 — Verify contract identities before assembling

Check the four identities from `../contracts/_MANIFEST.yaml`:

1. **all_concerns_covered**: Do concern_ac2.md, concern_ac3.md, and concern_ac4p.md each
   address their concern? Is any concern missing or only partially addressed?
2. **clean_partition**: Does each file cover exactly its own concern? Is there overlap?
3. **cite_pinned_commit**: Does every finding in every file cite the pinned commit?
4. **schema compliance**: Does each concern file follow the concern_findings_schema structure?

If any identity FAILS: author a remediation fix-task via `engine_amend_plan { add_task }` for
the spoke whose output fails the check. Do NOT silently fix the gap in FINDINGS.md.

### Step 2 — Assemble FINDINGS.md (only if all identities pass)

Assemble FINDINGS.md from the three concern files, following the parent contract schema
(`../../contracts/_MANIFEST.yaml` sections: `concerns_checked`, `findings`, `clean_items`).

```markdown
# Findings — landing-states review

## Concerns checked
- AC-2 (empty_view content and CTA): [one-line summary from concern_ac2.md]
- AC-3 (error state recoverability and role="alert"): [one-line summary from concern_ac3.md]
- AC-4 partial (header_nav in all states): [one-line summary from concern_ac4p.md]

## Findings
[Combined list of all findings from the three files, each with location/principle/rationale/
severity/resolution. If none across all three: "None — all three concerns checked clean."]

## Clean items
[For each concern that passed (or the clean parts of concerns with findings): what was
examined and what was found, citing specific lines]
```

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| Filename | `FINDINGS.md` |
| Location | `../` (parent workspace = SUBTASK_landing-states/) |
| Schema | `../../contracts/_MANIFEST.yaml` |

The synthesis terminal record is `SYNTHESIS.md` at the parent workspace (`../SYNTHESIS.md`).

---

## Success Criteria

- [ ] All four contract identities verified (pass or remediation scheduled)
- [ ] `FINDINGS.md` conforms to `../../contracts/_MANIFEST.yaml` schema
- [ ] All three concerns represented in `concerns_checked` section
- [ ] All findings from all three spokes present with full location/principle/rationale/severity/resolution
- [ ] All clean items from all three spokes present with specific evidence
- [ ] Every location cites `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- [ ] `FINDINGS.md` written to `../` (SUBTASK_landing-states/ workspace)
- [ ] `SYNTHESIS.md` authored at `../SYNTHESIS.md` before terminal report

---

## Suggested Methodology Files

**Task-type row matched**: Synthesizing / verifying a hub-and-spoke decomposition →
Primary: `synthesis`, Supporting: `code-review`

- `synthesis/Synthesis_Overview_Methodology.md` — the four-check model and gate pass/fail decision
- `synthesis/Synthesis_Contract_Verification_Methodology.md` — verify behavioral contracts are wired
- `synthesis/Synthesis_Wiring_Verification_Methodology.md` — verify outputs are connected, no detached work
- `synthesis/Synthesis_Remediation_Methodology.md` — how to schedule fix-tasks when a check fails

These are the parent's flagged suggestions. Load fewer if inapplicable; load more if your
reading of the brief reveals additional needs.

## Inherited Constraints

- Repository: `Nousix-LLC/nswe-demo` only
- Pinned commit: `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- Do not post to the PR
- FINDINGS.md must conform to parent contract schema; do not change its required sections
- Do not silently plug a failed identity — schedule a remediation fix-task instead
- Findings point at repository file paths and lines; never name host paths, private IPs,
  or internal infrastructure details

## Out-of-Scope Methodologies

- `synthesis/Synthesis_Duplication_Detection_Methodology.md` — not applicable; three concern
  checkers cover non-overlapping concerns by design; duplication is verified via clean_partition identity
- Decomposition methodologies — synthesis is reassembly, not decomposition
