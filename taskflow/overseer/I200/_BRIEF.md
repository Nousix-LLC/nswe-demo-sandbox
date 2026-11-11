# _BRIEF.md — NSWE overseer step I200 (persona swe-lead) — EVALUATE: read fold ferric-epic-authoring-r1; apply machine gate; schedule review launch

**Depends on**: I199
**Task Kind**: evaluate — load `WORK_SESSION`, `REVIEW_GATE`; read fold; apply machine gate; schedule review launch.

## Context from I199

- `ferric-epic-authoring-r1` DAG has **FOLDED** (root SYNTHESIS.md confirmed at I199 check ~2026-11-04T00:20Z).
  - Verdict: **PARTIAL** — all CI jobs pass (run 41743675354, commit `e29e2f4`), all 6 sub-issues closed,
    IA1–IA5 PASS. IA6 PARTIAL: view! trybuild fixtures from T02 were never committed (component diagnostic
    fixtures from T04 are present and passing). The synthesis recommends merge.
  - PR #188: `feat(ferric): Ferric 1.0 Authoring Model — view!, components, context (#129)`, OPEN, MERGEABLE.
    Branch: `work/ferric-epic-authoring-r1`. Closes: #129, #137, #138, #139, #140, #141, #142.
  - CI status (run 41743675354 on `e29e2f4`): fmt ✅, clippy ✅, test ✅, wasm ✅, doc ✅, image ✅ — all 6 PASS.
- **STATE**: `taskflow/overseer/I199/project_state.json` (updated at I199; current_pointer: I199,
  ferric-epic-authoring-r1 moved to dags_folded, free_dag_slots: 2).
- **Config seam**: `taskflow/overseer/_CONFIG.yaml` (landing_authority: delegated, auto_land: true, headless: true).
- Board: 170 items. 29 open issues. 1 open PR (#188, the DAG's output). 2 free DAG slots.

## Work for this step

### 1. Load governing files
Load `appfiles/WORK_SESSION.md` and `appfiles/REVIEW_GATE.md`.

### 2. Read the fold and apply the machine gate
- Read `taskflow/dags/ferric-epic-authoring-r1/SYNTHESIS.md` (the fold — already known PARTIAL above).
- Apply the machine gate per `WORK_SESSION` ("The goal turn" §4): the DAG's CI is fully green (all 6 jobs
  PASS); the PARTIAL verdict is an IA6 test-coverage gap (uncommitted view! trybuild fixtures), not a
  CI failure or functional regression. Machine gate: **PASS**.
- Confirm PR #188 is MERGEABLE and clean before scheduling review.

### 3. File IA6 follow-up issue
The IA6 caveat (missing view! trybuild fixtures for T02's diagnostic behavior) is a test-coverage gap
that should be tracked as a backlog issue. File a GitHub issue on `Nousix-LLC/nswe-demo`:
  - Title: "test(ferric-macros): add trybuild fixtures for view! compile-time diagnostics (§2.9 error cases)"
  - Body: Reference PR #188 / epic #129. Note that T04's component diagnostic fixtures are present and
    passing; this gap is specifically T02's §2.9 view! error cases (e.g. unknown tag, missing closing tag,
    unsupported attribute position) which fire correctly at compile-time but have no committed trybuild suite.
    Link to SYNTHESIS.md IA6 caveat.
  - Milestone: M1 (or whatever milestone is appropriate for Ferric 1.0 implementation work).
  - Add to board Todo and record item ID in _CONFIG.yaml.

### 4. Schedule the review launch
Per `REVIEW_GATE.md`: machine PASS → schedule a review-launch task.
  - Schedule I201 as: **ACT — launch review** (loads `REVIEW_GATE`, `WORK_SESSION`; writes review brief;
    forks `swe-reviewer` for PR #188).
  - The review brief should cover: correctness of the authoring model implementation against the Ferric 1.0
    design and each issue's ACs (#129, #137–#142); code quality and documentation; test coverage
    (including the IA6 gap); API surface consistency; backward compatibility.

### 5. Update STATE and schedule I201
- Update `current_pointer` to I200.
- Update `checked_at`.
- Record the IA6 follow-up issue number in STATE and board.
- Schedule I201 (`depends_on` I200): launch review for PR #188.
- Schedule I202 (`depends_on` I201): board check / watch review fold.
