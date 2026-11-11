# Ferric — Semver Contract & Changelog Practice

This document designs two things an author needs before they can depend on Ferric across releases: the **semver
contract** over Ferric's public surfaces — what a version number promises, and which changes are breaking versus
additive — and the **changelog practice** that records each release's changes so an author can upgrade without
guessing. Both are stated as testable `REQ-REL-020..039` requirements.

**What this settles, and what it does not.** It settles what each semver level *promises* for the frozen public
surfaces, a breaking-vs-additive classification an author and a reviewer can apply, and how each release's change
set is recorded and tied to its version bump. It is the API-stability-and-communication slice of release &
distribution. The *publishing mechanics* (crates.io metadata, licensing, the `path`→`version` dependency
conversion, multi-crate release order) are `REQ-REL-001..019`, owned by the publishing spoke; the broader *1.0
versioning and compatibility policy* (the MSRV promise, the frozen-`prelude` stability guarantee, additive-only
evolution across the line, cross-crate version coordination) is `REQ-REL-040..059`, owned by the versioning &
compatibility spoke. This document references both read-only and mints only `REQ-REL-020..039`.

**What, not how.** Each requirement reads as something a stranger could check against the published crates and
their changelog — a classification they can apply, a gate that blocks an unsignalled break, an entry a changelog
must carry — never a changelog generator or a CI job to build. Implementing a semver-check in CI or a changelog
tool is deferred to later code DAGs; this is the contract they implement against.

**Grounding.** Observations are grounded in `Nousix-LLC/nswe-demo` @ `main` (baseline `276138f`), confirmed from
the live repository:

- The public surfaces this contract governs are the `prelude` modules (and, for `ferric-http`, the top-level
  re-exports). Confirmed at `276138f`:
  - `ferric::prelude` — `Component`, `mount`, `batch`, `create_effect`, `create_memo`, `create_signal`, `Memo`,
    `Signal`, `EventKind`, `VElement`, `VNode`.
  - `ferric_router::prelude` — `link`, `Params`, `RoutePattern`, `current_path`, `navigate`, `Router`.
  - `ferric_http` — top-level re-exports `Client`, `ClientBuilder`, `Error`, `Result`, `Method`, `RequestBuilder`,
    `Response`, re-exported again through `ferric_http::prelude`.
- Many leaf bodies behind these surfaces are still `todo!()`; the public *shape* is fixed. The signature is the
  promise; the panic behind it is not — which is why filling a `todo!()` in is classified below (`REQ-REL-024`).
- All crates inherit `version.workspace = true` and `rust-version.workspace = true` from the virtual workspace, so
  they version in lockstep and share one MSRV today. The lockstep choice shapes the changelog scope (`REQ-REL-032`).
- **There is no `CHANGELOG.md` anywhere in the repository** (confirmed: zero matches). The changelog requirements
  below are written against that absence — the practice is designed from zero, not amended onto an existing one.

**Standards this contract rests on, cited by name.** Semantic Versioning 2.0.0 (semver.org); the Cargo book's
"SemVer Compatibility" chapter (the Rust-specific catalogue of major-vs-minor changes); the Rust API-evolution
guidance of RFC 1105 and the Rust API Guidelines; Keep a Changelog 1.1.0; and `cargo-semver-checks` as the
mechanical checker. Peer practice is compared by name (Leptos, Dioxus, Yew) in §E.

The sections below are: the governed surface (§A); the semver level contract (§B); the breaking-vs-additive
classification (§C); the changelog practice (§D); and the named-peer and standards comparison (§E). Each
requirement carries a `stage` and a `release_gating` flag and conforms to
`../../contracts/id_and_traceability_schema.yaml`.

---

## A. The surface the semver contract governs

A semver promise is only as meaningful as the surface it is made over. Before classifying changes, the contract
must say exactly what counts as "the public API" — otherwise a reviewer cannot tell whether a change touched it.
For Ferric that surface is the frozen `prelude` modules plus `ferric-http`'s top-level re-exports, enumerated
above; everything reachable only through a non-`pub` path, or behind `#[doc(hidden)]`, is internal and carries no
semver promise.

