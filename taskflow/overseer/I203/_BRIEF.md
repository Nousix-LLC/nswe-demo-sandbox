# _BRIEF.md — NSWE overseer step I203 (persona swe-lead) — ACT: process review (review-ferric-epic-authoring-r1) for PR #188

**Depends on**: I202
**Task Kind**: act — load `REVIEW_GATE`, `BOARD`; process the review-ferric-epic-authoring-r1 fold.

## Context from I202 (reconstruction wake)

- Review DAG `review-ferric-epic-authoring-r1` **FOLDED**: **APPROVE**.
  - 6 concerns checked; all PASS. 0 blockers.
  - IA6 gap (view! §2.9 trybuild fixtures) assessed as not a blocker; `usable_early` bar does not require
    snapshot-tested error messages.
  - Non-blocking issues filed by review DAG:
    - **#190**: "test(ferric-macros): add conformance test for conditional rendering and extract shared vnode_eq helper"
    - **#191**: "refactor(ferric-macros): build_panic_builder struct refactor, is_named_slot_type limitation, Computed/Memo naming alignment"
  - Review comment posted on PR #188 (1 comment confirmed APPROVE).
- PR #188: OPEN, MERGEABLE. CI all 6 PASS (run 41743675354, tip `e29e2f4`). Machine gate: PASS.
- Config seam: `landing_authority: delegated`, `auto_land: true`, `headless: true`.
- **STATE**: `taskflow/overseer/I202/project_state.json` (current_pointer: I202, dags_in_flight: empty,
  free_dag_slots: 2, review-ferric-epic-authoring-r1 in dags_folded with verdict APPROVE).
- **Config seam**: `taskflow/overseer/_CONFIG.yaml`.

## Work for this step

### 1. Load governing files
Load `appfiles/REVIEW_GATE.md` and `appfiles/BOARD.md`.

### 2. Add non-blocking issues to board project
Issues #190 and #191 were filed on GitHub by the review DAG but are not yet project board items.

For each issue, add it to the board project (PVT_kwDOEB9jls4BlZH4) and set status = "Todo":
```
gh api graphql -f query='mutation { addProjectV2ItemById(input: {projectId: "PVT_kwDOEB9jls4BlZH4", contentId: "<issue_node_id>"}) { item { id } } }'
```
Get each issue's node_id via `gh issue view <N> --repo Nousix-LLC/nswe-demo --json id`.

Then set status to "Todo":
```
gh api graphql -f query='mutation { updateProjectV2ItemFieldValue(input: {projectId: "PVT_kwDOEB9jls4BlZH4", itemId: "<item_id>", fieldId: "PVTSSF_lADOEB9jls4BlZH4zhkGLsc", value: {singleSelectOptionId: "f75ad846"}}) { projectV2Item { id } } }'
```

Record the project item IDs for #190 and #191 in `taskflow/overseer/_CONFIG.yaml` as `issue_190` and `issue_191`.

### 3. Update STATE
Write `taskflow/overseer/I203/project_state.json`:
- `current_pointer`: "overseer/I203"
- `checked_at`: now
- `board.total_items`: 173 (171 + #190 + #191)
- `board.note`: updated
- `free_dag_slots`: 2
- Add I203 to `forward_series`.

### 4. Write CONTINUE.md and report terminal
I204 (land PR #188) is already scheduled in the plan (`depends_on I203`).
Write `taskflow/overseer/I203/CONTINUE.md` and report terminal status=completed, thread_evaluation=Continue.
