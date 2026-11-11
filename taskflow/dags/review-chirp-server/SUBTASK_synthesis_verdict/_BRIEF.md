# Task: Synthesis gate — authoritative landing verdict for PR #19

## Task Specification
**Slug**: SUBTASK_synthesis_verdict
**Task Kind**: synthesis
**Status**: Pending

### Objective
Act as the **verification gate** for the review-chirp-server review DAG: integrate the four spoke
findings files against the findings contract, render the **authoritative** `APPROVE` /
`REQUEST-CHANGES` verdict on **PR #19**, post the gh PR review, and write the root `SYNTHESIS.md`
fold record at the fold location — then fold this DAG's root task `SUSPENDED → COMPLETED`.

**This task is a verification GATE, not a prose summary.** You run a contract-coverage + identity
check over the combined spoke outputs and either assert coverage (and derive the verdict) or, if a
spoke left an owned item unaddressed or produced a malformed findings file, schedule remediation
rather than silently plugging the hole.

### Context
Part of the review-chirp-server review DAG (`../_GLOBAL.md`). This is the hub position; the four
spokes are your dependencies. You review the *review* (coverage + consistency) and render the
landing verdict the overseer gates on. You do NOT edit source, fix defects, relock, or push to
`work/chirp-server` — if the combined findings contain an open `block` (or a `major` you judge
land-blocking), the verdict is `REQUEST-CHANGES` and remediation is the overseer's separate forked
code DAG.

**Dependencies**: `SUBTASK_rust_soundness_review`, `SUBTASK_architecture_contract_review`,
`SUBTASK_test_adequacy_review`, `SUBTASK_code_review_quality_review`. **Dependents**: none (this is the fold).

