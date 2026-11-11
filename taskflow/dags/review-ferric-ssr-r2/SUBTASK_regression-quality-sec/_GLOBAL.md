# Subtree Hub: SUBTASK_regression-quality-sec

**Status**: Active — decomposed into spoke tasks

## Project Context

### Objective

Verify that the 9 previously-clean acceptance criteria remain satisfied after the
ferric-ssr-r4 commits (PR #228), review the code quality of all new/changed code
in those commits, check for security issues (HTML injection, escaping gaps), and
identify any fresh non-blocking issues.

This is the SUBTASK_regression-quality-sec spoke of the review-ferric-ssr-r2 DAG.
Its parent context is in `../../_GLOBAL.md`.

### Scope

**In Scope:**
- Regression check: 9 previously-clean criteria (REQ-SSR-001/002/003/004/005,
  REQ-HYD-001/002/004, REQ-MIS-001/002) verified against ferric-ssr-r4 commits
- Code quality: cfg-gate pattern in `app.rs`; test file structure in `hydrate_wasm.rs`
- Security: HTML injection paths, escaping gaps introduced by new commits
- Fresh non-blocking issues found in new code (not to be re-raised #229–#242)

**Out of Scope:**
- B1 (REQ-HYD-003) and B2 (REQ-SSR-006) — handled by sibling spokes
- Previously filed non-blocking issues #229–#242
- Overseer I267 escalation comments

### Success Criteria

- [ ] Verdict file `verdict-regression-quality-sec.md` written to this workspace
- [ ] Regression check: all 9 criteria assessed (PASS/FAIL/UNCHANGED each)
- [ ] Code quality: cfg-gate pattern and test file reviewed
- [ ] Security: HTML injection and escaping gaps checked
- [ ] Fresh non-blockers listed (or "none found")
- [ ] Overall PASS or FAIL verdict stated

---

## Inputs

| Source | Location | Purpose |
|---|---|---|
| PR #228 diff | `gh pr diff 228 --repo Nousix-LLC/nswe-demo` | Full diff of ferric-ssr-r4 commits |
| `app.rs` | `crates/chirp-frontend/src/app.rs` on branch | cfg-gate quality review |
| `hydrate_wasm.rs` | `crates/ferric/tests/hydrate_wasm.rs` on branch | Test quality review |
| `ssr.rs` | `crates/ferric/src/ssr.rs` on branch | REQ-SSR-004 marker source |
| `hydrate.rs` | `crates/ferric/src/hydrate.rs` on branch | REQ-HYD-001/002, REQ-MIS-002 |
| `lib.rs` (ferric) | `crates/ferric/src/lib.rs` on branch | REQ-SSR-005 export |
| Issues #223, #224, #226 | GitHub | Requirement texts |

---

## Task Structure

```
_GLOBAL.md (this file)
├── contracts/_MANIFEST.yaml          — ownership manifest (thin seam)
├── SUBTASK_regression-check/
│   └── _BRIEF.md                     — verify 9 previously-clean criteria
├── SUBTASK_code-quality/
│   └── _BRIEF.md                     — code quality review of new code
├── SUBTASK_security/
│   └── _BRIEF.md                     — security review of new code
└── SUBTASK_synthesis/
    └── _BRIEF.md                     — synthesis: combine → verdict + SYNTHESIS.md fold
```

### Task Summary

| Task id | Depends on | Description | Output |
|---|---|---|---|
| `SUBTASK_regression-check` | none | Verify 9 previously-clean acceptance criteria | `regression-check.md` |
| `SUBTASK_code-quality` | none | Code quality review of app.rs and hydrate_wasm.rs | `code-quality.md` |
| `SUBTASK_security` | none | Security review — injection paths, escaping gaps | `security.md` |
| `SUBTASK_synthesis` | `SUBTASK_regression-check`, `SUBTASK_code-quality`, `SUBTASK_security` | Combine verdicts → verdict-regression-quality-sec.md + SYNTHESIS.md | `../verdict-regression-quality-sec.md`, `../SYNTHESIS.md` |

### Dependency Graph

```
SUBTASK_regression-check ───┐
                            ├── SUBTASK_synthesis
SUBTASK_code-quality ───────┤
                            │
SUBTASK_security ───────────┘
```

---

## Contract

**Contract location**: `contracts/`
**Contract kind**: ownership manifest (thin seam — spokes are independent reads, shared only by synthesis)

Each spoke reads the same source files independently and writes one verdict markdown file.
The synthesis task reads all three verdict files and produces the combined output.

### Structural Declarations

| Artifact | Kind | Declares |
|---|---|---|
| `contracts/_MANIFEST.yaml` | ownership manifest | Per-child output ownership and cross-task identities |

### Ownership

| Artifact | Owning subtask |
|---|---|
| `SUBTASK_regression-check/regression-check.md` | `SUBTASK_regression-check` |
| `SUBTASK_code-quality/code-quality.md` | `SUBTASK_code-quality` |
| `SUBTASK_security/security.md` | `SUBTASK_security` |
| `../verdict-regression-quality-sec.md` | `SUBTASK_synthesis` |
| `../SYNTHESIS.md` | `SUBTASK_synthesis` |

### Identities

- [ ] Every acceptance criterion listed in the brief (all 9) appears in `regression-check.md`
- [ ] `verdict-regression-quality-sec.md` addresses all three spoke areas (regression, quality, security)
- [ ] Overall PASS/FAIL verdict in `verdict-regression-quality-sec.md` is consistent with spoke findings

---

## Subtree Methodology Posture

**Dominant task type**: Code review (Rust library, verification-focused)

**Primary bundles across the subtree**: `code-review`, `rust`, `security`

**Files that bind the whole subtree**:
- `code-review/CodeReview_Process_Methodology.md` — systematic concern coverage
- `code-review/CodeReview_Checklist_Methodology.md` — regression and quality checklist
- `rust/Rust_Testing_Methodology.md` — Rust test quality standards (for SUBTASK_code-quality)
- `rust/Rust_WebAssembly_Browser_Methodology.md` — WASM/wasm-bindgen discipline
- `security/Security_Secure_Coding_Methodology.md` — HTML injection, escaping, XSS vectors (for SUBTASK_security)
- `framework-design/FrameworkDesign_UI_Reactivity_And_Rendering_Internals_Methodology.md` — SSR/hydration correctness

**Note**: These are starting points. Each child agent retains final judgment.

## Subtree-Wide Constraints

- **Repository**: Nousix-LLC/nswe-demo, branch `work/ferric-ssr-r1`, PR #228
- **Commits under inspection**: `7fb90c7`, `e625c3f`, `75c1eef`
- **Do not re-raise**: Issues #229–#242
- **Do not reference**: Overseer I267 escalation comments
- **Non-blockers**: List in verdict only; synthesis task decides whether to file GitHub issues
- **Prose bar**: Output must be free of AI-tell patterns (moral adjectives on metrics, narrated
  candor, slot-fill templates, padding filler)
- **Previously-clean criteria**: REQ-SSR-001/002/003/004/005, REQ-HYD-001/002/004, REQ-MIS-001/002
  — 9 criteria found clean in review-ferric-ssr-r1; verify they remain clean