#### REQ-REL-020 — The public API each crate's semver promise covers is defined and enumerable
- **Statement:** Each Ferric crate has a defined public API — the set of items an app author may name — that the
  semver contract governs, and that set is the crate's `prelude` module (plus `ferric-http`'s top-level
  re-exports). Items reachable only through a non-public path or marked `#[doc(hidden)]` are internal and carry no
  semver promise.
- **Rationale:** Breaking-vs-additive is undecidable without a fixed boundary for what is public. The baseline
  already froze these `prelude` surfaces and apps are written against them, so the boundary already exists in the
  code; the contract names it so a reviewer (and a mechanical checker) can enumerate exactly what must not break
  silently. Drawing the line at the `prelude` also keeps the internal `todo!()` bodies and helper modules free to
  change at patch level.
- **Acceptance criteria:** For each of `ferric`, `ferric-router`, `ferric-http`, the repository states which
  module(s) constitute the public API the semver contract covers, and the enumerated set matches the items
  actually exported there. A reviewer can list the governed items from the documentation and confirm the list
  equals the crate's exported public surface; a tool that snapshots the public API (for example `cargo-semver-checks`'s
  baseline, or `cargo public-api`) reports the same set.
- **Verification:** doc_inspection, automated_test
- **Stage:** one_oh · **Release gating:** true
- **References:** REQ-FW-009, REQ-FW-010 (read-only); REQ-REL-040..059 (frozen-`prelude` stability promise, owned
  by the versioning/compat spoke). Standards: Cargo book "SemVer Compatibility".

## B. The semver level contract

At 1.0 Ferric adopts standard Semantic Versioning 2.0.0: a version is `MAJOR.MINOR.PATCH`, and the level of the
bump tells an author what a release may have done to the public surface defined in §A. This is the promise a
version number carries; §C makes "breaking" and "additive" concrete enough to apply.

#### REQ-REL-021 — Each semver level has a defined meaning for the public surface
- **Statement:** For the 1.0 line, a **MAJOR** bump signals that the release contains at least one breaking change
  to the public surface; a **MINOR** bump signals only additive, backward-compatible changes (new public items,
  no removals or redefinitions); a **PATCH** bump signals no change to the public surface — bug fixes and
  behavior-preserving internal changes only. An author reading the version delta between two releases can tell,
  from the level alone, the strongest kind of change the release is permitted to contain.
- **Rationale:** This is what "governed by semver" in REQ-FW-010 means in practice: the number is a contract, not
  a label. Library authors (persona A3) decide whether an upgrade is safe to take automatically from the level, so
  the level must carry a defined, enforced meaning rather than a maintainer's habit.
- **Acceptance criteria:** The repository documents, for the 1.0 line, what MAJOR, MINOR, and PATCH each permit and
  forbid with respect to the public surface, consistent with Semantic Versioning 2.0.0 and the Cargo book's
  SemVer chapter. A reviewer can map any one of the classified change kinds in §C to exactly one required minimum
  level using this statement.
- **Verification:** doc_inspection
- **Stage:** one_oh · **Release gating:** true
- **References:** REQ-FW-010 (read-only); REQ-REL-040..059 (the 0.x→1.0 transition and cross-crate coordination,
  owned by the versioning/compat spoke). Standards: Semantic Versioning 2.0.0; Cargo book "SemVer Compatibility".

#### REQ-REL-022 — The pre-1.0 (0.x) semver convention is stated as the bridge to 1.0
- **Statement:** While Ferric is below 1.0 (today `0.1.0`), the Cargo 0.x convention holds: the leftmost non-zero
  component carries the breaking-change signal, so a breaking change bumps the **minor** (`0.y`) and an additive
  change bumps the **patch** (`0.y.z`). The contract states this so that pre-1.0 releases are versioned under a
  defined rule, and names 1.0 as the point at which the standard `MAJOR.MINOR.PATCH` meaning in `REQ-REL-021`
  takes effect.
