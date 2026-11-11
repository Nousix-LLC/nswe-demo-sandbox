# Re-review DAG: review-chirp-logged-out-r2

**Repository**: Nousix-LLC/nswe-demo  
**PR**: #263 (`work/chirp-logged-out`)  
**Branch HEAD under review**: `7f4b684671cab7eb778f5ad7f54dfdc82d57b3c4`  
**Previous HEAD (r1)**: `decb6196c2c1e6ed421d393a642f0c844cc333ba`  
**Issue**: #35 — "Logged-out reading and a useful landing with accurate states"

---

## Objective

Re-review PR #263 after the chirp-logged-out-r27 remediation commit, which claims to fix exactly two blockers from review-r1. Determine whether to APPROVE or REQUEST-CHANGES. Produce a posted GitHub review and a root `SYNTHESIS.md`.

## Scope

**In scope:**
- Verify B1 fix (timeline.rs:218 — was `pub_timeline()`, expected `timeline()`)
- Verify B2 fix (compose.rs:519 — was `link("/compose", "Log in →")`, expected `link("/signin", "Log in →")`)
- Confirm all 5 ACs still hold on HEAD `7f4b684`
- Code quality, test coverage, security, regression check on the remediation diff
- Post full review to GitHub PR #263 and write root `SYNTHESIS.md`

**Out of scope:**
- Re-reviewing the full original PR diff (already reviewed in r1); this re-review covers `decb6196..7f4b684` only
- Re-filing non-blockers already tracked as issues #264–#271

## Prior review context

- **r1 review**: `taskflow/dags/review-chirp-logged-out-r1/SYNTHESIS.md` — REQUEST-CHANGES, 2 blockers, 8 non-blockers
- **r27 remediation**: `taskflow/dags/chirp-logged-out-r27/SYNTHESIS.md` — PASS, CI 6/6 green

## Blockers from r1

**B1** (`crates/chirp-frontend/src/timeline.rs:218`): `pub_timeline(&query)` → expected fix: `timeline(&query)`  
**B2** (`crates/chirp-frontend/src/compose.rs:519`): `link("/compose", "Log in →")` → expected fix: `link("/signin", "Log in →")`

## Acceptance criteria (issue #35)

| ID | Criterion |
|----|-----------|
| AC-1 | Logged-out visitor reads home/public timeline and user profiles without being forced to sign up or sign in. No auth wall on `/` or `/@:handle`. |
| AC-2 | On arrival with no content: clear statement of what Chirp is plus an obvious way to sign up or sign in. Never a blank page or unexplained error. |
| AC-3 | If timeline fails to load: clear, recoverable error message shown; retry path exists. |
| AC-4 | "Create an account" route visible on landing and sign-in screen; following it reaches sign-up. Sign-up page "Log in →" CTA routes to `/signin`. |
| AC-5 | Logged-out landing/timeline renders loading, empty, error, and end-of-list states accurately and distinctly. No two states collapse. |

## Review concerns (enumerated)

1. **Fix correctness** — B1 and B2 each correct, complete, minimal
2. **AC re-verification** — all 5 ACs hold on `7f4b684`
3. **Code quality** — changes are clean, style-consistent
4. **Test coverage** — B1 and B2 fixes are tested
5. **Security** — no new attack surface from either change
6. **Regression** — no extra changes in the diff beyond the two targeted fixes

## Useful commands

```bash
gh pr diff 263 -R Nousix-LLC/nswe-demo           # see the full diff under review
gh pr view 263 -R Nousix-LLC/nswe-demo           # PR metadata
git diff decb6196 7f4b684 -- <file>              # single-file diff (if repo accessible)
```

---

## Task structure

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_verify-fixes` | none | Verify B1 and B2 fix correctness; code quality, tests, security, regression | `SUBTASK_verify-fixes/findings-fixes.md` |
| `SUBTASK_verify-acs` | none | Re-verify all 5 ACs hold on new HEAD | `SUBTASK_verify-acs/findings-acs.md` |
| `SUBTASK_synthesis` | `SUBTASK_verify-fixes`, `SUBTASK_verify-acs` | Synthesize findings, produce APPROVE/REQUEST-CHANGES verdict, post to GitHub, write SYNTHESIS.md | `SYNTHESIS.md` |

```
SUBTASK_verify-fixes ──┐
                       ├── SUBTASK_synthesis
SUBTASK_verify-acs   ──┘
```

---

## Subtree Methodology Posture

**Dominant task type**: Code review (Rust code)  
**Primary bundles**: Code Review (`code-review/`), Rust (`rust/`), Core (`core/`)  
**Supporting bundles**: Testing (`testing/`)

**Cross-cutting bindings across this subtree:**
- Every spoke MUST load `CodeReview_Checklist_Methodology.md` from the Code Review bundle
- Every spoke MUST NOT re-review concerns already cleanly covered in r1; scope is limited to the remediation diff `decb6196..7f4b684`
- The synthesis task MUST follow the Synthesis bundle posture (verification gate, not prose summary)
- Do not name host paths, tailnet addresses (`100.x`), or review DAG internal paths in any GitHub-posted content
- The repo under review is `Nousix-LLC/nswe-demo`

## Subtree-Wide Constraints

- HEAD under review: `7f4b684671cab7eb778f5ad7f54dfdc82d57b3c4` — do not drift to a different commit
- Non-blockers already tracked: issues #264–#271 from review-r1 — do not re-file duplicates
- Existing non-blockers from r1 do not change the verdict; only new blockers or unresolved old blockers matter
- The synthesis task writes the root `SYNTHESIS.md` at `taskflow/dags/review-chirp-logged-out-r2/SYNTHESIS.md` — this is the observation seam path; it must follow the SYNTHESIS.md named-state convention
- headless: true; landing_authority: delegated — if verdict is APPROVE, the overseer lands the PR; this review is the approval gate
