# _GLOBAL.md — Subtree Hub: SUBTASK_routing-ctas (sub-decomposition)

## Context

This is the sub-decomposition hub for `SUBTASK_routing-ctas`, a spoke of the
`review-chirp-logged-out-r1` review DAG.

**Review**: PR #263 (`Nousix-LLC/nswe-demo`, pinned commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`)
**Ancestor hub**: `../spoke-ui-states/_GLOBAL.md`
**This node's responsibility**: Three routing/CTA concerns — AC-4 sign-up path, CTA link
correctness in compose.rs, and the route annotation anomaly in app.rs. Each concern is
assigned to its own spoke child; a synthesis child assembles the findings.

## Scope

**In scope**: Three distinct analyses assigned to this node:
1. **AC-4 (sign-up path)**: sign_in_view → "Create an account" link → route resolution →
   usable sign-up implementation at the destination
2. **CTA link correctness**: compose.rs `render_signup()` contains `link("/compose", "Log in →")`;
   assess whether `/compose` is the right destination for a "Log in" CTA on the sign-up page
3. **Route annotation anomaly**: app.rs `/sign-in` alias has comment "for AC-3"; AC-3 is about
   recoverable error messages — assess whether this comment is a copy-paste error or signals
   a misunderstanding

**Out of scope**: AC-2 (empty_view), AC-3 (error message/Retry/role="alert"), header_nav, landing.rs —
those belong to SUBTASK_landing-states (sibling).

## Shared context for all children

**Repository**: `Nousix-LLC/nswe-demo`
**Pinned commit**: `decb6196c2c1e6ed421d393a642f0c844cc333ba`

**Route table** (confirmed in `app.rs`):
```
/signin     → sign_in_view       (sign_in.rs)
/sign-in    → sign_in_view       (alias; comment says "for AC-3" — concern 3)
/signup     → signup_view        (compose.rs — the FUNCTIONAL sign-up form)
```

**Key context**: `sign_up.rs` exports `sign_up_view` (a placeholder stub with a disabled
"Create account (coming soon)" button) — this stub is NOT in the route table.
Any visitor who follows a `/signup` link reaches `compose.rs`'s `signup_view`, not `sign_up.rs`.

**Primary source files**:
- `crates/chirp-frontend/src/sign_in.rs` — sign-in view, "Create an account" link (concern 1)
- `crates/chirp-frontend/src/sign_up.rs` — placeholder stub (concern 1 reference)
- `crates/chirp-frontend/src/compose.rs` — `signup_view`, `render_signup`, the CTA link (concern 2)
- `crates/chirp-frontend/src/app.rs` — route table, `/sign-in` alias annotation (concerns 1 + 3)

## Task structure

| Task id | Depends on | Concern | Output |
|---------|------------|---------|--------|
| `SUBTASK_ac4-path` | none | AC-4 sign-in-to-sign-up path | `SUBTASK_ac4-path/concern-ac4.md` |
| `SUBTASK_cta-link` | none | CTA link correctness (compose.rs) | `SUBTASK_cta-link/concern-cta.md` |
| `SUBTASK_annotation` | none | Route annotation anomaly (app.rs) | `SUBTASK_annotation/concern-annotation.md` |
| `SUBTASK_synthesis` | `SUBTASK_ac4-path`, `SUBTASK_cta-link`, `SUBTASK_annotation` | Assemble FINDINGS.md | `FINDINGS.md`, `SYNTHESIS.md` |

## Subtree Methodology Posture

**Dominant task type**: Code review
**Primary bundles**: `code-review` (primary), `frontend` (supporting)

**Cross-cutting binding**: Every finding MUST cite file path + line number at pinned commit
`decb6196c2c1e6ed421d393a642f0c844cc333ba`. Severity labels: `blocker` or `non-blocking` only.
Never name host paths, private IPs, or internal infrastructure details in findings.

These are suggestions; each child agent retains final judgment over what it loads.

## Contract

**Contract location**: `contracts/`

| Artifact | Kind | Declares |
|----------|------|----------|
| `contracts/_MANIFEST.yaml` | yaml_schema | Ownership and structure of concern outputs and FINDINGS.md |

**Ownership**:

| Artifact | Owning subtask |
|----------|----------------|
| `SUBTASK_ac4-path/concern-ac4.md` | `SUBTASK_ac4-path` |
| `SUBTASK_cta-link/concern-cta.md` | `SUBTASK_cta-link` |
| `SUBTASK_annotation/concern-annotation.md` | `SUBTASK_annotation` |
| `FINDINGS.md` | `SUBTASK_synthesis` |
| `SYNTHESIS.md` | `SUBTASK_synthesis` |

**Identities that MUST hold across combined outputs**:
- [ ] All three concerns (AC-4 path, CTA link, annotation) addressed in FINDINGS.md
- [ ] Every finding or clean note cites file + line at the pinned commit
- [ ] No concern is duplicated or omitted across the three spokes

## Subtree-Wide Constraints

- Repository: `Nousix-LLC/nswe-demo` only
- Pinned commit: `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- Do not post to the PR
- Findings cite repository file paths and lines; never name host paths, private IPs, or infrastructure details
- Do not investigate landing.rs concerns (AC-2, AC-3, header_nav) — those are SUBTASK_landing-states scope
