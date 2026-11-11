# Task: Test Injection Safety Analysis — hydrate_wasm.rs

## Task Specification

**Slug**: SUBTASK_test_inj
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-reviewer

### Objective

Examine `hydrate_wasm.rs` at commit `75c1eef` for test injection patterns. Determine whether any test fixture constructs HTML strings or DOM nodes from concatenation with unescaped values, whether test scaffolding inadvertently reflects injection patterns into the production code path, and whether WASM test entry points expose a surface that could allow external test input to reach the DOM unescaped. Produce `test_inj_finding.md` with the finding for the "Test Injection Safety in hydrate_wasm.rs" concern.

### Context

Spoke of the SUBTASK_sec_check decomposition. See `../_GLOBAL.md` for scope, constraints, and repo access instructions. Covers security only — code quality is a separate spoke.

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Hub document | `../_GLOBAL.md` | Scope, constraints, repo access instructions, pinned commit |
| Finding format | `../contracts/finding_format.md` | Required output structure |
| `hydrate_wasm.rs` | `gh api repos/Nousix-LLC/nswe-demo/contents/crates/ferric/tests/hydrate_wasm.rs?ref=work/ferric-ssr-r1` | File under review |

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| Filename | `test_inj_finding.md` |
| Location | `SUBTASK_test_inj/` (this workspace) |

The output file MUST conform to `../contracts/finding_format.md` with concern name `Test Injection Safety in hydrate_wasm.rs`.

---

## Success Criteria

- [ ] `hydrate_wasm.rs` read at commit `75c1eef`
- [ ] All test fixtures that build HTML or DOM content inspected: are values composed from concatenation with potentially external or test-controlled input?
- [ ] WASM test entry points examined: do they expose a surface that could reach the DOM unescaped?
- [ ] Any pattern where test scaffolding calls production code with unescaped input identified and cited by file + line
- [ ] `test_inj_finding.md` written conforming to `../contracts/finding_format.md`

---

## Suggested Methodology Files

**Task-type row matched**: "Security review" → Primary: `security`; Supporting: `code-review`  
Also applicable: "SSR / hydration in a Rust UI framework" → `framework-design`, "Rust WASM" → `rust`

Specific files to load:
- `security/Security_Secure_Coding_Methodology.md` — injection patterns, trust boundary in test code, test-controlled input as an attack surface
- `code-review/CodeReview_Process_Methodology.md` — reading for what isn't there; test assertions that check behavior vs. only that something ran
- `rust/Rust_WebAssembly_Browser_Methodology.md` — WASM test harness patterns, `wasm_bindgen_test` execution model

These are the parent's suggestions based on task type. Load fewer if inapplicable; load more if the work requires.

## Inherited Constraints

- Scope: ferric-ssr-r4 commits only (`7fb90c7`, `e625c3f`, `75c1eef`)
- Evidence must cite file + line at pinned commit `75c1eef` (not the branch head)
- Do NOT re-raise non-blockers #229–#242
- Do not reference overseer escalation comments from I267
- Code quality concerns are out of scope (separate spoke)
