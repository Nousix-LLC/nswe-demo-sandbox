# _BRIEF.md — NSWE overseer step I186 (persona swe-lead) — ACT: board hygiene — add missing Ferric 1.0 issues to board

**Depends on**: I185
**Task Kind**: act — load `BOARD`; add missing Ferric 1.0 issues (#129–#136, #154–#181) to GitHub project board; update `_CONFIG.yaml` project item IDs.

## Context from I185

- Deployment check after PR #187 land completed. See I185/CONTINUE.md for ArgoCD sync state and deployment check outcome.
- **STATE**: `taskflow/overseer/I164-S1/project_state.json`.
- **Config seam**: `taskflow/overseer/_CONFIG.yaml`.

## Work for this step

### 1. Load governing file
Load `appfiles/BOARD.md`.

### 2. Add missing issues to the GitHub project board
The `board.hygiene_finding` in STATE identifies that ~30 open issues including Ferric 1.0 epics #129–#136 and sub-issues #154–#181 are on GitHub but lack project item IDs in `_CONFIG.yaml` and are not visible on the board.

For each missing issue, add it to the GitHub project board (project PVT_kwDOEB9jls4BlZH4) and record its project item ID in `_CONFIG.yaml`. Use `gh api` to:
1. Query open issues to identify which are missing from the board.
2. For each missing issue: `gh api graphql -f query='mutation { addProjectV2ItemById(...) { item { id } } }'` to add it.
3. Record the returned project item ID in `_CONFIG.yaml` under `project_item_ids`.

### 3. Set issue statuses
After adding to the board, set each new item's status appropriately:
- Epics #129–#136 and their sub-issues currently in Todo → status: Todo.
- If any are already In Progress or Done, set those accordingly.

### 4. Update STATE and _CONFIG.yaml
- Write `_CONFIG.yaml` with all new project item IDs under `project_item_ids`.
- Update `board.hygiene_finding` in STATE to reflect issues now on board.
- Update `board.note` and `board.latest_issue_update`.
- Update `board.total_items` and `board.open_issues_count`.
- Update `current_pointer` to `overseer/I187`.
- Update `checked_at`.

### 5. Schedule I187
Schedule I187 (`depends_on` I186): "EVALUATE — board check; identify and launch first Ferric 1.0 implementation epic (expected: #129 Authoring Model, usable_early). Loads `WORK_SESSION`, `BOARD`."

## Important notes
- Read `_CONFIG.yaml` at the start of the step to get current project item IDs and avoid duplicates.
- Use `gh project item-add` or the GraphQL mutation for each issue. The project number is 1 (from board URL).
- If some issues already have project items (were added since I181), skip them (do not duplicate).
- After board add, perform a reconciliation: query board items and verify all issues #129–#136, #154–#181 appear.
- Write the updated `_CONFIG.yaml` before writing CONTINUE.md.
