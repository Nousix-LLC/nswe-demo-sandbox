# SYNTHESIS — SUBTASK_rbar_synthesis

Produced by: SUBTASK_rbar_assembly  
Folds: SUBTASK_rbar_synthesis  
Terminal record for: SUBTASK_rbar_assembly

---

## Identity verification

| Identity | Result | Notes |
|---|---|---|
| IA | passed | All 18 covered surfaces have ≥1 BAR-FERRIC-* criterion with references to their REQ-* ids. |
| IB | passed | No criterion references an out-of-1.0 surface. REQ-FW-015..018 and REQ-RT-009 do not appear in any criterion's references list. |
| I2 | passed | All 42 criteria reference ≥1 REQ-* id that exists in a spoke register. |
| I3 | passed | All one_oh/release_gating=true REQ-*s are mapped to a criterion in §4 of release-bar.md: 8 REQ-FW, 12 REQ-SSR, 3 REQ-API, 2 REQ-ASYNC, 1 REQ-RT, 3 REQ-HTTP, 9 REQ-DX, 32 REQ-REL, 10 REQ-PERF. |
| I4 | passed | BAR-FERRIC-020 is stage one_oh and carries must_have: true; it covers REQ-SSR-004 and REQ-FW-004 (hydration without re-render). |
| I5 | passed | All four named out-of-1.0 items appear in §5 with status=out-of-1.0: scoped CSS (REQ-FW-015), browser devtools (REQ-FW-016), hot reload (REQ-FW-017), desktop/mobile (REQ-FW-018). None are referenced by any BAR-FERRIC-* criterion. |

---

## Summary

| Metric | Value |
|---|---|
| BAR-FERRIC-* criteria total | 42 |
| stage: usable_early | 14 |
| stage: one_oh | 28 |
| must_have: true | 1 (BAR-FERRIC-020) |
| Covered surfaces | 18 |
| Out-of-1.0 surfaces | 7 (4 canonical + 3 additional) |
| Gaps (no REQ-* coverage) | 2 (accessibility of framework output; testing story for app authors) |

---

## Gap analysis inputs used

Primary: `SUBTASK_rbar_gap_review/gap-analysis.md` — found and read; 18 covered, 2 gaps, 7 out-of-1.0.  
Cross-check: `SUBTASK_rbar_gap/gap-analysis-internal.md` — found and read; findings aligned on all status assignments. The cross-check noted it could not read the primary during its own run and conducted an independent sweep; both analyses reached the same conclusions.

---

## Declared output paths

| Artifact | Path | Status |
|---|---|---|
| release-bar.md | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-ferric-1_0/SUBTASK_release_bar/release-bar.md` | written |
| SYNTHESIS.md (SUBTASK_release_bar fold) | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-ferric-1_0/SUBTASK_release_bar/SYNTHESIS.md` | written |
| SYNTHESIS.md (SUBTASK_rbar_synthesis fold) | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-ferric-1_0/SUBTASK_release_bar/SUBTASK_rbar_synthesis/SYNTHESIS.md` | this file |
