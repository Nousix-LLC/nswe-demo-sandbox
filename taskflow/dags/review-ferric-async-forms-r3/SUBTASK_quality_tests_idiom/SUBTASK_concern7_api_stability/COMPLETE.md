# COMPLETE — SUBTASK_concern7_api_stability

**Task**: API and Contract Stability Review — PR #193 Ferric Async (Concern 7)
**Status**: completed
**Output**: `findings_concern7.md`

## Summary

All four sub-questions in the review scope were examined against the PR diff and source files.

- **EventHandler backward compat**: Clean. `VElement::on()` signature unchanged; `NoArg` wrapping is transparent to all existing callers. The idiomatic prelude surface never exposed `EventHandler` as a nameable type, so the type alias → enum change does not break prelude callers.
- **on_input_event_handler() visibility and docs**: Clean. Correctly gated to `#[cfg(wasm32)]`, well-documented with numbered behavior and failure modes, covered by a WASM integration test.
- **create_resource naming**: Clean. Follows the library's `create_*` convention alongside `create_signal`, `create_effect`, `create_memo`.
- **Two non-blockers identified**: (C7-3) `EventHandler` missing from `prelude` alongside `Bind`; (C7-6) `ResourceState<T>` and `EventHandler` missing `#[non_exhaustive]`. Neither is a re-raise of #196–#201.
