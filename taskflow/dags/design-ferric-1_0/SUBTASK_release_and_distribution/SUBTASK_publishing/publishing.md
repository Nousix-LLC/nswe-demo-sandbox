# Ferric 1.0 — crates.io Publishing Readiness & Multi-Crate Release

This is the publishing partial of the release & distribution design (concern 7). It states what it takes for the
Ferric crates to be **publishable to crates.io** as a 1.0, and how the multi-crate workspace is released together,
as testable `REQ-REL-001..019` requirements. It designs **what** must be true of the published crates — the bar a
stranger could check against crates.io and `cargo` — not the implementation of any publishing automation. The semver
contract and changelog (`REQ-REL-020..039`, `SUBTASK_semver_changelog`) and the versioning/compatibility policy
(`REQ-REL-040..059`, `SUBTASK_versioning_compat`) are owned by sibling spokes; where a requirement here touches them,
it cross-references read-only and does not restate their ids.

**What, not how.** Each requirement reads as a condition on the published crates and the `cargo` commands that
produce them, verifiable by someone who was not in the room. How the metadata is edited, whether a release script or
`cargo-release` / `release-plz` drives it, and how the CI gate is wired are deferred to later code DAGs.

**Grounding.** Observations of "Ferric as it exists today" are grounded in `Nousix-LLC/nswe-demo` @ `main`
(baseline `276138f`), confirmed against the live workspace and crate manifests at design time:

- The root `Cargo.toml` is a **virtual workspace** (`members = ["crates/*"]`, `resolver = "2"`) with
  `[workspace.package] version = "0.1.0"`, `edition = "2021"`, `rust-version = "1.82"`,
  `repository = "https://github.com/Nousix-LLC/nswe-demo"`. The three Ferric crates (`ferric`, `ferric-router`,
  `ferric-http`) each inherit `version.workspace = true`, so they version in lockstep at `0.1.0` today.
- **No `license` or `license-file` field in any manifest, and no `LICENSE` file at the repo root.** crates.io
  rejects a publish without a license — this is the headline gap.
- **No `keywords`, `categories`, `documentation`, `homepage`, or explicit `readme` field** in any manifest. Each
  crate does carry a `description`, and a `README.md` exists at the repo root and in all three crate directories
  (`crates/ferric/README.md`, `crates/ferric-router/README.md`, `crates/ferric-http/README.md`).
- `ferric-router` depends on `ferric` via `{ path = "../ferric" }` with **no `version`**. `cargo` refuses to publish
  a crate whose dependency has a path but no version requirement, so this must become
  `{ path = "../ferric", version = "..." }`. `ferric-http` has no intra-workspace dependency (it pulls `serde`,
  `serde_json`, and `wasm-bindgen-futures` from crates.io directly).
- Many public-surface leaf bodies are still `todo!()`; the public `prelude` shapes are frozen. A `todo!()` body is a
  compiling expression, so it does not block `cargo package` — the crate still builds and packages.

**References used (cited by name, not restated).** The Cargo book, *Publishing on crates.io* and *Specifying
Dependencies*; the Rust API Guidelines, *Necessities* (C-PERMISSIVE on licensing, C-METADATA on Cargo.toml metadata);
docs.rs (automatic documentation build on publish). Peer practice is named in the *Peer and standards grounding*
section below.

---

## The publishing picture, end to end

Someone adopting Ferric runs `cargo add ferric` and expects a published, semver-versioned crate to resolve. Someone
releasing Ferric runs `cargo publish` for each crate and expects it to succeed. Between those two sits everything this
partial designs: the metadata crates.io demands, the license it will not publish without, the path→version conversion
that lets an intra-workspace dependency be published at all, the `cargo package` checks each crate must pass, and the
order and coordination a three-crate workspace release requires. The requirements below walk that path:

- **Licensing** — `REQ-REL-001`, with the license files shipped in the package by `REQ-REL-006`.
- **Per-crate crates.io metadata** — `REQ-REL-002` (the manifest fields) and `REQ-REL-003` (the docs.rs story).
- **The path→version dependency conversion** — `REQ-REL-004`, with `REQ-REL-011` ensuring no path/git requirement
  leaks into a published manifest.
