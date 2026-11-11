# Task: Dead-Code Reachability — sign_up::sign_up_view (Concern 6)

## Task Specification

**Slug**: child-dead-code
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective

Determine whether `sign_up::sign_up_view` in `crates/chirp-frontend/src/pages/sign_up.rs` is
reachable from any live route in the application, or whether it is effectively dead code.

### Context

This task covers concern 6 from the parent spoke `spoke-code-health`. See `../_GLOBAL.md` for
PR context, the pinned commit, and subtree constraints. The parent spoke's concern assignment:

> `sign_up.rs` exports `sign_up_view` (a stub with a disabled button). The route table routes
> `/signup` to `signup_view` from `compose.rs`, not to `sign_up::sign_up_view`. Is
> `sign_up::sign_up_view` reachable from any live route? If not, is the module dead code?

**Pin commit**: `decb6196c2c1e6ed421d393a642f0c844cc333ba`

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | PR context, pin commit, constraints |
| Concern finding schema | `../contracts/concern_finding_schema.md` | Output structure |
| `sign_up.rs` | `crates/chirp-frontend/src/pages/sign_up.rs` at HEAD | The module with `sign_up_view` |
| Route table / main.rs | `crates/chirp-frontend/src/main.rs` or similar at HEAD | Router definition |
| `compose.rs` (or wherever `signup_view` lives) | `crates/chirp-frontend/src/pages/compose.rs` or similar at HEAD | Competing signup view |
| PR diff | `gh pr diff 263 -R Nousix-LLC/nswe-demo` | What changed relevant to sign_up.rs |

Access file contents via:
```bash
gh api "repos/Nousix-LLC/nswe-demo/contents/PATH?ref=decb6196c2c1e6ed421d393a642f0c844cc333ba" \
  --jq '.content' | base64 -d
```

If the routing structure is unfamiliar, start with the PR diff and grep for usages of
`sign_up_view` and `signup_view` across the frontend crate.

---

## Process Specification

Reachability investigation:
1. Read the route table (likely `main.rs` or a dedicated router file) to enumerate all route-to-handler mappings, specifically for the `/signup` path
2. Identify which identifier is used for the `/signup` route handler — `sign_up::sign_up_view` or `compose::signup_view` (or another)
3. Search the codebase for any reference to `sign_up::sign_up_view` outside the defining module
4. If `sign_up_view` appears in `sign_up.rs` but is not referenced in any route or public API, conclude it is unreachable from any live route
5. Assess whether this is a stub in progress (expected dead code with a plan to wire it) or an orphaned export with no intended caller

### Methodology

Domain Mapping match: **Code review** → Primary: `Code Review`, Supporting: `Code Quality`

Suggested methodology files:
- `code-review/CodeReview_Checklist_Methodology.md` — the "what isn't there" and dead-code rows; this concern is exactly the dead-export pattern that row targets
- `code-quality/Framework_Clean_Code_Methodology.md` — dead exports, unnecessary scope expansion

These are suggested starting points; load fewer if inapplicable, more if needed.

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| Filename | `finding_c6.md` |
| Format | Markdown |
| Location | `child-dead-code/` (this workspace) |

Structure: per `../contracts/concern_finding_schema.md`.

Required sections:
1. `## Concern 6 — sign_up::sign_up_view Dead Code`
2. `## Investigation`
3. `## Verdict`
4. `## Finding` (if unreachable from any live route — this is a code-health finding)

---

## Success Criteria

- Definitive verdict: `sign_up::sign_up_view` is reachable or unreachable from any live route
- If unreachable: a Finding entry with location (file + line at pinned commit), principle, severity, and satisfying condition
- If reachable: Investigation explains which route wires to it
- No internal host paths, private IPs, or infrastructure details
- Prose passes the plain-voice bar

---

## Suggested Methodology Files

Domain Mapping match: **Code review** → Primary: `Code Review`, Supporting: `Core`, `Code Quality`

Specific files:
- `code-review/CodeReview_Checklist_Methodology.md` — dead-code and unreachable-export rows
- `code-quality/Framework_Clean_Code_Methodology.md` — dead exports and unnecessary public surface

These are suggested starting points. The child agent is the final judge of what the work requires.

## Inherited Constraints

- Findings point at repository file paths and line numbers at pinned commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- No host paths, private IPs, or infrastructure details in any finding
- Do not post to the PR
- Prose in finding_c6.md must pass the plain-voice bar
- Repository: `Nousix-LLC/nswe-demo` only

## Out-of-Scope

- concern 7 (`hydrate.rs`) — assigned to `child-hydrate-scope`
- test depth — assigned to `spoke-tests`
- security/error safety — assigned to `spoke-safety-idiom`
