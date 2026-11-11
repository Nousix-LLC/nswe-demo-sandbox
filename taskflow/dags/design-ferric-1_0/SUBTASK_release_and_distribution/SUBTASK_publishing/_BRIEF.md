# Task: Ferric 1.0 — crates.io publishing readiness & multi-crate release

## Task Specification
**Slug**: SUBTASK_publishing
**Task Kind**: standard
**Status**: Pending

### Objective
Design what it takes for the Ferric crates to be **publishable to crates.io** as a 1.0, and how the multi-crate
workspace is released together — expressed as testable `REQ-REL-001..019` requirements.

### Context
Part of concern 7, release & distribution (subtree hub: `../_GLOBAL.md`). You own the `REQ-REL-001..019` range
only (sub-contract `../contracts/_MANIFEST.yaml`, identity J1). Design the user-facing requirement and its
checkable bar — not the implementation of any publishing automation. The companion concerns (the semver
contract + changelog, and the versioning/compatibility policy) are owned by sibling spokes; where your
requirements touch them, cross-reference read-only, do not restate them as your own ids.

### Scope — the publishing concern
Cover, from the side of someone trying to `cargo add ferric` and someone trying to `cargo publish` it:
- **Per-crate crates.io readiness** for `ferric`, `ferric-router`, `ferric-http` (and any new 1.0 crate): the
  metadata crates.io requires or expects (license/license-file, description, readme, repository, documentation,
  keywords, categories, homepage), and the docs.rs story. The grounded gap set in `../_GLOBAL.md` is your
  starting point — the missing `license`/`LICENSE`, the absent `keywords`/`categories`, the per-crate README
  state — confirm it against the live manifests and design the requirement that closes it.
- **The path→version dependency conversion.** `ferric-router` depends on `ferric` via `{ path = "../ferric" }`
  with no version; crates.io rejects a dependency with no version requirement. Design the requirement that each
  intra-workspace dependency carries both a path (for local dev) and a version (for the published crate).
- **`cargo publish` / `cargo package` readiness.** What must hold for `cargo publish --dry-run` (and
  `cargo package`) to succeed for each crate, including that a crate with `todo!()` leaf bodies still builds and
  packages.
- **Multi-crate workspace release.** The order crates publish in (a dependency must be on crates.io before its
  dependents), and how a coordinated workspace release is designed given `version.workspace = true`.

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, grounded facts, constraints, the sub-contract summary. |
| Sub-contract | `../contracts/_MANIFEST.yaml` | Your `REQ-REL-001..019` range + the merge identities. |
| Parent contract | `../../contracts/id_and_traceability_schema.yaml` | The REQ field schema, verification_method + stage vocabularies to conform to. |
| 1.0 requirements | `../../SUBTASK_scope_and_requirements/scope-and-requirements.md` | Esp. REQ-FW-001 (crates.io install) and REQ-FW-013 (lean deps) to specialize. |
| Workspace manifests | `Nousix-LLC/nswe-demo` @ `main`: `Cargo.toml`, `crates/*/Cargo.toml` (reachable via `gh api`) | What is published and what metadata exists today. |
| Peer precedent | How Leptos / Dioxus / Yew publish their multi-crate workspaces to crates.io; the Cargo book's publishing chapter | Honest comparison; cite by name. |

### Declared output
- `publishing.md` (this task's workspace) — the publishing-readiness design + the `REQ-REL-001..019` register.

### Success criteria
- [ ] Each `REQ-REL-*` (in range) has a statement (what, not how), a rationale with named peer/standard evidence,
      acceptance criteria using the parent's `verification_method` vocabulary (publishability / doc_inspection),
      a `stage`, and `release_gating`.
- [ ] The license gap, the metadata gaps, the path→version conversion, and the multi-crate release order are
      each covered by at least one requirement with a checkable bar.
- [ ] Conforms to the parent schema and stays inside the `REQ-REL-001..019` range (identities J1–J3).

### Constraints
- Design, not implementation. `REQ-REL-001..019` only. Load your own crates.io/release-engineering methodology
  if available. Honor the writing-voice rules in `../_GLOBAL.md`.