- **Rationale:** Ferric is at `0.1.0` and will make pre-1.0 releases before the 1.0 cut; without a stated 0.x rule
  those releases are versioned ad hoc, and the classification in §C would have no level mapping to attach to.
  Cargo and SemVer 2.0.0 both define the 0.x behavior; stating it removes the ambiguity rather than leaving the
  first real consumer to infer it.
- **Acceptance criteria:** The repository states the 0.x versioning rule (breaking → minor bump, additive → patch
  bump) and the point at which 1.0 switches to the standard meaning. A reviewer can version a hypothetical
  pre-1.0 breaking change and a pre-1.0 additive change correctly from the statement.
- **Verification:** doc_inspection
- **Stage:** one_oh · **Release gating:** true
- **References:** REQ-REL-021; REQ-REL-040..059 (the actual 0.x→1.0 transition mechanics, owned by the
  versioning/compat spoke — this requirement states only the convention, not the transition plan). Standards:
  Semantic Versioning 2.0.0 §4; Cargo book "SemVer Compatibility".

## C. Breaking-vs-additive classification

The level contract in §B is only applicable if a reviewer can decide, for a concrete change, whether it is
breaking or additive. This section is the classification — grounded in the Cargo book's major-vs-minor catalogue
and RFC 1105 — stated so an author and a reviewer reach the same verdict, and `REQ-REL-026` names the tool that
checks it mechanically.

#### REQ-REL-023 — Breaking (major) changes are classified
- **Statement:** A change to the public surface is **breaking** (requires a MAJOR bump at 1.0) when it can stop a
  conforming downstream crate from compiling or change the documented behavior it relies on. The classification
  names at least: removing or renaming a public item (function, type, trait, variant, field, module, or
  re-export); changing a function or method signature (parameters, return type, or a tightened bound); adding a
  required trait method without a default; adding a variant to an enum that is not `#[non_exhaustive]`; adding a
  field to, or making newly public, a struct whose existing fields are all public and that is not
  `#[non_exhaustive]`; and making a previously public item private or `#[doc(hidden)]`.
- **Rationale:** This is the operative content of the semver contract — the list a reviewer applies to a pull
  request. It is grounded in the Cargo book's "major change" catalogue and RFC 1105 so the classification matches
  what the Rust ecosystem already means by a breaking change, rather than a Ferric-local definition an author
  would have to relearn. REQ-FW-009 promises the frozen `prelude` surfaces are carried forward additively; this
  requirement defines precisely what would violate that promise.
- **Acceptance criteria:** The repository lists the change kinds that require a MAJOR bump, covering at least the
  cases above and marked as consistent with the Cargo book's SemVer chapter. A reviewer handed a diff of the public
  surface can classify each changed item as breaking or not using the list, and `cargo-semver-checks` (REQ-REL-026)
  flags the mechanically detectable members of the list.
- **Verification:** doc_inspection, automated_test
- **Stage:** one_oh · **Release gating:** true
- **References:** REQ-FW-009 (read-only); REQ-REL-026. Standards: Cargo book "SemVer Compatibility"; RFC 1105.

#### REQ-REL-024 — Additive (minor) changes are classified
- **Statement:** A change is **additive** (requires only a MINOR bump at 1.0) when it extends the public surface
  without breaking a conforming downstream crate. The classification names at least: adding a new public item (a
  new export, function, method, type, or module); adding a defaulted method to an existing trait; adding a variant
  to a `#[non_exhaustive]` enum; and adding a field to a `#[non_exhaustive]` struct or one with a private field.
  Additive changes are the only changes a MINOR release may contain.
- **Rationale:** REQ-FW-009 commits the frozen surfaces to additive-only evolution; this requirement defines what
  "additive" admits, so "extend, never silently redefine" is checkable rather than aspirational. It is the
  counterpart to `REQ-REL-023`: together they let a reviewer sort any public-surface change into exactly one of
  breaking, additive, or neither.
