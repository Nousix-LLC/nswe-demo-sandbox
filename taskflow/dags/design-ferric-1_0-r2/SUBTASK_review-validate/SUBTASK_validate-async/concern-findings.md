# Concern Findings: Async resources, events, and forms

## concern_name

Async resources, events, and forms (concern 4)

## document_validated

`design/ferric/async-forms-events.md` on branch `work/design-ferric-1_0`

Compared against: `prior-art/async-forms-events.md`

## req_ids_found

25 requirements minted in this document (all REQ-ASYNC-*; no ids outside this register):

**Section A — Async resources and suspense (REQ-ASYNC-001..016):**
REQ-ASYNC-001, REQ-ASYNC-002, REQ-ASYNC-003, REQ-ASYNC-004, REQ-ASYNC-005,
REQ-ASYNC-006, REQ-ASYNC-007, REQ-ASYNC-008, REQ-ASYNC-009, REQ-ASYNC-010,
REQ-ASYNC-011, REQ-ASYNC-012, REQ-ASYNC-013, REQ-ASYNC-014, REQ-ASYNC-015,
REQ-ASYNC-016

**Section B — Full DOM event coverage and payload-carrying handler (REQ-ASYNC-020..024):**
REQ-ASYNC-020, REQ-ASYNC-021, REQ-ASYNC-022, REQ-ASYNC-023, REQ-ASYNC-024

**Section C — Forms and two-way input binding (REQ-ASYNC-040..043):**
REQ-ASYNC-040, REQ-ASYNC-041, REQ-ASYNC-042, REQ-ASYNC-043

**Unused headroom (reserved per manifest, not minted):**
REQ-ASYNC-017..019, REQ-ASYNC-025..039, REQ-ASYNC-044..059

**Cross-area references (read-only, no id minted here):**
REQ-FW-006 (upstream requirement being specialized), REQ-FW-009 (frozen surfaces),
REQ-FW-013 (lean dependency footprint), REQ-SSR-* (hydration, referenced read-only in
REQ-ASYNC-012 and 013), REQ-HTTP-* (HTTP client, referenced read-only in REQ-ASYNC-014),
REQ-API-* (authoring model, referenced read-only in REQ-ASYNC-003 and sections)

## status

valid

All six validation criteria pass. See per-criterion assessment below.

## Per-criterion assessment

**1. Branch reconciles prior-art draft**

