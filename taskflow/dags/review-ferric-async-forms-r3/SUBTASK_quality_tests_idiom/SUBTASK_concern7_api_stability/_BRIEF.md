# Task: Concern 7 — API and Contract Stability Review, PR #193

## Task Specification

**Slug**: SUBTASK_concern7_api_stability
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-reviewer

### Objective

Review API surface changes and contract stability in the four files changed by PR #193's remediation commits — verifying that existing callers of `EventHandler` are not broken, that the new `on_input_event_handler()` method and `create_resource` function follow established conventions and are documented, and that no public API invariant is violated. Produce a `partial_findings.md` conforming to the shared findings contract.

### Context

Part of the PR #193 concerns 2/3/6/7 subtree. See `../_GLOBAL.md` for full context, shared inputs, and inherited constraints. The contract for the output format is at `../contracts/findings_format.md`.

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree context | `../_GLOBAL.md` | Inherited constraints, shared inputs, scope |
| Findings contract | `../contracts/findings_format.md` | Required output schema |
| PR #193 diff | `gh pr diff 193 --repo Nousix-LLC/nswe-demo` | Changed lines |
| async_resource.rs | `crates/ferric/src/async_resource.rs` | create_resource API |
| vdom.rs | `crates/ferric/src/vdom.rs` | EventHandler enum, on_event API |
| dom.rs | `crates/ferric/src/dom.rs` | Dispatch logic |
| form.rs | `crates/ferric/src/form.rs` | Bind::on_input_event_handler API |

---

## Review Scope

Examine the following for Concern 7 (API and contract stability):

1. **`EventHandler` backward compatibility**: `EventHandler` is a public type. The enum redesign (adding a `NoArg` wrapper and an event-carrying variant) must preserve the existing public API surface. Verify that existing callers passing `impl Fn()` to `VElement::on_event()` still compile unchanged — the `NoArg` wrapper should be transparent to them through a `From` or `Into` impl (or equivalent). Check whether the transition is covered by a type alias, blanket impl, or explicit conversion.

2. **`on_input_event_handler()` on `Bind<T>`**: Does this new method extend the public API cleanly? Is it documented (at minimum a doc comment explaining what it does and its relationship to `create_resource`)? Does its signature follow the library's established naming conventions for handler-registration methods?

3. **`create_resource` naming and conventions**: Does `create_resource` follow the library's established naming patterns for constructors/factories? Is it appropriately documented? Is the generation counter's role in its contract communicated to callers (even briefly)?

---

## Output Specification

**Primary Output:** `partial_findings.md` at this task's workspace root

Must conform to `../contracts/findings_format.md`: two required sections (`## Findings` and `## What was examined`), using `concern: api-stability`, severity values from {`blocker`, `non-blocker`, `clean`}, repository-relative locations.

---

## Suggested Methodology Files

Task type row (Domain Mapping): **Ferric PR review (Rust library)** → Primary: `code-review`, Supporting: `rust`, `framework-design`

Specific files flagged for this concern:

- `code-review/CodeReview_Checklist_Methodology.md` — code review checklist; API surface checks are a standard review gate. Rationale: provides the structural frame for evaluating API changes in a review.
- `rust/Rust_Library_API_And_Stability_Methodology.md` — Rust library API semver, backward compatibility constraints, `From`/`Into` impls as compatibility bridges, public type invariants. Rationale: this concern is precisely about whether the `EventHandler` redesign is semver-safe for existing callers, which this methodology covers directly.
- `framework-design/FrameworkDesign_Library_API_Design_Methodology.md` — API invitability, naming conventions, documentation as contract. Rationale: `on_input_event_handler()` and `create_resource` are new public API surface; this methodology covers whether they meet the bar for clean library additions.

These are SUGGESTIONS. Load fewer if some are clearly inapplicable; load more if your reading of the files reveals additional methodology surface needed.

## Inherited Constraints

- Repository-relative paths only in all findings
- Issues #196–#201 MUST NOT be re-raised
- Severity `blocker` if `EventHandler` redesign breaks existing callers (a broken public API is a contract violation); `non-blocker` for missing documentation or naming inconsistencies
- Concerns 1, 2, 3, 4, 5, 6 are out of scope — focus only on Concern 7 (API and contract stability)

## Success Criteria

- `EventHandler` backward compatibility specifically verified against existing caller patterns
- `on_input_event_handler()` and `create_resource` evaluated for documentation and naming conventions
- `partial_findings.md` produced with `## Findings` and `## What was examined` sections
- API backward compatibility verdict (compatible / breaking) explicitly stated
