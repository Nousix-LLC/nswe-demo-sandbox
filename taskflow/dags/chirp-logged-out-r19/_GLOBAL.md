# _GLOBAL.md — chirp-logged-out-r19

## Project Context

**Status**: Active  
**Branch**: `work/chirp-logged-out`  
**Current HEAD**: `decb6196c2c1e6ed421d393a642f0c844cc333ba`  
**PR**: #263 (OPEN/MERGEABLE/CLEAN)  
**Issue**: #35 — Logged-out reading and a useful landing with accurate states  
**Repo**: `Nousix-LLC/nswe-demo`

### Objective

Verify that acceptance criteria AC-1 through AC-5 for issue #35 are met at the current branch
HEAD, make any minimum necessary fixes, and produce `SYNTHESIS.md` at the DAG root as the
fold/verdict record. This is the r19 round; r18 produced a PASS verdict at HEAD `decb6196`.

### Prior Art

r18 (`taskflow/dags/chirp-logged-out-r18/SYNTHESIS.md`) verified PASS for all 5 ACs at
HEAD `decb6196c2c1e6ed421d393a642f0c844cc333ba` with CI run 42194072348 all green. r19 must
confirm this is still the case at the current HEAD (same) and produce its own SYNTHESIS.md.

### Success Criteria

- [ ] AC-1 through AC-5 each assessed as MET or NOT-MET against current HEAD
- [ ] Any gaps fixed with minimum changes and pushed to `work/chirp-logged-out`
- [ ] `SYNTHESIS.md` produced at `taskflow/dags/chirp-logged-out-r19/SYNTHESIS.md`

---

## Acceptance Criteria

- **AC-1**: Logged-out visitor can read the public timeline and user profiles without forced auth
- **AC-2**: Empty-state shows Chirp description + sign-up/sign-in CTA — never blank or error
- **AC-3**: Timeline load failure shows a clear, recoverable message instead of a broken screen
- **AC-4**: "Create an account" is visible on landing/sign-in and routes to sign-up
- **AC-5**: The four states (loading, empty, error, end-of-list) are implemented as distinct UI states

---

## Constraints

- **Repo scope**: `Nousix-LLC/nswe-demo` only
- **Branch**: `work/chirp-logged-out` only; no new branches; no push to `main`
- **No force-push**
- **No new PR**: PR #263 is the existing PR; do not open another
- **SYNTHESIS.md is mandatory**: Must be produced at root path before exit

---

## Task Structure

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_ac-verify-remediate` | none | Verify AC-1–AC-5 at current HEAD; fix gaps if any; push commits | `SUBTASK_ac-verify-remediate/ac-verdicts.yaml` |
| `SUBTASK_synthesis` | `SUBTASK_ac-verify-remediate` | Read verdicts, write SYNTHESIS.md at root, fold DAG | `SYNTHESIS.md` (at root) |

### Dependency Graph

```
SUBTASK_ac-verify-remediate ──→ SUBTASK_synthesis
```

---

## Contract

**Contract location**: `contracts/`  
**Contract kind**: `yaml_schema`

Structural seam: SUBTASK_ac-verify-remediate produces `ac-verdicts.yaml` conforming to
`contracts/ac_verdict_schema.yaml`; SUBTASK_synthesis reads it to populate SYNTHESIS.md.

---

## Subtree Methodology Posture

**Dominant task type**: Code review / verification; "Fixing bugs" for gap remediation  
**Primary bundles**: `code-review` (for verification), `core` (for any code fixes)  
**Cross-cutting**: All work is on the `Nousix-LLC/nswe-demo` repo, Rust + WASM frontend stack.
