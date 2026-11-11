# Task: Synthesis — Merge Correctness Findings

## Task Specification

**Slug**: SUBTASK_synthesis
**Task Kind**: synthesis
**Depends on**: `SUBTASK_sql-correctness`, `SUBTASK_spec-deviation`
**Status**: Pending

### Objective

Merge the partial findings from both analysis children into a single `FINDINGS.md` at
the `spoke-correctness/` workspace level. This is the artifact the parent `spoke-code-quality`
DAG expects at `spoke-correctness/FINDINGS.md`.

### Context

This task is the synthesis gate for the spoke-correctness subtree. See `../_GLOBAL.md` for
the full task structure. The pinned commit for all file references is
`decb6196c2c1e6ed421d393a642f0c844cc333ba`.

Both analysis children have completed before this task runs. Their partial FINDINGS.md files
are the sole input. This task does not revisit source code or perform additional analysis.

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Hub context | `../_GLOBAL.md` | Task structure, ownership table |
| Contract manifest | `../contracts/_MANIFEST.yaml` | Ownership and identity constraints |
| Output schema | `../../contracts/findings_schema.md` | FINDINGS.md structure |
| SQL findings | `../SUBTASK_sql-correctness/FINDINGS.md` | Partial findings — concern 3 |
| Spec deviation findings | `../SUBTASK_spec-deviation/FINDINGS.md` | Partial findings — concern 4 |

All paths are relative to the `spoke-correctness/` workspace.

---

## Process Specification

1. **Read both partial FINDINGS.md files** in full.

2. **Collect all findings**: Gather every Finding from both files. Renumber them
   consecutively starting at 1 in the merged output (Finding 1, Finding 2, …), preserving
   all fields.

3. **Determine merged Verdict**:
   - If either child's Verdict is `FINDINGS`: merged Verdict = `FINDINGS`
   - If both children's Verdicts are `PASS`: merged Verdict = `PASS`

4. **Merge `## Clean Account`**: Collect all Clean Account bullets from both files. The
   merged Clean Account MUST have exactly two entries, one for concern 3 and one for
   concern 4. Update any Finding references in the bullets to use the renumbered Finding
   numbers.

5. **Write the merged `FINDINGS.md`** at `../FINDINGS.md` (i.e.,
   `spoke-correctness/FINDINGS.md`), conforming to `../../contracts/findings_schema.md`.

6. **Verify** that the merged file:
   - Contains `## Verdict` with exactly one value (PASS or FINDINGS)
   - Contains `## Findings` section with all findings from both children (if Verdict = FINDINGS)
   - Contains `## Clean Account` with exactly two bullets (concern 3 and concern 4)
   - Each finding has Location, Principle at stake, Why it matters, Severity, Satisfying condition
   - All Location fields cite `decb6196c2c1e6ed421d393a642f0c844cc333ba`
   - Prose passes the plain-voice bar

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| Filename | `FINDINGS.md` |
| Format | Markdown |
| Location | `../` relative to this workspace (i.e., `spoke-correctness/FINDINGS.md`) |

This is the final output of the spoke-correctness task. The parent `spoke-code-quality` DAG
reads it at `spoke-correctness/FINDINGS.md`.

---

## Success Criteria

- All findings from both children appear in the merged file, renumbered consecutively
- Merged Verdict reflects the union of both children's verdicts
- `## Clean Account` has exactly two entries covering concerns 3 and 4
- Output conforms to `../../contracts/findings_schema.md`
- No internal host paths, private IPs, or infrastructure details in any finding
- Prose passes the plain-voice bar

---

## Inherited Constraints

- All Location fields must cite pinned commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- Do not post to the PR
- Prose in FINDINGS.md must pass the plain-voice bar in `../../contracts/findings_schema.md`
- Repository: `Nousix-LLC/nswe-demo` only

## Out-of-Scope

- Re-analysis of source code — this task merges existing findings only
- New concerns beyond 3 and 4 — in-scope only for analysis children
