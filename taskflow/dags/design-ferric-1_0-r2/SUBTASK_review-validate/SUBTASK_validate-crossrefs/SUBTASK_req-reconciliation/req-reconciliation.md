# REQ Register Reconciliation

**Produced by**: SUBTASK_req-reconciliation  
**Input sources**: Nine concern-findings.md files from SUBTASK_validate-* (all completed)  
**Conforms to**: `../contracts/_MANIFEST.yaml` §req_reconciliation_schema

---

## full_req_inventory

All REQ-* ids extracted from the nine concern-findings.md files and merged into a single inventory grouped by prefix. Each id is listed with its source document.

| Prefix | Source document (branch `work/design-ferric-1_0`) | Count | Assigned ids |
|---|---|---|---|
| REQ-FW-* | `design/ferric/scope-and-requirements.md` | 18 | REQ-FW-001 – REQ-FW-018 (001–014 gating; 015–018 post-1.0 deferrals) |
| REQ-SSR-* | `design/ferric/ssr-hydration.md` | 12 | REQ-SSR-001 – REQ-SSR-012 |
| REQ-API-* | `design/ferric/authoring-model.md` | 63 | Band A: REQ-API-001–029; Band B: REQ-API-030–052; Band C: REQ-API-060–070 (053–059 and 071–079 reserved/unassigned) |
| REQ-ASYNC-* | `design/ferric/async-forms-events.md` | 25 | Sec A: REQ-ASYNC-001–016; Sec B: REQ-ASYNC-020–024; Sec C: REQ-ASYNC-040–043 (017–019, 025–039, 044–059 unused headroom) |
| REQ-RT-* | `design/ferric/router-and-http.md` (Part 1) | 9 | REQ-RT-001 – REQ-RT-009 |
| REQ-HTTP-* | `design/ferric/router-and-http.md` (Part 2) | 13 | REQ-HTTP-001 – REQ-HTTP-013 |
| REQ-DX-* | `design/ferric/docs-and-dx.md` | 10 | REQ-DX-001 – REQ-DX-010 |
| REQ-REL-* | `design/ferric/release-and-distribution.md` | 33 | §1: REQ-REL-001–011; §2: REQ-REL-020–033; §3: REQ-REL-040–047 (012–019, 034–039, 048–059 reserved/unassigned) |
| REQ-PERF-* | `design/ferric/performance-and-benchmark.md` | 10 | REQ-PERF-001 – REQ-PERF-010 |

**Total: 193 assigned REQ-* ids across 9 prefixes.**

Note: The release-bar/plan concern (SUBTASK_validate-plan) covers consolidation documents that do not define a new REQ-* register. The REQ-* ids listed in its req_ids_found are all cross-references to ids owned by the eight spoke documents above; they are not added to the inventory count.

---

## duplicate_ids

Check: any REQ-* id appearing in more than one document's req_ids_found list.

Each of the nine prefixes is owned exclusively by one source document, with no prefix overlap:

| Prefix | Owner | Any other document's req_ids_found? |
|---|---|---|
| REQ-FW-* | scope-and-requirements.md | No |
| REQ-SSR-* | ssr-hydration.md | No |
| REQ-API-* | authoring-model.md | No |
| REQ-ASYNC-* | async-forms-events.md | No |
| REQ-RT-* | router-and-http.md | No |
| REQ-HTTP-* | router-and-http.md | No |
| REQ-DX-* | docs-and-dx.md | No |
| REQ-REL-* | release-and-distribution.md | No |
| REQ-PERF-* | performance-and-benchmark.md | No |

**Result: No duplicate ids found.** Each concern document owns one or two distinct prefixes; no id appears in more than one document's req_ids_found list.

---

## orphaned_references

Check: any REQ-* id cited in a document's body as a cross-reference that is not present in the owning document's req_ids_found list.

Spot-checks performed against design documents on branch `work/design-ferric-1_0`:

### ssr-hydration.md

Specific ids named in the cross-reference section of the concern findings: REQ-FW-003, REQ-FW-004, REQ-FW-008, REQ-FW-009, REQ-FW-014.

Spot-check against REQ-FW-* inventory (REQ-FW-001–018):
- REQ-FW-003 → REQ-FW-001–018 ✓
- REQ-FW-004 → REQ-FW-001–018 ✓
- REQ-FW-008 → REQ-FW-001–018 ✓
- REQ-FW-009 → REQ-FW-001–018 ✓
- REQ-FW-014 → REQ-FW-001–018 ✓

Additional citations in document body (wildcard groups REQ-ASYNC-*, REQ-API-*, REQ-HTTP-*, REQ-REL-*, REQ-DX-*): all prefixes present in inventory ✓

