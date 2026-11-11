# Event Handler Security Surface — Decomposition Hub

## Project Context

**Status**: Active
**Parent task**: SUBTASK_sec_event (review-ferric-async-forms-r3 / SUBTASK_security)

### Objective

Decompose the two distinct security questions in SUBTASK_sec_event into focused atomic tasks:
1. Assess the panic-on-downcast reachability in the new `EventHandler::WithEvent` dispatch path.
2. Verify that `closure.forget()` in the WASM test (form.rs) is strictly test-scoped and does not appear in production code paths.

Synthesize the two sub-findings into the single `finding.md` required by the parent contract.

---

### Scope

**In Scope:**
- `crates/ferric/src/vdom.rs` — B2 remediation: `EventHandler::WithEvent` variant
- `crates/ferric/src/dom.rs` — B2 remediation: event dispatch, downcast, production `closure.forget()`
- `crates/ferric/src/form.rs` — B3 remediation: WASM test, test-scope `closure.forget()`
- Focused pass on the three remediation commits (9fedad9, 9557f0c, 838239e) only

**Out of Scope:**
- Other security concerns (HTML injection, secrets, unsafe code) — owned by sibling spokes
- Code quality concerns outside the two stated security questions

---

## Constraints

- Repository-relative paths only in all findings
- Severity `blocker` only for a concrete security vulnerability (panic-on-downcast is a blocker if reachable by a remotely-controlled event and causes DoS; a panic confined to test infrastructure is not)
- One `finding.md` at the SUBTASK_sec_event workspace root is the deliverable

---

## Input Specifications

| Source | Location/Command | Purpose |
|--------|-----------------|---------|
| PR diff | `gh pr diff 193 --repo Nousix-LLC/nswe-demo` | Changed lines |
| vdom.rs | `crates/ferric/src/vdom.rs` | EventHandler enum definition |
| dom.rs | `crates/ferric/src/dom.rs` | Dispatch path — downcast, production closure.forget() |
| form.rs | `crates/ferric/src/form.rs` | WASM test — test-scope closure.forget() |

---

## Subtree Methodology Posture

**Dominant task type:** Security review (Rust library)
**Primary bundles:** `security`
**Supporting bundles:** `rust`

**Cross-cutting bindings:**
- `security/Security_Secure_Coding_Methodology.md` — input validation and error handling in event paths; panic-on-invalid-input patterns
- `rust/Rust_WebAssembly_Browser_Methodology.md` — `closure.forget()` patterns, wasm-bindgen lifecycle

---

## Task Structure

```
SUBTASK_sec_event/
├── _GLOBAL.md              (this document)
├── contracts/
│   └── _MANIFEST.yaml
├── SUBTASK_sec_event_downcast/
│   └── _BRIEF.md
├── SUBTASK_sec_event_forget/
│   └── _BRIEF.md
└── SUBTASK_sec_event_synthesis/
    └── _BRIEF.md
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_sec_event_downcast` | none | Assess panic-on-downcast reachability in the EventHandler::WithEvent dispatch path | `SUBTASK_sec_event_downcast/finding_downcast.md` |
| `SUBTASK_sec_event_forget` | none | Verify closure.forget() in the WASM test is strictly test-scoped | `SUBTASK_sec_event_forget/finding_forget.md` |
| `SUBTASK_sec_event_synthesis` | `SUBTASK_sec_event_downcast`, `SUBTASK_sec_event_forget` | Compile sub-findings into the single finding.md | `finding.md` (at SUBTASK_sec_event/) |

### Dependency Graph

```
SUBTASK_sec_event_downcast ──┐
                              ├── SUBTASK_sec_event_synthesis → finding.md
SUBTASK_sec_event_forget   ──┘
```

---

## Contract

**Contract location:** `contracts/`
**Contract kind:** `yaml_schema`

See `contracts/_MANIFEST.yaml` for sub-finding structure, ownership, and identities.

### Structural Declarations

Each spoke MUST produce a sub-finding markdown file with:
- `severity`: `blocker | non-blocker | clean`
- `concern`: name of the specific sub-question
- `location`: repository-relative file:line or N/A
- `description`: what was found or verified clean

The synthesis task compiles both sub-findings into the parent-contract-required `finding.md`.

### Ownership

| Artifact | Owning subtask |
|----------|----------------|
| `SUBTASK_sec_event_downcast/finding_downcast.md` | `SUBTASK_sec_event_downcast` |
| `SUBTASK_sec_event_forget/finding_forget.md` | `SUBTASK_sec_event_forget` |
| `finding.md` (at SUBTASK_sec_event/) | `SUBTASK_sec_event_synthesis` |

### Identities

- Both sub-questions (downcast reachability AND closure.forget() scope) must be answered with evidence
- The synthesized `finding.md` must have a single `severity` verdict that reflects the combined finding
- The `finding.md` must conform to the schema in `../_GLOBAL.md` §Contract

---

## Output Specifications

| Deliverable | Format | Location | Description |
|-------------|--------|----------|-------------|
| `finding.md` | Markdown | `SUBTASK_sec_event/finding.md` | Single security finding per parent contract schema |
