# Traceability-matrix skeleton — design-side columns for `REQ-PROD-*` and `REQ-DOM-*`

This is the design-side slice of the whole-DAG traceability-matrix skeleton for two requirement
areas: product requirements (`REQ-PROD-*`) and domain & application design (`REQ-DOM-*`). It carries
only the three design-side columns this spoke owns — `req_id`, `release_gating`, and `design_doc_ref`
— one row per requirement, keyed by `req_id`, so the synthesis child can join it on `req_id` with the
`bar_ids`, `epic`/`issue_numbers`, and `live_status` slices the other spokes and the sibling produce.

It computes no `bar_ids`, no `epic`, no `issue_numbers`, and asserts no identity — those belong to
other owners per `../contracts/_MANIFEST.yaml`. It is a read-only extraction over two COMPLETED design
files; where a value is anomalous it is flagged here rather than guessed or corrected in place.

## Sources (by repository identity)

Both source files live in the repository `Nousix-LLC/nswe-demo`, grounded at commit `c805525`, and are
assembled into the repo `design/` tree per `design_artifact_map.yaml`:

| Area | Source design file (repo-relative, per `design_artifact_map.yaml`) |
|------|---------------------------------------------------------------------|
| `REQ-PROD-*` | `design/product-requirements.md` |
| `REQ-DOM-*` | `design/domain-application-design.md` |

## Column conventions

- **`req_id`** — the inherited `REQ-<AREA>-<NNN>` identifier, used verbatim from the source heading
  (`id_and_traceability_schema.yaml`). No id is renamed; no row is minted for an id not present in the
  source.
- **`release_gating`** — the verbatim `true`/`false` value of the requirement's own
  `- **release_gating**:` field in the source file. Where the source appends a reason after the value,
  only the boolean is carried here; the reason stays in the design doc.
- **`design_doc_ref`** — the area's repo-relative design path (above) plus the requirement's own
  section, identified by its `#### REQ-<AREA>-<NNN>` heading. Resolution convention:
  open the design file and locate the heading that begins with the `req_id`. Written compactly as
  `<repo-relative path> § <req_id>`.

## Counts (actual, as found)

| Area | Rows found | `release_gating: true` | `release_gating: false` | Hub estimate |
|------|-----------:|-----------------------:|------------------------:|--------------|
| `REQ-PROD-*` | 42 | 35 | 7 | ~42 (matches) |
| `REQ-DOM-*` | 81 | 79 | 2 | ~111 (actual is 81) |
| **Total** | **123** | **114** | **9** | — |

- `REQ-PROD-*`: exactly 42 entries, `REQ-PROD-001`–`REQ-PROD-042`, contiguous.
- `REQ-DOM-*`: exactly 81 entries across the source's three disjoint, intentionally gapped ranges —
  domain model `REQ-DOM-001`–`040` (40), persistence `REQ-DOM-100`–`118` (19), and modules & interfaces
  `REQ-DOM-200`–`208`, `REQ-DOM-215`–`222`, `REQ-DOM-223`–`227` (22). The gaps (`041`–`099`, `119`–`199`,
  `209`–`214`) are unused id space, not missing requirements; the source reserves `001..049 / 100..149 /
  200..249` per range but mints fewer. The hub's "~111" was an order-of-magnitude estimate; the count
  present in `domain-application-design.md` at `c805525` is **81**. No area is missing.
- `release_gating: false` requirements: `REQ-PROD-004, 015, 018, 027, 029, 031, 042`; `REQ-DOM-010, 016`.

## Anomalies

None. Every one of the 123 requirements carries a well-formed `- **release_gating**: true|false` field;
no value is absent, ambiguous, or malformed. Nothing was guessed. (Several `true` values are followed by
an explanatory clause in the source, e.g. `REQ-DOM-100`; the boolean itself is unambiguous in every case.)

---

## `REQ-PROD-*` — design-side skeleton rows

