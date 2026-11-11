# SUBTASK_verify-acs — AC Re-Verification Subtree

## Project Context

**Status**: Active  
**Parent task**: `review-chirp-logged-out-r2 / SUBTASK_verify-acs`  
**PR under review**: #263 (`work/chirp-logged-out`) — Nousix-LLC/nswe-demo  
**HEAD under review**: `7f4b684671cab7eb778f5ad7f54dfdc82d57b3c4`  
**Remediation diff scope**: `decb6196..7f4b684` (two single-line fixes: `timeline.rs:218` and `compose.rs:519`)

### Objective

Re-verify all five acceptance criteria from issue #35 at the new HEAD. In r1 (HEAD `decb6196`), AC-1 and AC-4 FAILED; AC-2, AC-3, and AC-5 PASSED. The remediation commit claims to fix B1 (timeline.rs:218) and B2 (compose.rs:519). Produce `findings-acs.md` conforming to the parent contract schema.

### Scope

**In Scope:**
- Verifying AC-1: public endpoint routing and frontend route guard status at `7f4b684`
- Verifying AC-4: B2 fix (`compose.rs:519` → `/signin`) and surrounding CTA routing at `7f4b684`
- Confirming AC-2, AC-3, AC-5 remain PASS (files unchanged or any changes do not affect the criteria)
- Assembling `findings-acs.md` with explicit PASS/FAIL verdicts for all five ACs

**Out of Scope:**
- Fix correctness from the implementation perspective (B1/B2 root-cause verification) — owned by SUBTASK_verify-fixes
- Re-reviewing code not in the remediation diff
- Re-filing non-blockers already tracked as issues #264–#271

### Success Criteria

- [ ] `findings-acs.md` written with explicit PASS/FAIL for AC-1 through AC-5
- [ ] Evidence cited for each verdict, including "file not in diff" for unchanged files
- [ ] Output conforms to `contracts/_MANIFEST.yaml` schema (parent and this subtree's)

---

## Input Specifications

| Input | Source | Purpose |
|-------|--------|---------|
| PR diff | `gh pr diff 263 -R Nousix-LLC/nswe-demo` | The diff under review |
| r1 SYNTHESIS | `taskflow/dags/review-chirp-logged-out-r1/SYNTHESIS.md` | Per-AC verdicts and evidence from r1 |
| Parent contracts manifest | `../contracts/_MANIFEST.yaml` | Required output schema for `findings-acs.md` |
| Source files (as needed) | `gh pr view 263 -R Nousix-LLC/nswe-demo` or repo files | Specific lines for AC verification |

---

## Task Structure

### Overview

```
SUBTASK_verify-acs/_GLOBAL.md                     (this hub)
├── SUBTASK_ac1-verify/_BRIEF.md                  (spoke: AC-1 verification)
├── SUBTASK_ac4-verify/_BRIEF.md                  (spoke: AC-4 verification)
├── SUBTASK_ac235-confirm/_BRIEF.md               (spoke: AC-2/3/5 unchanged confirmation)
└── SUBTASK_acs-gate/_BRIEF.md                    (synthesis gate: compile into findings-acs.md)
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_ac1-verify` | none | Verify AC-1: B1 fix and public endpoint guard status | `SUBTASK_ac1-verify/verdict-ac1.md` |
| `SUBTASK_ac4-verify` | none | Verify AC-4: B2 fix and CTA routing | `SUBTASK_ac4-verify/verdict-ac4.md` |
| `SUBTASK_ac235-confirm` | none | Confirm AC-2, AC-3, AC-5 unchanged | `SUBTASK_ac235-confirm/verdict-ac235.md` |
| `SUBTASK_acs-gate` | `SUBTASK_ac1-verify`, `SUBTASK_ac4-verify`, `SUBTASK_ac235-confirm` | Synthesis gate: verify all verdicts present and compile findings-acs.md | `../findings-acs.md` |

### Dependency Graph

```
SUBTASK_ac1-verify    ──┐
SUBTASK_ac4-verify    ──┼── SUBTASK_acs-gate
SUBTASK_ac235-confirm ──┘
```

---

## Contract

**Contract location**: `contracts/` (read-only for descendants)  
**Contract kind**: taxonomy

The parent contract at `../contracts/_MANIFEST.yaml` defines that `SUBTASK_verify-acs/findings-acs.md` must carry verdicts for AC-1 through AC-5. This subtree's internal contract (at `contracts/_MANIFEST.yaml`) defines the intermediate spoke outputs that feed into that final file.

### Structural Declarations

| Artifact | Kind | Declares |
|----------|------|---------|
| `contracts/_MANIFEST.yaml` | taxonomy | Per-spoke output schema; synthesis assembly contract |

### Ownership

| Artifact | Owning subtask |
|----------|----------------|
| `SUBTASK_ac1-verify/verdict-ac1.md` | `SUBTASK_ac1-verify` |
| `SUBTASK_ac4-verify/verdict-ac4.md` | `SUBTASK_ac4-verify` |
| `SUBTASK_ac235-confirm/verdict-ac235.md` | `SUBTASK_ac235-confirm` |
| `../findings-acs.md` | `SUBTASK_acs-gate` |

### Identities

- [ ] `verdict-ac1.md` MUST carry an `ac_1_verdict` field with value PASS or FAIL
- [ ] `verdict-ac4.md` MUST carry an `ac_4_verdict` field with value PASS or FAIL
- [ ] `verdict-ac235.md` MUST carry `ac_2_verdict`, `ac_3_verdict`, and `ac_5_verdict` fields
- [ ] `findings-acs.md` MUST carry explicit verdicts for all five ACs (required by parent `../contracts/_MANIFEST.yaml`)
- [ ] If any spoke verdict is FAIL, the synthesis MUST NOT produce an APPROVE-signaling output

---

## Subtree Methodology Posture

**Dominant task type**: Code review (re-verification of acceptance criteria against a small diff)

**Primary bundles**: `code-review` (CodeReview_Process_Methodology, CodeReview_Checklist_Methodology)

**Cross-cutting bindings**: All leaf tasks operate over the same PR diff (`decb6196..7f4b684`). Every task MUST check the diff first to establish what changed before making claims about code at the new HEAD.

**Note**: These are suggestions. Each descendant agent retains final judgment over which methodology files its work actually requires.

---

## Subtree-Wide Constraints

- HEAD under review is `7f4b684671cab7eb778f5ad7f54dfdc82d57b3c4`
- Scope is the remediation diff `decb6196..7f4b684` only
- When a file is not in the diff, verify it is unchanged and explicitly record that finding — do not silently skip
- Non-blockers already tracked as issues #264–#271 — note as "already tracked" if re-encountered; do not re-file
- Do NOT name host paths, tailnet addresses, or review DAG internal paths in any GitHub-posted content
- Repo is `Nousix-LLC/nswe-demo`
