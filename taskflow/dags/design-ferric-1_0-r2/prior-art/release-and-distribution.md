# Ferric — Release & Distribution

This document designs how Ferric is released and distributed as a **1.0**: what it takes for each crate to be
**published to crates.io** and how the three-crate workspace is released together; the **semver contract** over
Ferric's frozen public surfaces and which changes are breaking versus additive; the **changelog practice** that
records each release so an author can upgrade without guessing; and the **versioning and compatibility policy** a
1.0 promises — the MSRV, the frozen-`prelude` stability guarantee, additive-only evolution across the 1.x line, and
cross-crate version coordination. Every part is stated as a testable `REQ-REL-*` requirement.

**What this document settles, and what it does not.** It settles *what must be true* of the published crates, their
version numbers, their changelog, and the policy an author reads before depending on them — the bar a stranger could
check against crates.io, `cargo`, and the repository. It does not settle *how* any of it is built: a publishing
script or `cargo-release` / `release-plz`, a changelog generator, a CI semver gate — each is deferred to a later
code DAG. The release *bar* (`BAR-FERRIC-*`) and the release *plan* (epics and work-items) are owned by
`SUBTASK_release_bar` and `SUBTASK_release_plan` at the framework level; this document supplies the `REQ-REL-*`
they reference.

**What, not how.** Each requirement reads as a condition on the published crates and the `cargo` commands that
produce them, verifiable by someone who was not in the room — a classification a reviewer can apply, a gate that
blocks an unsignalled break, a field crates.io demands, a promise written where an author will find it.

**Grounding.** Observations of "Ferric as it exists today" are grounded in `Nousix-LLC/nswe-demo` @ `main` (baseline
`276138f`), confirmed against the live workspace, crate manifests, and `prelude` surfaces at design time:

- The root `Cargo.toml` is a **virtual workspace** (`members = ["crates/*"]`, `resolver = "2"`) with
  `[workspace.package] version = "0.1.0"`, `edition = "2021"`, `rust-version = "1.82"`, and
  `repository = "https://github.com/Nousix-LLC/nswe-demo"`. The three Ferric crates (`ferric`, `ferric-router`,
  `ferric-http`) each inherit `version.workspace = true` and `rust-version.workspace = true`, so they version in
  lockstep at `0.1.0` and share one MSRV today.
- **No `license` or `license-file` field in any manifest, and no `LICENSE` file at the repo root** — crates.io will
  not publish a crate without a license. This is the headline publishing gap.
- **No `keywords`, `categories`, `documentation`, `homepage`, or explicit `readme` field** in any manifest. Each
  crate carries a `description`; a `README.md` exists at the repo root and in all three crate directories.
- `ferric-router` depends on `ferric` via `{ path = "../ferric" }` with **no `version`** — `cargo` refuses to
  publish a crate whose path dependency carries no version requirement. `ferric-http` has no intra-workspace
  dependency (it pulls `serde`, `serde_json`, and `wasm-bindgen-futures` from crates.io directly).
- **No `CHANGELOG.md`** anywhere in the repository (zero matches) — the changelog practice is designed from zero,
  not amended onto an existing one.
- The frozen public surfaces this concern governs are the `prelude` modules: `ferric::prelude` (`Component`,
  `mount`, `batch`, `create_effect`, `create_memo`, `create_signal`, `Memo`, `Signal`, `EventKind`, `VElement`,
  `VNode`); `ferric_router::prelude` (`link`, `Params`, `RoutePattern`, `Router`, `navigate`, `current_path`); and
  `ferric_http`'s top-level re-exports plus `prelude` (`Client`, `ClientBuilder`, `Error`, `Method`,
  `RequestBuilder`, `Response`, `Result`). Many leaf bodies are still `todo!()`; the public *shape* is fixed. A
  `todo!()` body is a compiling expression, so a frozen-but-unimplemented surface still builds and packages.

**Standards and references, cited by name.** The Cargo book's *Publishing on crates.io* and *Specifying
Dependencies*; the Cargo book's *SemVer Compatibility* chapter; Semantic Versioning 2.0.0; RFC 1105 (API evolution)
and the Rust API Guidelines (C-PERMISSIVE, C-METADATA, the MSRV discussion rust-lang/api-guidelines #231); RFC 2495
(the `rust-version` field) and RFC 3537 (the MSRV-aware resolver); Keep a Changelog 1.1.0; `cargo-semver-checks`;
and docs.rs (automatic documentation build on publish). Peer practice is compared by name — Leptos, Dioxus, Yew —
in §5.

The five sections below are the required content of this artifact: publishing readiness and multi-crate release
(§1, `REQ-REL-001..019`); the semver contract (§2, `REQ-REL-020..029`); the changelog practice (§3,
`REQ-REL-030..039`); the versioning and compatibility policy (§4, `REQ-REL-040..059`); and the named-peer and
standards comparison (§5). Conformance: `../contracts/id_and_traceability_schema.yaml`.

---

## 1. Publishing readiness & multi-crate release

*(section: `publishing_readiness_and_release`, `REQ-REL-001..019`)*

Someone adopting Ferric runs `cargo add ferric` and expects a published, semver-versioned crate to resolve. Someone
releasing Ferric runs `cargo publish` for each crate and expects it to succeed. Between those two sits everything
this section designs: the metadata crates.io demands, the license it will not publish without, the path→version
conversion that lets an intra-workspace dependency be published at all, the `cargo package` checks each crate must
pass, and the order and coordination a three-crate workspace release requires. Every requirement here is
`stage: one_oh`, `release_gating: true` — crates.io publishing is the 1.0 add over the `usable_early` floor
(`REQ-FW-001`).

### Licensing

#### REQ-REL-001 — Every published crate declares a permissive license
- **Statement:** Each Ferric crate published to crates.io declares a license in its manifest, and the chosen license
  is a permissive one compatible with the Rust ecosystem.
- **Rationale:** crates.io will not publish a crate that declares neither `license` nor `license-file` (Cargo book,
  *Publishing on crates.io*, lists `license` or `license-file` among the fields that must be filled out). This is the
  one gap that blocks publishing outright today — no manifest has a license and there is no `LICENSE` file. The Rust
  API Guidelines (C-PERMISSIVE) recommend `license = "MIT OR Apache-2.0"` with both `LICENSE-APACHE` and `LICENSE-MIT`
  at the repository root for maximum ecosystem compatibility; Ferric's Rust peers publish under the same permissive
  convention (see §5). A permissive choice also keeps `REQ-REL-011`'s "depend only on permissively-licensed crates"
  tractable.
- **Acceptance criteria:**
  - Every published crate's `Cargo.toml` carries a `license` (an SPDX expression) or a `license-file`; the same
    expression is used across the three crates. (`doc_inspection`)
  - `cargo publish --dry-run` no longer fails for a missing-license reason for any crate. (`publishability`)
  - If the `MIT OR Apache-2.0` convention is taken, the corresponding `LICENSE-APACHE` and `LICENSE-MIT` files exist
    where the manifests reference them and the README states the license. (`doc_inspection`)
- **Verification:** `doc_inspection`, `publishability`
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
  An evaluating author (persona A1) judges a framework in an afternoon from its crates.io landing page; missing
  keywords/categories make it undiscoverable and a missing repository/docs link reads as unfinished. Today only
  `description` is present. `readme` need not be set explicitly if a `README.md` sits beside the manifest (Cargo
  auto-detects it) — the requirement is that the rendered crate shows a README, however that resolves.
- **Acceptance criteria:**
  - Each published crate's manifest (or workspace-inherited metadata) provides `description`, `repository`,
    `documentation`, `homepage`, `keywords`, and `categories`, and the crate renders a README on crates.io.
    (`doc_inspection`)
  - `categories` uses only slugs from the crates.io category list, and `keywords`/`categories` stay within
    crates.io's count limits, so publishing is not rejected for an invalid category or too many keywords.
    (`publishability`)
  - The three crates' metadata is consistent where it should be (shared `repository`, coherent keyword set), and each
    `description` reads as that crate's own one-line summary. (`doc_inspection`)
- **Verification:** `doc_inspection`, `publishability`
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
  declared in `[package.metadata.docs.rs]` rather than left to fail. The workspace already enforces
  `missing_docs = "warn"`, so the public surface is documented.
- **Acceptance criteria:**
  - `cargo doc --no-deps` builds the public API docs for each crate without error on the target docs.rs will use
    (the default host target, or the target declared in `[package.metadata.docs.rs]`). (`automated_test`)
  - After publish, each crate's docs.rs page renders the public `prelude` surface, and the crate's `documentation`
    field (`REQ-REL-002`) resolves to it. (`doc_inspection`)
- **Verification:** `automated_test`, `doc_inspection`
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
- **Verification:** `doc_inspection`, `publishability`, `automated_test`
- **Stage:** one_oh · **Release gating:** true
- **References:** `REQ-FW-001`; the versioning/compatibility policy (`REQ-REL-040..059`) owns how the version
  requirement is kept coherent across the workspace; `REQ-REL-009` (lockstep release).

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
- **Verification:** `publishability`
- **Stage:** one_oh · **Release gating:** true
- **References:** `REQ-REL-001`, `REQ-REL-004`, `REQ-REL-006`.

#### REQ-REL-006 — The packaged crate contains the license, README, and only intended files
- **Statement:** Each crate's packaged `.crate` archive contains the files a consumer and crates.io need — the
  source, the README, and the license file(s) the manifest references — and excludes files that do not belong in a
  published crate.
- **Rationale:** A published crate is self-contained: a `license-file`, or the `LICENSE-APACHE`/`LICENSE-MIT` files a
  `MIT OR Apache-2.0` crate ships, must be inside the `.crate` or the published crate has no license text even though
  the manifest names one; the README shown on crates.io must likewise be packaged. Because the crates live under
  `crates/*` in a virtual workspace, each crate's package must pull in the files it needs from its own directory
  (Cargo packages per-crate, not the whole workspace). Keeping stray or large non-source files out holds the WASM
  framework's published footprint to the source that belongs in it, consistent with the lean-footprint intent
  (`REQ-FW-013`).
- **Acceptance criteria:**
  - `cargo package --list` for each crate shows its source, its README, and the license file(s) its manifest
    references, and does not list unintended files. (`doc_inspection`)
  - For a `MIT OR Apache-2.0` crate, both license files are present in each crate's package (via repo-root files made
    available to each crate, a per-crate copy, or a `license-file` path that resolves in the package).
    (`publishability`)
