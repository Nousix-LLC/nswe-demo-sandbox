# Task: hydrate_wasm.rs — Dimension 4: Duplication

## Task Specification

**Slug**: SUBTASK_dim-duplication
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-reviewer

### Objective

Assess duplication patterns in `hydrate_wasm.rs` (commit `75c1eef`): whether repeated
setup logic, teardown, or test scaffolding has been appropriately extracted into helpers,
and whether any copy-pasted blocks represent a maintenance or correctness risk. Produce
`finding.md` with a severity label and cited evidence.

### Context

This task is one of five parallel dimension spokes within SUBTASK_hydrate-wasm-quality
(see `../_GLOBAL.md`). It assesses exactly one dimension: duplication.

The file contains two helper functions already extracted: `make_container()` (creates a
`<div>` and appends to `<body>`) and `cleanup(el)` (removes the element). The question
is whether further duplication remains across the three test functions, and whether any
remaining repetition is meaningful (the content differs meaningfully) or accidental
(boilerplate copy-paste that should be extracted).

---

## Input Specification

| Input | Source | Purpose |
|---|---|---|
| Subtree hub | `../_GLOBAL.md` | Subtree constraints and shared context |
| `hydrate_wasm.rs` | commit `75c1eef` | Primary file for this dimension |

**Reading the file:**
```bash
gh api "repos/Nousix-LLC/nswe-demo/contents/crates/ferric/tests/hydrate_wasm.rs?ref=75c1eef776953993ddd62dba1436845a0d53a281" \
  --jq '.content' | base64 -d
```

---

## Dimension Scope

Assess duplication in `hydrate_wasm.rs`:

- Compare the three test functions: does each have a meaningfully distinct body, or
  is there a repeated structural pattern that should be extracted further?
- Specifically check whether repeated `innerHTML` injection, VNode tree construction,
  or hydration call patterns constitute boilerplate worth extracting vs. necessarily
  distinct per-test content.
- The `make_container` / `cleanup` helpers are already extracted. Confirm they cover
  the shared scaffolding, or note if they leave duplication.
- Distinguish between "the content is different but the structure is the same" (possibly
  worth a parameterized helper) and "the structure is the same AND the content is the
  same" (definite extraction candidate).

Do NOT assess: test naming, DOM cleanup strategy (whether cleanup is called on failure
paths — that is SUBTASK_dim-cleanup), hardcoded strings, or assertion quality.

---

## Output Specification

**File**: `finding.md`
**Location**: `SUBTASK_dim-duplication/`

```markdown
## Duplication

**Severity**: [Blocker | Warning | Pass]
**Evidence**: [hydrate_wasm.rs:line or N/A]

[Finding text — plain voice, concrete, citable]
```

Severity semantics:
- **Blocker**: Duplication is so extensive that a correctness fix in one copy would
  silently leave the others broken, or copy-paste has already created a divergence.
- **Warning**: Duplication is a real quality issue (extract candidate) but poses no
  immediate correctness risk.
- **Pass**: Helpers are extracted appropriately; remaining repetition is meaningfully
  distinct per-test content.

---

## Success Criteria

- [ ] All three test functions compared for structural duplication
- [ ] Existing helpers (`make_container`, `cleanup`) acknowledged
- [ ] Any remaining duplication assessed for extraction value
- [ ] Severity assigned with rationale
- [ ] Evidence cites specific line(s) or states N/A
- [ ] `finding.md` written to this task's workspace

---

## Methodology Guidance

**Primary**: `rust/Rust_Testing_Methodology.md` — Rust test code quality and DRY patterns
**Secondary**: `code-review/CodeReview_Checklist_Methodology.md` — duplication checklist

---

## Inherited Constraints

- **Repository**: Nousix-LLC/nswe-demo, commit `75c1eef776953993ddd62dba1436845a0d53a281`
- **Do not re-raise**: Issues #229–#242
- **Do not reference**: Overseer I267 escalation comments
- **Prose bar**: No AI-tell patterns in output text
- **Scope**: Code quality only — security scope belongs to SUBTASK_security
