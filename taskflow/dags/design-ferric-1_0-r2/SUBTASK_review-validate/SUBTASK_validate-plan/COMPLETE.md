# COMPLETE — SUBTASK_validate-plan

## Status: completed

## What was done

Read `release-bar.md` and `release-plan.md` from branch `work/design-ferric-1_0` at `/home/user/nswe-demo` and validated them against the concern criteria specified in `_BRIEF.md`.

## Outputs produced

- `concern-findings.md` — concern findings conforming to `../contracts/_MANIFEST.yaml` §concern_findings_schema

## Summary of findings

**Status: needs-fix** — three gaps found.

### release-bar.md

- All 29 BAR-FERRIC-* criteria cite at least one REQ-* id ✓
- Staging principle is clearly defined; criterion assignments are logically consistent ✓
- All criteria are testable (concrete verification methods) ✓
- **GAP-080:** §4 coverage map is missing rows for REQ-DX-008, REQ-REL-024, and REQ-REL-027 — all three are cited in BAR criteria (BAR-022 and BAR-024) but absent from the one_oh coverage map (major)

### release-plan.md

- Epic delivery sequence is logically ordered ✓
- Individual work items correctly stage all criteria including the one_oh items within usable_early epics ✓
- Work items reference REQ-* ids, BAR-FERRIC-* ids, and design document sections ✓
- **GAP-081:** Plan references issue numbers #1, #5, #6 — none match the filed issues (#129–#136 epics, #137–#164 child issues). The plan and the filed backlog are unlinked (major)
- **GAP-082:** Epic Landscape table labels Client-side Router and HTTP/JSON Client as `usable_early`, but each contains a one_oh work item (BAR-016 and BAR-018 respectively); summary table is inconsistent with individual work-item staging (minor)

### Cross-document consistency

No staging contradictions between release-bar.md and release-plan.md at the work-item level. The Epic Landscape table issue (GAP-082) is the only cross-document inconsistency.

## Dependents

- SUBTASK_validate-crossrefs (reads req_ids_found from this file)
- SUBTASK_synthesis (reads concern-findings.md)
