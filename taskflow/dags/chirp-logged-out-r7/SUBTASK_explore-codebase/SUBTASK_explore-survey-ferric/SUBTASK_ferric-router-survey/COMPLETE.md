# Task Complete: Ferric Router API Survey (PR #203)

**Task**: SUBTASK_ferric-router-survey
**Status**: completed

## Output

- `ferric-router-notes.md` written at this workspace

## Schema Conformance

| Requirement | Status |
|---|---|
| Section: Source Locations | ✅ Lists all four `crates/ferric-router/src/` files with descriptions |
| Section: Public API with Rust type signatures | ✅ Full struct/fn signatures in fenced `rust` code blocks |
| Section: State Model | ✅ Explicit: one reactive `Signal<String>` current-path; no loading/error states |
| Section: Usage Example | ✅ Complete multi-route example with nested routes, navigation, and link |
| At least one Rust type signature in a code block | ✅ Multiple (Router, Params, RoutePattern, link, navigate, …) |
| Source locations reference actual `crates/ferric-router/` paths | ✅ |
| Route declaration covered | ✅ `.route()`, `.nest()` builder methods documented |
| Navigation API covered | ✅ `navigate`, `navigate_replace`, `current_path` documented |
| Not-found handling covered | ✅ `.fallback()` documented with per-level scoping noted |

## Coverage Summary

PR #203 introduced a standalone `crates/ferric-router` crate (not inside `crates/ferric/`). It provides:
- `Router` builder with flat routes, nested routes, and a fallback
- `navigate` (push) / `navigate_replace` (replace/redirect) navigation
- `current_path` reactive read
- `RoutePattern` + `Params` exact/prefix segment matcher
- `link` / `Link` declarative navigation node (span, not anchor, due to `preventDefault` constraint)
- Notable limitation: no `<a href>`, no wildcard segments, no query/hash extraction, no SSR route resolver
