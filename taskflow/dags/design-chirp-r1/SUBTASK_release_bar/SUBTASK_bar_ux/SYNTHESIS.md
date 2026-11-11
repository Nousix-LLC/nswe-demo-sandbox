# SYNTHESIS.md — SUBTASK_bar_ux fold record

**Task**: SUBTASK_bar_ux  
**Fold by**: SUBTASK_bar_ux_synthesis  
**Status**: COMPLETED — all 8 subtree identities hold; `SUBTASK_bar_ux/outputs/bar-ux.md` assembled and verified.

---

## Identity assertions (with evidence)

Evidence source: `verify/verify_bar_ux.py` run against the assembled `outputs/bar-ux.md` and all five spoke sub-fragments. Exit 0 (PASS). Recorded outputs below.

```
spoke BAR count: 94 ; assembled BAR count: 94
gating REQ-UX total: 106 (expect 106) ; covered: 106
cross-cutting (295..299) minted: []
stage reconciliations: none (every assembled stage equals its spoke's proposal)

PASS — all 8 identities hold with evidence above.
```

### 1. UX_BAR_RANGE_RESPECTED — PASS
Every `BAR-NNN` lies within its spoke's assigned sub-range. Verified per spoke:

| Spoke | Sub-range | BAR count | All within range |
|-------|-----------|-----------|-----------------|
| SUBTASK_bar_ux_ia | BAR-200..214 | 15 | ✓ |
| SUBTASK_bar_ux_visual | BAR-215..229 | 15 | ✓ |
| SUBTASK_bar_ux_screens | BAR-230..264 | 34 | ✓ (BAR-264 unused; screens used BAR-230..263) |
| SUBTASK_bar_ux_responsive | BAR-265..274 | 10 | ✓ |
| SUBTASK_bar_ux_a11y | BAR-275..294 | 20 | ✓ |

No spoke wrote a BAR-* outside its contracted sub-range.

### 2. UX_NO_BAR_COLLISION — PASS
94 distinct BAR-* ids across the five sub-fragments. No id appears in more than one spoke. The assembled `bar-ux.md` carries exactly the same 94 ids (no extras outside the 295..299 cross-cutting range, and no spoke ids absent).

### 3. UX_GATING_REQ_COVERAGE — PASS
106 of 106 release-gating `REQ-UX-*` are referenced by at least one `BAR-*` in the assembled fragment. Per sub-area:

| Sub-area | Gating set | All covered |
|----------|-----------|-------------|
| IA | 17 (001..014, 016, 017, 018) | ✓ |
| Visual | 17 (020, 021, 022, 025..029, 031..039) | ✓ |
| Screens | 43 (040..056, 058..063, 065..070, 073..077, 079, 082..089) | ✓ |
| Responsive | 10 (090..099) | ✓ |
| A11y | 19 (100..104, 106..119) | ✓ |

Non-gating excluded: REQ-UX-015, 019, 023, 024, 030, 057, 064, 071, 072, 078, 080, 081, 105 (13 total; none is the sole basis of any BAR-*).

### 4. UX_BAR_TESTABLE — PASS
Every `BAR-*` in the assembled fragment carries a `verification_method` from the closed vocabulary (`manual_user_check`, `automated_test`, `inspection`, `operational_check`) — exactly one per block — and references ≥1 `REQ-UX-*` (and in some cases additionally `REQ-PROD-*`). No block is missing either field.

### 5. UX_BAR_STAGED — PASS
Every `BAR-*` carries exactly one `stage` field with a value in `{usable_early, releasable}`. No criterion is staged two ways. Stage reconciliation: none — every assembled stage equals its spoke's proposal. The assembled fragment proposes 51 `usable_early` and 43 `releasable` criteria; the parent `SUBTASK_bar_synthesis` owns the final cross-area line.

### 6. UX_NONGATING_EXCLUDED — PASS
No `BAR-*` is justified solely by a non-gating `REQ-UX-*`. Where a non-gating requirement is cross-referenced (for context only), the block also carries at least one gating `REQ-UX-*` as its primary enforced requirement. Script confirmed: no block's reference set is a subset of the non-gating set.

### 7. UX_COVERAGE_NOTE_PRESENT — PASS
`bar-ux.md` carries a "Coverage note" section mapping all 106 release-gating `REQ-UX-*` to the `BAR-*`(s) covering each, organised by sub-area. The parent `SUBTASK_bar_synthesis` can assert experience-area `GATING_REQ_COVERAGE` from this map without re-deriving the gating set.

### 8. UX_HYGIENE — PASS
`bar-ux.md` contains no host/cluster addresses, no filesystem/taskflow paths, no agent/DAG/run ids, no `SYNTHESIS.md` or `SUSPENSION.md` references, no attribution trailers, no `SUBTASK_` slug references, and no `_BRIEF.md` or `_GLOBAL.md` references. Content is repository-ready.

---

## Cross-cutting BAR-295..299

None minted. On assembly, every release-gating `REQ-UX-*` is held by a sub-area criterion, and every cross-screen pattern (compose across three placements, the product-wide empty/error/loading treatment, its reach to assistive technology, one consistent visual and token system, the nav shell across viewports) is already owned by the sub-area that holds its gating requirement. No gap requiring a cross-cutting bar was found; minting one would either duplicate a sub-area criterion or rest solely on a non-gating requirement.

---

## Stage reconciliation note

All five spokes' stage proposals were carried through unchanged. No cross-area conflict was found: each sub-area proposes `usable_early` for criteria the core-loop or get-in users need in the first adoptable version, and `releasable` for the remainder. The assembled 51/43 split is coherent across the five sub-areas.

---

## Methodology posture

The Phase-B `design` methodology loader was unavailable in this environment (`agent_domain_unset`, run-wide; the parent subtree recorded the same). The product-designer persona's release-definition judgment and the relayed bundle guidance (Release Definition primary; Experience Design, Product Strategy supporting) were applied. This constraint is recorded here only and kept out of the repository-bound `bar-ux.md`.

---

## Derived artifact

**`SUBTASK_bar_ux/outputs/bar-ux.md`** — the assembled experience-area release bar fragment (`BAR-200..294`, 94 criteria, `BAR-264` and `BAR-295..299` unused) plus the 106-row coverage note. Repository-ready. Consumed by `SUBTASK_bar_synthesis`.
