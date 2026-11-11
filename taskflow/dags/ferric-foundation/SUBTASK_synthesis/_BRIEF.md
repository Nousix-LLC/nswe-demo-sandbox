# Task: Synthesis verification gate — verify, deliver (PR), and fold

**Slug**: SUBTASK_synthesis
**Task Kind**: synthesis
**Status**: Pending

## Objective
Act as the **verification gate** for the `ferric-foundation` subtree: mechanically verify that the
combined output of the implementation spokes satisfies the contract identities, deliver the
verified result as a PR into `main`, and author the `SYNTHESIS.md` verdict. This is **not** a prose
summary — it is a gate that either asserts coverage (**PASS**) or schedules remediation fix-tasks
(**FAIL**).

## Context
Final child of the `ferric-foundation` subtree (see `../_GLOBAL.md`). You depend on every
implementation spoke and read their combined output in the shared clone at `../checkout/`. You
author `SYNTHESIS.md` at the **subtree root** (`../SYNTHESIS.md`) — this is the fold record that
resolves the parent `ferric-foundation` node; make the **PR URL** and the **PASS/FAIL** verdict
prominent so the overseer can gate without re-running the build.

**Dependencies**: `SUBTASK_scaffold`, `SUBTASK_reactive_core`, `SUBTASK_view_and_diff`,
`SUBTASK_dom_runtime`.

## Inputs
- `../_GLOBAL.md`; `../contracts/_MANIFEST.yaml` (read-only — the **identities** you enumerate and
  run, and the **ownership** you check for coverage/duplication); `../contracts/ferric_api.rs`
  (the frozen public surface you assert is present).
- The combined output in `../checkout/` on branch `work/ferric-foundation`.
- The spokes' `COMPLETE.md` records (e.g. whether wasm-bindgen-test was runnable).

## Scope — the gate (run the four checks over the combined output)
1. **Contract verification** — enumerate every identity in `_MANIFEST.yaml` and run its `check`
   inside `../checkout/`: `cargo build --workspace`; `cargo build -p ferric --target
   wasm32-unknown-unknown`; `cargo test --workspace`; `cargo fmt --all --check`; `cargo clippy
   --all-targets -- -D warnings`; the `public_api_surface` import check; the counter-example wasm
   build. Record each exit result. The frozen public surface in `ferric_api.rs` must be present.
2. **Wiring / no-dead-code** — each module stub is now implemented and reachable from the prelude;
   no layer left as `todo!()`; the counter example actually exercises mount→render→event→re-render.
3. **Duplication / ownership** — exactly one producer wrote each owned path; no spoke re-implemented
   or paraphrased another's surface instead of importing it.
4. **Combined review** — a brief principal-level read of the public API for soundness and
   ergonomics against the "a Twitter-style SPA can be built on this later" bar.

**Delivery**: when the build/test/fmt/clippy identities pass, **push** `work/ferric-foundation`
and **open a PR into `main`** with `gh pr create` — title `ferric-foundation: workspace + ferric
core`, body summarizing the design + test results and ending with `Closes #4`. **Never** commit to
or force-push `main`. No commit-attribution trailers.

**On FAIL**: do not green-wash and do not silently fix — schedule remediation as decomposed
fix-task(s) via `engine_amend_plan { add_task }` (additive), scoped to the failing identity, and
record the FAIL with evidence. A clean FAIL with evidence beats a false PASS. (Browser-test
tooling being unavailable is **not** a FAIL on its own — document it; native tests + the wasm
*build* remain the gate, per the brief.)

## Outputs
- `../SYNTHESIS.md` (at the subtree root — the fold record), containing: a **build verdict**
  (workspace build + `ferric` wasm build), a **test verdict** (`cargo test` results, and
  wasm-bindgen-test status), **fmt/clippy** results, a **diff manifest** (files added/changed),
  the **PR URL**, and an overall **PASS/FAIL**.
- The pushed branch + the opened PR.

## Success criteria (carry the gate obligation — you cannot read this brief and miss that it is a gate)
- [ ] Every `_MANIFEST.yaml` identity was enumerated and its `check` run; results recorded.
- [ ] PASS requires: workspace build + `ferric` wasm build succeed, native tests pass, fmt + clippy
      clean. Otherwise FAIL with evidence + remediation fix-task(s) scheduled.
- [ ] Ownership coverage/duplication verified; frozen public surface present.
- [ ] PR opened into `main` from `work/ferric-foundation`, body ends with `Closes #4` (when PASS).
- [ ] `../SYNTHESIS.md` authored with PR URL + PASS/FAIL prominent; parent folded via
      `engine_resume_suspended` with `seam_path` = `../SYNTHESIS.md`.

## Suggested Methodology Files
Matched Domain-Mapping row (verbatim): **Synthesizing / verifying a hub-and-spoke decomposition
(contract + wiring + dedup + review gate) → Primary: Synthesis; Supporting: Code Review, Code
Quality**. Load `synthesis/Synthesis_Overview_Methodology.md` **first** (the four-check model + the
`SYNTHESIS.md` schema), then load as your reading of the subtree requires:
- `synthesis/Synthesis_Contract_Verification_Methodology.md` — Check 2; run the manifest identities
  as the assertion set (this subtree froze a `rust_trait` seam, so this file applies).
- `synthesis/Synthesis_Wiring_Verification_Methodology.md` — no `todo!()` left detached; prelude
  reachable; example exercises the whole path.
- `synthesis/Synthesis_Duplication_Detection_Methodology.md` — one producer per owned path.
- `synthesis/Synthesis_Code_Review_Methodology.md` + `code-review/CodeReview_Checklist_Methodology.md`
  — the combined-output review.
- `synthesis/Synthesis_Remediation_Methodology.md` — remediation-as-decomposition on FAIL.
- `operations/GitWorkflow_PR_Lifecycle_Methodology.md` + `code-review/CodeReview_PR_Authoring_Methodology.md`
  — pushing the branch and authoring the PR via `gh`.
You run a gate (prescribed); how deeply you run each check is your judgment — load fewer if a check
is clearly inapplicable, more if the subtree reveals additional surface.

## Inherited Constraints
- `contracts/` is read-only; verify against it, do not edit it.
- Never commit to / force-push `main`; branch `work/ferric-foundation` only; no attribution trailers.
- Report honestly — a clean FAIL with evidence is more useful than a green-washed PASS.

## Out-of-Scope Methodologies
- Decomposition (`decomposition/`) bundles are decomposer-side only — a synthesis gate never loads
  them. Do not implement framework features yourself; if something is missing, schedule a
  remediation fix-task rather than writing the feature inline.
