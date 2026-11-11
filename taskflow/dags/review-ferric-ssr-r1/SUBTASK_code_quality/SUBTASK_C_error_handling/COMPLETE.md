# COMPLETE — Area C: Error Handling

**Task**: SUBTASK_C_error_handling
**Status**: completed
**Verdict**: FINDING (NON-BLOCKER)

## Output

`area_c_error_handling.md` — produced at this workspace.

## Summary

Two non-blocking findings in PR #228's new error-handling surface:

1. `crates/ferric/src/hydrate.rs:217` — `let _ = element.remove_child(node)` in `strip_sentinels` discards the `Result` silently on a correctness-critical operation (index-alignment sentinel removal). Resolution: replace with `.expect(...)` that names the invariant.

2. `crates/chirp-server/src/ssr.rs:99` — `debug_assert!` for attribute-injection prevention is elided in release builds. The function is `pub`; a future dynamic caller would have no production guard. Resolution: promote to `assert!` or escape the value before interpolation.

The primary rendering path (`ferric::render_to_string`) is infallible by design and contains no `unwrap`/`expect`. All `expect()` calls in the hydration adopt-pass and reactive-update path carry descriptive messages and assert invariants the library controls. No blocker-level finding.
