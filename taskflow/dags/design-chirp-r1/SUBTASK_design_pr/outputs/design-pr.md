# SUBTASK_design_pr — design PR record

Internal record for downstream tasks (`SUBTASK_delivery_backlog`, `SUBTASK_synthesis`). Not repository
content. Names the PR by repository identity; carries no host/system detail.

## The PR

- **PR**: `Nousix-LLC/nswe-demo#122`
- **URL**: https://github.com/Nousix-LLC/nswe-demo/pull/122
- **Title**: `design(chirp-r1): refresh the chirp product design and release bar`
- **Base → head**: `main` ← `work/design-chirp-r1`
- **State at assembly**: OPEN (into `main`; `main` never force-pushed)
- **Branch tip commit**: `b4b65f1` (branched from `main` at `276138f`)
- **Diff**: 7 files changed, +9744 / −11789 (updates the existing `design/` set in place)

## Assembled file map (design/ tree)

Each design file placed at its `repo_path` from `../contracts/design_artifact_map.yaml`, copied
byte-identical from its owning task's output (no section content authored or altered here). `design/README.md`
is the index, owned and authored by this task.

| repo_path | owning task | source output copied from |
|-----------|-------------|---------------------------|
| `design/README.md` | `SUBTASK_design_pr` | authored here (index generated per `design_artifact_map.yaml`) |
| `design/product-requirements.md` | `SUBTASK_product_requirements` | `SUBTASK_product_requirements/outputs/product-requirements.md` |
| `design/domain-application-design.md` | `SUBTASK_domain_app_design` | `SUBTASK_domain_app_design/outputs/domain-application-design.md` |
| `design/experience-design.md` | `SUBTASK_experience_design` | `SUBTASK_experience_design/outputs/experience-design.md` |
| `design/identity-security.md` | `SUBTASK_identity_trust` | `SUBTASK_identity_trust/outputs/identity-security.md` |
| `design/operational-readiness.md` | `SUBTASK_operational_readiness` | `SUBTASK_operational_readiness/SUBTASK_ops_synthesis/outputs/operational-readiness.md` |
| `design/release-bar.md` | `SUBTASK_release_bar` | `SUBTASK_release_bar/outputs/release-bar.md` |

Note: `operational-readiness.md` is taken from the ops subtree's synthesis-child output
(`SUBTASK_ops_synthesis/outputs/…`), which the ops `SYNTHESIS.md` fold record names as that subtree's
verified parent deliverable (the other five concerns place their consolidated output at the subtree-root
`outputs/`).

## Assembly checks (success criteria)

- [x] Every file in `design_artifact_map.yaml` present at its `repo_path`, each from its owning task's
      output; one owner per file preserved (six concern files copied byte-identical; README owned here).
- [x] `design/README.md` indexes the set per the artifact map (sections: overview, document index,
      how the bar and backlog relate).
- [x] Exactly one PR into `main` from `work/design-chirp-r1` opened in this invocation (#122); `main`
      never force-pushed.
- [x] PR body reads for the repository's readers; carries no host/system/taskflow detail and no
      attribution trailer (re-scanned clean). Commit message carries no attribution trailer.

## Reconstruction note (for downstream and synthesis)

This node was reconstructed and re-dispatched; in this run it had not previously completed (only its
`_BRIEF.md` was present). A prior run's design PR (`Nousix-LLC/nswe-demo#33`) is already MERGED on `main`
and carried the first-run design. The current canonical concern outputs on disk differ from that merged
set across all six files (the design was revised/reconciled after #33 via the subtree's remediation),
so this node assembled the **current** outputs and opened #122 to bring `design/` to the current design
rather than re-recording the stale #33. `design/` reaches the current state on `main` when #122 lands;
until then `main` still shows the #33 design. Downstream tasks that read the design should read the
current on-disk concern outputs (the owning-task sources above) and treat #122 as the vehicle delivering
them to `main`.

## Environment note

The Phase-B `design`-domain methodology loader was unreachable in this reconstructed node
(`agent_domain_unset`); this assembly/packaging task is fully specified by `_BRIEF.md`, `../_GLOBAL.md`,
and `../contracts/`, which were sufficient. Recorded for transparency.
