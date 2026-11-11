# Task: Git Branch Setup

## Task Specification

**Slug**: SUBTASK_git_branch
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-coder

### Objective

Create or verify the `work/chirp-logged-out` branch from the specified base commit, push it to
origin if not already there, and record the branch status (HEAD SHA, created vs existed) in
`git_status.md`.

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `taskflow/dags/chirp-logged-out-r4/SUBTASK_explore_and_setup/_GLOBAL.md` | Project constraints |
| Repository | `/home/user/nousix-runtime/nswe-demo` | Git working tree |

### Key Parameters

- Base commit: `cb1ced3ffe6efc678d96a26ae16a63cb948d4237`
- Branch name: `work/chirp-logged-out`

---

## Process Specification

1. Check if `work/chirp-logged-out` exists locally (`git branch --list work/chirp-logged-out`).
2. Check if it exists on origin (`git ls-remote --heads origin work/chirp-logged-out`).
3. If the branch does NOT exist locally:
   - Create from the base commit: `git checkout -b work/chirp-logged-out cb1ced3ffe6efc678d96a26ae16a63cb948d4237`
4. If the branch already exists locally:
   - Check it out: `git checkout work/chirp-logged-out`
   - Verify it is at or ahead of `cb1ced3ffe6efc678d96a26ae16a63cb948d4237`
5. Push to origin if not already there: `git push origin work/chirp-logged-out`
6. Record HEAD SHA: `git rev-parse HEAD`
7. Write `git_status.md`.
8. Write `COMPLETE.md`.

**Constraint**: Do NOT put host paths, internal addresses, or taskflow references in git commits.

---

## Output Specification

### Primary Output

| Attribute | Value |
|-----------|-------|
| Filename | `git_status.md` |
| Location | `taskflow/dags/chirp-logged-out-r4/SUBTASK_explore_and_setup/SUBTASK_git_branch/` |

### Required Sections in `git_status.md`

```markdown
# Git Branch Status

## Branch
- Name: `work/chirp-logged-out`
- HEAD: <SHA>
- Status: created | already existed

## Base Commit Verification
- Base: cb1ced3ffe6efc678d96a26ae16a63cb948d4237
- Branch is at or ahead of base: yes | no (note discrepancy if no)

## Remote
- Pushed to origin: yes | already existed on origin
```

---

## Success Criteria

- [ ] Branch `work/chirp-logged-out` exists locally
- [ ] Branch is pushed to origin
- [ ] `git_status.md` exists with branch name, HEAD SHA, and created/existed status
- [ ] `COMPLETE.md` written

---

## Suggested Methodology Files

**Task-type row:** "Git workflow / branch management" — Primary: `operations`, Supporting: `code-review`

**Specific files:**
- `operations/GitWorkflow_PR_Lifecycle_Methodology.md` — Rationale: branch creation and push follow the PR lifecycle workflow conventions.

**These are SUGGESTIONS.** The child agent is the final judge.

## Inherited Constraints

- Repository is at `/home/user/nousix-runtime/nswe-demo`
- Base commit is `cb1ced3ffe6efc678d96a26ae16a63cb948d4237`
- Do NOT write any implementation code — only git operations
- Do NOT put host paths, internal addresses, or taskflow references in git commits
- Note: the cluster SSH pattern from CLAUDE.md is NOT needed for this task
