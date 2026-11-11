# Area F: Documentation — PR #228

## Task Specification

**Slug**: SUBTASK_F_documentation
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective

Examine the documentation introduced or modified in PR #228 (`work/ferric-ssr-r1`, repo `Nousix-LLC/nswe-demo`) — specifically public API doc comments, usage examples, and noted caveats — for sufficiency for a first-time user of the ferric SSR and hydration surface. Produce one area finding file at the declared output path.

---

## Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Hub | `../_GLOBAL.md` | PR coordinates, citation constraints, non-goal boundary |
| Findings schema | `../contracts/findings_schema.yaml` | Required output structure |
| PR diff | `gh pr diff 228 --repo Nousix-LLC/nswe-demo` | The change under review (doc comments and any docs/ additions) |
| ferric crate source | `crates/ferric/` on branch `work/ferric-ssr-r1` | Full doc comment content on public items |

---

## Review Scope

This area covers the documentation attached to the new public API surface:
- Whether `render_to_string` and `hydrate` have doc comments (`///`) at the pub API level
- Whether doc comments include a usage example or enough context for a first-time user to call the function correctly
- Whether important caveats are documented (e.g., "do not call hydrate before the SSR HTML is in the DOM", "the marker format is not stable across versions"), particularly anything that could cause silent misbehavior if a user misses it
- Whether the PR description or any associated prose (changelog entries, README changes) is clear and free of inflated language that obscures the actual change

The boundary: internal `//` comments are out of scope. The focus is `///` doc comments on `pub` items and any user-facing prose the PR ships.

---

## Output

| Attribute | Value |
|-----------|-------|
| File | `area_f_documentation.md` |
| Location | this workspace (`SUBTASK_F_documentation/`) |
| Must conform to | `../contracts/findings_schema.yaml` |

One verdict (CLEAN, FINDING (NON-BLOCKER), or FINDING (BLOCKER)). FINDING includes at least one citation with a repository-relative file path and line number.

---

## Success Criteria

- `area_f_documentation.md` exists before this task reports completed
- One verdict explicitly stated
- "What was checked" names which pub items were inspected for doc comments
- Each finding is specific: names the item missing documentation and what a sufficient doc comment would contain
- No finding cites #225 / REQ-SSR-007 (inherited non-goal)

## Inherited Constraints

- Read-only: do not modify source code
- Citations use repository-relative paths in `Nousix-LLC/nswe-demo`, not host paths
- #225 / REQ-SSR-007 is not a code quality finding for this PR
- Non-blockers: flag as FINDING (NON-BLOCKER); the outer synthesis will track them