- **Acceptance criteria:** The repository lists the change kinds that are additive and permitted in a MINOR
  release, covering at least the cases above and consistent with the Cargo book's SemVer chapter. A reviewer can
  confirm a stated additive change (for example a new helper method on `ClientBuilder`) is classified MINOR and
  requires no MAJOR bump.
- **Verification:** doc_inspection, automated_test
- **Stage:** usable_early · **Release gating:** true
- **References:** REQ-FW-009 (read-only); REQ-REL-027. Standards: Cargo book "SemVer Compatibility"; RFC 1105.

#### REQ-REL-025 — Patch changes, and the `todo!()` fill-in case, are classified
- **Statement:** A change is a **PATCH** when it leaves the public surface unchanged — a bug fix, a documentation
  correction, or a behavior-preserving internal change. Filling in a body that was `todo!()` at the baseline
  (making a frozen-signature function actually do what its signature and docs describe) is a PATCH when the
  signature and documented contract are unchanged: the `todo!()` panic was never a promised behavior, so replacing
  it with the specified behavior fixes a defect rather than changing the contract. A fill-in that must change the
  signature or the documented behavior to work is classified by `REQ-REL-023`/`REQ-REL-024` instead.
- **Rationale:** Ferric is distinctive here: its public shape is frozen but many bodies are still `todo!()`, so a
  large part of the 1.0 work is filling them in. Without an explicit rule, each fill-in invites a case-by-case
  semver argument. Anchoring the rule to "the signature and documented contract are the promise, the panic is not"
  keeps the common case (implement a stub as specified) at PATCH while still catching the case where implementing
  the stub forces a surface change.
- **Acceptance criteria:** The repository states the PATCH classification and the `todo!()` fill-in rule. A
  reviewer can take a stated example — a `ferric-router` or `ferric-http` function whose `todo!()` body is
  implemented to its documented signature — and confirm it is classified PATCH, and take a second example whose
  correct implementation requires a signature change and confirm it is classified MAJOR.
- **Verification:** doc_inspection
- **Stage:** one_oh · **Release gating:** true
- **References:** REQ-REL-023, REQ-REL-024; §Grounding (the `todo!()` bodies at `276138f`). Standards: Cargo book
  "SemVer Compatibility".

#### REQ-REL-026 — A breaking change is caught mechanically, not by reviewer memory alone
- **Statement:** The classification in `REQ-REL-023` is enforced by a mechanical check that compares a release's
  public API against the previously published version and reports any breaking change, so an unsignalled break
  cannot reach a published release silently. `cargo-semver-checks` is named as that check.
- **Rationale:** A written classification that depends on every reviewer remembering it fails the way the absent
  changelog failed — silently. The ecosystem's standard answer is `cargo-semver-checks`, which lints the public
  API diff against the SemVer rules; naming it as the required check turns "we classify breaking changes" into
  "a break that is not matched by a MAJOR bump is reported before release." This is a requirement's acceptance
  method, not an instruction to build a CI job — the implementation is a later code DAG's work.
- **Acceptance criteria:** `cargo-semver-checks` (or an equivalent that lints the public-API diff against the
  SemVer rules) runs against each crate comparing the release to its prior published version, and a release whose
  public-surface change is breaking but whose version bump is not MAJOR is reported as a violation. A reviewer can
  confirm the check is part of the stated release procedure and can reproduce a flagged break on a stated example.
- **Verification:** automated_test
- **Stage:** one_oh · **Release gating:** true
- **References:** REQ-REL-023; REQ-REL-001..019 (the release procedure the check runs within, owned by the
  publishing spoke). Standards: `cargo-semver-checks`; Cargo book "SemVer Compatibility".

