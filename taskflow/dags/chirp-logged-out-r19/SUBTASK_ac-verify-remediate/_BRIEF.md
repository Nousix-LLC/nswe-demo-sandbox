# _BRIEF.md — SUBTASK_ac-verify-remediate

## Task Specification

**Slug**: SUBTASK_ac-verify-remediate  
**Task Kind**: standard  
**Depends on**: none  
**Status**: Pending

### Objective

Verify AC-1 through AC-5 for issue #35 against the live code at the current HEAD of branch
`work/chirp-logged-out` (repo `Nousix-LLC/nswe-demo`). For any AC not met, make the minimum
necessary code changes and push them to the branch. Write `ac-verdicts.yaml` conforming to
the contract schema.

### Context

This is the first spoke of the chirp-logged-out-r19 DAG. See `../_GLOBAL.md` for full context.

r18 found PASS for all 5 ACs at HEAD `decb6196c2c1e6ed421d393a642f0c844cc333ba` with CI
all green (run 42194072348). The current branch HEAD is likely the same commit. Your job is
to confirm this is still correct (the branch may have changed since the brief was authored)
and document the evidence.

**Zero new commits is valid if all ACs are already met.**

---

## Acceptance Criteria to Verify

- **AC-1**: `GET /api/chirps` and `GET /api/users/{username}/chirps` are unauthenticated;
  the frontend renders `/` and `/@:handle` routes without an auth gate.
- **AC-2**: When the timeline is loaded but empty, `landing.rs` shows a welcome heading,
  Chirp description, and CTAs to `/signup` and `/signin` — no blank page.
- **AC-3**: When the timeline fails to load (initial error state), an error banner with
  a "Retry" button is rendered; a failed "load more" shows error + "Try again" button.
- **AC-4**: A "Create an account" link is present in every landing state (header nav) and
  on the sign-in screen, and `/signup` is a registered route.
- **AC-5**: The four required states (loading, empty, error, end-of-list) are implemented
  as distinct UI states driven by a single state model in `landing.rs`.

---

## Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Prior synthesis | `../../../chirp-logged-out-r18/SYNTHESIS.md` | r18 evidence baseline |
| Contract schema | `../contracts/ac_verdict_schema.yaml` | Output schema |
| Hub document | `../_GLOBAL.md` | Project context |
| Live code | `gh api repos/Nousix-LLC/nswe-demo/contents/...` or `gh pr view` | Verification |

## Process

1. Check current branch HEAD SHA via `gh api repos/Nousix-LLC/nswe-demo/branches/work/chirp-logged-out`.
2. For each AC, read the relevant source files from the GitHub API (or use `gh pr view` / `gh api` to fetch file contents) and verify the evidence r18 cited is still present.
3. For any AC NOT met: make the minimum code change, commit, and push to `work/chirp-logged-out`.
4. Check CI status of the final HEAD (via `gh run list` or `gh pr checks`).
5. Write `ac-verdicts.yaml` conforming to `../contracts/ac_verdict_schema.yaml`.

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| Filename | `ac-verdicts.yaml` |
| Location | `SUBTASK_ac-verify-remediate/` (this workspace) |
| Format | YAML conforming to `../contracts/ac_verdict_schema.yaml` |

The file must contain:
- `branch_head`: final branch HEAD SHA
- `ci_status`: CI pass/fail at that HEAD
- `commits_added`: list of any new commit SHAs (may be empty)
- `verdicts.AC-1` through `verdicts.AC-5`: each with `verdict` (MET/NOT-MET) and `evidence`

---

## Success Criteria

- [ ] `ac-verdicts.yaml` exists at this workspace and is valid per the contract schema
- [ ] Every AC has a verdict (MET or NOT-MET) with evidence
- [ ] Any gaps have been fixed and pushed
- [ ] CI is passing at the final HEAD (or failure is documented)

---

## Suggested Methodology Files

Task-type row matched: "Code review" → primary bundle `code-review`; "Fixing bugs" → primary
`core`, supporting `testing`.

Suggested files:
- `code-review/CodeReview_Checklist_Methodology.md` — systematic AC-by-AC verification checklist discipline
- `core/BestPractices_Coding_Standards_Methodology.md` — if any code changes are needed

The above are the parent's flagged methodologies based on the task type. The child agent
SHOULD load these as a starting point but is the final judge of what its work requires.

## Inherited Constraints

- Repo: `Nousix-LLC/nswe-demo` only
- Branch: `work/chirp-logged-out` only; no new branches; no push to `main`
- No force-push
- SSH for kubectl/helm, direct `gh` CLI for GitHub operations
- No new PR — PR #263 is the existing PR
