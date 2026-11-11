# _BRIEF.md — SUBTASK_tests: view! macro conformance tests and trybuild suite

**Task ID:** ferric-authoring-139-view-tests  
**Hub:** T02-139-view-macro  
**Branch:** `work/ferric-epic-authoring-r1`  
**Starts from:** SUBTASK_impl's tip commit (fetch before starting)  
**Owned artifacts:** `crates/ferric-macros/tests/` (all test files and fixtures)

---

## Objective

Write a complete test suite for the `view!` macro on top of the implementation committed by
SUBTASK_impl. The suite has two distinct halves:

1. **Native conformance tests** — for each construct in `design/ferric/authoring-model.md` §2.12,
   assert that `view!{…}` and the equivalent hand-built `VElement`/`vdom::text` builder chain
   produce structurally equal `VNode` values.

2. **`trybuild` diagnostic fixtures** — for each of the 7 error cases in §2.9, a `.rs` fixture
   that should compile-fail, plus a committed `.stderr` file matching the actual compiler output.
   All 7 fixtures must pass as part of `cargo test`.

---

## Inputs

| Input | Location |
|-------|----------|
| Lowering table (oracle) | `design/ferric/authoring-model.md` §2.12 — every row is a test case |
| Diagnostics spec | `design/ferric/authoring-model.md` §2.9 — 7 error cases, each with expected message vocabulary |
| VNode equality | `crates/ferric/src/vdom.rs` — check if `VNode`/`VElement` derive/impl `PartialEq`; if not, the test may need manual structural comparison or a helper |
| Installed macro | `crates/ferric-macros/` as committed by SUBTASK_impl — read all source to understand what lowering was implemented |
| Hub contract | `../contracts/_MANIFEST.yaml` — identity assertions I-LOWER-01, I-LOWER-02, I-DIAG-01 |

---

## Scope

The work spans two distinct concerns:

**1. Native conformance tests (`tests/lowering.rs`)**  
Write a `#[test]` function for each of the 10 acceptance criteria rows in the parent `_BRIEF.md`
and each row of the §2.12 lowering table, asserting structural equality between `view!{…}` output
and the hand-built equivalent. The tests must run via `cargo test -p ferric-macros` without a
browser. If `VNode` does not implement `PartialEq`, write a recursive `vnode_eq` helper or
assert on a serialized/debug form — whatever makes the equality check unambiguous and readable.

For the `<For>` list form, assert that every node in the produced `Vec<VNode>` is a
`VNode::Element` with a non-`None` key equal to the expected key (I-LOWER-02).

**2. `trybuild` diagnostic fixtures (`tests/compile_fail.rs` + `tests/compile_fail/`)**  
Create a trybuild test runner at `tests/compile_fail.rs` and one fixture `.rs` file per error
case. The 7 required fixture names and expected diagnostic category:

| Fixture file | Diagnostic category |
|---|---|
| `unclosed_element.rs` | Error at open tag span, naming the unclosed element |
| `mismatched_close_tag.rs` | Error naming the open tag and the mismatching close tag |
| `multiple_top_level.rs` | Error at second-sibling span, naming the single-root rule |
| `dynamic_not_into_string.rs` | Type error at the `{expr}` span (expr not `Into<String>`) |
| `unknown_event_name.rs` | Error naming the bad event and listing `click, input` |
| `handler_not_closure.rs` | Error at the value span, naming that a closure is required |
| `for_missing_key.rs` | Compile error flagging the absent `key` attribute on `<For>` |

**`.stderr` generation workflow:**  
Run `TRYBUILD=overwrite cargo test -p ferric-macros` on the build server via SSH to have
trybuild write the actual compiler output into each `.stderr` file. Then `git add` those files
and commit them. This is mandatory: trybuild fixtures fail on CI if the `.stderr` files are
absent or wrong.

```bash
ssh -i ~/.ssh/nousix_server_ed25519 -o IdentitiesOnly=yes -o BatchMode=yes mattm@100.90.75.93 \
  'bash -lc "cd ~/nswe-demo && TRYBUILD=overwrite cargo test -p ferric-macros 2>&1"'
```

After running that command, inspect the generated `.stderr` files. If any diagnostic message is
phrased in terms of macro internals rather than author vocabulary (BAR-FERRIC-008), coordinate
with the implementation (this is a constraint violation); otherwise commit as-is.

---

## Declared outputs

- `crates/ferric-macros/tests/lowering.rs` — native conformance tests
- `crates/ferric-macros/tests/compile_fail.rs` — trybuild runner
- `crates/ferric-macros/tests/compile_fail/unclosed_element.rs` + `.stderr`
- `crates/ferric-macros/tests/compile_fail/mismatched_close_tag.rs` + `.stderr`
- `crates/ferric-macros/tests/compile_fail/multiple_top_level.rs` + `.stderr`
- `crates/ferric-macros/tests/compile_fail/dynamic_not_into_string.rs` + `.stderr`
- `crates/ferric-macros/tests/compile_fail/unknown_event_name.rs` + `.stderr`
- `crates/ferric-macros/tests/compile_fail/handler_not_closure.rs` + `.stderr`
- `crates/ferric-macros/tests/compile_fail/for_missing_key.rs` + `.stderr`
- A commit on `work/ferric-epic-authoring-r1` containing exactly the above new/modified files.
  Commit message must reference issue #139 and state that the trybuild suite is complete.

---

## Success criteria

1. `cargo test -p ferric-macros` passes with all conformance tests green.
2. `cargo test -p ferric-macros` passes with all 7 trybuild fixtures green (requires committed
   `.stderr` files).
3. `cargo test -p ferric --lib` (37 pre-existing tests) still passes after this commit.
4. Identity assertions I-LOWER-01, I-LOWER-02, I-DIAG-01 from `../contracts/_MANIFEST.yaml`
   are all satisfied.
5. No `.stderr` file is absent or stale; CI will run trybuild without `TRYBUILD=overwrite`.

---

## Constraints

- Read `design/ferric/authoring-model.md` §2.12 and §2.9 fully before writing any test code.
- Do not modify any file in `crates/ferric-macros/src/` — that is SUBTASK_impl's domain.
- The `.stderr` files must be generated on the build server (same Rust toolchain version as CI)
  via `TRYBUILD=overwrite cargo test`. Do not hand-author `.stderr` content.
- If a diagnostic message in a generated `.stderr` file uses macro-internal language, that is a
  BAR-FERRIC-008 violation; note it in your commit message and flag it for SUBTASK_synthesis.
- Never put server address, SSH key path, user name, or host paths into committed files.
- Use `ssh -i ~/.ssh/nousix_server_ed25519 -o IdentitiesOnly=yes -o BatchMode=yes mattm@100.90.75.93 'bash -lc "…"'`
  for all remote git and cargo operations (see project CLAUDE.md).
- Leave the branch at a clean, CI-ready state for SUBTASK_synthesis.
