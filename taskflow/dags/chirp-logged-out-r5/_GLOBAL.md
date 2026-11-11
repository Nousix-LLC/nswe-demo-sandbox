# _GLOBAL.md — chirp-logged-out-r5 subtree hub

**Task**: chirp-logged-out-r5  
**Observation seam**: `taskflow/dags/chirp-logged-out-r5/SYNTHESIS.md`  
**Repo**: `Nousix-LLC/nswe-demo`, branch `work/chirp-logged-out`

## Discovered state

When this hub was materialized, the branch already contained an implementation of issue #35 from a later
re-fork that ran ahead of this node's first context window. The state at discovery time:

- Branch `work/chirp-logged-out` is 6 commits ahead of `main`:
  - `1d8edab feat(chirp-server): add public_timeline capability seam (skeleton)`
  - `7160514 Implement InMemoryRepository::public_timeline`
  - `ec70b78 Implement PostgresRepository::public_timeline`
  - `d57335d test(chirp-server): add integration tests for public_timeline endpoint`
  - `ac3471c style(chirp-server): rustfmt public_timeline stub signature in api.rs`
  - `908d703 feat(chirp-frontend): logged-out visitor experience (AC-1–AC-5)`
- PR #263 is OPEN: "feat: logged-out public timeline and user profiles (#35)"
- PR body contains "Closes #35" ✓
- All CI checks PASS: fmt, clippy, test, wasm, doc, image ✓

## Subtree shape

This is a two-task linear DAG: discovery → synthesis.

```
chirp-logged-out-r5 (this hub, suspended/NeedsDecompose)
├── SUBTASK_discovery   [Group 0]  reads code, verifies each AC-1–5, outputs review.md
└── SUBTASK_synthesis   [Group 1]  reads review.md, writes SYNTHESIS.md, folds parent
```

## Contracts

See `contracts/_MANIFEST.yaml` for the seam definition between discovery and synthesis.

## Completion condition

The hub completes when SUBTASK_synthesis folds it by writing `taskflow/dags/chirp-logged-out-r5/SYNTHESIS.md`
and calling `engine_resume_suspended` with this hub as the target.