- **`cargo publish` / `cargo package` readiness** — `REQ-REL-005`, with package contents fixed by `REQ-REL-006`.
- **Multi-crate workspace release** — crate-name ownership (`REQ-REL-007`), publish order (`REQ-REL-008`), lockstep
  coordination under `version.workspace = true` (`REQ-REL-009`), and a repeatable release procedure (`REQ-REL-010`).

---

## Requirements register (`REQ-REL-001..019`)

Each requirement carries the parent schema's fields: `statement` (what, not how), `rationale` (with named peer/standard
evidence where relevant), `acceptance_criteria` (checkable, with a `verification_method` from the parent's closed
vocabulary — here `publishability`, `doc_inspection`, `automated_test`), `stage`, `release_gating`, and read-only
`references`. Conformance: `../../contracts/id_and_traceability_schema.yaml`.

Every requirement below is `stage: one_oh`, `release_gating: true`: crates.io publishing is the 1.0 add over the
`usable_early` floor (an author can build a real app against a path or git dependency before 1.0; the published,
depend-on-normally story is what 1.0 promises — `REQ-FW-001`).

### Licensing

#### REQ-REL-001 — Every published crate declares a permissive license
- **Statement:** Each Ferric crate published to crates.io declares a license in its manifest, and the chosen license
  is a permissive one compatible with the Rust ecosystem.
- **Rationale:** crates.io will not publish a crate that declares neither `license` nor `license-file` (Cargo book,
  *Publishing on crates.io*, lists `license` or `license-file` among the fields that must be filled out). This is the
  one gap that blocks publishing outright today — no manifest has a license and there is no `LICENSE` file. The Rust
  API Guidelines (C-PERMISSIVE) recommend `license = "MIT OR Apache-2.0"` with both `LICENSE-APACHE` and `LICENSE-MIT`
  at the repository root for maximum ecosystem compatibility; Ferric's Rust peers publish under the same permissive
  convention (see *Peer and standards grounding*). A permissive choice also keeps `REQ-REL-011`'s "depend only on
  permissively-licensed crates" tractable.
- **Acceptance criteria:**
  - Every published crate's `Cargo.toml` carries a `license` (an SPDX expression) or a `license-file`; the same
    expression is used across the three crates. (`doc_inspection`)
  - `cargo publish --dry-run` no longer fails for a missing-license reason for any crate. (`publishability`)
  - If the `MIT OR Apache-2.0` convention is taken, the corresponding `LICENSE-APACHE` and `LICENSE-MIT` files exist
    where the manifests reference them and the README states the license. (`doc_inspection`)
- **Stage:** one_oh · **Release gating:** true
- **References:** `REQ-FW-001` (installable from crates.io); `REQ-REL-006` (the license files ship in the package).

### Per-crate crates.io metadata

#### REQ-REL-002 — Complete per-crate crates.io metadata
- **Statement:** Each published crate carries the metadata crates.io requires and the metadata an evaluating author
  expects to see on the crate's crates.io page: `description`, `repository`, `readme`, `documentation`, `homepage`,
  `keywords`, and `categories`.
- **Rationale:** `description` is required to publish (Cargo book, *Publishing on crates.io*); `repository`, `readme`,
  and `homepage` are the fields the same chapter recommends, and the Rust API Guidelines (C-METADATA) call for the
  crate's Cargo.toml to carry complete metadata so the crate is discoverable and its source and docs are reachable.
  An evaluating author (persona A1 in the scope doc) judges a framework in an afternoon from its crates.io landing
  page; missing keywords/categories make it undiscoverable and a missing repository/docs link reads as unfinished.
  Today only `description` is present. `readme` need not be set explicitly if a `README.md` sits beside the manifest
  (Cargo auto-detects it) — the requirement is that the rendered crate shows a README, however that resolves.
- **Acceptance criteria:**
  - Each published crate's manifest (or workspace-inherited metadata) provides `description`, `repository`,
    `documentation`, `homepage`, `keywords`, and `categories`, and the crate renders a README on crates.io.
    (`doc_inspection`)
  - `categories` uses only slugs from the crates.io category list, and `keywords`/`categories` stay within
    crates.io's count limits, so publishing is not rejected for an invalid category or too many keywords.
    (`publishability`)
  - The three crates' metadata is consistent where it should be (shared `repository`, coherent keyword set), and each
    `description` reads as that crate's own one-line summary. (`doc_inspection`)
