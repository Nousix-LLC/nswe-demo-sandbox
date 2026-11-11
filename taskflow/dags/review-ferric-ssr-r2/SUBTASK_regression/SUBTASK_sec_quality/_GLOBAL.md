# SUBTASK_sec_quality — Security Surface and Code Quality Sub-DAG

## Project Context

**Status**: Active  
**Goal**: Decompose the security + code quality review of ferric-ssr-r4 commits into two parallel spoke analyses (security surface, code quality) and one synthesis gate that assembles them into the required `sec_quality_findings.md`.

### Objective

Produce `sec_quality_findings.md` conforming to `../contracts/findings_schema.md` covering:
- Security Findings: HTML injection in ssr.rs, DOM spoofing in app.rs, test injection safety in hydrate_wasm.rs
- Code Quality Findings: app.rs new conditional hydrate/mount dispatch, hydrate_wasm.rs test code, fresh non-blockers
- What Was Examined and Found Clean: each concern checked with no finding

### Repository

- **Repository**: Nousix-LLC/nswe-demo
- **Branch**: `work/ferric-ssr-r1`
- **Pinned commit**: `75c1eef`
- **Commits under review (ferric-ssr-r4)**: `7fb90c7`, `e625c3f`, `75c1eef`

---

## Subtree Methodology Posture

**Dominant task type**: Ferric PR review (Rust library) — security surface sub-task  
**Primary bundles**: Code Review, Security, Rust  
**Supporting bundles**: Framework Design (UI reactivity & rendering internals)  
**Cross-cutting**: All leaf tasks apply the principal-reviewer persona from the swe-reviewer system prompt. Evidence over assertion; every finding cites file and line at pinned commit `75c1eef`. Do not re-raise #229–#242; do not check regression criteria (those are SUBTASK_reg_criteria).

---

## Task Structure

```
_GLOBAL.md (this document)
├── contracts/
│   ├── _MANIFEST.yaml
│   └── spoke_output_schema.md
├── SUBTASK_sec_check/_BRIEF.md     (security surface analysis)
├── SUBTASK_quality_check/_BRIEF.md (code quality analysis)
└── SUBTASK_secq_synthesis/_BRIEF.md     (synthesis gate → sec_quality_findings.md)
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_sec_check` | none | Security-only review: HTML injection in ssr.rs, DOM spoofing in app.rs, test injection in hydrate_wasm.rs | `SUBTASK_sec_check/security_raw_findings.md` |
| `SUBTASK_quality_check` | none | Code quality review: app.rs new code, hydrate_wasm.rs test code, fresh non-blockers | `SUBTASK_quality_check/quality_raw_findings.md` |
| `SUBTASK_secq_synthesis` | `SUBTASK_sec_check`, `SUBTASK_quality_check` | Synthesis gate: combine both outputs into sec_quality_findings.md per findings schema | `sec_quality_findings.md` |

### Dependency Graph

```
SUBTASK_sec_check     ──┐
                         ├── SUBTASK_secq_synthesis
SUBTASK_quality_check ──┘
```

---

## Contract

**Contract location**: `contracts/`  
**Contract kind**: `markdown`

### Inherited Contracts

| Ancestor contract | Path | What it binds here |
|---|---|---|
| Findings schema | `../contracts/findings_schema.md` | The final `sec_quality_findings.md` MUST follow this schema; synthesis assembles the two spoke outputs into it |

### Structural Declarations

| Artifact | Kind | Declares |
|---|---|---|
| `contracts/spoke_output_schema.md` | Markdown template | Sections each spoke output file must carry so synthesis can assemble them mechanically |

### Ownership

| Artifact | Owning subtask |
|---|---|
| `SUBTASK_sec_check/security_raw_findings.md` | `SUBTASK_sec_check` |
| `SUBTASK_quality_check/quality_raw_findings.md` | `SUBTASK_quality_check` |
| `sec_quality_findings.md` | `SUBTASK_synthesis` |

### Identities

- [ ] `security_raw_findings.md` carries a `## Security Findings` section with one entry per concern (HTML injection, DOM spoofing, test injection) in the findings schema format
- [ ] `quality_raw_findings.md` carries a `## Code Quality Findings` section and a `## What Was Examined and Found Clean` section
- [ ] `sec_quality_findings.md` assembles both spoke outputs into the full findings schema structure

---

## Subtree-Wide Constraints

- Scope is ferric-ssr-r4 commits only: `7fb90c7`, `e625c3f`, `75c1eef`
- Do NOT re-raise non-blockers #229–#242
- Evidence must cite file + line at pinned commit `75c1eef`
- Security surface bounded to HTML injection in SSR path and DOM spoofing in hydrate dispatch
- Do not reference overseer escalation comments from I267
- Do not check regression criteria (those are SUBTASK_reg_criteria's concern)

---

## Output Specification

| Deliverable | Location | Description |
|-------------|----------|-------------|
| `sec_quality_findings.md` | `SUBTASK_sec_quality/` | Security + quality findings following findings_schema.md |
