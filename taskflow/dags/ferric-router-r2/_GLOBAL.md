# ferric-router-r2 — Remediation DAG

**Status**: Active  
**Branch under construction**: `work/ferric-router-r2`  
**PR being remediated**: #192 (`work/ferric-router-r1` → `main`)  
**Review verdict**: REQUEST CHANGES — blocker B1 (undescribed scope bundled in PR)  
**Review artifact**: `taskflow/dags/review-ferric-router-r1/SYNTHESIS.md`  
**Observation seam**: `taskflow/dags/ferric-router-r2/SYNTHESIS.md` (read by overseer)

---

## Project Context

### Objective

Resolve blocker B1 from review-ferric-router-r1 by splitting PR #192 into its two distinct scopes:

1. **Router scope** (router-only PR): Cherry-pick the 3 router commits from `work/ferric-router-r1` onto a clean `work/ferric-router-r2` branch and open a focused PR closing #131, #146, #147. These commits already passed all review checks.
2. **Macros/context scope** (assessment only): Analyze the 12 ferric-macros and ferric context API commits that were bundled into PR #192 without a review brief; produce a scope document and PR brief template so a follow-on review can be properly commissioned.

### Scope

**In Scope:**
- Creating `work/ferric-router-r2` with **only** the 3 router commits
- Opening a router-only PR with correct closing keywords for #131, #146, #147
- Assessing the ferric-macros commits for scope, complexity, and actionability
- Writing the structured assessment that the overseer can use to commission the macros PR

**Out of Scope:**
- Reviewing `crates/ferric-macros/` in detail (that belongs in a dedicated review task)
- Modifying any macros code
- Merging the router PR (that is the overseer's decision after CI passes)

### Success Criteria

- [ ] `work/ferric-router-r2` branch exists on remote with exactly 3 router commits (`89687da`, `cab18b9`, `3868b2c`)
- [ ] A PR is open from `work/ferric-router-r2` → `main` with correct title, body, and `Closes` keywords
- [ ] The macros assessment document exists with: scope summary, issue-to-commit mapping, size estimate, suggested review brief outline
- [ ] Synthesis folds the two outputs and declares the remediation attempt complete or escalated

---

## Background: What the Review Found

The review (see `review-ferric-router-r1/SYNTHESIS.md`) gave:
- **Router scope (3 commits)**: PASS on all checks (correctness, quality, tests, security, Rust idioms, API stability)
- **Macros/context scope (~12 commits)**: NOT REVIEWED — no acceptance criteria were provided, so the reviewer could not evaluate ~3,290 lines of proc-macro code

The 3 router commits (purely in `crates/ferric-router/`):
| Commit | Description | Issues closed |
|--------|-------------|---------------|
| `89687da` | `feat(ferric-router): add navigate_replace (REQ-RT-003)` | #131 |
| `cab18b9` | `ferric-router: active-route awareness on Link::build() (REQ-RT-007)` | #146 |
| `3868b2c` | `feat(ferric-router): nested routes, replace navigation, active links (r1 spoke completions)` | #147 |

The 12 macros/ferric commits (in `crates/ferric-macros/` and `crates/ferric/`):
| Commit | Description |
|--------|-------------|
| `e29e2f4` | `fix(ci): resolve fmt, clippy, and rustdoc failures on ferric-macros` |
| `763f4d6` | `feat(ferric-macros): add compile-fail diagnostic suite for component authoring mistakes (#141)` |
| `82d267f` | `feat(ferric): implement context API — provide_context, use_context, expect_context (#142)` |
| `0088a5c` | `feat(ferric): implement #[component] macro, Children/Slot/SlotFn types (#140)` |
| `d027534` | `fix(conformance): resolve VElement::into() type ambiguity in test_nested_element` |
| `c28b0e1` | `fix(ferric): re-export VElement, VNode, EventKind at crate root` |
| `4c77b9a` | `test(ferric-macros): conformance tests for view! lowering table (§2.12)` |
| `3c3d4aa` | `feat(ferric-macros): implement view! macro (#139)` |
| `d25a7f7` | `feat(ferric-macros): implement full view! proc-macro (sec 2.12 + 2.9)` |
| `912ed57` | `ferric: wire ferric-macros dependency and re-export view! in prelude` |
| `3be2f51` | `feat(ferric-macros): scaffold proc-macro crate with stub view! macro` |
| `1ccdce0` | `test(ferric): baseline audit — #137 and #138 ACs satisfied` |

The ferric-macros commits close issues #137–#142.

---

## Task Structure

```
_GLOBAL.md (this document)
├── contracts/_MANIFEST.yaml
├── SUBTASK_router-branch/_BRIEF.md
├── SUBTASK_macros-assessment/_BRIEF.md
└── SUBTASK_synthesis/_BRIEF.md
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_router-branch` | none | Cherry-pick 3 router commits onto `work/ferric-router-r2`; open focused PR | `outputs/router-pr.md` |
| `SUBTASK_macros-assessment` | none | Assess the 12 macros/ferric commits; produce scope document | `outputs/macros-assessment.md` |
| `SUBTASK_synthesis` | `SUBTASK_router-branch`, `SUBTASK_macros-assessment` | Verify both outputs; fold results | `SYNTHESIS.md` |

### Dependency Graph

```
SUBTASK_router-branch      ──┐
                              ├── SUBTASK_synthesis
SUBTASK_macros-assessment  ──┘
```

---

## Subtree Methodology Posture

**Dominant task types**: Git workflow / PR creation (router-branch) + Code review / assessment (macros-assessment) + Synthesis/verification (synthesis)

**Primary bundles**:
- `operations` (GitWorkflow_PR_Lifecycle, GitWorkflow_Syscall_PR_Review) — for router-branch spoke
- `code-review` + `rust` — for macros-assessment spoke
- `synthesis` — for the synthesis gate

**Cross-cutting bindings**:
- All tasks operate on the `nswe-demo` repo via SSH per CLAUDE.md conventions
- Server: `mattm@100.90.75.93` with key `~/.ssh/nousix_server_ed25519`
- Repository path on server: `/home/user/nswe-demo`
- Run all git/kubectl commands through SSH; use `bash -lc` to load server PATH

---

## Contract

**Contract location**: `contracts/`  
**Contract kind**: `yaml_schema` (thin ownership + identities manifest)

The two spokes produce independent outputs consumed by the synthesis gate; there is no shared structural seam between them. The contract declares ownership boundaries and the identities the synthesis gate MUST verify.

### Ownership

| Artifact | Owning subtask |
|----------|---------------|
| `outputs/router-pr.md` | `SUBTASK_router-branch` |
| `outputs/macros-assessment.md` | `SUBTASK_macros-assessment` |
| `SYNTHESIS.md` | `SUBTASK_synthesis` |

### Identities (the synthesis gate MUST assert these)

- [ ] `work/ferric-router-r2` branch exists on remote with exactly the 3 router commits and NO macros commits
- [ ] A PR exists from `work/ferric-router-r2` closing #131, #146, and #147
- [ ] The macros assessment covers all 12 macros commits and identifies the issues they close (#137–#142)

---

## Output Specifications

| Deliverable | Format | Location |
|-------------|--------|----------|
| Router PR confirmation | Markdown | `SUBTASK_router-branch/outputs/router-pr.md` |
| Macros scope assessment | Markdown | `SUBTASK_macros-assessment/outputs/macros-assessment.md` |
| Fold record | Markdown | `SYNTHESIS.md` |
