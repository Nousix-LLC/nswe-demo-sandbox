# COMPLETE — SUBTASK_performance_and_benchmark (concern 8)

## What was done

Designed Ferric's performance bar and benchmark plan — a reproducible **js-framework-benchmark** entry measuring
speed, memory, and bundle size, with a comparison method against named peers that states its conditions and keeps
measured results separate from expectations. Authored the `REQ-PERF-*` register. Design only; no benchmark code,
per the brief and identity I1.

## Output produced

- `performance-and-benchmark.md` (this workspace) — the benchmark plan + the `REQ-PERF-*` register.
  Repo target (placed later by `SUBTASK_design_pr`): `design/ferric/performance-and-benchmark.md`.

## Structure of the deliverable

- **§1 The benchmark entry** — the suite's standard row-table app implemented through Ferric's public API, in the
  **keyed** category (exercising Ferric's keyed `VElement` diff + signals, no benchmark-only private path); run
  unmodified inside the suite's harness.
- **§2 What is measured** — speed (the 9 standard CPU operations), memory (ready/run/update/replace/repeated-clear),
  and bundle/startup size (compressed transfer size of the optimized `--release` + `wasm-bindgen` + `wasm-opt`
  build, plus the suite's startup metric).
- **§3 Comparison method** — peers named (Rust/WASM: Leptos, Sycamore, Dioxus, Yew as the primary like-with-like
  bar; JS context: vanillajs baseline, Solid/Svelte/Vue/React); same-conditions runs (same benchmark commit,
  Chromium, machine, keyed-only); the WASM-vs-JS memory/bundle caveat; and explicit no-cherry-picking rules
  (whole-table reporting, the suite's weighted geometric-mean as the only headline figure, conditions published
  with numbers, measured kept separate from expected).
- **§4 `REQ-PERF-001…010`** — testable requirements, verification `benchmark_run` (001–005, 007, 008, 010) or
  `doc_inspection` (006, 009), all `stage: one_oh`, `release_gating: true`.
- **§5 Reproducibility** — the pinned conditions (benchmark commit, Rust toolchain, `wasm-bindgen`/`wasm-opt`,
  Chromium, machine, run session) and the rerun procedure (`REQ-PERF-005`).
- **§6 Lean-footprint link** — bundle size as the objective check on `REQ-FW-013`.
- **§7 Targets** — expectations labelled as targets, not results; stated so a measurement can refute them.
- **§8 Measured-vs-expected discipline** — one in-repo results artifact, targets kept separate, whole-table
  reporting, conditions with numbers, cited peer figures marked; with an empty reporting-shape table.

## Success criteria — met

- [x] Entry, metrics (speed/memory/bundle size), and comparison method specified as testable `REQ-PERF-*` with
      `verification: benchmark_run`/`doc_inspection`, conforming to `../contracts/id_and_traceability_schema.yaml`.
- [x] Reproducibility addressed (§5, `REQ-PERF-005`): pinned versions + documented rerun → comparable numbers.
- [x] Peers named; comparison avoids cherry-picking and separates measured from expected (§3, §7, §8).

## Contract conformance

- **I1 (disjoint registers):** only `REQ-PERF-*` ids minted; all `REQ-FW-*` / `REQ-API-*` / `REQ-DX-*` references
  are read-only.
- **Verification vocabulary:** `benchmark_run` and `doc_inspection`, both in the contract's closed set.
- **Stage/gating:** all `one_oh`, `release_gating: true`; backs `REQ-FW-012` and `REQ-FW-013`.
- **Grounding:** `Nousix-LLC/nswe-demo` @ `276138f`. No measured numbers — every figure is a target/plan.

## Downstream composition

- `SUBTASK_release_bar` references these `REQ-PERF-*` ids from `BAR-FERRIC-*` (identity I2).
- `SUBTASK_release_plan` covers them with the performance work-item (identity I6); the benchmark *implementation*
  (entry code, build/CI, running it to produce measured numbers) is that work-item's, not this design's.
- `SUBTASK_design_pr` places `performance-and-benchmark.md` at `design/ferric/performance-and-benchmark.md`
  (identity I8).

## Notes

- The methodology domain was unbound in this deployment (`agent_domain_unset`); per the hub, each child selects
  its own methodology — applied benchmark/performance-design methodology directly.
- The repository code (`crates/ferric/`, `design/`) is not checked out in this taskflow workspace; the design is
  grounded in the baseline description relayed through the hub and `scope-and-requirements.md`, as the brief
  directs (design the plan, not the implementation).
</content>
