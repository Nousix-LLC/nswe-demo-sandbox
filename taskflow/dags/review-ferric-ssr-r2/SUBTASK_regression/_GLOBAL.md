# SUBTASK_regression — Regression / Security / Code Quality Sub-DAG

## Project Context

**Status**: Active  
**Goal**: Decompose the SUBTASK_regression scope into three atomic units: (1) check the 9 previously-clean criteria against the ferric-ssr-r4 commits; (2) check the security surface and code quality of new/changed code; (3) synthesize both into the required `regression_verdict.md`.

### Objective

Produce `regression_verdict.md` conforming to `../contracts/verdict_schema.md` with:
- PASS or FAIL verdict for each of REQ-SSR-001..003, REQ-SSR-005, REQ-HYD-001, REQ-HYD-002, REQ-HYD-004, REQ-MIS-001, REQ-MIS-002
- Security findings (HTML injection, DOM spoofing)
- Code quality findings for new code in `app.rs` and `hydrate_wasm.rs`
- Fresh non-blockers if any

### Repository

- **Repository**: Nousix-LLC/nswe-demo
- **Branch**: `work/ferric-ssr-r1`
- **Pinned commit**: `75c1eef`
- **Commits under review (ferric-ssr-r4)**: `7fb90c7`, `e625c3f`, `75c1eef`

---

## Subtree Methodology Posture

**Dominant task type**: Ferric PR review (Rust library)  
**Primary bundles**: Code Review, Rust  
**Supporting bundles**: Security, Framework Design (UI reactivity & rendering internals)  
**Cross-cutting**: All leaf tasks apply the principal-reviewer persona from the swe-reviewer system prompt. Evidence over assertion; every finding cites file and line at pinned commit `75c1eef`. Do not re-raise #229–#242; do not check B1/B2.

---

## Task Structure

```
_GLOBAL.md (this document)
├── SUBTASK_reg_criteria/_BRIEF.md    (9 previously-clean criteria regression check)
├── SUBTASK_sec_quality/_BRIEF.md     (security surface + code quality)
└── SUBTASK_verdict_synthesis/_BRIEF.md  (synthesize into regression_verdict.md)
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_reg_criteria` | none | Check 9 previously-clean criteria against ferric-ssr-r4 commits | `SUBTASK_reg_criteria/criteria_findings.md` |
| `SUBTASK_sec_quality` | none | Security surface + code quality of new/changed code | `SUBTASK_sec_quality/sec_quality_findings.md` |
| `SUBTASK_verdict_synthesis` | `SUBTASK_reg_criteria`, `SUBTASK_sec_quality` | Synthesize into regression_verdict.md following verdict_schema | `regression_verdict.md` |

### Dependency Graph

```
SUBTASK_reg_criteria   ──┐
                          ├── SUBTASK_verdict_synthesis
SUBTASK_sec_quality    ──┘
```

---

## Contract

**Contract location**: `contracts/`  
**Contract kind**: `yaml_schema`

### Inherited Contracts

| Ancestor contract | Path | What it binds here |
|---|---|---|
| Verdict schema | `../contracts/verdict_schema.md` | The final `regression_verdict.md` MUST follow this schema |

### Structural Declarations

| Artifact | Kind | Declares |
|---|---|---|
| `contracts/findings_schema.md` | Markdown template | Sections each findings file must carry (criteria results, security findings, quality findings, examined-and-clean list) |

### Ownership

| Artifact | Owning subtask |
|---|---|
| `SUBTASK_reg_criteria/criteria_findings.md` | `SUBTASK_reg_criteria` |
| `SUBTASK_sec_quality/sec_quality_findings.md` | `SUBTASK_sec_quality` |
| `regression_verdict.md` | `SUBTASK_verdict_synthesis` |

### Identities

- [ ] Every requirement in {REQ-SSR-001..003, REQ-SSR-005, REQ-HYD-001, REQ-HYD-002, REQ-HYD-004, REQ-MIS-001, REQ-MIS-002} appears with a verdict in `criteria_findings.md`
- [ ] `regression_verdict.md` consolidates all findings and states an overall PASS or FAIL verdict

---

## Subtree-Wide Constraints

- Scope is ferric-ssr-r4 commits only: `7fb90c7`, `e625c3f`, `75c1eef`
- Do NOT check B1 (REQ-HYD-003) or B2 (REQ-SSR-006) — those are SUBTASK_b1_verify and SUBTASK_b2_verify
- Do NOT re-raise non-blockers #229–#242
- Evidence must cite file + line at pinned commit `75c1eef`
- Security surface bounded to HTML injection in SSR path and DOM spoofing in hydrate dispatch
- Do not reference overseer escalation comments from I267

---

## Output Specification

| Deliverable | Location | Description |
|-------------|----------|-------------|
| `regression_verdict.md` | `taskflow/dags/review-ferric-ssr-r2/SUBTASK_regression/` | Final verdict following verdict_schema.md |
