# _BRIEF.md — SUBTASK_release-bar-quality

## Task Specification

**Slug**: SUBTASK_release-bar-quality  
**Task Kind**: standard  
**Depends on**: none  
**Status**: Pending

### Objective

Read `release-bar.md` and the design files that inform it. Evaluate each BAR-FERRIC-* item: is it stated as a concrete, independently verifiable criterion, or as aspiration? Record every item that an outside reviewer could not check — either because it is phrased as a hope rather than a fact, or because it lacks a specific threshold, reference, or observable outcome.

### Context

This task is part of the design-doc-review subtree (see `_GLOBAL.md` in the parent workspace at `taskflow/dags/design-ferric-1_0-r3/SUBTASK_design-doc-review/`).

This is review **concern 2**: release bar quality. The question is not whether the release bar is ambitious but whether an outside reviewer, reading each BAR-FERRIC-* item against the shipped product, could reach the same pass/fail verdict you would. A bar item that requires being in the room to interpret is a BLOCKING gap.

**Depends on**: none (runs in parallel with SUBTASK_completeness-review and SUBTASK_traceability-review)  
**Dependents**: SUBTASK_findings-synthesis depends on this task's output

---

## Inputs

| Input | Source | Purpose |
|---|---|---|
| Parent hub (design-doc-review) | `taskflow/dags/design-ferric-1_0-r3/SUBTASK_design-doc-review/_GLOBAL.md` | Shared context |
| Subtree hub (ferric review) | `taskflow/dags/design-ferric-1_0-r3/_GLOBAL.md` | Project-level context and verdict rules |
| Findings schema | `taskflow/dags/design-ferric-1_0-r3/SUBTASK_design-doc-review/contracts/spoke_findings_schema.yaml` | Output format contract |
| release-bar.md | `git show origin/work/design-ferric-1_0:design/ferric/release-bar.md` from `taskflow/dags/ferric-foundation/checkout/` | Primary review material: the release bar |
| scope-and-requirements.md | `git show origin/work/design-ferric-1_0:design/ferric/scope-and-requirements.md` from `taskflow/dags/ferric-foundation/checkout/` | Context for bar items tied to REQ-* IDs |

Other design files may be read as supporting context if needed to evaluate a specific bar item. The parent hub (`_GLOBAL.md`) lists all 14 files with their access commands.

### Methodology

Load and apply from `infrastructure/methodologies/design/`:

- `release-definition/ReleaseDefinition_ReleaseBar_Methodology.md`

This methodology defines what makes a release bar item concrete and independently testable versus aspirational, and how to audit each item for verifiability.

---

## Output

| Attribute | Value |
|---|---|
| Filename | `release-bar-findings.yaml` |
| Format | YAML conforming to `contracts/spoke_findings_schema.yaml` |
| Location | this workspace (`SUBTASK_release-bar-quality/`) |

The output is a YAML file with:
- `spoke: design-doc-review`
- `concern_ids: [2]`
- `findings: [...]` — one entry per bar item that cannot be verified, each with `id` (DDR-B-NNN), `severity`, `concern: 2`, `location` (specific BAR-FERRIC-* ID and section), `statement`, `recommendation`
- `summary: { blocking_count, non_blocking_count }`

A finding is BLOCKING if the bar item is not independently verifiable by an outside reviewer (aspirational language, missing threshold, missing observable outcome).

---

## Success Criteria

- `release-bar.md` read in full.
- Every BAR-FERRIC-* item evaluated for testability by an outside reviewer.
- Each non-verifiable item recorded as a finding with the specific BAR-FERRIC-* ID in the location field.
- Output file `release-bar-findings.yaml` written conforming to the spoke findings schema.
- No finding omits `severity`, `location`, `statement`, or `recommendation`.
