# _BRIEF.md — SUBTASK_findings-synthesis

## Task Specification

**Slug**: SUBTASK_findings-synthesis  
**Task Kind**: synthesis  
**Depends on**: SUBTASK_completeness-review, SUBTASK_release-bar-quality, SUBTASK_traceability-review  
**Status**: Pending

### Objective

Read the three spoke findings files. Verify that each satisfies the identities declared in `contracts/_MANIFEST.yaml`. Merge all findings into a single output file, `../design-doc-findings.md`, conforming to the ancestor hub's `contracts/findings_schema.yaml`. Record any verification failures with evidence.

This task is the synthesis gate for the design-doc-review subtree: it reconciles the siblings' combined output and asserts the subtree identities before producing the deliverable.

### Context

This task is part of the design-doc-review subtree (see `_GLOBAL.md` in the parent workspace at `taskflow/dags/design-ferric-1_0-r3/SUBTASK_design-doc-review/`).

The three spokes address concerns 1, 2, and 3 independently. This task integrates their outputs. The final file at `../design-doc-findings.md` is what SUBTASK_synthesis (the parent-level synthesis) reads.

**Depends on**: SUBTASK_completeness-review (completeness-findings.yaml), SUBTASK_release-bar-quality (release-bar-findings.yaml), SUBTASK_traceability-review (traceability-findings.yaml)  
**Dependents**: SUBTASK_synthesis (parent level) depends on `../design-doc-findings.md`

---

## Inputs

| Input | Source | Purpose |
|---|---|---|
| Parent hub (design-doc-review) | `taskflow/dags/design-ferric-1_0-r3/SUBTASK_design-doc-review/_GLOBAL.md` | Identities to assert |
| Contract manifest | `taskflow/dags/design-ferric-1_0-r3/SUBTASK_design-doc-review/contracts/_MANIFEST.yaml` | Identities and ownership to verify |
| Spoke findings schema | `taskflow/dags/design-ferric-1_0-r3/SUBTASK_design-doc-review/contracts/spoke_findings_schema.yaml` | Format each spoke output must conform to |
| Ancestor findings schema | `taskflow/dags/design-ferric-1_0-r3/contracts/findings_schema.yaml` | Format the final output must conform to |
| Completeness findings | `taskflow/dags/design-ferric-1_0-r3/SUBTASK_design-doc-review/SUBTASK_completeness-review/completeness-findings.yaml` | Concern 1 findings |
| Release bar findings | `taskflow/dags/design-ferric-1_0-r3/SUBTASK_design-doc-review/SUBTASK_release-bar-quality/release-bar-findings.yaml` | Concern 2 findings |
| Traceability findings | `taskflow/dags/design-ferric-1_0-r3/SUBTASK_design-doc-review/SUBTASK_traceability-review/traceability-findings.yaml` | Concern 3 findings |

---

## Verification Gate

Before writing the final output, assert each identity with evidence:

- **I-1**: Each spoke's `concern_ids` names exactly its concern(s) — completeness: [1], release-bar: [2], traceability: [3]. No overlap; together they cover [1, 2, 3].
- **I-2**: Every finding across all spokes has `severity`, `concern`, `location`, `statement`, and `recommendation` populated.
- **I-3**: The merged output contains every finding from every spoke. Count them before and after merging.
- **I-4**: `summary.blocking_count` in the merged output equals the count of findings where `severity == BLOCKING`.

If any identity fails, record the failure in the output with evidence (which spoke, which finding, which field). Do not silently plug the gap.

---

## Output

| Attribute | Value |
|---|---|
| Filename | `../design-doc-findings.md` |
| Format | YAML conforming to ancestor `contracts/findings_schema.yaml` |
| Location | `taskflow/dags/design-ferric-1_0-r3/SUBTASK_design-doc-review/design-doc-findings.md` (one level up from this workspace) |

The output is a YAML file (also readable as text) with:
- `spoke: design-doc-review`
- `concern_ids: [1, 2, 3]`
- `findings: [...]` — all findings from all three spokes merged, each with `id`, `severity`, `concern`, `location`, `statement`, `recommendation`
- `summary: { blocking_count, non_blocking_count }`

Finding IDs from the spokes are preserved unchanged (DDR-C-*, DDR-B-*, DDR-T-*).

---

## Success Criteria

- All three spoke findings files read.
- Every identity in contracts/_MANIFEST.yaml asserted with evidence.
- Any identity failure recorded in the output (no silent plugs).
- `../design-doc-findings.md` written at `taskflow/dags/design-ferric-1_0-r3/SUBTASK_design-doc-review/design-doc-findings.md`.
- Output conforms to ancestor findings_schema.yaml.
- `summary.blocking_count` matches the count of BLOCKING findings.
