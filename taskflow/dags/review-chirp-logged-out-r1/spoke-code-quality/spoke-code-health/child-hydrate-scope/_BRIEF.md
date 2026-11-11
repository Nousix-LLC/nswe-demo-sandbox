# Task: hydrate.rs Scope and Sync Assessment (Concern 7)

## Task Specification

**Slug**: child-hydrate-scope
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective

Assess whether the `hydrate.rs` EventKind expansion in PR #263 is causally required by the public
timeline feature, and whether `static_event_kinds()` introduces a manual-sync risk against the
`EventKind` enum.

### Context

This task covers concern 7 from the parent spoke `spoke-code-health`. See `../_GLOBAL.md` for
PR context, the pinned commit, and subtree constraints. The parent spoke's concern assignment:

> The `hydrate.rs` changes include an expansion from 2 to 47+ `EventKind` enum variants, an
> `EventHandler::WithEvent` variant, and a `static_event_kinds()` table. These are
> framework-level changes bundled with an application feature PR.
>
> Assess:
> - Are the `hydrate.rs` changes causally required by the public timeline feature, or are they
>   a scope expansion?
> - Does the `static_event_kinds()` table introduce a sync risk — that is, must it be kept
>   manually in sync with the `EventKind` enum, and if so, is there any guard against drift?
> - If a new `EventKind` variant is added without updating `static_event_kinds()`, what happens
>   at runtime? Is the failure silent, a panic, or detected at compile time?

**Pin commit**: `decb6196c2c1e6ed421d393a642f0c844cc333ba`

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | PR context, pin commit, constraints |
| Concern finding schema | `../contracts/concern_finding_schema.md` | Output structure |
| `hydrate.rs` | `crates/ferric/src/hydrate.rs` at HEAD | Full file — EventKind and static_event_kinds() |
| PR diff | `gh pr diff 263 -R Nousix-LLC/nswe-demo` | What changed in hydrate.rs vs prior state |

Access file contents via:
```bash
gh api "repos/Nousix-LLC/nswe-demo/contents/PATH?ref=decb6196c2c1e6ed421d393a642f0c844cc333ba" \
  --jq '.content' | base64 -d
```

To understand what was in hydrate.rs before the PR, compare the diff with the current file. The
diff will show which lines were added.

---

## Process Specification

For the scope question:
1. Read the full `hydrate.rs` at HEAD and count the `EventKind` enum variants
2. Read the PR diff for `hydrate.rs` to see which lines were added in this PR vs pre-existing
3. Identify which new EventKind variants (if any) are specifically required for the public
   timeline feature (e.g., `TimelinePost`, `TimelineLike`, `Scroll`, or whatever the feature uses)
4. Identify which new variants appear to be general framework additions not specific to the feature
5. Determine whether the diff mixes application-feature work and framework refactoring in a single
   commit/PR

For the sync risk question:
1. Read `static_event_kinds()` in its entirety — what does it return? A list of `EventKind`s?
2. Determine whether the return value is derived from the enum (via iteration, strum, or compile-
   time enumeration) or is a hand-written list that must track the enum manually
3. If hand-written: determine whether a new variant added to `EventKind` without updating
   `static_event_kinds()` would cause: a compile-time error (if used in a match with no default),
   a silent omission (if only listed as a "fire-and-forget" registration), or a panic
4. Check whether the codebase has any test, assertion, or compile-time guard that catches enum-
   vs-table drift

### Methodology

Domain Mapping match: **Code review** → Primary: `Code Review`, Supporting: `Core`, `Code Quality`

Suggested methodology files:
- `code-review/CodeReview_Process_Methodology.md` — reading for what the change touches beyond its
  own stated lines; the hydrate.rs framework refactor is exactly the "what isn't there" pattern
  (a framework expansion bundled with an app feature hides the scope expansion)
- `code-review/CodeReview_Checklist_Methodology.md` — scope discipline and "what this PR touches
  beyond its stated purpose" rows
- `code-quality/Framework_Clean_Code_Methodology.md` — unnecessary scope expansion, manual-sync
  anti-patterns

These are suggested starting points. The child agent is the final judge of what the work requires.

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| Filename | `finding_c7.md` |
| Format | Markdown |
| Location | `child-hydrate-scope/` (this workspace) |

Structure: per `../contracts/concern_finding_schema.md`.

Required sections:
1. `## Concern 7 — hydrate.rs Scope and Sync Risk`
2. `## Investigation`
3. `## Verdict`
4. `## Finding` (one entry per issue found — scope expansion and/or sync risk — if present)

---

## Success Criteria

- Verdict on whether the EventKind expansion is causally required by the public timeline feature
- Verdict on whether `static_event_kinds()` is manually synced or derived, and what the failure
  mode is if it drifts from the enum
- If a sync risk exists without a guard: a Finding entry with location, principle, severity,
  and satisfying condition
- If the scope expansion is a framework refactor bundled with an app PR: a Finding entry
- No internal host paths, private IPs, or infrastructure details
- Prose passes the plain-voice bar

---

## Suggested Methodology Files

Domain Mapping match: **Code review** → Primary: `Code Review`, Supporting: `Core`, `Code Quality`

Specific files:
- `code-review/CodeReview_Process_Methodology.md` — the "what the change touches beyond its own stated lines" principle
- `code-review/CodeReview_Checklist_Methodology.md` — scope discipline rows
- `code-quality/Framework_Clean_Code_Methodology.md` — manual-sync anti-patterns and unnecessary scope expansion

These are suggested starting points. The child agent is the final judge of what the work requires.

## Inherited Constraints

- Findings point at repository file paths and line numbers at pinned commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- No host paths, private IPs, or infrastructure details in any finding
- Do not post to the PR
- Prose in finding_c7.md must pass the plain-voice bar
- Repository: `Nousix-LLC/nswe-demo` only

## Out-of-Scope

- Concern 6 (`sign_up::sign_up_view`) — assigned to `child-dead-code`
- Test depth — assigned to `spoke-tests`
- Security/error safety — assigned to `spoke-safety-idiom`
- Rust idiom issues beyond the sync-risk question — assigned to `spoke-safety-idiom`
