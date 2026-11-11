# _BRIEF.md — SUBTASK_landing-states

## Task Specification

**Slug**: SUBTASK_landing-states
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective

Review `landing.rs` from PR #263 (`Nousix-LLC/nswe-demo`, commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`) for three concerns:
- **AC-2**: Does `empty_view()` explain what Chirp is and present an obvious CTA to sign up or sign in? Is it a clear statement — not a blank page or generic "No items"?
- **AC-3**: Does the initial-error path in `view_tree` render a user-readable message (not a raw technical error) and a usable Retry action? Does `role="alert"` on the error banner satisfy the recoverable-message bar?
- **AC-4 (partial)**: Is `header_nav()` present in EVERY rendered state of `landing_view` — including loading, error, and empty/populated states? This is the question of whether the sign-up / sign-in entry points are always visible from the landing page regardless of load outcome.

### Context

This task is part of the spoke-ui-states subtree (see `_GLOBAL.md` in the parent workspace).
Route table and shared context are in that hub document.

**Dependencies**: none (runs in parallel with SUBTASK_routing-ctas)
**Dependents**: SUBTASK_synthesis (reads this task's output)

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, route table, constraints |
| PR diff — landing.rs | GitHub API: `Nousix-LLC/nswe-demo`, PR #263 | See what changed |
| Source file | `crates/chirp-frontend/src/landing.rs` at pinned commit | Full context for review |

Optionally also read `crates/chirp-frontend/src/app.rs` to verify how `landing_view` is wired
(the route `/` → `landing_view`), but this file is SUBTASK_routing-ctas's primary concern.
Focus on `landing.rs`; do not duplicate routing-system work.

---

## Process Specification

For each of the three concerns, examine `landing.rs` directly:

**AC-2 — empty_view()**: Read `empty_view()`. Does it include a human-readable description of
what Chirp is? Does it include a CTA (button or link) to sign up or sign in? Does it avoid
"No items" or blank-page patterns?

**AC-3 — error state**: Find the error branch in `view_tree` (likely a match arm on the
`Status::Error` or `Err(_)` case). Check: (a) is the message human-readable rather than a
raw Rust error/debug repr? (b) is there a Retry action the user can take? (c) does the
element rendering the error message carry `role="alert"` or equivalent ARIA? Assess whether
this meets the bar for a "clear, recoverable message."

**AC-4 (partial) — header_nav presence**: Find ALL match arms / branches in `view_tree` (or
the equivalent dispatch logic). For each branch — loading state, error state, empty content,
populated content, any other — check whether `header_nav()` is called. Report the exact
branches and whether `header_nav()` appears in each one.

For each concern: if it passes, note what was checked and found clean. If it has a problem,
state the location (file + line), what principle is at stake, why it matters, severity
(blocker / non-blocking), and what would satisfy it.

### Methodology

Apply the Code Review methodology to this examination:
- Read the actual code, not the PR description
- Assess each concern against what it claimed to implement
- Cite specific lines at the pinned commit for every finding or clean note

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| Filename | `FINDINGS.md` |
| Location | `SUBTASK_landing-states/` (this workspace) |

The file MUST follow the schema in `../contracts/_MANIFEST.yaml`:

```markdown
# Findings — landing-states review

## Concerns checked
- AC-2 (empty_view content and CTA): [one-line summary]
- AC-3 (error state recoverability and role="alert"): [one-line summary]
- AC-4 partial (header_nav in all states): [one-line summary]

## Findings
[List of findings, each with location, principle, rationale, severity, resolution.
If none: "None — all three concerns checked clean."]

## Clean items
[For each concern that passed: what was examined and what was found]
```

---

## Success criteria

- [ ] AC-2 adjudicated with specific evidence from `empty_view()` code
- [ ] AC-3 adjudicated with evidence from the error branch in `view_tree`
- [ ] `role="alert"` or its absence noted explicitly
- [ ] AC-4 (partial): every branch of `view_tree`'s dispatch logic is accounted for in terms of `header_nav()` presence
- [ ] Every finding or clean note cites file + line at commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- [ ] `FINDINGS.md` written to this workspace

---

## Suggested Methodology Files

**Task-type row matched**: Code review → Primary: `code-review`, Supporting: `frontend`

Suggested files (from the methodology loader):
- `code-review/CodeReview_Process_Methodology.md` — the review process framework; use to structure your examination and verdict reasoning
- `code-review/CodeReview_Checklist_Methodology.md` — review checklist; apply the relevant items to `landing.rs`
- `frontend/Frontend_Component_Design_Methodology.md` — Leptos is a Rust frontend framework with component patterns; useful for evaluating whether empty_view and error_banner are structured correctly

These are the parent's flagged suggestions based on task type. Load fewer if some are clearly inapplicable; load more if your reading of the brief reveals additional needs.

## Inherited Constraints

- Repository: `Nousix-LLC/nswe-demo` only
- Pinned commit: `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- Do not post to the PR
- Findings point at repository file paths and lines; never name host paths, private IPs, or internal infrastructure
- Stay within AC-2, AC-3, and the header_nav aspect of AC-4; do not investigate AC-1, AC-5, code quality, or routing concerns (those belong to SUBTASK_routing-ctas or other spokes)

## Out-of-Scope Methodologies

- `code-review/CodeReview_PR_Authoring_Methodology.md` — not applicable; this task reads and judges, does not author PRs
- Routing concerns (sign-up path, route annotation, app.rs) — owned by SUBTASK_routing-ctas; do not duplicate
