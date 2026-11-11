# Code Quality Review — PR #263 Subtree Hub

## Project Context

**Status**: Active
**Parent task**: `spoke-code-quality` in DAG `review-chirp-logged-out-r1`
**PR**: #263 on `Nousix-LLC/nswe-demo`
**Head commit**: `decb6196c2c1e6ed421d393a642f0c844cc333ba`

### Objective

Decompose the 10 sub-concerns of the code-quality spoke into parallel analysis tasks, then
synthesize their findings into the single `REVIEW.md` declared by the spoke's brief.

### Scope

**In scope:**
- Each of the 10 numbered sub-concerns from the spoke brief, assigned to exactly one analysis child
- Code areas listed in the brief: `api.rs` (types), `handlers.rs` (tests), `in_memory.rs`,
  `postgres.rs`, `mod.rs` (trait), `tests/api.rs`, `crates/chirp-frontend/src/api.rs`,
  `hydrate.rs`, PR description and docstrings
- SQL syntactic and semantic correctness in `postgres.rs`
- Test depth across handler unit tests and integration tests
- Prose quality in code comments and PR description

**Out of scope:**
- Acceptance-criteria behavioral verification (assigned to AC-behavioral spokes in the parent DAG)
- Files not listed in the brief
- Posting findings to the PR (that is the synthesis child's parent DAG's responsibility)

### Success criteria

