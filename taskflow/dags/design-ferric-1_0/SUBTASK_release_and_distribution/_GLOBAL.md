# _GLOBAL.md — SUBTASK_release_and_distribution (concern 7 subtree hub)

## Project Context

**Status**: Active

### Objective

Design how the Ferric crates are published and versioned as a **1.0**: what it takes for each crate to be
publishable to **crates.io** and how the multi-crate workspace is released together; the **semver** contract
for the frozen public surfaces plus a **changelog** practice; and the **versioning and compatibility policy**
a 1.0 promises (MSRV, the frozen `prelude` surfaces, additive-only evolution, cross-crate coordination). The
bar: the crates are publishable with a semver contract and a changelog, each stated as a testable `REQ-REL-*`
requirement.

This subtree is **concern 7** of the Ferric 1.0 framework design (parent hub: `../_GLOBAL.md`). It owns the
`REQ-REL-*` register and nothing else (parent identity I1 — disjoint registers). It designs **what**, not
**how**: the implementation of publishing automation, a changelog tool, or a semver-check in CI is deferred to
later code DAGs. The single consolidated deliverable is `release-and-distribution.md` at this subtree root,
placed by `SUBTASK_design_pr` at `design/ferric/release-and-distribution.md`.

### Why this is decomposed

The parent brief names three distinct concerns for this task, and they are separable work a different
specialist could own in parallel: publishing mechanics (crates.io metadata, licensing, the path→version
dependency conversion, multi-crate release order) is a build/release-engineering concern; the semver contract
and changelog practice is an API-stability-and-communication concern; the versioning/compatibility policy
(MSRV, frozen-surface guarantees, cross-crate coordination) is a platform-stability concern. Each produces
`REQ-REL-*` requirements of the same shape, so they share a tight seam — one `REQ-REL-*` register that must not
collide or contradict. That seam is frozen in `contracts/_MANIFEST.yaml` before any spoke runs; the synthesis
gate merges the three partials into one register and asserts the seam held.

### Scope

**In Scope:**
- Publishing readiness for `ferric`, `ferric-router`, `ferric-http` (and any new 1.0 crate): per-crate crates.io
  metadata, licensing, docs, `cargo publish`/`cargo package` readiness; the multi-crate workspace release.
- The semver contract over the frozen `prelude` public surfaces; breaking-vs-additive classification; a
  changelog practice.
- The 1.0 versioning and compatibility policy: MSRV, the frozen `prelude` stability promise, additive-only
  evolution, cross-crate version coordination (the workspace uses `version.workspace = true`).
- Honest, named comparison to peer release/semver practice (Leptos, Dioxus, Yew) and the Rust API Evolution /
  Cargo SemVer reference guidelines.

**Out of Scope:**
- Any id register other than `REQ-REL-*` (other areas are owned by sibling spokes; cross-references are
  read-only).
- Implementing publishing automation, a changelog generator, a CI semver gate, or editing any crate — design
  only.
- The release *bar* (`BAR-FERRIC-*`) and the release *plan* (epics/work-items): owned by `SUBTASK_release_bar`
  and `SUBTASK_release_plan` at the parent level; this subtree supplies the `REQ-REL-*` they reference.

### Success Criteria

- [ ] Publishing readiness, the semver contract, the changelog practice, and the 1.0 compatibility policy are
      each specified as testable `REQ-REL-*` requirements with acceptance criteria a stranger could check (e.g.
      `cargo publish --dry-run` / `publishability`), conforming to `../contracts/id_and_traceability_schema.yaml`.
- [ ] The policy states what 1.0 promises about the frozen public `prelude` surfaces and the MSRV.
- [ ] Peer release practices are compared by name.
- [ ] One consolidated `release-and-distribution.md` carries the merged `REQ-REL-*` register with no range gaps
      or overlaps, in the repo's design-doc shape.

---

## Constraints and Requirements

### Process / Quality

- **What, not how.** Each requirement reads as something a stranger could verify against the published crates,
  not a chosen implementation.
- **Write `REQ-REL-*` only** (parent identity I1). Cross-references to other areas' REQ are read-only.
- **Evidence over memory.** Peer comparisons name the framework; "common practice" claims rest on something
  actually read (the Cargo book's SemVer chapter, the Rust API Evolution RFC/guidelines, Keep a Changelog,
  `cargo-semver-checks`). Cite by name, never by host path.
- **Writing voice.** Plain, checkable prose. No machine-writing tells (no character adjectives on things that
  cannot hold a character, no narrated candor, no unpaired contrasts, no slot-fill templates, no padded triads,
  no hollow intensifiers). Run the avoid-ai-writing pass over every narrative deliverable before finalizing.
- **GitHub hygiene** (inherited): nothing authored here names host, cluster, SSH, path, or environment detail;
  repository identities only.

### Grounding (observed facts the spokes build on)

