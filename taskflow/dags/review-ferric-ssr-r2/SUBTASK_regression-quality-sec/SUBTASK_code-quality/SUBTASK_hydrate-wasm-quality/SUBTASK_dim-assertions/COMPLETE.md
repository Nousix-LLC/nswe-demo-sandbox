# Completion Record — SUBTASK_dim-assertions

**Task**: Assess assertion quality in `hydrate_wasm.rs` (commit `75c1eef`)
**Output**: `finding.md` in this workspace

## What was done

Read `hydrate_wasm.rs` at commit `75c1eef776953993ddd62dba1436845a0d53a281` via the GitHub API. Applied `Rust_Testing_Methodology.md` §Assertion patterns and Anti-Pattern 5 (tests that pass when code is wrong) to each of the three tests in the file.

## Verdict

**Warning** — see `finding.md` for per-test evidence.

## Per-test findings

- **Test 1 (REQ-SSR-004)**: Checks element identity (`is_same_node` on `<div>` and `<span>`) but not text node identity. A hydration regression that re-creates the "hello" text node while preserving element nodes would not be caught.
- **Test 2 (REQ-SSR-005)**: Sound. `text_content() == Some("1")` checks event wiring; `is_same_node` checks adoption vs. fresh mount. Both would fail on the primary failure modes.
- **Test 3 (REQ-SSR-006)**: Sound for the realistic failure modes. `first_child.tag_name == "p"` catches the main regression (server `<div>` not replaced). Minor gap: container child count not checked.

## Outputs produced

- `finding.md`
