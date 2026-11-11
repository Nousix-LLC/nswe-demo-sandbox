# COMPLETE — active-link (SUBTASK_active_link)

## Summary

Extended `Link::build()` in `crates/ferric-router/src/link.rs` to emit
`aria-current="page"` when `self.to == current_path()`. All six success
criteria met; committed and pushed to `work/ferric-router-r1`.

---

## What was done

### Implementation — `crates/ferric-router/src/link.rs`

**Import change** (additive):
```rust
// Before:
use crate::router::navigate;
// After:
use crate::router::{current_path, navigate};
```

**`Link::build()` change** (additive behavior, frozen signature unchanged):
- Computed `is_active = to == current_path()` before constructing the element.
- Added `aria-current="page"` to the element only when `is_active`.
- Inactive path: element is structurally identical to the frozen surface —
  no `aria-current`, no extra attributes, no class change.

### Tests added (native, in existing `tests` module)

| Test | What it verifies |
|---|---|
| `active_link_emits_aria_current_when_path_matches` | `navigate("/active")` then `Link::new("/active", "Active").build()` → `aria-current="page"` present |
| `inactive_link_has_no_aria_current` | `navigate("/other")` then `Link::new("/active", "Active").build()` → no `aria-current` |
| `aria_current_toggles_on_navigation` | At "/home": no aria-current; after `navigate("/about")`: `aria-current="page"` |

---

## Success criteria verification

| Criterion | Result |
|---|---|
| `cargo test -p ferric-router` — all 33 tests pass | ✅ |
| `cargo build -p ferric-router --target wasm32-unknown-unknown` | ✅ |
| `cargo clippy -p ferric-router -- -D warnings` | ✅ clean |
| `cargo fmt --check -p ferric-router` | ✅ clean |
| Contract identity `active_link_awareness` met | ✅ |
| All frozen link tests pass without modification | ✅ (5 pre-existing frozen tests pass) |

---

## Commit

Branch: `work/ferric-router-r1`
Commit: `cab18b9` — "ferric-router: active-route awareness on Link::build() (REQ-RT-007)"

---

## Outputs

- `crates/ferric-router/src/link.rs` — extended with `aria-current` logic and 3 new tests