- All 10 sub-concerns explicitly addressed across the 5 analysis spokes
- `REVIEW.md` at `spoke-code-quality/REVIEW.md` written by synthesis
- No internal host paths, private IPs, or infrastructure details in any finding
- Each finding cites file + line at pinned commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`

---

## Input Specification

| Input | Location | Description |
|-------|----------|-------------|
| PR diff | `gh pr diff 263 -R Nousix-LLC/nswe-demo` | Full diff at HEAD |
| `chirp-types/src/api.rs` | repo | New wire types |
| `chirp-server/src/api/handlers.rs` | repo | Handler unit tests |
| `chirp-server/src/repository/in_memory.rs` | repo | In-memory implementations |
| `chirp-server/src/repository/postgres.rs` | repo | PostgreSQL implementations + SQL |
| `chirp-server/src/repository/mod.rs` | repo | Trait extension |
| `chirp-server/tests/api.rs` | repo | Integration tests |
| `chirp-frontend/src/api.rs` | repo | Frontend API client |
| `ferric/src/hydrate.rs` | repo | Hydration framework |
| PR description | `gh pr view 263 -R Nousix-LLC/nswe-demo` | PR text |

---

## Concern Assignments

| Concern # | Description | Assigned to |
|-----------|-------------|-------------|
| 1 | Handler unit test depth (404 paths, field checks) | `spoke-tests` |
| 2 | Integration test depth (pagination, auth regression guard) | `spoke-tests` |
| 3 | SQL formatting and semantic correctness in `postgres.rs` | `spoke-correctness` |
| 4 | Spec deviation: `before` as milliseconds vs ISO 8601 | `spoke-correctness` |
| 5 | `pub_timeline_url_has_correct_path_and_no_auth` test validity | `spoke-tests` |
| 6 | `sign_up::sign_up_view` dead-code question | `spoke-code-health` |
| 7 | `hydrate.rs` scope: framework refactor bundled with app feature | `spoke-code-health` |
| 8 | Error message safety: `user_message()` on `AppError` | `spoke-safety-idiom` |
| 9 | Prose quality: PR description + docstrings + inline comments | `spoke-prose` |
| 10 | Rust idiom: `spawn_local`, `thread_local!`, `Cell<bool>`, `Closure::forget()` | `spoke-safety-idiom` |

---

## Task Structure

```
_GLOBAL.md (this document)
├── contracts/
│   ├── _MANIFEST.yaml
│   └── findings_schema.md
├── spoke-tests/_BRIEF.md        (concerns 1, 2, 5)
├── spoke-correctness/_BRIEF.md  (concerns 3, 4)
├── spoke-code-health/_BRIEF.md  (concerns 6, 7)
├── spoke-safety-idiom/_BRIEF.md (concerns 8, 10)
├── spoke-prose/_BRIEF.md        (concern 9)
└── spoke-synthesis/_BRIEF.md    (synthesis gate — depends on all spokes)
```

## Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `spoke-tests` | none | Test depth analysis — concerns 1, 2, 5 | `spoke-tests/FINDINGS.md` |
| `spoke-correctness` | none | SQL correctness + spec deviation — concerns 3, 4 | `spoke-correctness/FINDINGS.md` |
| `spoke-code-health` | none | Dead code + scope analysis — concerns 6, 7 | `spoke-code-health/FINDINGS.md` |
| `spoke-safety-idiom` | none | Error safety + Rust idiom — concerns 8, 10 | `spoke-safety-idiom/FINDINGS.md` |
| `spoke-prose` | none | Prose quality — concern 9 | `spoke-prose/FINDINGS.md` |
| `spoke-synthesis` | `spoke-tests`, `spoke-correctness`, `spoke-code-health`, `spoke-safety-idiom`, `spoke-prose` | Synthesis gate: compile findings into REVIEW.md | `../REVIEW.md` |

## Dependency Graph

```
spoke-tests         ──┐
spoke-correctness   ──┤
spoke-code-health   ──┼── spoke-synthesis
spoke-safety-idiom  ──┤
spoke-prose         ──┘
```

---

## Contract

**Contract location**: `contracts/` (read-only for all descendants)
**Contract kind**: yaml_schema + markdown_schema

| Artifact | Kind | Declares |
|----------|------|----------|
| `contracts/_MANIFEST.yaml` | yaml | Ownership table, identities, derived artifacts |
| `contracts/findings_schema.md` | markdown | Required section structure for every FINDINGS.md |

### Ownership

| Artifact | Owning subtask |
|----------|----------------|
| `spoke-tests/FINDINGS.md` | `spoke-tests` |
| `spoke-correctness/FINDINGS.md` | `spoke-correctness` |
| `spoke-code-health/FINDINGS.md` | `spoke-code-health` |
| `spoke-safety-idiom/FINDINGS.md` | `spoke-safety-idiom` |
| `spoke-prose/FINDINGS.md` | `spoke-prose` |
| `../REVIEW.md` | `spoke-synthesis` |
| `../SYNTHESIS.md` | `spoke-synthesis` (fold record) |

### Identities

- [ ] Every concern in the Concern Assignments table is covered in exactly one analysis spoke's FINDINGS.md
- [ ] Each FINDINGS.md declares a `## Verdict` section (PASS or FINDINGS)
- [ ] Each FINDINGS.md contains a `## Clean Account` section covering each assigned sub-concern
- [ ] `../REVIEW.md` integrates findings from all five analysis spokes

---

## Subtree Methodology Posture

**Dominant task type**: Code review (all 5 analysis spokes + synthesis)
**Primary bundles**: `code-review`, `testing` (for spokes 1,2,5), `security` (spoke 8), `rust` (spoke 10)
**Cross-cutting binding**: All analysis spokes hold findings to the principal-reviewer bar: location
(file+line at pinned commit), principle at stake, why it matters, severity, satisfying condition.
Prose in findings and in REVIEW.md must pass the avoid-AI-writing bar: no moral/character adjectives
on technical things, no narrated candor, no unnamed contrast pairs, no slot-fill templates.

---

## Output Specification

| Deliverable | Format | Location |
|-------------|--------|----------|
| Final review | Markdown | `../REVIEW.md` (= `spoke-code-quality/REVIEW.md`) |
| Per-spoke findings | Markdown | `<spoke>/FINDINGS.md` (5 files) |
| Fold record | Markdown | `../SYNTHESIS.md` |
