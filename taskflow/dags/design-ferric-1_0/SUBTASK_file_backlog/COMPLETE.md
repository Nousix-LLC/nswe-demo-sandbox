# COMPLETE — SUBTASK_file_backlog

**Task:** File the Ferric 1.0 backlog on the board (delivery)
**Status:** Completed

## What was done

Read the release plan (`../SUBTASK_release_plan/release-plan.md`) and design PR record (`../SUBTASK_design_pr/design_pr.md`), scanned the board under epic #1 for existing issues, then filed the full backlog.

**Created:** 8 epic issues (#129–#136) and 28 work-item issues (#137–#164) under epic #1, all with acceptance criteria tracing to `REQ-*`/`BAR-FERRIC-*` ids and `design/ferric/…` doc sections from PR #128.

**#5 and #6 fold:** Added a comment to each closed issue pointing to its extending epic (#131 for the router, #132 for HTTP). Neither issue was re-opened or duplicated.

**De-duplication:** Scanned the board before filing; no existing issues matched any plan work item.

## Declared output

- `filed_backlog.md` — index of all created/edited issues, fold record for #5 and #6, BAR coverage check.

## Success criteria check

- [x] Every epic and work-item from the plan is on the board under #1, in dependency order, acceptance criteria tracing to the design (Identity I6).
- [x] #5 and #6 are extended/superseded (comment pointing to extending epic), not duplicated (Identity I7); the record states exactly what happened to each.
- [x] No duplicate of an existing board item was created.
