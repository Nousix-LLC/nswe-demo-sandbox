# SQL Correctness + Spec Deviation — PR #263 Subtree Hub

## Project Context

**Status**: Active
**Parent task**: `spoke-correctness` in `spoke-code-quality` decomposition
**PR**: #263 on `Nousix-LLC/nswe-demo`
**Head commit**: `decb6196c2c1e6ed421d393a642f0c844cc333ba`

### Objective

Decompose the two assigned concerns (3 and 4) into independent analysis tasks,
then merge their findings into the single `FINDINGS.md` declared by the
spoke-correctness brief.

### Scope

**In scope:**
- Concern 3: SQL formatting and semantic correctness in
  `crates/chirp-server/src/repository/postgres.rs`
- Concern 4: Spec deviation — `before` as milliseconds in
  `crates/chirp-types/src/api.rs` and `crates/chirp-frontend/src/api.rs`

**Out of scope:**
- All other concerns (assigned to sibling spokes in the parent DAG)
- Files not listed above
- Posting findings to the PR

### Success criteria

- Both concerns 3 and 4 are covered in the final `FINDINGS.md`
- Each finding cites file + line at pinned commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- No internal host paths, private IPs, or infrastructure details in any finding
- Final `FINDINGS.md` conforms to `../contracts/findings_schema.md`

---

## Input Specification

| Input | Location | Description |
|-------|----------|-------------|
| `postgres.rs` | `crates/chirp-server/src/repository/postgres.rs` at HEAD | SQL queries for concern 3 |
| `mod.rs` | `crates/chirp-server/src/repository/mod.rs` at HEAD | Trait docstrings (specification) |
| `in_memory.rs` | `crates/chirp-server/src/repository/in_memory.rs` at HEAD | Reference implementation |
| `api.rs` (types) | `crates/chirp-types/src/api.rs` at HEAD | `PublicTimelineQuery.before` type |
| `api.rs` (frontend) | `crates/chirp-frontend/src/api.rs` at HEAD | Frontend usage of `before` |

Access files via:
```bash
gh api "repos/Nousix-LLC/nswe-demo/contents/PATH?ref=decb6196c2c1e6ed421d393a642f0c844cc333ba" \
  --jq '.content' | base64 -d
```

---

## Task Structure

```
_GLOBAL.md (this document)
├── contracts/
│   └── _MANIFEST.yaml
├── SUBTASK_sql-correctness/_BRIEF.md   (concern 3 — SQL analysis)
├── SUBTASK_spec-deviation/_BRIEF.md    (concern 4 — type consistency)
└── SUBTASK_synthesis/_BRIEF.md         (synthesis gate — merges findings into FINDINGS.md)
```

## Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_sql-correctness` | none | SQL correctness — concern 3 | `SUBTASK_sql-correctness/FINDINGS.md` |
| `SUBTASK_spec-deviation` | none | Spec deviation — concern 4 | `SUBTASK_spec-deviation/FINDINGS.md` |
| `SUBTASK_synthesis` | `SUBTASK_sql-correctness`, `SUBTASK_spec-deviation` | Merge into final FINDINGS.md | `FINDINGS.md` |

## Dependency Graph

```
SUBTASK_sql-correctness ──┐
                          ├── SUBTASK_synthesis
SUBTASK_spec-deviation  ──┘
```

---

## Contract

**Contract location**: `contracts/` (read-only for all descendants)
**Schema reference**: `../contracts/findings_schema.md` — all FINDINGS.md files in this subtree MUST conform to this schema.

See `contracts/_MANIFEST.yaml` for ownership table and identities.

---

## Subtree Methodology Posture

**Dominant task type**: Code review (both analysis spokes + synthesis)
**Primary bundles**: `code-review`, supporting `rust` for type-level analysis
**Cross-cutting bindings**:
- All findings cite file+line at pinned commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- No host paths, private IPs, or infrastructure details in any finding
- Prose passes the plain-voice bar from `../contracts/findings_schema.md`
- SQL correctness verdict is based on reading the actual query, not on assuming the
  formatter would not introduce bugs

---

## Output Specification

| Deliverable | Format | Location |
|-------------|--------|----------|
| Final spoke findings | Markdown | `FINDINGS.md` (at this workspace) |
| Partial findings — SQL | Markdown | `SUBTASK_sql-correctness/FINDINGS.md` |
| Partial findings — spec | Markdown | `SUBTASK_spec-deviation/FINDINGS.md` |
