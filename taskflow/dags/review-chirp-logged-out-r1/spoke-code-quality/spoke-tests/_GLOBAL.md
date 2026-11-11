# spoke-tests Decomposition Hub

## Project Context

**Status**: Active
**Parent task**: `spoke-tests` in DAG `review-chirp-logged-out-r1 / spoke-code-quality`
**PR**: #263 on `Nousix-LLC/nswe-demo`
**Head commit**: `decb6196c2c1e6ed421d393a642f0c844cc333ba`

### Objective

Decompose the 3 test-depth concerns (1, 2, 5) assigned to `spoke-tests` into one analysis
task per concern, then synthesize their outputs into `FINDINGS.md` per the parent-level
findings schema (`../contracts/findings_schema.md`).

### Scope

**In scope:**
- Concern 1: Handler unit tests in `crates/chirp-server/src/api/handlers.rs` — 404 path
  coverage and field-level assertion depth
- Concern 2: Integration tests in `crates/chirp-server/tests/api.rs` (`mod public_timeline`)
  — pagination coverage and auth regression guard correctness
- Concern 5: `pub_timeline_url_has_correct_path_and_no_auth` in
  `crates/chirp-frontend/src/api.rs` — whether this test still exercises live-to-the-feature
  code after the PR's refactoring

**Out of scope:**
- Concerns 3, 4, 6, 7, 8, 9, 10 (assigned to other spokes)
- Posting to the PR (the parent DAG's synthesis responsibility)

### Success Criteria

- Each concern (1, 2, 5) has an explicit verdict in one analysis spoke's `analysis.md`
- `FINDINGS.md` written at `spoke-tests/FINDINGS.md` conforming to `../contracts/findings_schema.md`
- No concern silently omitted in the Clean Account section

---

## Input Specification

| Input | Location | Description |
|-------|----------|-------------|
| Parent context | `../_GLOBAL.md` | PR details, pin commit, full concern table |
| Parent findings schema | `../contracts/findings_schema.md` | FINDINGS.md structure |
| handlers.rs | repo at pinned commit | Handler unit tests (concern 1) |
| tests/api.rs | repo at pinned commit | Integration tests (concern 2) |
| frontend/api.rs | repo at pinned commit | Frontend test (concern 5) |
| timeline.rs | repo at pinned commit | Caller of pub_timeline() (concern 5) |
| repository/mod.rs | repo at pinned commit | Repository trait signatures |

Access pattern:
```bash
gh api "repos/Nousix-LLC/nswe-demo/contents/PATH?ref=decb6196c2c1e6ed421d393a642f0c844cc333ba" \
  --jq '.content' | base64 -d
```

---

## Task Structure

```
spoke-tests/_GLOBAL.md (this document)
├── contracts/
│   ├── _MANIFEST.yaml
│   └── analysis_schema.md
├── SUBTASK_handler-unit-tests/_BRIEF.md   (concern 1)
├── SUBTASK_integration-tests/_BRIEF.md    (concern 2)
├── SUBTASK_frontend-test-validity/_BRIEF.md (concern 5)
└── SUBTASK_synthesis/_BRIEF.md            (synthesis gate — depends on all 3 above)
```

## Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_handler-unit-tests` | none | Concern 1: handler unit test depth | `SUBTASK_handler-unit-tests/analysis.md` |
| `SUBTASK_integration-tests` | none | Concern 2: integration test depth | `SUBTASK_integration-tests/analysis.md` |
| `SUBTASK_frontend-test-validity` | none | Concern 5: frontend test validity | `SUBTASK_frontend-test-validity/analysis.md` |
| `SUBTASK_synthesis` | `SUBTASK_handler-unit-tests`, `SUBTASK_integration-tests`, `SUBTASK_frontend-test-validity` | Synthesize into FINDINGS.md | `../FINDINGS.md` |

## Dependency Graph

```
SUBTASK_handler-unit-tests     ──┐
SUBTASK_integration-tests      ──┼── SUBTASK_synthesis
SUBTASK_frontend-test-validity ──┘
```

---

## Contract

**Contract location**: `contracts/` (read-only for all descendants)
**Contract kind**: yaml_schema + markdown_schema

Inherited from parent (`../contracts/findings_schema.md`): structure for the final
`FINDINGS.md`. This decomposition level adds `contracts/analysis_schema.md` for
intermediate per-concern analysis outputs.

### Ownership

| Artifact | Owning subtask |
|----------|----------------|
| `SUBTASK_handler-unit-tests/analysis.md` | `SUBTASK_handler-unit-tests` |
| `SUBTASK_integration-tests/analysis.md` | `SUBTASK_integration-tests` |
| `SUBTASK_frontend-test-validity/analysis.md` | `SUBTASK_frontend-test-validity` |
| `../FINDINGS.md` | `SUBTASK_synthesis` |

### Identities

- [ ] Concern 1 appears in exactly `SUBTASK_handler-unit-tests/analysis.md`
- [ ] Concern 2 appears in exactly `SUBTASK_integration-tests/analysis.md`
- [ ] Concern 5 appears in exactly `SUBTASK_frontend-test-validity/analysis.md`
- [ ] `../FINDINGS.md` has a `## Verdict`, optional `## Findings`, and `## Clean Account`
      per `../contracts/findings_schema.md`

---

## Subtree Methodology Posture

**Dominant task type**: Code review (all 4 tasks)
**Primary bundles**: `code-review`, `testing`
**Cross-cutting binding for all analysis tasks**:
- Findings cite file + line number at pinned commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- Prose bar from `../contracts/findings_schema.md` applies to all analysis outputs
- No host paths, private IPs, or infrastructure details in any output
- Repository: `Nousix-LLC/nswe-demo` only

---

## Output Specification

| Deliverable | Format | Location |
|-------------|--------|----------|
| Final findings | Markdown | `../FINDINGS.md` |
| Per-concern analysis | Markdown | `SUBTASK_*/analysis.md` (3 files) |
