# chirp-logged-out-r12 — Subtree Hub

## Project Context

**Status**: Active  
**Branch**: `work/chirp-logged-out`  
**HEAD at launch**: `fed1fc8e187d2e706c0aa5d8a6a1f65fb5e92411`  
**CI at launch**: ALL 6/6 PASS (run 42171295267)  
**PR**: #263 OPEN/MERGEABLE — `feat: logged-out reading and accurate landing states (#35)`  
**Repository**: `Nousix-LLC/nswe-demo`

### Objective

Verify and complete the logged-out visitor experience for the Chirp app (issue #35). The branch
is claimed feature-complete at HEAD `fed1fc8e`. Previous runs (r10–r11) built and partially
verified the feature; r12 is the fresh synthesis run from the same HEAD.

### Scope

**In scope:**
- Code inspection of `crates/chirp-server` for AC-5 compliance
- Code inspection of `crates/chirp-frontend` for AC-1–AC-4 compliance
- Identifying and fixing any remaining gaps on `work/chirp-logged-out` (no force-push)
- Producing `SYNTHESIS.md` at `taskflow/dags/chirp-logged-out-r12/SYNTHESIS.md`

**Out of scope:**
- Authenticated features (posting, following, sessions)
- Design changes to acceptance criteria
- Changes to `main` or any other branch
- Opening new PRs (PR #263 already exists)

### Acceptance Criteria (issue #35)

| AC | Description |
|----|-------------|
| AC-1 | Logged-out visitor sees recent chirps at `/` without being redirected |
| AC-2 | Logged-out visitor sees user chirps at `/users/:username` without being redirected |
| AC-3 | Landing page `/` shows sign-up/sign-in CTA for unauthenticated visitors |
| AC-4 | `/sign_in` and `/sign_up` show accurate states (no phantom "logged in", no broken UI) |
| AC-5 | `GET /api/chirps` and `GET /api/users/:username/chirps` serve data without auth required |

---

## Subtree Methodology Posture

**Dominant task type**: Code review / verification with possible gap-filling commits.

**Primary bundles across the subtree**:
- `code-review` — the primary methodology for code inspection tasks
- `core` — coding standards, error handling, commit practices
- `synthesis` — the synthesis gate methodology (for the SUBTASK_synthesis task)

**Cross-cutting methodology bindings** (apply to all descendant tasks):
- `operations/GitWorkflow_PR_Lifecycle_Methodology.md` — any commits must land on
  `work/chirp-logged-out` only; CI must pass on the resulting HEAD
- `code-review/CodeReview_Checklist_Methodology.md` — the standard checklist
  applies to inspection work in both backend and frontend tasks

---

## Subtree-Wide Constraints

1. **Branch**: All commits go to `work/chirp-logged-out` only. No force-push.
2. **PR**: Do not open a new PR. PR #263 already covers this branch.
3. **CI**: Any new commits must result in passing CI (all 6 checks).
4. **Repository**: `Nousix-LLC/nswe-demo` only.
5. **SSH access**: Kubernetes/kubectl commands run on the build server via SSH
   (`ssh -i ~/.ssh/nousix_server_ed25519 ... mattm@100.90.75.93 'bash -lc "..."'`).
   App reachable at `http://100.90.75.93:8081`.
6. **Host facts**: Never put server address, SSH key path, user name, or host paths
   into GitHub issues, PRs, comments, or committed files.

---

## Cut Rationale

**Candidate cuts considered:**

**A (by component — CHOSEN)**: Split backend (chirp-server / AC-5) from frontend
(chirp-frontend / AC-1–4). Verdict: disjoint file ownership (separate crates), minimal
cross-sibling edges (backend_check and frontend_check are independent reads; synthesis
depends on both), sized S/M per child.

**B (by acceptance-criteria group)**: One task per AC. Verdict: creates 5 narrow tasks each
reading shared code paths; excessive fan-out for a verification run.

**C (monolithic inspect + synthesize)**: One big inspect task feeding synthesis. Verdict:
inspect task spans two distinct components, fails ownership-disjointness; would re-trigger
the same scope decompose at dispatch time.

**Choice**: Candidate A — backend_check / frontend_check (independent) / synthesis (dependent
on both).

**Verdict placement**: Synthesis-concentrated (Shape B from
`Decomp_Bugfix_And_Verification_Shapes_Methodology.md`). The subtree is small, CI is passing,
no known defects. Each check task produces a **per-component verdict file** that the synthesis
task reads to produce the root-level `SYNTHESIS.md`. If a check task finds and fixes a gap,
the fix is part of that check task's work (verify-and-fix is one kind of operation at the
component scope: "bring this component to a passing state").

---

## Task Structure

### Overview

```
_GLOBAL.md (this document)
├── contracts/
│   └── _MANIFEST.yaml      (verdict file schema)
├── SUBTASK_backend_check/
│   └── _BRIEF.md           → backend_verdict.md
├── SUBTASK_frontend_check/
│   └── _BRIEF.md           → frontend_verdict.md
└── SUBTASK_synthesis/
    └── _BRIEF.md           → SYNTHESIS.md (root-level, at this workspace)
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_backend_check` | none | Inspect chirp-server for AC-5; fix any gaps; produce backend verdict | `SUBTASK_backend_check/backend_verdict.md` |
| `SUBTASK_frontend_check` | none | Inspect chirp-frontend for AC-1–4; fix any gaps; produce frontend verdict | `SUBTASK_frontend_check/frontend_verdict.md` |
| `SUBTASK_synthesis` | `SUBTASK_backend_check`, `SUBTASK_frontend_check` | Synthesize verdicts; check live deployment; write root SYNTHESIS.md | `SYNTHESIS.md` |

### Dependency Graph

```
SUBTASK_backend_check ──┐
                        ├──▶ SUBTASK_synthesis
SUBTASK_frontend_check ─┘
```

---

## Contract

**Contract location**: `contracts/`  
**Contract kind**: `yaml_schema` — the shared verdict file format both check tasks must produce so the synthesis task can consume them mechanically.

### Structural Declarations

| Artifact | Kind | Declares |
|----------|------|----------|
| `contracts/verdict_schema.yaml` | yaml_schema | Schema for `backend_verdict.md` and `frontend_verdict.md` |

### Ownership

| Artifact | Owning subtask |
|----------|---------------|
| `SUBTASK_backend_check/backend_verdict.md` | `SUBTASK_backend_check` |
| `SUBTASK_frontend_check/frontend_verdict.md` | `SUBTASK_frontend_check` |
| `SYNTHESIS.md` (at this workspace) | `SUBTASK_synthesis` |

### Identities

- [ ] Every AC in the backend verdict has a `verdict: PASS | FAIL` field and an `evidence` list
- [ ] Every AC in the frontend verdict has a `verdict: PASS | FAIL` field and an `evidence` list
- [ ] The synthesis `SYNTHESIS.md` references every AC from AC-1 through AC-5 with an overall verdict

### Inherited Contracts

None (this is the root decomposition).

---

## Output Specifications

| Deliverable | Format | Location | Description |
|-------------|--------|----------|-------------|
| `backend_verdict.md` | Markdown | `SUBTASK_backend_check/backend_verdict.md` | AC-5 verdict with evidence |
| `frontend_verdict.md` | Markdown | `SUBTASK_frontend_check/frontend_verdict.md` | AC-1–4 verdicts with evidence |
| `SYNTHESIS.md` | Markdown | `taskflow/dags/chirp-logged-out-r12/SYNTHESIS.md` | Overall verdict (PASS/FAIL) with per-AC breakdown |
