# _GLOBAL.md — Sub-decomposition Hub: SUBTASK_landing-states

## Context

This is the hub document for the second-level decomposition of `SUBTASK_landing-states`.

**Parent workspace**: `spoke-ui-states/` (see `../_GLOBAL.md` for broader review context)
**Repository**: `Nousix-LLC/nswe-demo`
**Pinned commit**: `decb6196c2c1e6ed421d393a642f0c844cc333ba`
**Primary file under review**: `crates/chirp-frontend/src/landing.rs`

This decomposition covers three distinct acceptance-criteria checks of `landing.rs`,
each assigned to a parallel spoke, with a synthesis task combining them into `FINDINGS.md`.

## Scope

**In scope** (this sub-decomposition):
1. **AC-2** — Does `empty_view()` explain what Chirp is and present an obvious sign-up / sign-in CTA?
2. **AC-3** — Does the initial-error path in `view_tree` render a user-readable message (not raw
   Rust error/debug repr), offer a usable Retry action, and carry `role="alert"` on the error element?
3. **AC-4-partial** — Is `header_nav()` present in EVERY rendered state of `landing_view`:
   loading, error, empty, populated, and any other branch?

**Out of scope** (owned by `SUBTASK_routing-ctas` or parent siblings):
- AC-4 sign-up path correctness, CTA link, route annotation anomaly
- AC-1, AC-5, code quality, security, test coverage

## Shared inputs for all children

| Input | Source | Purpose |
|-------|--------|---------|
| Parent hub | `../_GLOBAL.md` | Broader review context, route table |
| Parent contract | `../contracts/_MANIFEST.yaml` | FINDINGS.md schema to conform to |
| Primary source | `crates/chirp-frontend/src/landing.rs` at pinned commit | File under review |

## Task structure

| Task id | Depends on | Concern | Output |
|---------|------------|---------|--------|
| `SUBTASK_check-ac2` | none | AC-2: `empty_view()` content and CTA | `SUBTASK_check-ac2/concern_ac2.md` |
| `SUBTASK_check-ac3` | none | AC-3: error-state recoverability and `role="alert"` | `SUBTASK_check-ac3/concern_ac3.md` |
| `SUBTASK_check-ac4p` | none | AC-4-partial: `header_nav()` in every branch | `SUBTASK_check-ac4p/concern_ac4p.md` |
| `SUBTASK_synthesis-findings` | `SUBTASK_check-ac2`, `SUBTASK_check-ac3`, `SUBTASK_check-ac4p` | Combine into FINDINGS.md | `FINDINGS.md` |

**Dependency graph**:
```
SUBTASK_check-ac2  ──┐
                     │
SUBTASK_check-ac3  ──├── SUBTASK_synthesis-findings → FINDINGS.md
                     │
SUBTASK_check-ac4p ──┘
```

## Subtree Methodology Posture

**Dominant task type**: Code review  
**Primary bundle**: `code-review` (CodeReview_Process, CodeReview_Checklist)  
**Supporting bundle**: `frontend` (Frontend_Component_Design — Leptos component patterns)

**Cross-cutting binding for all children**:
- Every finding MUST cite `crates/chirp-frontend/src/landing.rs` + line at pinned commit
  `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- Severity labels: `blocker` or `non-blocking` only
- Do NOT name host paths, private IPs, or internal infrastructure

These are suggestions, not prescriptions; each child agent retains final judgment.

## Contract

**Contract location**: `contracts/`

| Artifact | Kind | Declares |
|----------|------|----------|
| `contracts/_MANIFEST.yaml` | yaml_schema | Per-concern findings format, ownership, identities |
| `contracts/concern_findings_schema.yaml` | yaml_schema | Schema each concern-checker output must follow |

**Ownership**:
| Artifact | Owning subtask |
|----------|----------------|
| `SUBTASK_check-ac2/concern_ac2.md` | `SUBTASK_check-ac2` |
| `SUBTASK_check-ac3/concern_ac3.md` | `SUBTASK_check-ac3` |
| `SUBTASK_check-ac4p/concern_ac4p.md` | `SUBTASK_check-ac4p` |
| `FINDINGS.md` | `SUBTASK_synthesis-findings` |

**Identities that MUST hold across combined outputs**:
- [ ] All three concerns (AC-2, AC-3, AC-4-partial) are addressed in concern files
- [ ] Every finding includes location, principle, rationale, severity, resolution
- [ ] Every location cites the pinned commit
- [ ] `FINDINGS.md` conforms to the parent contract (`../contracts/_MANIFEST.yaml`) schema

## Subtree-Wide Constraints

- Repository: `Nousix-LLC/nswe-demo` only
- Pinned commit: `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- Do not post to the PR
- Findings point at repository file paths and lines; never name host paths, private IPs, or
  internal infrastructure details
- Each checker covers ONE concern only; do not bleed into sibling concerns
