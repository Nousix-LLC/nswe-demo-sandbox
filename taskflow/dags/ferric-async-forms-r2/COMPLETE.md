# COMPLETE — ferric-async-forms-r2

**Status:** completed  
**PR:** https://github.com/Nousix-LLC/nswe-demo/pull/193  
**Branch:** work/ferric-async-forms-r2  
**Closed issues:** #130 (EPIC), #143, #144, #145  

## Summary

Ported the r1 implementation from the wrong repo (`Nousix-LLC/ferric`) into
the correct repo (`Nousix-LLC/nswe-demo`, `crates/ferric`). All 6 CI jobs pass.

### Changes delivered

| File | Change |
|------|--------|
| `crates/ferric/Cargo.toml` | Add `wasm-bindgen-futures = "0.4"`; add 8 web-sys features for the new event types |
| `crates/ferric/src/async_resource.rs` | New: `ResourceState<T>`, `Resource<T>`, `suspense()` — 20 native + 3 WASM tests |
| `crates/ferric/src/form.rs` | New: `FormField<T>`, `Bind<T>` — 18 native tests |
| `crates/ferric/src/dom.rs` | Expand `event_name()` / `stash_key()` to return `String`; add `static_event_kinds()` (47 variants); Custom event tracking via `__ferric_custom_events` JS array |
| `crates/ferric/src/vdom.rs` | Expand `EventKind` from 2 → 47 static + `Custom(String)`; remove `Copy + Ord`; fix `*k` → `k.clone()` and `BTreeSet` → `HashSet` in tests |
| `crates/ferric/src/lib.rs` | Add `pub mod async_resource` and `pub mod form`; re-export new types in `prelude` |
| `Cargo.lock` | Updated |

### CI results (run 41780600207)
- fmt ✅ pass
- clippy ✅ pass
- doc ✅ pass
- test ✅ pass
- wasm ✅ pass
- image ✅ pass

### Lesson applied
PR was opened in the correct repository (`Nousix-LLC/nswe-demo`), not in
`Nousix-LLC/ferric` as the prior attempt did.
