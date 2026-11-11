# Task: Ferric 1.0 — synthesis & fold (root SYNTHESIS.md)

## Task Specification
**Slug**: SUBTASK_synthesis
**Task Kind**: synthesis
**Status**: Pending

### Objective
Verify that the subtree's parts composed, then author the **root `SYNTHESIS.md`** — the overseer's observation
seam — stating the Ferric 1.0 release bar and indexing the filed issues by epic, and fold the suspended parent
to COMPLETED.

### Context
The synthesis/verification gate for the design-ferric-1_0 subtree (see `../_GLOBAL.md`). It reads every spoke's
output, the release bar, the release plan, the PR record, and the filed-backlog record, runs the contract
identities as assertions, and consolidates the result. This is the gate node for its siblings.

**Dependencies**: all other children — `SUBTASK_scope_and_requirements`, the seven capability spokes,
`SUBTASK_release_bar`, `SUBTASK_release_plan`, `SUBTASK_design_pr`, `SUBTASK_file_backlog`.

### What to do (approach, not a runbook)
- Read all sibling outputs and `../contracts/`.
- Evaluate the contract identities **I1–I9** as assertions (disjoint registers; no invented REQ; gating
  coverage; SSR must-have present; out-of-1.0 recorded and enforced by no BAR; plan traces; #5/#6 folded not
  duplicated; artifacts placed once; frozen surfaces respected). A failure is reported as a structured signal,
  **never silently plugged** — if an identity fails, say so plainly and do not fabricate coverage.
- Author `SYNTHESIS.md` at the fold location (this subtree's hub root — see path below): the consolidated
  **Ferric 1.0 release bar**, the **issues indexed by epic** (from the filed-backlog record), the PR
  reference, and the identity-assertion results.

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub + contract | `../_GLOBAL.md`, `../contracts/` | Context + the identities to assert. |
| Release bar | `../SUBTASK_release_bar/release-bar.md` | The bar to state in the synthesis. |
| Release plan | `../SUBTASK_release_plan/release-plan.md` | The epic/work-item structure. |
| PR record | `../SUBTASK_design_pr/design_pr.md` | The PR to reference. |
| Filed backlog | `../SUBTASK_file_backlog/filed_backlog.md` | The issues to index by epic. |
| All design docs | each `../SUBTASK_*/<file>.md` | To assert the identities against. |

### Declared output
- `SYNTHESIS.md` authored at **`/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-ferric-1_0/SYNTHESIS.md`**
  (the fold location = this subtree's hub root, the overseer's observation seam).

### Success criteria
- [ ] `SYNTHESIS.md` states the Ferric 1.0 release bar and indexes the filed issues by epic.
- [ ] All nine identities are evaluated with a pass/fail result each; any failure is reported, not plugged.
- [ ] The PR and the board backlog are referenced by repository identity.

### Lifecycle (synthesis fold)
- This is the subtree's synthesis task. Author `SYNTHESIS.md` at the fold location, report
  `engine_report_status { status: "completed", artifact_path: ".../design-ferric-1_0/SYNTHESIS.md" }`, then
  `engine_resume_suspended { target_task_id: <the design-ferric-1_0 root>, synthesized_task_id: <this task>,
  seam_path: ".../design-ferric-1_0/SYNTHESIS.md" }` to fold the parent SUSPENDED→COMPLETED.

### Constraints
- Do not modify `contracts/` or any sibling's output. Report composition honestly; no silent plugs.
- Honor the writing-voice rules; run the avoid-ai-writing pass over `SYNTHESIS.md` before finalizing.
- GitHub-referenced text names only repository identities; no host/system detail.
