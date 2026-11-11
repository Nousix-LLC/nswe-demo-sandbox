# COMPLETE — SUBTASK_workflow_correctness

**Task**: Review `.github/workflows/ci.yml` at PR #21 head `c8123376` for concern 1 (CI workflow
correctness) and concern 2 (reproducibility / pinning); emit findings in the frozen schema.
**Decompose evaluation**: Atomic (single ~194-line artifact, one review responsibility, one output).
**Status**: Completed. Read-only review — nothing pushed, changed, merged, or reviewed on GitHub.

## What was done
- Loaded the suggested methodology (operations: `DevTools_CICD`, `DevTools_Build_Systems`) and the
  frozen contract (`../contracts/findings_schema.md`, `../contracts/_MANIFEST.yaml`).
- Fetched `ci.yml` at head `c8123376` (via `gh api … ?ref=c8123376`), with line numbers for cites.
- Gathered evidence read-only: `gh pr view 21` (files, triggers, job names, head), `gh pr checks 21`
  (live: fmt/clippy/test/wasm/doc = pass, image = skipping), `Cargo.lock` at head (wasm-bindgen
  version), YAML validity (`python3 -c yaml.safe_load`). `actionlint` not installed locally; relied
  on the already-folded machine-PASS (actionlint green at head per `../_GLOBAL.md`).

## Key results
- **Concern 1 (correctness): CLEAN.** All five PR/push jobs run their stated commands (verified
  line-by-line); triggers correct (PR+push→main, +dispatch); job names stable (name==id) and
  required-check-friendly; `image` correctly excluded from PR required checks; caching sound;
  `--locked` consistent everywhere it applies.
- **Concern 2 (reproducibility/pinning): sound core, 2 minor drift notes.** Verified
  `wasm-bindgen-cli 0.2.129` == `Cargo.lock` `wasm-bindgen 0.2.129` (no skew). `--locked` throughout;
  `rust-cache@v2` cache key (`Cargo.lock`+rustc) correct and non-divergent under `--locked`.
  WF-1 (toolchain series-float `"1.97"`) and WF-2 (manifest MSRV 1.82 not enforced by CI) are minor.

## Roll-up: block 0 · major 0 · minor 2 (WF-1, WF-2) · nit 0
On this spoke's scope, nothing blocks landing. Cross-references recorded (action SHA-pinning →
`SUBTASK_supply_chain_security`; `image` internals → `SUBTASK_image_job`) without adjudicating them.

## Output
- `SUBTASK_workflow_correctness/findings.md` — conformant to `../contracts/findings_schema.md`
  (`WF-` ids, severity enum, location+rationale per finding, head stated, concern-coverage notes,
  spoke roll-up). Consumed next by `SUBTASK_synthesis`.
