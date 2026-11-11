# Task: Ferric 1.0 — semver contract & changelog practice

## Task Specification
**Slug**: SUBTASK_semver_changelog
**Task Kind**: standard
**Status**: Pending

### Objective
Design the **semver contract** for Ferric's public surfaces and the **changelog practice** that communicates
change — expressed as testable `REQ-REL-020..039` requirements.

### Context
Part of concern 7, release & distribution (subtree hub: `../_GLOBAL.md`). You own the `REQ-REL-020..039` range
only (sub-contract `../contracts/_MANIFEST.yaml`, identity J1). This concern answers: given the frozen `prelude`
surfaces, what does a version number *promise*, what counts as a breaking vs an additive change, and how is each
release's change set recorded so an author can upgrade safely? The publishing mechanics (metadata, `cargo
publish`) and the broader compatibility policy (MSRV, cross-crate coordination) are sibling spokes; reference
them read-only.

### Scope — the semver + changelog concern
- **The semver contract over the public surface.** What semantic-versioning level (major/minor/patch) signals
  for each class of change to the frozen `prelude` surfaces of `ferric`, `ferric-router`, `ferric-http`. Ground
  the "what is the public surface" question in those `prelude` modules (enumerated in `../_GLOBAL.md`).
- **Breaking-vs-additive classification.** A classification an author (and a reviewer) can apply: which changes
  are additive (new exports, new methods) and which are breaking (removed/renamed/retyped exports, changed
  behavior), using the Rust API Evolution / Cargo SemVer reference vocabulary (major-change vs minor-change).
  Consider whether a tool such as `cargo-semver-checks` is named as the mechanical check (as a *requirement's
  acceptance method*, not as an implementation you build).
- **Changelog practice.** How each crate records its changes release to release (e.g. a per-crate `CHANGELOG.md`
  in Keep a Changelog form vs a workspace-level changelog), what each entry must state, and how the changelog
  ties to the semver level of the release. Ground in the observed absence of any `CHANGELOG.md` today.

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, the enumerated frozen `prelude` surfaces, constraints. |
| Sub-contract | `../contracts/_MANIFEST.yaml` | Your `REQ-REL-020..039` range + the merge identities. |
| Parent contract | `../../contracts/id_and_traceability_schema.yaml` | REQ field schema, verification_method + stage vocabularies. |
| 1.0 requirements | `../../SUBTASK_scope_and_requirements/scope-and-requirements.md` | Esp. REQ-FW-009 (frozen surfaces additive) and REQ-FW-010 (semver-governed API). |
| Public surfaces | `Nousix-LLC/nswe-demo` @ `main`: each crate's `src/lib.rs` `prelude` (via `gh api`) | The surface the semver contract governs. |
| Standards + peers | The Cargo book SemVer chapter, the Rust API Evolution guidelines, Keep a Changelog, `cargo-semver-checks`; Leptos / Dioxus / Yew changelog & semver practice | Standards grounding and honest comparison; cite by name. |

### Declared output
- `semver-changelog.md` (this task's workspace) — the semver contract + changelog design + the
  `REQ-REL-020..039` register.

### Success criteria
- [ ] Each `REQ-REL-*` (in range) has a statement, a rationale with named standard/peer evidence, acceptance
      criteria using the parent's `verification_method` vocabulary (doc_inspection / automated_test), a `stage`,
      and `release_gating`.
- [ ] The semver contract, the breaking-vs-additive classification, and the changelog practice are each covered
      by at least one requirement with a checkable bar.
- [ ] Conforms to the parent schema and stays inside the `REQ-REL-020..039` range (identities J1–J3).

### Constraints
- Design, not implementation. `REQ-REL-020..039` only. Load your own semver/release methodology if available.
  Honor the writing-voice rules in `../_GLOBAL.md`.
