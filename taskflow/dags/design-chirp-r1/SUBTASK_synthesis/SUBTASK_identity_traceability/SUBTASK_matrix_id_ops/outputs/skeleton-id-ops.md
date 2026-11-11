# Traceability-matrix skeleton — design-side columns for REQ-ID-* and REQ-OPS-*

This is one slice of the whole-DAG traceability-matrix skeleton: the **design-side columns**
(`req_id`, `release_gating`, `design_doc_ref`) for the two requirement areas this spoke owns —
identity, security & trust (`REQ-ID-*`) and operational readiness (`REQ-OPS-*`). It is keyed on
`req_id` so the synthesis child can join it on that key with the other skeleton slices, the
`REQ → bar_ids` map, and the `REQ/BAR → (epic, issue_numbers)` map.

This slice computes **no** `bar_ids`, `epic`, or `issue_numbers`, fills **no** `live_status`, and
asserts **no** identity. Those columns and checks belong to the sibling spokes and the synthesis
child per the subtree sub-contract.

## Column semantics

- **`req_id`** — the requirement id, used verbatim from the design file (`REQ-<AREA>-<NNN>`, the
  inherited scheme; not renamed).
- **`release_gating`** — the boolean value of the requirement's `release_gating` field, verbatim
  from the design file's consolidated requirements register (`true` or `false`). Non-gating
  (`false`) entries carry an inline reason in the design file itself; that rationale prose is not a
  value of this column and is read at the `design_doc_ref` section when needed.
- **`design_doc_ref`** — the repo-relative design path (from `design_artifact_map.yaml`) plus the
  requirement's own section heading. Format: `design/<file>.md § REQ-<AREA>-<NNN>`. The path is the
  committed repository artifact, independent of where the taskflow produced the file.

## Sources (both COMPLETED, read read-only)

| Area | `req_id` prefix | Design file (repo-relative, for `design_doc_ref`) | Register read |
|------|-----------------|---------------------------------------------------|---------------|
| Identity, security & trust | `REQ-ID-` | `design/identity-security.md` | `## Requirements and acceptance criteria` consolidated register (one `#### REQ-ID-NNN` entry per requirement) |
| Operational readiness | `REQ-OPS-` | `design/operational-readiness.md` | `## requirements_and_acceptance_criteria` consolidated register (one `#### REQ-OPS-NNN` entry per requirement) |

## Counts (actual, found in the design files)

| Area | Rows (requirements) | `release_gating: true` | `release_gating: false` |
|------|---------------------|------------------------|-------------------------|
| `REQ-ID-*`  | 73  | 63 | 10 |
| `REQ-OPS-*` | 75  | 59 | 16 |
| **Total**   | **148** | **122** | **26** |

The subtree hub and this spoke's brief estimated "on the order of 110 + 109" for the two areas; the
brief directed reporting the actual count found. The actuals are **73** and **75**. The id schemes
are block-allocated with intentional gaps (see the gap note below), so counting by the highest id
(`REQ-ID-101`, `REQ-OPS-095`) or by a dense range overstates the count — the actual register-entry
counts above are authoritative. Every row below corresponds to exactly one defining register entry;
no row is emitted for an id that has no entry.

---

## REQ-ID-* — identity, security & trust (73 rows)

