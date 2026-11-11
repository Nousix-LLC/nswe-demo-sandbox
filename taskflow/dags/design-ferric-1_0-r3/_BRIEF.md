# _BRIEF.md — design-ferric-1_0-r3

## Objective

Review PR#128 (`design: Ferric 1.0 framework design`) as a product design document.

This is a design PR review: evaluate the design for product completeness and coherence, not code. Post the review to the PR and produce a root `SYNTHESIS.md` with an APPROVE or REQUEST-CHANGES verdict.

## Target

**PR**: https://github.com/Nousix-LLC/nswe-demo/pull/128  
**Branch**: `work/design-ferric-1_0`  
**Head SHA**: bbdeb480aacda3a20b3fdc582f235806ce3ee310  
**Design location**: `design/ferric/` in the repository (14 files)

**Design document inventory** (all under `design/ferric/`):

| File | Concern |
|---|---|
| `README.md` | Design index and navigation |
| `scope-and-requirements.md` | Framework scope, users, 1.0 requirements (REQ-FW-*), MVP-vs-1.0 line, out-of-1.0 list |
| `ssr-hydration.md` | SSR via Axum + hydrate-without-re-render architecture — the 1.0 must-have (REQ-SSR-*) |
| `authoring-model.md` | `view!` macro, props, children, slots, context (REQ-API-*) |
| `async-forms-events.md` | Async resources, suspense, forms, two-way binding, DOM events |
| `router-and-http.md` | Client-side router (History API) + HTTP/JSON client |
| `docs-and-dx.md` | API docs, examples, tutorial, starter template, README, troubleshooting |
| `performance-and-benchmark.md` | Bundle size, dependency footprint, js-framework-benchmark |
| `release-and-distribution.md` | crates.io metadata, semver, changelog, versioning policy |
| `release-bar.md` | The concrete, testable 1.0 release bar |
| `release-plan.md` | Wave/ordering plan for the epic work |
| `contracts/_MANIFEST.yaml` | Contract manifest |
| `contracts/design_artifact_map.yaml` | Maps requirements to design artifacts and issues |
| `contracts/id_and_traceability_schema.yaml` | ID and traceability schema |

**Issues filed**: #129–#164 (36 issues: 8 epics + 28 feature issues, now on the board as Todo)

**Goal this design serves**: Issue #114 — "Directive: design and build Ferric to a 1.0 framework, with server-side rendering"

**Existing foundation** (already landed):
- `ferric-foundation` (#4): Cargo workspace, ferric core, fine-grained signals, virtual DOM, `view!` macro
- `ferric-router` (#5): Client-side router (History API)
- `ferric-http` (#6): Fetch-based HTTP/JSON client
- `chirp` app: functioning SPA with durable persistence (PR#113, awaiting landing)

## Review concerns

Evaluate each concern distinctly and report findings by concern:

1. **Completeness against the directive and a releasable framework**  
   Does the design cover what issue #114 calls for and what a 1.0 Rust/Wasm UI framework with SSR must include to be a product someone can build with? Are the must-have capabilities (SSR+hydration, authoring model, async, routing) fully designed? Are there obvious gaps — capabilities the framework would need for the bar to be met that are not covered by the design documents or the issued tickets?

2. **Release bar: concrete and testable**  
   Is `release-bar.md` a testable, specific bar (an executable acceptance checklist) or a high-level aspiration? Can each bar item be mechanically verified? Is any dimension of the release bar left unadjudicated (e.g. performance, DX, correctness)?

3. **Internal coherence and traceability**  
   Do the requirements (`scope-and-requirements.md`), the design artifacts, the contracts (`design_artifact_map.yaml`, `id_and_traceability_schema.yaml`), and the issued tickets (#129–#164) agree with each other and trace back to the requirements? Does every REQ-* ID in the requirements appear in the artifact map? Does every epic and feature ticket trace to a requirement? Are there requirements with no corresponding ticket?

4. **Buildability on the existing foundation**  
   Is the design coherent with the already-landed ferric-foundation, ferric-router, and ferric-http? Does the SSR/hydration architecture (`ssr-hydration.md`) make sound assumptions about what is already in the codebase and what needs to be built? Are there any design decisions that would require rewriting existing landed work?

5. **Ticket quality and wave plan**  
   Do the 36 issued tickets (#129–#164) represent a buildable, ordered work plan? Does `release-plan.md` give a coherent wave/dependency ordering? Are the "usable_early" epics (#129–#132) genuinely independent of SSR (#133)?

## Declared output

1. **A review comment posted to PR#128** carrying the verdict (APPROVE or REQUEST-CHANGES), a per-concern breakdown of what was checked and found, and the findings with severity (BLOCKING / non-blocking). No host paths, taskflow internals, or internal addresses in the posted review.

2. **A root `SYNTHESIS.md`** (at `taskflow/dags/design-ferric-1_0-r3/SYNTHESIS.md`) with:
   - Verdict: APPROVE or REQUEST-CHANGES
   - Per-concern findings with severity and block/non-block classification
   - Link to the posted review comment on PR#128
   - Summary of non-blocking findings that become board issues

3. **Non-blocking findings filed as backlog issues** on the board, linked to PR#128 and labelled appropriately. Blocking findings go into the posted review; the overseer will remediate blockers before landing.

## Acceptance criteria

- Every concern above is evaluated distinctly in `SYNTHESIS.md` and in the posted review.
- The verdict is an explicit APPROVE or REQUEST-CHANGES.
- Blockers are identified specifically (which document, which requirement, what is missing or wrong).
- Non-blocking findings are filed on the board as issues with labels and links.
- Nothing in the posted review or filed issues names host paths, taskflow internals, or internal network addresses.
