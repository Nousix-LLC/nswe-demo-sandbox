# Task: Ferric 1.0 — release & distribution (concern 7)

## Task Specification
**Slug**: SUBTASK_release_and_distribution
**Task Kind**: standard
**Status**: Pending

### Objective
Design how the Ferric crates are published and versioned as a 1.0: publishing to **crates.io** with **semver**
and a **changelog**, and the versioning and compatibility policy for a 1.0 across the multi-crate workspace
(`ferric`, `ferric-router`, `ferric-http`, and any new crates the 1.0 adds). Bar: the crates are publishable
with a semver contract and a changelog.

### Context
Part of the Ferric 1.0 framework design (see `../_GLOBAL.md`); owns `REQ-REL-*`. The crates use a workspace
`version.workspace = true`; distribution is to crates.io (not a deployed service). What "1.0" promises about
stability and compatibility is itself a design decision.

**Dependencies**: `SUBTASK_scope_and_requirements`.

### Distinct concerns to cover (name them; let your own evaluation decide how to split)
- **Publishing**: what it takes for each crate to be publishable to crates.io (metadata, licensing, docs,
  `cargo publish` readiness); how the multi-crate workspace is released together.
- **Semver + changelog**: the semver contract for the public surfaces, a changelog practice, and how breaking
  vs. additive changes are classified.
- **Versioning & compatibility policy**: what a 1.0 promises (MSRV, the frozen public `prelude` surfaces,
  additive-only evolution), and the cross-crate compatibility story.

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context + constraints. |
| Contract | `../contracts/` | `REQ-REL-*` schema; your namespace. |
| 1.0 requirements | `../SUBTASK_scope_and_requirements/scope-and-requirements.md` | The frame to specialize. |
| Workspace crates | `Cargo.toml` (workspace), `crates/*/Cargo.toml`, the frozen `prelude` surfaces | What is published and what the semver contract covers. |
| Peer precedent | Leptos/Dioxus/Yew release & semver practice, the Rust API Evolution / SemVer guidelines | Honest comparison; cite by name. |

### Declared output
- `release-and-distribution.md` (this task's workspace) — the release/distribution design + the `REQ-REL-*`
  register. Repo target `design/ferric/release-and-distribution.md`.

### Success criteria
- [ ] Publishing readiness, the semver contract, the changelog practice, and the 1.0 compatibility policy are
      each specified with testable `REQ-REL-*` acceptance criteria (e.g. `cargo publish --dry-run` /
      `publishability`), conforming to the contract schema.
- [ ] The policy states what 1.0 promises about the frozen public surfaces and MSRV.
- [ ] Peer release practices compared by name.

### Constraints
- Write `REQ-REL-*` only (identity I1). Design, not implementation. Load your own release-engineering methodology.
- Honor the writing-voice rules.
