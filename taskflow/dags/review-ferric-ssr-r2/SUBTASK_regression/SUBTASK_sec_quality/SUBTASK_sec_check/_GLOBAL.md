# SUBTASK_sec_check — Security Surface Analysis Sub-DAG

## Project Context

**Status**: Active  
**Parent task ID**: `proc-329f53fb-256d-41c0-8873-0894bcf81914`  
**Parent workspace**: this directory (`SUBTASK_sec_check/`)

### Objective

Produce `security_raw_findings.md` per `../contracts/spoke_output_schema.md` §SUBTASK_sec_check by decomposing the three security concerns into three parallel spoke analyses (one per concern / file) and one synthesis gate that assembles them.

### Repository

- **Repo**: `Nousix-LLC/nswe-demo`
- **Branch**: `work/ferric-ssr-r1`
- **Pinned commit**: `75c1eef`
- **Commits under review (ferric-ssr-r4)**: `7fb90c7`, `e625c3f`, `75c1eef`

**Retrieve file content via:**
```bash
gh api repos/Nousix-LLC/nswe-demo/contents/<path>?ref=work/ferric-ssr-r1 \
  | python3 -c "import sys,json,base64; print(base64.b64decode(json.load(sys.stdin)['content']).decode())"
```

---

## Subtree Methodology Posture

**Dominant task type**: Security review (Rust/WASM library)  
**Primary bundles**: `security`, `code-review`  
**Supporting bundles**: `rust` (Rust_WebAssembly_Browser_Methodology.md), `framework-design` (FrameworkDesign_UI_Reactivity_And_Rendering_Internals_Methodology.md)

**Cross-cutting constraints** (bind every leaf):
- Principal-reviewer persona: evidence over assertion; every finding cites file + line at commit `75c1eef`
- Do NOT re-raise non-blockers #229–#242
- Do not reference overseer escalation comments from I267

---

## Task Structure

```
_GLOBAL.md (this document)
├── contracts/
│   ├── _MANIFEST.yaml
│   └── finding_format.md          ← per-spoke output contract
├── SUBTASK_html_inj/_BRIEF.md     ← HTML injection in ssr.rs
├── SUBTASK_dom_spoof/_BRIEF.md    ← DOM spoofing in app.rs
├── SUBTASK_test_inj/_BRIEF.md     ← Test injection in hydrate_wasm.rs
└── SUBTASK_synthesis/_BRIEF.md   ← synthesis gate → security_raw_findings.md
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_html_inj` | none | HTML injection analysis in ssr.rs | `SUBTASK_html_inj/html_inj_finding.md` |
| `SUBTASK_dom_spoof` | none | DOM spoofing analysis in app.rs | `SUBTASK_dom_spoof/dom_spoof_finding.md` |
| `SUBTASK_test_inj` | none | Test injection analysis in hydrate_wasm.rs | `SUBTASK_test_inj/test_inj_finding.md` |
| `SUBTASK_seccheck_synth` | `SUBTASK_html_inj`, `SUBTASK_dom_spoof`, `SUBTASK_test_inj` | Synthesis gate: assemble security_raw_findings.md, fold parent | `security_raw_findings.md` (at this workspace root), `SYNTHESIS.md` (at this workspace root) |

### Dependency Graph

```
SUBTASK_html_inj   ──┐
                      ├── SUBTASK_seccheck_synth
SUBTASK_dom_spoof  ──┤
                      │
SUBTASK_test_inj   ──┘
```

---

## Contract

**Contract location**: `contracts/`  
**Contract kind**: `markdown`

### Inherited Contracts

| Ancestor contract | Path | What it binds here |
|---|---|---|
| Spoke output schema | `../contracts/spoke_output_schema.md` | `security_raw_findings.md` MUST follow §SUBTASK_sec_check of that schema |

### Structural Declarations

| Artifact | Kind | Declares |
|---|---|---|
| `contracts/finding_format.md` | Markdown template | Per-concern finding format all spokes must produce |

### Ownership

| Artifact | Owning subtask |
|---|---|
| `SUBTASK_html_inj/html_inj_finding.md` | `SUBTASK_html_inj` |
| `SUBTASK_dom_spoof/dom_spoof_finding.md` | `SUBTASK_dom_spoof` |
| `SUBTASK_test_inj/test_inj_finding.md` | `SUBTASK_test_inj` |
| `security_raw_findings.md` (at this workspace root) | `SUBTASK_seccheck_synth` |
| `SYNTHESIS.md` (at this workspace root — fold record) | `SUBTASK_seccheck_synth` |

### Identities

- [ ] `security_raw_findings.md` has `## Security Findings` with exactly 3 subsections: "HTML Injection in ssr.rs", "DOM Spoofing in app.rs", "Test Injection Safety in hydrate_wasm.rs"
- [ ] Each subsection carries **Result** (Clean or Finding) and **Evidence** (file:line at `75c1eef`)
- [ ] **Finding** field present if and only if Result is Finding
- [ ] `security_raw_findings.md` has `## What Was Examined and Found Clean` section listing concerns whose Result is Clean

---

## Subtree-Wide Constraints

- Scope: ferric-ssr-r4 commits only: `7fb90c7`, `e625c3f`, `75c1eef`
- Do NOT re-raise non-blockers #229–#242
- Evidence must cite file + line at pinned commit `75c1eef`
- Security surface bounded to: HTML injection in SSR path, DOM spoofing in hydrate dispatch, test injection patterns
- Do not reference overseer escalation comments from I267

---

## Synthesis Fold Information

The SUBTASK_synthesis child folds this SUSPENDED parent back to COMPLETED:

- **Parent task ID** (use as `target_task_id` in `engine_resume_suspended`): `proc-329f53fb-256d-41c0-8873-0894bcf81914`
- **Fold location**: This workspace root (parent workspace)
- **SYNTHESIS.md absolute path**: `/home/user/nousix-runtime/nswe-demo/taskflow/dags/review-ferric-ssr-r2/SUBTASK_regression/SUBTASK_sec_quality/SUBTASK_sec_check/SYNTHESIS.md`
- **security_raw_findings.md absolute path**: `/home/user/nousix-runtime/nswe-demo/taskflow/dags/review-ferric-ssr-r2/SUBTASK_regression/SUBTASK_sec_quality/SUBTASK_sec_check/security_raw_findings.md`

---

## Output Specification

| Deliverable | Location | Description |
|-------------|----------|-------------|
| `security_raw_findings.md` | This workspace root | Security findings per `../contracts/spoke_output_schema.md` §SUBTASK_sec_check |
| `SYNTHESIS.md` | This workspace root | Fold record authored by SUBTASK_synthesis |
