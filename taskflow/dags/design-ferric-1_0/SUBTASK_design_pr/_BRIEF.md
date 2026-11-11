# Task: Ferric 1.0 — assemble the design and open the PR (delivery)

## Task Specification
**Slug**: SUBTASK_design_pr
**Task Kind**: standard
**Status**: Pending

### Objective
Deliver the Ferric 1.0 design as **one reviewable PR**: place every owned design artifact at its mapped repo
path under `design/ferric/`, author the `design/ferric/README.md` index, ship the contract schema alongside,
on branch `work/design-ferric-1_0`, and open one PR into `main`.

### Context
Part of the Ferric 1.0 framework design (see `../_GLOBAL.md`). The design docs are the declared outputs of the
upstream spokes, each in its own workspace; this task gathers them per `../contracts/design_artifact_map.yaml`
and publishes them. It writes no design content of its own except the index README.

**Dependencies**: `SUBTASK_scope_and_requirements`, all seven capability spokes, `SUBTASK_release_bar`, and
`SUBTASK_release_plan` (every design artifact must exist before assembly).

### What to do (approach, not a runbook)
- Clone `Nousix-LLC/nswe-demo`, create branch `work/design-ferric-1_0` off `main`.
- Copy each artifact from its owner's workspace to its `repo_path` per `../contracts/design_artifact_map.yaml`
  (identity I8 — each doc placed exactly once).
- Author `design/ferric/README.md` (an index: the doc list, how the bar and backlog relate, where the release
  bar lives), mirroring the existing `design/README.md`.
- Copy the contract (`id_and_traceability_schema.yaml`, `design_artifact_map.yaml`) into
  `design/ferric/contracts/` so the REQ/BAR scheme is documented in-repo.
- Commit, push, open one PR into `main` with a description summarizing the design and the release bar.

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context + constraints. |
| Artifact map | `../contracts/design_artifact_map.yaml` | Where each doc lands (authoritative). |
| Design artifacts | each `../SUBTASK_*/<file>.md` (owners' workspaces) | The docs to place. |
| Contract schema | `../contracts/id_and_traceability_schema.yaml`, `_MANIFEST.yaml` | Ships with the design. |
| Repo precedent | `design/README.md` | The index shape to match. |

### Declared output
- `design_pr.md` (this task's workspace) — a record of the PR: branch, commit, PR number/URL, and the list of
  files placed with their repo paths.

### Success criteria
- [ ] Branch `work/design-ferric-1_0` carries every mapped artifact at its `repo_path`, placed exactly once
      (identity I8), plus the index README and the contract copy.
- [ ] Exactly one PR into `main` is open, its description written for the repository's readers.
- [ ] The PR record (`design_pr.md`) states the branch, commit, and PR number/URL.

### Constraints
- Repo scope `Nousix-LLC/nswe-demo` only; branch `work/design-ferric-1_0`; never force-push `main`.
- **No attribution trailers** on the commit or PR; nothing on GitHub carries host, cluster, SSH, path, or any
  system/environment detail. Name only repository identities.
- Do not alter the design docs' content; place them as delivered (fix only obvious path/link glue).
