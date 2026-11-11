# COMPLETE — SUBTASK_dim-strings

**Status**: completed
**Task**: hydrate_wasm.rs — Dimension 3: Hardcoded Strings vs. Imported Constants
**Commit examined**: 75c1eef776953993ddd62dba1436845a0d53a281

## What was checked

- All three `set_inner_html` call sites in `hydrate_wasm.rs` (lines 62, 113, 174) checked against actual `render_to_string` output for the same text content
- Import block (lines 11–15) checked for `ferric::ssr::TEXT_OPEN_MARKER` / `TEXT_CLOSE_MARKER`
- Full file scanned for local constant definitions duplicating production sentinel values
- `ssr.rs` `render_node` path for `VNode::Text` confirmed to wrap output in `TEXT_OPEN_MARKER` / `TEXT_CLOSE_MARKER`

## Verdict

**Blocker.** No test injects the `<!--$t-->` / `<!--/$t-->` sentinel comment nodes that `render_to_string` would produce. The sentinel-handling code paths in `hydrate.rs` are never exercised. See `finding.md` for full evidence and the per-test comparison table.

## Output

- `finding.md` — severity label, evidence table, coverage gap description
