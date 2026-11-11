# review-ferric-http-r2

## Project Context

**Status**: Active

### Objective

Re-review PR #210 (`work/ferric-http-r1` → `main`) after the ferric-http-r2 remediation commit (`0436218`) to verify that all 2 original blockers (B1, B2) and 3 should-fix items (SF3–SF5) from review-ferric-http-r1 are resolved, and produce a final verdict (APPROVE or REQUEST-CHANGES).

**PR**: #210 on `Nousix-LLC/nswe-demo`  
**Head commit under review**: `0436218` — `fix(ferric-http): correct API signatures in CHANGELOG.md (review-ferric-http-r1 blockers)`  
**Issues**: #132 (frozen API surface), #148 (HTTP client documentation)

### Scope

**In Scope:**
- Correctness: every documented signature in CHANGELOG.md matches the compiled crate source (ground truth: source files)
- Code quality: CHANGELOG.md structure coherence, correct placement, no duplication
- Security: no absolute host paths, private/internal network addresses, host runtime or taskflow directory references in committed content
- Final verdict: APPROVE or REQUEST-CHANGES posted as a review comment on PR #210
- SYNTHESIS.md at this workspace root with per-item resolution status

**Out of Scope:**
- Re-opening original blockers without evidence of persistent failure
- Reviewing CHANGELOG.md sections not touched by this PR

### Success Criteria

- [ ] B1 (query() signature) and B2 (Response::text() signature) resolution verified with source-code evidence
- [ ] SF3, SF4, SF5 resolution verified with source-code evidence
- [ ] Code quality concern checked and found sound or flagged
- [ ] Security concern checked and found sound or flagged
- [ ] Verdict (APPROVE or REQUEST-CHANGES) posted on PR #210
- [ ] SYNTHESIS.md authored with per-item resolution status and concern-by-concern account

---

## Original Blockers (must resolve)

- **B1**: `query()` signature — was `(self, key: &str, value: &str) -> Self`, must be `(self, params: &[(&str, &str)]) -> Self` matching `crates/ferric-http/src/request.rs`
- **B2**: `Response::text()` signature — was `(&self) -> &str`, must be `(self) -> String` matching `crates/ferric-http/src/response.rs`

## Should-fix Items (must verify)

- **SF3** (issue #211): `header()` / `default_header()` declared with correct `&str` (not `impl Into<String>`)
- **SF4** (issue #212): Missing public API members added — `Error::is_network/is_status/status`, `Method::as_str/Display`, `RequestBuilder::body_string`, `Response::status_text/headers/body`
- **SF5** (issue #213): `Method` `#[non_exhaustive]` deferred note added referencing #149

---

## Input Specifications

| Input | Location | Description |
|-------|----------|-------------|
| PR #210 | `gh pr view 210 --repo Nousix-LLC/nswe-demo` | PR description, commits, existing comments |
| Source files | `crates/ferric-http/src/{request,response,client,error,lib}.rs` | Ground truth for public API signatures |
| CHANGELOG.md | repo root | Documented API surface added/corrected by this PR |
| Remediation commit | `0436218` | The specific fix commit |
| Issues #132, #148 | `gh issue view 132/148 --repo Nousix-LLC/nswe-demo` | Acceptance criteria |

---

## Task Structure

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_correctness` | none | Verify B1, B2, SF3, SF4, SF5 by comparing CHANGELOG signatures to source code | `SUBTASK_correctness/correctness_findings.md` |
| `SUBTASK_code_quality` | none | Check CHANGELOG.md structure, placement, no duplication | `SUBTASK_code_quality/code_quality_findings.md` |
| `SUBTASK_security` | none | Check committed content for path/network leaks | `SUBTASK_security/security_findings.md` |
| `SUBTASK_verdict` | `SUBTASK_correctness`, `SUBTASK_code_quality`, `SUBTASK_security` | Integrate findings, post PR comment, write SYNTHESIS.md, file new issues | `SYNTHESIS.md` |

### Dependency Graph

```
SUBTASK_correctness  ──┐
                        │
SUBTASK_code_quality ──├── SUBTASK_verdict
                        │
SUBTASK_security     ──┘
```

---

## Contract

**Contract location**: `contracts/`  
**Contract kind**: `yaml_schema`

### Structural Declarations

Each spoke task (correctness, code_quality, security) produces a findings file. The verdict task reads all three. The findings files must follow a common structure so the verdict can process them.

| Artifact | Kind | Declares |
|---|---|---|
| `contracts/findings_schema.yaml` | yaml_schema | Required sections and severity classifications for each findings file |

### Ownership

| Artifact | Owning subtask |
|---|---|
| `SUBTASK_correctness/correctness_findings.md` | `SUBTASK_correctness` |
| `SUBTASK_code_quality/code_quality_findings.md` | `SUBTASK_code_quality` |
| `SUBTASK_security/security_findings.md` | `SUBTASK_security` |
| `SYNTHESIS.md` | `SUBTASK_verdict` |

### Identities

- [ ] Every verified item (B1, B2, SF3, SF4, SF5) has an explicit status (RESOLVED / UNRESOLVED / PARTIAL) in correctness_findings.md
- [ ] Every review concern area (Correctness, Code Quality, Security) has an account in SYNTHESIS.md
- [ ] The verdict in SYNTHESIS.md matches the verdict posted on PR #210
- [ ] Any new blocker discovered has a corresponding GitHub issue reference

---

## Subtree Methodology Posture

**Dominant task type:** Ferric PR review (Rust library) — Code Review, Rust, Framework Design
**Primary bundles per child:**
- SUBTASK_correctness: Code Review, Rust (signature reading, library API)
- SUBTASK_code_quality: Code Review, Framework Design (documentation as contract)
- SUBTASK_security: Security (secure coding, configuration management)
- SUBTASK_verdict: Synthesis, Code Review

**Cross-cutting bindings:**
- Code Review methodology binds every node — it sets the standard for what a review examines and how findings are classified
- avoid-ai-writing skill (P0/P1 patterns in `references/patterns.md`) binds every node — all review output prose must be free of machine-writing tells

## Subtree-Wide Constraints

- Head commit: `0436218` on branch `work/ferric-http-r1` — this is the reference point; ground truth is the source, not prior review notes
- Verdict must be binary: APPROVE or REQUEST-CHANGES — no ambiguous "mostly OK" outcomes
- If the platform will not accept a formal approval (same account as PR author), post as a review comment carrying the verdict
- SYNTHESIS.md at the workspace root (`taskflow/dags/review-ferric-http-r2/SYNTHESIS.md`) is the authoritative verdict record
- Do not expose server addresses, SSH key paths, user names, or internal host paths in any committed artifact or review comment
