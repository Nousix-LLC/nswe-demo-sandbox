# Concern 2 (Code Quality) — Decomposition Hub

## Project Context

**Status**: Active

### Objective

Examine the four design questions in Concern 2 of PR #193 — (Q1) responsibility partitioning and coupling, (Q2) EventHandler abstraction boundary, (Q3) generation counter clarity in `create_resource`, (Q4) correct-use design — through four independent spoke tasks, then synthesize findings into `partial_findings.md` at this workspace root.

### Scope

**In Scope:**
- Concern 2 design questions only (Q1–Q4)
- Files: `crates/ferric/src/async_resource.rs`, `crates/ferric/src/vdom.rs`, `crates/ferric/src/dom.rs`, `crates/ferric/src/form.rs`

**Out of Scope:**
- Concerns 1, 3, 4, 5, 6, 7 — covered by sibling tasks
- Issues #196–#201 — already filed; must not be re-raised

### Success Criteria

- [ ] All four design questions answered with evidence from actual code
- [ ] `partial_findings.md` produced at this workspace root, conforming to `../contracts/findings_format.md`
- [ ] `SYNTHESIS.md` fold record produced at this workspace root

---

## Shared Inputs

Each spoke reads the following inputs independently.

| Input | Source | Purpose |
|-------|--------|---------|
| Parent context | `../_GLOBAL.md` | Inherited constraints, scope |
| Findings format contract | `../contracts/findings_format.md` | Required output schema for partial_findings.md |
| PR #193 diff | `gh pr diff 193 --repo Nousix-LLC/nswe-demo` | Changed lines for context |
| async_resource.rs | `crates/ferric/src/async_resource.rs` | B1: implementation and new tests |
| vdom.rs | `crates/ferric/src/vdom.rs` | B2: EventHandler enum |
| dom.rs | `crates/ferric/src/dom.rs` | B2: dispatch + WASM test |
| form.rs | `crates/ferric/src/form.rs` | B3: on_input_event_handler + WASM test |

---

## Inherited Constraints

- Repository-relative paths only in all findings (e.g., `crates/ferric/src/async_resource.rs:42`)
- Issues #196–#201 MUST NOT be re-raised
- Severity `blocker` only if a stated requirement is unmet or an existing public API contract is broken for callers; style/preference = at most `non-blocker`
- Concerns 1, 3, 4, 5, 6, 7 are out of scope
- Concern label for all entries in this subtree: `code-quality`

---

## Parent Task

**Suspended task ID:** `SUBTASK_concern2_code_quality`  
**Fold location (SYNTHESIS.md):** This workspace (the `_GLOBAL.md` directory above)  
The synthesis child MUST call `engine_resume_suspended { target_task_id: "SUBTASK_concern2_code_quality", ... }` after producing `../partial_findings.md` and `SYNTHESIS.md` at this workspace.

---

## Task Structure

### Overview

```
_GLOBAL.md (this document)
├── contracts/
│   └── _MANIFEST.yaml
├── SUBTASK_q1_coupling/
│   └── _BRIEF.md
├── SUBTASK_q2_eventhandler/
│   └── _BRIEF.md
├── SUBTASK_q3_gen_counter/
│   └── _BRIEF.md
├── SUBTASK_q4_correct_use/
│   └── _BRIEF.md
└── SUBTASK_cq_synthesis/
    └── _BRIEF.md
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_q1_coupling` | none | Q1: Responsibility partitioning and coupling across all 4 files | `sub_findings.md` |
| `SUBTASK_q2_eventhandler` | none | Q2: EventHandler abstraction boundary (vdom.rs, dom.rs) | `sub_findings.md` |
| `SUBTASK_q3_gen_counter` | none | Q3: Generation counter clarity in create_resource (async_resource.rs) | `sub_findings.md` |
| `SUBTASK_q4_correct_use` | none | Q4: Correct-use design across all 4 files | `sub_findings.md` |
| `SUBTASK_cq_synthesis` | `SUBTASK_q1_coupling`, `SUBTASK_q2_eventhandler`, `SUBTASK_q3_gen_counter`, `SUBTASK_q4_correct_use` | Synthesize sub-findings into partial_findings.md, write SYNTHESIS.md fold record | `../partial_findings.md`, `SYNTHESIS.md` |

### Dependency Graph

```
SUBTASK_q1_coupling      ──┐
SUBTASK_q2_eventhandler  ──┼── SUBTASK_cq_synthesis
SUBTASK_q3_gen_counter   ──┤
SUBTASK_q4_correct_use   ──┘
```

---

## Contract

**Contract location:** `contracts/`
**Contract kind:** `yaml_schema`

### Structural Declarations

Each spoke MUST produce `sub_findings.md` using the same section format declared in the parent's `../contracts/findings_format.md` — two required sections (`## Findings` and `## What was examined`).

| Artifact | Kind | Declares |
|---|---|---|
| `contracts/_MANIFEST.yaml` | manifest | Ownership, identities, sub-finding format |

### Ownership

| Artifact | Owning subtask |
|---|---|
| `SUBTASK_q1_coupling/sub_findings.md` | `SUBTASK_q1_coupling` |
| `SUBTASK_q2_eventhandler/sub_findings.md` | `SUBTASK_q2_eventhandler` |
| `SUBTASK_q3_gen_counter/sub_findings.md` | `SUBTASK_q3_gen_counter` |
| `SUBTASK_q4_correct_use/sub_findings.md` | `SUBTASK_q4_correct_use` |
| `../partial_findings.md` | `SUBTASK_cq_synthesis` |
| `SYNTHESIS.md` | `SUBTASK_cq_synthesis` |

### Identities

- [ ] All `sub_findings.md` use `concern: code-quality` label
- [ ] No finding duplicates issues #196–#201
- [ ] Each sub-question (Q1–Q4) addressed by exactly one spoke
- [ ] `../partial_findings.md` conforms to `../contracts/findings_format.md`

---

## Subtree Methodology Posture

**Dominant task type:** Ferric PR review (Rust library) → `code-review` primary, `rust` + `framework-design` supporting

**Primary bundles all spokes draw on:** `code-review`, `framework-design`, `code-quality`

**Cross-cutting bindings:**
- `code-review/CodeReview_Checklist_Methodology.md` — review-process discipline for all 4 spoke tasks
- `framework-design/FrameworkDesign_Library_API_Design_Methodology.md` — abstraction boundary and correct-use criteria (especially Q2 and Q4)
- `code-quality/Framework_Clean_Code_Methodology.md` — single responsibility, cohesion, naming clarity (especially Q1 and Q3)

Dispatched agents are the final judges of what they actually need; these are starting-point suggestions.
