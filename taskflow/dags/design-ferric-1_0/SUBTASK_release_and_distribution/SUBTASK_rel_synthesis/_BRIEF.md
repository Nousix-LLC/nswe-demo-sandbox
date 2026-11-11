# Task: Ferric 1.0 — release & distribution synthesis (merge + fold)

## Task Specification
**Slug**: SUBTASK_rel_synthesis
**Task Kind**: synthesis
**Status**: Pending

### Objective
Merge the three spoke partials into the single consolidated `release-and-distribution.md` carrying the complete
`REQ-REL-*` register, assert the sub-contract merge identities, and fold this concern's parent task.

### Context
This is the synthesis gate for concern 7, release & distribution (subtree hub: `../_GLOBAL.md`). The three
spokes each designed one facet into its own partial with a disjoint `REQ-REL-*` range; this task reassembles
them into one coherent design doc in the repo's design-doc shape and verifies the parts composed. It is the
node that integrates its siblings' combined output — the parent's declared output does not exist until this
task produces it.

**Dependencies**: `SUBTASK_publishing`, `SUBTASK_semver_changelog`, `SUBTASK_versioning_compat`.

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, the merge identities J1–J7, the output spec. |
| Sub-contract | `../contracts/_MANIFEST.yaml` | The REQ-REL partition and the identities to assert. |
| Parent contract | `../../contracts/id_and_traceability_schema.yaml`, `../../contracts/_MANIFEST.yaml` | The schema to conform to and the parent identities (I1) this concern must respect. |
| Publishing partial | `../SUBTASK_publishing/publishing.md` | `REQ-REL-001..019` + publishing design. |
| Semver/changelog partial | `../SUBTASK_semver_changelog/semver-changelog.md` | `REQ-REL-020..039` + semver/changelog design. |
| Versioning/compat partial | `../SUBTASK_versioning_compat/versioning-compat.md` | `REQ-REL-040..059` + policy design. |
| Repo doc shape | `../../SUBTASK_scope_and_requirements/scope-and-requirements.md` | The design-doc shape (sections, Metadata) to match. |

### What this task produces
- **`../release-and-distribution.md`** — the parent task's declared output, at the subtree root: one coherent
  release & distribution design (publishing readiness, the semver contract, the changelog practice, the 1.0
  versioning & compatibility policy) with the full merged `REQ-REL-*` register, named-peer comparison, and a
  Metadata section naming the owning task and the `conforms_to` contract. Repo target
  `design/ferric/release-and-distribution.md`.
- **`../SYNTHESIS.md`** — the fold record at the fold location (the parent `SUBTASK_release_and_distribution`
  workspace): what was merged, the identity-assertion results (J1–J7, and parent I1 for the REL register), and
  any gaps surfaced (never silently plugged).

### How to resolve
Merge, do not re-derive: pull each spoke's `REQ-REL-*` entries verbatim into one register, preserving ids.
Assert the identities mechanically; if one fails (an id collision, a range violation, a missing concern, a
missing MSRV/frozen-surface promise, an unconformant criterion), record it as a structured gap and surface it
rather than inventing a plug. Then fold: author `../SYNTHESIS.md`, report `status="completed"` with
`artifact_path` the `SYNTHESIS.md`, and call `engine_resume_suspended` to flip the parent
`SUBTASK_release_and_distribution` from SUSPENDED to COMPLETED with the merged doc as its output.

### Success criteria
- [ ] `../release-and-distribution.md` exists, carries the complete `REQ-REL-*` register with no range
      gaps/overlaps, and matches the repo design-doc shape (identity J7).
- [ ] Identities J1–J7 asserted with results recorded in `../SYNTHESIS.md`; any failure surfaced, not plugged.
- [ ] The parent REL register respects parent identity I1 (only `REQ-REL-*` ids written).

### Constraints
- Merge and verify, not re-design. Honor the writing-voice rules in `../_GLOBAL.md` over the final doc (run the
  avoid-ai-writing pass). Design, not implementation.
