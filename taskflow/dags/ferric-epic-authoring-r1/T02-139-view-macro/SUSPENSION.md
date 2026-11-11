# SUSPENSION.md — T02-139-view-macro

**Task ID:** ferric-authoring-139-view  
**Status:** SUSPENDED / NeedsDecompose  
**Suspended at:** 2026-11-03

---

## Reason for suspension

T02 has been decomposed into three child subtasks. This node suspends and waits for the
child subtree to complete before it reaches a terminal state.

---

## Decomposition summary

| Child task ID | Workspace | Depends on |
|---|---|---|
| `ferric-authoring-139-view-impl` | `SUBTASK_impl/` | (T01 complete) |
| `ferric-authoring-139-view-tests` | `SUBTASK_tests/` | `ferric-authoring-139-view-impl` |
| `ferric-authoring-139-view-synthesis` | `SUBTASK_synthesis/` | `ferric-authoring-139-view-tests` |

---

## Authored state

- `_GLOBAL.md` — hub document with task summary table, methodology posture, contract reference,
  branch protocol
- `contracts/_MANIFEST.yaml` — behavioral spec with 6 identity assertions and file ownership
- `SUBTASK_impl/_BRIEF.md` — implementation brief (proc-macro crate scaffold, parser, lowering,
  diagnostics, crate wiring)
- `SUBTASK_tests/_BRIEF.md` — testing brief (native conformance tests + trybuild suite with
  committed .stderr files)
- `SUBTASK_synthesis/_BRIEF.md` — synthesis/verification brief (verify all 6 assertions, close
  #139)

---

## Resumption condition

This node resumes when `ferric-authoring-139-view-synthesis` reaches COMPLETED with its
`SYNTHESIS.md` artifact showing all six identity assertions PASS and issue #139 closed.
