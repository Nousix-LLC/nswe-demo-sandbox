# B1 Resolution: Conditional ferric::hydrate / mount wiring

## Summary

Finding B1 (REQ-HYD-003) has been remediated. The WASM entry point now calls
`ferric::hydrate(root, app)` when the mount root already contains server-rendered
children, and falls back to `ferric::dom::mount(root, app)` for a fresh
client-side render. The `assemble_document` docstring in `ssr.rs` has been
corrected to accurately describe this conditional path.

---

## Commit SHA

`7fb90c7` on branch `work/ferric-ssr-r1`, pushed to origin
(`Nousix-LLC/nswe-demo`, PR #228).

---

## Exact Lines Changed

### `crates/chirp-frontend/src/app.rs`

| Change | Before | After |
|--------|--------|-------|
| Comment on root acquisition (line ~140) | `// Mount into \`#app\` if the page provides it, otherwise into \`<body>\`.` | `// Acquire the mount root: \`#app\` if the page provides it, otherwise \`<body>\`.` |
| Final call in `start()` (line ~150) | `mount(root, app);` | Conditional block: `if root.has_child_nodes() { ferric::hydrate(root, app); } else { mount(root, app); }` with explanatory comment |

Full new block (lines 149–157):
```rust
// Hydrate when the server has already populated the mount root with SSR markup; fall back
// to a fresh client-side mount when there is no server-rendered content in the root.
if root.has_child_nodes() {
    ferric::hydrate(root, app);
} else {
    mount(root, app);
}
```

### `crates/chirp-server/src/ssr.rs`

| Location | Before | After |
|----------|--------|-------|
| `assemble_document` doc, item 4 (~line 70–71) | `Loads \`wasm_script_path\` as an ES module so the WASM bundle initialises and calls \`ferric::hydrate\` after the document is parsed.` | `Loads \`wasm_script_path\` as an ES module so the WASM bundle initialises and calls \`ferric::hydrate\` when \`#app\` already contains server-rendered children (the normal SSR path), or \`ferric::dom::mount\` when the page has no server markup.` |

---

## Build Verification

Both checks ran on the build server against the committed state:

| Check | Command | Result |
|-------|---------|--------|
| WASM frontend | `cargo check --target wasm32-unknown-unknown -p chirp-frontend` | ✅ exit 0 — `Finished dev profile` |
| Server crate | `cargo check -p chirp-server` | ✅ exit 0 — `Finished dev profile` |

---

## Complications

None. The fix was straightforward:

- `ferric::hydrate` is already implemented (466 lines, `crates/ferric/src/hydrate.rs`) and
  re-exported at `ferric::hydrate` with `#[cfg(target_arch = "wasm32")]`.
- `has_child_nodes()` is available on `web_sys::Element` via the `Node` trait without any
  additional imports.
- No dependency or Cargo.toml changes were required.
