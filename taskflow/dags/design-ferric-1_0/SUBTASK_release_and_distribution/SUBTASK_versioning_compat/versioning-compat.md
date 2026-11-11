# Ferric 1.0 — Versioning & Compatibility Policy (`REQ-REL-040..059`)

This partial designs the **versioning and compatibility policy** a Ferric 1.0 promises: the minimum Rust
version it supports and how that floor may move, what the frozen public `prelude` surfaces are guaranteed to
do across the 1.x line, that the surface evolves by addition only within 1.x, and how the three crates version
and stay compatible with one another. It is the *promise* a library author (persona A3) and an app author (A2)
read before they depend on Ferric and before they upgrade.

It owns `REQ-REL-040..059` only. The semver *mechanics* — what a major/minor/patch bump signals for each class
of change, the breaking-vs-additive classification, and the changelog — are `REQ-REL-020..039`
(`SUBTASK_semver_changelog`); the publishing *mechanics* — crates.io metadata, licensing, the path→version
dependency conversion, release order — are `REQ-REL-001..019` (`SUBTASK_publishing`). References to those
ranges here are read-only; this partial does not restate them as its own ids.

Design, not implementation: each requirement reads as something a stranger could check against the published
crates and the repository, not as a chosen mechanism to build.

---

## Policy in brief

1. **MSRV.** 1.0 states a supported minimum Rust version and keeps it as a declared floor, not "whatever is
   latest." The floor may rise within 1.x, but only as a minor release, announced, and never silently.
2. **Frozen surfaces.** The public `prelude` surfaces carried from the baseline remain usable for the life of
   the 1.x line. Code that compiles against them at 1.0 keeps compiling against every later 1.x.
3. **Additive-only.** Within 1.x the public surface grows by addition. Removing or redefining a public item is
   a breaking change, and a breaking change is deferred to a future major (2.0).
4. **Cross-crate coordination.** `ferric`, `ferric-router`, and `ferric-http` version in lockstep and release
   together at one version, so an app author can depend on the set at a single 1.x version and trust the parts
   fit.
5. **Stated scope.** The promise covers the documented public surfaces. Items outside them — anything not
   re-exported in a `prelude`, the runtime behaviour of leaf bodies still unimplemented (`todo!()`) at a given
   release, and anything behind a future unstable flag — are named as outside the 1.x stability promise rather
   than left ambiguous.

---

## Requirements

### `REQ-REL-040` — 1.0 states a supported minimum Rust version (MSRV)

- **Statement:** Ferric 1.0 declares a minimum supported Rust version and every published crate builds on that
  version of stable Rust. The declared MSRV is discoverable from the crates themselves, not only from prose.
- **Rationale:** A "1.0" that does not say which Rust versions it supports leaves an app author (A2) and a
  library author (A3) guessing whether an upgrade of either Ferric or their toolchain will compile. The
  workspace already pins `rust-version = "1.82"` in `[workspace.package]`, so the floor exists; the requirement
  is that 1.0 commits to it as a promise. The `rust-version` field (RFC 2495, *the minimum-supported-rust-version
  field*) is the ecosystem's standard way to state this, and Cargo's MSRV-aware resolver (RFC 3537) reads it
  during dependency resolution so a consumer on an older stable toolchain still resolves a compatible version
  rather than failing to build. Peer frameworks declare an MSRV through this field and track recent stable
  rather than pinning an old floor — as reported by their published crates, Leptos sits around Rust 1.88, Yew
  around 1.84, and Dioxus around 1.83; Ferric's 1.82 is consistent with that range.
- **Acceptance criteria:**
  - `doc_inspection`: each published crate (`ferric`, `ferric-router`, `ferric-http`) carries a `rust-version`
    field, and the repository states the supported-MSRV promise where an author will find it (the compatibility
    policy of `REQ-REL-046`).
  - `automated_test`: a build of each crate on the declared MSRV toolchain targeting `wasm32-unknown-unknown`
    through the standard tooling succeeds.
- **Stage:** `one_oh` · **Release gating:** `true`
- **References:** `REQ-FW-003` (stable Rust / standard toolchain, "compatible-version ranges are stated"),
  `REQ-FW-010` (compatibility policy); `REQ-REL-046` (where the promise is written).

### `REQ-REL-041` — How the MSRV may rise within the 1.x line

- **Statement:** The supported MSRV may increase within 1.x, but only in a minor release, and each increase is
  recorded so an author can see it before upgrading. Raising the MSRV within 1.x is not treated as a
  major-breaking change and does not require a 2.0.
