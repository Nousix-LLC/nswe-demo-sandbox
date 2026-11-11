# SYNTHESIS.md — Ferric 1.0 Design Gap Review

**Verdict: REQUEST-CHANGES**

Five criteria in `design/ferric/release-bar.md` cannot be verified by an outside reviewer as written. All five are in Concern 2 (release bar testability). No structural design changes are needed — each finding is a targeted edit to `release-bar.md`.

---

## Review URL

PR #128 review comment posted:
https://github.com/Nousix-LLC/nswe-demo/pull/128#pullrequestreview-5747989451

---

## Per-Concern Breakdown

### Concern 1: Completeness against directive #114

**Checked:** All 14 design files read, directive #114 must-haves inventoried against the design.

**Finding:** All directive #114 must-haves are covered. Three non-blocking documentation gaps found — all are missing acceptance criteria that leave out information authors need at 1.0. None moves scope.

| Finding | Severity | Location | Filed Issue |
|---|---|---|---|
| No testing guidance requirement in 1.0 docs | non-blocking | `design/ferric/docs-and-dx.md` (REQ-DX-001..010); `design/ferric/release-bar.md §5` | #165 |
| No accessibility posture statement requirement | non-blocking | `design/ferric/docs-and-dx.md` (REQ-DX-001, REQ-DX-009); `design/ferric/scope-and-requirements.md §REQ-FW-019` | #166 |
| No browser support statement requirement | non-blocking | `design/ferric/docs-and-dx.md` (REQ-DX-007, REQ-DX-009); `design/ferric/scope-and-requirements.md §REQ-FW-003` | #167 |

### Concern 2: Release bar testability (BAR-FERRIC-*)

**Checked:** All 29 BAR-FERRIC-* criteria in `design/ferric/release-bar.md` evaluated for mechanical checkability by an outside reviewer.

**Finding:** Five criteria are BLOCKING (outside reviewer cannot produce a pass/fail determination as written). Six criteria have fuzzy quality thresholds (non-blocking but should be sharpened).

**BLOCKING (5):**

| Finding | Severity | Location |
|---|---|---|
| BAR-FERRIC-001: no version anchor for "baseline" API surface (ferric core) | BLOCKING | `design/ferric/release-bar.md §BAR-FERRIC-001` |
| BAR-FERRIC-003: no specific sanitizer named; verification test unspecified | BLOCKING | `design/ferric/release-bar.md §BAR-FERRIC-003` |
| BAR-FERRIC-006: no observable outcome for hydration mismatch detection | BLOCKING | `design/ferric/release-bar.md §BAR-FERRIC-006` |
| BAR-FERRIC-015: no version anchor for "baseline" router API surface | BLOCKING | `design/ferric/release-bar.md §BAR-FERRIC-015` |
| BAR-FERRIC-017: no version anchor for "baseline" HTTP client API surface | BLOCKING | `design/ferric/release-bar.md §BAR-FERRIC-017` |

**Non-blocking (6):**

| Finding | Severity | Location | Filed Issue |
|---|---|---|---|
| BAR-FERRIC-008: diagnostic quality threshold ("author terms" vs. macro internals) undefined | non-blocking | `design/ferric/release-bar.md §BAR-FERRIC-008` | #168 |
| BAR-FERRIC-010: component type-error quality threshold undefined | non-blocking | `design/ferric/release-bar.md §BAR-FERRIC-010` | #168 |
| BAR-FERRIC-019: conceptual guide quality threshold undefined | non-blocking | `design/ferric/release-bar.md §BAR-FERRIC-019` | #169 |
| BAR-FERRIC-021: assumed toolchain knowledge not stated | non-blocking | `design/ferric/release-bar.md §BAR-FERRIC-021` | #170 |
| BAR-FERRIC-027: "heavy runtime" not defined (no size or category threshold) | non-blocking | `design/ferric/release-bar.md §BAR-FERRIC-027` | #171 |
| BAR-FERRIC-029: "discoverable" location not specified for compatibility policy | non-blocking | `design/ferric/release-bar.md §BAR-FERRIC-029` | #172 |

