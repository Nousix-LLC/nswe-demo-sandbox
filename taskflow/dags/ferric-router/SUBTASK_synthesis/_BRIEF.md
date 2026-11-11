# Task: ferric-router synthesis verification gate + delivery

## Task Specification
**Slug**: SUBTASK_synthesis
**Task Kind**: synthesis
**Status**: Pending

### Objective
Run the **verification gate** over the combined output of the implementation spokes, then **deliver**
the verified result: push `work/ferric-router` and open the PR into `main` (`Closes #5`), and author
`SYNTHESIS.md` at the subtree root carrying the PASS/FAIL verdict + the PR URL.

> This task is a **verification gate, NOT a prose summary.** It runs the four-check model against the
> frozen contract and either asserts coverage (PASS) or schedules remediation fix-tasks (FAIL). Report
> honestly — a clean FAIL with evidence beats a green-washed pass.

### Context
Final task of the `ferric-router` work-item (see `../_GLOBAL.md`, `../contracts/`). The scaffold +
matcher + navigation + view spokes are COMPLETED; the crate is implemented in `checkout/` on branch
`work/ferric-router`. You verify, then deliver. You do NOT own any `src/` file — you assert over them.

**Dependencies**: `SUBTASK_scaffold`, `SUBTASK_matcher`, `SUBTASK_navigation`, `SUBTASK_view`.

## Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Hub | `../_GLOBAL.md` | success criteria, PASS bar, constraints |
| Frozen contract | `../contracts/_MANIFEST.yaml` (identities + ownership), `../contracts/ferric_router_api.rs` | the assertion set to enumerate and run; the ownership map to check |
| Combined output | `<subtree_root>/checkout/` on `work/ferric-router` | the implemented crate you build/test/review |
| Spoke records | each `../SUBTASK_*/COMPLETE.md` | what each spoke claims it produced |

## What to do (approach — the gate, then delivery)
Run the gate as a **mechanical-then-review** process over the clone:
1. **Contract check** — enumerate every identity in `_MANIFEST.yaml` and run its `check`; record each
   exit code. Minimum set: `cargo build --workspace`; `cargo build -p ferric-router --target
   wasm32-unknown-unknown`; `cargo test -p ferric-router` (incl. matcher param-extraction);
   `cargo build -p ferric-router --example app --target wasm32-unknown-unknown`; `cargo fmt --all
   --check`; `cargo clippy --all-targets -- -D warnings`; a compile-only `use ferric_router::prelude::*;`
   resolving every frozen item. For `wasm_bindgen_test_optional`: compile for wasm32; RUN only if a
   headless-browser runner is available — if none, record it as a documented non-FAIL (native tests +
   wasm build remain the gate).
2. **Wiring check** — no `todo!()`/`unimplemented!()` left in `src`/`examples`; every frozen prelude item
   reachable; the example actually exercises matcher→router→outlet→link.
3. **Duplication check** — one producer per owned path (manifest ⇄ git authorship); no module re-implements
   `ferric`'s reactivity/DOM or a sibling's module; no foreign writes.
4. **Code review** — a principal-level read of the public router API + implementations (correctness,
   clarity, the documented `preventDefault` composition constraint, extensibility for a later SPA).
5. **Verdict & remediation** — overall **PASS** requires: workspace + ferric-router wasm build succeed,
   native tests pass, fmt + clippy clean. On any failure, do NOT plug it silently: author a clear FAIL
   verdict and schedule remediation as decomposed fix-task(s) via `engine_amend_plan { add_task }`
   (Inject), then re-verify. A documented missing browser runner is NOT a FAIL.
6. **Deliver** (on PASS, or on FAIL per the honest-report rule): push `work/ferric-router`; open the PR
   into `main` with `gh pr create`, title `ferric-router: client-side router (History API)`, body
   summarizing design + build/test results, ending `Closes #5`. NEVER touch/force-push `main`.
7. **Author `SYNTHESIS.md`** at the subtree root (`<subtree_root>/SYNTHESIS.md` — this is the
   observation seam the overseer reads): build verdict, test verdict, fmt/clippy results, the four-check
   table with mechanical evidence, a diff manifest, the **PR URL**, and the overall **PASS/FAIL**.

## Outputs (you own)
- `<subtree_root>/SYNTHESIS.md` — the gate verdict + fold record (prominent PR URL + PASS/FAIL).
- the pushed branch + the opened PR (delivery of the verified result).

## Success Criteria (the gate cannot be read and missed as a gate)
- [ ] All `_MANIFEST.yaml` identities enumerated and each run; exit codes recorded in `SYNTHESIS.md`.
- [ ] Four checks (contract / wiring / duplication / code-review) each executed with mechanical evidence.
- [ ] No identity silently plugged; any failure → FAIL verdict + injected remediation fix-task(s) + re-verify.
- [ ] PR opened into `main` with `Closes #5`; PR URL + PASS/FAIL prominent in `SYNTHESIS.md`; `main` never touched.
- [ ] PASS only if workspace + ferric-router wasm build succeed, native tests pass, fmt + clippy clean.

## Constraints
- `../contracts/` READ-ONLY — verify AGAINST it; do not edit it.
- Do not modify spoke `src/` outputs to make the gate pass — on failure, remediate via amendment, not inline edits.
- NEVER commit to or force-push `main`; no commit-attribution trailers.

## Suggested Methodology Files (parent's flags — you are the final judge of coverage depth)
Task type (Domain Mapping): **Synthesizing/verifying a hub-and-spoke decomposition** → primary
**Synthesis**, supporting **Code Review**, **Code Quality**, **Testing**. Load `Synthesis_Overview` first (always):
- `synthesis` — `synthesis/Synthesis_Overview_Methodology.md` (the four-check gate + `SYNTHESIS.md` schema — anchor, always),
  `synthesis/Synthesis_Contract_Verification_Methodology.md` (Check 2 — this subtree froze a contract, so run it),
  `synthesis/Synthesis_Wiring_Verification_Methodology.md`, `synthesis/Synthesis_Duplication_Detection_Methodology.md`,
  `synthesis/Synthesis_Code_Review_Methodology.md`, `synthesis/Synthesis_Remediation_Methodology.md` (on any FAIL).
- `code-review` — `code-review/CodeReview_Checklist_Methodology.md`.
- `operations` — `operations/GitWorkflow_PR_Lifecycle_Methodology.md` (push + `gh pr create` + `Closes #5`).
Load the sibling check files your reading of the subtree reveals you need; you judge coverage depth —
*that* you run a gate is prescribed, *how deeply* is your judgment.

## Inherited Constraints
PASS bar fixed by the hub; `contracts/` read-only; honest reporting (clean FAIL + evidence > green-wash);
deliver via PR into `main` only; no attribution trailers. A missing headless-browser runner is a
documented non-FAIL.

## Out-of-Scope Methodologies
Do NOT load `decomposition/` — synthesis is the reassembly, not the split. Do NOT author crate `src/`
code (remediate via injected fix-tasks instead).