Grounded in `Nousix-LLC/nswe-demo` @ `main` (baseline `276138f`):

- The workspace `Cargo.toml` is a **virtual workspace** (`members = ["crates/*"]`) with
  `[workspace.package] version = "0.1.0"`, `edition = "2021"`, `rust-version = "1.82"`,
  `repository = "https://github.com/Nousix-LLC/nswe-demo"`. All Ferric crates inherit these with
  `version.workspace = true` (so the crates version in lockstep today).
- Workspace lints already enforce `missing_docs = "warn"` and `unsafe_code = "warn"`; release profile is
  size-tuned (`opt-level = "s"`, `lto = true`, `codegen-units = 1`).
- **No `license` or `license-file` field in any manifest, and no top-level `LICENSE` file** — crates.io
  **requires** a license (or license-file) to publish. This is the headline publishing gap.
- No `keywords`, `categories`, `documentation`, or `homepage` fields; each crate has a `description`. A top-level
  `README.md` and `crates/ferric/README.md` exist; the other two crates' README/`readme` field state is for the
  publishing spoke to confirm.
- **No `CHANGELOG.md`** anywhere.
- `ferric-router` depends on `ferric` via `{ path = "../ferric" }` with **no version** — `cargo publish`
  requires a version requirement on a dependency, so this must become `{ path = "../ferric", version = "..." }`.
  `ferric-http` has no intra-workspace dependency.
- The frozen public surfaces are the `prelude` modules: `ferric::prelude` (`Component`, `mount`, `batch`,
  `create_effect`, `create_memo`, `create_signal`, `Memo`, `Signal`, `EventKind`, `VElement`, `VNode`);
  `ferric_router::prelude` (`link`, `Params`, `RoutePattern`, `Router`, `navigate`, `current_path`);
  `ferric_http` top-level re-exports + `prelude` (`Client`, `ClientBuilder`, `Error`, `Method`,
  `RequestBuilder`, `Response`, `Result`). Many leaf bodies are still `todo!()`; the public shape is fixed.

---

## Input Specifications

| Source | Location | Purpose |
|--------|----------|---------|
| Parent hub | `../_GLOBAL.md` | Framework-wide context, constraints, the parent contract and identities. |
| Parent contract | `../contracts/` | The `REQ-<AREA>-NNN` scheme, verification_method + stage vocabularies, the bar/epic schemas. READ-ONLY; the sub-contract here extends it, never overrides. |
| 1.0 requirements | `../SUBTASK_scope_and_requirements/scope-and-requirements.md` | The cross-cutting frame to specialize — esp. REQ-FW-001 (crates.io install), REQ-FW-003 (stable Rust + MSRV), REQ-FW-009 (frozen surfaces additive), REQ-FW-010 (semver + compat policy), REQ-FW-013 (lean deps). |
| Subtree contract | `contracts/_MANIFEST.yaml` | The `REQ-REL-*` partition, per-spoke ownership, and the merge identities this subtree asserts. |
| Workspace manifests | `Nousix-LLC/nswe-demo` @ `main`: `Cargo.toml`, `crates/{ferric,ferric-router,ferric-http}/Cargo.toml`, each `src/lib.rs` prelude | What is published; what the semver contract covers; the publishing gaps. Reachable via `gh api` (repo content) — not a local checkout. |
| Peer precedent | Leptos, Dioxus, Yew release & semver practice; the Cargo book SemVer chapter, Rust API Evolution guidelines, Keep a Changelog, `cargo-semver-checks` | Honest comparison and standards grounding; cite by name. |

---

## Task Structure

### Overview

```
_GLOBAL.md (this hub)
├── contracts/
│   └── _MANIFEST.yaml                     (REQ-REL-* partition + merge identities — READ-ONLY for spokes)
├── SUBTASK_publishing/_BRIEF.md           (REQ-REL-001..019 — crates.io readiness + multi-crate release)
├── SUBTASK_semver_changelog/_BRIEF.md     (REQ-REL-020..039 — semver contract + changelog practice)
├── SUBTASK_versioning_compat/_BRIEF.md    (REQ-REL-040..059 — 1.0 versioning & compatibility policy)
└── SUBTASK_rel_synthesis/_BRIEF.md        (synthesis gate — merge into release-and-distribution.md + fold)
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_publishing` | none | crates.io publishing readiness per crate (license/metadata/docs/`cargo publish`), the path→version dependency conversion, and the multi-crate workspace release. Owns `REQ-REL-001..019`. | `publishing.md` |
| `SUBTASK_semver_changelog` | none | The semver contract over the frozen `prelude` surfaces, breaking-vs-additive classification, and a changelog practice. Owns `REQ-REL-020..039`. | `semver-changelog.md` |
| `SUBTASK_versioning_compat` | none | The 1.0 versioning & compatibility policy: MSRV, frozen-surface guarantees, additive-only evolution, cross-crate version coordination. Owns `REQ-REL-040..059`. | `versioning-compat.md` |
| `SUBTASK_rel_synthesis` | `SUBTASK_publishing`, `SUBTASK_semver_changelog`, `SUBTASK_versioning_compat` | Merge the three partials into one `release-and-distribution.md` with the full `REQ-REL-*` register; assert the merge identities; fold the parent. (Id is `SUBTASK_rel_synthesis` — distinct from the parent-level root `SUBTASK_synthesis`.) | `../release-and-distribution.md`, `../SYNTHESIS.md` |

