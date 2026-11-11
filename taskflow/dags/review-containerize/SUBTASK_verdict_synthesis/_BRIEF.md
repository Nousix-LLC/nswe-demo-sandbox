# Task: Synthesis gate — render the PR #22 verdict, write root SYNTHESIS.md, post the review

## Task Specification

**Slug**: SUBTASK_verdict_synthesis
**Task Kind**: synthesis
**Status**: Pending

### Objective

Act as the **verification gate** for the review-containerize subtree: integrate the five spokes'
`findings.md`, evaluate the contract identities as assertions, map the findings to work-item #12's
acceptance criteria, and render the **one authoritative APPROVE / REQUEST-CHANGES verdict** — written
to the root `SYNTHESIS.md` and posted as a review on PR #22. This is a **gate, not a prose summary**:
it either asserts coverage and renders a defensible verdict, or it surfaces the violations that block
one.

### Context

Hub-and-spoke synthesis for the review-containerize DAG (see `../_GLOBAL.md` and `../contracts/`).

**Dependencies**: `SUBTASK_dockerfile_build`, `SUBTASK_security_supplychain`, `SUBTASK_operability_docs`,
`SUBTASK_rustcode_sigterm`, `SUBTASK_scope_verification` — all five spoke `findings.md` are available
as inputs when this task runs (trust that; do not poll).

### The gate (four-check model + verdict)

Run these checks over the combined spoke outputs and record the result of each:

1. **Coverage (identity I1)** — every brief concern 1..8 is addressed exactly once with an explicit
   disposition. A hole (unaddressed concern) or a race (two spokes primary-owning one concern) is a
   gate FAIL to be surfaced, not plugged.
2. **Ownership / dedup (identities I2)** — the concern-6 idiom partition and the concern-2
   layer-vs-leakage seam were respected; no single defect is double-filed. Consolidate any legitimate
   cross-references into one canonical finding.
3. **Severity discipline (identity I4)** — audit every `block`/`major`: each must name a concrete,
   landable defect. **Downgrade** any `block`/`major` that is merely a hardening wish / posture
   preference to `minor`/`nit`, and say so explicitly.
4. **Acceptance-criteria map (identity I6)** — emit an explicit pass/fail for EACH of the nine
   work-item #12 acceptance criteria (enumerated in `containerize/SYNTHESIS.md`), each traceable to the
   spoke finding(s) that support the call.

Then render the verdict under **identity I3**: **REQUEST-CHANGES iff ≥1 open `block` finding** exists
across all spokes; otherwise **APPROVE**, which additionally requires an explicit disposition on every
open `major`. Render exactly one verdict.

**Remediation (review-DAG form).** This is a review DAG — it reviews, it never edits/fixes/merges. So
"remediation" here is NOT spawning fix-tasks that touch the repo; it is ensuring a REQUEST-CHANGES
verdict carries landable, concrete findings (location + evidence + remediation) that the code DAG or a
human can act on. If the spoke findings are internally inconsistent or a gate check FAILS in a way that
prevents a defensible verdict, prefer surfacing that (and, if genuinely needed, an additive
`engine_amend_plan` re-verification task) over plugging it silently.

### Input Specification