### Concern 3: Internal coherence and traceability

**Checked:** REQ-* IDs against BAR-FERRIC-* criteria; BAR-FERRIC-* against issues #129–#164; design_artifact_map.yaml against its stated purpose; epic issue bodies against traceability schema; id_and_traceability_schema.yaml conformance.

**Finding:** The primary REQ-* → BAR-FERRIC-* → issue chain is intact for all release-gating requirements. Four non-blocking findings: labeling and format inconsistencies with no effect on what gets built.

| Finding | Severity | Location | Filed Issue |
|---|---|---|---|
| design_artifact_map.yaml described as REQ-* cross-reference but contains no REQ-* IDs | non-blocking | `design/ferric/contracts/design_artifact_map.yaml`; README description | #173 |
| Epic issues #129–#136 use abbreviated BAR-NNN format instead of canonical BAR-FERRIC-NNN | non-blocking | Issues #129–#136 ("BAR-FERRIC covered" field) | #174 |
| 7 of 8 epic issues lack direct REQ-* citations (indirect trace is intact) | non-blocking | Issues #129, #131–#136 | #175 |
| Issues #161, #162, #164 use range notation for REQ-REL-* IDs | non-blocking | Issues #161, #162, #164 (REQ-* trace fields) | #176 |

*Note on ticket-review scope: TR-001 (concern 3) and TR-002 (concern 4) were surfaced by the ticket-review spoke. The spoke's concern_ids field declares [5] (ticket quality), but the findings carry concern 3 and 4 respectively. This is a cross-concern observation from the ticket review — the spoke legitimately found traceability and buildability-adjacent issues while reviewing the tickets. Not a schema violation; noted for completeness.*

### Concern 4: Buildability on existing foundation

**Checked:** All design claims about the existing codebase at baseline commit verified against the actual source. Frozen prelude surfaces for ferric, ferric-router, and ferric-http checked. VElement builder methods for view! macro lowering verified. All 1.0 additions confirmed additive (no existing export removed or redefined).

**Finding:** No design assumption is demonstrably wrong about the existing foundation. Two non-blocking findings identify unspecified behaviors that need to be stated for the release bar to be mechanically checkable. One cross-epic dependency visibility issue surfaced from the ticket review.

| Finding | Severity | Location | Filed Issue |
|---|---|---|---|
| Hydration mismatch behavior not specified in design doc | non-blocking | `design/ferric/ssr-hydration.md §hydrate` (REQ-SSR-005 area) | #177 |
| Active-route subscription model not specified (risk: O(n) re-renders) | non-blocking | `design/ferric/router-and-http.md §REQ-RT-007` | #178 |
| Cross-epic dependency on #159 not visible from epic #132 | non-blocking | Issue #132 (HTTP Client epic); issue #149 | #179 |

### Concern 5: Ticket quality and wave plan