#### REQ-REL-027 — Public enums and structs are future-proofed so later additions stay additive
- **Statement:** Public enums and structs on the frozen surface that are expected to gain members after 1.0 are
  marked `#[non_exhaustive]` (or given an equivalent sealed-extension pattern) before the 1.0 freeze, so that
  adding a variant or field later is an additive (MINOR) change rather than a breaking (MAJOR) one. `EventKind`
  (new event kinds will be added as event coverage grows) and `Method` are the named candidates; the contract
  states which public types are frozen as exhaustive and which are open.
- **Rationale:** This decision can only be made *before* 1.0: once an exhaustive enum ships in 1.0, adding a
  variant is a breaking change forever on that line, so an un-future-proofed `EventKind` would force a 2.0 just to
  add a DOM event. REQ-FW-006 commits the 1.0 to the full DOM event range, which means `EventKind` will grow;
  marking it `#[non_exhaustive]` now is what lets that growth stay additive under `REQ-REL-024`. This is a design
  requirement on the surface, stated as "what" (which types are open), not a code change made here.
- **Acceptance criteria:** The repository states, for each public enum and struct on the governed surface, whether
  it is frozen exhaustive or `#[non_exhaustive]`, with a reason for the types expected to grow (at least
  `EventKind` and `Method`). A reviewer can confirm a stated post-1.0 addition of an `EventKind` variant is
  classified MINOR under this decision, and `cargo-semver-checks` agrees.
- **Verification:** doc_inspection, automated_test
- **Stage:** usable_early · **Release gating:** true
- **References:** REQ-FW-006, REQ-FW-009 (read-only); REQ-REL-024, REQ-REL-026. Standards: Cargo book "SemVer
  Compatibility"; Rust API Guidelines (future-proofing).

#### REQ-REL-028 — Behavior documented for a public item is part of the semver contract
- **Statement:** The semver contract covers documented behavior, not only type signatures. A change that keeps a
  signature intact but alters the behavior its documentation promises, in a way a conforming downstream crate
  relies on, is a breaking change under `REQ-REL-023`. A public item's documented contract is therefore what the
  release promises to preserve across MINOR and PATCH releases.
- **Rationale:** Signature-only semver misses the breaks that hurt most: a router that silently changes how it
  matches a path parameter, or a client that changes how it treats a non-2xx status, breaks callers without
  changing a single type. Tying the contract to documented behavior is what the Cargo book's "behavioral changes"
  guidance and RFC 1105 intend; it also makes the acceptance criteria of other areas (for example the router and
  HTTP behavior in REQ-RT-* / REQ-HTTP-*) the behavior the semver contract protects.
- **Acceptance criteria:** The repository states that documented behavior of a public item is covered by the
  semver contract and classified as breaking when changed incompatibly. A reviewer can take a stated
  behavior-only change to a public item (for example a changed error-handling rule) and confirm it is classified
  MAJOR even though the signature is unchanged.
- **Verification:** doc_inspection
- **Stage:** one_oh · **Release gating:** true
- **References:** REQ-REL-023. Standards: Cargo book "SemVer Compatibility" (behavioral changes); RFC 1105.

#### REQ-REL-029 — Removal of a public item is preceded by a deprecation
- **Statement:** A public item is not removed without first being marked `#[deprecated]`, with a note naming the
  replacement, in a released MINOR version; the removal itself happens only in a later MAJOR release. Adding the
  `#[deprecated]` attribute is an additive (MINOR) change; the removal is a breaking (MAJOR) change recorded in the
  changelog under `REQ-REL-031`.
- **Rationale:** A 1.0 that removes items abruptly breaks the library authors (A3) it promised stability to, even
  when the removal is correctly signalled by a MAJOR bump. Deprecate-then-remove gives downstream crates a release
  in which the item still works but the compiler warns, so the upgrade can be staged. This is standard Rust
  practice (`#[deprecated]` is a language feature) and is what "a stable public API across a release line" in
  REQ-FW-010 means in the removal case.
- **Acceptance criteria:** The repository states the deprecate-before-remove policy and the semver level of each
  step. A reviewer can confirm a stated removal was preceded by a `#[deprecated]` item in an earlier MINOR release
  whose changelog recorded the deprecation, and that the deprecated item still compiled (with a warning) in that
  release.
