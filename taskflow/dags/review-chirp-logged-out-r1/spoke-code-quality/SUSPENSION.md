# Suspension Record — spoke-code-quality

**Task**: `review-chirp-logged-out-r1/spoke-code-quality`
**Status**: SUSPENDED / NeedsDecompose
**Suspended at**: 2026-11-06

## Decomposition Decision

The 10 sub-concerns in the brief span distinct analysis areas (testing, SQL correctness, spec
deviation, dead code, framework scope, error safety, Rust idiom, prose quality) that could be
worked by different specialists in parallel. The enumerated-concerns rule fired — 10 numbered
distinct concerns across testing, correctness, code health, security, and prose themes — and
the Output Size trigger fired (REVIEW.md covering 10 concerns would exceed 400 lines). The
decompose evaluation produced `NeedsDecompose`.

## Children Materialized

| Task | Covers | Declared Output |
|------|--------|----------------|
| `spoke-tests` | Concerns 1, 2, 5 (test depth) | `spoke-tests/FINDINGS.md` |
| `spoke-correctness` | Concerns 3, 4 (SQL + spec deviation) | `spoke-correctness/FINDINGS.md` |
| `spoke-code-health` | Concerns 6, 7 (dead code + scope) | `spoke-code-health/FINDINGS.md` |
| `spoke-safety-idiom` | Concerns 8, 10 (error safety + Rust idiom) | `spoke-safety-idiom/FINDINGS.md` |
| `spoke-prose` | Concern 9 (prose quality) | `spoke-prose/FINDINGS.md` |
| `spoke-synthesis` | Synthesis gate + REVIEW.md | `../REVIEW.md` + `../SYNTHESIS.md` |

## Resumption Condition

All six children reach terminal lifecycle state. The synthesis task (`spoke-synthesis`) folds
this task `SUSPENDED → COMPLETED` by calling `engine_resume_suspended` with
`seam_path = spoke-code-quality/SYNTHESIS.md`.

## Named State Authored

- `_GLOBAL.md` — subtree hub at `spoke-code-quality/`
- `contracts/_MANIFEST.yaml` — ownership table, identities
- `contracts/findings_schema.md` — FINDINGS.md structure contract
- `spoke-tests/_BRIEF.md`
- `spoke-correctness/_BRIEF.md`
- `spoke-code-health/_BRIEF.md`
- `spoke-safety-idiom/_BRIEF.md`
- `spoke-prose/_BRIEF.md`
- `spoke-synthesis/_BRIEF.md`
