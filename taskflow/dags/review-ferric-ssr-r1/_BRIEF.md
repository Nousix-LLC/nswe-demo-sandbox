# _BRIEF.md — review-ferric-ssr-r1 (swe-reviewer)

**Goal**: Review PR #228 (`feat(ferric): SSR render_to_string + client-side hydration + Axum integration`) on
branch `work/ferric-ssr-r1` in repo `Nousix-LLC/nswe-demo`.

## What is being reviewed

PR #228 implements the Ferric SSR/hydration capability described in Ferric 1.0 epics #133–#136. It closes
issues #223, #224, and #226. It is the second remediation attempt (ferric-ssr-r3) of the ferric-ssr goal. All
six CI checks passed (fmt, clippy, test, wasm, doc, image). The PR is mergeable and clean (no conflicts).

The machine gate SYNTHESIS is at `taskflow/dags/ferric-ssr-r3/SYNTHESIS.md` (verdict: PASS).

### Issues and acceptance criteria this PR is held to

**#223 — SSR: render_to_string for static and async components**
- REQ-SSR-001: `render_to_string(component, props)` renders a ferric component tree to an HTML string on the
  server (without a DOM).
- REQ-SSR-002: Signal-driven components render from their initial signal state at render time.
- REQ-SSR-003: Child components and slot-based composition render correctly in the SSR pass.
- REQ-SSR-004: The rendered HTML includes the data-hydration-id attribute markers required for client-side
  hydration to anchor to.
- REQ-SSR-005: The function is accessible from an Axum handler (the SSR integration point).

**#224 — Hydration: `hydrate()` reattaches a live component tree to SSR-rendered HTML**
- REQ-HYD-001: `hydrate(component, props, root)` walks the existing DOM rendered by SSR, matches each
  component node to its marker, and attaches signal listeners without re-creating or replacing DOM nodes.
- REQ-HYD-002: After hydration, signal updates propagate to the DOM exactly as in a fresh client-side mount.
- REQ-HYD-003: `hydrate()` is called once from the WASM entry point and completes without error on a
  correctly SSR-rendered page.
- REQ-HYD-004: The hydration pass uses the same data-hydration-id markers the SSR pass emitted; the
  marker format is agreed and consistent between server (render_to_string) and client (hydrate).

**#226 — Mismatch detection and Axum integration**
- REQ-SSR-006: If a client-side hydration walks a node whose type or marker does not match what the SSR pass
  emitted, hydration logs a recoverable mismatch warning (does not panic) and falls back to a fresh mount for
  that subtree.
- REQ-MIS-001: The Axum integration provides a handler pattern (or example) demonstrating how to call
  render_to_string from an Axum route and return the HTML response.
- REQ-MIS-002: The Axum-rendered HTML is well-formed and contains the hydration markers the client needs.

**Non-goal — do NOT block on this**:
- #225 (REQ-SSR-007): async resource state carry across the SSR seam is blocked on issue #130 and is
  explicitly out of scope for this PR.
- Anything outside the ferric-ssr goal's scope (router integration, form submission, etc.).

### Design context

The design epics governing this work are #133 (SSR + Hydration) and the broader Ferric 1.0 framework design
(epics #133–#136, design PR #128 and its docs). The design docs are on `main` in the repository. Specifically:
- Epic #133 defines the SSR/hydration capability and the release bar items BAR-003, BAR-004, BAR-006.
- Sub-issue #224 (BAR-004) is the hydration implementation; sub-issue #226 (BAR-006) covers mismatch detection
  and Axum integration.

## Review concerns

Evaluate each of these as a distinct concern, with a named finding for each issue (or a "clean" finding if
none):

### 1. Correctness
Does the change implement the acceptance criteria for #223, #224, and #226 above — including edge cases, error
paths, and the stated non-goal boundary?

Specifically:
- Does `render_to_string` produce correct, well-formed HTML from a component tree without a DOM?
- Does `hydrate()` correctly walk and reattach to SSR-rendered HTML without re-creating nodes?
- Does the marker format (data-hydration-id or equivalent) agree between the SSR and hydration code paths?
- Does mismatch detection fire on actual structural mismatches and fall back gracefully (no panic)?
- Does the Axum integration correctly call render_to_string and return the result as an HTTP response?
- Are signal-driven re-renders correct after hydration (same behavior as a fresh mount)?

### 2. Code quality and design
- API surface and naming: are `render_to_string`, `hydrate`, and the Axum integration point named and
  positioned consistently with the rest of the ferric API (crates/ferric)?
- Abstraction boundaries: is the SSR/hydration code cleanly separated from the DOM-side rendering?
- Error handling: are errors surfaced clearly? Is `hydrate()` on a mismatched tree recoverable?
- Function size, duplication, and extensibility: does the implementation leave the code simpler to extend for
  future SSR concerns (e.g. async resources when #130 lands)?
- Test coverage: do the tests exercise each acceptance criterion, edge cases (empty component trees, nested
  children, component with no props), and the error/mismatch path? Do they assert real behavior and not vacuous
  passes?
- Doc coverage: are `render_to_string` and `hydrate` documented at the pub API level with examples or usage
  notes?

### 3. Security — HTML escaping
- Does `render_to_string` correctly escape injection characters (< > & " ') in component output, attribute
  values, and text nodes?
- Is there any path through the SSR renderer where user-supplied or dynamic content could be inserted into the
  HTML output without escaping?
- Are there any unescaped uses of format strings, raw HTML insertions, or trust boundaries that could allow
  XSS in the SSR output?

### 4. Security — host/infrastructure detail exposure
- Does the diff commit any host-specific or internal-infrastructure detail: an absolute host path, a Tailscale
  or LAN IP address (100.x, 192.168.x), an internal server URL, or a host runtime/taskflow directory path?
  (These must not appear in committed files, issues, PRs, or comments.)
- Does any added dependency pull in something that should be reviewed for supply-chain risk?

## Declared output

1. **Posted review on PR #228**: the review text with the verdict (APPROVE or REQUEST-CHANGES) and all
   findings. If the platform does not allow posting as a formal approval (same account as author), post as a
   review comment that carries the verdict and all findings. Every reviewed PR shows its review.
2. **Root `SYNTHESIS.md`** at `taskflow/dags/review-ferric-ssr-r1/SYNTHESIS.md`: the verdict (APPROVE or
   REQUEST-CHANGES), a concern-by-concern account of what was checked and what was found (clean or finding),
   the severity and block/non-block classification of each finding, and the board issues filed for
   non-blocking findings.
3. **Non-blocking findings** filed as backlog issues on the board (grouped, de-duplicated against the board,
   linked to this PR and the relevant issue they came from). These do not hold the landing but must be filed.
4. The `SYNTHESIS.md` verdict is authoritative for the landing decision (not the posted GitHub review status,
   which may be downgraded by platform same-account rules).

## Constraints

- Repository: `Nousix-LLC/nswe-demo`; branch `work/ferric-ssr-r1`; PR #228.
- Do not modify source code. The reviewer reads and judges.
- Do not comment on #225 (REQ-SSR-007) as a blocker or finding — it is an explicit non-goal for this PR.
- Findings that name lines or files point at the repository (`Nousix-LLC/nswe-demo`), not host paths or
  taskflow internals.
- Non-blockers become backlog issues; they do not hold the landing.
