# Task: Code Quality Synthesis — Assemble code-quality.md

## Task Specification

**Slug**: SUBTASK_quality-synthesis
**Task Kind**: synthesis
**Depends on**: `SUBTASK_app-rs-quality`, `SUBTASK_hydrate-wasm-quality`
**Status**: Pending
**Assigned To**: swe-reviewer

### Objective

Act as the verification gate for SUBTASK_code-quality: read the two spoke finding-note files
(`app-rs-notes.md` and `hydrate-wasm-notes.md`), verify the contract identities hold, then
assemble the final `code-quality.md` with an overall PASS/FAIL verdict. This task MUST run as
a verification gate, not a prose summary.

### Context

This task is the synthesis hub for SUBTASK_code-quality (see `../_GLOBAL.md`). It depends on
SUBTASK_app-rs-quality and SUBTASK_hydrate-wasm-quality, both of which must have reached
COMPLETED before this task dispatches.

The gate checks:
1. **Coverage**: Both note files contain findings for all five required quality dimensions.
2. **Format conformance**: Each finding includes a severity label and evidence citation per
   the `../contracts/_MANIFEST.yaml` format.
3. **Verdict consistency**: The overall verdict stated in `code-quality.md` is consistent with
   the severity labels in the spoke notes (a Blocker finding from either spoke → overall FAIL).
4. **Prose quality**: The assembled output passes the prose bar (no AI-tell patterns).

If any identity fails, this task does NOT silently fix it — it surfaces the gap in the output
with a clear statement of what failed and why, then still produces a `code-quality.md` with an
explicit FAIL verdict and the specific gap identified.

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|---|---|---|
| Subtree hub | `../_GLOBAL.md` | Project constraints and subtree-wide context |
| Ownership contract | `../contracts/_MANIFEST.yaml` | Format and identity requirements to verify |
| app.rs findings | `../SUBTASK_app-rs-quality/app-rs-notes.md` | Spoke output 1 |
| hydrate_wasm.rs findings | `../SUBTASK_hydrate-wasm-quality/hydrate-wasm-notes.md` | Spoke output 2 |

---

## Gate Checks

Before assembling `code-quality.md`, run these checks mechanically:

### Check 1 — Coverage
- [ ] `app-rs-notes.md` contains a finding section for each of: cfg-gate idiom, conditional
      dispatch logic, error handling, docstring accuracy, readability
- [ ] `hydrate-wasm-notes.md` contains a finding section for each of: test structure and
      naming, setup/teardown and DOM cleanup, hardcoded strings vs. imported constants,
      duplication, assertion quality
- Failure: surface the missing dimension(s) explicitly in `code-quality.md`

### Check 2 — Format conformance
- [ ] Each finding includes a Severity label (Blocker | Warning | Pass)
- [ ] Each finding includes an Evidence citation (file:line or "N/A")
- Failure: surface the non-conforming finding(s) explicitly

### Check 3 — Verdict consistency
- [ ] If any finding has Severity = Blocker, the overall verdict is FAIL
- [ ] If no Blocker findings exist and at least one Warning exists, the verdict is PASS with
      warnings noted
- [ ] If all findings are Pass, the verdict is PASS
- Failure: a verdict that contradicts the severity evidence is itself a gate failure

### Check 4 — Prose quality
- [ ] No finding text contains AI-tell patterns (moral adjectives on metrics, narrated
      candor phrases, slot-fill templates, padding filler)
- [ ] Review text is in plain voice — concrete, citable, specific
- Failure: flag the specific sentences that contain tells

---

## Output Specification

**File**: `code-quality.md`
**Location**: `../` (the SUBTASK_code-quality workspace root, i.e.,
`/home/user/nousix-runtime/nswe-demo/taskflow/dags/review-ferric-ssr-r2/SUBTASK_regression-quality-sec/SUBTASK_code-quality/code-quality.md`)

The file MUST follow the output structure specified in the original `_BRIEF.md` for
SUBTASK_code-quality:

```markdown
# Code Quality Review — New Code

## app.rs — cfg-gate Pattern

### cfg-gate idiom
[Severity + Finding]

### Conditional dispatch logic
[Severity + Finding]

### Error handling
[Severity + Finding]

### Docstring accuracy
[Severity + Finding]

### Readability
[Severity + Finding]

## hydrate_wasm.rs — Test File

### Test structure and naming
[Severity + Finding]

### Setup/teardown and DOM cleanup
[Severity + Finding]

### Hardcoded strings vs. imported constants
[Severity + Finding]

### Duplication
[Severity + Finding]

### Assertion quality
[Severity + Finding]

## Fresh Non-Blockers (if any)

[Combined list from both note files, or "None found"]

## Overall Code Quality Verdict: [PASS | FAIL]

[If FAIL: state what must be fixed and why it is a blocker]
[If any gate check failed: state which check failed and what was missing/inconsistent]
```

This task also writes a `SYNTHESIS.md` at the SUBTASK_code-quality workspace root (the fold
record) and calls `engine_resume_suspended` to fold the SUBTASK_code-quality parent task
from SUSPENDED to COMPLETED.

---

## Success Criteria

- [ ] All four gate checks executed explicitly (not implicitly assumed)
- [ ] `code-quality.md` written at `../code-quality.md` with all required sections
- [ ] Overall verdict is PASS or FAIL and consistent with finding severities
- [ ] Any gate check failures are surfaced, not silently plugged
- [ ] Prose in `code-quality.md` passes the AI-tell bar

---

## Suggested Methodology Files

**Task type**: "Synthesizing / verifying a hub-and-spoke decomposition" → Primary: `synthesis`

| File | Rationale |
|---|---|
| `synthesis/Synthesis_Overview_Methodology.md` | Anchor — defines the four-check verification gate model; this task MUST run as a gate, not a summary |
| `synthesis/Synthesis_Contract_Verification_Methodology.md` | Verifying the contract identities from `../contracts/_MANIFEST.yaml` (coverage and format checks) |
| `synthesis/Synthesis_Code_Review_Methodology.md` | Assembling a combined code review output from spoke findings; prose quality gate |
| `code-review/CodeReview_Checklist_Methodology.md` | Supporting reference for evaluating whether the spoke findings cover the right quality dimensions |

The above are the parent's flagged methodologies based on the task type. The child agent SHOULD
load these as a starting point but is the final judge of what its work requires.

## Inherited Constraints

- **Repository**: Nousix-LLC/nswe-demo, branch `work/ferric-ssr-r1`, PR #228
- **Commits under inspection**: `7fb90c7`, `e625c3f`, `75c1eef`
- **Do not re-raise**: Issues #229–#242
- **Do not reference**: Overseer I267 escalation comments
- **Prose bar**: Output must be free of AI-tell patterns
- **Scope**: Code quality only — security is SUBTASK_security; regression is
  SUBTASK_regression-check

## Out-of-Scope Methodologies

- `decomposition/` bundle — this task is the synthesis/reassembly side; it MUST NOT load
  decomposition-side methodology content
- `rust/` bundle — the spoke tasks have already applied Rust-specific methodology; this task
  reads their outputs and verifies the gate, not re-reviews the code from scratch
