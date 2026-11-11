# Task: Assemble the design into the repository and open the design PR

## Task Specification
**Slug**: SUBTASK_design_pr
**Task Kind**: standard
**Status**: Pending

### Objective
Assemble the completed design-area outputs and the release bar into the repository `design/` tree per
`../contracts/design_artifact_map.yaml`, on branch `work/design-chirp-r1`, and open **one** PR into `main`,
written for the repository's readers.

### Context
Part of design-chirp-r1 (see `../_GLOBAL.md`, `../contracts/`). You own the `design/` index (`design/README.md`)
and the PR itself; you do **not** author the section content (each concern task owns its file). Place each
produced file at its `repo_path` from the artifact map, generate the index, commit, push the branch, and open
the PR with a body that explains the design to the repo's readers and carries plain-text `Closes`/`Refs`
linkage to the relevant epics/issues as appropriate.
**Dependencies**: all five concern designs + `SUBTASK_release_bar`.
**Dependents**: `SUBTASK_delivery_backlog`, `SUBTASK_synthesis`.

## Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context/constraints |
| Contract | `../contracts/` (read-only) | The file→repo_path map, owners, and index requirements |
| All six produced design files | `../SUBTASK_*/outputs/*.md` (the five concerns + `release-bar.md`) | The content to assemble |
| Repo | `Nousix-LLC/nswe-demo` @ `c805525` | Clone into THIS workspace; branch `work/design-chirp-r1`; open PR into `main` |

## Output
- The branch `work/design-chirp-r1` pushed with the `design/` tree, and one open PR into `main`.
- `SUBTASK_design_pr/outputs/design-pr.md` recording the PR number/URL, the branch, and the assembled file map
  (for downstream tasks to reference). This local record may name the PR by its repo identity only.

## Success criteria
- [ ] Every file in `design_artifact_map.yaml` is present at its `repo_path`, each from its owning task's output
      (no section content authored or altered here; one owner per file preserved).
- [ ] `design/README.md` indexes the set per the artifact map.
- [ ] Exactly one PR into `main` from `work/design-chirp-r1`; `main` never force-pushed.
- [ ] The PR body reads for the repository's readers and carries no host/system/taskflow detail and no
      attribution trailer.

## Constraints
- Assembly and packaging only — do not edit the design content or write product code.
- Clone the repo into this task's own workspace (tasks do not share a working tree).
- Repository-ready hygiene on the branch, the commits, and the PR body (no host/system/taskflow detail; no
  attribution trailers — see #27/HYG-1).