- **Stage:** one_oh · **Release gating:** true
- **References:** `REQ-FW-001`; `REQ-FW-011` (documentation sufficient to evaluate and learn, owned by `REQ-DX-*`);
  `REQ-REL-003` (the `documentation` link points at the docs.rs build).

#### REQ-REL-003 — API documentation builds on docs.rs for every published crate
- **Statement:** Each published crate's API documentation builds successfully on docs.rs so that a reader reaches
  rendered docs for the public surface from the crate's crates.io page.
- **Rationale:** docs.rs builds and hosts documentation automatically for every crate published to crates.io; a crate
  whose docs.rs build fails ships to adopters with a broken "docs" link, which an evaluating author reads as an
  unfinished crate. Ferric's crates are WASM-targeted but their binding dependencies (`wasm-bindgen`, `web-sys`,
  `js-sys`) compile off-`wasm32` (the repo already relies on this for native tests of `ferric-http`), so the default
  docs.rs target should build; where a crate genuinely needs a WASM target or feature set to document, that is
  declared in `[package.metadata.docs.rs]` rather than left to fail. The workspace already enforces `missing_docs =
  "warn"`, so the public surface is documented.
- **Acceptance criteria:**
  - `cargo doc --no-deps` builds the public API docs for each crate without error on the target docs.rs will use
    (the default host target, or the target declared in `[package.metadata.docs.rs]`). (`automated_test`)
  - After publish, each crate's docs.rs page renders the public `prelude` surface, and the crate's `documentation`
    field (`REQ-REL-002`) resolves to it. (`doc_inspection`)
- **Stage:** one_oh · **Release gating:** true
- **References:** `REQ-REL-002`; `REQ-FW-011`.

### The path→version dependency conversion

#### REQ-REL-004 — Intra-workspace dependencies carry both a path and a version
- **Statement:** Every dependency between Ferric crates is declared with both a `path` (for local development) and a
  `version` requirement (for the published crate), so each crate is publishable while the workspace still builds
  locally against its sibling sources.
- **Rationale:** Cargo will not publish a crate with a path dependency that lacks a version requirement (Cargo book,
  *Specifying Dependencies*: a path dependency must also carry a `version` to be published, because the published
  crate must resolve its dependency from crates.io, not from a local path that does not exist on the registry). Today
  `ferric-router` depends on `ferric` via `{ path = "../ferric" }` with no version, which blocks its publish. The
  standard fix is `{ path = "../ferric", version = "..." }`: Cargo uses the path when building inside the workspace
  and records the version requirement in the published manifest.
- **Acceptance criteria:**
  - `ferric-router`'s dependency on `ferric` (and any future intra-workspace dependency) carries both `path` and a
    `version` requirement matching the released version line. (`doc_inspection`)
  - `cargo publish --dry-run` for `ferric-router` no longer fails for a path-dependency-without-version reason.
    (`publishability`)
  - A local `cargo build` of the workspace still compiles `ferric-router` against the sibling `ferric` source, not a
    registry copy. (`automated_test`)
- **Stage:** one_oh · **Release gating:** true
- **References:** `REQ-FW-001`; the versioning/compatibility policy (`REQ-REL-040..059`, `SUBTASK_versioning_compat`)
  owns how the version requirement is kept coherent across the workspace; `REQ-REL-009` (lockstep release).

### `cargo publish` / `cargo package` readiness

#### REQ-REL-005 — Each crate passes `cargo publish --dry-run` / `cargo package`
- **Statement:** Each Ferric crate packages and verifies cleanly — `cargo publish --dry-run` (equivalently
  `cargo package`) succeeds for it — including while public-surface leaf bodies are still `todo!()`.
- **Rationale:** `cargo publish --dry-run`, which the Cargo book says is equivalent to `cargo package`, runs the
  verification crates.io performs: it checks the package, compresses the source into a `.crate`, and extracts and
  compiles it in a temporary directory. Making this the bar catches a missing license (`REQ-REL-001`), a
  version-less path dependency (`REQ-REL-004`), and packaging problems (`REQ-REL-006`) before a real publish. A
  `todo!()` body is a compiling expression that panics only at runtime, so a frozen-but-unimplemented surface still
  compiles and packages — the dry-run bar holds today's walking skeleton to the same standard as a finished crate.
