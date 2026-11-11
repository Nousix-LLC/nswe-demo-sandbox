# Task: Event Handler Security Surface and closure.forget() Scope

## Task Specification

**Slug**: SUBTASK_sec_event
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-reviewer

### Objective

Assess whether the new event-carrying handler path exposes a surface for a crafted event to cause unexpected behavior (e.g., panics on downcast that could be triggered by a remote actor), and verify that the `closure.forget()` pattern in the WASM test is limited strictly to test scope and does not leak into production code paths.

---

## Context

This task is part of the security review subtree for PR #193. See `../_GLOBAL.md` for full scope and constraints.

**Files changed by the remediation commits relevant to this concern:**
- `crates/ferric/src/vdom.rs` — B2 adds `EventHandler::WithEvent` variant; closure receives a `&dyn Any`
- `crates/ferric/src/dom.rs` — B2 event dispatch; this is where the downcast happens
- `crates/ferric/src/form.rs` — B3 adds WASM test; `closure.forget()` appears here

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Project context | `../_GLOBAL.md` | Scope and constraints |
| PR diff | `gh pr diff 193 --repo Nousix-LLC/nswe-demo` | Changed lines |
| vdom.rs | `crates/ferric/src/vdom.rs` | EventHandler enum definition and dispatch |
| dom.rs | `crates/ferric/src/dom.rs` | Event dispatch path — where downcast occurs |
| form.rs | `crates/ferric/src/form.rs` | WASM test with closure.forget() |

---

## Review Questions

1. Does the new event-carrying handler path have any surface for a crafted event to cause unexpected behavior — specifically, can a panic on a failed type downcast (e.g., `dyn Any → web_sys::Event`) be triggered by a remotely-controlled event type, and if so is the panic reachable from browser event delivery?
2. Is the `closure.forget()` pattern in the WASM test limited to test scope only, and does it not appear in any production code path in the diff?

---

## Output Specification

**Primary Output:** `finding.md` at this task's workspace root (`SUBTASK_sec_event/finding.md`)

The finding file MUST follow the schema in `../_GLOBAL.md` §Contract:

```markdown
## Finding

- **severity**: blocker | non-blocker | clean
- **concern**: Event handler security surface / closure.forget() scope
- **location**: crates/ferric/src/file.rs:LINE (or N/A)
- **description**: [what was found or verified clean — be specific about the downcast mechanism and closure scope]

## What was examined
[Files read, diff sections reviewed, and which sub-questions above were answered]
```

---

## Suggested Methodology Files

Task type row (Domain Mapping): **Security review / Rust library** → Primary: `security`, Supporting: `rust`

- `security/Security_Secure_Coding_Methodology.md` — input validation and error handling in event paths; panic-on-invalid-input patterns
- `rust/Rust_WebAssembly_Browser_Methodology.md` — `closure.forget()` patterns, wasm-bindgen lifecycle, and why `JsValue` / closure ownership works the way it does in browser contexts

These are SUGGESTIONS. The agent is the final judge of what its work requires.

## Inherited Constraints

- Repository-relative paths only in all findings
- Focused pass on the three remediation commits only
- Severity `blocker` only for concrete security vulnerability — a panic-on-downcast is a blocker if it is reachable by a remotely-controlled event and causes a DoS or exploitable condition; a panic confined to test infrastructure is not a blocker

## Success Criteria

- [ ] Both review questions answered with evidence from the diff and source files
- [ ] `finding.md` produced with `severity` assigned
- [ ] The downcast mechanism in dom.rs evaluated explicitly (whether the downcast is guarded, e.g. by `downcast_ref` with a match, or unguarded with `unwrap`/`expect`)
