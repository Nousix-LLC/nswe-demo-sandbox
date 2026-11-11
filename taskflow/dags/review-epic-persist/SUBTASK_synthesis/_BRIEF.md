# Task: Synthesis — render the verdict, post the review, file backlog — PR #113

## Task Specification

**Slug**: SUBTASK_synthesis
**Task Kind**: synthesis
**Status**: Pending
**Dependencies**: SUBTASK_correctness, SUBTASK_durability_proof, SUBTASK_code_quality,
SUBTASK_architecture_contract, SUBTASK_security, SUBTASK_operational_readiness, SUBTASK_ci_doc_diagnosis

### Objective

Fold the seven concern findings into one authoritative APPROVE / REQUEST-CHANGES verdict on PR #113, deliver
it on GitHub, and file the non-blocking findings as backlog — the one gate the overseer reads.

### Context

The synthesis/verification gate of the PR #113 review DAG (see `../_GLOBAL.md` and `../contracts/`). This is
the only task in the subtree that writes to GitHub. The verdict in `SYNTHESIS.md` is authoritative and
independent of whether the platform lets the review post as a formal approval.

## Inputs

| Input | Source | Purpose |
|---|---|---|
| Subtree hub | `../_GLOBAL.md` | Target, constraints, the identities to evaluate |
| Contract | `../contracts/_MANIFEST.yaml`, `../contracts/finding_schema.md` | The identities (ID-*) to assert; the finding/severity vocabulary |
| Seven findings docs | `../SUBTASK_*/outputs/findings.md` | The folded review input |
| PR #113 | `gh` (read for state; write for the review + comments) | Where the review posts |
| Existing issues | `gh issue list` on `Nousix-LLC/nswe-demo` | De-duplicate backlog against open issues |

## What to produce

1. **Evaluate the contract identities** (`ID-SCHEMA`, `ID-PIN`, `ID-SEVERITY`, `ID-ACTIONABLE`, `ID-DOC-GATE`,
   `ID-VERDICT`, `ID-BACKLOG`, `ID-NO-HOST`, `ID-PLAIN-VOICE`, `ID-64-OPEN`) as assertions over the seven
   findings docs. Do **not** silently plug a failing identity — if a spoke's output is missing or
   malformed, surface it (a gap in the review is itself a finding; decide whether it blocks a verdict).
2. **Root `SYNTHESIS.md`** at this DAG's root — `../SYNTHESIS.md` (the fold location / observation seam):
   - A single **APPROVE** or **REQUEST-CHANGES** verdict. Per `ID-VERDICT`: REQUEST-CHANGES iff any concern
     carries a `blocks_landing: true` finding (the `doc` failure is one such blocker per `ID-DOC-GATE`),
     otherwise APPROVE with the explicit note that landing is gated on `doc` going green and the PR being
     mergeable and clean.
   - Findings grouped **per concern**, each with severity and whether it blocks; and, per concern, an explicit
     statement of what was checked and what was found clean.
   - Blockers named as what must change before landing.
3. **The review posted on PR #113.** `gh pr review --approve` is rejected for an owner-authored PR (same
   org/account), so post the review **as a PR comment carrying the verdict**, plus inline/line comments on the
   specific findings at their pinned locations. Every reviewed PR must visibly show its review.
4. **Backlog issues** for the non-blocking findings: grouped, de-duplicated against existing issues, each
   linked back to PR #113 and to epic #56 / the originating issue. Blockers are **not** filed as backlog.
   Do not close #64; note its status per the correctness finding.

## Fold mechanics

`SYNTHESIS.md` is this synthesis task's terminal record AND the record the parent fold consumes — write it at
`../SYNTHESIS.md`, report it as your `artifact_path` on terminal `completed`, and call
`engine_resume_suspended` with `seam_path` = `../SYNTHESIS.md` to flip the review-DAG root
`SUSPENDED → COMPLETED`. Write no separate `COMPLETE.md`.

## Success criteria

- [ ] All ten identities evaluated; any failure surfaced, none plugged.
- [ ] `../SYNTHESIS.md` carries one clear verdict, per-concern findings with severity/blocks, and per-concern
  what-checked / what-clean.
- [ ] The review is visibly posted on PR #113 (comment + inline comments).
- [ ] Non-blocking findings filed as backlog, grouped, de-duplicated, linked; blockers named in the verdict,
  not filed.

## Constraints

Repo scope `Nousix-LLC/nswe-demo` only; the only writes are the posted review/comments and the backlog issues
— no code changes, no push, no merge. **No host/cluster/SSH/credential details, no secret values, and no
taskflow/DAG internals** in anything posted to GitHub or in repo-reader-facing `SYNTHESIS.md` content. **No
attribution trailers** on anything posted. Run the avoid-ai-writing finishing pass over the verdict, the PR
comment, the inline comments, and every filed issue before posting — plain voice throughout.
