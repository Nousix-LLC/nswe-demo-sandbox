# Task: Ferric 1.0 — performance & honest comparison (concern 8)

## Task Specification
**Slug**: SUBTASK_performance_and_benchmark
**Task Kind**: standard
**Status**: Pending

### Objective
Design a **js-framework-benchmark** entry for Ferric that measures speed, memory, and bundle size, with an
honest comparison methodology against peer frameworks. Bar: a reproducible benchmark entry with stated results.
Design the benchmark plan and the performance bar — what is measured, how it is run reproducibly, and how peers
are compared honestly — not the benchmark implementation.

### Context
Part of the Ferric 1.0 framework design (see `../_GLOBAL.md`); owns `REQ-PERF-*`. Ferric's keyed-VDOM +
fine-grained-reactivity design makes performance a real claim to measure, not assert. Honest comparison means
stating method and conditions, and keeping measured results separate from expectations.

**Dependencies**: `SUBTASK_scope_and_requirements`.

### Distinct concerns to cover (name them; let your own evaluation decide how to split)
- **The benchmark entry**: what a Ferric entry in js-framework-benchmark looks like (the implementation shape
  it must provide), and how it is run reproducibly.
- **What is measured**: the speed, memory, and bundle-size metrics, and how each is captured.
- **Honest comparison**: which peers Ferric is compared against (Leptos, Sycamore, Dioxus, Yew; and JS
  frameworks in the suite), the method, and how results are reported without cherry-picking.

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context + constraints. |
| Contract | `../contracts/` | `REQ-PERF-*` schema; `verification_method: benchmark_run`. |
| 1.0 requirements | `../SUBTASK_scope_and_requirements/scope-and-requirements.md` | The frame to specialize. |
| Ferric baseline | `crates/ferric/` (keyed diff, reactivity) | What the benchmark exercises. |
| Peer precedent | the js-framework-benchmark project and its Rust/WASM entries (Leptos, Sycamore, Dioxus, Yew) | The benchmark's structure + honest comparison; cite by name. |

### Declared output
- `performance-and-benchmark.md` (this task's workspace) — the benchmark plan + the `REQ-PERF-*` register.
  Repo target `design/ferric/performance-and-benchmark.md`.

### Success criteria
- [ ] The benchmark entry, the measured metrics (speed/memory/bundle size), and the comparison methodology are
      specified with testable `REQ-PERF-*` acceptance criteria (verification `benchmark_run`), conforming to the
      contract schema.
- [ ] Reproducibility is addressed (how a stranger reruns it and gets comparable numbers).
- [ ] Peer frameworks named; the comparison method avoids cherry-picking and separates measured from expected.

### Constraints
- Write `REQ-PERF-*` only (identity I1). Design the benchmark, not its code. Load your own benchmark methodology.
- Any numeric claim is a plan/target until measured; do not present an expectation as a measured result.
- Honor the writing-voice rules.