| req_id | release_gating | design_doc_ref |
|--------|----------------|----------------|
| REQ-PROD-001 | true | `design/product-requirements.md` § REQ-PROD-001 |
| REQ-PROD-002 | true | `design/product-requirements.md` § REQ-PROD-002 |
| REQ-PROD-003 | true | `design/product-requirements.md` § REQ-PROD-003 |
| REQ-PROD-004 | false | `design/product-requirements.md` § REQ-PROD-004 |
| REQ-PROD-005 | true | `design/product-requirements.md` § REQ-PROD-005 |
| REQ-PROD-006 | true | `design/product-requirements.md` § REQ-PROD-006 |
| REQ-PROD-007 | true | `design/product-requirements.md` § REQ-PROD-007 |
| REQ-PROD-008 | true | `design/product-requirements.md` § REQ-PROD-008 |
| REQ-PROD-009 | true | `design/product-requirements.md` § REQ-PROD-009 |
| REQ-PROD-010 | true | `design/product-requirements.md` § REQ-PROD-010 |
| REQ-PROD-011 | true | `design/product-requirements.md` § REQ-PROD-011 |
| REQ-PROD-012 | true | `design/product-requirements.md` § REQ-PROD-012 |
| REQ-PROD-013 | true | `design/product-requirements.md` § REQ-PROD-013 |
| REQ-PROD-014 | true | `design/product-requirements.md` § REQ-PROD-014 |
| REQ-PROD-015 | false | `design/product-requirements.md` § REQ-PROD-015 |
| REQ-PROD-016 | true | `design/product-requirements.md` § REQ-PROD-016 |
| REQ-PROD-017 | true | `design/product-requirements.md` § REQ-PROD-017 |
| REQ-PROD-018 | false | `design/product-requirements.md` § REQ-PROD-018 |
| REQ-PROD-019 | true | `design/product-requirements.md` § REQ-PROD-019 |
| REQ-PROD-020 | true | `design/product-requirements.md` § REQ-PROD-020 |
| REQ-PROD-021 | true | `design/product-requirements.md` § REQ-PROD-021 |
| REQ-PROD-022 | true | `design/product-requirements.md` § REQ-PROD-022 |
| REQ-PROD-023 | true | `design/product-requirements.md` § REQ-PROD-023 |
| REQ-PROD-024 | true | `design/product-requirements.md` § REQ-PROD-024 |
| REQ-PROD-025 | true | `design/product-requirements.md` § REQ-PROD-025 |
| REQ-PROD-026 | true | `design/product-requirements.md` § REQ-PROD-026 |
| REQ-PROD-027 | false | `design/product-requirements.md` § REQ-PROD-027 |
| REQ-PROD-028 | true | `design/product-requirements.md` § REQ-PROD-028 |
| REQ-PROD-029 | false | `design/product-requirements.md` § REQ-PROD-029 |
| REQ-PROD-030 | true | `design/product-requirements.md` § REQ-PROD-030 |
| REQ-PROD-031 | false | `design/product-requirements.md` § REQ-PROD-031 |
| REQ-PROD-032 | true | `design/product-requirements.md` § REQ-PROD-032 |
| REQ-PROD-033 | true | `design/product-requirements.md` § REQ-PROD-033 |
| REQ-PROD-034 | true | `design/product-requirements.md` § REQ-PROD-034 |
| REQ-PROD-035 | true | `design/product-requirements.md` § REQ-PROD-035 |
| REQ-PROD-036 | true | `design/product-requirements.md` § REQ-PROD-036 |
| REQ-PROD-037 | true | `design/product-requirements.md` § REQ-PROD-037 |
| REQ-PROD-038 | true | `design/product-requirements.md` § REQ-PROD-038 |
| REQ-PROD-039 | true | `design/product-requirements.md` § REQ-PROD-039 |
| REQ-PROD-040 | true | `design/product-requirements.md` § REQ-PROD-040 |
| REQ-PROD-041 | true | `design/product-requirements.md` § REQ-PROD-041 |
| REQ-PROD-042 | false | `design/product-requirements.md` § REQ-PROD-042 |

---

## `REQ-DOM-*` — design-side skeleton rows