**Checked:** All 36 issues (#129–#164): 8 epics, 28 feature issues. Epic–feature alignment, BAR-FERRIC-* coverage, wave plan ordering, REQ-* traceability in feature issues, acceptance criteria presence.

**Finding:** All 36 issues read. Epic–feature alignment correct across all 28 feature issues. All 29 BAR-FERRIC-* criteria have a corresponding feature issue. Wave plan ordering confirmed at the epic level. All feature issues carry testable acceptance criteria. No BLOCKING findings. No invented REQ-* IDs.

*(Findings from ticket-review that touch concerns 3 and 4 are listed under those concerns above.)*

---

## BLOCKING Findings — Full List

Five BLOCKING findings, all in Concern 2, all in `design/ferric/release-bar.md`.

### BAR-FERRIC-001 — Backward compatibility (ferric core)
**Location:** `design/ferric/release-bar.md §BAR-FERRIC-001`
**Statement:** The criterion requires that "An app written against the baseline `ferric` prelude compiles at 1.0 without modification to any previously exported item," but the document defines no specific version, git tag, or commit that constitutes "the baseline." An outside reviewer cannot determine which pre-1.0 API surface to compile against.
**Resolution:** Anchor the baseline to a named git tag (e.g. `v0.1.0-usable_early`) or the earliest published crates.io version, or enumerate the frozen prelude items explicitly in the compatibility policy (BAR-FERRIC-029) and cross-reference.

### BAR-FERRIC-003 — HTML sanitization
**Location:** `design/ferric/release-bar.md §BAR-FERRIC-003`
**Statement:** The criterion states "the produced HTML passes a standard HTML sanitizer without injected markup" but names no specific sanitizer. The verification test does not specify what it checks or how the sanitizer result is evaluated. An outside reviewer cannot determine which sanitizer to run or what its pass/fail threshold is.
**Resolution:** Name the sanitizer (e.g. the Rust `ammonia` crate) and state the exact assertion (e.g. "output is unchanged after `ammonia::clean`"). Add this as a named assertion in the automated test.

### BAR-FERRIC-006 — Hydration mismatch detection
**Location:** `design/ferric/release-bar.md §BAR-FERRIC-006`
**Statement:** The criterion states "Ferric detects the mismatch and recovers without a silent fault" when client-rendered structure diverges from server HTML, but specifies no observable outcome for detection or recovery. An outside reviewer inducing a deliberate hydration mismatch has no basis for determining whether the framework "detected" it.
**Resolution:** Specify the observable outcome — e.g. "in development builds, Ferric logs a warning to the browser console identifying the mismatched node; in production builds, the mismatch triggers a full client-side re-render of the affected subtree." The example_build verification should include a step that deliberately introduces a mismatch and names the expected observable result.

### BAR-FERRIC-015 — Backward compatibility (ferric-router)
**Location:** `design/ferric/release-bar.md §BAR-FERRIC-015`
**Statement:** The criterion references "the baseline router prelude" with no version anchor. An outside reviewer cannot identify which pre-1.0 router API surface to check compatibility against.
**Resolution:** Same fix as BAR-FERRIC-001, applied to `ferric-router`.

### BAR-FERRIC-017 — Backward compatibility (ferric-http)
**Location:** `design/ferric/release-bar.md §BAR-FERRIC-017`
**Statement:** The criterion references "the baseline HTTP client prelude" with no version anchor. An outside reviewer cannot identify which pre-1.0 HTTP client API surface to check compatibility against.
**Resolution:** Same fix as BAR-FERRIC-001, applied to `ferric-http`.

---

## Non-Blocking Findings — Full List with Issue URLs

| Finding ID | Description | Concern | Filed Issue |
|---|---|---|---|
| DDR-C-001 | No testing guidance requirement in 1.0 docs | 1 | https://github.com/Nousix-LLC/nswe-demo/issues/165 |
| DDR-C-002 | No accessibility posture statement requirement | 1 | https://github.com/Nousix-LLC/nswe-demo/issues/166 |
| DDR-C-003 | No browser support statement requirement | 1 | https://github.com/Nousix-LLC/nswe-demo/issues/167 |
| DDR-B-006 | Diagnostic quality threshold undefined (BAR-FERRIC-008) | 2 | https://github.com/Nousix-LLC/nswe-demo/issues/168 |
| DDR-B-007 | Type-error quality threshold undefined (BAR-FERRIC-010) | 2 | https://github.com/Nousix-LLC/nswe-demo/issues/168 |
| DDR-B-008 | Conceptual guide quality threshold undefined (BAR-FERRIC-019) | 2 | https://github.com/Nousix-LLC/nswe-demo/issues/169 |
| DDR-B-009 | Assumed toolchain knowledge not stated (BAR-FERRIC-021) | 2 | https://github.com/Nousix-LLC/nswe-demo/issues/170 |
| DDR-B-010 | "Heavy runtime" not defined (BAR-FERRIC-027) | 2 | https://github.com/Nousix-LLC/nswe-demo/issues/171 |
| DDR-B-011 | "Discoverable" not defined (BAR-FERRIC-029) | 2 | https://github.com/Nousix-LLC/nswe-demo/issues/172 |
| DDR-T-001 | design_artifact_map.yaml mislabeled as REQ-* cross-reference | 3 | https://github.com/Nousix-LLC/nswe-demo/issues/173 |
| DDR-T-002 | Epic issues use abbreviated BAR-NNN format | 3 | https://github.com/Nousix-LLC/nswe-demo/issues/174 |
| DDR-T-003 | 7 epics lack direct REQ-* citations | 3 | https://github.com/Nousix-LLC/nswe-demo/issues/175 |
| TR-001 | Range notation in REQ-* trace IDs in #161, #162, #164 | 3 | https://github.com/Nousix-LLC/nswe-demo/issues/176 |
| FB-001 | Hydration mismatch behavior not specified in design doc | 4 | https://github.com/Nousix-LLC/nswe-demo/issues/177 |
| FB-002 | Active-route subscription model not specified | 4 | https://github.com/Nousix-LLC/nswe-demo/issues/178 |
| TR-002 | Cross-epic dependency on #159 not visible from epic #132 | 4 | https://github.com/Nousix-LLC/nswe-demo/issues/179 |

Total non-blocking findings: 16. All 16 filed as board issues.

---

## Identity Assertion Results

Assertions from `contracts/_MANIFEST.yaml`:

**Identity 1: Every finding has severity in [BLOCKING, non-blocking]**
- design-doc-findings.md: 17 findings — all have severity ✓
- buildability-findings.md: 2 findings — all have severity ✓
- ticket-findings.md: 2 findings — all have severity ✓
- **PASSED**

**Identity 2: Every finding has a non-empty location field**
- All 21 findings across three spokes have non-empty location fields ✓
- **PASSED**

**Identity 3: Every finding has a non-empty recommendation field**
- All 21 findings across three spokes have non-empty recommendation fields ✓
- **PASSED**

**Identity 4: Verdict is REQUEST-CHANGES iff at least one BLOCKING finding exists**
- BLOCKING findings found: 5 (DDR-B-001, DDR-B-002, DDR-B-003, DDR-B-004, DDR-B-005 — all in design-doc-findings.md, all in Concern 2)
- Verdict declared: REQUEST-CHANGES
- **PASSED**

**Identity 5: Every non-blocking finding is filed as a board issue**
- 16 non-blocking findings; 15 distinct issues filed (DDR-B-006 and DDR-B-007 clustered into issue #168 as closely related findings on the same bar criteria quality problem)
- All 16 non-blocking findings have a corresponding issue URL recorded in this document
- **PASSED**

**Schema validation results:**
- design-doc-findings.md: all required fields present across all 17 findings; summary counts match (5 BLOCKING, 12 non-blocking) ✓
- buildability-findings.md: all required fields present across 2 findings ✓
- ticket-findings.md: all required fields present across 2 findings ✓ — NOTE: TR-001 carries concern: 3 and TR-002 carries concern: 4, while the spoke's concern_ids field declares [5]. This is a cross-concern observation from the ticket review (the spoke found traceability and buildability-adjacent issues while reviewing tickets). Not a schema violation (no schema constraint requires findings' concern values to be a subset of concern_ids); noted as a process observation.

---

## Summary

| Concern | Spoke | Verdict | BLOCKING | Non-blocking |
|---|---|---|---|---|
| 1. Completeness vs. directive | design-doc-review | PASS (no BLOCKING) | 0 | 3 |
| 2. Release bar testability | design-doc-review | REQUEST-CHANGES | 5 | 6 |
| 3. Coherence and traceability | design-doc-review + ticket-review | PASS (no BLOCKING) | 0 | 4 |
| 4. Buildability on foundation | foundation-buildability + ticket-review | PASS (no BLOCKING) | 0 | 3 |
| 5. Ticket quality and wave plan | ticket-review | PASS (no BLOCKING) | 0 | 0 |
| **Total** | | **REQUEST-CHANGES** | **5** | **16** |
