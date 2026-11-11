# Concern Findings — Performance & Benchmark

## concern_name

Performance & Benchmark

## document_validated

`performance-and-benchmark.md` on branch `work/design-ferric-1_0`

## req_ids_found

- REQ-PERF-001
- REQ-PERF-002
- REQ-PERF-003
- REQ-PERF-004
- REQ-PERF-005
- REQ-PERF-006
- REQ-PERF-007
- REQ-PERF-008
- REQ-PERF-009
- REQ-PERF-010

Cross-cutting traceability also references REQ-FW-012 and REQ-FW-013 (owned by scope-and-requirements.md).

## status

valid

## specific_issues

_(empty — status is valid)_

## gaps

_(empty — no gaps in range GAP-070 through GAP-079)_

---

## Validation Notes

The document passes all five validation criteria. Notes on each:

**1. js-framework-benchmark entry required as a 1.0 gate, with stated methodology.**
REQ-PERF-001 carries `stage: one_oh` and `release_gating: true`. §1 defines the entry shape (keyed, implemented through Ferric's public API, standard row-table app); §1.3 requires the entry to run inside the benchmark harness unmodified; §3 documents the full comparison method; §5 documents the pinned conditions. The methodology is comprehensive.

**2. Peer comparison is grounded.**
§3.1 names the primary peers (Leptos, Sycamore, Dioxus, Yew) and the JS context set (vanillajs, Solid, Svelte, Vue, React). §3.2 states the conditions that make a comparison valid: same benchmark commit, same Chromium version, same machine, one run session, keyed category. Where a peer number was not measured in the same session, its source and date must be given. REQ-PERF-007 and REQ-PERF-008 make these requirements release-gated. All comparisons are qualified as plans or expectations — no measured data is asserted.

**3. Bundle-size and dependency-footprint requirements stated with a measurable bar.**
REQ-PERF-004 specifies what to measure (transfer size in compressed and uncompressed form, the suite's startup metric) and the build conditions (optimized release: `--release`, `wasm-bindgen`-processed, `wasm-opt`-optimized). REQ-PERF-010 ties the measured size to the documented dependency set and explicitly names REQ-FW-013 (in scope-and-requirements.md) as the footprint bar this size figure is held to. §7 states a qualitative target ("competitive with the leaner Rust/WASM peers", "stays defensible against named peers") as the planning reference. The cross-document split is intentional and traceable: the measurement methodology lives here; the acceptability threshold lives in REQ-FW-013.

**4. Benchmark methodology is transparent enough to reproduce.**
§5 lists all items that must be pinned and recorded with every published result set: benchmark commit, Rust toolchain version, wasm-bindgen + wasm-opt versions, Chromium version, machine class, run session. REQ-PERF-005 states comprehensive acceptance criteria. The step-by-step rerun procedure is deferred to the implementation work item, which is appropriate for a plan document; the document specifies exactly what the procedure must contain.

**5. Performance claims presented as expectations or results, appropriately hedged.**
The document's hedging is exemplary. The introduction states "No measured result exists yet. Every numeric figure Ferric might cite is a target or a plan until the entry has been run and its output recorded." §7 labels every target explicitly as "(expectation, not measured)." §8 defines the reporting discipline that will govern measured results once produced. The results table in §8 shows dashes for all Ferric entries, with a note explaining they mark unmeasured cells. REQ-PERF-009 makes the measured-vs-expected separation a release gate.
