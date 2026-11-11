# Task: Synthesis verification gate — acceptance mapping, fold & landing verdict (PR #21, concern 6)

## Task Specification

**Slug**: SUBTASK_synthesis
**Task Kind**: synthesis
**Status**: Pending

### Objective

Act as the **verification gate** for the PR #21 review DAG. This is **not a prose summary** — it is
a gate that (a) verifies every spoke emitted conformant findings, (b) de-duplicates overlapping
findings, (c) maps every issue-#11 acceptance criterion to evidence (pass/fail), (d) aggregates
block/major/minor/nit counts and applies the verdict rule, and (e) authors the **root
`SYNTHESIS.md`** — the authoritative landing verdict the overseer gates on. If the gate finds its
inputs incomplete or non-conformant, it reports that (and, where appropriate, schedules remediation)
rather than papering over it.

### Context

Part of the review DAG for PR #21 (see `../_GLOBAL.md`). This is the fold node: its `SYNTHESIS.md`
resolves the SUSPENDED parent DAG. **Dependencies**: `SUBTASK_workflow_correctness`,
`SUBTASK_supply_chain_security`, `SUBTASK_image_job`, `SUBTASK_folded_minors` (all four spokes).
Their `findings.md` outputs are real, readable inputs (they complete before this task runs).

## The gate (four checks + remediation), adapted to a review DAG

1. **Contract / conformance check** — every spoke's `findings.md` exists and conforms to
   `../contracts/findings_schema.md` (severity in enum; each finding has location + rationale; every
   `block`/`major` has a `required_change`; each spoke states it reviewed head `c8123376`). A missing
   or non-conformant findings file is a gate failure — report it; do not fabricate the spoke's result.
2. **Coverage / wiring check** — each of the six brief concerns is covered by exactly one spoke's
   scope (1+2 → workflow_correctness, 3 → supply_chain_security, 4 → image_job, 5 → folded_minors,
   6 → this gate). No concern dropped; none silently double-owned.
3. **Duplication check** — findings two spokes raised about the same `location` are reconciled into
   one (keep the higher severity; note the cross-reference), so counts are not inflated.
4. **Review / verdict check** — aggregate the roll-ups, apply the verdict rule from the schema
   (`APPROVE` iff total block == 0 AND total major == 0; else `REQUEST-CHANGES`), and confirm the
   verdict is supported by the findings.

**Remediation**: if a spoke failed, produced a non-conformant or missing findings file, or left a
concern uncovered, prefer a plan amendment (`engine_amend_plan { add_task }`, Inject) to obtain the
missing analysis + a re-verification, rather than guessing the result. (Judgment: for a small gap you
may note it as a gate caveat; for a material gap, remediate.)

## Concern 6 — acceptance-criteria mapping (this gate owns it)

Map **every** requirement of issue #11 to evidence in the spoke findings and the diff, pass/fail per
criterion. Criteria (from `../_GLOBAL.md` shared facts): `ci.yml` runs on PR + push to `main`;
`cargo fmt --check`; `cargo clippy -D warnings`; `cargo test`; build the WASM frontend; on `main`
build + push the chirp-server image to GHCR; cache cargo/target; required-check friendly; delivered
as a PR into `main`. List any unmet/partial criterion and tie it to the findings that establish it.

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Shared facts, concerns, acceptance criteria | `../_GLOBAL.md` | What the verdict must cover |
| Findings schema + identities | `../contracts/findings_schema.md`, `../contracts/_MANIFEST.yaml` | Conformance + verdict rule + identities to assert |
| Spoke findings (×4) | `../SUBTASK_workflow_correctness/findings.md`, `../SUBTASK_supply_chain_security/findings.md`, `../SUBTASK_image_job/findings.md`, `../SUBTASK_folded_minors/findings.md` | The evidence to aggregate |
| PR metadata (to confirm head) | `gh pr view 21 --repo Nousix-LLC/nswe-demo --json headRefOid,state,mergeable` | Confirm head still `c8123376` |

## Output Specification

| Attribute | Value |
|-----------|-------|
| Filename | `SYNTHESIS.md` |
| Location | **the DAG root**: `/home/user/nousix-runtime/nswe-demo/taskflow/dags/review-ci-actions-r2/SYNTHESIS.md` (the SUSPENDED parent's directory — the overseer's observation seam and the fold record) |

### `SYNTHESIS.md` body MUST carry

- An explicit **verdict: `APPROVE` or `REQUEST-CHANGES`** (the overseer gates on this body).
- **Counts** of block / major / minor / nit, with each finding listed (id, severity, `file:line`, rationale; `required_change` for block/major).
- The **acceptance-criteria mapping** (issue #11), pass/fail per criterion.
- **Confirmation of the PR head reviewed** (`c8123376`).
- For `REQUEST-CHANGES`: the specific changes required (the union of every block + major `required_change`).

This `SYNTHESIS.md` is both the gate's terminal record and the record that folds the parent
`SUSPENDED → COMPLETED`. Do **not** post an approving GitHub review (self-review is platform-blocked
and non-authoritative); the `SYNTHESIS.md` body is the authoritative verdict.

## Success Criteria

- [ ] All four checks run; conformance of all four spoke findings files asserted (or failures reported/remediated — never silently plugged).
- [ ] Each of the six concerns confirmed covered; duplicates reconciled.
- [ ] Every issue-#11 acceptance criterion mapped pass/fail.
- [ ] Verdict rule applied correctly; `REQUEST-CHANGES` enumerates the required changes.
- [ ] Root `SYNTHESIS.md` written at the DAG root with all required body elements and head `c8123376` confirmed.

## Suggested Methodology Files

Parent's Domain-Mapping reading: **"Synthesizing / verifying a hub-and-spoke decomposition"**
(primary: Synthesis; supporting: Code Review, Code Quality).

- `synthesis/Synthesis_Overview_Methodology.md` — **always, first** — the four-check gate model + the gate pass/fail decision + the `SYNTHESIS.md` schema.
- `synthesis/Synthesis_Contract_Verification_Methodology.md` — this subtree froze a `taxonomy` contract; use this to assert conformance/identities against `../contracts/`.
- `synthesis/Synthesis_Duplication_Detection_Methodology.md` — reconciling findings two spokes raised about the same location.
- `synthesis/Synthesis_Remediation_Methodology.md` — if a spoke failed / a concern is uncovered: remediation-as-decomposition via `engine_amend_plan { add_task }`.
- `code-review/CodeReview_Feedback_Guidelines_Methodology.md` — so the verdict's required-changes are specific and actionable.

Load via `engine_load_methodology { name: "synthesis" }` (read `Synthesis_Overview` first), then
`{ name: "code-review" }`. **Gate posture is mandatory; which sibling check files you load and how
deeply you run each check is your judgment** — load fewer if a check is clearly inapplicable, more if
the inputs reveal additional surface.

## Inherited Constraints

- **Read-only review (P1): push nothing, change nothing in the repo.** Authoring `SYNTHESIS.md` and
  (if needed) injecting remediation tasks is in scope; writing to the PR/branch is not.
- **No silent plugs**: a failed identity or missing spoke output is reported (or remediated), never fabricated.
- **Verdict semantics are the contract's**: `APPROVE` iff 0 block AND 0 major; any block/major → `REQUEST-CHANGES`.
- Rely on the already-folded machine-PASS for build/lint/test/wasm/actionlint; your verdict is about review findings + acceptance mapping, not a re-run.

## Out-of-Scope Methodologies

- `decomposition/` bundle is decomposer-side; a synthesis gate never loads it.
