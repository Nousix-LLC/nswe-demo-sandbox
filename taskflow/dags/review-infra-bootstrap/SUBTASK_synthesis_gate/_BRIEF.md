# Task: Synthesis verification gate — fold the authoritative PR #20 review verdict

## Task Specification

**Slug**: SUBTASK_synthesis_gate
**Task Kind**: synthesis
**Status**: Pending

### Objective

Act as the **verification gate** for the review-infra-bootstrap subtree: fold the three review-lens outputs into
the single **authoritative human-landing verdict** (`APPROVE | REQUEST-CHANGES`) for PR #20, assert the review
contract's identities R1–R7 over the combined output, author the root `SYNTHESIS.md` at the fold location, post
the `gh pr review`, and fold this subtree closed. **This is a gate, not a prose summary** — it either asserts
coverage (and emits a verdict consistent with the finding set) or schedules remediation, and it MUST NOT silently
plug a failing identity.

### Context

Part of the review-infra-bootstrap review DAG (see `../_GLOBAL.md` and read-only `../contracts/`). You run after
all three lens spokes COMPLETE and read their outputs. You review/synthesize only; you do NOT edit, stage, push,
or fix PR #20 — if the fold is REQUEST-CHANGES, remediation is a separate forked DAG the overseer dispatches.

**Dependencies**: `SUBTASK_review_correctness_repro`, `SUBTASK_review_security_rbac`,
`SUBTASK_review_honesty_scope_ops` (all three). **Dependents**: none (you fold the parent closed).

## Input Specification