- **Acceptance criteria:**
  - `cargo package` (or `cargo publish --dry-run`) completes without error for `ferric`, `ferric-router`, and
    `ferric-http`, with the verification compile succeeding. (`publishability`)
  - The dry-run produces no publish-blocking warnings about missing required metadata. (`publishability`)
  - The run succeeds even with `todo!()` leaf bodies present (no requirement that bodies be implemented to package).
    (`publishability`)
- **Stage:** one_oh · **Release gating:** true
- **References:** `REQ-REL-001`, `REQ-REL-004`, `REQ-REL-006`.

#### REQ-REL-006 — The packaged crate contains the license, README, and only intended files
- **Statement:** Each crate's packaged `.crate` archive contains the files a consumer and crates.io need — the source,
  the README, and the license file(s) the manifest references — and excludes files that do not belong in a published
  crate.
- **Rationale:** A published crate is self-contained: a `license-file`, or the `LICENSE-APACHE`/`LICENSE-MIT` files a
  `MIT OR Apache-2.0` crate ships, must be inside the `.crate` or the published crate has no license text even though
  the manifest names one; the README shown on crates.io must likewise be packaged. Because the crates live under
  `crates/*` in a virtual workspace, each crate's package must pull in the files it needs from its own directory
  (Cargo packages per-crate, not the whole workspace). Keeping stray or large non-source files out holds the WASM
  framework's published footprint to the source that belongs in it, consistent with the lean-footprint intent (`REQ-FW-013`).
- **Acceptance criteria:**
  - `cargo package --list` for each crate shows its source, its README, and the license file(s) its manifest
    references, and does not list unintended files. (`doc_inspection`)
  - For a `MIT OR Apache-2.0` crate, both license files are present in each crate's package (via repo-root files made
    available to each crate, a per-crate copy, or a `license-file` path that resolves in the package). (`publishability`)
- **Stage:** one_oh · **Release gating:** true
- **References:** `REQ-REL-001`; `REQ-REL-002`; `REQ-FW-013` (lean footprint, measured under `REQ-PERF-*`).

### Multi-crate workspace release

#### REQ-REL-007 — The crate names are owned on crates.io
- **Statement:** The names `ferric`, `ferric-router`, and `ferric-http` (and any new 1.0 crate) are registered to and
  owned by the project on crates.io before the 1.0 release depends on them.
- **Rationale:** crates.io names are first-come and permanent; a 1.0 that promises `cargo add ferric` cannot rest on a
  name the project does not control, and the first publish of each crate is what claims the name. Confirming ownership
  (or that the name is free and claimed by an initial publish) removes a late, unrecoverable surprise where a name is
  already taken. This is a publishing-readiness fact independent of the crate contents.
- **Acceptance criteria:**
  - Each crate name resolves on crates.io to a crate owned by the project (or is confirmed unregistered and reserved
    by the initial 1.0 publish). (`doc_inspection`)
  - The manifest `name` of each crate matches the owned crates.io name. (`doc_inspection`)
- **Stage:** one_oh · **Release gating:** true
- **References:** `REQ-FW-001`.

#### REQ-REL-008 — Crates publish in dependency order
- **Statement:** A coordinated release publishes the crates in an order that respects their dependency graph: a crate
  is published only after every Ferric crate it depends on is already available on crates.io at the version it
  requires.
- **Rationale:** crates.io resolves a published crate's dependencies from the registry at publish time, so a dependent
  cannot be published before its dependency exists there at the required version. For Ferric the order is `ferric`
  first, then `ferric-router` (which depends on `ferric` per `REQ-REL-004`); `ferric-http` has no intra-workspace
  dependency and may publish independently. Peer multi-crate frameworks release their companion crates as a
  coordinated set for exactly this reason (see *Peer and standards grounding*).
- **Acceptance criteria:**
  - The release publishes `ferric` before `ferric-router`; `ferric-http` has no Ferric dependency and orders freely.
    (`doc_inspection`)
  - Publishing the dependents succeeds because their required `ferric` version is already on crates.io — no publish
    fails for an unresolved intra-workspace dependency. (`publishability`)
  - The required order is derivable from the manifests (the dependency graph), not from tribal knowledge.
    (`doc_inspection`)
