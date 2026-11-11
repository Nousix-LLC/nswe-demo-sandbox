# Correctness and Concurrency Review — Decomposition Hub

## Context

This is the subtree hub for the SUBTASK_correctness_concurrency node of
review-ferric-async-forms-r3. The parent node's brief covers three distinct
file-level analysis areas (async_resource.rs for B1+concurrency; vdom.rs/dom.rs
for B2; form.rs for B3), each independently verifiable. This decomposition
dispatches them as parallel spokes with a synthesis gate producing the final findings.md.

**Repository**: Nousix-LLC/nswe-demo  
**Branch**: work/ferric-async-forms-r2  
**PR**: #193 — Head SHA: 838239e  
**Parent brief**: SUBTASK_correctness_concurrency/_BRIEF.md  
**Ancestor context**: review-ferric-async-forms-r3/_GLOBAL.md  
**Inherited contract**: review-ferric-async-forms-r3/contracts/_MANIFEST.yaml

## Scope

Verify correctness of three remediation blockers from review-ferric-async-forms-r2:
- **B1 (REQ-ASYNC-001, 003, 005, 016)**: create_resource reactive constructor in async_resource.rs
- **B2 (REQ-ASYNC-023)**: EventHandler enum redesign in vdom.rs and dom.rs
- **B3 (REQ-ASYNC-042)**: Bind::on_input_event_handler() in form.rs
- **Concurrency**: spawn_local/reactive-effect composition hazards (async_resource.rs)

## Constraints

- Findings derive from actual source code, not from taskflow synthesis docs
- Repository-relative paths only (no host paths, no taskflow paths)
- Non-blockers previously filed as #196–#201 must NOT be re-raised as blockers
- Severity: blocker = requirement unmet; preference = at most non-blocker
- Final findings.md must be written at SUBTASK_correctness_concurrency/findings.md

## Task Structure

```
SUBTASK_correctness_concurrency/
├── _GLOBAL.md                        (this document)
├── contracts/_MANIFEST.yaml          (sub-schema, ownership, identities)
├── SUBTASK_b1_concurrency/           (B1 + concurrency analysis of async_resource.rs)
│   └── _BRIEF.md
├── SUBTASK_b2_event/                 (B2 analysis of vdom.rs + dom.rs)
│   └── _BRIEF.md
├── SUBTASK_b3_form/                  (B3 analysis of form.rs)
│   └── _BRIEF.md
└── SUBTASK_findings_synthesis/       (synthesis: collects spokes → findings.md)
    └── _BRIEF.md
```

## Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_b1_concurrency` | none | B1 + concurrency: verify create_resource in async_resource.rs; assess spawn_local/generation-counter safety | `SUBTASK_b1_concurrency/b1_findings.md` |
| `SUBTASK_b2_event` | none | B2: verify EventHandler enum in vdom.rs + dom.rs dispatch in dom.rs | `SUBTASK_b2_event/b2_findings.md` |
| `SUBTASK_b3_form` | none | B3: verify Bind::on_input_event_handler() in form.rs | `SUBTASK_b3_form/b3_findings.md` |
| `SUBTASK_findings_synthesis` | `SUBTASK_b1_concurrency`, `SUBTASK_b2_event`, `SUBTASK_b3_form` | Collect spoke findings into findings.md at parent workspace root | `../findings.md` |

## Dependency Graph

```
SUBTASK_b1_concurrency ──┐
                          │
SUBTASK_b2_event       ──┼── SUBTASK_findings_synthesis
                          │
SUBTASK_b3_form        ──┘
```

## Contract

**Contract location**: `SUBTASK_correctness_concurrency/contracts/` (read-only for descendants)
**Contract kind**: yaml_schema

See `contracts/_MANIFEST.yaml` for sub-findings ownership and identities.

## Output

The final deliverable of this decomposition is:
`SUBTASK_correctness_concurrency/findings.md`

Produced by SUBTASK_findings_synthesis, following the schema from both:
- `review-ferric-async-forms-r3/contracts/_MANIFEST.yaml` (ancestor)
- `SUBTASK_correctness_concurrency/contracts/_MANIFEST.yaml` (this level)
