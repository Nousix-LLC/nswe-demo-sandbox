# Area A: API Surface and Naming — PR #228

## Task Specification

**Slug**: SUBTASK_A_api_surface
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective

Examine the public API surface introduced or modified in PR #228 (`work/ferric-ssr-r1`, repo `Nousix-LLC/nswe-demo`) for naming consistency with the existing ferric crate, Rust idiom, and fitness for first-time users. Produce one area finding file at the declared output path.

---

## Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Hub | `../_GLOBAL.md` | PR coordinates, citation constraints, non-goal boundary |
| Findings schema | `../contracts/findings_schema.yaml` | Required output structure |
| PR diff | `gh pr diff 228 --repo Nousix-LLC/nswe-demo` | The change under review |
| ferric crate source | `crates/ferric/` on branch `work/ferric-ssr-r1` | Full file content for touched files, existing API surface |

---

## Review Scope

This area covers the public (crate-level `pub`) API surface exposed by the PR:
- Naming and positioning of `render_to_string`, `hydrate`, and the Axum integration point relative to the rest of the ferric API
- Module structure under `crates/ferric/` and how the new surface fits
- Function signature conventions against Rust naming idioms and existing ferric patterns
- Naming consistency and anything that would surprise a ferric API user

The boundary: internals and private items are out of scope for this area. Cross-area overlap (e.g., an API shape that also reflects an abstraction concern) should be noted but the primary finding belongs to the most applicable area.

---

## Output

| Attribute | Value |
|-----------|-------|
| File | `area_a_api_surface.md` |
| Location | this workspace (`SUBTASK_A_api_surface/`) |
| Must conform to | `../contracts/findings_schema.yaml` |

The output file must have one verdict (CLEAN, FINDING (NON-BLOCKER), or FINDING (BLOCKER)). If FINDING, include at least one citation with a repository-relative file path and line number in `Nousix-LLC/nswe-demo`.

---

## Success Criteria

- `area_a_api_surface.md` exists before this task reports completed
- One verdict, explicitly stated
- "What was checked" names the specific exports, modules, and functions examined
- Each finding is actionable: a reader who was not inside the reviewer's head can act on it
- No finding cites #225 / REQ-SSR-007 (inherited non-goal)

## Inherited Constraints

- Read-only: do not modify source code
- Citations use repository-relative paths in `Nousix-LLC/nswe-demo`, not host paths
- #225 / REQ-SSR-007 is not a code quality finding for this PR
- Non-blockers: flag as FINDING (NON-BLOCKER); the outer synthesis will track them
