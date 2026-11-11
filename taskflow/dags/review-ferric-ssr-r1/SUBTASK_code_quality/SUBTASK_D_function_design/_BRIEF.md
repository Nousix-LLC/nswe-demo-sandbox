# Area D: Function Size, Duplication, and Extensibility — PR #228

## Task Specification

**Slug**: SUBTASK_D_function_design
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective

Examine the function-level design in PR #228 (`work/ferric-ssr-r1`, repo `Nousix-LLC/nswe-demo`) for maintainability: function size, logical duplication between the SSR and client-side mount paths, and whether the design leaves clear extension points for future SSR concerns (e.g., async resources when #130 lands). Produce one area finding file at the declared output path.

---

## Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Hub | `../_GLOBAL.md` | PR coordinates, citation constraints, non-goal boundary |
| Findings schema | `../contracts/findings_schema.yaml` | Required output structure |
| PR diff | `gh pr diff 228 --repo Nousix-LLC/nswe-demo` | The change under review |
| ferric crate source | `crates/ferric/` on branch `work/ferric-ssr-r1` | Full file content for touched files |

---

## Review Scope

This area covers the internal design of the new code:
- Function sizes: are any functions large enough to impede review or future maintenance?
- Logical duplication between the SSR rendering path and the client-side mount/hydration path that could diverge over time (e.g., both contain their own version of a serialization step or component traversal)
- Extensibility: does the design leave seams for future SSR concerns (async resource handling in #130 is the documented upcoming case)? Or is the design monolithic in a way that would require invasive changes?
- Whether the structure is open for extension and closed for modification where appropriate

The boundary: compile-time separation via cfg/features belongs in Area B; `unwrap()`/panic-safety belongs in Area C; API naming belongs in Area A.

---

## Output

| Attribute | Value |
|-----------|-------|
| File | `area_d_function_design.md` |
| Location | this workspace (`SUBTASK_D_function_design/`) |
| Must conform to | `../contracts/findings_schema.yaml` |

One verdict (CLEAN, FINDING (NON-BLOCKER), or FINDING (BLOCKER)). FINDING includes at least one citation with a repository-relative file path and line number.

---

## Success Criteria

- `area_d_function_design.md` exists before this task reports completed
- One verdict explicitly stated
- "What was checked" names the specific functions and logical paths examined
- Duplication findings name both instances and explain why they could diverge
- Extensibility findings name the specific future concern (#130 / async resources) and where the design would need modification
- No finding cites #225 / REQ-SSR-007 (inherited non-goal)

## Inherited Constraints

- Read-only: do not modify source code
- Citations use repository-relative paths in `Nousix-LLC/nswe-demo`, not host paths
- #225 / REQ-SSR-007 is not a code quality finding for this PR
- Non-blockers: flag as FINDING (NON-BLOCKER); the outer synthesis will track them