- **Stage:** one_oh · **Release gating:** true
- **References:** `REQ-REL-004`; `REQ-REL-009`.

#### REQ-REL-009 — The workspace releases as one coordinated, lockstep version set
- **Statement:** Because every Ferric crate inherits `version.workspace = true`, a release bumps them together to one
  shared version and publishes them as a single coordinated set, rather than versioning or releasing a crate on its
  own.
- **Rationale:** The workspace already pins a single `[workspace.package] version` that all three crates inherit, so
  the crates version in lockstep by construction; the release design must honor that rather than fight it. A single
  shared version across companion crates is the model Ferric's peers use (Leptos, Dioxus, Yew version their core and
  companion crates together), and it keeps the intra-workspace `version` requirements of `REQ-REL-004` trivially
  coherent — every crate requires the same version line. The detailed compatibility rules of the lockstep policy
  (what a bump promises, the MSRV) are owned by the versioning/compatibility spoke; this requirement fixes only the
  release mechanics: one version, released as a set.
- **Acceptance criteria:**
  - A release carries one version across all Ferric crates (the inherited `[workspace.package] version`), and all are
    published from the same release. (`doc_inspection`)
  - No Ferric crate is published at a version out of step with its siblings for the same release. (`publishability`)
- **Stage:** one_oh · **Release gating:** true
- **References:** `REQ-REL-004`, `REQ-REL-008`; the versioning/compatibility policy (`REQ-REL-040..059`,
  `SUBTASK_versioning_compat`) owns the MSRV and the meaning of a version bump; the semver contract
  (`REQ-REL-020..039`, `SUBTASK_semver_changelog`) owns breaking-vs-additive classification.

#### REQ-REL-010 — A documented, repeatable release procedure
- **Statement:** The repository documents the steps to cut a coordinated workspace release — set the version, the
  publish order, the per-crate dry-run, and the publish — so a release can be performed the same way by someone who
  did not design it.
- **Rationale:** A three-crate release with an ordering constraint and a shared version is error-prone when it lives in
  one person's memory; a written procedure is what makes the release repeatable and reviewable, and is the publishing
  counterpart to the changelog practice the sibling spoke designs. This is a documentation requirement, not an
  automation requirement — whether the steps are later encoded in a script or a CI job is left to a code DAG.
- **Acceptance criteria:**
  - A reviewer finds a release procedure in the repository that states the version bump, the `ferric`-before-
    `ferric-router` publish order, the per-crate `cargo publish --dry-run` check, and the publish step. (`doc_inspection`)
  - Following the documented steps on the current workspace reaches a successful set of per-crate dry-runs.
    (`publishability`)
- **Stage:** one_oh · **Release gating:** true
- **References:** `REQ-REL-005`, `REQ-REL-008`, `REQ-REL-009`; the changelog practice (`REQ-REL-020..039`,
  `SUBTASK_semver_changelog`).

### Published-manifest hygiene

#### REQ-REL-011 — Published manifests carry only resolvable crates.io version requirements
- **Statement:** Every dependency recorded in a published crate's manifest resolves from crates.io at a real version
  requirement — no path-only or git-only requirement reaches the published crate.
- **Rationale:** A consumer running `cargo add ferric` gets the published manifest; any dependency there that cannot
  resolve from crates.io (a bare path, a git revision) makes the crate uninstallable, defeating `REQ-FW-001`. The
  path→version conversion of `REQ-REL-004` is the specific case; this requirement is the general invariant across all
  dependencies (including the direct crates.io dependencies `ferric-http` already declares — `serde`, `serde_json`,
  `wasm-bindgen-futures`). The Rust API Guidelines' C-PERMISSIVE note that a crate's distribution is constrained by its
  dependencies' licenses also lands here: a published crate should depend only on permissively-licensed,
  registry-resolvable crates.
- **Acceptance criteria:**
  - In each crate's packaged manifest, every normal (non-dev) dependency carries a version requirement resolvable from
    crates.io; none is path-only or git-only. (`publishability`)
  - A `cargo add` of each published crate into a fresh project resolves and builds without a git or path override.
    (`automated_test`)
