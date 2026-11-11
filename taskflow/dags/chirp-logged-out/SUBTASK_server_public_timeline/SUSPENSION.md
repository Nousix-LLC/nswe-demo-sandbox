# SUSPENSION.md — SUBTASK_server_public_timeline

**Status:** Suspended — NeedsDecompose  
**Suspended at:** 2026-11-06

## Decomposition summary

This task was decomposed into four sequential children that together deliver the full `GET /api/public/timeline` feature:

| Child | Scope | Depends on |
|-------|-------|------------|
| `CHILD_skeleton` | Trait method + `todo!()` stubs + handler + route; `cargo build` gate | — |
| `CHILD_in_memory` | Real `InMemoryRepository::public_timeline` impl | `CHILD_skeleton` |
| `CHILD_postgres` | Real `PostgresRepository::public_timeline` impl | `CHILD_in_memory` |
| `CHILD_tests` | Integration tests + CI pass (`fmt`, `clippy`, `test`) + parent `COMPLETE.md` | `CHILD_postgres` |

## Resumption

This task resumes when all four children have reached terminal COMPLETED state. `CHILD_tests` produces `COMPLETE.md` at this workspace on its completion.
