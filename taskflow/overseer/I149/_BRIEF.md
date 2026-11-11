# _BRIEF.md — NSWE overseer iteration I149 (persona swe-lead) — EXECUTE LANDING DECISION

**Depends on**: I148
**Task Kind**: act — execute the landing decision the user gave in I148. Load `DELIVERABLES_GIT` + `RETENTION` or `WORK_SESSION` + `BOARD` as needed.
Read `I148/CONTINUE.md` and `I146/project_state.json`.

## Context from I148

- PR#113 (epic-persist) is OPEN, CLEAN, Machine PASS (all 6 CI checks green), Review APPROVE.
- I148 re-presented the landing packet. User's decision is recorded in I148/CONTINUE.md.
- Co-reviewer constraint: GitHub branch-protection requires a formal approval from a co-reviewer before merge.
- Issues closed by PR#113: #65, #66, #67. Issue #64 stays open.
- r1 non-blockers on board: #115–#121.
- design-ferric-1_0-r3 running (forked in I146, not yet complete).
- Main SHA: 276138f.

## Work for this iteration

Read I148/CONTINUE.md to get the user's landing decision, then act on it:

### If `approve`:
1. Surface co-reviewer step: remind user that a formal GitHub approval from another account is needed before merge (branch protection). They may: (a) have another account approve on GitHub, (b) merge directly as maintainer if they have authority to bypass, or (c) reconfigure branch protection.
2. Load `DELIVERABLES_GIT` to execute the landing procedure (PR merge, close issues, update main SHA, update board).
3. After merge: close issues #65, #66, #67. Update board. Update project_state.json.

### If `reject <feedback>` or `request-changes <feedback>`:
1. Load `WORK_SESSION` + `BOARD` to triage the feedback.
2. Fork a remediation DAG (swe-coder) with the feedback, the prior diff, and the acceptance criteria.
3. Update board and project_state.json.

### If unclear:
- Re-present the landing packet and ask again.

## Schedule

- **I150** (depends_on I149): Next board sweep / project continuation.

## Important notes

- No attribution trailers on anything posted to GitHub.
- PR#113 link: https://github.com/Nousix-LLC/nswe-demo/pull/113
