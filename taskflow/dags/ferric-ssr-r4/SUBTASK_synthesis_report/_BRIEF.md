# SUBTASK_synthesis_report: Verify CI + Update PR + Write SYNTHESIS.md

## Task Specification

**Slug**: SUBTASK_synthesis_report  
**Task Kind**: synthesis  
**Depends on**: SUBTASK_b2_wasm_tests  
**Status**: Pending  

### Objective

Verify that all 6 CI checks pass on the updated `work/ferric-ssr-r1` branch, update the PR #228 identity table to add `wasm-tests-pass: ✅`, and author the `SYNTHESIS.md` for the ferric-ssr-r4 DAG with verdict PASS or FAIL.

### Context

This task is part of ferric-ssr-r4 (see `_GLOBAL.md` in the parent workspace).

**Branch**: `work/ferric-ssr-r1` in `/home/user/nswe-demo` (B1 and B2 commits already applied)  
**PR**: #228 (Nousix-LLC/nswe-demo)

At this point both B1 (hydrate call + docstring fix) and B2 (3 wasm tests) should be committed and pushed. The synthesis task verifies the whole remediation is correct and complete.

#### 6 CI checks that must pass

1. `fmt` — `cargo fmt --all -- --check`
2. `clippy` — `cargo clippy --all-targets --all-features -- -D warnings`
3. `doc` — `cargo doc --no-deps --workspace`
4. `build` — `cargo build --workspace` (native + wasm32 targets)
5. `native-tests` — `cargo test --workspace`
6. `wasm-tests` — `wasm-pack test crates/ferric --headless` (the new B2 tests)

---

## Inputs

| Input | Location |
|---|---|
| Subtree hub | `taskflow/dags/ferric-ssr-r4/_GLOBAL.md` |
| B1 resolution | `taskflow/dags/ferric-ssr-r4/SUBTASK_b1_hydrate_fix/b1_resolution.md` |
| B2 resolution | `taskflow/dags/ferric-ssr-r4/SUBTASK_b2_wasm_tests/b2_resolution.md` |
| PR identity table | PR #228 description (via `gh pr view 228 --repo Nousix-LLC/nswe-demo`) |
| CI check results | Build server via SSH / GitHub Actions |

---

## Success Criteria

- All 6 CI checks confirmed passing (either via build server SSH verification or GitHub Actions run).
- PR #228 body updated with `wasm-tests-pass: ✅` in the identity assertions table.
- `SYNTHESIS.md` authored at `taskflow/dags/ferric-ssr-r4/SYNTHESIS.md` with verdict PASS or FAIL.
- `engine_resume_suspended` called to fold the parent ferric-ssr-r4 DAG.

---

## Declared Output

`taskflow/dags/ferric-ssr-r4/SYNTHESIS.md`

The file must carry:
- Verdict: PASS or FAIL
- Commit SHA(s) for B1 and B2 fixes on `work/ferric-ssr-r1`
- CI run URL or build server verification summary
- Summary of what was changed (B1: which lines in app.rs/ssr.rs; B2: which file, test names)
- Any residual concerns not addressed by this remediation