- **Verification:** `doc_inspection`, `publishability`
- **Stage:** one_oh · **Release gating:** true
- **References:** `REQ-REL-001`; `REQ-REL-002`; `REQ-FW-013` (lean footprint, measured under `REQ-PERF-*`).

### Multi-crate workspace release

#### REQ-REL-007 — The crate names are owned on crates.io
- **Statement:** The names `ferric`, `ferric-router`, and `ferric-http` (and any new 1.0 crate) are registered to and
  owned by the project on crates.io before the 1.0 release depends on them.
- **Rationale:** crates.io names are first-come and permanent; a 1.0 that promises `cargo add ferric` cannot rest on
  a name the project does not control, and the first publish of each crate is what claims the name. Confirming
  ownership (or that the name is free and claimed by an initial publish) removes a late, unrecoverable surprise where
  a name is already taken. This is a publishing-readiness fact independent of the crate contents.
- **Acceptance criteria:**
  - Each crate name resolves on crates.io to a crate owned by the project (or is confirmed unregistered and reserved
    by the initial 1.0 publish). (`doc_inspection`)
  - The manifest `name` of each crate matches the owned crates.io name. (`doc_inspection`)
- **Verification:** `doc_inspection`
- **Stage:** one_oh · **Release gating:** true
- **References:** `REQ-FW-001`.

#### REQ-REL-008 — Crates publish in dependency order
- **Statement:** A coordinated release publishes the crates in an order that respects their dependency graph: a crate
  is published only after every Ferric crate it depends on is already available on crates.io at the version it
  requires.
- **Rationale:** crates.io resolves a published crate's dependencies from the registry at publish time, so a
  dependent cannot be published before its dependency exists there at the required version. For Ferric the order is
  `ferric` first, then `ferric-router` (which depends on `ferric` per `REQ-REL-004`); `ferric-http` has no
  intra-workspace dependency and may publish independently. Peer multi-crate frameworks release their companion
  crates as a coordinated set for exactly this reason (see §5).
- **Acceptance criteria:**
  - The release publishes `ferric` before `ferric-router`; `ferric-http` has no Ferric dependency and orders freely.
    (`doc_inspection`)
  - Publishing the dependents succeeds because their required `ferric` version is already on crates.io — no publish
    fails for an unresolved intra-workspace dependency. (`publishability`)
  - The required order is derivable from the manifests (the dependency graph), not from tribal knowledge.
    (`doc_inspection`)
- **Verification:** `doc_inspection`, `publishability`
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
  (what a bump promises, the MSRV) are owned by the versioning/compatibility section (`REQ-REL-040..059`); this
  requirement fixes only the release mechanics: one version, released as a set.
- **Acceptance criteria:**
  - A release carries one version across all Ferric crates (the inherited `[workspace.package] version`), and all are
    published from the same release. (`doc_inspection`)
  - No Ferric crate is published at a version out of step with its siblings for the same release. (`publishability`)
- **Verification:** `doc_inspection`, `publishability`
- **Stage:** one_oh · **Release gating:** true
- **References:** `REQ-REL-004`, `REQ-REL-008`; the versioning/compatibility policy (`REQ-REL-040..059`) owns the
  MSRV and the meaning of a version bump; the semver contract (`REQ-REL-020..039`) owns breaking-vs-additive
  classification.

#### REQ-REL-010 — A documented, repeatable release procedure
- **Statement:** The repository documents the steps to cut a coordinated workspace release — set the version, the
  publish order, the per-crate dry-run, and the publish — so a release can be performed the same way by someone who
  did not design it.
- **Rationale:** A three-crate release with an ordering constraint and a shared version is error-prone when it lives
  in one person's memory; a written procedure is what makes the release repeatable and reviewable, and is the
  publishing counterpart to the changelog practice in §3. This is a documentation requirement, not an automation
  requirement — whether the steps are later encoded in a script or a CI job is left to a code DAG.
- **Acceptance criteria:**
  - A reviewer finds a release procedure in the repository that states the version bump, the `ferric`-before-
    `ferric-router` publish order, the per-crate `cargo publish --dry-run` check, and the publish step.
    (`doc_inspection`)
  - Following the documented steps on the current workspace reaches a successful set of per-crate dry-runs.
    (`publishability`)
- **Verification:** `doc_inspection`, `publishability`
- **Stage:** one_oh · **Release gating:** true
- **References:** `REQ-REL-005`, `REQ-REL-008`, `REQ-REL-009`; the changelog practice (`REQ-REL-030..033`).

### Published-manifest hygiene

#### REQ-REL-011 — Published manifests carry only resolvable crates.io version requirements
- **Statement:** Every dependency recorded in a published crate's manifest resolves from crates.io at a real version
  requirement — no path-only or git-only requirement reaches the published crate.
- **Rationale:** A consumer running `cargo add ferric` gets the published manifest; any dependency there that cannot
  resolve from crates.io (a bare path, a git revision) makes the crate uninstallable, defeating `REQ-FW-001`. The
  path→version conversion of `REQ-REL-004` is the specific case; this requirement is the general invariant across all
  dependencies (including the direct crates.io dependencies `ferric-http` already declares — `serde`, `serde_json`,
  `wasm-bindgen-futures`). The Rust API Guidelines' C-PERMISSIVE note that a crate's distribution is constrained by
  its dependencies' licenses also lands here: a published crate should depend only on permissively-licensed,
  registry-resolvable crates.
- **Acceptance criteria:**
  - In each crate's packaged manifest, every normal (non-dev) dependency carries a version requirement resolvable
    from crates.io; none is path-only or git-only. (`publishability`)
  - A `cargo add` of each published crate into a fresh project resolves and builds without a git or path override.
    (`automated_test`)
