# Task: Security Surface Synthesis Gate

## Task Specification

**Slug**: SUBTASK_seccheck_synth
**Task Kind**: synthesis
**Depends on**: SUBTASK_html_inj, SUBTASK_dom_spoof, SUBTASK_test_inj
**Status**: Pending
**Assigned To**: swe-reviewer

### Objective

After all three security-concern spokes complete, assemble their per-concern finding subsections into the required `security_raw_findings.md` output at the SUBTASK_sec_check workspace root (the fold location), then author `SYNTHESIS.md` there and call `engine_resume_suspended` to fold the SUBTASK_sec_check parent from SUSPENDED to COMPLETED.

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Hub document | `../_GLOBAL.md` | Scope, fold location, parent task ID, synthesis instructions |
| Spoke output contract | `../contracts/spoke_output_schema.md` (at the SUBTASK_sec_quality level) | Structure `security_raw_findings.md` must conform to |
| Per-concern format | `../contracts/finding_format.md` | Verbatim concern names, field rules |
| Artifact manifest | `../contracts/_MANIFEST.yaml` | Ownership and identity assertions to verify |
| HTML injection finding | `../SUBTASK_html_inj/html_inj_finding.md` | Spoke output for HTML injection concern |
| DOM spoofing finding | `../SUBTASK_dom_spoof/dom_spoof_finding.md` | Spoke output for DOM spoofing concern |
| Test injection finding | `../SUBTASK_test_inj/test_inj_finding.md` | Spoke output for test injection concern |

---

## Output Specification

**Both outputs are written at the SUBTASK_sec_check workspace root (`../`), not at this synthesis workspace.**

| Attribute | Value |
|-----------|-------|
| Filename 1 | `security_raw_findings.md` |
| Location 1 | `../` (SUBTASK_sec_check workspace root = fold location) |
| Absolute path 1 | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/review-ferric-ssr-r2/SUBTASK_regression/SUBTASK_sec_quality/SUBTASK_sec_check/security_raw_findings.md` |
| Filename 2 | `SYNTHESIS.md` |
| Location 2 | `../` (SUBTASK_sec_check workspace root = fold location) |
| Absolute path 2 | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/review-ferric-ssr-r2/SUBTASK_regression/SUBTASK_sec_quality/SUBTASK_sec_check/SYNTHESIS.md` |

---

## Success Criteria

- [ ] All three spoke finding files present and conforming to `../contracts/finding_format.md`
- [ ] `security_raw_findings.md` assembled at fold location: `## Security Findings` header, three subsections pasted verbatim from each spoke file, `## What Was Examined and Found Clean` section listing concerns whose Result is Clean
- [ ] `security_raw_findings.md` identity assertions in `../contracts/_MANIFEST.yaml` all satisfied
- [ ] `SYNTHESIS.md` authored at fold location
- [ ] `engine_resume_suspended` called with:
  - `target_task_id`: `proc-329f53fb-256d-41c0-8873-0894bcf81914`
  - `synthesized_task_id`: this task's own process/task ID (assigned at dispatch time)
  - `seam_path`: `/home/user/nousix-runtime/nswe-demo/taskflow/dags/review-ferric-ssr-r2/SUBTASK_regression/SUBTASK_sec_quality/SUBTASK_sec_check/SYNTHESIS.md`
- [ ] Terminal `report_status { status: "completed" }` called after fold

---

## Assembly Instructions

1. Read all three spoke finding files.
2. Verify each conforms to `../contracts/finding_format.md`: concern name matches verbatim, Result field present, Evidence cites file + line at `75c1eef`, Finding field present iff Result is Finding.
3. Write `security_raw_findings.md` at `../` with:
   ```
   ## Security Findings

   <paste SUBTASK_html_inj finding subsection verbatim>

   <paste SUBTASK_dom_spoof finding subsection verbatim>

   <paste SUBTASK_test_inj finding subsection verbatim>

   ## What Was Examined and Found Clean

   <list concerns whose Result is Clean, with brief note on what was checked>
   ```
4. Write `SYNTHESIS.md` at `../` recording that the synthesis completed, what spokes were consumed, and which concerns produced findings vs. were clean.
5. Call `engine_resume_suspended` with the parameters above.
6. Take the `completed` terminal path.

---

## Inherited Constraints

- Scope: ferric-ssr-r4 commits only (`7fb90c7`, `e625c3f`, `75c1eef`)
- Do NOT re-raise non-blockers #229–#242
- Do not reference overseer escalation comments from I267
- Output at fold location (`../`), not at this synthesis workspace
