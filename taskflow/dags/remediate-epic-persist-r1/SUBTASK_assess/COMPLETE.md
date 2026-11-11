# COMPLETE — SUBTASK_assess

**Status**: completed
**Task**: Diagnose PR #113 `doc` hazards — produce the correction inventory

## Summary

Surveyed `Nousix-LLC/nswe-demo` branch `work/epic-persist` at pinned head
`09fa453c3c40e39a9b4647e0de6e00dcf50ecb21`. Produced `INVENTORY.md` with 14 schema-conforming
correction records covering all four hazard classes.

## Hazard counts

| Class | Records | Criterion |
|-------|---------|-----------|
| `public_to_private_link` | 1 (CI-01) | CI-01 |
| `ungated_to_gated_link` | 1 (H-02) | #118 |
| `stale_scaffold_doc` | 9 (H-03–H-12) | #118 |
| `internal_vocab` | 3 (H-12–H-14) | #118 |

Note: H-12 is classified `internal_vocab`; H-09 and H-14 are combined (same paragraph, one edit).

## CI-blocking queue

1. **CI-01** — `in_memory.rs` `fn export_user_data` ~L787: `` [`ExportDocument`](super::export::ExportDocument) `` → `` `ExportDocument` ``
2. **H-02** — `export.rs` module doc ~L7: `` [`PostgresRepository`](crate::repository::postgres::PostgresRepository) `` → `` `PostgresRepository` ``

Applying both clears all `-D warnings` errors under `cargo doc --workspace --no-deps --locked` (default features).

## Output

- `SUBTASK_assess/INVENTORY.md` — primary deliverable, ready for `SUBTASK_apply_fixes` consumption