| req_id | release_gating | design_doc_ref |
|--------|----------------|----------------|
| REQ-ID-001 | true | design/identity-security.md § REQ-ID-001 |
| REQ-ID-002 | true | design/identity-security.md § REQ-ID-002 |
| REQ-ID-003 | true | design/identity-security.md § REQ-ID-003 |
| REQ-ID-004 | true | design/identity-security.md § REQ-ID-004 |
| REQ-ID-005 | true | design/identity-security.md § REQ-ID-005 |
| REQ-ID-006 | false | design/identity-security.md § REQ-ID-006 |
| REQ-ID-007 | true | design/identity-security.md § REQ-ID-007 |
| REQ-ID-008 | true | design/identity-security.md § REQ-ID-008 |
| REQ-ID-009 | true | design/identity-security.md § REQ-ID-009 |
| REQ-ID-010 | true | design/identity-security.md § REQ-ID-010 |
| REQ-ID-011 | false | design/identity-security.md § REQ-ID-011 |
| REQ-ID-012 | false | design/identity-security.md § REQ-ID-012 |
| REQ-ID-013 | true | design/identity-security.md § REQ-ID-013 |
| REQ-ID-014 | true | design/identity-security.md § REQ-ID-014 |
| REQ-ID-015 | true | design/identity-security.md § REQ-ID-015 |
| REQ-ID-016 | true | design/identity-security.md § REQ-ID-016 |
| REQ-ID-017 | true | design/identity-security.md § REQ-ID-017 |
| REQ-ID-018 | true | design/identity-security.md § REQ-ID-018 |
| REQ-ID-019 | true | design/identity-security.md § REQ-ID-019 |
| REQ-ID-020 | true | design/identity-security.md § REQ-ID-020 |
| REQ-ID-021 | true | design/identity-security.md § REQ-ID-021 |
| REQ-ID-022 | true | design/identity-security.md § REQ-ID-022 |
| REQ-ID-023 | true | design/identity-security.md § REQ-ID-023 |
| REQ-ID-024 | true | design/identity-security.md § REQ-ID-024 |
| REQ-ID-030 | true | design/identity-security.md § REQ-ID-030 |
| REQ-ID-031 | true | design/identity-security.md § REQ-ID-031 |
| REQ-ID-032 | true | design/identity-security.md § REQ-ID-032 |
| REQ-ID-033 | true | design/identity-security.md § REQ-ID-033 |
| REQ-ID-034 | true | design/identity-security.md § REQ-ID-034 |
| REQ-ID-035 | true | design/identity-security.md § REQ-ID-035 |
| REQ-ID-036 | true | design/identity-security.md § REQ-ID-036 |
| REQ-ID-037 | true | design/identity-security.md § REQ-ID-037 |
| REQ-ID-038 | true | design/identity-security.md § REQ-ID-038 |
| REQ-ID-039 | true | design/identity-security.md § REQ-ID-039 |
| REQ-ID-040 | true | design/identity-security.md § REQ-ID-040 |
| REQ-ID-041 | true | design/identity-security.md § REQ-ID-041 |
| REQ-ID-042 | true | design/identity-security.md § REQ-ID-042 |
| REQ-ID-043 | true | design/identity-security.md § REQ-ID-043 |
| REQ-ID-044 | true | design/identity-security.md § REQ-ID-044 |
| REQ-ID-045 | true | design/identity-security.md § REQ-ID-045 |
| REQ-ID-046 | true | design/identity-security.md § REQ-ID-046 |
| REQ-ID-047 | false | design/identity-security.md § REQ-ID-047 |
| REQ-ID-048 | false | design/identity-security.md § REQ-ID-048 |
| REQ-ID-050 | false | design/identity-security.md § REQ-ID-050 |
| REQ-ID-051 | false | design/identity-security.md § REQ-ID-051 |
| REQ-ID-060 | true | design/identity-security.md § REQ-ID-060 |
| REQ-ID-061 | true | design/identity-security.md § REQ-ID-061 |
| REQ-ID-062 | true | design/identity-security.md § REQ-ID-062 |
| REQ-ID-063 | true | design/identity-security.md § REQ-ID-063 |
| REQ-ID-064 | true | design/identity-security.md § REQ-ID-064 |
| REQ-ID-065 | true | design/identity-security.md § REQ-ID-065 |
| REQ-ID-066 | true | design/identity-security.md § REQ-ID-066 |
| REQ-ID-067 | true | design/identity-security.md § REQ-ID-067 |
| REQ-ID-068 | true | design/identity-security.md § REQ-ID-068 |
| REQ-ID-069 | true | design/identity-security.md § REQ-ID-069 |
| REQ-ID-070 | true | design/identity-security.md § REQ-ID-070 |
| REQ-ID-071 | true | design/identity-security.md § REQ-ID-071 |
| REQ-ID-072 | true | design/identity-security.md § REQ-ID-072 |
| REQ-ID-073 | true | design/identity-security.md § REQ-ID-073 |
| REQ-ID-074 | true | design/identity-security.md § REQ-ID-074 |
| REQ-ID-080 | true | design/identity-security.md § REQ-ID-080 |
| REQ-ID-081 | true | design/identity-security.md § REQ-ID-081 |
| REQ-ID-082 | true | design/identity-security.md § REQ-ID-082 |
| REQ-ID-083 | false | design/identity-security.md § REQ-ID-083 |
| REQ-ID-084 | false | design/identity-security.md § REQ-ID-084 |
| REQ-ID-085 | true | design/identity-security.md § REQ-ID-085 |
| REQ-ID-086 | true | design/identity-security.md § REQ-ID-086 |
| REQ-ID-087 | true | design/identity-security.md § REQ-ID-087 |
| REQ-ID-088 | true | design/identity-security.md § REQ-ID-088 |
| REQ-ID-089 | false | design/identity-security.md § REQ-ID-089 |
| REQ-ID-090 | true | design/identity-security.md § REQ-ID-090 |
| REQ-ID-100 | true | design/identity-security.md § REQ-ID-100 |
| REQ-ID-101 | true | design/identity-security.md § REQ-ID-101 |