| req_id | release_gating | design_doc_ref |
|--------|----------------|----------------|
| REQ-DOM-001 | true | `design/domain-application-design.md` § REQ-DOM-001 |
| REQ-DOM-002 | true | `design/domain-application-design.md` § REQ-DOM-002 |
| REQ-DOM-003 | true | `design/domain-application-design.md` § REQ-DOM-003 |
| REQ-DOM-004 | true | `design/domain-application-design.md` § REQ-DOM-004 |
| REQ-DOM-005 | true | `design/domain-application-design.md` § REQ-DOM-005 |
| REQ-DOM-006 | true | `design/domain-application-design.md` § REQ-DOM-006 |
| REQ-DOM-007 | true | `design/domain-application-design.md` § REQ-DOM-007 |
| REQ-DOM-008 | true | `design/domain-application-design.md` § REQ-DOM-008 |
| REQ-DOM-009 | true | `design/domain-application-design.md` § REQ-DOM-009 |
| REQ-DOM-010 | false | `design/domain-application-design.md` § REQ-DOM-010 |
| REQ-DOM-011 | true | `design/domain-application-design.md` § REQ-DOM-011 |
| REQ-DOM-012 | true | `design/domain-application-design.md` § REQ-DOM-012 |
| REQ-DOM-013 | true | `design/domain-application-design.md` § REQ-DOM-013 |
| REQ-DOM-014 | true | `design/domain-application-design.md` § REQ-DOM-014 |
| REQ-DOM-015 | true | `design/domain-application-design.md` § REQ-DOM-015 |
| REQ-DOM-016 | false | `design/domain-application-design.md` § REQ-DOM-016 |
| REQ-DOM-017 | true | `design/domain-application-design.md` § REQ-DOM-017 |
| REQ-DOM-018 | true | `design/domain-application-design.md` § REQ-DOM-018 |
| REQ-DOM-019 | true | `design/domain-application-design.md` § REQ-DOM-019 |
| REQ-DOM-020 | true | `design/domain-application-design.md` § REQ-DOM-020 |
| REQ-DOM-021 | true | `design/domain-application-design.md` § REQ-DOM-021 |
| REQ-DOM-022 | true | `design/domain-application-design.md` § REQ-DOM-022 |
| REQ-DOM-023 | true | `design/domain-application-design.md` § REQ-DOM-023 |
| REQ-DOM-024 | true | `design/domain-application-design.md` § REQ-DOM-024 |
| REQ-DOM-025 | true | `design/domain-application-design.md` § REQ-DOM-025 |
| REQ-DOM-026 | true | `design/domain-application-design.md` § REQ-DOM-026 |
| REQ-DOM-027 | true | `design/domain-application-design.md` § REQ-DOM-027 |
| REQ-DOM-028 | true | `design/domain-application-design.md` § REQ-DOM-028 |
| REQ-DOM-029 | true | `design/domain-application-design.md` § REQ-DOM-029 |
| REQ-DOM-030 | true | `design/domain-application-design.md` § REQ-DOM-030 |
| REQ-DOM-031 | true | `design/domain-application-design.md` § REQ-DOM-031 |
| REQ-DOM-032 | true | `design/domain-application-design.md` § REQ-DOM-032 |
| REQ-DOM-033 | true | `design/domain-application-design.md` § REQ-DOM-033 |
| REQ-DOM-034 | true | `design/domain-application-design.md` § REQ-DOM-034 |
| REQ-DOM-035 | true | `design/domain-application-design.md` § REQ-DOM-035 |
| REQ-DOM-036 | true | `design/domain-application-design.md` § REQ-DOM-036 |
| REQ-DOM-037 | true | `design/domain-application-design.md` § REQ-DOM-037 |
| REQ-DOM-038 | true | `design/domain-application-design.md` § REQ-DOM-038 |
| REQ-DOM-039 | true | `design/domain-application-design.md` § REQ-DOM-039 |
| REQ-DOM-040 | true | `design/domain-application-design.md` § REQ-DOM-040 |
| REQ-DOM-100 | true | `design/domain-application-design.md` § REQ-DOM-100 |
| REQ-DOM-101 | true | `design/domain-application-design.md` § REQ-DOM-101 |
| REQ-DOM-102 | true | `design/domain-application-design.md` § REQ-DOM-102 |
| REQ-DOM-103 | true | `design/domain-application-design.md` § REQ-DOM-103 |
| REQ-DOM-104 | true | `design/domain-application-design.md` § REQ-DOM-104 |
| REQ-DOM-105 | true | `design/domain-application-design.md` § REQ-DOM-105 |
| REQ-DOM-106 | true | `design/domain-application-design.md` § REQ-DOM-106 |
| REQ-DOM-107 | true | `design/domain-application-design.md` § REQ-DOM-107 |
| REQ-DOM-108 | true | `design/domain-application-design.md` § REQ-DOM-108 |
| REQ-DOM-109 | true | `design/domain-application-design.md` § REQ-DOM-109 |
| REQ-DOM-110 | true | `design/domain-application-design.md` § REQ-DOM-110 |
| REQ-DOM-111 | true | `design/domain-application-design.md` § REQ-DOM-111 |
| REQ-DOM-112 | true | `design/domain-application-design.md` § REQ-DOM-112 |
| REQ-DOM-113 | true | `design/domain-application-design.md` § REQ-DOM-113 |
| REQ-DOM-114 | true | `design/domain-application-design.md` § REQ-DOM-114 |
| REQ-DOM-115 | true | `design/domain-application-design.md` § REQ-DOM-115 |
| REQ-DOM-116 | true | `design/domain-application-design.md` § REQ-DOM-116 |
| REQ-DOM-117 | true | `design/domain-application-design.md` § REQ-DOM-117 |
| REQ-DOM-118 | true | `design/domain-application-design.md` § REQ-DOM-118 |
| REQ-DOM-200 | true | `design/domain-application-design.md` § REQ-DOM-200 |
| REQ-DOM-201 | true | `design/domain-application-design.md` § REQ-DOM-201 |
| REQ-DOM-202 | true | `design/domain-application-design.md` § REQ-DOM-202 |
| REQ-DOM-203 | true | `design/domain-application-design.md` § REQ-DOM-203 |
| REQ-DOM-204 | true | `design/domain-application-design.md` § REQ-DOM-204 |
| REQ-DOM-205 | true | `design/domain-application-design.md` § REQ-DOM-205 |
| REQ-DOM-206 | true | `design/domain-application-design.md` § REQ-DOM-206 |
| REQ-DOM-207 | true | `design/domain-application-design.md` § REQ-DOM-207 |
| REQ-DOM-208 | true | `design/domain-application-design.md` § REQ-DOM-208 |
| REQ-DOM-215 | true | `design/domain-application-design.md` § REQ-DOM-215 |
| REQ-DOM-216 | true | `design/domain-application-design.md` § REQ-DOM-216 |
| REQ-DOM-217 | true | `design/domain-application-design.md` § REQ-DOM-217 |
| REQ-DOM-218 | true | `design/domain-application-design.md` § REQ-DOM-218 |
| REQ-DOM-219 | true | `design/domain-application-design.md` § REQ-DOM-219 |
| REQ-DOM-220 | true | `design/domain-application-design.md` § REQ-DOM-220 |
| REQ-DOM-221 | true | `design/domain-application-design.md` § REQ-DOM-221 |
| REQ-DOM-222 | true | `design/domain-application-design.md` § REQ-DOM-222 |
| REQ-DOM-223 | true | `design/domain-application-design.md` § REQ-DOM-223 |
| REQ-DOM-224 | true | `design/domain-application-design.md` § REQ-DOM-224 |
| REQ-DOM-225 | true | `design/domain-application-design.md` § REQ-DOM-225 |
| REQ-DOM-226 | true | `design/domain-application-design.md` § REQ-DOM-226 |
| REQ-DOM-227 | true | `design/domain-application-design.md` § REQ-DOM-227 |

---

## For the synthesis join

- Join on `req_id` (verbatim). This slice supplies `release_gating` and `design_doc_ref` for every
  `REQ-PROD-*` and `REQ-DOM-*`; `bar_ids` comes from `SUBTASK_bar_mapping`, `epic`/`issue_numbers` from
  `SUBTASK_backlog_pr`, and `live_status` from the sibling `SUBTASK_live_measurement` (attached by the
  fold).
- Release-gating rows this slice contributes for the `BAR_COVERS_GATING_REQS` assertion:
  35 `REQ-PROD-*` (all except `004, 015, 018, 027, 029, 031, 042`) and 79 `REQ-DOM-*`
  (all except `010, 016`).
- No identity is asserted here; no `bar_ids`/`epic`/`issue_numbers` are computed here.

## Methodology limitation (recorded, per the subtree hub)

The `design` methodology loader was unavailable run-wide (`agent_domain_unset`); this extraction applied
the principal-product-designer posture by prose and did not block on the loader. The task is a mechanical,
verbatim extraction over two COMPLETED design files, so the limitation does not affect the result: every
`req_id`, `release_gating` value, and `design_doc_ref` is taken directly from the source text.