- **Verification:** doc_inspection, automated_test
- **Stage:** one_oh · **Release gating:** true
- **References:** REQ-FW-010 (read-only); REQ-REL-023, REQ-REL-031. Standards: Rust API Guidelines; Cargo book
  "SemVer Compatibility".

## D. Changelog practice

The repository has no `CHANGELOG.md` today. A semver contract records the *level* of a change; the changelog
records *what* changed, so an author deciding whether and how to upgrade can read the actual change set rather
than infer it from a version number. The practice below follows Keep a Changelog 1.1.0 and ties each entry to the
semver level the change demands.

#### REQ-REL-030 — Every release records its changes in a maintained changelog
- **Statement:** Ferric maintains a changelog that records each release's changes in human-readable form, kept
  current as part of making a release, following the Keep a Changelog 1.1.0 structure: a reverse-chronological
  list of released versions each with its release date, plus an `Unreleased` section at the top for changes not
  yet released.
- **Rationale:** REQ-FW-010 and journey JA5 require that an author can "read a changelog, understand what a version
  bump changes, and upgrade without silent breakage." No changelog exists today, so the practice is designed from
  zero. Keep a Changelog is the ecosystem's common structure and is what an evaluating author (A1) expects to find
  when judging whether the project is maintained.
- **Acceptance criteria:** The repository contains a changelog in Keep a Changelog form with per-version,
  date-stamped sections in reverse-chronological order and an `Unreleased` section; a reviewer can confirm a
  released version's section exists and matches that release, and that the structure follows Keep a Changelog
  1.1.0.
- **Verification:** doc_inspection
- **Stage:** one_oh · **Release gating:** true
- **References:** REQ-FW-010 (read-only); JA5. Standards: Keep a Changelog 1.1.0.

#### REQ-REL-031 — Each changelog entry states change type, affected crate, and whether it is breaking
- **Statement:** Each changelog entry is grouped under a Keep a Changelog change type — `Added`, `Changed`,
  `Deprecated`, `Removed`, `Fixed`, `Security` — names the crate(s) it affects, and marks whether the change is
  breaking or additive per the §C classification. An author scanning a release's entries can see which crate
  changed, in what way, and whether the change can affect their code.
- **Rationale:** A changelog that only lists commit subjects does not answer the author's real question — "will
  this upgrade break me, and where?" Grouping by change type and marking breaking-vs-additive makes the entry
  carry the §C classification, so the changelog and the semver contract state the same facts in two forms. Naming
  the affected crate matters because the workspace ships three crates that version together (`REQ-REL-032`).
- **Acceptance criteria:** A reviewer can take a release's changelog section and, for each entry, read its change
  type, the crate(s) affected, and a breaking/additive marking; a `Removed` or breaking `Changed` entry is marked
  breaking and a `Added` entry is marked additive, consistent with §C.
- **Verification:** doc_inspection
- **Stage:** one_oh · **Release gating:** true
- **References:** REQ-REL-023, REQ-REL-024, REQ-REL-032. Standards: Keep a Changelog 1.1.0.

#### REQ-REL-032 — A release's semver level is justified by its changelog entries
- **Statement:** The semver level of a release is consistent with, and derivable from, its changelog entries: a
  release containing any `Removed` entry or any breaking-marked `Changed` entry is a MAJOR release; a release whose
  strongest entry is an additive `Added` or `Deprecated` is a MINOR release; a release containing only `Fixed`
  (and no public-surface change) is a PATCH release. The changelog and the version bump cannot disagree.
- **Rationale:** This is the seam between §B and §D — it makes the changelog the human-readable justification of
  the version number, and the version number a claim the changelog must support. It also gives the mechanical
  check in `REQ-REL-026` a documentary counterpart: where `cargo-semver-checks` proves the code's break is
  signalled, this proves the recorded change set agrees.