## REQ-OPS-* — operational readiness (75 rows)

| req_id | release_gating | design_doc_ref |
|--------|----------------|----------------|
| REQ-OPS-001 | true | design/operational-readiness.md § REQ-OPS-001 |
| REQ-OPS-002 | true | design/operational-readiness.md § REQ-OPS-002 |
| REQ-OPS-003 | true | design/operational-readiness.md § REQ-OPS-003 |
| REQ-OPS-004 | true | design/operational-readiness.md § REQ-OPS-004 |
| REQ-OPS-005 | true | design/operational-readiness.md § REQ-OPS-005 |
| REQ-OPS-006 | true | design/operational-readiness.md § REQ-OPS-006 |
| REQ-OPS-007 | true | design/operational-readiness.md § REQ-OPS-007 |
| REQ-OPS-008 | true | design/operational-readiness.md § REQ-OPS-008 |
| REQ-OPS-009 | true | design/operational-readiness.md § REQ-OPS-009 |
| REQ-OPS-010 | true | design/operational-readiness.md § REQ-OPS-010 |
| REQ-OPS-011 | true | design/operational-readiness.md § REQ-OPS-011 |
| REQ-OPS-012 | true | design/operational-readiness.md § REQ-OPS-012 |
| REQ-OPS-013 | true | design/operational-readiness.md § REQ-OPS-013 |
| REQ-OPS-014 | true | design/operational-readiness.md § REQ-OPS-014 |
| REQ-OPS-015 | true | design/operational-readiness.md § REQ-OPS-015 |
| REQ-OPS-016 | true | design/operational-readiness.md § REQ-OPS-016 |
| REQ-OPS-020 | true | design/operational-readiness.md § REQ-OPS-020 |
| REQ-OPS-021 | true | design/operational-readiness.md § REQ-OPS-021 |
| REQ-OPS-022 | true | design/operational-readiness.md § REQ-OPS-022 |
| REQ-OPS-023 | true | design/operational-readiness.md § REQ-OPS-023 |
| REQ-OPS-024 | true | design/operational-readiness.md § REQ-OPS-024 |
| REQ-OPS-025 | true | design/operational-readiness.md § REQ-OPS-025 |
| REQ-OPS-026 | true | design/operational-readiness.md § REQ-OPS-026 |
| REQ-OPS-027 | true | design/operational-readiness.md § REQ-OPS-027 |
| REQ-OPS-028 | true | design/operational-readiness.md § REQ-OPS-028 |
| REQ-OPS-029 | true | design/operational-readiness.md § REQ-OPS-029 |
| REQ-OPS-030 | true | design/operational-readiness.md § REQ-OPS-030 |
| REQ-OPS-031 | true | design/operational-readiness.md § REQ-OPS-031 |
| REQ-OPS-032 | true | design/operational-readiness.md § REQ-OPS-032 |
| REQ-OPS-033 | true | design/operational-readiness.md § REQ-OPS-033 |
| REQ-OPS-040 | true | design/operational-readiness.md § REQ-OPS-040 |
| REQ-OPS-041 | true | design/operational-readiness.md § REQ-OPS-041 |
| REQ-OPS-042 | true | design/operational-readiness.md § REQ-OPS-042 |
| REQ-OPS-043 | true | design/operational-readiness.md § REQ-OPS-043 |
| REQ-OPS-044 | true | design/operational-readiness.md § REQ-OPS-044 |
| REQ-OPS-045 | true | design/operational-readiness.md § REQ-OPS-045 |
| REQ-OPS-046 | true | design/operational-readiness.md § REQ-OPS-046 |
| REQ-OPS-047 | false | design/operational-readiness.md § REQ-OPS-047 |
| REQ-OPS-048 | false | design/operational-readiness.md § REQ-OPS-048 |
| REQ-OPS-060 | true | design/operational-readiness.md § REQ-OPS-060 |
| REQ-OPS-061 | true | design/operational-readiness.md § REQ-OPS-061 |
| REQ-OPS-062 | true | design/operational-readiness.md § REQ-OPS-062 |
| REQ-OPS-063 | true | design/operational-readiness.md § REQ-OPS-063 |
| REQ-OPS-064 | true | design/operational-readiness.md § REQ-OPS-064 |
| REQ-OPS-065 | true | design/operational-readiness.md § REQ-OPS-065 |
| REQ-OPS-066 | true | design/operational-readiness.md § REQ-OPS-066 |
| REQ-OPS-067 | false | design/operational-readiness.md § REQ-OPS-067 |
| REQ-OPS-068 | true | design/operational-readiness.md § REQ-OPS-068 |
| REQ-OPS-069 | true | design/operational-readiness.md § REQ-OPS-069 |
| REQ-OPS-070 | false | design/operational-readiness.md § REQ-OPS-070 |
| REQ-OPS-071 | false | design/operational-readiness.md § REQ-OPS-071 |
| REQ-OPS-072 | true | design/operational-readiness.md § REQ-OPS-072 |
| REQ-OPS-073 | false | design/operational-readiness.md § REQ-OPS-073 |
| REQ-OPS-074 | false | design/operational-readiness.md § REQ-OPS-074 |
| REQ-OPS-075 | true | design/operational-readiness.md § REQ-OPS-075 |
| REQ-OPS-076 | false | design/operational-readiness.md § REQ-OPS-076 |
| REQ-OPS-077 | true | design/operational-readiness.md § REQ-OPS-077 |
| REQ-OPS-078 | false | design/operational-readiness.md § REQ-OPS-078 |
| REQ-OPS-079 | true | design/operational-readiness.md § REQ-OPS-079 |
| REQ-OPS-080 | true | design/operational-readiness.md § REQ-OPS-080 |
| REQ-OPS-081 | true | design/operational-readiness.md § REQ-OPS-081 |
| REQ-OPS-082 | false | design/operational-readiness.md § REQ-OPS-082 |
| REQ-OPS-083 | true | design/operational-readiness.md § REQ-OPS-083 |
| REQ-OPS-084 | false | design/operational-readiness.md § REQ-OPS-084 |
| REQ-OPS-085 | true | design/operational-readiness.md § REQ-OPS-085 |
| REQ-OPS-086 | true | design/operational-readiness.md § REQ-OPS-086 |
| REQ-OPS-087 | false | design/operational-readiness.md § REQ-OPS-087 |
| REQ-OPS-088 | true | design/operational-readiness.md § REQ-OPS-088 |
| REQ-OPS-089 | false | design/operational-readiness.md § REQ-OPS-089 |
| REQ-OPS-090 | true | design/operational-readiness.md § REQ-OPS-090 |
| REQ-OPS-091 | false | design/operational-readiness.md § REQ-OPS-091 |
| REQ-OPS-092 | true | design/operational-readiness.md § REQ-OPS-092 |
| REQ-OPS-093 | true | design/operational-readiness.md § REQ-OPS-093 |
| REQ-OPS-094 | false | design/operational-readiness.md § REQ-OPS-094 |
| REQ-OPS-095 | false | design/operational-readiness.md § REQ-OPS-095 |

