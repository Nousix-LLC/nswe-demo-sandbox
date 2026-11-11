# _BRIEF.md — clippy-fix

**Goal slug**: `clippy-fix`  
**Kind**: code atomic  
**Repo**: `Nousix-LLC/nswe-demo`  
**Branch**: `work/ferric-router-r1`

---

## Objective

Fix the one clippy error that is blocking PR #192. The GitHub Actions CI pipeline runs:

```
cargo clippy --workspace --all-targets --locked -- -D warnings
```

That command fails with:

```
error: unused import: `VNode`
  --> crates/ferric-router/src/router.rs:436:46
   |
   |                 use ferric::vdom::{VElement, VNode};
   |                                              ^^^^
   = note: `-D unused-imports` implied by `-D warnings`
```

The import is inside a test closure (`nested_route_renders_layout_with_child_view`). Only
`VElement` is used in the closure body; `VNode` is not referenced. Remove it.

---

## Inputs

- Branch `work/ferric-router-r1` on `Nousix-LLC/nswe-demo`, current HEAD.
- `crates/ferric-router/src/router.rs`, line ~436 (inside the test function
  `nested_route_renders_layout_with_child_view`):

  ```rust
  use ferric::vdom::{VElement, VNode};
  ```

---

## Required change

In `crates/ferric-router/src/router.rs`, locate the test function
`nested_route_renders_layout_with_child_view` and change:

```rust
use ferric::vdom::{VElement, VNode};
```

to:

```rust
use ferric::vdom::VElement;
```

No other changes are needed.

---

## Verification

After the edit, run locally to confirm the error is gone:

```
cargo clippy --workspace --all-targets --locked -- -D warnings
```

Also verify tests still pass:

```
cargo test -p ferric-router
```

---

## Commit and push

If both commands are clean, commit and push:

```
git add crates/ferric-router/src/router.rs
git commit -m "fix(ferric-router): remove unused VNode import in test

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
git push origin work/ferric-router-r1
```

---

## Declared output

- One commit on `work/ferric-router-r1` removing the unused `VNode` import.
- `COMPLETE.md` at this workspace confirming the commit SHA and that local clippy + tests are
  clean.

---

## Constraints

- Touch only `crates/ferric-router/src/router.rs`. No other files.
- Do not force-push the branch.
- Do not modify anything under `design/`.
- Do not merge the PR.
- Security: never put the host's server address, SSH key path, user name, or local paths into
  commits, issues, or PR comments.