- **Acceptance criteria:** A reviewer can take any released version, read its changelog section, and confirm the
  version-level bump from the prior release is the minimum level the entries require under `REQ-REL-021`; a release
  with a `Removed` entry but a non-MAJOR bump, or a MINOR release with no additive entry, is a detectable
  inconsistency.
- **Verification:** doc_inspection
- **Stage:** one_oh · **Release gating:** true
- **References:** REQ-REL-021, REQ-REL-026, REQ-REL-031. Standards: Keep a Changelog 1.1.0; Semantic Versioning 2.0.0.

#### REQ-REL-033 — The changelog covers the multi-crate workspace, with per-crate changes attributable
- **Statement:** The changelog records changes for all three crates (`ferric`, `ferric-router`, `ferric-http`),
  and a reader can attribute each change to the crate it affects. Because the crates version in lockstep today
  (`version.workspace = true`), a single workspace-level `CHANGELOG.md` with per-crate grouping within each release
  satisfies this; should a crate ever version independently, that crate carries its own `CHANGELOG.md`. The
  requirement fixes the outcome — per-crate attribution across the workspace — not a single file layout.
- **Rationale:** A workspace that ships three crates from one repository can hide which crate a change touched if
  the changelog is flat. The lockstep versioning observed at the baseline makes one workspace changelog with
  per-crate sections the simple fit, and it keeps the three crates' release notes in step with their shared
  version. Stating the requirement as "per-crate attribution" rather than "one file" leaves the layout to the
  implementer while keeping the testable property. The cross-crate *version-coordination* rule itself is owned by
  the versioning/compat spoke (`REQ-REL-040..059`); this requirement only governs how that coordination is recorded.
- **Acceptance criteria:** A reviewer can find, for a given release, the changes to each of the three crates and
  tell which crate each entry affects; where crates version in lockstep a single workspace changelog with per-crate
  grouping is accepted, and where a crate versions independently its own changelog is present.
- **Verification:** doc_inspection
- **Stage:** one_oh · **Release gating:** true
- **References:** REQ-REL-030, REQ-REL-031; REQ-REL-040..059 (cross-crate version coordination, owned by the
  versioning/compat spoke); §Grounding (`version.workspace = true`). Standards: Keep a Changelog 1.1.0.

## E. Named-peer and standards comparison

The classification and the changelog practice above are not invented for Ferric; they track what the Rust
ecosystem and Ferric's named peers already do, so an evaluating author (A1) meets a convention they recognize.

- **The reference standards.** The semver level meanings follow Semantic Versioning 2.0.0; the breaking-vs-additive
  catalogue follows the Cargo book's "SemVer Compatibility" chapter (the Rust-specific enumeration of
  major-vs-minor changes) and the API-evolution direction of RFC 1105 and the Rust API Guidelines; the changelog
  structure follows Keep a Changelog 1.1.0; the mechanical break check is `cargo-semver-checks`, the ecosystem's
  tool for linting a crate's public-API diff against the SemVer rules.
- **Leptos, Dioxus, Yew.** Each of Ferric's Rust peers publishes to crates.io under Cargo semver and maintains a
  changelog (Leptos and Dioxus keep a repository `CHANGELOG.md`; Yew documents releases in its project
  documentation). Each has also made breaking changes across its pre-1.0 (`0.x`) line under the Cargo 0.x
  convention `REQ-REL-022` states — the normal shape for a framework still before 1.0, and the reason Ferric's
  contract states the 0.x rule explicitly rather than leaving its first consumer to infer it. Ferric's choice to
  name `cargo-semver-checks` as a release gate (`REQ-REL-026`) matches the growing ecosystem practice of enforcing
  the classification mechanically rather than by review alone.
- **Where Ferric differs.** Ferric's `todo!()`-body situation (`REQ-REL-025`) has no direct peer analogue — it
  comes from shipping a frozen public shape ahead of its implementation — which is why the contract classifies the
  fill-in case explicitly rather than borrowing a peer's rule.