PASS. The branch version carries the same 25 requirements with the same IDs, the same
baseline description (276138f), the same three capabilities, and the same peer
comparison tables. Structural differences are editorial: the prior-art uses
`# Section A/B/C` with lettered sub-sections (A.1–A.4, B.1–B.5, C.1–C.5); the branch
uses `## 1.`, `## 2.`, `## 3.` with generic sub-sections. The prior-art has a dedicated
`## What concern 4 settles, traced to REQ-FW-006` traceability section near the top;
the branch places the equivalent table in the register summary. The branch condenses the
J1–J7 sub-contract identity assertions to a single line ("Sub-identities J1–J7 all pass
(verified by SUBTASK_afe_synthesis; see SYNTHESIS.md)") rather than naming each one. No
requirement content is absent; no requirement ID is dropped or renumbered.

**2. Async resources addressed with testable requirements**

PASS. REQ-ASYNC-001 through REQ-ASYNC-016 cover the full async-resource primitive
surface: the primitive itself (001), four-state reactive read (002), declarative
state-to-view mapping (003), empty as a first-class declared state (004), error carriage
without wedging (005), re-fetch on reactive dependency change (006), imperative refetch
(007), composition with the reactive graph (008), suspense boundary over multiple
resources (009), nested suspense boundaries (010), reloading-with-previous-value (011),
SSR handoff by reference (012–013), abstract data source (014), additivity over frozen
surfaces (015), and superseded-fetch cleanup (016). Every requirement carries explicit
acceptance criteria with named verification_method values (automated_test,
wasm-bindgen-test, example_build, or doc_inspection). All are release_gating: true.

**3. Suspense-style loading and error states addressed**

PASS. Loading states: REQ-ASYNC-002 (four states, including loading, as a reactive
read), REQ-ASYNC-003 (declarative per-state render), REQ-ASYNC-011 (loading-with-prior-
value distinct from first load). Error states: REQ-ASYNC-005 (error carries the failure
value, does not wedge the view), REQ-ASYNC-007 (imperative refetch recovers from error).
Suspense aggregation: REQ-ASYNC-009 (boundary over multiple pending resources) and
REQ-ASYNC-010 (nested boundaries for staged reveal). The empty state is also addressed
as a first-class concern in REQ-ASYNC-004, which goes beyond peers that leave it to
author-written conditionals. All requirements have testable acceptance criteria with
wasm-bindgen-test and example_build verification.

**4. Two-way form binding addressed**

PASS. REQ-ASYNC-040 (basic two-way binding of one signal to one input, both directions),
REQ-ASYNC-041 (per-kind coverage: text, textarea, checkbox, radio group, single select,
multiple select, number input), REQ-ASYNC-042 (reactive validation ergonomics: per-field
and per-form validity and error messages without a bundled DSL), REQ-ASYNC-043
(submission: suppress default navigation, read model from signals, gate on validity).
The seam between forms and events is handled correctly: binding is composed on the
payload-carrying handler (REQ-ASYNC-020) and value read (REQ-ASYNC-022) from Section B,
not restated.

**5. Full DOM event handling surface addressed**

PASS. REQ-ASYNC-020 (payload-carrying handler form, additive over the frozen zero-arg
form), REQ-ASYNC-021 (full event coverage: submit, keydown, keyup, keypress, focus,
blur, change, plus any event by name; baseline click and input remain first-class),
REQ-ASYNC-022 (reading event data: input value, key, raw web_sys::Event),
REQ-ASYNC-023 (default-action and propagation control from a payload handler),
REQ-ASYNC-024 (re-binding guarantees across the keyed diff, stated as author-facing
contract for both handler forms and all event types). The event-payload seam is defined
once in Section B (sub-contract J3) and referenced read-only by Section C.

**6. Requirements testable by a stranger checking a running framework**

PASS. All 25 requirements carry at least one acceptance criterion, and each criterion
names a verification_method from the parent contract schema: automated_test (native
cargo test or headless wasm-bindgen-test), example_build (a compilable example against
the 1.0 surface), or doc_inspection (the document itself stating the required fact).
Criteria describe observable outcomes ("the resource's value becomes the fetched data
after the fetch resolves," "submitting the form does not reload or navigate the page")
that a reviewer checking a live framework can verify without needing to know the
implementation. No criterion relies on internal state or memory of design intent.

## specific_issues

(none — status is valid)

## gaps

### GAP-031

- **id**: GAP-031
- **description**: Inconsistent schema path reference within the document. The inline
  requirements prose cites `contracts/id_and_traceability_schema.yaml` (no directory
  prefix, ambiguous from `design/ferric/`), while the metadata table at the bottom cites
  `../../contracts/id_and_traceability_schema.yaml` (resolves to the repo root
  `contracts/`). One path is wrong; the prior-art used `../../contracts/` in the
  metadata, consistent with the repo layout where the parent schema lives at root level.
- **severity**: minor
- **action_required**: Standardize the schema path reference to
  `../../contracts/id_and_traceability_schema.yaml` throughout the document (or whatever
  the correct repo-relative path is), so the inline reference and the metadata table
  agree and both resolve to the same file.

### GAP-032

- **id**: GAP-032
- **description**: The prior-art's dedicated "Register summary and traceability" section
  named and verified each sub-contract identity (J1–J7) individually with prose
  evidence. The branch version condenses this to one line: "Sub-identities J1–J7 all
  pass (verified by SUBTASK_afe_synthesis; see SYNTHESIS.md)." An independent reviewer
  checking the document alone cannot verify J4 (additive over frozen surfaces — stated
  throughout but not explicitly asserted per-item) or J7 (conforms to parent schema —
  stated in metadata but not cross-checked) without reading SYNTHESIS.md. This does not
  affect the requirements themselves, but it weakens the document's self-contained
  auditability.
- **severity**: minor
- **action_required**: Either restore the named per-identity assertions in the register
  summary (listing J1 through J7 with a one-line verification statement for each), or
  confirm that SYNTHESIS.md is available alongside the document and that reviewers are
  directed there. If SYNTHESIS.md accompanies the branch file, this gap may be closed
  by adding a cross-reference note in the register summary.
