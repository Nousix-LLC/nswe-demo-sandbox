# SUBTASK_hydrate-wasm-quality — Subtree Hub

**Status**: Active — decomposed into dimension spokes + synthesis

## Project Context

### Objective

Review `hydrate_wasm.rs` (197-line wasm-bindgen-test file added in commits `7fb90c7` /
`e625c3f` / `75c1eef`) across five quality dimensions, then combine the findings into
`hydrate-wasm-notes.md` following the format required by the parent contract
(`../contracts/_MANIFEST.yaml`).

### Scope

**In Scope:**
- Five quality dimensions: test structure/naming, setup/teardown/DOM cleanup,
  hardcoded strings vs. imported constants, duplication, assertion quality
- Fresh non-blocking issues found in `hydrate_wasm.rs`

**Out of Scope:**
- Security concerns (HTML injection, escaping) — SUBTASK_security
- Previously filed issues #229–#242
- `app.rs` review — SUBTASK_app-rs-quality (sibling)

### Success Criteria

- [ ] All five quality dimensions assessed with Blocker / Warning / Pass severity and evidence
- [ ] `hydrate-wasm-notes.md` written at this workspace root following the parent contract format
- [ ] Fresh non-blockers noted or "None found" stated

---

## Inputs

| Source | Location | Purpose |
|---|---|---|
| Parent contract | `../contracts/_MANIFEST.yaml` | Finding-note format identity |
| `hydrate_wasm.rs` | commit `75c1eef`, path `crates/ferric/tests/hydrate_wasm.rs` | Primary file for all dimension spokes |
| `ssr.rs` | commit `75c1eef`, path `crates/ferric/src/ssr.rs` | Reference for SSR marker constants (dimension 3) |

**Reading files:**
```bash
gh api "repos/Nousix-LLC/nswe-demo/contents/crates/ferric/tests/hydrate_wasm.rs?ref=75c1eef776953993ddd62dba1436845a0d53a281" --jq '.content' | base64 -d
gh api "repos/Nousix-LLC/nswe-demo/contents/crates/ferric/src/ssr.rs?ref=75c1eef776953993ddd62dba1436845a0d53a281" --jq '.content' | base64 -d
```

---

## Task Structure

```
_GLOBAL.md (this file)
├── contracts/
│   └── _MANIFEST.yaml                  — sub-contract: dimension finding format
├── SUBTASK_dim-naming/
│   └── _BRIEF.md                       — assess test structure & naming
├── SUBTASK_dim-cleanup/
│   └── _BRIEF.md                       — assess setup/teardown & DOM cleanup
├── SUBTASK_dim-strings/
│   └── _BRIEF.md                       — assess hardcoded strings vs. imports
├── SUBTASK_dim-duplication/
│   └── _BRIEF.md                       — assess duplication
├── SUBTASK_dim-assertions/
│   └── _BRIEF.md                       — assess assertion quality
└── SUBTASK_dim-synthesis/
    └── _BRIEF.md                       — combine findings → hydrate-wasm-notes.md
```

### Task Summary

| Task id | Depends on | Description | Output |
|---|---|---|---|
| `SUBTASK_dim-naming` | none | Assess test structure and naming in hydrate_wasm.rs | `SUBTASK_dim-naming/finding.md` |
| `SUBTASK_dim-cleanup` | none | Assess setup/teardown and DOM cleanup in hydrate_wasm.rs | `SUBTASK_dim-cleanup/finding.md` |
| `SUBTASK_dim-strings` | none | Assess hardcoded strings vs. imported constants in hydrate_wasm.rs | `SUBTASK_dim-strings/finding.md` |
| `SUBTASK_dim-duplication` | none | Assess duplication patterns in hydrate_wasm.rs | `SUBTASK_dim-duplication/finding.md` |
| `SUBTASK_dim-assertions` | none | Assess assertion quality in hydrate_wasm.rs | `SUBTASK_dim-assertions/finding.md` |
| `SUBTASK_dim-synthesis` | `SUBTASK_dim-naming`, `SUBTASK_dim-cleanup`, `SUBTASK_dim-strings`, `SUBTASK_dim-duplication`, `SUBTASK_dim-assertions` | Combine dimension findings into hydrate-wasm-notes.md | `../hydrate-wasm-notes.md` |

### Dependency Graph

```
SUBTASK_dim-naming       ──┐
SUBTASK_dim-cleanup      ──┤
SUBTASK_dim-strings      ──┼── SUBTASK_dim-synthesis
SUBTASK_dim-duplication  ──┤
SUBTASK_dim-assertions   ──┘
```

---

## Contract

**Contract location**: `contracts/`
**Contract kind**: ownership manifest + dimension finding format (`yaml_schema`)

Five independent dimension spokes each produce a small finding fragment. The synthesis
task reads all five and assembles the final `hydrate-wasm-notes.md`.

### Structural Declarations

| Artifact | Kind | Declares |
|---|---|---|
| `contracts/_MANIFEST.yaml` | ownership manifest | Per-child output paths and dimension-finding format |

### Ownership

| Artifact | Owning subtask |
|---|---|
| `SUBTASK_dim-naming/finding.md` | `SUBTASK_dim-naming` |
| `SUBTASK_dim-cleanup/finding.md` | `SUBTASK_dim-cleanup` |
| `SUBTASK_dim-strings/finding.md` | `SUBTASK_dim-strings` |
| `SUBTASK_dim-duplication/finding.md` | `SUBTASK_dim-duplication` |
| `SUBTASK_dim-assertions/finding.md` | `SUBTASK_dim-assertions` |
| `../hydrate-wasm-notes.md` | `SUBTASK_dim-synthesis` |

### Identities

- [ ] Each `finding.md` contains a severity label (Blocker / Warning / Pass)
- [ ] Each `finding.md` contains an evidence citation (hydrate_wasm.rs:line or N/A)
- [ ] Each `finding.md` covers exactly the dimension assigned to its spoke
- [ ] `../hydrate-wasm-notes.md` contains all five dimension sections in order
- [ ] `../hydrate-wasm-notes.md` follows the finding-note format from `../contracts/_MANIFEST.yaml`

### Derived Artifacts

None — spokes are read-only analyses.

---

## Subtree Methodology Posture

**Dominant task type**: Rust testing quality review (wasm-bindgen-test)

**Primary bundles**:
- `rust` — Rust test quality standards: naming, assertion quality, isolation
- `code-review` — systematic concern coverage

**Files that bind the whole subtree**:
- `rust/Rust_Testing_Methodology.md` — primary guide for all five dimensions
- `rust/Rust_WebAssembly_Browser_Methodology.md` — wasm-bindgen-test framework specifics
- `code-review/CodeReview_Process_Methodology.md` — systematic coverage discipline

**Note**: These are starting points; each child agent retains final judgment.

---

## Subtree-Wide Constraints

- **Repository**: Nousix-LLC/nswe-demo, commit `75c1eef776953993ddd62dba1436845a0d53a281`
- **PR**: #228 (branch `work/ferric-ssr-r1`, now merged)
- **Commits under inspection**: `7fb90c7`, `e625c3f`, `75c1eef`
- **Do not re-raise**: Issues #229–#242
- **Do not reference**: Overseer I267 escalation comments
- **Prose bar**: No AI-tell patterns in output text
- **Scope**: Code quality only — security (HTML injection, escaping) belongs to SUBTASK_security
