# SUSPENSION.md — ferric-ssr-r1

## Status: NeedsDecompose

This task has decomposed into a five-node subtree and is suspending pending completion of all
child tasks.

## Decomposition Cut

Walking skeleton (Group 0) → three parallel spokes (Group 1) → synthesis gate (Group 2).

| Task ID | Role | Branch | Depends On |
|---|---|---|---|
| ferric-ssr-r1-skeleton | Structural foundation: `lib.rs`, `Cargo.toml`, stubs | `work/ferric-ssr-r1` | — |
| ferric-ssr-r1-server-render | `render_to_string` in `src/ssr.rs` | `work/ferric-ssr-r1-server` | skeleton |
| ferric-ssr-r1-client-hydrate | `hydrate` in `src/hydrate.rs` | `work/ferric-ssr-r1-client` | skeleton |
| ferric-ssr-r1-axum-integration | Axum handler in `crates/chirp-server` | `work/ferric-ssr-r1-axum` | skeleton |
| ferric-ssr-r1-synthesis | Merge, verify, PR, SYNTHESIS.md | `work/ferric-ssr-r1` | all three spokes |

## Contract Seam

`contracts/_MANIFEST.yaml` and `contracts/ferric_ssr_contract.rs` fix the composition seam
between spokes: `TEXT_OPEN_MARKER` = `<!--$t-->`, `TEXT_CLOSE_MARKER` = `<!--/$t-->`;
`render_to_string` and `hydrate` function signatures.

## Resumption Condition

This task resumes (via synthesis fold) when `ferric-ssr-r1-synthesis` completes and writes
`taskflow/dags/ferric-ssr-r1/SYNTHESIS.md`.