(The merged `release-and-distribution.md` carries the consolidated named-peer comparison for the whole concern;
this section supplies the semver/changelog slice of it.)

---

## Register summary

| Id | Covers | Facet | Stage | Gating | Verification |
|---|---|---|---|---|---|
| REQ-REL-020 | Governed public surface defined | semver contract | one_oh | true | doc_inspection, automated_test |
| REQ-REL-021 | Semver level meanings for 1.0 | semver contract | one_oh | true | doc_inspection |
| REQ-REL-022 | 0.x convention as bridge to 1.0 | semver contract | one_oh | true | doc_inspection |
| REQ-REL-023 | Breaking (major) classification | breaking-vs-additive | one_oh | true | doc_inspection, automated_test |
| REQ-REL-024 | Additive (minor) classification | breaking-vs-additive | usable_early | true | doc_inspection, automated_test |
| REQ-REL-025 | Patch + `todo!()` fill-in classification | breaking-vs-additive | one_oh | true | doc_inspection |
| REQ-REL-026 | Mechanical break check (`cargo-semver-checks`) | breaking-vs-additive | one_oh | true | automated_test |
| REQ-REL-027 | `#[non_exhaustive]` future-proofing | breaking-vs-additive | usable_early | true | doc_inspection, automated_test |
| REQ-REL-028 | Behavior is part of the contract | semver contract | one_oh | true | doc_inspection |
| REQ-REL-029 | Deprecate-before-remove | semver contract | one_oh | true | doc_inspection, automated_test |
| REQ-REL-030 | A maintained changelog per release | changelog practice | one_oh | true | doc_inspection |
| REQ-REL-031 | Entry type, crate, breaking marking | changelog practice | one_oh | true | doc_inspection |
| REQ-REL-032 | Semver level justified by changelog | changelog practice | one_oh | true | doc_inspection |
| REQ-REL-033 | Multi-crate changelog attribution | changelog practice | one_oh | true | doc_inspection |

All ids are inside the assigned `REQ-REL-020..039` range (identity J1); `REQ-REL-034..039` are unused and left for
additive amendment. Every entry carries the parent schema's fields (identity J2) and a `verification_method` from
the closed vocabulary — `doc_inspection`, `automated_test` (identity J3). The semver contract, the
breaking-vs-additive classification, and the changelog practice are each covered by more than one requirement
(identity J4, this spoke's share).

## Metadata

- **Owning task:** `SUBTASK_semver_changelog` (owns `REQ-REL-020..039`; sub-contract identity J1).
- **Scope boundary:** this partial mints only `REQ-REL-020..039`. Publishing readiness and the `path`→`version`
  conversion are `REQ-REL-001..019` (publishing spoke); the MSRV promise, the frozen-`prelude` stability
  guarantee, additive-only evolution across the line, and cross-crate version coordination are `REQ-REL-040..059`
  (versioning/compat spoke). All cross-references to those ranges and to `REQ-FW-*` are read-only.
- **Conforms to:** `../../contracts/id_and_traceability_schema.yaml` (REQ fields, stage vocabulary,
  `release_gating`, `verification_method`); `../contracts/_MANIFEST.yaml` (the `REQ-REL-*` partition and merge
  identities J1–J7).
- **Grounding commit:** `Nousix-LLC/nswe-demo` @ `276138f` (`main`) — `prelude` surfaces and `version.workspace`/
  `rust-version.workspace` confirmed from the live repository; no `CHANGELOG.md` present (zero matches).
- **Standards cited:** Semantic Versioning 2.0.0; Cargo book "SemVer Compatibility"; RFC 1105; Rust API Guidelines;
  Keep a Changelog 1.1.0; `cargo-semver-checks`. Peers named: Leptos, Dioxus, Yew.
- **Merged into:** `release-and-distribution.md` by `SUBTASK_rel_synthesis`, placed at
  `design/ferric/release-and-distribution.md` by `SUBTASK_design_pr`.
</content>
</invoke>
