# SYNTHESIS — SUBTASK_identity_traceability (identity-assertion + traceability-matrix subtree)

Fold record for the internal-consistency half of the synthesis gate. The six spokes partitioned the corpus
by source, each emitting its slice; this synthesis joined the slices into the whole-DAG traceability-matrix
skeleton, asserted the one cross-source identity, and collected all eight identity verdicts into the gate
deliverable. Repository: `Nousix-LLC/nswe-demo`, grounded at commit `c805525`.

**Deliverable produced:** `outputs/identity-and-traceability.md` (at this subtree root) — the eight identity
verdicts with evidence, the two gate structural identities, and the 390-row matrix skeleton (every inherited
column except `live_status`, which is present-but-empty and keyed by `bar_id` for the fold).

## Ownership coverage (each owned artifact produced by its one declared owner; no double-writes)

| Artifact | Declared owner | Produced | Note |
|----------|----------------|----------|------|
| `SUBTASK_matrix_prod_dom/outputs/skeleton-prod-dom.md` | SUBTASK_matrix_prod_dom | ✓ | 42 `REQ-PROD-*` + 81 `REQ-DOM-*` design-side rows |
| `SUBTASK_matrix_ux/outputs/skeleton-ux.md` | SUBTASK_matrix_ux | ✓ | 119 `REQ-UX-*` design-side rows |
| `SUBTASK_matrix_id_ops/outputs/skeleton-id-ops.md` | SUBTASK_matrix_id_ops | ✓ | 73 `REQ-ID-*` + 75 `REQ-OPS-*` design-side rows |
| `SUBTASK_bar_mapping/outputs/bar-mapping.md` | SUBTASK_bar_mapping | ✓ | `REQ → bar_ids` (343 keys); `BAR_TESTABLE` |
| `SUBTASK_backlog_pr/outputs/backlog-pr.md` | SUBTASK_backlog_pr | ✓ | `REQ/BAR → (epic, issue)`; `ISSUE_TRACES`, `GAP_HAS_ISSUE`(design half), `GITHUB_HYGIENE`, `ONE_OWNER_PER_FILE` |
| `SUBTASK_concern_surface/outputs/concern-surface.md` | SUBTASK_concern_surface | ✓ | `CONCERN_COVERAGE`, `SURFACE_COVERAGE` |
| `outputs/identity-and-traceability.md` | SUBTASK_assemble | ✓ | gate deliverable (this fold) |
| `SYNTHESIS.md` | SUBTASK_assemble | ✓ | this fold record |

Each owned artifact was produced by exactly its one declared owner; no artifact was double-written, and this
synthesis re-derived no spoke's slice (it joined them). The one reconciled ownership detail —
`design/operational-readiness.md` produced at the operational concern's synthesis-child output rather than
its subtree-root path — leaves the owning task unchanged and is recorded under `ONE_OWNER_PER_FILE`.

## The eight identity dispositions