| Input | Source | Purpose |
|---|---|---|
| Hub | `../_GLOBAL.md` | Shared context + success criteria |
| Contract | `../contracts/_MANIFEST.yaml`, `../contracts/findings_schema.md` | Identities I1–I6 + severity taxonomy to assert against |
| Spoke findings | `../SUBTASK_dockerfile_build/findings.md`, `../SUBTASK_security_supplychain/findings.md`, `../SUBTASK_operability_docs/findings.md`, `../SUBTASK_rustcode_sigterm/findings.md`, `../SUBTASK_scope_verification/findings.md` | The findings to integrate |
| Machine gate | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/containerize/SYNTHESIS.md` | The nine acceptance criteria + build/run facts to map against |
| PR | `gh pr view 22 --repo Nousix-LLC/nswe-demo` | To post the review (read-only otherwise) |

### Output Specification

| Deliverable | Format | Location |
|---|---|---|
| Root verdict record | Markdown | `../SYNTHESIS.md` — i.e. `/home/user/nousix-runtime/nswe-demo/taskflow/dags/review-containerize/SYNTHESIS.md` (the DAG-root fold location; this is this subtree's one fold record) |
| Posted review | gh review (or review comment) | PR #22 on `Nousix-LLC/nswe-demo` |

The root `SYNTHESIS.md` MUST carry: the **APPROVE / REQUEST-CHANGES** verdict; the explicit
per-acceptance-criterion (×9) pass/fail; the consolidated severity-tagged findings list
(block/major/minor/nit) with location + evidence + remediation for each block/major; and the four-check
gate results. The posted PR review carries the verdict + key findings; if a formal self-approval is
blocked because the authoring account owns the PR, post the verdict as a **review comment** — the
authoritative verdict is the `SYNTHESIS.md` body, not the gh review state.

### Success Criteria

- [ ] Four-check gate results recorded (coverage, dedup, severity discipline, acceptance-criteria map).
- [ ] Identities I1–I6 each evaluated and reported (pass or surfaced violation; no silent plug).
- [ ] Exactly one APPROVE / REQUEST-CHANGES verdict, consistent with I3 (REQUEST-CHANGES iff ≥1 open block).
- [ ] Explicit pass/fail for all nine acceptance criteria.
- [ ] Root `SYNTHESIS.md` written at the DAG root; review posted on PR #22.
- [ ] Read-only honored except the single posted review (identity I5).

## Suggested Methodology Files

Domain Mapping row matched (verbatim): **"Synthesizing / verifying a hub-and-spoke decomposition
(contract + wiring + dedup + review gate) | Synthesis | Code Review, Code Quality"**. Load on demand via
`engine_load_methodology { name: "<bundle_id>" }`:

- `synthesis/Synthesis_Overview_Methodology.md` — **anchor, load first**: the four-check model and the gate pass/fail posture.
- `synthesis/Synthesis_Code_Review_Methodology.md` — running the gate as a code review of the combined output and calibrating the verdict.
- `synthesis/Synthesis_Duplication_Detection_Methodology.md` — the dedup check (identity I2), consolidating cross-referenced findings.
- `synthesis/Synthesis_Remediation_Methodology.md` — if a gate check FAILS or findings conflict, how to surface it / schedule additive re-verification rather than plug it.
- `code-review/CodeReview_Feedback_Guidelines_Methodology.md` + `code-review/CodeReview_PR_Authoring_Methodology.md` — authoring the posted PR review clearly and actionably.
- `code-quality/Framework_Clean_Code_Methodology.md` — baseline quality lens for the code-review face of the gate.

These are the gate's flagged methodologies; load `Synthesis_Overview` first (always), then the sibling
check/remediation files your reading of the subtree reveals you need — you are the final judge of
coverage DEPTH. (That this task runs a gate is prescribed; how deeply it runs each check is your judgment.)

## Inherited Constraints

- **Read-only** (identity I5): no edit/stage/commit/push/rebase/relock/merge; `main` and
  `work/containerize` untouched. The ONLY GitHub write is this task's single posted review on PR #22.
- Rely on the machine gate for build/test facts; do not rebuild.
- Render exactly ONE authoritative verdict, in the root `SYNTHESIS.md`.
- A `major`/`block` in the final verdict must name a concrete landable defect — not a hardening wish
  (record non-blocking hardening as minor/nit).
- PR #22 head `bc0c3c0d6380c9edd1b9433addc7fdcbffb55751`; repo `Nousix-LLC/nswe-demo`.

## Out-of-Scope Methodologies

- `decomposition/` bundle — decomposition is decomposer-side; a synthesis gate is the reassembly, not the split, and never loads it.
- The per-artifact deep-analysis bundles (containerization/security/rust/operations as PRIMARY analysis) — the spokes already applied those; here you integrate and verify, you do not re-run their analyses from scratch.
