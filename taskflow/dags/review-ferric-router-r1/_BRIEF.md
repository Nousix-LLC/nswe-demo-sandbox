# _BRIEF.md — review-ferric-router-r1

**Task kind**: Review DAG (swe-reviewer)
**Objective**: Review PR #192 (`feat(ferric-router): nested routes, replace navigation, active links`) for
correctness, code quality, test coverage, security, Rust idioms, and API/contract stability.

---

## Target

**PR**: https://github.com/Nousix-LLC/nswe-demo/pull/192
**Branch**: `work/ferric-router-r1` → `main`
**Head commit**: `2bf76698c474fb60ca663f6cd074845600caea93`
**CI run**: 41778305739 — all 6 checks SUCCESS (fmt, clippy, test, wasm, doc, image)

**Code DAG verdict**: PASS (ferric-router-r1 `SYNTHESIS.md` at
`taskflow/dags/ferric-router-r1/SYNTHESIS.md` in `Nousix-LLC/nswe-demo`).

---

## Issues and acceptance criteria

This PR closes three issues. The review holds the change to all three:

### Issue #131 — `navigate_replace` / REQ-RT-003

- `navigate_replace(path: &str)` is exported from the ferric prelude alongside `navigate(path)`.
- On `cfg(target_arch = "wasm32")` the implementation calls `history.replaceState` (no new history entry,
  no history growth).
- After calling `navigate_replace`, `current_path()` reflects the new path reactively (signals updated).
- Tests for both native and wasm32 targets are present and cover the replace semantics.

### Issue #146 — Active-link awareness / REQ-RT-007

- `Link::build()` reads `current_path()` at render time and conditionally emits `aria-current="page"` when
  the link's href matches the current path.
- An inactive link has no `aria-current` attribute (not present, not empty).
- The frozen `link()` function signature is unchanged from what the router's initial API committed
  (issue #5 contract surface).

### Issue #147 — Nested routes / REQ-RT-005

- `RoutePattern::match_prefix(path)` exists and returns a prefix-match result with the remaining suffix
  correctly stripped.
- `Router::nest(prefix, layout, child_builder)` exists: a prefix-matched route that renders the layout
  around the result of routing the suffix through the child builder.
- `Router::outlet()` tries nested routes first, then flat routes; if a nested prefix matches, the nested
  router handles the remainder.
- Per-level fallback is defined: a prefix-match failure falls through to flat routes at the same level
  before giving up.
- Existing flat-route behaviour is preserved exactly (regression test or proof-by-inspection).

---

## Design reference

**`design/ferric/router-and-http.md`** (Part 1, REQ-RT-001..008) in `Nousix-LLC/nswe-demo` on `main`
(merged with PR #128). The review holds the implementation to these requirements; discrepancies between the
code and the design are correctness findings.

---

## Review concerns

Each concern is a distinct axis of evaluation. Report each one's findings separately, with what was checked
and what was found, whether the concern is PASS or whether it has findings, and the severity of each finding.

### 1. Correctness

Does the change do what the three acceptance criteria and the design (REQ-RT-001..008) say?

- Each of the three issues: are the specified behaviours present, correct, and complete?
- Edge cases: empty path, root `/`, trailing slash, path with query string passed to `navigate_replace`.
- Error paths: what happens when `history.replaceState` is unavailable or throws; what happens when no route
  matches a nested prefix.
- Reactive invariants: does `current_path()` update consistently after `navigate_replace`; is there a
  race between route matching and signal update?
- Contract surface: the five identities from the code DAG's SYNTHESIS.md (prelude exports,
  `navigate` / `navigate_replace`, `Link::build`, `RoutePattern::match_prefix`, `Router::nest`) must be
  present and match the declared signatures.

### 2. Code quality

- Responsibility boundaries and coupling between the router, signal layer, and the history/wasm32 abstraction.
- Abstraction choices: is the split between `RoutePattern`, `Router`, and `Link` coherent; is there
  unnecessary duplication?
- Naming clarity and function/struct sizes.
- Error-handling style: panics vs. `Result`, especially in the wasm32 path.
- Whether the change leaves the router code simpler to extend (new route types, new navigation variants).

### 3. Test coverage

- Are there tests for each of the three acceptance criteria (not just happy paths)?
- Native and wasm32 test targets: does `navigate_replace` have tests under both?
- Edge cases from concern 1: which are tested, which are absent, and whether the absent ones are a gap.
- Do the tests assert real behaviour (the signal value, the aria attribute presence and absence, the
  prefix-stripped path) or do they pass vacuously?
- Coverage of the per-level fallback and the flat-route regression.

### 4. Security

- No `unsafe` blocks introduced without necessity and documentation.
- Event-handling safety in the wasm32 path: closure captures, dropped event listeners, potential
  use-after-free in JS/WASM interop.
- No host-specific or infrastructure detail committed (absolute host paths, internal network addresses such as
  Tailscale `100.x` IPs, internal server URLs, host runtime or taskflow directory paths).
- Nothing the diff pulls in that expands the trust surface.

### 5. Rust idioms

- Lifetime annotations, borrow patterns, and ownership are idiomatic.
- Trait implementations (any `Display`, `From`, `PartialEq`, etc.) are complete and consistent.
- Use of `cfg` attributes for platform branching follows the crate's existing convention.
- No new clippy lints introduced beyond what CI already passes.

### 6. API/contract stability

- The frozen surface from issue #5 (the router's initial API) is not broken: `link()`, `navigate()`, and the
  `Router`/`RoutePattern` public API as it existed before this PR are unchanged or only additive.
- The prelude exports before this PR remain intact; the new additions (`navigate_replace`,
  `RoutePattern::match_prefix`, `Router::nest`) are purely additive.
- Nothing in `crates/chirp-frontend` or `crates/chirp-types` or `crates/chirp-server` is broken by the
  router's new API surface.

---

## Declared output

1. **Posted GitHub review** on PR #192 — an APPROVE or REQUEST-CHANGES review comment carrying the verdict
   and all findings per concern, with file/line references for each finding. If the platform does not allow
   posting as an approval (author and reviewer same account), post as a comment carrying the verdict explicitly.
   The review is written for the repository's readers: file and line references in the repository, no host
   paths or internal infra detail, no mention of DAG internals.
2. **Non-blocking findings** filed as GitHub issues on `Nousix-LLC/nswe-demo`, grouped and de-duplicated
   against the board, linked to PR #192 and the relevant issue. Each filed as a backlog issue.
3. **Root `SYNTHESIS.md`** at the DAG root (`taskflow/dags/review-ferric-router-r1/SYNTHESIS.md`) carrying:
   - Overall verdict: APPROVE or REQUEST-CHANGES.
   - Per-concern summary: what was checked, what was found, severity of each finding, and whether it blocks.
   - List of blocking findings (if any) with how each maps to an acceptance criterion.
   - List of non-blocking findings and the issue numbers filed for them.
   - Concerns the review did not cover (if any), with the reason.

---

## Constraints

- Repository: `Nousix-LLC/nswe-demo` only. Do not push commits or open PRs in any other repo.
- Read-only outside the declared output: the review reads and judges; it does not change the branch.
- No force-push to `main` or to `work/ferric-router-r1`.
- Nothing in the declared output names host paths, Tailscale IPs, internal server addresses, or the
  DAG/taskflow directory structure.
