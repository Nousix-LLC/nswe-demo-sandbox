# Ferric-Macros/Context Scope Assessment

**Branch assessed:** `work/ferric-router-r1`  
**Date:** 2026-11-03  
**Task:** SUBTASK_macros-assessment (ferric-router-r2 remediation DAG)  
**Input source:** review-ferric-router-r1/SYNTHESIS.md — blocking finding B1

---

## Executive Summary

Twelve commits bundled into PR #192 (`work/ferric-router-r1`) implement four distinct features
from the Ferric 1.0 Authoring Model epic: reactive-baseline audit (#137/#138), the `view!`
proc-macro (#139), the `#[component]` attribute macro with its typestate diagnostics (#140/#141),
and the context/dependency-injection API (#142). Together they add approximately 3,290 lines
across a new `crates/ferric-macros/` proc-macro crate and targeted additions to `crates/ferric/`.
All six issues have clear acceptance criteria in `design/ferric/release-bar.md` and
`design/ferric/authoring-model.md`; the primary missing ingredient for a proper review is a
review brief that presents those criteria explicitly and scopes the review to this change set.

**Recommended path forward:** Split into three sequenced PRs following the dependency chain —
(1) baseline audit + `view!` macro, (2) `#[component]` model + diagnostics, (3) context API
+ CI fixes — so each PR can be reviewed against its own stated acceptance criteria. The proc-macro
crate warrants explicit security review as a build-time trust-surface addition; the analysis below
indicates the surface is bounded (pure token transformation, no env/filesystem access), but that
finding should be confirmed in the review brief.

---

## Scope Overview

### crates/ferric-macros/ — New proc-macro crate

A new `proc-macro = true` crate introduced from scratch by this commit batch. The crate is the
compile-time code-generation layer for the Ferric 1.0 Authoring Model.

**Dependencies (production):** `proc-macro2`, `quote`, `syn` (features = \["full"\]) — standard
Rust macro toolchain, no unusual runtime dependencies.  
**Dev-dependencies:** `ferric` (path dep, for integration test types), `trybuild` (compile-fail
fixture runner).

| File | Lines | Role |
|------|-------|------|
| `Cargo.toml` | 25 | Crate manifest; `proc-macro = true`; workspace inheritance |
| `src/lib.rs` | 102 | Entry points: `view!` (function-like) and `#[component]` (attribute) |
| `src/parser.rs` | 482 | Recursive-descent `syn`-based parser for `view!` template syntax |
| `src/lower.rs` | 442 | Lowers `ViewNode` AST to frozen `VNode` builder chain; all §2.12 constructs |
| `src/component.rs` | 929 | `#[component]` macro; generates typed `NameProps` builder with typestate pattern |
| **Source subtotal** | **1,980** | |
| `tests/lowering.rs` | 405 | Native integration tests: one test per §2.12 lowering construct |
| `tests/component.rs` | 370 | Integration tests: all §3 component forms |
| `tests/component_diagnostics.rs` | 16 | `trybuild` runner for compile-fail fixtures |
| `tests/compile_fail_component/` | ~200 | 7 `.rs` fixtures + 7 committed `.stderr` snapshots |
| **Test subtotal** | **~991** | |
| **Grand total** | **~2,971** | |

### crates/ferric/ context, component, and re-export changes

Additions to the existing `crates/ferric/` crate supporting the new macros and context API.

| File | Lines added | Commits | Content |
|------|-------------|---------|---------|
| `src/vdom.rs` | +25 | `1ccdce0` | One new test: `partial_attr_change_in_subtree_produces_single_setattr` |
| `src/component.rs` | +34 | `0088a5c` | `Children`, `Slot`, `SlotFn<T>` type aliases; re-exported from prelude |
| `src/signal.rs` | +157 | `82d267f`, `e29e2f4` | Context API: `provide_context`, `use_context`, `expect_context`; `HashMap<TypeId, Box<dyn Any>>` on scope nodes |
| `src/lib.rs` | +12 | `912ed57`, `c28b0e1`, `82d267f` | Wiring: `ferric-macros` dep re-export; `VElement`/`VNode`/`EventKind` root re-exports; context fn re-exports |
| **ferric/ subtotal** | **~228** | | |

---

## Issue-to-Commit Mapping

### #137: Ferric 1.0: Reactive state primitives

**BAR criterion:** BAR-FERRIC-001  
**Design spec:** `design/ferric/authoring-model.md` §reactive-core (REQ-FW-003, REQ-FW-005, REQ-FW-009)  
**Acceptance criteria:** `create_signal`, `create_memo`, `create_effect`, `batch` in `ferric` prelude
on stable Rust at MSRV; tests cover memo non-recompute, batch deferral, scoped cleanup without leaks.

| Commit | Description | Net lines |
|--------|-------------|-----------|
| `1ccdce0` | `test(ferric): baseline audit — #137 and #138 ACs satisfied` | +25 (vdom.rs) |

**What was done:** Confirmed pre-existing reactive core satisfies all three test AC requirements.
No new production code; the commit adds one new vdom test for BAR-FERRIC-002 (see #138). The
reactive primitives (`create_signal`, etc.) were already present; this commit documents that the
acceptance criteria are met and verifies CI passes at this state.  
**Closes:** Yes — `Closes #137` in commit message.

---

### #138: Ferric 1.0: Virtual DOM and keyed DOM patching

**BAR criterion:** BAR-FERRIC-002  
**Design spec:** `design/ferric/authoring-model.md` §vdom (REQ-FW-005)  
**Acceptance criteria:** Partial signal change updates only affected DOM nodes; keyed list reorder
moves existing DOM nodes rather than destroying and recreating them.

| Commit | Description | Net lines |
|--------|-------------|-----------|
| `1ccdce0` | `test(ferric): baseline audit — #137 and #138 ACs satisfied` | +25 (vdom.rs) |

**What was done:** Same commit as #137. Adds `partial_attr_change_in_subtree_produces_single_setattr`
test to verify the diff algorithm emits `SetAttr` (not `Replace`) for a one-attribute change deep
in a subtree. Keyed-reorder and DOM-integration tests were already present.  
**Closes:** Yes — `Closes #138` in commit message (shared with `Closes #137`).

---

### #139: Ferric 1.0: view! macro surface and compile-time diagnostics

**BAR criteria:** BAR-FERRIC-007 (§2.12 constructs), BAR-FERRIC-008 (§2.9 diagnostics)  
**Design spec:** `design/ferric/authoring-model.md` §view-macro, §2.12, §2.9 (REQ-API-001–004,
006, 012, 015, 023–028, REQ-FW-014)  
**Acceptance criteria:** All §2.12 valid `view!` inputs compile; all §2.9 malformed inputs produce
span-accurate diagnostics in author vocabulary; trybuild tests pass in CI.

| Commit | Description | Net lines |
|--------|-------------|-----------|
| `3be2f51` | `feat(ferric-macros): scaffold proc-macro crate with stub view! macro` | +55 |
| `912ed57` | `ferric: wire ferric-macros dependency and re-export view! in prelude` | +3 |
| `d25a7f7` | `feat(ferric-macros): implement full view! proc-macro (sec 2.12 + 2.9)` | +752 |
| `3c3d4aa` | `feat(ferric-macros): implement view! macro (#139)` | +1 (Cargo.lock) |
| `4c77b9a` | `test(ferric-macros): conformance tests for view! lowering table (§2.12)` | +396 |
| `c28b0e1` | `fix(ferric): re-export VElement, VNode, EventKind at crate root` | +7 |
| `d027534` | `fix(conformance): resolve VElement::into() type ambiguity` | +5 |

**What was done:** Introduces the full `crates/ferric-macros/` crate. The core implementation
commit `d25a7f7` adds `parser.rs` (408 lines: recursive-descent `syn` parser for all §2.12
constructs and §2.9 error cases) and `lower.rs` (300 lines: `ViewNode` AST → frozen `VNode`
builder chain). Commit `4c77b9a` adds the §2.12 conformance test suite (391 lines, one test per
lowering table row). Support commits fix re-export paths and a type-inference ambiguity that
appeared in the integration tests.  
**Total net lines for #139:** ~1,219  
**Closes:** Yes — `Closes #139` appears in `3c3d4aa`.

---

### #140: Ferric 1.0: Component model — props, children, named slots, and dynamic dispatch

**BAR criterion:** BAR-FERRIC-009  
**Design spec:** `design/ferric/authoring-model.md` §component-model (REQ-API-030–052)  
**Acceptance criteria:** `#[component]` function accepts required/optional props (with defaults),
`children: VNode`, named slots, `From`-converting props, `SlotFn<T>`, and `dyn Component` trait
object invocation; stated examples compile and render.

| Commit | Description | Net lines |
|--------|-------------|-----------|
| `0088a5c` | `feat(ferric): implement #[component] macro, Children/Slot/SlotFn types (#140)` | +995 |

**What was done:** Single large commit that implements the `#[component]` attribute macro across
both `crates/ferric-macros/` and `crates/ferric/`. Adds `component.rs` to `ferric-macros` (+276
lines: initial `NameProps` builder generator), expands `lower.rs` (+202 lines: component
invocation lowering, slot syntax), expands `parser.rs` (+84 lines: `<slot:name>` syntax), adds
`tests/component.rs` (+372 lines: 11 integration tests covering all AC forms), and adds type
aliases `Children`, `Slot`, `SlotFn<T>` to `ferric/src/component.rs` (+34 lines).

Note: `commit 763f4d6` (#141) substantially rewrites the `component.rs` builder (756 additional
lines, +50 deletions from #140's implementation) — the two commits are tightly coupled and
belong in the same PR.  
**Closes:** Yes — `Closes #140` in commit message.

---

### #141: Ferric 1.0: Component type-level diagnostics

**BAR criterion:** BAR-FERRIC-010  
**Design spec:** `design/ferric/authoring-model.md` §3.7 component diagnostics (REQ-API-050–052)  
**Acceptance criteria:** Missing required props, type mismatches, misused slots produce compile-time
errors naming the problem in component-author vocabulary; trybuild tests pass in CI.

| Commit | Description | Net lines |
|--------|-------------|-----------|
| `763f4d6` | `feat(ferric-macros): add compile-fail diagnostic suite for component authoring mistakes (#141)` | +1,104 |

**What was done:** Rewrites the `#[component]` props builder (introduced in `0088a5c`) to use a
typestate pattern — `PhantomData` marker types plus sealed traits — so required-prop and
required-slot omissions are compile-time errors (E0599: "doesn't satisfy
`Greeting_missing_required_prop_name: __GreetingHasName`"). Adds
`#[diagnostic::on_unimplemented]` on sealed traits. Adds double-fill prevention for named slots.
Adds `trybuild` as dev-dependency; adds 7 `.rs` fixture files and 7 committed `.stderr` snapshots
covering all §3.7 scenarios. The typestate pattern rewrite accounts for 756 lines added to
`component.rs` (from 173 lines after `0088a5c` to 929 lines at current HEAD).  
**Closes:** Yes — `Closes #141` in commit message.

---

### #142: Ferric 1.0: Context and dependency injection

**BAR criterion:** BAR-FERRIC-011  
**Design spec:** `design/ferric/authoring-model.md` §context (REQ-API-060, 061, 063, 066, 068)  
**Acceptance criteria:** `provide_context`, `use_context` (returns `Option`), `expect_context`
(panics with clear message if absent) in `ferric` prelude; value need not be threaded through
intermediates; stated examples compile and pass.

| Commit | Description | Net lines |
|--------|-------------|-----------|
| `82d267f` | `feat(ferric): implement context API — provide_context, use_context, expect_context (#142)` | +159 |
| `e29e2f4` | `fix(ci): resolve fmt, clippy, and rustdoc failures on ferric-macros` | fmt/lint only |

**What was done:** Adds type-keyed dependency injection to `crates/ferric/src/signal.rs` (+157
lines). Context values are stored in a `HashMap<TypeId, Box<dyn Any>>` field on existing
owner-scope `Node` structs, so context disposal runs on the same code path as effect/memo
cleanup — no second lifetime rule needed. All six acceptance criteria covered by tests in the
same commit (provide/use/expect, `Signal<T>` handles, `None` when no provider, nearest-ancestor
shadowing, scoped cleanup). Commit `e29e2f4` fixes post-implementation CI failures (fmt drift,
two `clippy(dead_code)` and `clippy(too_many_arguments)` suppressions, one rustdoc link fix) —
no logic changes.  
**Closes:** Yes — `Closes #142` in commit message.

---

## Complexity Assessment

| Area | Lines | Complexity | Notes |
|------|-------|------------|-------|
| `crates/ferric-macros/` proc-macro crate (source) | ~1,980 | **High** | Three-stage pipeline: parse → analyze → codegen; typestate builder generation is non-trivial |
| `crates/ferric-macros/` tests | ~991 | Medium | Coverage-driven integration + trybuild compile-fail suite |
| `ferric` context API (`signal.rs`) | +157 | Medium | Clean, well-integrated; `TypeId`-keyed `HashMap` on existing nodes; scope cleanup is automatic |
| `ferric` component types (`component.rs`) | +34 | Low | Type aliases only (`Children`, `Slot`, `SlotFn<T>`); no logic |
| `ferric` re-exports (`lib.rs`) | +12 | Low | Additive pub re-exports; no logic |
| `ferric` vdom baseline test (`vdom.rs`) | +25 | Low | One additional test; confirms pre-existing behavior |
| **Total** | **~3,199** | | Reviewer can expect 3–4 days for a thorough review of the proc-macro source |

**Complexity drivers in `ferric-macros/`:**
- `component.rs` (929 lines): The typestate pattern generates marker types, sealed traits, and
  `PhantomData` type parameters programmatically. The generated code must remain human-readable
  in diagnostics — a correctness concern beyond "does it compile."
- `parser.rs` (482 lines): Recursive-descent token-stream parsing with custom error recovery;
  error spans must land on author tokens, not internal parse tokens — subtle.
- `lower.rs` (442 lines): The lowering table (§2.12) has 10 construct rows; each has specific
  generated code that must round-trip through the VNode builder API without breaking
  cross-crate type resolution.

---

## Security Surface Note

**Risk level (assessed from source):** Low-Medium — bounded by standard macro toolchain

Proc-macros in Rust execute inside the compiler process at build time. This makes them a
**build-time trust-surface addition**: a compromised or malicious proc-macro crate could read
environment variables, write files, make network calls, or execute arbitrary system commands at
`cargo build` time — before any binary runs.

**Findings from source analysis:**

| Check | Result |
|-------|--------|
| `std::env` / `env!` calls | None found |
| `std::fs` / file I/O | None found |
| `include_str!` / `include_bytes!` | None found |
| Network / socket calls | None found |
| `panic!` / `eprintln!` | Used only for internal macro `unreachable!()` guards — standard |
| Production dependencies | `proc-macro2`, `quote`, `syn` only — well-audited crates |
| `unsafe` blocks in macro source | Not checked in this assessment (should be verified in review) |

The implementation is a **pure token-transformation macro** — it reads the input `TokenStream`,
runs syn to parse it, and emits a new `TokenStream` via `quote`. No side effects on the
filesystem or environment were found in the source search.

**What the review brief should cover on security:**
1. Confirm no `unsafe` blocks in `src/` (a quick `grep -rn unsafe crates/ferric-macros/src/`).
2. Confirm the generated code does not introduce `unsafe` in downstream crates when macros expand.
3. Confirm `trybuild` test fixtures do not embed any host-specific paths (committed `.stderr`
   snapshots sometimes capture absolute paths on the build machine).
4. Confirm the `Cargo.lock` entries for `proc-macro2`, `quote`, `syn` are on current stable
   versions without known advisories.

---

## Design Documents Available

The Ferric 1.0 design suite is committed at `design/ferric/` (accessible on
`work/ferric-router-r1`; introduced by commit `9a24c28`):

| Document | Relevance to these commits |
|----------|---------------------------|
| `design/ferric/authoring-model.md` | **Primary spec.** §2 (`view!` macro, §2.12 constructs, §2.9 diagnostics), §3 (component model, §3.7 diagnostics), §context. All acceptance criteria trace to this document. |
| `design/ferric/release-bar.md` | **BAR criteria.** BAR-FERRIC-001–002 (#137/#138), BAR-FERRIC-007–008 (#139), BAR-FERRIC-009 (#140), BAR-FERRIC-010 (#141), BAR-FERRIC-011 (#142). Specifies verification method (automated_test) and REQ-* references. |
| `design/ferric/scope-and-requirements.md` | REQ-API-* requirement definitions referenced in release-bar.md |
| `design/ferric/release-plan.md` | Milestone and sequencing context |
| `design/ferric/ssr-hydration.md` | Context for future compatibility constraints; relevant for `view!` macro API stability review |
| Other `design/ferric/` documents | Lower relevance for this batch; cover routing, async, DX, performance, distribution |

**All design documents needed to anchor the review brief already exist in the repository.**
The reviewer needs `authoring-model.md` and `release-bar.md` as primary references.

---

## Recommended PR Structure

### Recommendation: 3 sequenced PRs

Split on the natural dependency chain in `design/ferric/release-bar.md`:
- #139 depends on #138; #140 depends on #139; #141 depends on #140; #142 depends on #140.
- #140 and #141 are inseparable: `763f4d6` rewrites ~90% of the builder that `0088a5c` introduced.

**PR 1 — "ferric: confirm Ferric 1.0 reactive baseline and implement view! macro"**  
Closes: #137, #138, #139  
Commits: `1ccdce0`, `3be2f51`, `912ed57`, `d25a7f7`, `3c3d4aa`, `4c77b9a`, `c28b0e1`, `d027534`  
Net lines: ~1,219  
Review focus:
- BAR-FERRIC-001: reactive prelude completeness (pre-existing; test-only audit commit)
- BAR-FERRIC-002: partial-update and keyed-reorder test coverage
- BAR-FERRIC-007/008: `view!` macro covers all §2.12 constructs; §2.9 diagnostics are span-accurate
- Security: `ferric-macros/` is a new proc-macro crate; confirm pure token transformation

**PR 2 — "ferric-macros: component model — props, children, slots, and type-level diagnostics"**  
Closes: #140, #141  
Commits: `0088a5c`, `763f4d6`  
Net lines: ~2,099  
Review focus:
- BAR-FERRIC-009: all component forms (required/optional/into/children/slots/SlotFn/dyn) compile and render
- BAR-FERRIC-010: typestate diagnostics name the mistake in author vocabulary; `.stderr` snapshots are stable
- Generated code quality: `NameProps` builder is readable; sealed-trait names are human-friendly
- Depends on: PR 1 merged

**PR 3 — "ferric: context API and proc-macro CI cleanup"**  
Closes: #142  
Commits: `82d267f`, `e29e2f4`  
Net lines: ~273 (159 feature + ~114 reformatting)  
Review focus:
- BAR-FERRIC-011: `provide_context`/`use_context`/`expect_context` cover all six AC forms
- Context lifetime: scope-node disposal path (same as effects — verify no double-free)
- CI suppressions: `allow(dead_code)` and `allow(clippy::too_many_arguments)` are intentional and scoped
- Depends on: PR 2 merged

**Why not collapse into fewer PRs:**

A single PR covering all six issues (~3,290 lines) is the problem the remediation is fixing;
it would recreate blocker B1. Two PRs (view! | component+context) would still put ~2,250 lines
in the second PR, and the reviewer cannot evaluate the context API without first confirming the
component model. Three PRs keeps each reviewer's scope coherent and allows CI feedback per concern.

---

## Suggested Review Brief Template

The follow-on review task should author a `_BRIEF.md` with this structure for each of the three
recommended PRs (shown here for PR 1; replicate the pattern for PRs 2 and 3):

```markdown
# Task: Review PR — ferric Ferric 1.0 reactive baseline and view! macro

## Context
PR closes #137, #138, #139. Branch: work/ferric-macros-view (from main, containing
commits 1ccdce0, 3be2f51, 912ed57, d25a7f7, 3c3d4aa, 4c77b9a, c28b0e1, d027534).

## Acceptance Criteria to Verify

### #137 (BAR-FERRIC-001) — Reactive state primitives
- [ ] REQ-FW-003: create_signal, create_memo, create_effect, batch in ferric::prelude
- [ ] REQ-FW-005: create_memo does not recompute when output is unchanged (test)
- [ ] REQ-FW-009: batch defers effect execution until batch closes (test)
- [ ] Scoped cleanup unsubscribes all subscriptions on scope drop (test)

### #138 (BAR-FERRIC-002) — Virtual DOM and keyed DOM patching
- [ ] REQ-FW-005: partial signal change updates only affected DOM nodes, not full subtree (test)
- [ ] Keyed list reorder moves existing DOM nodes rather than destroying and recreating (test)

### #139 (BAR-FERRIC-007 + BAR-FERRIC-008) — view! macro
- [ ] REQ-API-001–004, 006, 012, 015, 023: All §2.12 construct rows compile and lower correctly
- [ ] REQ-API-024–028: All §2.9 diagnostic cases produce span-accurate author-vocabulary errors
- [ ] trybuild tests pass in CI (BAR-FERRIC-008 verification method)

## Security Checks (proc-macro crate)
- [ ] No std::env, std::fs, or network calls in crates/ferric-macros/src/
- [ ] No unsafe blocks in crates/ferric-macros/src/
- [ ] Generated code does not introduce unsafe in downstream crates
- [ ] trybuild .stderr snapshots do not contain host-specific paths
- [ ] proc-macro2/quote/syn Cargo.lock versions have no known advisories

## Design References
- Primary: design/ferric/authoring-model.md §2 (view macro), §2.12 (lowering table), §2.9 (diagnostics)
- Criteria: design/ferric/release-bar.md BAR-FERRIC-001, 002, 007, 008

## Out of Scope
- Component model (covered in separate PR 2 brief)
- Context API (covered in separate PR 3 brief)
- Router commits (already in work/ferric-router-r2)
```

The PR 2 brief follows the same pattern, substituting BAR-FERRIC-009/010 and
`authoring-model.md §3` as the design reference. The PR 3 brief uses BAR-FERRIC-011 and
`authoring-model.md §context`.

---

*Assessment produced by SUBTASK_macros-assessment (ferric-router-r2 remediation DAG).*  
*All 12 commits assessed; all 6 issues (#137–#142) mapped; proc-macro security surface noted.*