## Input Specification
| Input | Source | Purpose |
|-------|--------|---------|
| Hub | `../_GLOBAL.md` | Shared context, task structure, identities |
| Contract | `../contracts/_MANIFEST.yaml`, `../contracts/findings_schema.md` | Coverage map (AC1–AC8, F1_1–F1_4), identities, severity rule |
| Root rubric | `../_BRIEF.md` | The acceptance rubric + the fold's required contents |
| Spoke outputs | `../SUBTASK_rust_soundness_review/findings_rust_soundness.md`, `../SUBTASK_architecture_contract_review/findings_architecture_contract.md`, `../SUBTASK_test_adequacy_review/findings_test_adequacy.md`, `../SUBTASK_code_review_quality_review/findings_code_review_quality.md` | The four review lenses to integrate |
| Code DAG verdict | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/chirp-server/SYNTHESIS.md` | The machine gate (PASS round 1) — context the human verdict composes with |

## Process (the gate — four checks + decision, then fold)
1. **Coverage check**: assert every acceptance criterion AC1–AC8 has an explicit verdict from its
   owner spoke and every F1 sub-question F1_1–F1_4 is answered (per `_MANIFEST.yaml`). A missing or
   malformed owned item is a gate FAIL → see Remediation.
2. **Consistency check**: every finding across the four files uses the fixed severity vocabulary and
   cites evidence; reconcile any cross-spoke disagreement (e.g. a craft note vs a soundness verdict)
   to a single consolidated finding list with stable ids.
3. **F1 consolidated ruling**: integrate F1_1 (live/not-dead), F1_2 (flipped test + no 422 pin),
   F1_3 (`details` contract-satisfaction analysis), F1_4 (no regression) into ONE explicit F1 line:
   **F1 fix sound / not sound**, and make the **`details`-limitation ruling** — *acceptable
   trade-off* vs *blocking weakening of the wire contract* — as an explicit **gate decision with
   reasoning** (this is the gate's call, not a spoke's).
4. **F2 disposition**: confirm the code DAG's tracked minor F2 is non-gating and record the
   tracked-issue recommendation for CI work-items #10–#13 (or escalate with reasoning).
5. **Verdict derivation**: `REQUEST-CHANGES` iff any open `block`; decide with reasoning whether any
   open `major` also forces `REQUEST-CHANGES`; otherwise `APPROVE`. State explicitly whether any
   block/major finding is open.
6. **Post the gh review**: `gh pr review 19 -R Nousix-LLC/nswe-demo --comment --body <verdict summary>`
   (it will post as **COMMENTED** due to the self-review platform block — expected; the authoritative
   verdict lives in `SYNTHESIS.md`, not the gh review state). Do NOT use `--approve`/`--request-changes`
   given the self-review block; post the verdict in the comment body.
7. **Write the fold record & fold**: author `../SYNTHESIS.md` (the root observation seam) and resolve
   this DAG's root via the synthesis fold (see Output).

## Remediation (if the gate FAILs on coverage/consistency, NOT on PR findings)
A gate FAIL here means a **spoke** under-delivered (missing owned verdict, malformed findings file),
not that PR #19 has defects. If so, schedule a fix-task via `engine_amend_plan { add_task }` (Inject)
to re-run the deficient lens, depend this synthesis on it, and re-verify — do not fabricate the
missing coverage. (A PR #19 defect, by contrast, is simply recorded as a finding and flows to the
`REQUEST-CHANGES` verdict — that is a normal gate PASS with a change-request outcome, not a
remediation.)

## Methodology (load on demand — IDs only) — SYNTHESIS gate posture
### Suggested Methodology Files
Matched row: **"Synthesizing / verifying a hub-and-spoke decomposition" → Synthesis / Code Review, Code Quality**.
- `synthesis` — **primary, anchor first**: `Synthesis_Overview_Methodology.md` (the four-check gate
  model + `SYNTHESIS.md` schema — always), then `Synthesis_Contract_Verification_Methodology.md`
  (assert the findings contract's coverage/identities), `Synthesis_Code_Review_Methodology.md`
  (reviewing the combined review), and `Synthesis_Remediation_Methodology.md` (remediation-as-
  decomposition, if a spoke under-delivered).
- `code-review` — `CodeReview_Process_Methodology.md` for the verdict framing.
- `code-quality` — optional, for consolidating craft findings.
Load the anchor first, then the sibling files your reading of the subtree requires. **Which check
files you load and how deeply you run each check is your judgment; THAT you run the gate is
prescribed.**

### Inherited Constraints
- The root `SYNTHESIS.md` is the **authoritative landing verdict** — the overseer gates on it, not on
  the gh review state or the code DAG's machine gate alone.
- Reviewer discipline (P1): no source edits, no push/rebase/relock, never touch `main`; only
  `Nousix-LLC/nswe-demo`. Do NOT resolve PR #19's `Cargo.lock` conflict (overseer's forked relock DAG).
- Do NOT treat the CONFLICTING/DIRTY mergeability as a finding.

## Output Specification
**Primary output / fold record**: `../SYNTHESIS.md` (this DAG's root workspace — the observation
seam `/home/user/nousix-runtime/nswe-demo/taskflow/dags/review-chirp-server/SYNTHESIS.md`).

It MUST contain:
- `verdict: APPROVE` **or** `verdict: REQUEST-CHANGES` (explicit).
- The consolidated per-severity finding list (block / major / minor / nit) with stable ids + evidence.
- The acceptance-criteria checklist **N/N** (AC1–AC8, each pass/fail with the owning spoke's verdict).
- The explicit **F1 line** (fix sound / not sound) and the **`details`-limitation ruling**
  (acceptable / blocking) with reasoning.
- The **F2 disposition** + tracked-issue recommendation for #10–#13.
- An explicit statement of whether any **block/major finding is open**.
- A note recording the gh review was posted (COMMENTED) and that this file is authoritative.

**Fold mechanics**: write `../SYNTHESIS.md` as this task's terminal record at the fold location, then
`engine_report_status { status: "completed", outputs: ["../SYNTHESIS.md"], artifact_path: "../SYNTHESIS.md" }`
and `engine_resume_suspended { target_task_id: <root review DAG task>, synthesized_task_id: <this task>, seam_path: ".../review-chirp-server/SYNTHESIS.md" }` to flip the root `SUSPENDED → COMPLETED`.
(No separate root `COMPLETE.md`: the root resolves entirely via this fold record.)

## Success Criteria (the gate cannot be read and mistaken for a summary)
- [ ] **Four-check gate run**: coverage (AC1–AC8 + F1_1–F1_4 all addressed), consistency (severity
      vocabulary + evidence), F1 consolidated ruling, F2 disposition — each explicitly recorded.
- [ ] Verdict derived by the fixed rule and stated as `APPROVE`/`REQUEST-CHANGES` with open-block/
      major status explicit.
- [ ] If any owned item was unaddressed/malformed → remediation fix-task injected and re-verified
      (NOT silently plugged).
- [ ] gh PR review posted (COMMENTED expected).
- [ ] `../SYNTHESIS.md` written at the observation seam; root folded `SUSPENDED → COMPLETED`.
