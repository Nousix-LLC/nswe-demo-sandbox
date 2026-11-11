# _BRIEF.md — Synthesis: Aggregate Findings and Post PR Review

## Objective

Read the four spoke `REVIEW.md` outputs, aggregate their findings into a coherent review verdict,
write `SYNTHESIS.md` at the DAG workspace root, and post the review to PR #263.

## Inputs

- Global context: `taskflow/dags/review-chirp-logged-out-r1/_GLOBAL.md`
- Spoke outputs (read all four before writing):
  - `taskflow/dags/review-chirp-logged-out-r1/spoke-access-auth/REVIEW.md`
  - `taskflow/dags/review-chirp-logged-out-r1/spoke-ui-states/REVIEW.md`
  - `taskflow/dags/review-chirp-logged-out-r1/spoke-state-machine/REVIEW.md`
  - `taskflow/dags/review-chirp-logged-out-r1/spoke-code-quality/REVIEW.md`
- PR: `Nousix-LLC/nswe-demo` #263, head `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- Issue: `Nousix-LLC/nswe-demo` #35

## Declared outputs

1. **`SYNTHESIS.md`** at
   `taskflow/dags/review-chirp-logged-out-r1/SYNTHESIS.md` containing:
   - Overall verdict: **APPROVE** or **REQUEST-CHANGES**
   - Per-AC verdict: for each of AC-1 through AC-5, pass or fail with the key evidence
   - Per-concern findings from all spokes: each finding with file+line, severity (blocker /
     non-blocking), and disposition (blocks verdict / advisory)
   - What each concern examined and found clean
   - Non-blocking findings recommended for board issue filing

2. **Review comment posted on PR #263** via `gh pr review` or `gh pr comment`. Because the
   reviewer account is likely the same as the PR author (same-account restriction applies to
   formal approval), post as a comment if formal approval is not available. The posted text must
   include the overall verdict, the per-AC pass/fail summary, any blockers, and notable
   non-blocking findings. Write in the swe-reviewer plain voice: concrete, courteous, no
   AI-writing tells.

## Success criteria

- Both outputs exist and are consistent with each other
- The verdict is derived from the spoke findings, not invented independently
- Any blocker in any spoke propagates to a REQUEST-CHANGES verdict
- The PR comment is actually posted (confirm with `gh pr view 263 --repo Nousix-LLC/nswe-demo
  --comments` or equivalent)
- The prose in `SYNTHESIS.md` and the PR comment passes the avoid-ai-writing bar

## Constraints

- Repository: `Nousix-LLC/nswe-demo` only
- Do not force-push
- Findings in the PR comment point at repository file paths and lines; do not name host paths,
  private IPs, SSH key paths, or internal infrastructure details
- The PR comment must not contain the server address (`100.90.75.93`), SSH key paths, user names,
  or host taskflow paths
