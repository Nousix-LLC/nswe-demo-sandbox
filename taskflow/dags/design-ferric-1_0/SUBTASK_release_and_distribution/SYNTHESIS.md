# SYNTHESIS.md — SUBTASK_release_and_distribution (concern 7)

**Synthesis task:** `SUBTASK_rel_synthesis`
**Folded parent:** `SUBTASK_release_and_distribution`
**Output authored:** `release-and-distribution.md` (at this subtree root)

---

## What was merged

Three spoke partials, each owning a disjoint `REQ-REL-*` range, were assembled verbatim into one
consolidated design document. No requirement was re-derived; each was carried from its partial with its
id, statement, rationale, acceptance criteria, stage, release_gating, and references intact.

| Spoke | Partial | Range merged |
|---|---|---|
| `SUBTASK_publishing` | `SUBTASK_publishing/publishing.md` | `REQ-REL-001..011` |
| `SUBTASK_semver_changelog` | `SUBTASK_semver_changelog/semver-changelog.md` | `REQ-REL-020..033` |
| `SUBTASK_versioning_compat` | `SUBTASK_versioning_compat/versioning-compat.md` | `REQ-REL-040..047` |

---

## Identity assertion results

### J1 — Disjoint REQ-REL ranges
**PASS.** Publishing: REQ-REL-001..011 (REQ-REL-012..019 unused/reserved); Semver: REQ-REL-020..033
(REQ-REL-034..039 unused/reserved); Versioning: REQ-REL-040..047 (REQ-REL-048..059 unused/reserved).
No id appears in two spokes; no collision.

### J2 — Schema conformance
**PASS.** Every REQ-REL-* carries all required fields per `../../contracts/id_and_traceability_schema.yaml`:
`id`, `statement`, `rationale`, `acceptance_criteria`, `stage`, `release_gating`, and `references`. The
semver-changelog spoke renders `verification_method` as a separate `Verification:` field in its formatting;
the value is present and from the closed vocabulary. All 33 defined requirements conform.

### J3 — Framework-appropriate verification methods
**PASS.** All verification methods used across the three partials: `doc_inspection`, `automated_test`,
`publishability`, `example_build`. Every method is in the parent contract's closed vocabulary. No method
outside the vocabulary was used. Summary:
- `publishability`: REQ-REL-001..011 extensively; REQ-REL-044, REQ-REL-045
- `doc_inspection`: present in all three spokes
- `automated_test`: present in all three spokes
- `example_build`: REQ-REL-045

### J4 — All four concerns covered
**PASS.**
- Publishing readiness: ✅ REQ-REL-001..011 (11 requirements)
- Semver contract: ✅ REQ-REL-020..022, REQ-REL-028..029 (the semver level and classification contract)
- Changelog practice: ✅ REQ-REL-030..033 (4 requirements)
- Versioning/compatibility policy: ✅ REQ-REL-040..047 (8 requirements)

### J5 — 1.0 promise stated
**PASS.**
- MSRV promise: ✅ REQ-REL-040 ("1.0 states a supported minimum Rust version (MSRV)")
- Frozen-prelude stability promise for 1.0: ✅ REQ-REL-042 ("The frozen `prelude` surfaces stay usable
  across 1.x") and REQ-REL-047 (scope of the stability promise stated explicitly)

### J6 — Peers named
**PASS.** The merged document names Leptos, Dioxus, and Yew in the "Peer and standards comparison" section
and in individual requirement rationales. Standards cited by name: Semantic Versioning 2.0.0, the Cargo
book "SemVer Compatibility" chapter, RFC 1105 (Rust API evolution), RFC 2495 (rust-version field), RFC 3537
(MSRV-aware resolver), Rust API Guidelines, Keep a Changelog 1.1.0, and `cargo-semver-checks`. Tokio named
as counter-example for independent per-crate versioning (REQ-REL-044).

### J7 — Placed once, repo shape
**PASS.**
- Complete register: 33 defined requirements (REQ-REL-001..011, REQ-REL-020..033, REQ-REL-040..047)
  carried in one document. No range gaps in the used sequences; unused ranges (012..019, 034..039,
  048..059) documented as reserved.
- No id duplication.
- Metadata section present: names `SUBTASK_rel_synthesis` as owning task, lists conforms_to contracts
  (`../../contracts/id_and_traceability_schema.yaml` and `../contracts/_MANIFEST.yaml`), lists sources
  merged, names repo target `design/ferric/release-and-distribution.md`.
- Shape: matches the repo design-doc shape — opening prose paragraph, "what this settles / what it does
  not" framing, "grounding" paragraph, numbered sections, requirements within sections, register summary
  table, peer comparison section, Metadata section.

### Parent identity I1 — Disjoint registers
**PASS.** This document writes only `REQ-REL-*` ids. No id from any other area register was minted here.

---

## Gaps surfaced

None. All three partials produced well-formed requirements within their assigned ranges, all schema fields
are present, all identities passed, and no range collision occurred. No plugging was needed.

---

## Completion record

The consolidated `release-and-distribution.md` is now at the parent workspace root. This `SYNTHESIS.md` is
the fold record. The parent task `SUBTASK_release_and_distribution` is folded from SUSPENDED to COMPLETED
via `engine_resume_suspended`.
