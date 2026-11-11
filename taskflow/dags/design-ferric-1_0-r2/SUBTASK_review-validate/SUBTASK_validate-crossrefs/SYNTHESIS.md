# SYNTHESIS.md — SUBTASK_validate-crossrefs

**Fold record for**: SUBTASK_validate-crossrefs (NeedsDecompose parent)  
**Synthesized by**: SUBTASK_synthesis-crossrefs  
**Date**: 2026-11-02

---

## What was synthesized

This synthesis task assembled `crossrefs-findings.md` from two completed spoke outputs:

| Spoke | Output | Status |
|---|---|---|
| SUBTASK_req-reconciliation | `SUBTASK_req-reconciliation/req-reconciliation.md` | Completed |
| SUBTASK_issue-traceability | `SUBTASK_issue-traceability/issue-traceability.md` | Completed |

The final output is `crossrefs-findings.md`, written at `SUBTASK_validate-crossrefs/crossrefs-findings.md` as specified by the parent contract (`../contracts/_MANIFEST.yaml`).

---

## How the subtree resolved

**REQ register reconciliation (from req-reconciliation.md):**  
Status: **clean**. No duplicate ids, no orphaned cross-references, no BAR-FERRIC-* criteria citing undefined ids. All 193 REQ-* ids across 9 prefixes are properly owned and mutually exclusive. All 29 BAR-FERRIC-* criteria are fully anchored to the inventory.

**Issue traceability (from issue-traceability.md):**  
Status: **has-issues**. One major finding and several minor/informational findings:
- Major: REQ-FW-007 has no direct GitHub issue citation
- Minor: 30 REQ-API-* ids uncited but implicitly covered; REQ-ASYNC-003 and REQ-ASYNC-014 unconfirmed
- Informational: epic bodies use BAR-FERRIC-* as coverage language, not REQ-* ids or child issue numbers

**Cross-reference gaps (new, GAP-090–GAP-099 range):**  
Two new gaps assigned: GAP-090 (REQ-FW-007 traceability gap, major) and GAP-091 (REQ-ASYNC-003/014 status unconfirmed, minor). No gaps were found in ranges 090–099 by the prior nine concern tasks.

---

## Contract identities verified

From `contracts/_MANIFEST.yaml`:

- [x] `full_req_inventory` in req-reconciliation.md contains no id appearing in more than one source document — confirmed (clean status, no duplicates).
- [x] `crossrefs-findings.md` contains all three required sections (req_register_reconciliation, issue_traceability, gaps) per the parent schema — confirmed.
- [x] All GAP-NNN ids in crossrefs-findings.md are in range GAP-090 through GAP-099 and do not duplicate ids from the nine concern-findings.md files — confirmed (GAP-090, GAP-091 only).

---

## Declared outputs

- `crossrefs-findings.md` at `SUBTASK_validate-crossrefs/crossrefs-findings.md` ✓
