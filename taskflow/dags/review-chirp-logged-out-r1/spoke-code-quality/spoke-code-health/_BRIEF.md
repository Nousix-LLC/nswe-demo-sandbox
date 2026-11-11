# Task: Dead Code + Scope Analysis — PR #263

## Task Specification

**Slug**: spoke-code-health
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective

Assess dead-code reachability and scope discipline in PR #263 on `Nousix-LLC/nswe-demo`,
covering concerns 6 and 7 from the parent spoke brief.

### Context

This task is part of the code-quality review decomposition. See `../_GLOBAL.md` for PR details,
the full concern assignment table, and `../contracts/` for the FINDINGS.md output schema.

**Concerns assigned to this spoke:**

6. **`sign_up::sign_up_view` dead-code question**:
   `sign_up.rs` exports `sign_up_view` (a stub with a disabled button). The route table routes
   `/signup` to `signup_view` from `compose.rs`, not to `sign_up::sign_up_view`. Is
   `sign_up::sign_up_view` reachable from any route? If not, is the module dead code?

   To verify: read the route table (likely in a router or main.rs file), enumerate what routes
   to `sign_up.rs`, and check whether any live route calls `sign_up::sign_up_view` vs.
   `compose::signup_view`. If the function is unreachable from any live route, that is a code
   health finding.

7. **`ferric/src/hydrate.rs` scope**:
   The `hydrate.rs` changes include an expansion from 2 to 47+ `EventKind` enum variants, an
   `EventHandler::WithEvent` variant, and a `static_event_kinds()` table. These are
   framework-level changes bundled with an application feature PR.

   Assess:
   - Are the `hydrate.rs` changes causally required by the public timeline feature, or are they
     a scope expansion?
   - Does the `static_event_kinds()` table introduce a sync risk — that is, must it be kept
     manually in sync with the `EventKind` enum, and if so, is there any guard against drift?
   - If a new `EventKind` variant is added without updating `static_event_kinds()`, what happens
     at runtime? Is the failure silent, a panic, or detected at compile time?

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Hub context | `../_GLOBAL.md` | Concern assignments, pin commit, output schema |
| Contract schema | `../contracts/findings_schema.md` | FINDINGS.md structure |
| `sign_up.rs` | `crates/chirp-frontend/src/pages/sign_up.rs` at HEAD | The module with `sign_up_view` |
| `compose.rs` | `crates/chirp-frontend/src/pages/compose.rs` (or wherever `signup_view` is) | Competing signup view |
| Route table | Likely `crates/chirp-frontend/src/main.rs` or similar at HEAD | What routes to what |
| `hydrate.rs` | `crates/ferric/src/hydrate.rs` at HEAD | Full file — EventKind expansion and table |
| PR diff | `gh pr diff 263 -R Nousix-LLC/nswe-demo` | What changed in this PR |

Access files via:
```bash
gh api "repos/Nousix-LLC/nswe-demo/contents/PATH?ref=decb6196c2c1e6ed421d393a642f0c844cc333ba" \
  --jq '.content' | base64 -d
```

If the routing structure is unfamiliar, start with the PR diff and grep the codebase for
usages of `sign_up_view` and `signup_view`.

---

## Process Specification

For concern 6 (dead code):
- Locate the route table / router definition
- Enumerate which identifier routes to `/signup`
- Check whether any route references `sign_up::sign_up_view`
- If unreachable: is the module a stub in progress (expected dead code) or an accidentally
  dead exported function that should be removed or wired?

For concern 7 (scope):
- Read the `hydrate.rs` diff (or full file) and count the EventKind variants before and after
- Assess whether the new variants are used by the public timeline feature or are general
  framework additions
- Read `static_event_kinds()`: what does it return? How is it used?
- Determine whether `static_event_kinds()` must stay in sync with the `EventKind` enum by hand,
  or whether it is derived from the enum (e.g., via iteration, strum, or compile-time assertion)
- If manual sync is required: assess the correctness risk and whether a guard exists

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| Filename | `FINDINGS.md` |
| Format | Markdown |
| Location | `spoke-code-health/` (this workspace) |

Structure: per `../contracts/findings_schema.md`.

---

## Success Criteria

- Concerns 6 and 7 each appear in the Clean Account
- For concern 6: definitive verdict on reachability of `sign_up::sign_up_view` from any live route
- For concern 7: verdict on whether `hydrate.rs` changes are causally related to the feature,
  and on the sync risk of `static_event_kinds()` vs. the `EventKind` enum
- Severity assigned and justified for each finding
- No internal infrastructure details in any finding

---

## Suggested Methodology Files

Domain Mapping match: **Code review** → Primary: `Code Review`, Supporting: `Core`, `Code Quality`

Specific files:
- `code-review/CodeReview_Checklist_Methodology.md` — the "what isn't there" and dead-code rows
- `code-quality/Framework_Clean_Code_Methodology.md` — dead exports, unnecessary scope expansion
- `code-review/CodeReview_Process_Methodology.md` — reading for what the change touches beyond
  its own stated lines (the `hydrate.rs` framework refactor is exactly this pattern)

These are suggested starting points; load fewer if inapplicable, more if needed.

## Out-of-Scope Methodologies

- `testing/` bundle — test depth is handled by `spoke-tests`
- `security/` bundle — error safety is handled by `spoke-safety-idiom`
- `synthesis/` bundle — belongs to `spoke-synthesis`

## Inherited Constraints

- Findings point at repository file paths and line numbers at pinned commit
  `decb6196c2c1e6ed421d393a642f0c844cc333ba`; no host paths, private IPs, or infrastructure details
- Do not post to the PR
- Prose in FINDINGS.md must pass the plain-voice bar in `../contracts/findings_schema.md`
- Repository: `Nousix-LLC/nswe-demo` only
