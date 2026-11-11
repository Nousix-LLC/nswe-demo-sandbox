# SYNTHESIS — SUBTASK_routing-ctas

## Verdict
gate: PASS
round: 1

## Checks

| Check       | Result | Mechanical evidence                                                                   | Notes |
|-------------|--------|---------------------------------------------------------------------------------------|-------|
| wiring      | pass   | All three concern files present and readable; each contains required sections per `contracts/_MANIFEST.yaml` | — |
| contract    | pass   | All three concerns from `_GLOBAL.md` Scope addressed by their assigned spokes; all three contract identities hold | — |
| duplication | pass   | Each concern covered by exactly one spoke; ownership manifest verified against outputs | — |
| code-review | pass   | All outputs cite file+line at pinned commit `decb6196`; severity labels are `blocker`/`non-blocking`; analyses are well-reasoned and actionable | Two domain findings recorded in FINDINGS.md |

## Findings

No gate-level violations. The two domain findings produced by the spokes (F1 blocker,
F2 non-blocking) are recorded in `FINDINGS.md`; they reflect defects in the code under
review, not defects in the spoke outputs.

## Coverage assertion

- ownership coverage: every declared artifact has exactly one producer ✓
  (`concern-ac4.md` → `SUBTASK_ac4-path`; `concern-cta.md` → `SUBTASK_cta-link`;
  `concern-annotation.md` → `SUBTASK_annotation`; `FINDINGS.md` and `SYNTHESIS.md` →
  `SUBTASK_synthesis`)
- wiring: all three concern outputs present and conforming to schema ✓
- identities: all three contract identities evaluated — `all_concerns_in_findings` ✓,
  `cite_pinned_commit` ✓, `clean_partition` ✓; none plugged ✓
- review: combined spoke outputs reviewed; no block-severity gate finding open ✓
