# Concern 7 API Stability — Subtree Hub

## Project Context

**Status**: Active
**Parent**: SUBTASK_quality_tests_idiom / review-ferric-async-forms-r3

### Objective

Produce `partial_findings.md` at this workspace root, containing API and contract stability findings for PR #193, conforming to the shared findings contract at `../contracts/findings_format.md`.

### Prior Work

A prior atomic execution of this task already analyzed the PR in full and produced `findings_concern7.md` at this workspace. That file contains 6 structured findings (C7-1 through C7-6) with complete evidence, covering all three sub-questions from the brief:

1. `EventHandler` backward compatibility — C7-1 and C7-2 (both clean)
2. `on_input_event_handler()` on `Bind<T>` documentation/naming — C7-4 (clean)
3. `create_resource` naming and conventions — C7-5 (clean)
4. Cross-cutting: C7-3 and C7-6 (non-blockers: EventHandler missing from prelude; `#[non_exhaustive]` missing)

### Scope

**In scope**: Reformatting `findings_concern7.md` into the declared output `partial_findings.md` with correct section headers per `../contracts/findings_format.md`, then folding the parent.

**Out of scope**: Re-analyzing the PR diff or source code (already done); re-raising issues #196–#201.

### Success Criteria

- [ ] `partial_findings.md` exists at this workspace root
- [ ] It contains `## Findings` and `## What was examined` sections
- [ ] All findings use `concern: api-stability`
- [ ] No issue from #196–#201 is re-raised
- [ ] `SYNTHESIS.md` exists at this workspace root (fold record)

---

## Task Structure

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_produce_partial_findings` | none | Read `findings_concern7.md`, reformat to `partial_findings.md` conforming to `../contracts/findings_format.md`, fold parent via `SYNTHESIS.md` | `partial_findings.md` at parent workspace, `SYNTHESIS.md` at parent workspace |

---

## Contract

**Contract location**: `contracts/`
**Contract kind**: inherited from parent + local format constraint

### Inherited Contracts

| Ancestor contract | Path | What it binds here |
|---|---|---|
| Findings format | `../contracts/findings_format.md` | Required section headers and finding entry structure for `partial_findings.md` |

### Structural Declarations

| Artifact | Kind | Declares |
|---|---|---|
| `contracts/_MANIFEST.yaml` | yaml_schema | Per-child ownership and identities |

### Ownership

| Artifact | Owning subtask |
|---|---|
| `partial_findings.md` | `SUBTASK_produce_partial_findings` |
| `SYNTHESIS.md` | `SUBTASK_produce_partial_findings` |

### Identities

- [ ] `partial_findings.md` contains exactly `## Findings` as the top-level findings section header
- [ ] `partial_findings.md` contains exactly `## What was examined` as the examination section header
- [ ] All findings entries use `concern: api-stability`
- [ ] No finding re-raises issues #196–#201

---

## Subtree Methodology Posture

**Dominant task type**: Ferric PR review (Rust library) — verification/reformatting node
**Primary bundles**: code-review, rust
**Cross-cutting bindings**: findings_format.md contract (from parent contracts/)
