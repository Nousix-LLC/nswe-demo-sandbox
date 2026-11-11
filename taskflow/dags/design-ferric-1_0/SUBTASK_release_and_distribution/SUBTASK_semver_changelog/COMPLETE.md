# COMPLETE — SUBTASK_semver_changelog

## What was done
Designed the **semver contract** over Ferric's frozen public surfaces, a **breaking-vs-additive classification**,
and a **changelog practice**, expressed as the testable `REQ-REL-020..039` register in `semver-changelog.md`.

## What was produced
- `semver-changelog.md` (this workspace) — the single declared output. Contains:
  - §A the governed public surface (`REQ-REL-020`);
  - §B the semver level contract incl. the 0.x bridge (`REQ-REL-021..022`);
  - §C breaking / additive / patch classification, the mechanical `cargo-semver-checks` gate, `#[non_exhaustive]`
    future-proofing, behavioral compatibility, and deprecate-before-remove (`REQ-REL-023..029`);
  - §D the Keep-a-Changelog practice and its tie to the semver level across the multi-crate workspace
    (`REQ-REL-030..033`);
  - §E named-peer (Leptos, Dioxus, Yew) and standards comparison;
  - a register summary table and a Metadata section.

## How it composes with the parent
- **J1 (disjoint ranges):** mints only `REQ-REL-020..033`, inside the assigned `020..039`; `034..039` left free
  for additive amendment.
- **J2 (schema conformance):** every `REQ-REL-*` carries id, statement, rationale, acceptance_criteria, stage,
  release_gating, references per `../../contracts/id_and_traceability_schema.yaml`.
- **J3 (framework verification):** every acceptance criterion uses `doc_inspection` and/or `automated_test` from
  the parent's closed vocabulary.
- **J4 (this spoke's share):** the semver contract, the breaking-vs-additive classification, and the changelog
  practice are each covered by more than one requirement.
- **J5:** the MSRV promise and the frozen-`prelude` stability promise are deliberately NOT minted here — they are
  `REQ-REL-040..059` (versioning/compat spoke); referenced read-only so the synthesis gate can assert J5 across
  the subtree without collision.
- **J6:** peers (Leptos, Dioxus, Yew) and the Rust SemVer / API-evolution references are named in §E, feeding the
  merged doc's comparison.

## Grounding
`Nousix-LLC/nswe-demo` @ `276138f` (`main`): the three crates' `prelude` surfaces, `version.workspace`/
`rust-version.workspace` inheritance, and the repo-wide absence of any `CHANGELOG.md` were each confirmed from the
live repository via `gh api`.

## Boundary notes
- Design only (what, not how); no implementation of a CI semver gate or changelog tool.
- Phase B methodology surface was unavailable on this reconstructed node (`agent_domain_unset`); the work was
  grounded in the brief/hub-named standards (Cargo SemVer, RFC 1105, Keep a Changelog, `cargo-semver-checks`) and
  the persona's product-design judgment. This did not affect the deliverable's conformance to the parent contract.

## Verification performed
- Range check: all ids within `REQ-REL-020..039`.
- Field check: all parent schema fields present on every requirement; verification methods within the closed
  vocabulary.
- Grounding check: preludes, manifest inheritance, and changelog absence re-read from the repository.
- avoid-ai-writing pass run over the deliverable before finalizing.
</content>
