# _BRIEF.md — NSWE overseer step I204 (persona swe-lead) — ACT: land PR #188

**Depends on**: I203
**Task Kind**: act — load `DELIVERABLES_GIT`, `RETENTION`; land PR #188 under delegated authority.

## Context from I203

- review-ferric-epic-authoring-r1 APPROVE. Non-blockers #190 and #191 added to board project (Todo).
- PR #188: OPEN, MERGEABLE. CI all 6 PASS (run 41743675354, tip `e29e2f4`). Machine gate: PASS. Review: APPROVE.
- Config seam: `landing_authority: delegated`, `auto_land: true`, `headless: true`.
- All landing conditions met: machine PASS + review APPROVE + MERGEABLE + config delegated/auto_land.
- **STATE**: `taskflow/overseer/I203/project_state.json` (current_pointer: I203, free_dag_slots: 2).
- **Config seam**: `taskflow/overseer/_CONFIG.yaml`.
- Issues to close: #129, #137, #138, #139, #140, #141, #142.
- Branch: `work/ferric-epic-authoring-r1`, tip `e29e2f4`.

## Work for this step

### 1. Load governing files
Load `appfiles/DELIVERABLES_GIT.md` and `appfiles/RETENTION.md`.

### 2. Verify landing conditions (read from live sources)
- PR mergeable: check `gh pr view 188 --repo Nousix-LLC/nswe-demo --json mergeable`.
- CI status: confirm all checks pass on PR #188.
- Review: verify review-ferric-epic-authoring-r1 SYNTHESIS.md says APPROVE.
- Config seam: `landing_authority: delegated`, `auto_land: true` confirmed at I203.
- If all conditions hold → proceed to land.

### 3. Land PR #188
```
gh pr merge 188 --repo Nousix-LLC/nswe-demo --squash --delete-branch \
  --subject "feat(ferric): Ferric 1.0 Authoring Model — view!, components, context (#129)"
```
Record the merge commit SHA (output of `gh pr view 188 --json mergeCommit` after merge).

### 4. Update board — close issues
Issues #129, #137, #138, #139, #140, #141, #142 should auto-close from the PR (they are in `closes_issues`).
Verify each is closed on GitHub. If any did not auto-close, close them: `gh issue close <N> --repo Nousix-LLC/nswe-demo`.

Move each from "In Progress" to "Done" on the board project using `updateProjectV2ItemFieldValue` with status
option id `98236657` (Done). Use the project item IDs from `_CONFIG.yaml` (issue_129, issue_137–issue_142).

### 5. Update STATE
Write `taskflow/overseer/I204/project_state.json`:
- `current_pointer`: "overseer/I204"
- `checked_at`: now
- Update `PR188.status`: "MERGED", add `merged_at` and `merge_commit`.
- Update `main_sha` to merge commit SHA.
- Append `work_items` entry for ferric-epic-authoring-r1:
  ```json
  {
    "item_slug": "ferric-epic-authoring-r1",
    "issues_closed": [129, 137, 138, 139, 140, 141, 142],
    "pr": 188,
    "landed_commit_shas": ["<merge_commit>"],
    "machine_gate": "PASS",
    "review_verdict": "APPROVE",
    "gate_outcome": "LANDED",
    "landed_at": "<timestamp>",
    "review_outcome": {
      "blockers_resolved": 0,
      "uncovered_concerns": [],
      "followup_issues": [189, 190, 191]
    }
  }
  ```
- `free_dag_slots`: 2.
- Add I204 to `forward_series`.

### 6. Write CONTINUE.md and report terminal
I205 (deployment check) is already scheduled. Write CONTINUE.md and report terminal.
