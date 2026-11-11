# Task: Re-verification gate for `chirp-server` (round 1) — re-run the gate, then deliver on PASS

## Task Specification

**Slug**: SUBTASK_reverify_gate
**Task Kind**: synthesis
**Status**: Pending
**Round**: 1 (remediation ceiling = 3; see §Bounded recursion)

### Objective

Act as the **re-verification gate** for the `chirp-server` subtree after the F1 remediation lands.
Re-run the authoritative build/test/fmt/clippy **and** the four-check model over the combined
output. **Only if every check now passes**: push `work/chirp-server`, open the PR into `main`, and
write the authoritative **PASS** `SYNTHESIS.md` fold record at the hub (`../SYNTHESIS.md`). If any
check still fails, record a clean FAIL and schedule the next remediation round (unless the ceiling
is reached — then escalate). This is the task that replaces `SUBTASK_synthesis_gate` as the terminal
gate; the original gate FAILED on finding F1 and deliberately did **not** open a PR on broken work.

### Context

Injected by `SUBTASK_synthesis_gate` on its FAIL verdict (see `../SYNTHESIS.md`, finding F1 +
injected-fix-task manifest). You run after the one fix-task completes. The subtree parent
(`chirp-server`) resolves once every child — including you — is terminal; your PASS `SYNTHESIS.md`
at the hub is the fold record the overseer observes at the observation seam (`_FORK.md`).

**Dependencies**: `SUBTASK_fix_validation_error_mapping` (the F1 fix).
**Dependents**: none — your `SYNTHESIS.md` at the hub is the terminal fold/observation record.

### Process / Approach — this is a verification GATE (re-run, do not summarize)

1. **Assemble context cold**: read `../_GLOBAL.md`, `../contracts/_MANIFEST.yaml` (the `identities`
   assertion set), the three spoke handoffs, `../SYNTHESIS.md` (the prior FAIL + F1), and
   `../SUBTASK_fix_validation_error_mapping/FIX_NOTES.md` (what the fix changed).
2. **Re-run the authoritative mechanical identities** from the clone at `../checkout`:
   `cargo build --workspace`, `cargo test` (unit + integration, no DB), `cargo fmt --check`,
   `cargo clippy --all-targets -- -D warnings`. Capture real output as evidence.
3. **Re-run the four checks** — contract, wiring, duplication, code-review — over the combined
   output, re-using the same mechanical directives the first gate used. **Specifically re-verify F1**:
   a well-formed-JSON body with an invalid DTO field value now returns **400** + `ApiError` with
   `code == VALIDATION_ERROR` and non-empty `details` (confirm the characterization test now asserts
   the contract, not 422). Also confirm the fix introduced no regression and no new duplication/dead
   code and did not re-declare any `chirp-types` DTO.
4. **Decision.**
   - **PASS** (all identities + four checks clean): push `work/chirp-server`; open the PR into `main`
     with `gh pr create` (title = `contracts/_MANIFEST.yaml` `conventions.pr.title`; body summarizes
     design + the now-conforming error contract + test results and **ends with `Closes #8`**); then
     write the hub `../SYNTHESIS.md` as a **PASS** fold record carrying the build/test/fmt/clippy
     verdicts, the four-check results, the diff manifest, the **PR URL**, and `round: 1`.
   - **FAIL** (a check still fails): do NOT open a PR. Record a FAIL `SYNTHESIS.md` with evidence and,
     if `round < 3`, inject one fix-task per residual violation + one further re-verification gate
     (`round: 2`), per the remediation methodology. If `round` would exceed 3, do NOT inject another
     round — record the unresolved violation prominently and escalate to the session LLM.

### Methodology

Read `synthesis/Synthesis_Overview_Methodology.md` first (the four-check model + the `SYNTHESIS.md`
schema + PASS/FAIL decision), then the sibling check/remediation files your reading requires. You are
the final judge of coverage depth, but the gate posture (four checks + no-green-wash + remediation)
is mandatory.

### Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, success criteria, identities |
| Contract | `../contracts/_MANIFEST.yaml` | The `identities` assertion set + error-mapping + ownership |
| Prior gate verdict | `../SYNTHESIS.md` | The FAIL + finding F1 you re-verify |
| Fix handoff | `../SUBTASK_fix_validation_error_mapping/FIX_NOTES.md` | What the fix changed |
| Spoke handoffs | `../SUBTASK_scaffold_and_repository/IMPLEMENTATION_NOTES.md`, `../SUBTASK_api_layer/API_NOTES.md`, `../SUBTASK_integration_tests_and_docs/TEST_NOTES.md` | The combined output claims |
| Committed code | the shared clone at `../checkout` | The real assembled crate to re-verify + deliver |

### Output Specification

| Attribute | Value |
|-----------|-------|
| Primary (fold record) | `SYNTHESIS.md` at the **hub** (`../SYNTHESIS.md`, i.e. `/home/user/nousix-runtime/nswe-demo/taskflow/dags/chirp-server/SYNTHESIS.md`) — overwrite the interim FAIL with the authoritative verdict |
| On PASS | the pushed branch + the PR into `main` (`Closes #8`), PR URL recorded in `SYNTHESIS.md` |

Must contain: build/test/fmt/clippy verdicts, four-check results (with the F1 re-check called out),
diff manifest, PR URL (on PASS), the round counter, and an overall **PASS/FAIL** prominent.

### Success Criteria

- [ ] All contract `identities` re-evaluated with real command output captured as evidence (no assertion skipped, no silent plug).
- [ ] F1 explicitly re-verified: invalid DTO field → 400 `ApiError`/`VALIDATION_ERROR` with `details`; characterization test asserts the contract.
- [ ] On PASS: branch pushed, PR into `main` opened with body ending `Closes #8`, PR URL recorded.
- [ ] On FAIL: clean FAIL + evidence; remediation scheduled (round ≤ 3) or escalated at the ceiling; no false PASS.
- [ ] Hub `../SYNTHESIS.md` written with verdicts, four-check results (incl. F1), diff manifest, PR URL (on PASS), round, and PASS/FAIL prominent.

## Suggested Methodology Files

Matched Domain-Mapping row: **Synthesizing / verifying a hub-and-spoke decomposition → primary
`synthesis`; supporting `code-review`, `code-quality`**; plus `testing` (judge the suite incl. the
flipped F1 test) and `operations` (the push + `gh pr create` mechanics).

- `synthesis` — `synthesis/Synthesis_Overview_Methodology.md` (anchor; four-check + schema + decision), `synthesis/Synthesis_Contract_Verification_Methodology.md` (re-assert the contract identities incl. the F1 error path), `synthesis/Synthesis_Wiring_Verification_Methodology.md`, `synthesis/Synthesis_Duplication_Detection_Methodology.md`, `synthesis/Synthesis_Code_Review_Methodology.md`, `synthesis/Synthesis_Remediation_Methodology.md` (the round-2 FAIL path + ceiling/escalation).
- `code-review` — `code-review/CodeReview_Checklist_Methodology.md` for the (small) fix diff review.
- `operations` — `operations/GitWorkflow_PR_Lifecycle_Methodology.md` for the push + `gh pr create` flow on PASS.

The gate posture (four-check + remediation) is mandatory; how deeply you run each check is your judgment.

## Inherited Constraints

- Run the authoritative checks from the ONE shared clone at `../checkout` — do NOT re-clone.
- Report honestly: a clean FAIL with evidence beats a green-washed PASS. Do not modify spoke/fix code to force a pass; schedule remediation instead.
- Never commit to / force-push `main`; the only write to `main` is via the PR. No commit-attribution trailers.
- `Closes #8` must end the PR body; PR title per the contract's `conventions.pr.title`.
- Carry `round` forward (this is round 1); ceiling = 3, then escalate rather than loop.

## Out-of-Scope Methodologies

- Decomposition methodologies are decomposer-side only: a gate never loads `decomposition/` content. Remediation (if needed) is a targeted Inject per `synthesis/Synthesis_Remediation_Methodology.md`, not a re-plan of the subtree.
- Do NOT author feature code yourself; incomplete/broken work is a FAIL + remediation, not a fix-in-the-gate. (Gate finding F2 — rustdoc intra-doc-link nits — is non-gating tracked debt; do not block on it.)
