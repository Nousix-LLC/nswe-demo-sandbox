# Task: Ferric 1.0 — framework scope & 1.0 requirements (concern 1)

## Task Specification
**Slug**: SUBTASK_scope_and_requirements
**Task Kind**: standard
**Status**: Pending

### Objective
Establish the foundation every other Ferric 1.0 design concern traces back to: who uses Ferric and what they
must be able to build with it, what a credible 1.0 of a Rust/WASM UI framework must provide (as testable
requirements and acceptance criteria), the explicit **MVP-vs-1.0 line**, and the explicit **out-of-1.0 list**.
State what the framework must do and judge "done" from an app author's side — **what, not how.**

### Context
Part of the Ferric 1.0 framework design (see `../_GLOBAL.md`). This is the requirements spine: it owns the
`REQ-FW-*` register and sets the cross-cutting frame the capability spokes (SSR, authoring, async, router/http,
docs/DX, release, performance) specialize into their own area registers. You do not design each capability in
depth — you set the requirements and the 1.0 line they all answer to.

**Dependencies**: none. **Dependents**: every capability spoke, the release bar, and the release plan.

### Distinct concerns to cover (name them; let your own evaluation decide how to split)
- **Users & what they build**: the Rust/WASM application authors Ferric is for; the kinds of app a 1.0 must let
  them build; where Ferric sits among Rust peers (Leptos/Sycamore/Dioxus/Yew) and design analogs (Solid/Vue).
- **The 1.0 requirements**: what a credible 1.0 of a framework of this kind must provide, as `REQ-FW-*`
  requirements with testable acceptance criteria — cross-cutting ones here, area-specific ones delegated to the
  owning spoke per the contract namespace partition.
- **The MVP-vs-1.0 line**: what makes Ferric *usable early* to build a real app, vs. what the full 1.0 bar
  requires on top. No hidden cuts.
- **The out-of-1.0 list**: scoped CSS/styling, devtools, hot reload, and desktop/mobile targets — each recorded
  as a deliberate post-1.0 item with a reason and `release_gating: false`, never a silent omission.

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, scope, constraints. |
| Contract | `../contracts/` (`id_and_traceability_schema.yaml`, `_MANIFEST.yaml`) | The `REQ-FW-*` schema, stage vocabulary, and namespace partition you own and must conform to. |
| Ferric baseline | `crates/ferric/` in `Nousix-LLC/nswe-demo` @ `main` | What exists today, to set the 1.0 line against. |
| Repo design precedent | `design/` (chirp: `REQ-*`/`BAR-*`, MVP-vs-releasable scoping) | The repo's own requirements/bar shape to match. |
| Peer frameworks | Leptos, Sycamore, Dioxus, Yew, Solid, Vue | Honest comparison of what a 1.0 of this kind provides; cite by name. |

### Declared output
- `scope-and-requirements.md` (in this task's workspace) — the `REQ-FW-*` register, the users/what-you-build
  section, the MVP-vs-1.0 line, and the out-of-1.0 list. Repo target `design/ferric/scope-and-requirements.md`.

### Success criteria
- [ ] Every `REQ-FW-*` has a statement (what, not how), rationale, testable acceptance criteria, a `stage`, and
      a `release_gating` flag, conforming to `../contracts/id_and_traceability_schema.yaml`.
- [ ] The MVP-vs-1.0 line is explicit and principled (what absence makes Ferric unusable for a real app vs.
      what a credible 1.0 adds).
- [ ] The out-of-1.0 list names styling, devtools, hot reload, desktop/mobile, each with a reason; none is
      enforced by any later bar criterion.
- [ ] Peer comparisons cite frameworks by name, grounded in what you actually read.

### Constraints
- Write `REQ-FW-*` only; do not write other areas' registers (identity I1). Cross-reference read-only.
- Design, not code. No implementation choices. Select and load your own library/framework-design methodology.
- Honor the hub's writing-voice rules; run the avoid-ai-writing pass before finalizing.
