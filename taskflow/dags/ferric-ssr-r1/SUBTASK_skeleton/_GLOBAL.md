# _GLOBAL.md — ferric-ssr-r1-skeleton

Atomic task. See parent hub: `../\_GLOBAL.md`.

This task establishes the structural foundation for the ferric-ssr-r1 subtree: module
declarations in `lib.rs`, build configuration in `Cargo.toml`, and working stubs for the two
new modules (`src/ssr.rs`, `src/hydrate.rs`) that satisfy the contract signatures.

After this task commits, the branch `work/ferric-ssr-r1` is in a valid build state on both
native and wasm32 targets, and the three parallel spokes can begin without touching `lib.rs`
or `Cargo.toml`.

Contracts inherited read-only from `../contracts/`.
