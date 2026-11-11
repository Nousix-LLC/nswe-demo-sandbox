# Concern Findings: Release & Distribution

## concern_name

crates.io publishing, semver contract, changelog, and versioning & compatibility policy

---

## document_validated

`design/ferric/release-and-distribution.md` on branch `work/design-ferric-1_0`

Also consulted: `prior-art/release-and-distribution.md` (the prior-art draft this document synthesises from)

---

## req_ids_found

33 requirements defined across four concern areas:

**Publishing readiness & multi-crate release (§1):**
REQ-REL-001, REQ-REL-002, REQ-REL-003, REQ-REL-004, REQ-REL-005, REQ-REL-006, REQ-REL-007,
REQ-REL-008, REQ-REL-009, REQ-REL-010, REQ-REL-011

**Semver contract & changelog practice (§2):**
REQ-REL-020, REQ-REL-021, REQ-REL-022, REQ-REL-023, REQ-REL-024, REQ-REL-025, REQ-REL-026,
REQ-REL-027, REQ-REL-028, REQ-REL-029, REQ-REL-030, REQ-REL-031, REQ-REL-032, REQ-REL-033

**Versioning & compatibility policy (§3):**
REQ-REL-040, REQ-REL-041, REQ-REL-042, REQ-REL-043, REQ-REL-044, REQ-REL-045, REQ-REL-046,
REQ-REL-047

**Reserved, not defined (as documented in both files):**
REQ-REL-012..019, REQ-REL-034..039, REQ-REL-048..059

---

## status

**valid**

All validation criteria pass. The branch document fully reconciles the prior-art and covers every required surface.

---

## specific_issues

[]

No issues found.

---

## gaps

[]

No gaps in range GAP-060..069 required.

---

## Validation detail

### Prior-art reconciliation

The branch document reconciles the prior-art draft. Every requirement from the prior-art (33 REQ-REL-* ids
across all four concern areas) is present in the branch version. The structural difference — the prior-art
kept semver contract (§2, REQ-REL-020..029) and changelog practice (§3, REQ-REL-030..033) as separate
sections, while the branch merges them into one section (§2, REQ-REL-020..033, "Semver Contract &
Changelog Practice") — is a legitimate consolidation. Both documents define the same id set with the same
acceptance criteria.

The branch document also tightens minor formatting details: verification methods appear inline in
parentheses on each acceptance-criterion bullet rather than in a separate `**Verification:**` line per
requirement, then are collected in the full register summary table. This is a presentation difference, not
a content gap.

### crates.io metadata requirements: stated and testable

All six metadata fields the brief specifies are covered:

| Field | Requirement | Verification |
|---|---|---|
| name | REQ-REL-007 (crate name matches owned crates.io name) | doc_inspection |
| description | REQ-REL-002 | doc_inspection, publishability |
| keywords | REQ-REL-002 | doc_inspection, publishability |
| license | REQ-REL-001 | doc_inspection, publishability |
| repository URL | REQ-REL-002 | doc_inspection |
| documentation URL | REQ-REL-002 | doc_inspection |

Note: `name` is addressed through REQ-REL-007 (ownership/identity check: "The manifest `name` of each
crate matches the owned crates.io name") rather than REQ-REL-002. This split is correct: `name` is a
required Cargo package identifier, not an optional metadata field. REQ-REL-002 lists the fields an
author would expect to see on a crate's crates.io page that require explicit manifest entries.

Each requirement carries concrete acceptance criteria (specific `cargo` command outputs, field presence
checks) against named verification methods from the parent vocabulary.

### Semver policy: stated with clear rules for breaking changes

REQ-REL-021 defines what MAJOR, MINOR, and PATCH each permit and forbid. REQ-REL-023 lists the breaking
change kinds at least: removing or renaming a public item; changing a function or method signature;
adding a required trait method without a default; adding a variant to a non-`#[non_exhaustive]` enum;
adding a public field to a struct without `#[non_exhaustive]`; and making a public item private.
REQ-REL-026 requires `cargo-semver-checks` as a mechanical gate so the classification is not dependent
on reviewer memory. REQ-REL-028 extends the contract to documented behavior, not only type signatures.

All rules are testable: each acceptance criterion names a specific verification method (doc_inspection,
automated_test) and describes a concrete check a reviewer can run.

### Changelog format: required

REQ-REL-030 explicitly requires Keep a Changelog 1.1.0 structure: reverse-chronological, per-version
sections with dates, and an `Unreleased` section at the top. REQ-REL-031 further specifies entry
content (change type, affected crate, breaking/additive marking). REQ-REL-032 ties the semver level
to the strongest entry in the changelog so the two cannot disagree.

### Multi-crate workspace versioning: addressed

REQ-REL-009 (publishing mechanics) and REQ-REL-044 (compatibility policy) both require lockstep
versioning. REQ-REL-044 rationale explicitly states that "1.0 keeps the workspace's lockstep versioning
(`version.workspace = true`) rather than letting the crates drift to independent version numbers" and
that "allowing independent versions later would itself be a policy change for a future major." Independent
versioning within 1.x is therefore not permitted; it would require a 2.0. The requirement is clear
and the policy choice is documented with its rationale.

### Testability

Every requirement in the branch document has acceptance criteria with a named verification method from
the parent vocabulary: `publishability`, `doc_inspection`, `automated_test`, `example_build`. No
requirement is stated as a vague aspiration; each has at least one concrete check a reviewer can run
against the live crates or repository.
