# PR #193 Ferric Async — Concerns 2, 3, 6, 7 Subtree

## Project Context

**Status**: Active

### Objective

Decompose the review of PR #193 (`work/ferric-async-forms-r2`, head `838239e`) across four distinct analytical concerns — code quality/design (Concern 2), test coverage/depth (Concern 3), Rust language idiom (Concern 6), and API/contract stability (Concern 7) — and synthesize them into a single `findings.md` at this workspace root.

### Scope

**In Scope:**
- Four concern spoke reviews, each applying a distinct analytical lens to the same set of changed files
- One synthesis task that aggregates spoke findings into the final unified `findings.md`

**Out of Scope:**
- Concerns 1 (async/reactive correctness), 4 (security), 5 (documentation) — covered by sibling tasks in the parent DAG
- Re-raising issues #196–#201 (non-blockers already filed in a prior round)
- Files not listed in the shared inputs table

### Success Criteria

- [ ] Concern 2 spoke: coupling, `EventHandler` abstraction boundary, generation counter clarity reviewed and evidenced
- [ ] Concern 3 spoke: each acceptance-criteria test evaluated for behavioral depth; unexercised scenarios identified
- [ ] Concern 6 spoke: `closure.forget()`, private field access, unsafe patterns, and anti-patterns reviewed and evidenced
- [ ] Concern 7 spoke: `EventHandler` backward compat verified; `on_input_event_handler()` and `create_resource` API assessed against naming and documentation conventions
- [ ] Synthesis task: `findings.md` produced with every concern addressed and severity assigned

---

## Shared Inputs

Each spoke reads the following inputs independently.

| Input | Source | Purpose |
|-------|--------|---------|
| PR #193 diff | `gh pr diff 193 --repo Nousix-LLC/nswe-demo` | Actual changed lines for context |
| async_resource.rs | `crates/ferric/src/async_resource.rs` | B1 implementation and new tests |
| vdom.rs | `crates/ferric/src/vdom.rs` | B2 EventHandler enum |
| dom.rs | `crates/ferric/src/dom.rs` | B2 dispatch + WASM test |
| form.rs | `crates/ferric/src/form.rs` | B3 on_input_event_handler + WASM test |

---

## Inherited Constraints

- Repository-relative paths only in all findings (e.g. `crates/ferric/src/async_resource.rs:42`)
- Issues #196–#201 MUST NOT be re-raised
- Severity calibration: `blocker` only if a requirement is unmet or an existing API contract is broken for callers; style and preference observations are at most `non-blocker`
- Concerns 1, 4, 5 are out of scope for this subtree

---

## Task Structure

### Overview

```
_GLOBAL.md (this document)
├── contracts/
│   ├── _MANIFEST.yaml
│   └── findings_format.md
├── SUBTASK_concern2_code_quality/
│   └── _BRIEF.md
├── SUBTASK_concern3_tests/
│   └── _BRIEF.md
├── SUBTASK_concern6_idiom/
│   └── _BRIEF.md
├── SUBTASK_concern7_api_stability/
│   └── _BRIEF.md
└── SUBTASK_findings_synthesis/
    └── _BRIEF.md
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_concern2_code_quality` | none | Concern 2: code quality and design review | `partial_findings.md` |
| `SUBTASK_concern3_tests` | none | Concern 3: test coverage and depth review | `partial_findings.md` |
| `SUBTASK_concern6_idiom` | none | Concern 6: Rust language idiom review | `partial_findings.md` |
| `SUBTASK_concern7_api_stability` | none | Concern 7: API and contract stability review | `partial_findings.md` |
| `SUBTASK_qti_synthesis` | `SUBTASK_concern2_code_quality`, `SUBTASK_concern3_tests`, `SUBTASK_concern6_idiom`, `SUBTASK_concern7_api_stability` | Synthesis: aggregate spoke findings into findings.md | `../findings.md`, `../SYNTHESIS.md` |

### Dependency Graph

```
SUBTASK_concern2_code_quality  ──┐
                                 │
SUBTASK_concern3_tests          ──┼── SUBTASK_findings_synthesis
                                 │
SUBTASK_concern6_idiom          ──┤
                                 │
SUBTASK_concern7_api_stability  ──┘
```

(Synthesis task ID: `SUBTASK_qti_synthesis`)

---

## Contract

**Contract location**: `contracts/`
**Contract kind**: `yaml_schema`

### Structural Declarations

Each concern spoke MUST produce a `partial_findings.md` conforming to the format declared in `contracts/findings_format.md`. The synthesis task reads all four partial findings files and produces `findings.md` and `SYNTHESIS.md` at the parent workspace root.

| Artifact | Kind | Declares |
|---|---|---|
| `contracts/findings_format.md` | format-spec | Schema every spoke's `partial_findings.md` MUST follow |
| `contracts/_MANIFEST.yaml` | manifest | Ownership: which task writes which artifact |

### Ownership

| Artifact | Owning subtask |
|---|---|
| `SUBTASK_concern2_code_quality/partial_findings.md` | `SUBTASK_concern2_code_quality` |
| `SUBTASK_concern3_tests/partial_findings.md` | `SUBTASK_concern3_tests` |
| `SUBTASK_concern6_idiom/partial_findings.md` | `SUBTASK_concern6_idiom` |
| `SUBTASK_concern7_api_stability/partial_findings.md` | `SUBTASK_concern7_api_stability` |
| `../findings.md` | `SUBTASK_qti_synthesis` |
| `../SYNTHESIS.md` | `SUBTASK_qti_synthesis` |

### Identities

- [ ] Every `partial_findings.md` conforms to `contracts/findings_format.md` (required sections present, severity values from the allowed set, paths repository-relative)
- [ ] Every sub-question in the parent brief's four concern sections has at least one entry (blocker, non-blocker, or clean) in the combined output
- [ ] No finding duplicates an issue from #196–#201
- [ ] No finding appears in more than one spoke output (concerns are non-overlapping by assignment)

---

## Subtree Methodology Posture

**Dominant task type:** Ferric PR review (Rust library) — `code-review` primary, `rust` + `framework-design` supporting

**Primary bundles all spokes draw on:** `code-review` (checklist, feedback guidelines), `rust` (testing, library API stability)

**Cross-cutting bindings that apply to multiple spokes:**
- `code-review/CodeReview_Checklist_Methodology.md` — review-process discipline for every spoke
- `rust/Rust_Testing_Methodology.md` — test adequacy criteria for Concern 3 and idiom patterns in Concern 6
- `rust/Rust_Library_API_And_Stability_Methodology.md` — API surface and semver for Concern 7
- `framework-design/FrameworkDesign_Library_API_Design_Methodology.md` — abstraction boundary assessment for Concerns 2 and 7

Dispatched agents are the final judges of what they actually need; these are starting-point suggestions.
