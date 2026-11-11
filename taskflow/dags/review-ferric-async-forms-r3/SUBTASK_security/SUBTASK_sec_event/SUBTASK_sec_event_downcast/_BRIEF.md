# Task: Assess Panic-on-Downcast Reachability in EventHandler::WithEvent

## Task Specification

**Slug**: SUBTASK_sec_event_downcast
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-reviewer

### Objective

Determine whether the new `EventHandler::WithEvent` dispatch path in `dom.rs` exposes a surface for a panic triggered by a failed type downcast (e.g., `dyn Any → web_sys::Event`) that could be reached by a remotely-controlled browser event, and assess whether such a panic, if reachable, would constitute a Denial-of-Service condition.

---

## Context

This task is part of the event handler security surface decomposition. See `../_GLOBAL.md` for full scope and constraints.

**Relevant diff:** PR #193 remediation commit B2 adds `EventHandler::WithEvent` variant in `vdom.rs` and the dispatch logic in `dom.rs` where the actual downcast occurs.

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree context | `../_GLOBAL.md` | Scope and constraints |
| PR diff | `gh pr diff 193 --repo Nousix-LLC/nswe-demo` | Changed lines |
| vdom.rs | `crates/ferric/src/vdom.rs` | `EventHandler::WithEvent` enum definition |
| dom.rs | `crates/ferric/src/dom.rs` | `set_events()` dispatch — the downcast site |

---

## Review Questions

This task answers exactly one question:

> Does the new `EventHandler::WithEvent` dispatch path have any surface for a crafted event to cause unexpected behavior — specifically, can a panic on a failed type downcast (`dyn Any → web_sys::Event`) be triggered by a remotely-controlled event type, and if so is the panic reachable from browser event delivery?

Specific sub-checks:
1. What is the concrete Rust type of `event` at the downcast site in `dom.rs`? Is it always `web_sys::Event` by construction (Closure type constraint) or is it polymorphic?
2. Does the dispatch use a guarded downcast (`downcast_ref` with `if let`) or an unguarded one (`unwrap`/`expect`/`downcast`)?
3. If the downcast is guarded: can a remote actor reach the unguarded path at all? What does the browser's event delivery contract guarantee about the type at the wasm-bindgen boundary?
4. If the downcast is unguarded: is the panic reachable from normal browser event delivery? What type controls the value at the panic site?

---

## Output Specification

**Primary Output:** `finding_downcast.md` at this task's workspace root (`SUBTASK_sec_event_downcast/finding_downcast.md`)

```markdown
## Sub-Finding: Downcast Reachability

- **severity**: blocker | non-blocker | clean
- **concern**: EventHandler::WithEvent downcast safety
- **location**: crates/ferric/src/dom.rs:LINE (or N/A)
- **description**: [specific answer: is the downcast guarded? can a remote actor cause a panic? cite the evidence]

## What was examined
[Specific lines of dom.rs diff, the Closure type parameter, the downcast mechanism]
```

---

## Suggested Methodology Files

Task type row (Domain Mapping): **Security review / Rust library** → Primary: `security`, Supporting: `rust`

- `security/Security_Secure_Coding_Methodology.md` — input validation and error handling; panic-on-invalid-input patterns in security review
- `rust/Rust_WebAssembly_Browser_Methodology.md` — wasm-bindgen closure type parameters, what guarantees the browser's event delivery makes about the Rust type at the closure boundary

These are SUGGESTIONS. The agent is the final judge of what its work requires.

## Inherited Constraints

- Repository-relative paths only in all findings
- Severity `blocker` only if panic is concretely reachable by a remote actor and causes DoS; a panic that cannot be reached from browser event delivery is not a blocker
- Focused pass on the three remediation commits only (9fedad9, 9557f0c, 838239e)

## Success Criteria

- [ ] The downcast mechanism in dom.rs evaluated explicitly (guarded vs. unguarded)
- [ ] The Closure type parameter at the dispatch site identified
- [ ] Whether a remote actor can inject a non-`web_sys::Event` type at the boundary assessed
- [ ] `finding_downcast.md` produced with `severity` assigned and evidence cited
