# _GLOBAL.md — SUBTASK_verify_deliver subtree

## Project Context

**Parent task**: `SUBTASK_verify_deliver`  
**Parent workspace**: `taskflow/dags/remediate-epic-persist-r1/SUBTASK_verify_deliver/`  
**Parent task ID** (for synthesis fold): `SUBTASK_verify_deliver`

### Objective

Verify that PR #113 (`Nousix-LLC/nswe-demo`, branch `work/epic-persist`) CI checks — `doc`,
`clippy`, `fmt`, `test`, `wasm` — are all green on commit `e63e607`, then update PR #113 in place
with a clear, reader-facing description stating what changed, why, how it was verified, and which
issues it closes. Produce `VERIFICATION.md` at the parent workspace as the folded result.

### Scope

**In scope:**
- Observing CI check results on PR #113 for the current head commit (`e63e607`)
- Confirming the `doc` check is green (fresh run evidence — not inferred)
- Confirming `clippy`, `fmt`, `test`, `wasm` remain green (no durability regression)
- Updating PR #113 description via `gh` with a reader-facing narrative
- Producing `VERIFICATION.md` at `SUBTASK_verify_deliver/VERIFICATION.md`

**Out of scope:**
- Merging PR #113, pushing to main, or force-pushing anything
- Any source-code changes
- Opening a second PR (unless updating #113 is impossible — fallback: one PR into main closing #65/#66/#67)

### Constraints

- **Output hygiene (hard):** Nothing posted to GitHub (PR body, comments) may carry host/absolute
  paths, cluster/SSH/credential details, or taskflow/agent/run identifiers. Name everything by
  repository identity: `owner/repo`, issue/PR numbers, commit SHAs, repo-relative paths.
- **No attribution trailers** on any commits.
- **Never merge** PR #113 or push to `main`.

---

## Input Specifications

| Source | Path | Purpose |
|--------|------|---------|
| Ancestor hub | `../_GLOBAL.md` | Full project context and constraints |
| Changeset | `../SUBTASK_apply_fixes/CHANGESET.md` | What was changed (13 corrections, commit `e63e607`) |
| Inventory | `../SUBTASK_assess/INVENTORY.md` | The hazards that must now be clear |

---

## Task Structure

### Overview

```
SUBTASK_verify_deliver/          (this hub + parent workspace)
├── _GLOBAL.md                   (this file)
├── contracts/
│   └── _MANIFEST.yaml           (ownership and seam schema)
├── SUBTASK_ci_verify/
│   └── _BRIEF.md
├── SUBTASK_pr_update/
│   └── _BRIEF.md
└── SUBTASK_synthesis/
    └── _BRIEF.md
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_ci_verify` | none | Check all required CI checks on PR #113 (`doc`, `clippy`, `fmt`, `test`, `wasm`) are green on commit `e63e607`; record fresh evidence | `SUBTASK_ci_verify/CI_EVIDENCE.md` |
| `SUBTASK_pr_update` | `SUBTASK_ci_verify` | Update PR #113 description in place with a reader-facing narrative (what changed, why, how verified, issues closed) | `SUBTASK_pr_update/PR_UPDATE.md` |
| `SUBTASK_synthesis` | `SUBTASK_ci_verify`, `SUBTASK_pr_update` | Synthesize CI evidence + PR update confirmation into `VERIFICATION.md` at the parent workspace; fold parent task | `../VERIFICATION.md` |

### Dependency Graph

```
SUBTASK_ci_verify ──┬── SUBTASK_pr_update ──┐
                    └──────────────────────── SUBTASK_synthesis
```

---

## Contract

**Contract location**: `contracts/` (read-only for every descendant)  
**Contract kind**: `yaml_schema`

### Structural Declarations

| Artifact | Kind | Declares |
|---|---|---|
| `contracts/_MANIFEST.yaml` | `yaml_schema` | Per-child ownership, CI_EVIDENCE.md and PR_UPDATE.md output schemas |

### Ownership

| Artifact | Owning subtask |
|---|---|
| `SUBTASK_ci_verify/CI_EVIDENCE.md` | `SUBTASK_ci_verify` |
| `SUBTASK_pr_update/PR_UPDATE.md` | `SUBTASK_pr_update` |
| `../VERIFICATION.md` (at parent workspace) | `SUBTASK_synthesis` |

### Identities

Invariants the synthesis task evaluates as assertions (no silent plugs):

- [ ] **Blocker cleared**: `CI_EVIDENCE.md` records the `doc` check as PASSED with a fresh run
  reference on commit `e63e607` (not inferred from clearing the first error — evidenced).
- [ ] **No regression**: `CI_EVIDENCE.md` records `clippy`, `fmt`, `test`, `wasm` all PASSED on
  the same run.
- [ ] **Delivery confirmed**: `PR_UPDATE.md` confirms PR #113 was updated in place and is
  mergeable/clean; the update text is reader-facing and names what changed, why, how verified, and
  which issues (#65, #66, #67) it closes.
- [ ] **Output hygiene**: nothing in `PR_UPDATE.md` carries host/SSH/cluster/credential/taskflow
  details.

---

## Output Specifications

| Deliverable | Location | Description |
|-------------|----------|-------------|
| CI evidence | `SUBTASK_ci_verify/CI_EVIDENCE.md` | Per-check status and run reference |
| PR update record | `SUBTASK_pr_update/PR_UPDATE.md` | Confirmation of what was posted to GitHub |
| Verification record | `../VERIFICATION.md` | Fold record + declared output of parent task |