- **Rationale:** Pinning an MSRV for the life of a major line would freeze Ferric out of compiler improvements
  for years; raising it without warning would break downstream builds silently. The Cargo Book's *SemVer
  Compatibility* chapter classifies increasing the minimum required Rust version as a possibly-breaking change,
  and the Rust API Guidelines MSRV discussion (rust-lang/api-guidelines #231) gives the convention that a
  1.0-and-above crate raising its MSRV bumps the minor version rather than the major. Stating this up front
  tells an author the one rule that matters: a Ferric minor upgrade may ask for a newer Rust, a patch upgrade
  never will. The semver level an MSRV change signals is owned by the semver contract (`REQ-REL-020..039`);
  this requirement is the compatibility-policy commitment that the floor moves this way and no other.
- **Acceptance criteria:**
  - `doc_inspection`: the compatibility policy states that an MSRV increase occurs only in a minor (or major)
    release, never a patch, and is announced in the changelog for the release that makes it.
  - `automated_test`: for any release that raises the declared `rust-version`, the version bump is at least a
    minor bump (checkable from the version numbers and the `rust-version` values across two released versions).
- **Stage:** `one_oh` · **Release gating:** `true`
- **References:** `REQ-REL-020..039` (semver level of a change; changelog practice); `REQ-FW-010`.

### `REQ-REL-042` — The frozen `prelude` surfaces stay usable across 1.x

- **Statement:** The public `prelude` surfaces carried from the baseline remain usable for the whole 1.x line.
  Code that compiles against the 1.0 preludes continues to compile against every later 1.x release without
  change.
- **Rationale:** This is the policy side of `REQ-FW-009` (frozen surfaces carried forward additively). The
  baseline already froze the public shape of three preludes — `ferric::prelude` (`Component`, `mount`, `batch`,
  `create_effect`, `create_memo`, `create_signal`, `Memo`, `Signal`, `EventKind`, `VElement`, `VNode`);
  `ferric_router::prelude` (`link`, `Params`, `RoutePattern`, `Router`, `navigate`, `current_path`); and
  `ferric_http`'s top-level re-exports plus `prelude` (`Client`, `ClientBuilder`, `Error`, `Method`,
  `RequestBuilder`, `Response`, `Result`). Apps are already written against these. A 1.0 whose preludes shifted
  under a minor or patch release would make "1.0" a number with no stability behind it. Many leaf bodies are
  still `todo!()`, but the public *shape* is fixed; this requirement is about that shape, not the
  not-yet-implemented behaviour behind it (see `REQ-REL-047`).
- **Acceptance criteria:**
  - `automated_test`: an example (or a `trybuild`-style compile test) that imports and uses the baseline
    `prelude` items of all three crates compiles against the 1.0 release and against a later 1.x release
    unchanged.
  - `doc_inspection`: the compatibility policy names the `prelude` surfaces as the guaranteed-stable public API
    for 1.x.
- **Stage:** `one_oh` · **Release gating:** `true`
- **References:** `REQ-FW-009` (frozen surfaces additive); `REQ-REL-043` (additive-only evolution);
  `REQ-RT-*`, `REQ-HTTP-*` (the per-crate surface detail, read-only).

### `REQ-REL-043` — The public surface evolves by addition only within 1.x

- **Statement:** Within the 1.x line the public API grows by addition — new exports, new methods, new optional
  parameters handled compatibly. Removing a public item, renaming it, or changing its type or documented
  behaviour is a breaking change, and a breaking change is deferred to a future major version (2.0).
- **Rationale:** Additive-only evolution is what lets an author upgrade a minor release and trust their code
  still builds; it is the discipline that keeps the walking skeleton a dependable base while leaf bodies get
  implemented. The classification of which concrete changes are additive versus breaking is the semver
  contract's (`REQ-REL-020..039`), grounded in the Cargo Book's *SemVer Compatibility* chapter and the Rust API
  evolution guidelines; this requirement is the *commitment* that, having that classification, 1.x only ever
  makes additive changes and defers every breaking one. Peer frameworks follow the same rule across their crate
  families — Leptos, Dioxus, and Yew each reserve breaking public-API changes for a new major (or, pre-1.0,
  a new `0.x`) rather than shipping them mid-line.
- **Acceptance criteria:**
  - `automated_test`: a public-API check (for example `cargo-semver-checks`, named by the semver contract as the
    mechanical gate) run between two 1.x releases reports no removed or redefined public item; any such finding
    blocks the release or forces a major bump.
  - `doc_inspection`: the compatibility policy states the additive-only rule for 1.x and that removals/redefinitions
    are deferred to 2.0.
- **Stage:** `one_oh` · **Release gating:** `true`
- **References:** `REQ-FW-009`; `REQ-REL-020..039` (breaking-vs-additive classification, the semver gate);
  `REQ-REL-042`.