---

## Notes and findings (for the synthesis child)

1. **Methodology-loader limitation (run-wide).** The Phase-B `design` methodology loader was
   unavailable (`agent_domain_unset`), as every sibling gate observed. This slice was produced on the
   principal-product-designer posture and the relayed Release-Definition guidance, reached by prose.
   The limitation did not block the extraction (a mechanical read of two consolidated registers).

2. **Every `release_gating` field is present and well-formed.** All 73 `REQ-ID-*` and all 75
   `REQ-OPS-*` register entries carry a `- **release_gating**:` field whose value is `true` or
   `false`. None is absent or malformed; nothing was guessed. (Non-gating entries carry an inline
   rationale after the boolean in the design file; the boolean is the column value recorded here.)

3. **Count vs. estimate.** Actuals are `REQ-ID-*` = 73 and `REQ-OPS-*` = 75, against the hub/brief
   estimate of ~110 and ~109. The gap is id-range allocation with intentional gaps, not missing
   requirements:
   - `REQ-ID-*` blocks: accounts/lifecycle 001–024 (025–029 unused), auth/sessions 030–051 (049,
     052–059 unused), authorization 060–074 (075–079 unused), abuse/privacy 080–090 (091–099
     unused), threat-driven 100–101.
   - `REQ-OPS-*` blocks: durable data 001–016, backups/recovery 020–033, limits 040–048,
     observability 060–079, status/incident 080–095 (ranges allocated with gaps between blocks).

