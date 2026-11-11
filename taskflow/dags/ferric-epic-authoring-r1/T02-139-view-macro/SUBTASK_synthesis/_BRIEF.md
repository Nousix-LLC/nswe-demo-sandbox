# _BRIEF.md — SUBTASK_synthesis: verification gate and issue close

**Task ID:** ferric-authoring-139-view-synthesis  
**Hub:** T02-139-view-macro  
**Branch:** `work/ferric-epic-authoring-r1`  
**Starts from:** SUBTASK_tests' tip commit (fetch before starting)  
**Task kind:** synthesis (verification gate — no new implementation code)

---

## Objective

Verify that the branch tip produced by SUBTASK_impl and SUBTASK_tests satisfies every identity
assertion declared in `../contracts/_MANIFEST.yaml`. Once all six assertions are confirmed, close
GitHub issue #139 with a comment referencing the branch commit, and produce `SYNTHESIS.md` at
this workspace summarizing the verification outcome.

---

## Inputs

| Input | Location |
|-------|----------|
| Hub contract | `../contracts/_MANIFEST.yaml` — 6 identity assertions to verify |
| Parent brief | `../_BRIEF.md` — full acceptance criteria and declared outputs checklist |
| Implementation | `crates/ferric-macros/` on branch tip — read to confirm ownership completeness |
| Test results | Output of `cargo test -p ferric-macros` and `cargo test -p ferric --lib` on the branch tip |
| trybuild fixtures | `crates/ferric-macros/tests/compile_fail/*.stderr` — confirm all 7 are present and non-empty |
| Prelude wiring | `crates/ferric/src/lib.rs` — confirm `pub use ferric_macros::view;` is present |
| GitHub issue | #139 — must be closed with a summary comment |

---

## Verification checklist

For each assertion in `../contracts/_MANIFEST.yaml`, confirm the stated evidence:

| Assertion | Evidence required |
|-----------|-------------------|
| **I-LOWER-01** | `cargo test -p ferric-macros` shows all conformance test functions green; each §2.12 row has at least one test |
| **I-LOWER-02** | The `<For>` conformance test asserts every produced node is a `VNode::Element` with a non-None key equal to the expected value |
| **I-DIAG-01** | Exactly 7 fixture files exist under `tests/compile_fail/`; each has a paired non-empty `.stderr`; `cargo test -p ferric-macros` passes the trybuild runner |
| **I-EXPORT-01** | `crates/ferric/src/lib.rs` contains `pub use ferric_macros::view;` inside `pub mod prelude`; `use ferric::prelude::*; view!{<div/>}` compiles |
| **I-ADDITIVE-01** | `cargo test -p ferric --lib` shows ≥37 tests passing with no new failures; no existing public export removed or renamed |
| **I-MSRV-01** | `cargo +1.82 build -p ferric-macros` succeeds (or CI matrix confirms 1.82; no nightly feature is used) |

---

## Declared outputs

- `SYNTHESIS.md` at this workspace (`SUBTASK_synthesis/SYNTHESIS.md`) containing:
  - Verification table (one row per assertion: PASS / FAIL + evidence)
  - Final branch tip commit SHA
  - Confirmation that issue #139 is closed
  - Any outstanding issues or caveats for downstream tasks (T03)
- GitHub issue #139 closed with a comment citing the branch commit SHA and listing the
  assertions verified.

---

## Success criteria

All six identity assertions show PASS. Issue #139 is closed. The branch is at a clean commit
with no uncommitted changes and all CI-required files present (committed `.stderr` files,
workspace member entry, ferric dependency).

If any assertion shows FAIL, write `SYNTHESIS.md` documenting the gap, do NOT close the issue,
and mark this task FAILED with the specific assertion IDs that failed in the `error` field of
the terminal `report_status` call.

---

## Constraints

- This task writes no implementation or test code. Its only code-level action is reading files
  to verify them and running `cargo test` / `cargo build` on the server.
- Do not modify any files in `crates/ferric-macros/` or `crates/ferric/`.
- The branch must be left in a clean, CI-ready state for T03.
- Never put server address, SSH key path, user name, or host paths into committed files or
  into the GitHub issue comment.
- Use `ssh -i ~/.ssh/nousix_server_ed25519 -o IdentitiesOnly=yes -o BatchMode=yes mattm@100.90.75.93 'bash -lc "…"'`
  for all remote git and cargo operations (see project CLAUDE.md).
