# Task: Create router-only branch and open focused PR

## Task Specification

**Slug**: SUBTASK_router-branch  
**Task Kind**: standard  
**Depends on**: none  
**Status**: Pending  
**Assigned To**: swe-coder

### Objective

Create the `work/ferric-router-r2` branch on the `nswe-demo` repository containing exactly the 3 router commits from `work/ferric-router-r1`, then open a focused GitHub PR from `work/ferric-router-r2` → `main` with the correct title, body, and `Closes` keywords for issues #131, #146, #147.

### Context

This task is part of the ferric-router-r2 remediation DAG (see `../_GLOBAL.md`).

PR #192 (`work/ferric-router-r1`) received REQUEST CHANGES because it bundled ~3,290 lines of undescribed proc-macro code alongside the 3 router commits. The 3 router commits already passed all review checks. This task creates a clean, router-only PR.

**Git repository**: `/home/user/nswe-demo` on server `mattm@100.90.75.93`  
**SSH command pattern** (per `../../../CLAUDE.md`):
```bash
ssh -i ~/.ssh/nousix_server_ed25519 -o IdentitiesOnly=yes -o BatchMode=yes mattm@100.90.75.93 \
  'bash -lc "cd /home/user/nswe-demo && <git command>"'
```

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Project context | `../_GLOBAL.md` | Understand scope and constraints |
| Contract manifest | `../contracts/_MANIFEST.yaml` | Confirm owned output path |
| Review synthesis | `../../review-ferric-router-r1/SYNTHESIS.md` | Confirm the 3 passing commits and issue numbers |

### Key Facts (pre-verified by parent)

**3 router commits to cherry-pick** (oldest to newest):
1. `89687da` — `feat(ferric-router): add navigate_replace (REQ-RT-003)` — closes #131
2. `cab18b9` — `ferric-router: active-route awareness on Link::build() (REQ-RT-007)` — closes #146
3. `3868b2c` — `feat(ferric-router): nested routes, replace navigation, active links (r1 spoke completions)` — closes #147

All 3 commits touch ONLY `crates/ferric-router/` — no `crates/ferric-macros/` or `crates/ferric/` changes.

**Base branch**: `main` (current checkout on the server is `work/ferric-router-r1`)

---

## Process Specification

The task involves:
1. Creating `work/ferric-router-r2` from `main` on the server
2. Cherry-picking the 3 commits in oldest-to-newest order
3. Pushing the branch to `origin`
4. Opening a GitHub PR via `gh pr create`
5. Verifying the branch contains exactly the right commits

Conflict handling: if any cherry-pick conflicts, the router commits are known to be purely in `crates/ferric-router/` while the macros commits are in `crates/ferric-macros/` and `crates/ferric/`. Conflicts would be unexpected; if they occur, assess before proceeding.

---

## Output Specification

### Primary Output

| Attribute | Value |
|-----------|-------|
| Filename | `router-pr.md` |
| Location | `outputs/` |

### Output Structure

```markdown
# Router-Only PR — ferric-router-r2

## Branch
work/ferric-router-r2

## PR
<URL of opened PR>

## Commits on branch (vs main)
<git log --oneline output>

## Issues closed
- #131 (navigate_replace)
- #146 (active-route awareness)
- #147 (nested routes)

## CI Status
<pending / link to CI run if available>

## Notes
<any cherry-pick issues, conflicts, or observations>
```

---

## Success Criteria

- [ ] `work/ferric-router-r2` branch exists on `origin` with exactly 3 commits (89687da, cab18b9, 3868b2c) versus `main`
- [ ] No `crates/ferric-macros/` or non-ferric-router `crates/ferric/` files in the branch diff
- [ ] A PR is open from `work/ferric-router-r2` → `main`
- [ ] PR title references ferric-router and the router features
- [ ] PR body closes #131, #146, #147 explicitly
- [ ] `outputs/router-pr.md` exists with PR URL

---

## Suggested Methodology Files

**Task-type row matched**: "PR creation and management via gh CLI" → Primary: `operations`, Supporting: `code-review`

**Specific files to load**:
- `operations/GitWorkflow_PR_Lifecycle_Methodology.md` — PR authoring discipline: title, body, closing keywords, review-ready criteria. Load this first.
- `operations/CodeManagement_Branching_Strategy_Methodology.md` — Branch naming conventions and clean-branch principles.

*Rationale*: The core work here is git branch creation + cherry-pick + gh PR creation. The PR lifecycle methodology covers the PR authoring discipline (title, body, closing keywords). Branching strategy covers creating a clean, purpose-scoped branch.

**These are the parent's suggestions; the child agent loads what its own work requires — load fewer if inapplicable, load more if the work reveals additional needs.**

---

## Inherited Constraints

- Use SSH for all server operations per `CLAUDE.md` (never run kubectl/git locally)
- Server address `mattm@100.90.75.93` and SSH key path MUST NOT appear in committed files, PRs, or GitHub issues
- Never commit `.env` files or credentials
- Attribution line for commits: `Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>`
- Attribution for PRs: end body with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`
- The repo is GitOps-managed via ArgoCD; stay within the `nswe-demo` repo permissions

---

## Out-of-Scope Methodologies

- `rust/` bundle files — no Rust coding work in this task; purely git branch + PR operations
- `synthesis/` bundle — this is a standard (not synthesis) task