4. **Range-endpoint ids are notation, not requirements.** `identity-security.md` section headings
   name block ranges — e.g. `Accounts and lifecycle (REQ-ID-001 .. REQ-ID-029)`, `Threat model
   (REQ-ID-100 .. REQ-ID-119)`. The upper bounds `REQ-ID-029/059/079/099/119` are range notation
   with no defining entry; correctly, no row is emitted for them. `REQ-OPS-*` has no
   referenced-but-undefined id.

5. **Authoritative source = the consolidated register.** `operational-readiness.md` presents each
   `REQ-OPS-*` twice: under per-surface sections (`##### REQ-OPS-NNN` within `durable_data`,
   `backups_and_recovery`, `limits_and_quotas`, `observability`, `status_and_incident`) and in the
   consolidated `## requirements_and_acceptance_criteria` register (`#### REQ-OPS-NNN`). This slice
   reads the consolidated register, which the file's own preamble states holds 75 requirements with
   59 release-gating — matching the extracted counts. The two presentations agreed on the gating
   tally; the synthesis child should treat the consolidated register as canonical if it ever needs
   to re-derive. `identity-security.md` has a single consolidated register.

6. **`design_doc_ref` uses the committed repo path.** The paths are `design/identity-security.md`
   and `design/operational-readiness.md` from the inherited `design_artifact_map.yaml` — the
   repository artifacts assembled by the design PR, not the location where the taskflow produced the
   source. (For awareness: the artifact map lists the operational-readiness `produced_at` as a single
   file, whereas the operational area decomposed and its synthesis child produced the file; this does
   not affect `design_doc_ref`, which names the committed repo path.)