### Dependency Graph

```
SUBTASK_publishing ────────────┐
SUBTASK_semver_changelog ──────┼─► SUBTASK_rel_synthesis ─► (fold release_and_distribution)
SUBTASK_versioning_compat ─────┘
```

---

## Contract

**REQUIRED and present** at `contracts/_MANIFEST.yaml` (read-only for every spoke). It extends the parent
contract (`../contracts/`): it does not redefine the `REQ-<AREA>-NNN` scheme, the verification_method
vocabulary, or the stage vocabulary — it **partitions the `REQ-REL-*` number space** across the three spokes
so the registers never collide, fixes per-spoke ownership and output filenames, and declares the identities the
synthesis gate asserts when it merges the three partials into one register. See the manifest for the field
schemas; the narrative lives here.

**Contract location**: `contracts/` · **Contract kind**: `yaml_schema` (extends the parent `yaml_schema`).

### Ownership (REQ-REL range + output per spoke)

| Spoke | Owns `REQ-REL-*` range | Output file |
|---|---|---|
| `SUBTASK_publishing` | `REQ-REL-001` .. `REQ-REL-019` | `publishing.md` |
| `SUBTASK_semver_changelog` | `REQ-REL-020` .. `REQ-REL-039` | `semver-changelog.md` |
| `SUBTASK_versioning_compat` | `REQ-REL-040` .. `REQ-REL-059` | `versioning-compat.md` |
| `SUBTASK_rel_synthesis` | the merged register + `release-and-distribution.md` | `../release-and-distribution.md` |

### Identities (the synthesis gate asserts these; no silent plugs)

- [ ] **J1 — disjoint REQ-REL ranges.** Each spoke mints only `REQ-REL-*` ids inside its assigned range; no id
      is used by two spokes and no id collides.
- [ ] **J2 — schema conformance.** Every `REQ-REL-*` carries the parent schema's fields (id, statement,
      rationale, acceptance_criteria, stage, release_gating, references) per `../contracts/id_and_traceability_schema.yaml`.
- [ ] **J3 — framework-appropriate verification.** Every acceptance criterion uses a `verification_method` from
      the parent's closed vocabulary (expected here: `publishability`, `doc_inspection`, `automated_test`,
      `example_build`).
- [ ] **J4 — all three concerns covered.** ≥1 `REQ-REL-*` covers publishing readiness; ≥1 covers the semver
      contract; ≥1 covers the changelog practice; ≥1 covers the versioning/compatibility policy.
- [ ] **J5 — 1.0 promise stated.** At least one `REQ-REL-*` states the MSRV promise and at least one states the
      frozen-`prelude` stability promise for 1.0.
- [ ] **J6 — peers named.** The merged doc compares release/semver practice to named peers (Leptos, Dioxus, Yew)
      and cites the Rust SemVer / API-evolution reference by name.
- [ ] **J7 — placed once, repo shape.** The merged `release-and-distribution.md` carries the complete register
      with no range gaps/overlaps, a Metadata section naming the owning task and the `conforms_to` contract, in
      the shape of the repo's existing design docs (e.g. `../SUBTASK_scope_and_requirements/scope-and-requirements.md`).

### Derived artifacts

- The three spoke partials (`publishing.md`, `semver-changelog.md`, `versioning-compat.md`) are the sources
  `SUBTASK_synthesis` merges into `release-and-distribution.md`.
- `release-and-distribution.md` is the single doc `SUBTASK_design_pr` (parent level) places at
  `design/ferric/release-and-distribution.md`.

---

## Output Specifications

| Deliverable | Location | Description |
|-------------|----------|-------------|
| Publishing partial | `SUBTASK_publishing/publishing.md` | crates.io readiness + multi-crate release; `REQ-REL-001..019`. |
| Semver/changelog partial | `SUBTASK_semver_changelog/semver-changelog.md` | semver contract + changelog practice; `REQ-REL-020..039`. |
| Versioning/compat partial | `SUBTASK_versioning_compat/versioning-compat.md` | 1.0 versioning & compatibility policy; `REQ-REL-040..059`. |
| Consolidated design doc | `release-and-distribution.md` (this subtree root) | The merged release/distribution design + full `REQ-REL-*` register. Repo target `design/ferric/release-and-distribution.md`. |
| Fold record | `SYNTHESIS.md` (this subtree root) | The synthesis task's terminal + fold record for this concern. |
