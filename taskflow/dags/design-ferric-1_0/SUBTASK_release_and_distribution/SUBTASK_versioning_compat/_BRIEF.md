# Task: Ferric 1.0 — versioning & compatibility policy

## Task Specification
**Slug**: SUBTASK_versioning_compat
**Task Kind**: standard
**Status**: Pending

### Objective
Design the **versioning and compatibility policy** a Ferric 1.0 promises — what "1.0" commits to about stability,
MSRV, the frozen public surfaces, additive-only evolution, and how the crates version together — expressed as
testable `REQ-REL-040..059` requirements.

### Context
Part of concern 7, release & distribution (subtree hub: `../_GLOBAL.md`). You own the `REQ-REL-040..059` range
only (sub-contract `../contracts/_MANIFEST.yaml`, identity J1). This concern answers: what does a user get to
*rely on* across the 1.x line? It is the policy a library author (persona A3) and an app author (A2) read before
depending on Ferric. The semver *mechanics* (what a version bump signals, the changelog) are the sibling
`SUBTASK_semver_changelog`; the publishing *mechanics* are `SUBTASK_publishing`; this spoke owns the *promise*.
Reference the siblings read-only.

### Scope — the versioning & compatibility concern
- **MSRV policy.** What minimum supported Rust version 1.0 commits to (the workspace sets `rust-version = 1.82`
  today), and the policy for when/how MSRV may rise within the 1.x line.
- **Frozen-`prelude` stability guarantee.** What 1.0 promises about the public `prelude` surfaces carried
  forward (enumerated in `../_GLOBAL.md`): that they remain usable across 1.x, that evolution is additive-only,
  and what a consumer can build against and trust. This is the policy side of REQ-FW-009.
- **Additive-only evolution.** The commitment that the public surface grows by addition within 1.x and that any
  removal/redefinition is a breaking change deferred to a future major.
- **Cross-crate version coordination.** How `ferric`, `ferric-router`, `ferric-http` version relative to one
  another given `version.workspace = true` (lockstep today): whether the 1.0 keeps lockstep workspace versioning
  or allows independent crate versions, and what compatibility an app author can assume across the set (e.g. a
  `ferric-router` 1.x works with `ferric` 1.x). State the policy and its reason.

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, the grounded workspace facts (MSRV 1.82, `version.workspace`), the frozen surfaces, constraints. |
| Sub-contract | `../contracts/_MANIFEST.yaml` | Your `REQ-REL-040..059` range + the merge identities. |
| Parent contract | `../../contracts/id_and_traceability_schema.yaml` | REQ field schema, verification_method + stage vocabularies. |
| 1.0 requirements | `../../SUBTASK_scope_and_requirements/scope-and-requirements.md` | Esp. REQ-FW-003 (stable Rust / MSRV), REQ-FW-009 (frozen surfaces additive), REQ-FW-010 (compatibility policy). |
| Workspace facts | `Nousix-LLC/nswe-demo` @ `main`: `Cargo.toml` (`[workspace.package]`), each crate's `prelude` (via `gh api`) | MSRV, the lockstep versioning, the surfaces the policy governs. |
| Peer precedent | How Leptos / Dioxus / Yew state MSRV and cross-crate compatibility; the Cargo book on `rust-version` and SemVer compatibility | Honest comparison; cite by name. |

### Declared output
- `versioning-compat.md` (this task's workspace) — the 1.0 versioning & compatibility policy + the
  `REQ-REL-040..059` register.

### Success criteria
- [ ] Each `REQ-REL-*` (in range) has a statement, a rationale with named peer/standard evidence, acceptance
      criteria using the parent's `verification_method` vocabulary (doc_inspection / automated_test), a `stage`,
      and `release_gating`.
- [ ] The MSRV promise and the frozen-`prelude` stability promise are each stated as a requirement (merge
      identity J5), alongside additive-only evolution and the cross-crate coordination policy.
- [ ] Conforms to the parent schema and stays inside the `REQ-REL-040..059` range (identities J1–J3).

### Constraints
- Design, not implementation. `REQ-REL-040..059` only. Load your own versioning/compatibility methodology if
  available. Honor the writing-voice rules in `../_GLOBAL.md`.
