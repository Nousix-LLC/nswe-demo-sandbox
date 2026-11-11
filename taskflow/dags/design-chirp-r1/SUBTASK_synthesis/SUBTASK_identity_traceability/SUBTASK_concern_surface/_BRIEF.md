# Task: Assert CONCERN_COVERAGE and SURFACE_COVERAGE over the design set

## Task Specification
**Slug**: SUBTASK_concern_surface
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective
Inspect the assembled design set and assert the two coverage identities with recorded evidence:
**`CONCERN_COVERAGE`** (each of the six brief concerns is covered by a design file or recorded out-of-scope with a
reason) and **`SURFACE_COVERAGE`** (each recurring account/operational surface is designed or recorded out-of-scope
with a reason).

### Context
Part of `SUBTASK_identity_traceability` (see `../_GLOBAL.md`). This spoke owns the two coverage-inspection
identities. It builds no matrix columns and asserts no other identity. Both are coverage inspections over the same
design corpus (the five area designs plus the release bar's surfaces sweep), which is why they are one spoke; judge
your own atomic-vs-decompose decision against that honestly and decompose if warranted.

**Dependencies**: none. **Dependents**: `SUBTASK_assemble`.

### Inputs
| Input | Source (from this workspace) | Purpose |
|-------|------------------------------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints |
| Subtree sub-contract | `../contracts/_MANIFEST.yaml` | The `CONCERN_COVERAGE` + `SURFACE_COVERAGE` assignments — READ-ONLY |
| DAG-root identities | `../../../contracts/_MANIFEST.yaml` | The exact `CONCERN_COVERAGE` and `SURFACE_COVERAGE` statements; the enumerated surfaces |
| Design-artifact map | `../../../contracts/design_artifact_map.yaml` | Which design file carries which concern + the required sections |
| Five area designs | `../../../SUBTASK_product_requirements/outputs/product-requirements.md`, `../../../SUBTASK_domain_app_design/outputs/domain-application-design.md`, `../../../SUBTASK_experience_design/outputs/experience-design.md`, `../../../SUBTASK_identity_trust/outputs/identity-security.md`, `../../../SUBTASK_operational_readiness/SUBTASK_ops_synthesis/outputs/operational-readiness.md` | The designed concerns and surfaces |
| Release bar surfaces sweep | `../../../SUBTASK_release_bar/outputs/release-bar.md` (the completeness-and-gap-review / Product Surfaces section) | The per-surface in/out-of-scope judgments, with reasons and `BAR-*` refs |

The recurring surfaces `SURFACE_COVERAGE` enumerates are at least: sign-up, sign-in, recovery, account deletion,
data export, onboarding, settings, notifications, admin/support, and billing. The six brief concerns are those named
in the inherited `CONCERN_COVERAGE` statement and the design-artifact map's concern files.

### Output
- `outputs/concern-surface.md` — containing:
  1. **`CONCERN_COVERAGE`** verdict (`PASS`/`FAIL`) with evidence: a per-concern line naming the covering design
     file/section, or the recorded out-of-scope reason. On `FAIL`, name the uncovered concern.
  2. **`SURFACE_COVERAGE`** verdict (`PASS`/`FAIL`) with evidence: a per-surface line naming where the surface is
     designed (design file/section and/or the bar's surfaces-sweep judgment and `BAR-*` refs), or the recorded
     out-of-scope reason. On `FAIL`, name the surface that is neither designed nor consciously out-of-scope, and say
     whether it is fixable.

### Success criteria
- [ ] Each of the six concerns has an explicit covered / out-of-scope-with-reason disposition; `CONCERN_COVERAGE`
      carries a `PASS`/`FAIL` verdict with evidence.
- [ ] Each enumerated surface has an explicit designed / out-of-scope-with-reason disposition citing the design
      location or bar judgment; `SURFACE_COVERAGE` carries a `PASS`/`FAIL` verdict with evidence.
- [ ] A surface or concern that is simply absent (neither designed nor consciously scoped out) is reported as a
      `FAIL` with specifics, not silently treated as covered.

### Constraints
- Own only `CONCERN_COVERAGE` + `SURFACE_COVERAGE`; build no matrix columns, assert no other identity.
- Read-only over completed inputs; report findings, do not edit the designs or bar.
- The `design` methodology loader is unavailable run-wide (`agent_domain_unset`); record the limitation and proceed.
- Output carries no host/system/taskflow detail and no attribution trailer.
