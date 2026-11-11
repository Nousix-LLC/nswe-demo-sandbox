# Security Review Subtree: PR #193 Ferric Async Remediation

## Project Context

**Status**: Active

### Objective

Conduct a focused security review of PR #193 (`work/ferric-async-forms-r2`, head `838239e`) across four distinct concern areas — HTML injection/escaping, secrets and infrastructure data, unsafe code, and event-handler security surface — producing `findings.md` at the SUBTASK_security workspace root.

### Scope

**In Scope:**
- HTML injection / escaping gap in the new event-handling and form-binding code paths
- Secrets and infrastructure data committed in the diff (IPs, creds, tokens, SSH keys, real server addresses)
- New unsafe code blocks introduced by the remediation commits and their stated invariants
- Event handler security surface (panic-on-downcast exposure) and `closure.forget()` scope

**Out of Scope:**
- Comprehensive library-wide security audit (this is a focused pass on the three remediation commits)
- Non-security code quality concerns
- Files not changed by the three remediation commits (9fedad9, 9557f0c, 838239e)

### Success Criteria
- [ ] All four concern areas answered with evidence from the diff and source files
- [ ] `findings.md` produced at `SUBTASK_security/findings.md`
- [ ] No unexamined security concern within scope
- [ ] Severity assigned: `blocker` only for concrete security vulnerability introduced by this PR

---

## Constraints

- Repository-relative paths only in all findings (no internal hosts, SSH keys, or infra addresses)
- Focused pass on the three remediation commits only
- A finding is a blocker only if it represents a concrete security vulnerability introduced by this PR

---

## Input Specifications

| Source | Location/Command | Purpose |
|--------|-----------------|---------|
| PR diff | `gh pr diff 193 --repo Nousix-LLC/nswe-demo` | Changed lines |
| async_resource.rs | `crates/ferric/src/async_resource.rs` | B1 source |
| vdom.rs | `crates/ferric/src/vdom.rs` | B2 source |
| dom.rs | `crates/ferric/src/dom.rs` | B2 source |
| form.rs | `crates/ferric/src/form.rs` | B3 source |

---

## Subtree Methodology Posture

**Dominant task type:** Security review (Rust library)
**Primary bundles:** `security`
**Supporting bundles:** `code-review`, `rust`

**Cross-cutting methodology bindings across all spokes:**
- `security/Security_Secure_Coding_Methodology.md` — the secure coding checklist applies to every spoke
- `code-review/CodeReview_Checklist_Methodology.md` — security section of the review checklist

---

## Task Structure

```
SUBTASK_security/
├── _GLOBAL.md              (this document)
├── contracts/
│   └── _MANIFEST.yaml
├── SUBTASK_sec_injection/
│   └── _BRIEF.md
├── SUBTASK_sec_secrets/
│   └── _BRIEF.md
├── SUBTASK_sec_unsafe/
│   └── _BRIEF.md
├── SUBTASK_sec_event/
│   └── _BRIEF.md
└── SUBTASK_sec_synthesis/
    └── _BRIEF.md
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_sec_injection` | none | HTML injection / escaping gap: trace HtmlInputElement::value() through signal write to DOM render path | `SUBTASK_sec_injection/finding.md` |
| `SUBTASK_sec_secrets` | none | Secrets / infra data: scan diff for hardcoded IPs, creds, tokens, real server addresses | `SUBTASK_sec_secrets/finding.md` |
| `SUBTASK_sec_unsafe` | none | Unsafe code: detect new `unsafe` blocks, evaluate stated invariants | `SUBTASK_sec_unsafe/finding.md` |
| `SUBTASK_sec_event` | none | Event handler security surface: panic-on-downcast exposure + `closure.forget()` scope | `SUBTASK_sec_event/finding.md` |
| `SUBTASK_sec_synthesis` | `SUBTASK_sec_injection`, `SUBTASK_sec_secrets`, `SUBTASK_sec_unsafe`, `SUBTASK_sec_event` | Compile spoke findings into `findings.md` (verification gate) | `findings.md` (at SUBTASK_security/) |

### Dependency Graph

```
SUBTASK_sec_injection ──┐
                         │
SUBTASK_sec_secrets  ──┤── SUBTASK_sec_synthesis → findings.md
                         │
SUBTASK_sec_unsafe   ──┤
                         │
SUBTASK_sec_event    ──┘
```

---

## Contract

**Contract location:** `contracts/`
**Contract kind:** `yaml_schema`

See `contracts/_MANIFEST.yaml` for findings structure, ownership, and identities each spoke must satisfy.

### Structural Declarations

Each spoke MUST produce a `finding.md` at its own workspace root with this structure:

```markdown
## Finding

- **severity**: blocker | non-blocker | clean
- **concern**: [name of area]
- **location**: crates/ferric/src/file.rs:LINE (or N/A)
- **description**: [what was found or verified clean]

## What was examined
[Files, diff sections, and sub-questions examined]
```

### Ownership

| Artifact | Owning subtask |
|----------|----------------|
| `SUBTASK_sec_injection/finding.md` | `SUBTASK_sec_injection` |
| `SUBTASK_sec_secrets/finding.md` | `SUBTASK_sec_secrets` |
| `SUBTASK_sec_unsafe/finding.md` | `SUBTASK_sec_unsafe` |
| `SUBTASK_sec_event/finding.md` | `SUBTASK_sec_event` |
| `findings.md` (at SUBTASK_security/) | `SUBTASK_sec_synthesis` |

### Identities

- [ ] Every concern area (injection, secrets, unsafe, event surface) must appear in `findings.md` with a verdict
- [ ] `findings.md` must compile all 4 spoke findings into the format specified in the parent task's `_BRIEF.md`
- [ ] Any blocker must include a repository-relative location and actionable description

---

## Output Specifications

| Deliverable | Format | Location | Description |
|-------------|--------|----------|-------------|
| `findings.md` | Markdown | `SUBTASK_security/findings.md` | Compiled security findings with severity for each concern |
