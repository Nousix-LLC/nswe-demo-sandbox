# Task: hydrate_wasm.rs — Dimension 5: Assertion Quality

## Task Specification

**Slug**: SUBTASK_dim-assertions
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-reviewer

### Objective

Assess assertion quality in `hydrate_wasm.rs` (commit `75c1eef`): whether each
assertion would catch a real regression in the behavior it claims to test, whether
assertions check observable behavior or only that something ran, and whether any
key behavior is asserted at all. Produce `finding.md` with a severity label and
cited evidence.

### Context

This task is one of five parallel dimension spokes within SUBTASK_hydrate-wasm-quality
(see `../_GLOBAL.md`). It assesses exactly one dimension: assertion quality.

The file has three tests:
1. `hydrate_adopt_walk_no_structural_mutations` — REQ-SSR-004: adopt walk without structural mutations
2. `hydrate_event_wiring_post_hydration` — REQ-SSR-005: event wiring preserved post-hydration
3. `hydrate_mismatch_detection_recovery` — REQ-SSR-006: mismatch detection + DOM recovery

For each, the question is: would the assertions fail if the requirement they claim to
cover were broken? A test that returns `Ok(())` and asserts `true` covers nothing.
A test that checks `assert!(div.is_same_node(Some(&original_div)))` genuinely verifies
node identity preservation — but only if the original node reference was captured before
the operation under test.

---

## Input Specification

| Input | Source | Purpose |
|---|---|---|
| Subtree hub | `../_GLOBAL.md` | Subtree constraints and shared context |
| `hydrate_wasm.rs` | commit `75c1eef` | Primary file for this dimension |

**Reading the file:**
```bash
gh api "repos/Nousix-LLC/nswe-demo/contents/crates/ferric/tests/hydrate_wasm.rs?ref=75c1eef776953993ddd62dba1436845a0d53a281" \
  --jq '.content' | base64 -d
```

---

## Dimension Scope

Assess assertion quality in `hydrate_wasm.rs`:

**For each test, ask:**
1. What behavior does the test name claim to verify?
2. What do the assertions actually check?
3. Would the assertions fail if the claimed behavior were broken?
4. Is there any key behavior claimed by the test name that no assertion covers?

**Specific concerns to check:**
- **Test 1 (REQ-SSR-004)**: Does it check that the original DOM nodes were REUSED
  (not replaced)? `is_same_node` on the div and span? Does it cover text node identity
  too, or only element nodes?
- **Test 2 (REQ-SSR-005)**: Does it check that the event handler is wired (click →
  counter increments)? Does it verify this only works post-hydration, or would it also
  pass with a fresh mount?
- **Test 3 (REQ-SSR-006)**: Does it check that the mismatch is DETECTED (not silently
  ignored) and that the DOM RECOVERS (a `<p>` replaces the `<div>`)? Does it verify
  the old node is removed, or only that a `<p>` exists somewhere?

**What is not being assessed here:** whether the input HTML is SSR-faithful (sentinel
markers) — that is SUBTASK_dim-strings. Focus on whether the assertions are valid
given the input the test provides.

Do NOT assess: naming, cleanup, hardcoded strings, or structural duplication.

---

## Output Specification

**File**: `finding.md`
**Location**: `SUBTASK_dim-assertions/`

```markdown
## Assertion quality

**Severity**: [Blocker | Warning | Pass]
**Evidence**: [hydrate_wasm.rs:line or N/A]

[Finding text — plain voice, concrete, citable]
```

Severity semantics:
- **Blocker**: An assertion does not check the behavior it claims, so the test passes
  even when the requirement is broken.
- **Warning**: Assertions check the right behavior but are weaker than they could be;
  a regression in a secondary invariant could slip through.
- **Pass**: Assertions clearly verify the stated behavior and would fail on a regression.

---

## Success Criteria

- [ ] All three tests assessed for assertion strength
- [ ] Each test's assertions mapped to its stated requirement (REQ-SSR-004/005/006)
- [ ] Any gaps between claimed coverage and actual assertion coverage stated explicitly
- [ ] Severity assigned with rationale
- [ ] Evidence cites specific line(s) in hydrate_wasm.rs
- [ ] `finding.md` written to this task's workspace

---

## Methodology Guidance

**Primary**: `rust/Rust_Testing_Methodology.md` — assertion quality, behavior coverage
**Secondary**: `code-review/CodeReview_Checklist_Methodology.md` — assertion audit checklist

---

## Inherited Constraints

- **Repository**: Nousix-LLC/nswe-demo, commit `75c1eef776953993ddd62dba1436845a0d53a281`
- **Do not re-raise**: Issues #229–#242
- **Do not reference**: Overseer I267 escalation comments
- **Prose bar**: No AI-tell patterns in output text
- **Scope**: Code quality only — security scope belongs to SUBTASK_security