- **Verification:** `publishability`, `automated_test`
- **Stage:** one_oh · **Release gating:** true
- **References:** `REQ-REL-004`; `REQ-FW-001`; `REQ-FW-013` (lean, justified dependency set, measured under
  `REQ-PERF-*`).

---

## 2. The semver contract

*(section: `semver_contract`, `REQ-REL-020..039`, part one — `020..029`)*

A semver promise is only as meaningful as the surface it is made over and the classification that decides whether a
change touched it. This section defines the governed public surface, what each semver level promises for the 1.0
line, and the breaking-vs-additive classification a reviewer and a mechanical checker apply — grounded in the Cargo
book's *SemVer Compatibility* chapter and RFC 1105.

### The governed surface

#### REQ-REL-020 — The public API each crate's semver promise covers is defined and enumerable
- **Statement:** Each Ferric crate has a defined public API — the set of items an app author may name — that the
  semver contract governs, and that set is the crate's `prelude` module (plus `ferric-http`'s top-level re-exports).
  Items reachable only through a non-public path or marked `#[doc(hidden)]` are internal and carry no semver promise.
- **Rationale:** Breaking-vs-additive is undecidable without a fixed boundary for what is public. The baseline
  already froze these `prelude` surfaces and apps are written against them, so the boundary already exists in the
  code; the contract names it so a reviewer (and a mechanical checker) can enumerate exactly what must not break
  silently. Drawing the line at the `prelude` also keeps the internal `todo!()` bodies and helper modules free to
  change at patch level.
- **Acceptance criteria:** For each of `ferric`, `ferric-router`, `ferric-http`, the repository states which
  module(s) constitute the public API the semver contract covers, and the enumerated set matches the items actually
  exported there. A reviewer can list the governed items from the documentation and confirm the list equals the
  crate's exported public surface; a tool that snapshots the public API (for example `cargo-semver-checks`'s
  baseline, or `cargo public-api`) reports the same set.
- **Verification:** `doc_inspection`, `automated_test`
- **Stage:** one_oh · **Release gating:** true
- **References:** `REQ-FW-009`, `REQ-FW-010` (read-only); `REQ-REL-040..059` (frozen-`prelude` stability promise).
  Standards: Cargo book *SemVer Compatibility*.

### The semver level contract

#### REQ-REL-021 — Each semver level has a defined meaning for the public surface
- **Statement:** For the 1.0 line, a **MAJOR** bump signals that the release contains at least one breaking change to
  the public surface; a **MINOR** bump signals only additive, backward-compatible changes (new public items, no
  removals or redefinitions); a **PATCH** bump signals no change to the public surface — bug fixes and
  behavior-preserving internal changes only. An author reading the version delta between two releases can tell, from
  the level alone, the strongest kind of change the release is permitted to contain.
- **Rationale:** This is what "governed by semver" in `REQ-FW-010` means in practice: the number is a contract, not a
  label. Library authors (persona A3) decide whether an upgrade is safe to take automatically from the level, so the
  level must carry a defined, enforced meaning rather than a maintainer's habit.
- **Acceptance criteria:** The repository documents, for the 1.0 line, what MAJOR, MINOR, and PATCH each permit and
  forbid with respect to the public surface, consistent with Semantic Versioning 2.0.0 and the Cargo book's SemVer
  chapter. A reviewer can map any one of the classified change kinds in `REQ-REL-023..025` to exactly one required
  minimum level using this statement.
- **Verification:** `doc_inspection`
- **Stage:** one_oh · **Release gating:** true
- **References:** `REQ-FW-010` (read-only); `REQ-REL-040..059` (the 0.x→1.0 transition and cross-crate coordination).
  Standards: Semantic Versioning 2.0.0; Cargo book *SemVer Compatibility*.

#### REQ-REL-022 — The pre-1.0 (0.x) semver convention is stated as the bridge to 1.0
- **Statement:** While Ferric is below 1.0 (today `0.1.0`), the Cargo 0.x convention holds: the leftmost non-zero
  component carries the breaking-change signal, so a breaking change bumps the **minor** (`0.y`) and an additive
  change bumps the **patch** (`0.y.z`). The contract states this so that pre-1.0 releases are versioned under a
  defined rule, and names 1.0 as the point at which the standard `MAJOR.MINOR.PATCH` meaning in `REQ-REL-021` takes
  effect.
- **Rationale:** Ferric is at `0.1.0` and will make pre-1.0 releases before the 1.0 cut; without a stated 0.x rule
  those releases are versioned ad hoc, and the classification in `REQ-REL-023..025` would have no level mapping to
  attach to. Cargo and SemVer 2.0.0 both define the 0.x behavior; stating it removes the ambiguity rather than
  leaving the first real consumer to infer it.
- **Acceptance criteria:** The repository states the 0.x versioning rule (breaking → minor bump, additive → patch
  bump) and the point at which 1.0 switches to the standard meaning. A reviewer can version a hypothetical pre-1.0
  breaking change and a pre-1.0 additive change correctly from the statement.
- **Verification:** `doc_inspection`
- **Stage:** one_oh · **Release gating:** true
- **References:** `REQ-REL-021`; `REQ-REL-040..059` (the actual 0.x→1.0 transition mechanics — this requirement
  states only the convention, not the transition plan). Standards: Semantic Versioning 2.0.0 §4; Cargo book
  *SemVer Compatibility*.

### Breaking-vs-additive classification

#### REQ-REL-023 — Breaking (major) changes are classified
- **Statement:** A change to the public surface is **breaking** (requires a MAJOR bump at 1.0) when it can stop a
  conforming downstream crate from compiling or change the documented behavior it relies on. The classification names
  at least: removing or renaming a public item (function, type, trait, variant, field, module, or re-export);
  changing a function or method signature (parameters, return type, or a tightened bound); adding a required trait
  method without a default; adding a variant to an enum that is not `#[non_exhaustive]`; adding a field to, or making
  newly public, a struct whose existing fields are all public and that is not `#[non_exhaustive]`; and making a
  previously public item private or `#[doc(hidden)]`.
- **Rationale:** This is the operative content of the semver contract — the list a reviewer applies to a pull
  request. It is grounded in the Cargo book's "major change" catalogue and RFC 1105 so the classification matches
  what the Rust ecosystem already means by a breaking change, rather than a Ferric-local definition an author would
  have to relearn. `REQ-FW-009` promises the frozen `prelude` surfaces are carried forward additively; this
  requirement defines precisely what would violate that promise.
- **Acceptance criteria:** The repository lists the change kinds that require a MAJOR bump, covering at least the
  cases above and marked as consistent with the Cargo book's SemVer chapter. A reviewer handed a diff of the public
  surface can classify each changed item as breaking or not using the list, and `cargo-semver-checks` (`REQ-REL-026`)
  flags the mechanically detectable members of the list.
- **Verification:** `doc_inspection`, `automated_test`
- **Stage:** one_oh · **Release gating:** true
- **References:** `REQ-FW-009` (read-only); `REQ-REL-026`. Standards: Cargo book *SemVer Compatibility*; RFC 1105.

#### REQ-REL-024 — Additive (minor) changes are classified
- **Statement:** A change is **additive** (requires only a MINOR bump at 1.0) when it extends the public surface
  without breaking a conforming downstream crate. The classification names at least: adding a new public item (a new
  export, function, method, type, or module); adding a defaulted method to an existing trait; adding a variant to a
  `#[non_exhaustive]` enum; and adding a field to a `#[non_exhaustive]` struct or one with a private field. Additive
  changes are the only changes a MINOR release may contain.
- **Rationale:** `REQ-FW-009` commits the frozen surfaces to additive-only evolution; this requirement defines what
  "additive" admits, so "extend, never silently redefine" is checkable rather than aspirational. It is the
  counterpart to `REQ-REL-023`: together they let a reviewer sort any public-surface change into exactly one of
  breaking, additive, or neither.
- **Acceptance criteria:** The repository lists the change kinds that are additive and permitted in a MINOR release,
  covering at least the cases above and consistent with the Cargo book's SemVer chapter. A reviewer can confirm a
  stated additive change (for example a new helper method on `ClientBuilder`) is classified MINOR and requires no
  MAJOR bump.