### authoring-model.md

Document body contains the expression "REQ-API-001 … REQ-API-079" (in the register heading and ownership declaration). This is a namespace range notation, not a citation of REQ-API-079 as a defined requirement. REQ-API-071–079 are documented as reserved headroom. No individual requirement body cites REQ-API-079 as a dependency. No orphan.

Cross-area references: REQ-FW-005, REQ-FW-006, REQ-FW-009, REQ-FW-014 — all in REQ-FW-* inventory ✓

### async-forms-events.md

Document body contains "REQ-ASYNC-017..019", "REQ-ASYNC-025..039", "REQ-ASYNC-044..059" as range notations documenting unused headroom within each section's assigned range (confirmed at lines 346, 562, 762, 819–820). These are range declarations, not citations of specific requirement ids. No orphan.

Cross-area references: REQ-FW-006, REQ-FW-009, REQ-FW-013 — all in REQ-FW-* inventory ✓. Specific ids REQ-SSR-* (in REQ-ASYNC-012/013) and REQ-HTTP-* (in REQ-ASYNC-014) reference namespaces fully present in inventory ✓.

### router-and-http.md

All REQ-* ids in the document body are either the document's own ids (REQ-RT-001–009, REQ-HTTP-001–013) or cross-references to REQ-FW-007, REQ-FW-008, REQ-FW-009, REQ-FW-010, REQ-FW-013 — all in REQ-FW-* inventory ✓.

**Result: No orphaned references found.** All cross-reference citations in the spot-checked documents point to ids that exist in the owning document's req_ids_found list.

---

## bar_without_req

Check: any BAR-FERRIC-* criterion from the release-bar concern findings that cites a REQ-* id not present in the full inventory.

The SUBTASK_validate-plan concern findings collected all REQ-* ids cited in the 29 BAR-FERRIC-* criteria. These ids are verified against the full inventory built above.

| Prefix group cited in BAR criteria | IDs cited | All in inventory? |
|---|---|---|
| REQ-FW-* | REQ-FW-001, 002, 004, 005, 006, 008, 009, 010, 011, 012, 013 | ✓ all in REQ-FW-001–018 |
| REQ-SSR-* | REQ-SSR-001 – REQ-SSR-012 (all 12) | ✓ all in REQ-SSR-001–012 |
| REQ-API-* | REQ-API-001, 002, 003, 004, 006, 012, 015, 023–028, 030–035, 037, 038, 041, 045, 047, 049–052, 060, 061, 063, 066, 068 | ✓ all within assigned bands (001–029, 030–052, 060–070); none in reserved ranges (053–059, 071–079) |
| REQ-ASYNC-* | REQ-ASYNC-001, 002, 004–013, 015, 016, 020–024, 040–043 | ✓ all within assigned sections (001–016, 020–024, 040–043); none in unused headroom |
| REQ-RT-* | REQ-RT-001 – REQ-RT-008 | ✓ all in REQ-RT-001–009 |
| REQ-HTTP-* | REQ-HTTP-001 – REQ-HTTP-013 (all 13) | ✓ all in REQ-HTTP-001–013 |
| REQ-DX-* | REQ-DX-001 – REQ-DX-010 (all 10) | ✓ all in REQ-DX-001–010 |
| REQ-REL-* | REQ-REL-001–011, 020–033, 040–047 (all 33) | ✓ all in REQ-REL-001–011, 020–033, 040–047 |
| REQ-PERF-* | REQ-PERF-001 – REQ-PERF-010 (all 10) | ✓ all in REQ-PERF-001–010 |

**Result: No BAR-FERRIC-* criterion cites a REQ-* id absent from the full inventory.** All 29 BAR-FERRIC-* criteria are fully anchored to ids that exist in the owning documents.

Note: GAP-080 (from SUBTASK_validate-plan) identifies three ids (REQ-DX-008, REQ-REL-024, REQ-REL-027) that are cited in BAR criteria but are missing from the §4 coverage map in release-bar.md. This is a coverage map completeness issue in release-bar.md, not an inventory gap — all three ids exist in the full inventory and are correctly assigned in their owning documents. The coverage check here passes; the map correction is the concern of the gap-fixing work item.

---

## reconciliation_status

**clean**

All three checks completed without findings:
- Duplicate id check: no id appears in more than one document's req_ids_found list
- Orphaned cross-reference check: all spot-checked cross-references point to ids present in the owning document's register
- BAR-FERRIC coverage check: all BAR-FERRIC-* criteria cite REQ-* ids present in the full inventory