### `REQ-REL-044` — The crates version in lockstep and release together

- **Statement:** `ferric`, `ferric-router`, and `ferric-http` share one version number and are released
  together: every 1.0 release publishes all of them at the same version. 1.0 keeps the workspace's lockstep
  versioning (`version.workspace = true`) rather than letting the crates drift to independent version numbers.
- **Rationale:** The workspace inherits a single `[workspace.package] version` through `version.workspace = true`,
  so the crates version in lockstep today. Lockstep is the simplest contract an app author can hold: one version
  number describes the whole set, and there is no matrix of "which `ferric-router` works with which `ferric`" to
  reason about. This matches how the peer families ship — Leptos releases `leptos`, `leptos_router`, `leptos_meta`
  and the rest together at a shared version within a release, and Dioxus and Yew coordinate their companion
  crates the same way. Independent per-crate versioning (as in, for example, the Tokio family) buys finer-grained
  release cadence at the cost of a compatibility matrix; for a three-crate set that is designed and tested as one
  framework, lockstep is the better trade, and 1.0 commits to it. Allowing independent versions later would itself
  be a policy change for a future major.
- **Acceptance criteria:**
  - `doc_inspection`: the compatibility policy states lockstep versioning for the 1.x line; the workspace manifest
    shows `version.workspace = true` and each crate inherits it.
  - `publishability`: a coordinated workspace release publishes `ferric`, `ferric-router`, and `ferric-http` at
    the same version (`cargo publish` succeeds for each at that version; release order per `REQ-REL-001..019`).
- **Stage:** `one_oh` · **Release gating:** `true`
- **References:** `REQ-FW-010` (version-coordination rule); `REQ-REL-001..019` (multi-crate release order,
  path→version conversion); `REQ-REL-045`.

### `REQ-REL-045` — Cross-crate compatibility an app author can rely on

- **Statement:** An app author can depend on `ferric`, `ferric-router`, and `ferric-http` at the same 1.x
  version and trust that the three compose without version conflicts: a `ferric-router` 1.x and a `ferric-http`
  1.x work with `ferric` 1.x, because the set is built, tested, and released together at that version.