- **Verification:** `doc_inspection`, `automated_test`
- **Stage:** usable_early · **Release gating:** true
- **References:** `REQ-FW-009` (read-only); `REQ-REL-027`. Standards: Cargo book *SemVer Compatibility*; RFC 1105.

#### REQ-REL-025 — Patch changes, and the `todo!()` fill-in case, are classified
- **Statement:** A change is a **PATCH** when it leaves the public surface unchanged — a bug fix, a documentation
  correction, or a behavior-preserving internal change. Filling in a body that was `todo!()` at the baseline (making
  a frozen-signature function actually do what its signature and docs describe) is a PATCH when the signature and
  documented contract are unchanged: the `todo!()` panic was never a promised behavior, so replacing it with the
  specified behavior fixes a defect rather than changing the contract. A fill-in that must change the signature or
  the documented behavior to work is classified by `REQ-REL-023`/`REQ-REL-024` instead.
- **Rationale:** Ferric is distinctive here: its public shape is frozen but many bodies are still `todo!()`, so a
  large part of the 1.0 work is filling them in. Without an explicit rule, each fill-in invites a case-by-case semver
  argument. Anchoring the rule to "the signature and documented contract are the promise, the panic is not" keeps the
  common case (implement a stub as specified) at PATCH while still catching the case where implementing the stub
  forces a surface change.
- **Acceptance criteria:** The repository states the PATCH classification and the `todo!()` fill-in rule. A reviewer
  can take a stated example — a `ferric-router` or `ferric-http` function whose `todo!()` body is implemented to its
  documented signature — and confirm it is classified PATCH, and take a second example whose correct implementation
  requires a signature change and confirm it is classified MAJOR.
- **Verification:** `doc_inspection`
- **Stage:** one_oh · **Release gating:** true
- **References:** `REQ-REL-023`, `REQ-REL-024`; §Grounding (the `todo!()` bodies at `276138f`). Standards: Cargo book
  *SemVer Compatibility*.

#### REQ-REL-026 — A breaking change is caught mechanically, not by reviewer memory alone
- **Statement:** The classification in `REQ-REL-023` is enforced by a mechanical check that compares a release's
  public API against the previously published version and reports any breaking change, so an unsignalled break cannot
  reach a published release silently. `cargo-semver-checks` is named as that check.
- **Rationale:** A written classification that depends on every reviewer remembering it fails the way the absent
  changelog failed — silently. The ecosystem's standard answer is `cargo-semver-checks`, which lints the public API
  diff against the SemVer rules; naming it as the required check turns "we classify breaking changes" into "a break
  that is not matched by a MAJOR bump is reported before release." This is a requirement's acceptance method, not an
  instruction to build a CI job — the implementation is a later code DAG's work.
- **Acceptance criteria:** `cargo-semver-checks` (or an equivalent that lints the public-API diff against the SemVer
  rules) runs against each crate comparing the release to its prior published version, and a release whose
  public-surface change is breaking but whose version bump is not MAJOR is reported as a violation. A reviewer can
  confirm the check is part of the stated release procedure and can reproduce a flagged break on a stated example.
- **Verification:** `automated_test`
- **Stage:** one_oh · **Release gating:** true
- **References:** `REQ-REL-023`; `REQ-REL-001..019` (the release procedure the check runs within). Standards:
  `cargo-semver-checks`; Cargo book *SemVer Compatibility*.

#### REQ-REL-027 — Public enums and structs are future-proofed so later additions stay additive
- **Statement:** Public enums and structs on the frozen surface that are expected to gain members after 1.0 are
  marked `#[non_exhaustive]` (or given an equivalent sealed-extension pattern) before the 1.0 freeze, so that adding
  a variant or field later is an additive (MINOR) change rather than a breaking (MAJOR) one. `EventKind` (new event
  kinds will be added as event coverage grows) and `Method` are the named candidates; the contract states which
  public types are frozen as exhaustive and which are open.
- **Rationale:** This decision can only be made *before* 1.0: once an exhaustive enum ships in 1.0, adding a variant
  is a breaking change forever on that line, so an un-future-proofed `EventKind` would force a 2.0 just to add a DOM
  event. `REQ-FW-006` commits the 1.0 to the full DOM event range, which means `EventKind` will grow; marking it
  `#[non_exhaustive]` now is what lets that growth stay additive under `REQ-REL-024`. This is a design requirement on
  the surface, stated as "what" (which types are open), not a code change made here.
- **Acceptance criteria:** The repository states, for each public enum and struct on the governed surface, whether it
  is frozen exhaustive or `#[non_exhaustive]`, with a reason for the types expected to grow (at least `EventKind` and
  `Method`). A reviewer can confirm a stated post-1.0 addition of an `EventKind` variant is classified MINOR under
  this decision, and `cargo-semver-checks` agrees.
- **Verification:** `doc_inspection`, `automated_test`
- **Stage:** usable_early · **Release gating:** true
- **References:** `REQ-FW-006`, `REQ-FW-009` (read-only); `REQ-REL-024`, `REQ-REL-026`. Standards: Cargo book
  *SemVer Compatibility*; Rust API Guidelines (future-proofing).

#### REQ-REL-028 — Behavior documented for a public item is part of the semver contract
- **Statement:** The semver contract covers documented behavior, not only type signatures. A change that keeps a
  signature intact but alters the behavior its documentation promises, in a way a conforming downstream crate relies
  on, is a breaking change under `REQ-REL-023`. A public item's documented contract is therefore what the release
  promises to preserve across MINOR and PATCH releases.
- **Rationale:** Signature-only semver misses the breaks that hurt most: a router that silently changes how it
  matches a path parameter, or a client that changes how it treats a non-2xx status, breaks callers without changing
  a single type. Tying the contract to documented behavior is what the Cargo book's "behavioral changes" guidance and
  RFC 1105 intend; it also makes the acceptance criteria of other areas (for example the router and HTTP behavior in
  `REQ-RT-*` / `REQ-HTTP-*`) the behavior the semver contract protects.
- **Acceptance criteria:** The repository states that documented behavior of a public item is covered by the semver
  contract and classified as breaking when changed incompatibly. A reviewer can take a stated behavior-only change to
  a public item (for example a changed error-handling rule) and confirm it is classified MAJOR even though the
  signature is unchanged.
- **Verification:** `doc_inspection`
- **Stage:** one_oh · **Release gating:** true
- **References:** `REQ-REL-023`. Standards: Cargo book *SemVer Compatibility* (behavioral changes); RFC 1105.

#### REQ-REL-029 — Removal of a public item is preceded by a deprecation
- **Statement:** A public item is not removed without first being marked `#[deprecated]`, with a note naming the
  replacement, in a released MINOR version; the removal itself happens only in a later MAJOR release. Adding the
  `#[deprecated]` attribute is an additive (MINOR) change; the removal is a breaking (MAJOR) change recorded in the
  changelog under `REQ-REL-031`.
- **Rationale:** A 1.0 that removes items abruptly breaks the library authors (A3) it promised stability to, even
  when the removal is correctly signalled by a MAJOR bump. Deprecate-then-remove gives downstream crates a release in
  which the item still works but the compiler warns, so the upgrade can be staged. This is standard Rust practice
  (`#[deprecated]` is a language feature) and is what "a stable public API across a release line" in `REQ-FW-010`
  means in the removal case.
- **Acceptance criteria:** The repository states the deprecate-before-remove policy and the semver level of each
  step. A reviewer can confirm a stated removal was preceded by a `#[deprecated]` item in an earlier MINOR release
  whose changelog recorded the deprecation, and that the deprecated item still compiled (with a warning) in that
  release.
- **Verification:** `doc_inspection`, `automated_test`
- **Stage:** one_oh · **Release gating:** true
- **References:** `REQ-FW-010` (read-only); `REQ-REL-023`, `REQ-REL-031`. Standards: Rust API Guidelines; Cargo book
  *SemVer Compatibility*.

---

## 3. Changelog practice

