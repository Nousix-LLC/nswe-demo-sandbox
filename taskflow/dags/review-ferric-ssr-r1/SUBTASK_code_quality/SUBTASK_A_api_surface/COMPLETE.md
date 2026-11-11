# COMPLETE — Area A: API Surface and Naming

**Task**: SUBTASK_A_api_surface
**Status**: completed
**Verdict**: FINDING (NON-BLOCKER)

## Output produced

- `area_a_api_surface.md` — area finding file conforming to `../contracts/findings_schema.yaml`

## Summary

Two non-blocking naming issues found in the new public surface:

1. `ferric::hydrate` names both a module (`pub mod hydrate;`) and a crate-root re-export (`pub use crate::hydrate::hydrate;`). The module and function live in different Rust namespaces so it compiles, but `use ferric::hydrate;` imports the module rather than the function, contrary to what first-time users will expect. The parallel entry point `render_to_string` avoids this because its module is named `ssr`. Mitigation: rename the module to `hydration` (or `client`), or keep the function only at `ferric::hydrate::hydrate`.

2. `chirp_server::ssr::ssr_handler` repeats `ssr` from the module name. The idiomatic form is `chirp_server::ssr::handler` (C-WORD-ORDER).

The rest of the API surface — function names, closure bounds, constant naming, module placement, exclusion from the frozen `prelude` — is clean.
