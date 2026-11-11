# _BRIEF.md — review-digest-r1-synthesis

**Kind**: review synthesis (atomic)  
**Role**: Synthesis hub  
**Parent DAG**: review-update-chirp-server-digest-r1

---

## Objective

Aggregate the four concern findings into a final review verdict, author `SYNTHESIS.md` at the
observation seam, and post the review comment on PR #209.

---

## Inputs (declared dependencies — all four must be COMPLETED before this task runs)

| Concern | FINDINGS.md path |
|---|---|
| Correctness | `taskflow/dags/review-update-chirp-server-digest-r1/review-correctness/FINDINGS.md` |
| Safety | `taskflow/dags/review-update-chirp-server-digest-r1/review-safety/FINDINGS.md` |
| Hygiene | `taskflow/dags/review-update-chirp-server-digest-r1/review-hygiene/FINDINGS.md` |
| Security | `taskflow/dags/review-update-chirp-server-digest-r1/review-security/FINDINGS.md` |

The seam contract is at:
`taskflow/dags/review-update-chirp-server-digest-r1/contracts/_MANIFEST.yaml`

---

## Scope

1. Read all four FINDINGS.md files and verify each satisfies the contract identities (verdict is
   PASS or FAIL; evidence section is non-empty; a FAIL verdict has at least one finding listed).

2. Determine the overall verdict:
   - APPROVE if all four concerns are PASS and no blocking findings appear in any FINDINGS.md
   - REQUEST-CHANGES if any concern is FAIL or any FINDINGS.md contains a blocking finding

3. File any non-blocking findings as GitHub issues on `Nousix-LLC/nswe-demo`, linking to PR #209
   and issue #206.

4. Post the review as a comment on PR #209 (`Nousix-LLC/nswe-demo`). The comment must include:
   - The overall verdict (APPROVE or REQUEST-CHANGES)
   - A per-concern section for each of the four concerns: what was checked, what was found,
     any findings and their severity
   - A note on what was clean (specifically, not just "no findings")
   - For non-blocking findings: the issue number filed

5. Author `SYNTHESIS.md` at the observation seam path.

---

## Declared Outputs

1. `taskflow/dags/review-update-chirp-server-digest-r1/SYNTHESIS.md`  
   (observation seam — this is what the owner process reads to determine review completion)

2. A comment posted on PR #209 (`Nousix-LLC/nswe-demo`) carrying the full verdict and findings.

3. Any non-blocking finding issues filed on the board (zero or more).

---

## SYNTHESIS.md structure

```
# SYNTHESIS.md — review-update-chirp-server-digest-r1

## Verdict
APPROVE | REQUEST-CHANGES

## Blocking Findings
None. | <list>

## Non-blocking Findings
None. | <list with issue numbers>

## Per-Concern Results

### Correctness
<verdict, evidence summary, findings>

### Deployment Safety
<verdict, evidence summary, findings>

### Ops Hygiene
<verdict, evidence summary, findings>

### Security
<verdict, evidence summary, findings>

## PR Comment
Posted: <gh comment URL>
```

---

## Success Criteria

This task is complete when:
- All four FINDINGS.md files have been read and their contract identities verified
- Overall verdict is determined and justified by the concern verdicts
- SYNTHESIS.md is authored at the observation seam path
- A review comment is posted on PR #209
- Non-blocking findings (if any) are filed as board issues