*(section: `changelog_practice`, `REQ-REL-030..039`)*

The repository has no `CHANGELOG.md` today. A semver contract records the *level* of a change; the changelog records
*what* changed, so an author deciding whether and how to upgrade can read the actual change set rather than infer it
from a version number. The practice below follows Keep a Changelog 1.1.0 and ties each entry to the semver level the
change demands.

#### REQ-REL-030 — Every release records its changes in a maintained changelog
- **Statement:** Ferric maintains a changelog that records each release's changes in human-readable form, kept
  current as part of making a release, following the Keep a Changelog 1.1.0 structure: a reverse-chronological list
  of released versions each with its release date, plus an `Unreleased` section at the top for changes not yet
  released.
- **Rationale:** `REQ-FW-010` and journey JA5 require that an author can "read a changelog, understand what a version
  bump changes, and upgrade without silent breakage." No changelog exists today, so the practice is designed from
  zero. Keep a Changelog is the ecosystem's common structure and is what an evaluating author (A1) expects to find
  when judging whether the project is maintained.
- **Acceptance criteria:** The repository contains a changelog in Keep a Changelog form with per-version,
  date-stamped sections in reverse-chronological order and an `Unreleased` section; a reviewer can confirm a released
  version's section exists and matches that release, and that the structure follows Keep a Changelog 1.1.0.
- **Verification:** `doc_inspection`
- **Stage:** one_oh · **Release gating:** true
- **References:** `REQ-FW-010` (read-only); JA5. Standards: Keep a Changelog 1.1.0.

#### REQ-REL-031 — Each changelog entry states change type, affected crate, and whether it is breaking
- **Statement:** Each changelog entry is grouped under a Keep a Changelog change type — `Added`, `Changed`,
  `Deprecated`, `Removed`, `Fixed`, `Security` — names the crate(s) it affects, and marks whether the change is
  breaking or additive per the `REQ-REL-023..025` classification. An author scanning a release's entries can see
  which crate changed, in what way, and whether the change can affect their code.
- **Rationale:** A changelog that only lists commit subjects does not answer the author's real question — "will this
  upgrade break me, and where?" Grouping by change type and marking breaking-vs-additive makes the entry carry the
  classification of §2, so the changelog and the semver contract state the same facts in two forms. Naming the
  affected crate matters because the workspace ships three crates that version together (`REQ-REL-033`).
- **Acceptance criteria:** A reviewer can take a release's changelog section and, for each entry, read its change
  type, the crate(s) affected, and a breaking/additive marking; a `Removed` or breaking `Changed` entry is marked
  breaking and an `Added` entry is marked additive, consistent with §2.
- **Verification:** `doc_inspection`
- **Stage:** one_oh · **Release gating:** true
- **References:** `REQ-REL-023`, `REQ-REL-024`, `REQ-REL-033`. Standards: Keep a Changelog 1.1.0.

#### REQ-REL-032 — A release's semver level is justified by its changelog entries
- **Statement:** The semver level of a release is consistent with, and derivable from, its changelog entries: a
  release containing any `Removed` entry or any breaking-marked `Changed` entry is a MAJOR release; a release whose
  strongest entry is an additive `Added` or `Deprecated` is a MINOR release; a release containing only `Fixed` (and
  no public-surface change) is a PATCH release. The changelog and the version bump cannot disagree.
- **Rationale:** This is the seam between §2 and §3 — it makes the changelog the human-readable justification of the
  version number, and the version number a claim the changelog must support. It also gives the mechanical check in
  `REQ-REL-026` a documentary counterpart: where `cargo-semver-checks` proves the code's break is signalled, this
  proves the recorded change set agrees.
- **Acceptance criteria:** A reviewer can take any released version, read its changelog section, and confirm the
  version-level bump from the prior release is the minimum level the entries require under `REQ-REL-021`; a release
  with a `Removed` entry but a non-MAJOR bump, or a MINOR release with no additive entry, is a detectable
  inconsistency.
- **Verification:** `doc_inspection`
- **Stage:** one_oh · **Release gating:** true
- **References:** `REQ-REL-021`, `REQ-REL-026`, `REQ-REL-031`. Standards: Keep a Changelog 1.1.0; Semantic Versioning
  2.0.0.

#### REQ-REL-033 — The changelog covers the multi-crate workspace, with per-crate changes attributable
- **Statement:** The changelog records changes for all three crates (`ferric`, `ferric-router`, `ferric-http`), and a
  reader can attribute each change to the crate it affects. Because the crates version in lockstep today
  (`version.workspace = true`), a single workspace-level `CHANGELOG.md` with per-crate grouping within each release
  satisfies this; should a crate ever version independently, that crate carries its own `CHANGELOG.md`. The
  requirement fixes the outcome — per-crate attribution across the workspace — not a single file layout.
- **Rationale:** A workspace that ships three crates from one repository can hide which crate a change touched if the
  changelog is flat. The lockstep versioning observed at the baseline makes one workspace changelog with per-crate
  sections the simple fit, and it keeps the three crates' release notes in step with their shared version. Stating
  the requirement as "per-crate attribution" rather than "one file" leaves the layout to the implementer while
  keeping the testable property. The cross-crate *version-coordination* rule itself is owned by §4
  (`REQ-REL-040..059`); this requirement only governs how that coordination is recorded.
- **Acceptance criteria:** A reviewer can find, for a given release, the changes to each of the three crates and tell
  which crate each entry affects; where crates version in lockstep a single workspace changelog with per-crate
  grouping is accepted, and where a crate versions independently its own changelog is present.
- **Verification:** `doc_inspection`
- **Stage:** one_oh · **Release gating:** true
- **References:** `REQ-REL-030`, `REQ-REL-031`; `REQ-REL-040..059` (cross-crate version coordination); §Grounding
  (`version.workspace = true`). Standards: Keep a Changelog 1.1.0.

---

## 4. Versioning & compatibility policy

*(section: `versioning_and_compatibility_policy`, `REQ-REL-040..059`)*

This section designs the versioning and compatibility policy a Ferric 1.0 promises: the minimum Rust version it
supports and how that floor may move, what the frozen public `prelude` surfaces are guaranteed to do across the 1.x
line, that the surface evolves by addition only within 1.x, and how the three crates version and stay compatible with
one another. It is the *promise* a library author (persona A3) and an app author (A2) read before they depend on
Ferric and before they upgrade. The semver *mechanics* that classify a change and the changelog are §2 and §3; this
section is the policy those mechanics serve.

**Policy in brief.**
1. **MSRV.** 1.0 states a supported minimum Rust version and keeps it as a declared floor, not "whatever is latest."
   The floor may rise within 1.x, but only as a minor release, announced, and never silently.
2. **Frozen surfaces.** The public `prelude` surfaces carried from the baseline remain usable for the life of the 1.x
   line. Code that compiles against them at 1.0 keeps compiling against every later 1.x.
3. **Additive-only.** Within 1.x the public surface grows by addition. Removing or redefining a public item is a
   breaking change, and a breaking change is deferred to a future major (2.0).
4. **Cross-crate coordination.** `ferric`, `ferric-router`, and `ferric-http` version in lockstep and release
   together at one version, so an app author can depend on the set at a single 1.x version and trust the parts fit.
5. **Stated scope.** The promise covers the documented public surfaces. Items outside them are named as outside the
   1.x stability promise rather than left ambiguous.

#### REQ-REL-040 — 1.0 states a supported minimum Rust version (MSRV)
- **Statement:** Ferric 1.0 declares a minimum supported Rust version and every published crate builds on that
  version of stable Rust. The declared MSRV is discoverable from the crates themselves, not only from prose.
- **Rationale:** A "1.0" that does not say which Rust versions it supports leaves an app author (A2) and a library
  author (A3) guessing whether an upgrade of either Ferric or their toolchain will compile. The workspace already
  pins `rust-version = "1.82"` in `[workspace.package]`, so the floor exists; the requirement is that 1.0 commits to
  it as a promise. The `rust-version` field (RFC 2495, the minimum-supported-rust-version field) is the ecosystem's
  standard way to state this, and Cargo's MSRV-aware resolver (RFC 3537) reads it during dependency resolution so a
  consumer on an older stable toolchain still resolves a compatible version rather than failing to build. Peer
  frameworks declare an MSRV through this field and track recent stable rather than pinning an old floor — as
  reported by their published crates, Leptos sits around Rust 1.88, Yew around 1.84, and Dioxus around 1.83; Ferric's
  1.82 is consistent with that range.
