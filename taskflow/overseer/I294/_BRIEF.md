# _BRIEF.md — NSWE overseer step I294 (persona swe-lead) — ACT: land PR #193

**Depends on**: I293
**Task Kind**: act — load `appfiles/DELIVERABLES_GIT.md`.

## Context from I293

I293 processed the review fold for review-ferric-async-forms-r3:
- review-ferric-async-forms-r3: APPROVE confirmed (self-review restriction — posted as COMMENTED with explicit APPROVE verdict; SYNTHESIS.md authoritative per REVIEW_GATE.md)
- Non-blockers #248–#253 added to project board (Todo status set) in I293
- _CONFIG.yaml updated with project item IDs for #248–#253

Both landing gates are met:
- **Machine gate**: ferric-async-forms-r3 PASS (6 CI checks green, head SHA `838239e`, CI run https://github.com/Nousix-LLC/nswe-demo/actions/runs/42126720006)
- **Review gate**: review-ferric-async-forms-r3 APPROVE (confirmed I292, processed I293)

Landing authority: **delegated** (`auto_land: true`, `headless: true` from _CONFIG.yaml).

STATE at: `taskflow/overseer/I293/project_state.json`
Config seam: `taskflow/overseer/_CONFIG.yaml`

## Work for this step

### 1. Load governing file

Load `appfiles/DELIVERABLES_GIT.md`.

### 2. Confirm PR #193 is mergeable

Check PR #193 state via `gh pr view 193 --repo Nousix-LLC/nswe-demo --json mergeable,mergeStateStatus,headRefOid`:
- Confirm `mergeable: MERGEABLE`
- Confirm `headRefOid` is `838239e` (or the full SHA starting with `838239e`)
- If not mergeable (conflicts), do NOT merge inline — this would require a code DAG.

### 3. Merge PR #193

If mergeable:
```
gh pr merge 193 --repo Nousix-LLC/nswe-demo --merge --subject "Merge pull request #193: Async resources, expanded events, form binding (ferric-async-forms-r3)"
```

Record the merge SHA.

### 4. Confirm issue #130 is closed

After merge, verify `gh issue view 130 --repo Nousix-LLC/nswe-demo --json state` returns `state: "CLOSED"`.
If not closed automatically (no `Closes #130` in PR description), close manually:
```
gh issue close 130 --repo Nousix-LLC/nswe-demo --comment "Closed by PR #193 (ferric-async-forms-r3 — async resources, expanded events, form binding)."
```

### 5. Update issue #130 and PR #193 board status to Done

Set the project board item for issue #130 (project item ID `PVTI_lADOEB9jls4BlZH4zhFl_I0`) to Done (`98236657`):
```
gh api graphql -f query='mutation { updateProjectV2ItemFieldValue(input: { projectId: "PVT_kwDOEB9jls4BlZH4", itemId: "PVTI_lADOEB9jls4BlZH4zhFl_I0", fieldId: "PVTSSF_lADOEB9jls4BlZH4zhkGLsc", value: { singleSelectOptionId: "98236657" } }) { projectV2Item { id } } }'
```

### 6. Update STATE

Write updated STATE at `taskflow/overseer/I294/project_state.json` reflecting:
- ferric_async_forms_goal: status LANDED, merge SHA recorded
- PR193: MERGED
- issue #130: CLOSED, board Done

### 7. Proceed

Schedule I295 (post-land hygiene: groom board, check deployment) as the next step.

## Notes

- Landing authority is **delegated** (`auto_land: true`, `headless: true`).
- Branch: `work/ferric-async-forms-r2`, head SHA `838239e`, epic #130.
- After landing, check whether any sub-issues of #130 (the async-forms epic) need closing as well.
- chirp-logged-out is still running independently; I295 and I296 watch it after landing hygiene.
