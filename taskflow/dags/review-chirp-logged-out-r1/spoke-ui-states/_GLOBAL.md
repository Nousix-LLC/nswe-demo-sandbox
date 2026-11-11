# _GLOBAL.md — Subtree Hub: spoke-ui-states

## Context

This is the subtree hub for the `spoke-ui-states` node of the `review-chirp-logged-out-r1` DAG.

**Parent review**: PR #263 (`Nousix-LLC/nswe-demo`, head `decb6196c2c1e6ed421d393a642f0c844cc333ba`)
**Ancestor hub**: `taskflow/dags/review-chirp-logged-out-r1/_GLOBAL.md`
**This spoke's responsibility**: Review AC-2 (empty-state CTA), AC-3 (recoverable error message),
and AC-4 (sign-up / sign-in CTA visibility and reachability), including two code-specific
sub-observations surfaced while examining AC-4.

## Scope

**In scope**: The five concerns the parent brief assigns to this spoke:
1. AC-2 — `empty_view()` in `landing.rs`: does it explain Chirp and show an obvious CTA?
2. AC-3 — initial-error path in `view_tree`: recoverable message and usable Retry; `role="alert"` check
3. AC-4 — `header_nav()` presence in every rendered state; sign-in-to-sign-up link; which sign-up implementation is reached
4. CTA link correctness — `link("/compose", "Log in →")` in `compose.rs` `render_signup()`
5. Route annotation anomaly — `/sign-in` alias comment "for AC-3"

**Out of scope**: AC-1 (access without forced auth), AC-5 (state machine completeness), code
quality / security / tests — those belong to sibling spokes of the parent DAG.

## Shared context for all children

**Repository**: `Nousix-LLC/nswe-demo`
**Pinned commit**: `decb6196c2c1e6ed421d393a642f0c844cc333ba`

**Route table** (from parent _GLOBAL.md, confirmed from `app.rs`):
```
/signin     → sign_in_view       (sign_in.rs)
/sign-in    → sign_in_view       (alias; comment says "for AC-3" — anomaly to investigate)
/signup     → signup_view        (compose.rs — the FUNCTIONAL form)
```
Note: `sign_up.rs` exports `sign_up_view` (placeholder stub with disabled button) which is NOT
in the route table. Any visitor following a `/signup` link reaches `compose.rs`'s `signup_view`.

**Primary code areas** (each child reads what it needs; listed here for orientation):
- `crates/chirp-frontend/src/landing.rs` — `empty_view()`, `header_nav()`, `error_banner()`,
  `footer()`, `view_tree` dispatch logic
- `crates/chirp-frontend/src/sign_in.rs` — sign-in stub, its "Create an account" link
- `crates/chirp-frontend/src/sign_up.rs` — sign-up placeholder stub (not in route table)
- `crates/chirp-frontend/src/compose.rs` — `signup_view`, `render_signup`,
  `link("/compose", "Log in →")` link
- `crates/chirp-frontend/src/app.rs` — route table, `/sign-in` alias annotation

**Notable context from parent**: `timeline.rs` now routes the authenticated home timeline through
`/api/public/timeline` rather than the per-user following feed — a cross-cutting observation that
other spokes handle. Children here do NOT need to investigate that; stay within AC-2/3/4.

## Task structure

| Task id | Depends on | Concern cluster | Output |
|---------|------------|-----------------|--------|
| `SUBTASK_landing-states` | none | AC-2, AC-3, header_nav aspect of AC-4 | `SUBTASK_landing-states/FINDINGS.md` |
| `SUBTASK_routing-ctas` | none | AC-4 sign-up path, CTA link, route annotation | `SUBTASK_routing-ctas/FINDINGS.md` |
| `SUBTASK_synthesis` | `SUBTASK_landing-states`, `SUBTASK_routing-ctas` | Combine into final verdict | `REVIEW.md` + `SYNTHESIS.md` |

## Subtree Methodology Posture

**Dominant task type**: Code review (all three children)
**Primary bundles**: `code-review` (primary), `frontend` (supporting — Leptos/Rust frontend patterns)

**Cross-cutting binding**: Every finding MUST cite file path + line number at the pinned commit.
Severity labels are: `blocker` or `non-blocking`. Do NOT name host paths, private IPs, or
internal infrastructure details in findings.

These are suggestions, not prescriptions. Each child agent retains final judgment over which
methodology files to load.

## Contract

**Contract location**: `contracts/`

| Artifact | Kind | Declares |
|----------|------|----------|
| `contracts/_MANIFEST.yaml` | yaml_schema | Ownership and structure of FINDINGS.md outputs |

**Ownership**:
| Artifact | Owning subtask |
|----------|----------------|
| `SUBTASK_landing-states/FINDINGS.md` | `SUBTASK_landing-states` |
| `SUBTASK_routing-ctas/FINDINGS.md` | `SUBTASK_routing-ctas` |
| `REVIEW.md` | `SUBTASK_synthesis` |
| `SYNTHESIS.md` | `SUBTASK_synthesis` |

**Identity that MUST hold across combined outputs**:
- [ ] Every AC-2, AC-3, and AC-4 sub-concern named in this hub's Scope section is addressed
      in at least one FINDINGS.md
- [ ] No sub-concern is claimed by both SUBTASK_landing-states and SUBTASK_routing-ctas
      (partition is clean)
- [ ] Every finding cites the pinned commit hash and a file+line reference

## Subtree-Wide Constraints

- Repository: `Nousix-LLC/nswe-demo` only
- Pinned commit: `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- Do not post to the PR (that is the parent DAG's synthesis child's responsibility)
- Do not investigate concerns outside this spoke's scope (AC-1, AC-5, code quality, etc.)
- Findings point at repository file paths and lines; never name host paths, private IPs, or
  internal infrastructure details
