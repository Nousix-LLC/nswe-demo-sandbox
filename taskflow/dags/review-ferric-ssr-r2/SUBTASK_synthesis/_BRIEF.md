# Task: Synthesis — combine verdicts, write SYNTHESIS.md, post PR review

## Task Specification

**Slug**: SUBTASK_synthesis
**Task Kind**: synthesis
**Depends on**: SUBTASK_b1-verify, SUBTASK_b2-verify, SUBTASK_regression-quality-sec
**Status**: Pending
**Assigned To**: swe-reviewer

### Objective

Gate the three parallel verdict spokes. Read `verdict-b1.md`, `verdict-b2.md`, and
`verdict-regression-quality-sec.md`. Produce a final APPROVE or REQUEST-CHANGES verdict in
`SYNTHESIS.md` at the dag root. Post the verdict as a review comment on PR #228. Then fold the
root task via `engine_resume_suspended`.

This is a synthesis node: it reasons only over the sibling spokes' recorded verdicts plus any
direct evidence those verdicts cite. It does not re-read the codebase from scratch — it reads the
verdict files, verifies their internal consistency, and combines them. If a verdict is internally
inconsistent or incomplete (a check listed as required was not addressed), that is itself a finding.

---

## Input Specification

### Required Inputs

| Input | Location | Purpose |
|---|---|---|
| `verdict-b1.md` | `../SUBTASK_b1-verify/verdict-b1.md` | B1 (REQ-HYD-003) verdict: PASS or FAIL |
| `verdict-b2.md` | `../SUBTASK_b2-verify/verdict-b2.md` | B2 (REQ-SSR-006) verdict: PASS or FAIL |
| `verdict-regression-quality-sec.md` | `../SUBTASK_regression-quality-sec/verdict-regression-quality-sec.md` | Regression + quality + security: PASS or FAIL |
| `_GLOBAL.md` | `../_GLOBAL.md` | Project context, scope, success criteria |
| PR #228 state | GitHub (`gh pr view 228 --repo Nousix-LLC/nswe-demo`) | Current CI status, PR description |

---

## Process Guidance

### Step 1: Read and validate the three verdict files

For each verdict file:
- Is the verdict stated (PASS or FAIL)?
- Was every required check in the brief addressed? (Do not silently pass a check that was
  listed as required but not addressed in the verdict.)
- Are file:line citations present where the brief required them?
- Is the reasoning in the open (not just "PASS" with no explanation)?

If a verdict file is missing a required check, treat that check as not verified. A not-verified
blocker check is itself a blocker in the final verdict.

### Step 2: Gate logic

**APPROVE** if and only if ALL of the following hold:
- `verdict-b1.md` says PASS (B1 resolved — REQ-HYD-003 hydrate() wiring confirmed)
- `verdict-b2.md` says PASS (B2 resolved — REQ-SSR-006 wasm-bindgen-test coverage confirmed)
- `verdict-regression-quality-sec.md` says PASS (9 regression criteria still satisfied;
  no new blockers in quality or security)
- CI is green on the PR

**REQUEST-CHANGES** if any of the above is FAIL or not fully addressed.

There is no partial approval or "approve with concerns": if a blocker stands, the verdict is
REQUEST-CHANGES.

### Step 3: Write SYNTHESIS.md

Write `SYNTHESIS.md` at the dag root (`../SYNTHESIS.md` relative to this workspace, i.e.,
`taskflow/dags/review-ferric-ssr-r2/SYNTHESIS.md`).

The file format:

```markdown
# Review Synthesis — PR #228 (ferric-ssr-r4 re-review)

## Verdict: [APPROVE | REQUEST-CHANGES]

## B1 — REQ-HYD-003: hydrate() wiring

[Summary of what verdict-b1.md found. Cite file:line from the spoke's verdict.]

## B2 — REQ-SSR-006: wasm-bindgen-test coverage

[Summary of what verdict-b2.md found. Cite from the spoke's verdict.]

## Regression, Quality, Security

[Summary of what verdict-regression-quality-sec.md found.]

## Fresh Non-Blockers

[List any fresh non-blockers found across all spokes, with file:line. Or "None found."]

## If REQUEST-CHANGES: Remaining Blockers

[Numbered list; each entry: Requirement ID, what is wrong, what would satisfy it.
Omit this section on APPROVE.]

## If APPROVE: What Was Clean

[What was verified across all 11 criteria. Omit this section on REQUEST-CHANGES.]
```

The prose in SYNTHESIS.md must be free of AI-tell patterns (see persona bar: no moral adjectives
on metrics, no narrated candor, no slot-fill templates, no padding filler).

### Step 4: Post the review to PR #228

Post the SYNTHESIS.md content as a GitHub review on PR #228:

```bash
gh pr review 228 \
  --repo Nousix-LLC/nswe-demo \
  --[approve|request-changes] \
  --body "$(cat ../SYNTHESIS.md)"
```

Use `--approve` if the verdict is APPROVE; use `--request-changes` if REQUEST-CHANGES.

If the PR has already been approved or if CI is not green, note it in the SYNTHESIS.md but
do not let that block posting the review — post whatever the verdict is.

### Step 5: Fold the parent via engine_resume_suspended

After SYNTHESIS.md is written and the PR review is posted, call:

```
engine_resume_suspended {
  target_task_id: "<root task ID of review-ferric-ssr-r2>",
  synthesized_task_id: "<your own task ID>",
  seam_path: "<absolute path to SYNTHESIS.md>"
}
```

The root task ID is the task that owns this subtree. You can find it from your process context
or from the `_GLOBAL.md` task structure. The seam path is the absolute path to the SYNTHESIS.md
file you wrote in Step 3 (i.e., `taskflow/dags/review-ferric-ssr-r2/SYNTHESIS.md` resolved to
its absolute path under the repository root).

---

## Output Specification

**Primary output**: `taskflow/dags/review-ferric-ssr-r2/SYNTHESIS.md`
(written as `../SYNTHESIS.md` relative to this workspace)

**Secondary output**: PR #228 review comment posted via `gh pr review`

---

## Success Criteria

- [ ] All 3 verdict files read and validated (each required check addressed)
- [ ] Gate logic applied correctly (APPROVE iff all three PASS + CI green)
- [ ] SYNTHESIS.md written at dag root with stated verdict
- [ ] PR #228 review posted with matching approve/request-changes
- [ ] `engine_resume_suspended` called to fold the root task
- [ ] No AI-tell patterns in SYNTHESIS.md prose

---

## Suggested Methodology Files

**Task type**: synthesis / gate task — combine prior verdicts, no re-read of code

- `synthesis/Synthesis_Report_Writing_Methodology.md` — synthesis report structure if available
- `code-review/CodeReview_Process_Methodology.md` — final verdict framing and prose bar
- `avoid-ai-writing` skill (if available) — prose check before posting

If `synthesis` bundle is not available, apply the persona's self-verification checklist
directly (§Self-Verification Before Finalizing in the system prompt).

---

## Inherited Constraints

- Repository: Nousix-LLC/nswe-demo, branch `work/ferric-ssr-r1`, PR #228
- Do not re-raise previously filed non-blockers #229–#242
- Do not reference overseer I267 escalation comments
- Prose bar: no AI-tell patterns in SYNTHESIS.md or PR review comment
- Security: do not put server address, SSH key path, user name, or host paths into the PR comment
