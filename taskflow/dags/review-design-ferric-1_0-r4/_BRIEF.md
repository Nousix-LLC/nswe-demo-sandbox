# _BRIEF.md — review-design-ferric-1_0-r4 (swe-reviewer)

## Objective

Review PR#128 (`work/design-ferric-1_0` → `main`) on `Nousix-LLC/nswe-demo` — the Ferric 1.0 framework design — after remediation of the 5 BLOCKING findings from review `design-ferric-1_0-r3`. Issue the re-review verdict and land the PR if APPROVE.

**Config (read from overseer _CONFIG.yaml)**: `landing_authority: delegated`, `auto_land: true`, `headless: true`.

---

## Target

**PR**: #128 — "design: Ferric 1.0 framework design"  
**Branch**: `work/design-ferric-1_0` → `main`  
**Head commit**: `ade5bdde424638b9f993c5699219c638d02e0e59` — "design(ferric): remediate 5 blocking release-bar testability findings"  
**State**: OPEN, MERGEABLE, all CI green (clippy, doc, fmt, image, test, wasm all pass on run 41688826102)  
**Prior review verdict**: `design-ferric-1_0-r3` REQUEST-CHANGES — 5 BLOCKING findings in `design/ferric/release-bar.md` (Concern 2: release bar testability)  
**Remediation result**: `remediate-design-ferric-1_0-r1` SYNTHESIS.md — APPROVE; all 5 findings fixed in commit `ade5bdd`

**What the diff contains** (10 documents under `design/ferric/`):

| Document | Concern |
|---|---|
| `scope-and-requirements.md` | Framework scope, users, 1.0 requirements (`REQ-FW-*`), MVP-vs-1.0 line |
| `ssr-hydration.md` | SSR via Axum + hydrate-without-re-render architecture (`REQ-SSR-*`) |
| `authoring-model.md` | `view!` macro, props, children, slots, context (`REQ-API-*`) |
| `async-forms-events.md` | Async resources with suspense, two-way form binding, DOM events (`REQ-ASYNC-*`) |
| `router-and-http.md` | Router + HTTP/JSON client (`REQ-RT-*`, `REQ-HTTP-*`) |
| `docs-and-dx.md` | Guide, tutorial, API docs, starter template, DX bar (`REQ-DX-*`) |
| `release-and-distribution.md` | crates.io publishing, semver policy, changelog (`REQ-REL-*`) |
| `performance-and-benchmark.md` | js-framework-benchmark methodology (`REQ-PERF-*`) |
| `release-bar.md` | Consolidated `BAR-FERRIC-*` criteria — the remediated document |
| `release-plan.md` | Ordered epics + work items tracing to `REQ-*`/`BAR-*` |

Also `design/ferric/contracts/`: id and traceability schema + artifact map.

**Issues this PR closes**: none filed with Closes/Fixes keywords — it is a design PR that drives the work-item tree under epic #1 (ferric) and folded in router (#5) and http (#6) design.

---

## Remediation to verify (PRIMARY concern — confirm these blockers are fixed)

From `design-ferric-1_0-r3`, all 5 BLOCKING findings were in `release-bar.md`. The remediation commit `ade5bdd` claims to fix:

| ID | Finding | Fix claimed |
|---|---|---|
| BAR-FERRIC-001 | No version anchor for backward compat baseline (ferric core) | `v0.1.0-usable_early` git tag |
| BAR-FERRIC-003 | No sanitizer named, no assertion for HTML sanitization | `ammonia` crate + `assert_eq!(html, ammonia::clean(&html))` |
| BAR-FERRIC-006 | No observable outcome for hydration mismatch detection | `console.warn` (dev) + full re-render of subtree (prod) |
| BAR-FERRIC-015 | No version anchor (ferric-router) | `v0.1.0-usable_early` git tag |
| BAR-FERRIC-017 | No version anchor (ferric-http) | `v0.1.0-usable_early` git tag |

Verify each fix is present and sufficient: the anchor or assertion is named, specific, and a reviewer can run the check from the text alone.

---

## Review concerns

Review this PR as a **design PR** — judge the product, not code. This is a design re-review after remediation; cover the full design as well as the confirmed fixes.

### Concern 1 — Remediation verification (PRIMARY BLOCKER CHECK)
Confirm each of the 5 fixes above is present in `release-bar.md` and resolves the original finding. A fix that names an anchor but leaves the verifiability gap open is not resolved. Each fix must be specific enough for an outside reviewer to replicate the check.

### Concern 2 — Release bar completeness and testability
Beyond the 5 remediated criteria, is the release bar (`release-bar.md`) complete? Do all other `BAR-FERRIC-*` criteria name what to check and how in sufficient detail that a reviewer can determine pass/fail without open-ended interpretation? A criterion that says "adequate" or "standard" without a named test or assertion is a candidate finding.

### Concern 3 — Design coverage and product completeness
Does the set of 10 documents cover what a releasable Ferric 1.0 product of this kind calls for? Are there gaps in the SSR/hydration architecture, the component model, the async model, or the distribution plan that a builder would hit? Is the 1.0/MVP line coherent and justified?

### Concern 4 — Requirements, design, and tickets traceability
Do the `REQ-*` requirements, the design documents, and the `BAR-FERRIC-*` bar entries agree and trace back to each other? Does `release-plan.md` cover all the work needed to meet the release bar? Are the epics and work items under #1 consistent with the design?

### Concern 5 — Buildability
Is the design buildable on the existing `ferric` codebase (crates/ferric at v0.1.0-usable_early)? Does it call for primitives or interfaces that conflict with what exists? Does the SSR path require infrastructure changes beyond the existing Axum server?

### Concern 6 — Security and confidentiality
Does the diff commit any host path, tailnet address (100.x), internal URL, private credential, or taskflow-runtime path? Does any design document expose internal infrastructure details that belong only in operating config?

---

## Declared output

1. **Review posted on PR#128** — a review comment on GitHub (as an approval or comment, whichever the platform allows for this account) carrying the full findings: verdict, per-concern results, each finding with severity and whether it blocks.
2. **Root `SYNTHESIS.md`** at `taskflow/dags/review-design-ferric-1_0-r4/SYNTHESIS.md` — APPROVE or REQUEST-CHANGES verdict, findings per concern with severity, what each concern found clean, and non-blocking findings flagged for board filing.
3. **Non-blocking findings filed on the board** as backlog issues, linked to PR#128 and this review.
4. **Landing** — if APPROVE: confirm PR#128 is mergeable and all CI green, then merge it via `gh pr merge 128 --squash --delete-branch`. Update PR#128 and issues on the board to Done.

If REQUEST-CHANGES: do not land; record the blocking findings in SYNTHESIS.md for the overseer to remediate.

---

## Repo path

`Nousix-LLC/nswe-demo` — use a checkout at `taskflow/dags/review-design-ferric-1_0-r4/checkout/` (clone or reuse from the ferric-foundation checkout; read the branch `work/design-ferric-1_0`).

---

## Governing guidance

`appfiles/REVIEW_GATE.md` governs this review (loaded by this DAG at boot — no need to load it from the brief).