- **Acceptance criteria:**
  - Each published crate (`ferric`, `ferric-router`, `ferric-http`) carries a `rust-version` field, and the
    repository states the supported-MSRV promise where an author will find it (the compatibility policy of
    `REQ-REL-046`). (`doc_inspection`)
  - A build of each crate on the declared MSRV toolchain targeting `wasm32-unknown-unknown` through the standard
    tooling succeeds. (`automated_test`)
- **Verification:** `doc_inspection`, `automated_test`
- **Stage:** one_oh · **Release gating:** true
- **References:** `REQ-FW-003` (stable Rust / standard toolchain, "compatible-version ranges are stated"),
  `REQ-FW-010` (compatibility policy); `REQ-REL-046` (where the promise is written).

#### REQ-REL-041 — How the MSRV may rise within the 1.x line
- **Statement:** The supported MSRV may increase within 1.x, but only in a minor release, and each increase is
  recorded so an author can see it before upgrading. Raising the MSRV within 1.x is not treated as a major-breaking
  change and does not require a 2.0.
- **Rationale:** Pinning an MSRV for the life of a major line would freeze Ferric out of compiler improvements for
  years; raising it without warning would break downstream builds silently. The Cargo book's *SemVer Compatibility*
  chapter classifies increasing the minimum required Rust version as a possibly-breaking change, and the Rust API
  Guidelines MSRV discussion (rust-lang/api-guidelines #231) gives the convention that a 1.0-and-above crate raising
  its MSRV bumps the minor version rather than the major. Stating this up front tells an author the one rule that
  matters: a Ferric minor upgrade may ask for a newer Rust, a patch upgrade never will. The semver level an MSRV
  change signals is owned by §2; this requirement is the compatibility-policy commitment that the floor moves this
  way and no other.
- **Acceptance criteria:**
  - The compatibility policy states that an MSRV increase occurs only in a minor (or major) release, never a patch,
    and is announced in the changelog for the release that makes it. (`doc_inspection`)
  - For any release that raises the declared `rust-version`, the version bump is at least a minor bump (checkable
    from the version numbers and the `rust-version` values across two released versions). (`automated_test`)
- **Verification:** `doc_inspection`, `automated_test`
- **Stage:** one_oh · **Release gating:** true
- **References:** `REQ-REL-020..039` (semver level of a change; changelog practice); `REQ-FW-010`.

#### REQ-REL-042 — The frozen `prelude` surfaces stay usable across 1.x
- **Statement:** The public `prelude` surfaces carried from the baseline remain usable for the whole 1.x line. Code
  that compiles against the 1.0 preludes continues to compile against every later 1.x release without change.
- **Rationale:** This is the policy side of `REQ-FW-009` (frozen surfaces carried forward additively). The baseline
  already froze the public shape of three preludes (enumerated in §Grounding). Apps are already written against
  these. A 1.0 whose preludes shifted under a minor or patch release would make "1.0" a number with no stability
  behind it. Many leaf bodies are still `todo!()`, but the public *shape* is fixed; this requirement is about that
  shape, not the not-yet-implemented behavior behind it (see `REQ-REL-047`).
- **Acceptance criteria:**
  - An example (or a `trybuild`-style compile test) that imports and uses the baseline `prelude` items of all three
    crates compiles against the 1.0 release and against a later 1.x release unchanged. (`automated_test`)
  - The compatibility policy names the `prelude` surfaces as the guaranteed-stable public API for 1.x.
    (`doc_inspection`)
- **Verification:** `automated_test`, `doc_inspection`
- **Stage:** one_oh · **Release gating:** true
- **References:** `REQ-FW-009` (frozen surfaces additive); `REQ-REL-043` (additive-only evolution); `REQ-RT-*`,
  `REQ-HTTP-*` (the per-crate surface detail, read-only).

#### REQ-REL-043 — The public surface evolves by addition only within 1.x
- **Statement:** Within the 1.x line the public API grows by addition — new exports, new methods, new optional
  parameters handled compatibly. Removing a public item, renaming it, or changing its type or documented behavior is
  a breaking change, and a breaking change is deferred to a future major version (2.0).
- **Rationale:** Additive-only evolution is what lets an author upgrade a minor release and trust their code still
  builds; it is the discipline that keeps the walking skeleton a dependable base while leaf bodies get implemented.
  The classification of which concrete changes are additive versus breaking is §2's (`REQ-REL-023..025`), grounded in
  the Cargo book's *SemVer Compatibility* chapter and the Rust API evolution guidelines; this requirement is the
  commitment that, having that classification, 1.x only ever makes additive changes and defers every breaking one.
  Peer frameworks follow the same rule across their crate families — Leptos, Dioxus, and Yew each reserve breaking
  public-API changes for a new major (or, pre-1.0, a new `0.x`) rather than shipping them mid-line.
- **Acceptance criteria:**
  - A public-API check (for example `cargo-semver-checks`, named by §2 as the mechanical gate) run between two 1.x
    releases reports no removed or redefined public item; any such finding blocks the release or forces a major bump.
    (`automated_test`)
  - The compatibility policy states the additive-only rule for 1.x and that removals/redefinitions are deferred to
    2.0. (`doc_inspection`)
- **Verification:** `automated_test`, `doc_inspection`
- **Stage:** one_oh · **Release gating:** true
- **References:** `REQ-FW-009`; `REQ-REL-020..039` (breaking-vs-additive classification, the semver gate);
  `REQ-REL-042`.

#### REQ-REL-044 — The crates version in lockstep and release together
- **Statement:** `ferric`, `ferric-router`, and `ferric-http` share one version number and are released together:
  every 1.0 release publishes all of them at the same version. 1.0 keeps the workspace's lockstep versioning
  (`version.workspace = true`) rather than letting the crates drift to independent version numbers.
- **Rationale:** The workspace inherits a single `[workspace.package] version` through `version.workspace = true`, so
  the crates version in lockstep today. Lockstep is the simplest contract an app author can hold: one version number
  describes the whole set, and there is no matrix of "which `ferric-router` works with which `ferric`" to reason
  about. This matches how the peer families ship — Leptos releases `leptos`, `leptos_router`, `leptos_meta` and the
  rest together at a shared version within a release, and Dioxus and Yew coordinate their companion crates the same
  way. Independent per-crate versioning (as in, for example, the Tokio family) buys finer-grained release cadence at
  the cost of a compatibility matrix; for a three-crate set designed and tested as one framework, lockstep is the
  better trade, and 1.0 commits to it. Allowing independent versions later would itself be a policy change for a
  future major.
- **Acceptance criteria:**
  - The compatibility policy states lockstep versioning for the 1.x line; the workspace manifest shows
    `version.workspace = true` and each crate inherits it. (`doc_inspection`)
  - A coordinated workspace release publishes `ferric`, `ferric-router`, and `ferric-http` at the same version
    (`cargo publish` succeeds for each at that version; release order per `REQ-REL-001..019`). (`publishability`)
- **Verification:** `doc_inspection`, `publishability`
- **Stage:** one_oh · **Release gating:** true
- **References:** `REQ-FW-010` (version-coordination rule); `REQ-REL-001..019` (multi-crate release order,
  path→version conversion); `REQ-REL-045`.

#### REQ-REL-045 — Cross-crate compatibility an app author can rely on
- **Statement:** An app author can depend on `ferric`, `ferric-router`, and `ferric-http` at the same 1.x version and
  trust that the three compose without version conflicts: a `ferric-router` 1.x and a `ferric-http` 1.x work with
  `ferric` 1.x, because the set is built, tested, and released together at that version.
- **Rationale:** `ferric-router` depends on `ferric` (today via a path dependency that §1 converts to carry a
  version); the router and HTTP client exist to compose with the view framework over the frozen surfaces. The
  compatibility an author needs is simple to state under lockstep: pick a 1.x version, use it for all three. This is
  the compatibility half of `REQ-FW-010` and the stability leg of journey JA5 ("rely on a public API that does not
  shift … with a documented compatibility policy across the multi-crate workspace").
- **Acceptance criteria:**
  - A stated example app that depends on all three crates at the same 1.x version builds and runs the described
    behavior (routing + a JSON request + rendering) over their public surfaces. (`example_build`)
  - The compatibility policy states that the three crates are compatible when taken at the same 1.x version and that
    this is the supported way to depend on the set. (`doc_inspection`)
- **Verification:** `example_build`, `doc_inspection`
- **Stage:** one_oh · **Release gating:** true
- **References:** `REQ-FW-007` (router + HTTP compose with the view framework), `REQ-FW-010`; `REQ-REL-044`;
  `REQ-REL-001..019` (the intra-workspace dependency carries a version).

#### REQ-REL-046 — The compatibility policy is written down and discoverable
- **Statement:** The versioning and compatibility policy for 1.0 — the MSRV promise and its raise rule, the
  frozen-surface guarantee, additive-only evolution, and cross-crate coordination — is written in the repository
  where an author will find it before depending on or upgrading Ferric, not left implicit in the version numbers.
- **Rationale:** `REQ-FW-010` requires a *documented* compatibility policy: a reader must be able to learn, from the
  repository, what a given version bump is allowed to change. Stating the policy in one discoverable place (a
  `COMPATIBILITY.md`, a documented section of the top-level README, or the published crate docs) is what turns the
  preceding requirements from internal intent into a promise an author can hold the project to. The semver level each
  change signals and the per-release change set live in §2 and §3; this requirement is that the *policy* itself is
  published alongside them.
- **Acceptance criteria:**
  - A reviewer finds, in the repository, a stated compatibility policy covering MSRV and its raise rule, the
    frozen-`prelude` guarantee, additive-only 1.x evolution, and lockstep cross-crate versioning; it is linked from
    where an author starts (README / crate docs). (`doc_inspection`)
- **Verification:** `doc_inspection`
- **Stage:** one_oh · **Release gating:** true
- **References:** `REQ-FW-010`; `REQ-REL-040`, `REQ-REL-041`, `REQ-REL-042`, `REQ-REL-043`, `REQ-REL-044`,
  `REQ-REL-045` (the policy content it collects); `REQ-REL-020..039` (semver + changelog it sits beside).

#### REQ-REL-047 — What the 1.x promise does not cover (stated, not implied)
- **Statement:** The 1.x stability promise covers the documented public `prelude` surfaces. It does not cover: items
  not re-exported in a `prelude`; the runtime behavior of leaf bodies still unimplemented (`todo!()`) at a given
  release, until the work-item that implements them lands; and anything placed behind a future unstable or
  experimental feature flag. These exclusions are named in the compatibility policy.
- **Rationale:** The baseline ships a fixed public *shape* with many `todo!()` leaf bodies, so a stability promise
  that did not separate "this API shape is stable" from "this behavior is implemented" would either overclaim
  (promising behavior that is not built yet) or get quietly narrowed later. Naming the exclusions is what keeps the
  promise accurate: an author knows exactly what is guaranteed and what is still moving. A hidden cut — discovering
  after adoption that some re-exported-looking item was never in scope — costs more trust than an exclusion stated
  plainly at 1.0. This keeps `REQ-REL-042`'s guarantee precise rather than aspirational.
- **Acceptance criteria:**
  - The compatibility policy states that the stability guarantee applies to the documented `prelude` surfaces, and
    names the three exclusions (non-prelude items, not-yet-implemented `todo!()` behavior, and future
    unstable-flagged APIs). (`doc_inspection`)
- **Verification:** `doc_inspection`
- **Stage:** one_oh · **Release gating:** true
- **References:** `REQ-REL-042` (the guaranteed surface); `REQ-FW-009`; `REQ-REL-046` (where the exclusions are
  written).

---

## 5. Named-peer and standards comparison

*(section: `peer_and_standards_comparison`)*

The publishing readiness, the semver contract, the changelog practice, and the compatibility policy above are not
invented for Ferric; they track what the Rust ecosystem and Ferric's named peers already do, so an evaluating author
(A1) meets a convention they recognize.

### The reference standards, cited by name

- **crates.io / Cargo (the registry's own rules).** The Cargo book's *Publishing on crates.io* names `license` or
  `license-file` and `description` as fields that must be filled out, recommends `homepage`, `repository`, and
  `readme`, and recommends running `cargo publish --dry-run` (equivalent to `cargo package`) first — it verifies the
  package, builds the `.crate`, and compiles it in a temp directory. The Cargo book's *Specifying Dependencies* is the
  source for the path→version rule (`REQ-REL-004`). docs.rs builds and hosts each published crate's documentation
  automatically (`REQ-REL-003`).
- **Rust API Guidelines (ecosystem convention).** C-PERMISSIVE recommends `license = "MIT OR Apache-2.0"` with both
  `LICENSE-APACHE` and `LICENSE-MIT` at the repository root and a license section in the README, and notes that a
  crate's distribution is constrained by its dependencies' licenses (reflected in `REQ-REL-001`, `REQ-REL-011`).
  C-METADATA calls for complete Cargo.toml metadata (`REQ-REL-002`). The MSRV discussion (rust-lang/api-guidelines
  #231) gives the convention that a ≥1.0 crate bumps its minor version on an MSRV increase (`REQ-REL-041`).
- **Semver and API evolution.** The semver level meanings follow Semantic Versioning 2.0.0; the breaking-vs-additive
  catalogue follows the Cargo book's *SemVer Compatibility* chapter (the Rust-specific enumeration of
  major-vs-minor changes, including the treatment of an MSRV increase as possibly-breaking) and the API-evolution
  direction of RFC 1105; the `rust-version` mechanism is RFC 2495 and the MSRV-aware resolver RFC 3537; the changelog
  structure follows Keep a Changelog 1.1.0; the mechanical break check is `cargo-semver-checks`, the ecosystem's tool
  for linting a crate's public-API diff against the SemVer rules.

### Leptos, Dioxus, Yew — how comparable frameworks publish and version

- **Multi-crate workspaces on crates.io.** Leptos, Dioxus, and Yew are each distributed as a core crate plus
  companion crates (a router among them — `leptos_router`, `dioxus-router`, `yew-router`), published under permissive
  licenses (the `MIT OR Apache-2.0` convention; Leptos under MIT) and released as a coordinated set with their crates
  versioned together. This is the pattern `REQ-REL-008`, `REQ-REL-009`, and `REQ-REL-044` hold Ferric to: a
  dependency on crates.io before its dependents, and one coordinated lockstep version across the workspace. Each peer
  also carries full crates.io metadata and working docs.rs pages, which an evaluating author uses to judge the
  framework — the bar `REQ-REL-002` and `REQ-REL-003` set.
- **MSRV through `rust-version`, tracking recent stable.** Each peer declares an MSRV through the `rust-version` field
  and tracks recent stable rather than pinning a conservative old floor — as reported by their published crate
  metadata around 2026, Leptos ≈ 1.88, Yew ≈ 1.84, Dioxus ≈ 1.83. Ferric's 1.82 is consistent with that range
  (`REQ-REL-040`). These figures are read as a recency pattern from the frameworks' published metadata, not a precise
  contemporaneous claim; the point they support is that none pins an old floor. **Tokio** is the named counter-example
  of independent per-crate versioning with a stated MSRV policy — the trade `REQ-REL-044` weighs and declines for a
  three-crate framework set.
- **Changelog and mechanical gating.** Leptos and Dioxus keep a repository `CHANGELOG.md`; Yew documents releases in
  its project documentation (`REQ-REL-030`). Each has made breaking changes across its pre-1.0 (`0.x`) line under the
  Cargo 0.x convention `REQ-REL-022` states — the normal shape for a framework still before 1.0, and the reason
  Ferric's contract states the 0.x rule explicitly. Ferric's choice to name `cargo-semver-checks` as a release gate
  (`REQ-REL-026`) matches the growing ecosystem practice of enforcing the classification mechanically rather than by
  review alone.

### Where Ferric differs

Ferric's `todo!()`-body situation (`REQ-REL-025`, `REQ-REL-047`) has no direct peer analogue — it comes from shipping
a frozen public shape ahead of its implementation — which is why the contract classifies the fill-in case and names
the not-yet-implemented behavior as outside the stability promise, rather than borrowing a peer's rule.

---

## Register summary

The complete `REQ-REL-*` register for release & distribution. Defined ids are contiguous within each owning area's
range; the gaps between areas (`REQ-REL-012..019`, `034..039`, `048..059`) are reserved-unused by the sub-contract's
range partition (`contracts/_MANIFEST.yaml`), held for additive amendment — not gaps in the defined register.

| Id | Covers | Concern | Stage | Gating | Verification |
|---|---|---|---|---|---|
| REQ-REL-001 | Every published crate declares a permissive license | publishing | one_oh | true | doc_inspection, publishability |
| REQ-REL-002 | Complete per-crate crates.io metadata | publishing | one_oh | true | doc_inspection, publishability |
| REQ-REL-003 | API docs build on docs.rs per crate | publishing | one_oh | true | automated_test, doc_inspection |
| REQ-REL-004 | Intra-workspace deps carry path + version | publishing | one_oh | true | doc_inspection, publishability, automated_test |
| REQ-REL-005 | Each crate passes `cargo publish --dry-run` | publishing | one_oh | true | publishability |
| REQ-REL-006 | Packaged crate contains license, README, only intended files | publishing | one_oh | true | doc_inspection, publishability |
| REQ-REL-007 | Crate names owned on crates.io | publishing | one_oh | true | doc_inspection |
| REQ-REL-008 | Crates publish in dependency order | publishing | one_oh | true | doc_inspection, publishability |
| REQ-REL-009 | Workspace releases as one lockstep version set | publishing | one_oh | true | doc_inspection, publishability |
| REQ-REL-010 | Documented, repeatable release procedure | publishing | one_oh | true | doc_inspection, publishability |
| REQ-REL-011 | Published manifests carry only resolvable version reqs | publishing | one_oh | true | publishability, automated_test |
| REQ-REL-020 | Governed public surface defined & enumerable | semver contract | one_oh | true | doc_inspection, automated_test |
| REQ-REL-021 | Semver level meanings for 1.0 | semver contract | one_oh | true | doc_inspection |
| REQ-REL-022 | 0.x convention as bridge to 1.0 | semver contract | one_oh | true | doc_inspection |
| REQ-REL-023 | Breaking (major) classification | semver contract | one_oh | true | doc_inspection, automated_test |
| REQ-REL-024 | Additive (minor) classification | semver contract | usable_early | true | doc_inspection, automated_test |
| REQ-REL-025 | Patch + `todo!()` fill-in classification | semver contract | one_oh | true | doc_inspection |
| REQ-REL-026 | Mechanical break check (`cargo-semver-checks`) | semver contract | one_oh | true | automated_test |
| REQ-REL-027 | `#[non_exhaustive]` future-proofing | semver contract | usable_early | true | doc_inspection, automated_test |
| REQ-REL-028 | Documented behavior is part of the contract | semver contract | one_oh | true | doc_inspection |
| REQ-REL-029 | Deprecate-before-remove | semver contract | one_oh | true | doc_inspection, automated_test |
| REQ-REL-030 | A maintained changelog per release | changelog practice | one_oh | true | doc_inspection |
| REQ-REL-031 | Entry type, crate, breaking marking | changelog practice | one_oh | true | doc_inspection |
| REQ-REL-032 | Semver level justified by changelog | changelog practice | one_oh | true | doc_inspection |
| REQ-REL-033 | Multi-crate changelog attribution | changelog practice | one_oh | true | doc_inspection |
| REQ-REL-040 | 1.0 states a supported MSRV | versioning/compat | one_oh | true | doc_inspection, automated_test |
| REQ-REL-041 | How the MSRV may rise within 1.x | versioning/compat | one_oh | true | doc_inspection, automated_test |
| REQ-REL-042 | Frozen `prelude` surfaces stay usable across 1.x | versioning/compat | one_oh | true | automated_test, doc_inspection |
| REQ-REL-043 | Public surface evolves by addition only within 1.x | versioning/compat | one_oh | true | automated_test, doc_inspection |
| REQ-REL-044 | Crates version in lockstep and release together | versioning/compat | one_oh | true | doc_inspection, publishability |
| REQ-REL-045 | Cross-crate compatibility an app author can rely on | versioning/compat | one_oh | true | example_build, doc_inspection |
| REQ-REL-046 | Compatibility policy written down and discoverable | versioning/compat | one_oh | true | doc_inspection |
| REQ-REL-047 | What the 1.x promise does not cover | versioning/compat | one_oh | true | doc_inspection |

**Register facts.** 33 requirements, ids `REQ-REL-001..011`, `020..033`, `040..047`. Every id is inside its owning
area's assigned range with no collision (sub-contract identity J1). Every requirement carries the parent schema's
fields (J2) and every acceptance criterion names a `verification_method` from the parent closed vocabulary —
`publishability`, `doc_inspection`, `automated_test`, `example_build` (J3). The four concerns are each covered by
more than one requirement (J4). The MSRV promise is stated by `REQ-REL-040` and the frozen-`prelude` stability
promise by `REQ-REL-042` (J5). Only `REQ-REL-*` ids are minted here, respecting parent identity I1.

---

## Metadata

- **Owning task:** `SUBTASK_release_and_distribution` (concern 7; owns the `REQ-REL-*` register). Merged from three
  spoke partials by `SUBTASK_rel_synthesis`: `publishing.md` (`SUBTASK_publishing`, `REQ-REL-001..019`),
  `semver-changelog.md` (`SUBTASK_semver_changelog`, `REQ-REL-020..039`), and `versioning-compat.md`
  (`SUBTASK_versioning_compat`, `REQ-REL-040..059`).
- **Repository target:** `design/ferric/release-and-distribution.md` (placed by `SUBTASK_design_pr`).
- **Conforms to:** `../contracts/id_and_traceability_schema.yaml` (REQ fields, the `verification_method` and `stage`
  vocabularies, `release_gating`); `../../contracts/_MANIFEST.yaml` (parent identity I1 — disjoint registers);
  `contracts/_MANIFEST.yaml` (the `REQ-REL-*` range partition and merge identities J1–J7).
- **Register summary:** defined ids `REQ-REL-001..011`, `REQ-REL-020..033`, `REQ-REL-040..047` — all
  `release_gating: true`, staged `one_oh` except `REQ-REL-024` and `REQ-REL-027` (`usable_early`). Reserved-unused:
  `REQ-REL-012..019`, `034..039`, `048..059` (held for additive amendment; no gap in the defined register).
- **Verification methods used:** `publishability`, `doc_inspection`, `automated_test`, `example_build` — all from the
  parent closed vocabulary.
- **Grounding commit:** `Nousix-LLC/nswe-demo` @ `276138f` (`main`) — workspace manifests, `prelude` surfaces,
  `version.workspace`/`rust-version.workspace`, the absent license/`LICENSE`, and the absent `CHANGELOG.md` confirmed
  from the live repository.
- **Standards cited:** Cargo book (*Publishing on crates.io*, *Specifying Dependencies*, *SemVer Compatibility*);
  Semantic Versioning 2.0.0; RFC 1105; RFC 2495; RFC 3537; Rust API Guidelines (C-PERMISSIVE, C-METADATA, #231);
  Keep a Changelog 1.1.0; `cargo-semver-checks`; docs.rs. Peers named: Leptos, Dioxus, Yew (with Tokio as the
  independent-versioning counter-example).
- **Cross-references** to `REQ-FW-*` (owned by `SUBTASK_scope_and_requirements`) and to `REQ-RT-*` / `REQ-HTTP-*`
  (owned by `SUBTASK_router_and_http`) are read-only; those registers are not minted here.