- **Stage:** one_oh · **Release gating:** true
- **References:** `REQ-REL-004`; `REQ-FW-001`; `REQ-FW-013` (lean, justified dependency set, measured under
  `REQ-PERF-*`).

---

## Coverage of the brief's four facets

| Facet from the brief | Covered by |
|---|---|
| The license gap (no license/LICENSE anywhere) | `REQ-REL-001`, with files shipped by `REQ-REL-006` |
| The metadata gaps (keywords/categories/documentation/homepage/readme) | `REQ-REL-002`, `REQ-REL-003` |
| The path→version dependency conversion (`ferric-router` → `ferric`) | `REQ-REL-004`, `REQ-REL-011` |
| The multi-crate workspace release order & coordination | `REQ-REL-007`, `REQ-REL-008`, `REQ-REL-009`, `REQ-REL-010` |
| `cargo publish` / `cargo package` readiness (incl. `todo!()`) | `REQ-REL-005`, `REQ-REL-006` |

---

## Peer and standards grounding

**crates.io / Cargo (the registry's own rules).** The Cargo book's *Publishing on crates.io* names `license` or
`license-file` and `description` as fields that must be filled out, recommends `homepage`, `repository`, and `readme`,
and recommends running `cargo publish --dry-run` (equivalent to `cargo package`) first — it verifies the package,
builds the `.crate`, and compiles it in a temp directory. The Cargo book's *Specifying Dependencies* is the source for
the path→version rule: a path dependency must also carry a `version` to be publishable, because the published crate
resolves that dependency from the registry. docs.rs builds and hosts each published crate's documentation
automatically, which is why `REQ-REL-003` makes the docs.rs build a gating condition.

**Rust API Guidelines (ecosystem convention).** The *Necessities* chapter's C-PERMISSIVE recommends
`license = "MIT OR Apache-2.0"` with both `LICENSE-APACHE` and `LICENSE-MIT` at the repository root and a license
section in the README, for maximum ecosystem compatibility, and notes that a crate's distribution is constrained by
its dependencies' licenses (so a permissive crate should depend only on permissive crates — reflected in
`REQ-REL-011`). C-METADATA calls for complete Cargo.toml metadata (`REQ-REL-002`).

**Named Rust peers (how comparable frameworks publish).** Leptos, Dioxus, and Yew are all distributed as **multi-crate
workspaces on crates.io**: a core crate plus companion crates (a router among them — `leptos_router`, `dioxus-router`,
`yew-router`), published under permissive licenses (the `MIT OR Apache-2.0` convention above; Leptos under MIT) and
released as a coordinated set with their crates versioned together. This is the pattern `REQ-REL-008` and
`REQ-REL-009` hold Ferric to: a dependency on crates.io before its dependents, and one coordinated lockstep version
across the workspace. Each peer also carries full crates.io metadata and working docs.rs pages, which an evaluating
author (persona A1) uses to judge the framework — the bar `REQ-REL-002` and `REQ-REL-003` set.

---

## Metadata

- **Owning task:** `SUBTASK_publishing` (owns `REQ-REL-001..019`; identities J1–J3). This partial is a source
  `SUBTASK_rel_synthesis` merges into `release-and-distribution.md`.
- **Register:** `REQ-REL-001` .. `REQ-REL-011` defined here; `REQ-REL-012` .. `REQ-REL-019` unused (reserved within
  this spoke's range, no gaps claimed as defined). All are `stage: one_oh`, `release_gating: true`.
- **Verification methods used:** `publishability`, `doc_inspection`, `automated_test` (all from the parent closed
  vocabulary; identity J3).
- **Conforms to:** `../../contracts/id_and_traceability_schema.yaml` (REQ fields, `verification_method` + `stage`
  vocabularies, `release_gating`); `../contracts/_MANIFEST.yaml` (the `REQ-REL-001..019` partition and merge
  identities J1–J7).
- **Cross-references** to `REQ-FW-*` (owned by `SUBTASK_scope_and_requirements`) and to the sibling `REQ-REL-020..039`
  (semver + changelog) and `REQ-REL-040..059` (versioning/compatibility) ranges are read-only; those registers are
  owned by their spokes and are not minted here.
- **Grounding commit:** `Nousix-LLC/nswe-demo` @ `276138f` (`main`).