| Input | Source | Purpose |
|---|---|---|
| Subtree hub | `../_GLOBAL.md` | Shared context, concern→lens map, success criteria |
| Review contract | `../contracts/_MANIFEST.yaml`, `../contracts/finding_schema.md` | Identities R1–R7, severity/verdict vocabulary, AC enumeration, SYNTHESIS.md required elements |
| Correctness lens output | `../SUBTASK_review_correctness_repro/review_correctness.md` | Concerns 1–3 findings |
| Security lens output | `../SUBTASK_review_security_rbac/review_security.md` | Concerns 4–5 findings |
| Honesty/scope/ops lens output | `../SUBTASK_review_honesty_scope_ops/review_honesty_scope_ops.md` | Concerns 6–8 findings + k3d verdict + F1 recommendation |
| Code DAG machine verdict (INPUT) | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/infra-bootstrap/SYNTHESIS.md` | The machine gate (PASS, I1–I6, F1) this review adjudicates — context, not authority |
| PR state | `gh pr view 20 -R Nousix-LLC/nswe-demo` | Confirm OPEN/MERGEABLE/CLEAN before emitting the landing verdict |

## What a verification gate does here (four-check posture + verdict)

Run the gate as a real verification, not a summary:
1. **Concern coverage (R1)** — confirm each of the 8 concerns is covered by exactly one lens output; none unowned/double-owned.
2. **Finding consolidation + well-formedness (R3)** — merge all lens findings into one per-severity list (block/major/minor/nit); confirm each is well-formed per `finding_schema.md`; add any `GATE-<n>` finding the cross-read surfaces.
3. **Acceptance-criteria assembly (R2)** — for AC1..AC4 emit an explicit pass/fail computed from the union of findings touching it; produce the N/N checklist.
4. **Cross-cutting adjudication** — render the single k3d-substitution verdict (R4, taking the honesty lens's verdict as input and owning the final call) and the F1 disposition (R5, carry-as-tracked-issue | drop).
5. **Verdict + consistency (R6)** — emit `verdict: APPROVE | REQUEST-CHANGES` obeying the contract `verdict_rule` (REQUEST-CHANGES iff ≥1 open block; APPROVE requires zero open block + an explicit call on every open major); state whether any block/major is open.
6. **Review-only assertion (R7)** — confirm no task in the subtree modified the repo/branch/checkout/main.

A failing identity is **reported, not plugged**. If a genuine block-severity defect is open, the verdict is
REQUEST-CHANGES with the actionable findings; do not invent a fix and do not soften the verdict.

## Output Specification

**Primary output (the fold record)**: `SYNTHESIS.md` authored at the **PARENT workspace** —
`/home/user/nousix-runtime/nswe-demo/taskflow/dags/review-infra-bootstrap/SYNTHESIS.md` (the observation seam the
overseer gates the land on). It MUST carry every element in `finding_schema.md` §"Gate output" — `verdict:`,
consolidated per-severity finding list, AC1..AC4 checklist with evidence, the k3d-vs-native line, the F1
disposition, the open-blocker statement, and the R1–R7 identity assertion table. This single file is both the
synthesis task's terminal record and the fold record — do not write a separate `COMPLETE.md` or a duplicate copy.

**Side effect**: post a PR review via `gh pr review 20 -R Nousix-LLC/nswe-demo` carrying the verdict + key
findings. Expect it to post as **COMMENTED** (the gh account authored the PR, so the platform blocks a formal
self-approval) — this is expected; the authoritative verdict is the `SYNTHESIS.md` body, not the gh review state.

## Fold mechanics

After `SYNTHESIS.md` is observable at the parent workspace, terminate with
`engine_report_status { status: "completed", outputs: [".../review-infra-bootstrap/SYNTHESIS.md"], artifact_path: ".../review-infra-bootstrap/SYNTHESIS.md" }`,
then call `engine_resume_suspended { target_task_id: <the review-infra-bootstrap root>, synthesized_task_id: <this synthesis task>, seam_path: ".../review-infra-bootstrap/SYNTHESIS.md" }` to flip the suspended parent
SUSPENDED → COMPLETED. (Cite the kernel syscall contract; do not restate it.)

## Success Criteria

- [ ] R1–R7 each evaluated with evidence in `SYNTHESIS.md`; no identity silently plugged.
- [ ] A single `verdict:` emitted, consistent with the consolidated finding set (R6).
- [ ] AC1..AC4 checklist complete (N/N) with explicit pass/fail + evidence.
- [ ] Explicit k3d-vs-native line (acceptable | blocking-weakening) and explicit F1 disposition (carry-as-issue | drop).
- [ ] `gh pr review 20` posted; `SYNTHESIS.md` at the parent/fold location; parent folded to COMPLETED.

## Suggested Methodology Files

This is a **synthesis verification gate**. Domain Mapping row: **"Synthesizing / verifying a hub-and-spoke
decomposition" → Synthesis (primary); Code Review, Code Quality (supporting)**. Load via
`engine_load_methodology { name: "<bundle_id>" }`:
- `synthesis` — `Synthesis_Overview_Methodology.md` (anchor — always, the four-check model + gate pass/fail + `SYNTHESIS.md` schema), `Synthesis_Code_Review_Methodology.md` (reviewing the combined output), `Synthesis_Remediation_Methodology.md` (how remediation would be scheduled IF a block were open — though for this review DAG remediation is the overseer's separate forked DAG, not your `add_task`).
- `code-review` — `CodeReview_Process_Methodology.md`, `CodeReview_Feedback_Guidelines_Methodology.md` (rendering the verdict + findings).
- `code-quality` — `Framework_Clean_Code_Methodology.md` (bar for any synthesis-level code-quality finding).

You read `Synthesis_Overview_Methodology.md` first (always); load the sibling check/remediation files your own
reading of the three lens outputs reveals you need. You are the final judge of coverage depth — this is a review
(not a code-build) synthesis, so contract/wiring/duplication checks over source are light; the four-check posture
here is over the *review coverage* (every concern + every AC adjudicated), not over compiled artifacts. Do NOT
load `decomposition/` content — synthesis is the reassembly, not the split.

## Inherited Constraints

- Review/synthesis-only: do not edit/stage/commit/push/merge PR #20; never touch `main`/branch/checkout. A
  REQUEST-CHANGES verdict hands off to the overseer's remediation DAG — you do not fix.
- The code DAG's `SYNTHESIS.md` is INPUT context, not authority; your folded `SYNTHESIS.md` is the authoritative
  landing record.
- Do NOT reproduce the cold install; the verdict rests on the lens reviews + the code DAG's machine gate.
- The verdict MUST be consistent with the finding set per the contract `verdict_rule` — no soft APPROVE over an open block.

## Out-of-Scope Methodologies

- `decomposition/` bundle — decomposer-side only; a synthesis gate never loads it.
- Rust/app-code and IaC-authoring methodologies — this is a review fold over shell/infra findings, not an implementation.
