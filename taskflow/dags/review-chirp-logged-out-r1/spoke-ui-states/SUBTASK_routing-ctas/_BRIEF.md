# _BRIEF.md — SUBTASK_routing-ctas

## Task Specification

**Slug**: SUBTASK_routing-ctas
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective

Review the sign-up / sign-in routing and CTA links introduced by PR #263 (`Nousix-LLC/nswe-demo`, commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`) for three concerns:
- **AC-4 (remaining)**: Does `sign_in_view` link to sign-up? Does following that link reach a usable sign-up page? Which sign-up implementation does a visitor actually reach via the route table?
- **CTA link correctness**: `compose.rs`'s `render_signup()` contains `link("/compose", "Log in →")`. Does this link to the right place for a logged-out visitor, or does it expose an internal compose path?
- **Route annotation anomaly**: The `/sign-in` alias in `app.rs` has the comment "for AC-3". AC-3 is about recoverable error messages. Is this a copy-paste error or does it signal a genuine misunderstanding?

### Context

This task is part of the spoke-ui-states subtree (see `_GLOBAL.md` in the parent workspace).
The route table is documented in that hub document.

Key context from the hub: `sign_up.rs` exports `sign_up_view` (placeholder stub with a
disabled "Create account (coming soon)" button) which is **NOT in the route table**.
The route `/signup` → `signup_view` (compose.rs — a functional form). This context is
provided so you can verify it rather than re-derive it.

**Dependencies**: none (runs in parallel with SUBTASK_landing-states)
**Dependents**: SUBTASK_synthesis (reads this task's output)

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, route table, constraints |
| PR diff — routing files | GitHub API: `Nousix-LLC/nswe-demo`, PR #263 | See what changed |
| Source file | `crates/chirp-frontend/src/sign_in.rs` | sign-in view and its "Create an account" link |
| Source file | `crates/chirp-frontend/src/compose.rs` | `signup_view`, `render_signup`, and the `/compose` link |
| Source file | `crates/chirp-frontend/src/sign_up.rs` | Placeholder stub — confirm not in route table |
| Source file | `crates/chirp-frontend/src/app.rs` | Route table, `/sign-in` alias annotation |

---

## Process Specification

**AC-4 (remaining) — sign-in-to-sign-up path**:
1. Read `sign_in.rs`. Locate the "Create an account" link (or equivalent CTA). What path does it link to? (Expected: `/signup` or `/sign-up` or similar.)
2. Cross-reference with the route table in `app.rs`: does that path resolve to a route?
3. Read the target route's implementation: is the sign-up page usable (functional form, not a placeholder with a disabled button)?
4. Confirm: a visitor who clicks the "Create an account" link from the sign-in screen reaches a working sign-up form, not a dead end.

**CTA link correctness — compose.rs**:
1. Read `render_signup()` in `compose.rs`. Locate `link("/compose", "Log in →")`.
2. Assess: `/compose` is the compose/write-chirp route (also in the route table). Is this the right destination for a "Log in" CTA on the sign-up page? A logged-out visitor on the sign-up page clicking "Log in →" would reach the compose view — is this correct behavior or a bug?
3. The correct destination for "Log in" from a sign-up form is the sign-in page (`/signin`). Assess whether the link target exposes an internal app route inappropriately.

**Route annotation anomaly — app.rs**:
1. Find the `/sign-in` alias in `app.rs` with its "for AC-3" comment.
2. AC-3 is about recoverable error messages on the timeline. What is the connection between a `/sign-in` route alias and AC-3? None — AC-3 does not require a route alias.
3. Assess: is this a copy-paste error (the comment was meant for a different route or a different kind of note), or does it signal that the author misunderstands what AC-3 requires?
4. This is a prose/annotation finding. Rate its severity: does it indicate an actual behavioral bug, or only a misleading comment?

For each concern: if it passes, note what was checked and found clean. If it has a problem,
state the location (file + line), what principle is at stake, why it matters, severity
(blocker / non-blocking), and what would satisfy it.

### Methodology

Apply the Code Review methodology:
- Read the actual code, not the PR description
- Assess each concern against the acceptance criteria it claims to implement
- Cite specific lines at the pinned commit for every finding or clean note

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| Filename | `FINDINGS.md` |
| Location | `SUBTASK_routing-ctas/` (this workspace) |

The file MUST follow the schema in `../contracts/_MANIFEST.yaml`:

```markdown
# Findings — routing-ctas review

## Concerns checked
- AC-4 remaining (sign-in-to-sign-up path and usable sign-up): [one-line summary]
- CTA link correctness (compose.rs link("/compose", ...)): [one-line summary]
- Route annotation anomaly (/sign-in alias "for AC-3" comment): [one-line summary]

## Findings
[List of findings, each with location, principle, rationale, severity, resolution.
If none: "None — all three concerns checked clean."]

## Clean items
[For each concern that passed: what was examined and what was found]
```

---

## Success criteria

- [ ] AC-4 (remaining): sign-in-to-sign-up path traced end-to-end with evidence; which sign-up implementation is reached is stated explicitly
- [ ] CTA link: `link("/compose", "Log in →")` destination assessed as correct or incorrect with reasoning
- [ ] Route annotation anomaly: the "for AC-3" comment assessed with a verdict (copy-paste error, misunderstanding, or intentional-and-correct)
- [ ] Every finding or clean note cites file + line at commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- [ ] `FINDINGS.md` written to this workspace

---

## Suggested Methodology Files

**Task-type row matched**: Code review → Primary: `code-review`, Supporting: `frontend`

Suggested files (from the methodology loader):
- `code-review/CodeReview_Process_Methodology.md` — review process framework; use to structure examination and verdict reasoning
- `code-review/CodeReview_Checklist_Methodology.md` — review checklist; apply navigation/routing items
- `frontend/Frontend_Application_Architecture_Methodology.md` — routing and navigation architecture; useful for assessing whether the route table and CTA links are structured correctly

These are the parent's flagged suggestions. Load fewer if some are clearly inapplicable; load more if your reading of the brief reveals additional needs.

## Inherited Constraints

- Repository: `Nousix-LLC/nswe-demo` only
- Pinned commit: `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- Do not post to the PR
- Findings point at repository file paths and lines; never name host paths, private IPs, or internal infrastructure
- Stay within the routing/CTA concerns assigned here; do not investigate landing.rs states (AC-2, AC-3, header_nav — those belong to SUBTASK_landing-states)

## Out-of-Scope Methodologies

- `code-review/CodeReview_PR_Authoring_Methodology.md` — not applicable; this task reads and judges, does not author PRs
- Landing page states (empty_view, error_banner, header_nav) — owned by SUBTASK_landing-states; do not duplicate
