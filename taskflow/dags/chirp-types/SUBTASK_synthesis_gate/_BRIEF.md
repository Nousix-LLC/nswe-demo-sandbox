# Task: Synthesis verification gate — verify, deliver, and fold the chirp-types subtree

## Task Specification

**Slug**: SUBTASK_synthesis_gate
**Task Kind**: synthesis
**Status**: Pending
**Dependencies**: SUBTASK_implement_crate

### Objective

Act as the **verification gate** for the `chirp-types` subtree — NOT a prose summary. Run the
authoritative quality checks over the implemented crate, deliver it as a PR into `main`, and author
the PASS/FAIL fold record. Report honestly: a clean FAIL with evidence beats a green-washed pass.

### Context

This is the terminal hub of the `chirp-types` subtree (see `../_GLOBAL.md` and the frozen conventions
+ assertion set in `../contracts/_MANIFEST.yaml`). The implementation spoke
(`SUBTASK_implement_crate`) has produced the crate in the isolated clone and committed it to
`work/chirp-types`. Your job is to verify that combined output against the contract's identities,
ship it, and record the verdict at the fold location so the parent subtree resolves.

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Objective, scope, success criteria |
| Contract | `../contracts/_MANIFEST.yaml` | The conventions + the **assertion set** you must run (each identity has a runnable `check:`) — READ-ONLY |
| Implementation handoff | `../SUBTASK_implement_crate/IMPLEMENTATION_NOTES.md` | Type surface, local build/test status, branch + clone path |
| The built crate | the clone at the contract's `clone_dir` (branch `work/chirp-types`) | The real output you verify, build, and deliver |

`gh` is authenticated; `git`, `cargo`, `rustup` available.

---

## What to do (gate posture, not a runbook)

Run the gate as a verification gate over the combined output, then deliver and fold:

1. **Run the assertion set.** Execute every identity's `check:` from `contracts/_MANIFEST.yaml`
   against the clone — workspace build, native tests, `fmt --check`, `clippy --all-targets -D
   warnings` — and capture the real results. Also sanity-check the crate against the acceptance
   criteria (domain + DTO types present, serde on all types with explicit field naming, README +
   rustdoc, dependency-light). Decide **PASS/FAIL** from the evidence, not from the handoff's claims.
2. **Deliver** (only once the checks pass): push `work/chirp-types` and open the PR into `main` with
   the contract's `pr_title` and a body summarizing the design + test results and ending with
   `Closes #7`. Capture the PR URL.
3. **On FAIL**: do not green-wash and do not silently fix in place. Record the failing checks with
   evidence and schedule remediation as decomposed fix-task(s) via `engine_amend_plan { add_task }`
   (remediation-as-decomposition), then re-verify. A genuinely blocked gate reports FAIL honestly.
4. **Author the fold record** `SYNTHESIS.md` at the subtree root (the contract's `fold_record_path`
   = `/home/user/nousix-runtime/nswe-demo/taskflow/dags/chirp-types/SYNTHESIS.md`) and fold the
   parent via the kernel's synthesis→`resume_suspended` mechanism.

> Your own atomic-vs-decompose evaluation at dispatch is yours to make per the kernel; if the gate +
> remediation genuinely spans multiple responsibilities, evaluate accordingly.

### Declared output

| Attribute | Value |
|-----------|-------|
| Primary declared output | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/chirp-types/SYNTHESIS.md` (the fold record at the subtree root / observation seam) |

`SYNTHESIS.md` MUST contain, prominently: a **build verdict** (`cargo build --workspace`), a **test
verdict** (`cargo test`), **fmt/clippy** results, a **diff manifest** (files added/changed), the
**PR URL**, and an overall **PASS/FAIL**. Make the PR URL and the PASS/FAIL verdict prominent so the
overseer can gate without re-running the build.

---

## Suggested Methodology Files

Matched Domain-Mapping row (verbatim): **"Synthesizing / verifying a hub-and-spoke decomposition
(contract + wiring + dedup + review gate)" → Primary: Synthesis; Supporting: Code Review, Code
Quality"**. This is a verification-gate task — load the Synthesis bundle. Load via
`engine_load_methodology { name: "<bundle>" }`.

- Bundle `synthesis`:
  - `synthesis/Synthesis_Overview_Methodology.md` — **anchor, load first**: the four-check gate model + the PASS/FAIL decision + the `SYNTHESIS.md` schema.
  - `synthesis/Synthesis_Contract_Verification_Methodology.md` — enumerate the contract's identities and run each one's check (the gate-time inverse of the freeze set).
  - `synthesis/Synthesis_Wiring_Verification_Methodology.md` — confirm the crate is actually wired into the workspace (no detached/dead member).
  - `synthesis/Synthesis_Code_Review_Methodology.md` — review of the combined output (type-surface coherence, serde stability, docs).
  - `synthesis/Synthesis_Remediation_Methodology.md` — on FAIL, schedule fix-tasks via `add_task` rather than reconciling inline.
- Bundle `code-review`:
  - `code-review/CodeReview_Checklist_Methodology.md` — the review pass over the crate.
  - `code-review/CodeReview_PR_Authoring_Methodology.md` — a clear PR body summarizing design + test results.
- Bundle `operations`:
  - `operations/GitWorkflow_PR_Lifecycle_Methodology.md` — branch push + `gh pr create` mechanics into `main`.

*The gate posture (that you run a verification gate, not a summary) is mandatory. Which sibling
check/remediation files you load and how deeply you run each check is your judgment: load
`Synthesis_Overview` first, then the sibling files your reading of the subtree reveals you need.*

## Inherited Constraints

- Verify against the **real** built clone and the contract's assertion set — not the handoff's
  self-reported claims.
- PASS requires: workspace build succeeds, native tests pass, fmt clean, clippy clean. Anything
  short of that is a FAIL recorded honestly.
- **Never** commit to or force-push `main`; deliver via the `work/chirp-types` branch + a PR into
  `main` only. PR body ends with `Closes #7`. No commit-attribution trailers.
- `SYNTHESIS.md` is authored at the subtree root (the fold location), per the contract's
  `fold_record_path`.

## Out-of-Scope Methodologies

- Do NOT load `decomposition/` content for the gate itself (it is decomposer-side); you MAY use
  `Synthesis_Remediation_Methodology.md`'s remediation-as-decomposition if a FAIL requires fix-tasks.
- Do NOT re-author the crate's types — if implementation is wrong, that is a FAIL + remediation
  fix-task, not an inline rewrite here.

## Success Criteria

- [ ] Every identity in `contracts/_MANIFEST.yaml` was run against the real clone and its result recorded with evidence.
- [ ] A PR into `main` exists (title per contract; body ends `Closes #7`) when the checks pass; the PR URL is captured.
- [ ] `SYNTHESIS.md` at the subtree root contains the build/test/fmt/clippy verdicts, a diff manifest, the PR URL, and a prominent overall PASS/FAIL.
- [ ] On FAIL: failing checks recorded with evidence and remediation scheduled (not green-washed, not silently plugged).
- [ ] The parent subtree is folded via the synthesis→`resume_suspended` mechanism.
