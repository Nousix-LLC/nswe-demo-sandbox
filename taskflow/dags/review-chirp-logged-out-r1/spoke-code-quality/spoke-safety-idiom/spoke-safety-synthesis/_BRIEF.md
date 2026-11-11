# Task: Synthesis — Combine Error Safety + Rust Idiom Findings

## Task Specification

**Slug**: spoke-safety-synthesis
**Task Kind**: synthesis
**Depends on**: spoke-error-safety, spoke-rust-idiom
**Status**: Pending

### Objective

This task is a verification gate. Read the partial findings from both concern spokes, assert that
the contract identities hold, and produce a combined `FINDINGS.md` covering concerns 8 and 10
per the findings schema. If any identity fails, report it rather than silently plugging it.

### Context

This task is the synthesis gate for the `spoke-safety-idiom` decomposition (see `../_GLOBAL.md`).
It depends on `spoke-error-safety` (concern 8 partial findings) and `spoke-rust-idiom` (concern 10
partial findings). It produces `FINDINGS.md` at the parent workspace (`../FINDINGS.md`) and
`SYNTHESIS.md` at the parent workspace (`../SYNTHESIS.md` — the fold record). After writing both
files, it calls `engine_resume_suspended` to fold the parent (`spoke-safety-idiom`) from
SUSPENDED to COMPLETED.

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Hub context | `../_GLOBAL.md` | Subtree constraints, task identities |
| Contract manifest | `../contracts/_MANIFEST.yaml` | Ownership and identities to assert |
| Ancestor schema | `../../../contracts/findings_schema.md` | Combined FINDINGS.md structure |
| Concern 8 partial findings | `../spoke-error-safety/error_safety_findings.md` | AppError / user_message() findings |
| Concern 10 partial findings | `../spoke-rust-idiom/rust_idiom_findings.md` | Rust/WASM idiom findings |

---

## Gate Checks (Four-Check Model)

This task MUST run these checks before accepting the combined output:

1. **Ownership coverage**: every artifact listed in `../contracts/_MANIFEST.yaml` has a
   producing spoke that wrote a value. If any artifact is missing, report and FAIL.

2. **Contract identity assertions**: every identity in `../contracts/_MANIFEST.yaml` must hold:
   - Concerns 8 and 10 each appear in the Clean Account
   - Every finding includes a file path and line number at the pinned commit
   - Verdict is exactly PASS or FINDINGS
   - If Verdict is FINDINGS, at least one finding subsection exists
   - No internal infrastructure details in any finding

3. **Structural verification**: the combined FINDINGS.md conforms to the ancestor findings schema
   (`../../../contracts/findings_schema.md`) — Verdict section, Findings section (when applicable),
   Clean Account section, in order, with no missing sections.

4. **Prose bar**: the combined text passes the plain-voice bar (no moral adjectives, no narrated
   candor, no inflated filler).

If a check fails, report the failure in `SYNTHESIS.md` rather than silently fixing it.

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| Combined findings | `../FINDINGS.md` (parent workspace root) |
| Fold record | `../SYNTHESIS.md` (parent workspace root — required for fold) |

**After writing both files**, call `engine_resume_suspended` with:
- `target_task_id`: the task ID of `spoke-safety-idiom` (the suspended parent)
- `synthesized_task_id`: this task's ID
- `seam_path`: absolute path to `../SYNTHESIS.md`

Declare `outputs: ["../FINDINGS.md"]` in the terminal `engine_report_status`.

---

## Success Criteria

- All four gate checks pass (or failures are reported, not silently plugged)
- `FINDINGS.md` at parent workspace covers both concerns 8 and 10
- `FINDINGS.md` conforms to the ancestor findings schema
- `SYNTHESIS.md` at parent workspace exists as the fold record
- `engine_resume_suspended` called successfully to fold the parent COMPLETED

---

## Suggested Methodology Files

Domain Mapping match: **Synthesizing / verifying a hub-and-spoke decomposition** → Primary: `Synthesis`,
Supporting: `Code Review`, `Code Quality`

Specific files to load (starting points — the executing agent is the final judge):

- `synthesis/Synthesis_Overview_Methodology.md` — the four-check gate model; always load first.
- `synthesis/Synthesis_Contract_Verification_Methodology.md` — verify the contract identities
  hold across the combined spoke outputs.
- `synthesis/Synthesis_Wiring_Verification_Methodology.md` — verify every concern assigned to
  this decomposition appears in the output (no detached / silent gaps).

These are the parent's flagged starting points. Load fewer if a check is clearly inapplicable;
load more if the subtree shape reveals additional check surface.

## Inherited Constraints

- Combined `FINDINGS.md` must pass the plain-voice bar defined in
  `../../../contracts/findings_schema.md`
- No internal infrastructure details in any output
- Do not post to the PR
- Repository: `Nousix-LLC/nswe-demo` only
- Pinned commit: `decb6196c2c1e6ed421d393a642f0c844cc333ba`
