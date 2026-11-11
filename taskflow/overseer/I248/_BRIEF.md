# _BRIEF.md — NSWE overseer step I248 (persona swe-lead) — EVALUATE: file #133 sub-issues + assess product work readiness

**Depends on**: I247
**Task Kind**: evaluate — load `appfiles/WORK_SESSION.md`, `appfiles/BOARD.md`, `appfiles/PRODUCT_DESIGN.md`.

## Context from I247 (EVALUATE: check escalation + pick next epic)

- **CI**: all 6 jobs PASS on merge commit `945fade38abd6b053268501f3801734756f02502` (PR #210, CHANGELOG-only)
- **Deployment**: chirp-server pod running `sha256:f845ca8c` (d8230fea build) — healthy, no change needed
- **Escalation `escalation_ferric_async_forms_budget_exhausted`**: STILL ACTIVE — no user response on PR #193. Checked I247 at current time. Last comment remains the escalation itself. Clearing condition NOT met.
- **#133 (SSR/Hydration) dependency check**:
  - Design: EXISTS at `design/ferric/ssr-hydration.md` in repo (merged via PR #128) ✓
  - Sub-issues: NOT FILED (GitHub shows sub-issues: 0) ✗
  - **Blocked on #130**: issue #133 explicitly "Depends on: #130 (Async, Forms, and Events)" which is escalated → #133 NOT ready to dispatch
- **Ferric 1.0 epic chain**: ALL blocked on #130 escalation (#134 depends on #130+#133; #135 depends on #130+#133; #136 depends on #135+#134)
- **Product epics #34–#43**: #35 has "blocked" label; full readiness assessment not complete — need to assess which product work (if any) can proceed without #130 completion
- **STATE**: `taskflow/overseer/I247/project_state.json`
- **Config seam**: `taskflow/overseer/_CONFIG.yaml`

## Work for this step

### 1. Load governing files

Load `appfiles/WORK_SESSION.md`, `appfiles/BOARD.md`, `appfiles/PRODUCT_DESIGN.md`. Read `_CONFIG.yaml`.

### 2. File sub-issues for #133 (board hygiene)

The design exists and the work items are described in #133's epic body. File the 4 work items as sub-issues linked to parent #133:
- Server-side HTML rendering and per-request scope isolation (BAR-003)
- Client hydration without re-render — must-have (BAR-004)
- State carry and async resource resume across the SSR seam (BAR-005)
- Hydration mismatch detection and Axum integration (BAR-006)

Each sub-issue needs:
- Restated goal and acceptance criteria (from `design/ferric/ssr-hydration.md` and `design/ferric/scope-and-requirements.md`)
- BAR-FERRIC reference(s)
- Dependency links (parent: #133; blocked-by: #130 for all)
- Labels: `framework`, `type:feature`, `blocked`
- Add each to the project board (Todo status)

Also update `_CONFIG.yaml` with the new project_item_ids for the new issues.

### 3. Read the SSR/Hydration design spec

Read `design/ferric/ssr-hydration.md` to understand:
- What specific #130 features (async resources, event bindings, forms) the SSR implementation requires
- Whether any SSR work can proceed before #130 completes (e.g., the server-side rendering engine itself, the HTML serializer, the hydration protocol) independently of async resource state carry
- If there is a decomposable subset of #133 that does NOT depend on #130

If a meaningful subset of #133 is independent of #130 (e.g., the server-rendering path without async resource state hydration across the seam):
- Note it; schedule I249 as ACT to fork that partial #133 goal (scope-limited)

If #133 is fully coupled to #130:
- Note it; move to step 4

### 4. Assess product epics #34–#43 for ready work

Check each of the product epics (chirp app layer: #34–#43) and their sub-issues:
```bash
gh issue list --repo Nousix-LLC/nswe-demo --label app --state open --limit 50
```

For each open product issue, assess:
- Does it require async forms/event bindings (from #130)?
- Does it require SSR/Hydration (from #133)?
- Or does it only need: authoring model (#129 Done), router (#131 Done), HTTP client (#132 Done)?

A read-only chirp feature (displaying a timeline, viewing a profile) may be fully implementable with the current ferric. A write feature (compose, like, follow) may need event handling improvements from #130.

Identify: is there a coherent, valuable subset of product work (#34-#43) that is ready right now (no dependency on #130 or #133)?

Specifically check whether #35 (Logged-out reading and a useful landing) can proceed. Its "blocked" label may refer to a specific dependency — confirm what it's blocked on.

### 5. Decide: what code work is ready, and schedule I249

Based on steps 3 and 4:

**Option A**: A meaningful subset of #133 SSR work does not depend on #130 → schedule I249 as ACT to fork a scope-limited ferric-ssr-r1 code DAG for that subset.

**Option B**: No #133 work is independent of #130, but product work is ready (some #34-#43 issues viable without #130/133) → schedule I249 as ACT to fork a code DAG for the top ready product goal.

**Option C**: Neither ferric nor product work can proceed without #130 → schedule I249 as an EVALUATE (board check + pacing wake) to watch for escalation clearing, with a 30-minute bounded wake.

Write I249's `_BRIEF.md` accordingly.

### 6. Update STATE

Write `taskflow/overseer/I248/project_state.json` with:
- Escalation status (still ACTIVE)
- New #133 sub-issues filed (issue numbers, project item IDs)
- Readiness assessment result
- Forward plan

### 7. Write CONTINUE.md

Write `taskflow/overseer/I248/CONTINUE.md` after completing the step (this is I248's terminal record, authored after the work).

## Notes

- Config: `landing_authority: delegated`, `auto_land: true`, `headless: true`
- main_sha: `945fade38abd6b053268501f3801734756f02502`
- ferric-async-forms escalation: ACTIVE, clearing condition NOT met
- Design docs for ferric in repo at `design/ferric/` (all merged via PR #128)
- Product design for chirp at `design/domain-application-design.md` and `design/experience-design.md`
- When filing issues for GitHub: use `owner/repo` paths, no host paths, no internal addresses (per BOARD.md "Writing for GitHub")
