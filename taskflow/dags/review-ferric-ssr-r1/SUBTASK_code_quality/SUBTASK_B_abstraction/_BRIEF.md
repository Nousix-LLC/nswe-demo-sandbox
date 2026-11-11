# Area B: Abstraction Boundaries — PR #228

## Task Specification

**Slug**: SUBTASK_B_abstraction
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective

Examine the abstraction boundaries in PR #228 (`work/ferric-ssr-r1`, repo `Nousix-LLC/nswe-demo`) between the SSR code path and the client-side (browser/WASM) code path. Identify leaks, inappropriate cross-path dependencies, or design decisions that conflate the two concerns. Produce one area finding file at the declared output path.

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

This area covers how the PR separates the SSR code path from the client-side rendering path:
- Whether the SSR path avoids referencing browser-only types, `web-sys`, or `wasm-bindgen` APIs
- Whether the client-side hydration path re-implements (duplicates) any SSR HTML serialization logic
- Whether `cfg` attributes or Cargo feature flags correctly isolate platform-specific code, or whether platform branching is mixed into shared logic via runtime flags
- Any abstraction leak: SSR logic leaking into client-only paths, or DOM/WASM calls guarded only by a flag rather than by compile-time separation

The boundary: naming consistency belongs in Area A; error handling belongs in Area C; duplication between paths belongs in Area D. If a leak finding also touches another area, note it but keep the primary finding here.

---

## Output

| Attribute | Value |
|-----------|-------|
| File | `area_b_abstraction.md` |
| Location | this workspace (`SUBTASK_B_abstraction/`) |
| Must conform to | `../contracts/findings_schema.yaml` |

One verdict (CLEAN, FINDING (NON-BLOCKER), or FINDING (BLOCKER)). FINDING includes at least one citation with a repository-relative file path and line number.

---

## Success Criteria

- `area_b_abstraction.md` exists before this task reports completed
- One verdict explicitly stated
- "What was checked" names the specific modules, cfg attributes, and code paths examined
- Each finding is actionable with enough specificity to guide the author
- No finding cites #225 / REQ-SSR-007 (inherited non-goal)

## Inherited Constraints

- Read-only: do not modify source code
- Citations use repository-relative paths in `Nousix-LLC/nswe-demo`, not host paths
- #225 / REQ-SSR-007 is not a code quality finding for this PR
- Non-blockers: flag as FINDING (NON-BLOCKER); the outer synthesis will track them