- **Rationale:** `ferric-router` depends on `ferric` (today via a path dependency that the publishing spoke
  converts to carry a version); the router and HTTP client exist to compose with the view framework over the
  frozen surfaces. The compatibility an author needs is simple to state under lockstep: pick a 1.x version, use
  it for all three. This is the compatibility half of `REQ-FW-010` and the stability leg of journey JA5 ("rely on
  a public API that does not shift … with a documented compatibility policy across the multi-crate workspace").
- **Acceptance criteria:**
  - `example_build`: a stated example app that depends on all three crates at the same 1.x version builds and
    runs the described behaviour (routing + a JSON request + rendering) over their public surfaces.
  - `doc_inspection`: the compatibility policy states that the three crates are compatible when taken at the same
    1.x version and that this is the supported way to depend on the set.
- **Stage:** `one_oh` · **Release gating:** `true`
- **References:** `REQ-FW-007` (router + HTTP compose with the view framework), `REQ-FW-010`; `REQ-REL-044`;
  `REQ-REL-001..019` (the intra-workspace dependency carries a version).

### `REQ-REL-046` — The compatibility policy is written down and discoverable

- **Statement:** The versioning and compatibility policy for 1.0 — the MSRV promise and its raise rule, the
  frozen-surface guarantee, additive-only evolution, and cross-crate coordination — is written in the repository
  where an author will find it before depending on or upgrading Ferric, not left implicit in the version numbers.
- **Rationale:** `REQ-FW-010` requires a *documented* compatibility policy: a reader must be able to learn, from
  the repository, what a given version bump is allowed to change. Stating the policy in one discoverable place
  (a `COMPATIBILITY.md`, a documented section of the top-level README, or the published crate docs) is what turns
  the preceding requirements from internal intent into a promise an author can hold the project to. The semver
  level each change signals and the per-release change set live in the semver contract and the changelog
  (`REQ-REL-020..039`); this requirement is that the *policy* itself is published alongside them.
- **Acceptance criteria:**
  - `doc_inspection`: a reviewer finds, in the repository, a stated compatibility policy covering MSRV and its
    raise rule, the frozen-`prelude` guarantee, additive-only 1.x evolution, and lockstep cross-crate
    versioning; it is linked from where an author starts (README / crate docs).
- **Stage:** `one_oh` · **Release gating:** `true`
- **References:** `REQ-FW-010`; `REQ-REL-040`, `REQ-REL-041`, `REQ-REL-042`, `REQ-REL-043`, `REQ-REL-044`,
  `REQ-REL-045` (the policy content it collects); `REQ-REL-020..039` (semver + changelog it sits beside).

### `REQ-REL-047` — What the 1.x promise does not cover (stated, not implied)

- **Statement:** The 1.x stability promise covers the documented public `prelude` surfaces. It does not cover:
  items not re-exported in a `prelude`; the runtime behaviour of leaf bodies still unimplemented (`todo!()`) at a
  given release, until the work-item that implements them lands; and anything placed behind a future unstable or
  experimental feature flag. These exclusions are named in the compatibility policy.
- **Rationale:** The baseline ships a fixed public *shape* with many `todo!()` leaf bodies, so a stability
  promise that did not separate "this API shape is stable" from "this behaviour is implemented" would either
  overclaim (promising behaviour that is not built yet) or get quietly narrowed later. Naming the exclusions is
  what keeps the promise accurate: an author knows exactly what is guaranteed and what is still moving. A hidden
  cut — discovering after adoption that some re-exported-looking item was never in scope — costs more trust than
  an exclusion stated plainly at 1.0. This keeps `REQ-REL-042`'s guarantee precise rather than aspirational.
- **Acceptance criteria:**
  - `doc_inspection`: the compatibility policy states that the stability guarantee applies to the documented
    `prelude` surfaces, and names the three exclusions (non-prelude items, not-yet-implemented `todo!()`
    behaviour, and future unstable-flagged APIs).
- **Stage:** `one_oh` · **Release gating:** `true`
- **References:** `REQ-REL-042` (the guaranteed surface); `REQ-FW-009`; `REQ-REL-046` (where the exclusions are
  written).

---

## Evidence base (named)

- **The Cargo Book — *SemVer Compatibility*.** Classification of API changes as major/minor, and the treatment
  of increasing the minimum required Rust version as a possibly-breaking change. (Used in `REQ-REL-041`,
  `REQ-REL-043`.)
- **The `rust-version` field — RFC 2495 (*the minimum-supported-rust-version field*)** and the **MSRV-aware
  dependency resolver — RFC 3537**. The standard mechanism for declaring an MSRV and Cargo reading it during
  resolution. (Used in `REQ-REL-040`.)
- **Rust API Guidelines — MSRV policy discussion (rust-lang/api-guidelines #231).** The convention that a
  ≥1.0 crate bumps its minor version on an MSRV increase. (Used in `REQ-REL-041`.)
- **Peer frameworks — Leptos, Dioxus, Yew.** Each declares an MSRV through the `rust-version` field and tracks
  recent stable (as reported by their published crates ~2026: Leptos ≈ 1.88, Yew ≈ 1.84, Dioxus ≈ 1.83), and
  each publishes a crate family versioned in lockstep within a release. **Tokio** is named as the counter-example
  of independent per-crate versioning with a stated MSRV policy. (Used in `REQ-REL-040`, `REQ-REL-043`,
  `REQ-REL-044`.)

Peer MSRV figures are reported from the frameworks' published crate metadata and read as a recency pattern, not
a precise contemporaneous claim; the point they support is that none of the three pins a conservative old floor.

---

## Metadata

- **Owning task:** `SUBTASK_versioning_compat` (concern 7, release & distribution).
- **Id range owned:** `REQ-REL-040..059` (used: `REQ-REL-040..047`; `REQ-REL-048..059` unused and available).
- **`conforms_to`:** `../../contracts/id_and_traceability_schema.yaml` (parent schema — `requirement_fields`,
  `verification_method`, `stage`) via `../contracts/_MANIFEST.yaml` (sub-contract, identities J1–J7).
- **Merge identities this partial supports:** J1 (ids inside `REQ-REL-040..059`, no collision); J2 (every
  requirement carries id/statement/rationale/acceptance_criteria/stage/release_gating/references); J3
  (verification_method ∈ {doc_inspection, automated_test, example_build, publishability}); J4 (versioning/
  compatibility policy covered); J5 (`REQ-REL-040` states the MSRV promise, `REQ-REL-042` states the
  frozen-`prelude` stability promise); J6 (peers Leptos/Dioxus/Yew and the Cargo SemVer / RFC references named).
- **Verification methods used:** `doc_inspection`, `automated_test`, `example_build`, `publishability`.
- **Read-only cross-references:** `REQ-FW-003`, `REQ-FW-007`, `REQ-FW-009`, `REQ-FW-010`; sibling ranges
  `REQ-REL-001..019` (publishing) and `REQ-REL-020..039` (semver + changelog); `REQ-RT-*`, `REQ-HTTP-*`.
