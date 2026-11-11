# Task: SUBTASK_synthesis_gate — verification gate + fold (SYNTHESIS.md, PR)

## Task Specification
**Slug**: SUBTASK_synthesis_gate
**Task Kind**: synthesis
**Status**: Pending

### Objective
Act as the **verification gate** for the chirp-frontend (#9) subtree: verify the combined crate
against the frozen contract, build it (incl. the wasm target) and run the suites, emit a PASS/FAIL
verdict with a diff manifest and contract/wiring checks in **`SYNTHESIS.md`**, then **fold** —
commit the work, open the PR into `main`, write `COMPLETE.md`, and resolve the subtree.

This task is a **gate, not a prose summary**. It runs the four-check model (contract, wiring,
duplication, review) and either asserts coverage (PASS) or schedules remediation fix-tasks (FAIL)
via `engine_amend_plan { add_task }`; it MUST NOT silently plug a failing check.

### Context
Part of chirp-frontend (#9) — see `../_GLOBAL.md`. **Dependencies**: `SUBTASK_scaffold`,
`SUBTASK_api_client`, `SUBTASK_timeline`, `SUBTASK_compose`, `SUBTASK_profile` (all COMPLETED;
their files are in `../checkout/crates/chirp-frontend/`). You are the hub/fold for this subtree;
the overseer reads your `SYNTHESIS.md` verdict at its machine gate and does NOT re-run the build.

### Inputs
- `../_GLOBAL.md`, `../contracts/_MANIFEST.yaml` (identities + ownership), `../contracts/app_api.rs`,
  `../contracts/rest_endpoints.md`.
- The combined working tree at `../checkout/` on branch `work/chirp-frontend`.

### Declared output (you own this) + the fold
- `../SYNTHESIS.md` at the fold location (the SUSPENDED parent's directory) containing:
  - **Verdict**: PASS/FAIL over the manifest identities — workspace build **including**
    `cargo build -p chirp-frontend --target wasm32-unknown-unknown`; `cargo test -p chirp-frontend`;
    `cargo fmt --all --check`; `cargo clippy --workspace --all-targets -- -D warnings`.
  - **Diff manifest**: per-file summary of what each spoke produced (ownership coverage: every
    owned artifact has exactly one producer; no stub left unreplaced).
  - **Contract/wiring checks**: the SPA composes `chirp-types` DTOs as the wire contract (no
    redefinition); `ApiClient` calls `ferric-http` correctly and each method maps one-to-one to
    `rest_endpoints.md`; the route table binds the three frozen views + fallback; `no-panic/no-unsafe`
    in runtime modules; errors surface to the UI. Record any **REST-path assumptions** chirp-server
    #8 must honor (base URL `/api`, the endpoint table) so the reviewer can check cross-crate coherence.
  - Note the documented wasm-test posture (compile-only `wasm-bindgen-test`; no headless runner — not a FAIL).
- The **fold**: commit the Group-1 feature work on `work/chirp-frontend` (let Cargo author
  `Cargo.lock`; no attribution trailer; never touch `main`/force-push), open a **PR into `main`**
  with `Closes #9`, write `../COMPLETE.md`, and perform the synthesis fold (terminal
  `report_status { completed, artifact_path: ../SYNTHESIS.md }` + `resume_suspended`).

### Success criteria
- [ ] All manifest identities evaluated; verdict is explicit PASS/FAIL (not prose).
- [ ] On FAIL: per-violation remediation fix-tasks injected via `engine_amend_plan { add_task }`
      + a re-verification synthesis; nothing silently plugged.
- [ ] On PASS: PR opened into `main` on `work/chirp-frontend`, `Closes #9`; `SYNTHESIS.md` +
      `COMPLETE.md` written; subtree folded.

## Suggested Methodology Files
Domain Mapping: *Synthesizing/verifying a hub-and-spoke decomposition → Synthesis + Code Review + Code Quality*;
*PR creation via gh CLI → Operations + Code Review*.
- `synthesis/Synthesis_Overview_Methodology.md` (anchor — the four-check gate + `SYNTHESIS.md` schema).
- `synthesis/Synthesis_Contract_Verification_Methodology.md` — assert the frozen `contracts/` identities (Check 2).
- `synthesis/Synthesis_Wiring_Verification_Methodology.md` — routes bound, views mounted, client wired, no dead stubs.
- `synthesis/Synthesis_Duplication_Detection_Methodology.md` — no redefined DTOs / duplicated shared code.
- `synthesis/Synthesis_Code_Review_Methodology.md`, `synthesis/Synthesis_Remediation_Methodology.md` — review + remediation-as-decomposition.
- `testing/Testing_Strategy_Methodology.md`; `operations/GitWorkflow_PR_Lifecycle_Methodology.md` (+ `GitWorkflow_Syscall_PR_Review_Methodology.md`) for the PR.
Load `Synthesis_Overview_Methodology.md` first; load the rest as the subtree's shape warrants (you are the judge of coverage depth). Do NOT load `decomposition/` content — synthesis is the reassembly, not the split.

## Inherited Constraints
`../_GLOBAL.md` §Subtree-Wide Constraints. You are the ONLY task that performs the Group-2 git
(stage/commit/build/PR). Verify against the real combined tree (the scaffold stubs must be fully
replaced). The overseer gates on your verdict; a clean FAIL with remediation beats a plausible wrong PASS.

## Out-of-Scope Methodologies
Not `decomposition/` (decomposer-side only). Do not re-implement feature behaviour — verify it;
on inadequacy, inject remediation fix-tasks rather than editing a sibling's output inline.