| # | Identity | Owner | Verdict | Evidence / note |
|---|----------|-------|---------|-----------------|
| 1 | `BAR_COVERS_GATING_REQS` | SUBTASK_assemble (cross-source) | **PASS** | 342/342 gating `REQ-*` covered by ≥1 `BAR-*`; 0 uncovered (set difference empty; `calc_001`) |
| 2 | `BAR_TESTABLE` | SUBTASK_bar_mapping | **PASS** | all 278 `BAR-*` name a vocab method and reference ≥1 `REQ-*`; 0 offenders |
| 3 | `ONE_OWNER_PER_FILE` | SUBTASK_backlog_pr | **PASS** | 7 `design/*.md`, one owner each; PR #122 map ⟷ artifact map agree |
| 4 | `CONCERN_COVERAGE` | SUBTASK_concern_surface | **PASS** | 6 brief concerns each covered by a design artifact |
| 5 | `SURFACE_COVERAGE` | SUBTASK_concern_surface | **PASS** | 10 surfaces: 8 designed+gated; notifications + billing out of scope with reasons |
| 6 | `ISSUE_TRACES` | SUBTASK_backlog_pr | **PASS** (scoped exception ruled) | 56/56 requirement-bearing issues cite ≥1 REQ/BAR; one epic per issue; 4 non-requirement follow-ups (#23/#24/#25/#27) ruled outside the per-req obligation — trivially fixable, non-gating |
| 7 | `GAP_HAS_ISSUE` | SUBTASK_backlog_pr | **PASS** (design/backlog half); live half deferred | both recorded gaps filed (#123 under #34; #124 under #90); live-measurement half owned by sibling `SUBTASK_live_measurement`, completes at the DAG fold |
| 8 | `GITHUB_HYGIENE` | SUBTASK_backlog_pr | **PASS** | PR #122, filed epics/issues, #2 index name things by repository identity only; no live posted-text re-scan (out of read-only scope) |

All eight carry a verdict with recorded evidence; none bare, none silently plugged. The two spoke-surfaced
shortfalls were ruled on (the four non-requirement follow-ups under `ISSUE_TRACES`) or attributed to their
owner (the live half of `GAP_HAS_ISSUE`), not reconciled away.

## Gate structural identities over the joined matrix

- **`ALL_EIGHT_ASSERTED` — PASS.** Each inherited identity carries a verdict with evidence.
- **`SKELETON_COMPLETE` — PARTIAL (surfaced, fixable; no gating requirement hidden).** All 342 gating
  `REQ-*` appear as exactly one row with `bar_ids` ≥ 1 and a `design_doc_ref`; no `req_id` twice; all five
  areas present; 48 non-gating rows also carried (390 rows total). The "covering `epic` + `issue_numbers`"
  clause is unmet for **70** gating `REQ-*` that have `BAR-*` coverage but no direct backlog issue trace
  (36 DOM, 20 UX, 8 ID, 4 OPS, 2 PROD; full list in the deliverable appendix). This is a backlog
  trace-granularity finding, not a release-bar coverage failure — every one of the 70 is enforced by the
  bar and falls within an epic's scope. Fixable (extend backlog §4, or the fold accepts epic-grain
  coverage) and non-gating to the bar.

## How the slices composed into the deliverable

One matrix row per `REQ-*`, keyed by `req_id`: `release_gating` from the owning design slice; `design_doc_ref`
as the area's repo-relative design path plus the requirement's section; `bar_ids` from the inverted
`REQ → bar_ids` map; `epic`/`issue_numbers` from the backlog §4 trace (empty where untraced);
`live_status` left empty for the sibling and the fold. Counts reconciled to the delivered design at
`c805525` (390 `REQ-*`, 278 `BAR-*`), with the hub's order-of-magnitude estimates recorded as superseded
by the delivered files (gapped id space / a stale UX figure), not treated as missing requirements.

## Fold

Parent `SUBTASK_identity_traceability` is resumed `SUSPENDED → COMPLETED` with this `SYNTHESIS.md` as the
seam. The deliverable `outputs/identity-and-traceability.md` is present for the sibling `SUBTASK_fold`,
keyed so each `BAR-*`'s `live_status` joins by `bar_id` (worst-case roll-up per row).

**Handed up to the fold:** (1) the `SKELETON_COMPLETE` shortfall (70 gating `REQ-*` without a direct issue
trace — fixable, non-gating); (2) the `ISSUE_TRACES` housekeeping item (4 non-requirement follow-ups to tag
or anchor); (3) the live-measurement half of `GAP_HAS_ISSUE`, to complete once the sibling's live gaps are
known.

**Methodology limitation (recorded):** the Phase-B `design` methodology loader was unavailable run-wide
(`agent_domain_unset`); this gate proceeded on the principal-product-designer posture and the relayed
Release-Definition guidance by prose. The join and the coverage assertion are a mechanical set computation
over frozen inputs, reproducible by `calc_001` / `calc_002`, so the limitation does not affect the result.
