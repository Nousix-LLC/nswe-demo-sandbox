# SUBTASK_backlog_pr — backlog/PR trace map + four identity verdicts

This spoke owns two columns of the whole-DAG traceability matrix — `epic` and `issue_numbers`, expressed
as the `REQ/BAR → (epic, issue_numbers)` map (Part A) — and four of the eight inherited identities
(Part B): `ISSUE_TRACES`, `GAP_HAS_ISSUE` (design/backlog half), `GITHUB_HYGIENE`, and
`ONE_OWNER_PER_FILE`. It does not build the design-side skeleton columns or the `REQ → bar_ids` map
(sibling spokes own those), and it does not exercise the live product (the live-measurement sibling owns
`live_status`).

**Sources (all completed, read-only):** the delivery backlog (epic index §2, wave graph §3, issue trace
map §4, reconciliation §5, completeness/gap analysis §6) and the design-PR record for
`Nousix-LLC/nswe-demo#122`. Contracts composed against, not redefined: the DAG-root identity statements
and `id_and_traceability_schema.yaml`; `design_artifact_map.yaml` (file-owner map); the gate and subtree
sub-contracts (column/identity ownership). Ids are used verbatim; no id scheme, column set, or identity
statement is restated or altered here.

**Method / limitation.** The `design` methodology loader was unavailable for this reconstructed node
(`agent_domain_unset`); this task is fully specified by the brief, the subtree hub, and the inherited
contracts, so it proceeded on the principal-product-designer posture and the relayed Release Definition
guidance by prose, with the limitation recorded here. The Part-A map is the mechanical inversion of the
backlog §4 trace map (area prefix carried across each slash group, e.g. `REQ-DOM-040/101` →
`REQ-DOM-040`, `REQ-DOM-101`; one issue sits under exactly one epic, so each issue contributes its single
epic to every id it cites). The inversion is reproducible from §4 by a cold reviewer.

---

## Part A — `REQ/BAR → (epic, issue_numbers)` map (for the synthesis join)

### A.1 What this map is

For every `REQ-*` and `BAR-*` that the backlog §4 trace map cites, the map records the epic(s) and
issue number(s) under which it is tracked. The synthesis child (`SUBTASK_assemble`) joins the
`epic`/`issue_numbers` columns onto each matrix row by `req_id` from the REQ table (A.2); the BAR table
(A.3) carries the same relation for each `BAR-*` so the fold can cross-reference by `bar_id`. An id may
appear under more than one epic/issue when distinct issues legitimately cite it (16 `REQ-*` and 19
`BAR-*` do; see A.4) — all occurrences are listed.

Only ids the backlog traces appear here. A release-gating `REQ-*` that no issue cites would not appear in
this map; surfacing such a `REQ-*` as a coverage gap is the join's job in `SUBTASK_assemble`
(`BAR_COVERS_GATING_REQS` / `SKELETON_COMPLETE`), not this spoke's — this spoke reports only what the
backlog trace contains.

### A.2 `REQ-* → (epic, issue_numbers)`

| REQ | Epic(s) | Issue(s) |
|-----|---------|----------|
| REQ-DOM-009 | #77 | #79 |
| REQ-DOM-017 | #34 | #39 |
| REQ-DOM-022 | #34 | #39 |
| REQ-DOM-023 | #34 | #39 |
| REQ-DOM-024 | #34 | #39 |
| REQ-DOM-025 | #34 | #37 |
| REQ-DOM-026 | #34 | #37 |
| REQ-DOM-027 | #34 | #37 |
| REQ-DOM-028 | #34 | #37 |
| REQ-DOM-037 | #77 | #80 |
| REQ-DOM-038 | #77 | #81 |
| REQ-DOM-040 | #56 | #65 |
| REQ-DOM-101 | #56 | #65 |
| REQ-DOM-104 | #56 | #65 |
| REQ-DOM-105 | #56 | #65 |
| REQ-DOM-106 | #83 | #86 |
| REQ-DOM-107 | #56 | #65 |
| REQ-DOM-111 | #56 | #65 |
| REQ-DOM-112 | #77 | #80 |
| REQ-DOM-113 | #56 | #64 |
| REQ-DOM-114 | #56 | #64, #66 |
| REQ-DOM-115 | #90 | #93 |
| REQ-DOM-116 | #56 | #67 |
| REQ-DOM-117 | #56, #77 | #67, #81 |
| REQ-DOM-118 | #44, #56 | #51, #66 |
| REQ-DOM-200 | #89 | #91 |
| REQ-DOM-201 | #89 | #91 |
| REQ-DOM-202 | #89 | #91 |
| REQ-DOM-203 | #43 | #46 |
| REQ-DOM-204 | #56 | #66 |
| REQ-DOM-205 | #89 | #91 |
| REQ-DOM-207 | #43 | #46 |
| REQ-DOM-215 | #89 | #91 |
| REQ-DOM-216 | #89 | #91 |
| REQ-DOM-217 | #89 | #91 |
| REQ-DOM-219 | #43 | #47 |
| REQ-DOM-221 | #89 | #91 |
| REQ-DOM-222 | #89 | #91 |
| REQ-DOM-223 | #56 | #66 |
| REQ-DOM-224 | #89 | #91 |
| REQ-DOM-225 | #89 | #91 |
| REQ-DOM-226 | #90 | #93 |
| REQ-DOM-227 | #89 | #92 |
| REQ-ID-002 | #83 | #84 |
| REQ-ID-003 | #83 | #84 |
| REQ-ID-004 | #83 | #84 |
| REQ-ID-005 | #83 | #84 |
| REQ-ID-007 | #77 | #79 |
| REQ-ID-008 | #77 | #82 |
| REQ-ID-013 | #77 | #78 |
| REQ-ID-014 | #77 | #78 |
| REQ-ID-015 | #77 | #78 |
| REQ-ID-016 | #77 | #78 |
| REQ-ID-017 | #52, #77 | #59, #81 |
| REQ-ID-018 | #52, #77 | #59, #81 |
| REQ-ID-019 | #77 | #81 |
| REQ-ID-020 | #52, #77 | #59, #80 |
| REQ-ID-021 | #52, #77 | #57, #80 |
| REQ-ID-022 | #77 | #80 |
| REQ-ID-023 | #52, #77 | #59, #80 |
| REQ-ID-030 | #83 | #85 |
| REQ-ID-031 | #83 | #85 |
| REQ-ID-032 | #83 | #85 |
| REQ-ID-033 | #83 | #85 |
| REQ-ID-036 | #43 | #47 |
| REQ-ID-037 | #83 | #86 |
| REQ-ID-038 | #83 | #86 |
| REQ-ID-039 | #83 | #87 |
| REQ-ID-040 | #83 | #86 |
| REQ-ID-041 | #83 | #86 |
| REQ-ID-042 | #83 | #86 |
| REQ-ID-043 | #83 | #88 |
| REQ-ID-044 | #83 | #86 |
| REQ-ID-045 | #83 | #86 |
| REQ-ID-046 | #83 | #88 |
| REQ-ID-060 | #43 | #46 |
| REQ-ID-061 | #43 | #46 |
| REQ-ID-062 | #43 | #46 |
| REQ-ID-063 | #43 | #46 |
| REQ-ID-064 | #43 | #45 |
| REQ-ID-065 | #43 | #45 |
| REQ-ID-066 | #43 | #45 |
| REQ-ID-067 | #43 | #45 |
| REQ-ID-068 | #43 | #45 |
| REQ-ID-069 | #43 | #46 |
| REQ-ID-070 | #72 | #75 |
| REQ-ID-071 | #72 | #75 |
| REQ-ID-072 | #72 | #75 |
| REQ-ID-073 | #72 | #76 |
| REQ-ID-074 | #52, #72 | #57, #76 |
| REQ-ID-080 | #52 | #54 |
| REQ-ID-081 | #52 | #54 |
| REQ-ID-082 | #52 | #54 |
| REQ-ID-083 | #52 | #55 |
| REQ-ID-084 | #52 | #55 |
| REQ-ID-085 | #72 | #73 |
| REQ-ID-086 | #52 | #58 |
| REQ-ID-090 | #52 | #58, #59 |
| REQ-ID-100 | #43 | #47 |
| REQ-ID-101 | #72 | #73 |
| REQ-OPS-001 | #56 | #64 |
| REQ-OPS-002 | #56 | #64 |
| REQ-OPS-003 | #56 | #64 |
| REQ-OPS-004 | #44, #56 | #51, #66 |
| REQ-OPS-006 | #56 | #65 |
| REQ-OPS-008 | #56 | #65 |
| REQ-OPS-009 | #56 | #64 |
| REQ-OPS-010 | #56 | #67 |
| REQ-OPS-011 | #56, #77 | #67, #80 |
| REQ-OPS-012 | #56 | #67 |
| REQ-OPS-013 | #56, #77 | #67, #81 |
| REQ-OPS-014 | #83 | #86 |
| REQ-OPS-016 | #52, #56 | #58, #67 |
| REQ-OPS-020 | #44 | #48 |
| REQ-OPS-021 | #44 | #48 |
| REQ-OPS-022 | #44 | #51 |
| REQ-OPS-023 | #44 | #48 |
| REQ-OPS-024 | #44 | #49 |
| REQ-OPS-025 | #44 | #49 |
| REQ-OPS-026 | #44 | #49 |
| REQ-OPS-027 | #44 | #49 |
| REQ-OPS-028 | #44 | #49 |
| REQ-OPS-029 | #44 | #50 |
| REQ-OPS-030 | #44 | #50 |
| REQ-OPS-031 | #44 | #49 |
| REQ-OPS-032 | #44 | #48 |
| REQ-OPS-033 | #44 | #49 |
| REQ-OPS-040 | #72 | #73 |
| REQ-OPS-041 | #72 | #73 |
| REQ-OPS-042 | #72 | #73 |
| REQ-OPS-043 | #72 | #74 |
| REQ-OPS-044 | #72 | #74 |
| REQ-OPS-046 | #72 | #73 |
| REQ-OPS-047 | #72 | #73 |
| REQ-OPS-060 | #90 | #93 |
| REQ-OPS-061 | #90 | #93 |
| REQ-OPS-062 | #90 | #93 |
| REQ-OPS-063 | #90 | #93 |
| REQ-OPS-064 | #90 | #93 |
| REQ-OPS-065 | #90 | #93 |
| REQ-OPS-066 | #90 | #94 |
| REQ-OPS-068 | #90 | #94 |
| REQ-OPS-069 | #90 | #94 |
| REQ-OPS-072 | #90 | #97 |
| REQ-OPS-075 | #90 | #97 |
| REQ-OPS-077 | #72 | #76 |
| REQ-OPS-079 | #90 | #94 |
| REQ-OPS-080 | #90 | #98 |
| REQ-OPS-081 | #90 | #96, #98 |
| REQ-OPS-083 | #90 | #96 |
| REQ-OPS-085 | #90 | #124 |
| REQ-OPS-086 | #90 | #124 |
| REQ-OPS-088 | #90 | #124 |
| REQ-OPS-090 | #90 | #95 |
| REQ-OPS-092 | #90 | #124 |
| REQ-OPS-093 | #90 | #124 |
| REQ-PROD-001 | #34 | #36 |
| REQ-PROD-002 | #34 | #37 |
| REQ-PROD-005 | #34 | #39 |
| REQ-PROD-006 | #34 | #39 |
| REQ-PROD-007 | #34 | #35, #38 |
| REQ-PROD-008 | #83 | #84 |
| REQ-PROD-009 | #83 | #84 |
| REQ-PROD-010 | #83 | #85 |
| REQ-PROD-011 | #83 | #85 |
| REQ-PROD-012 | #77 | #78 |
| REQ-PROD-013 | #77 | #78 |
| REQ-PROD-014 | #83 | #87 |
| REQ-PROD-016 | #77 | #79 |
| REQ-PROD-017 | #77 | #82 |
| REQ-PROD-019 | #77 | #81 |
| REQ-PROD-020 | #77 | #80 |
| REQ-PROD-021 | #77 | #80 |
| REQ-PROD-022 | #77 | #80 |
| REQ-PROD-023 | #43 | #45 |
| REQ-PROD-024 | #43 | #47 |
| REQ-PROD-025 | #52 | #54 |
| REQ-PROD-026 | #52 | #54 |
| REQ-PROD-028 | #72 | #75 |
| REQ-PROD-030 | #34 | #35 |
| REQ-PROD-031 | #34 | #35 |
| REQ-PROD-032 | #34 | #123 |
| REQ-PROD-033 | #34 | #41 |
| REQ-PROD-034 | #34, #90 | #41, #95 |
| REQ-PROD-035 | #53 | #62 |
| REQ-PROD-036 | #53 | #68 |
| REQ-PROD-037 | #56 | #64 |
| REQ-PROD-039 | #90 | #93 |
| REQ-PROD-040 | #90 | #124 |
| REQ-PROD-041 | #72 | #73 |
| REQ-UX-001 | #34 | #35 |
| REQ-UX-002 | #34 | #42 |
| REQ-UX-003 | #34 | #42 |
| REQ-UX-005 | #34 | #42 |
| REQ-UX-012 | #34 | #41 |
| REQ-UX-013 | #34 | #36 |
| REQ-UX-020 | #53 | #60 |
| REQ-UX-021 | #53 | #60 |
| REQ-UX-022 | #53 | #60, #70 |
| REQ-UX-025 | #53 | #68 |
| REQ-UX-026 | #53 | #60 |
| REQ-UX-027 | #53 | #61 |
| REQ-UX-028 | #53 | #61 |
| REQ-UX-029 | #53 | #61 |
| REQ-UX-031 | #34 | #40 |
| REQ-UX-032 | #53 | #60 |
| REQ-UX-033 | #34, #53 | #40, #61 |
| REQ-UX-034 | #53 | #61 |
| REQ-UX-036 | #34 | #40 |
| REQ-UX-039 | #34 | #41 |
| REQ-UX-040 | #34 | #35 |
| REQ-UX-041 | #83 | #84 |
| REQ-UX-042 | #83 | #84 |
| REQ-UX-043 | #83 | #84 |
| REQ-UX-044 | #83 | #85 |
| REQ-UX-045 | #83 | #85 |
| REQ-UX-046 | #77 | #78 |
| REQ-UX-047 | #77 | #78 |
| REQ-UX-048 | #83 | #87 |
| REQ-UX-051 | #34 | #37 |
| REQ-UX-052 | #34 | #37 |
| REQ-UX-053 | #34 | #37 |
| REQ-UX-054 | #34 | #36 |
| REQ-UX-055 | #34 | #36 |
| REQ-UX-056 | #34 | #36 |
| REQ-UX-059 | #34 | #39 |
| REQ-UX-060 | #34 | #39 |
| REQ-UX-061 | #34 | #38 |
| REQ-UX-062 | #34 | #38 |
| REQ-UX-063 | #34 | #38 |
| REQ-UX-065 | #34 | #123 |
| REQ-UX-066 | #34 | #123 |
| REQ-UX-067 | #77 | #79 |
| REQ-UX-068 | #77 | #79 |
| REQ-UX-069 | #77 | #82 |
| REQ-UX-075 | #77 | #81 |
| REQ-UX-076 | #77 | #80 |
| REQ-UX-077 | #77 | #80 |
| REQ-UX-079 | #52 | #54 |
| REQ-UX-082 | #72 | #75 |
| REQ-UX-083 | #52 | #58 |
| REQ-UX-084 | #34 | #35 |
| REQ-UX-085 | #34 | #40 |
| REQ-UX-086 | #34 | #40 |
| REQ-UX-087 | #34 | #40 |
| REQ-UX-088 | #34 | #40 |
| REQ-UX-089 | #34 | #41 |
| REQ-UX-090 | #53 | #62 |
| REQ-UX-091 | #53 | #62 |
| REQ-UX-092 | #34, #53 | #42, #62 |
| REQ-UX-093 | #34, #53 | #42, #63 |
| REQ-UX-094 | #53 | #63 |
| REQ-UX-095 | #53 | #62 |
| REQ-UX-096 | #53 | #63 |
| REQ-UX-097 | #53 | #63 |
| REQ-UX-098 | #53 | #62 |
| REQ-UX-099 | #53 | #62 |
| REQ-UX-100 | #53 | #71 |
| REQ-UX-101 | #53 | #68 |
| REQ-UX-102 | #53 | #68 |
| REQ-UX-103 | #53 | #68 |
| REQ-UX-104 | #53 | #68 |
| REQ-UX-106 | #53 | #69 |
| REQ-UX-107 | #53 | #69 |
| REQ-UX-108 | #53 | #69 |
| REQ-UX-109 | #53 | #69 |
| REQ-UX-110 | #53 | #69 |
| REQ-UX-111 | #53 | #70 |
| REQ-UX-112 | #53 | #63 |
| REQ-UX-113 | #53 | #70 |
| REQ-UX-114 | #53 | #70 |
| REQ-UX-115 | #53 | #69 |
| REQ-UX-116 | #53 | #69 |
| REQ-UX-117 | #53 | #69 |
| REQ-UX-118 | #53 | #71 |
| REQ-UX-119 | #53 | #71 |

### A.3 `BAR-* → (epic, issue_numbers)`

| BAR | Epic(s) | Issue(s) |
|-----|---------|----------|
| BAR-001 | #34 | #36 |
| BAR-002 | #34 | #37 |
| BAR-004 | #34 | #39 |
| BAR-005 | #34 | #39 |
| BAR-006 | #34 | #35, #38 |
| BAR-007 | #83 | #84 |
| BAR-008 | #83 | #84 |
| BAR-009 | #83 | #85 |
| BAR-010 | #83 | #85 |
| BAR-011 | #43 | #45 |
| BAR-012 | #43 | #47 |
| BAR-013 | #56 | #64 |
| BAR-014 | #77 | #78 |
| BAR-015 | #77 | #78 |
| BAR-016 | #83 | #87 |
| BAR-017 | #77 | #79 |
| BAR-018 | #77 | #82 |
| BAR-019 | #77 | #81 |
| BAR-020 | #77 | #80 |
| BAR-021 | #77 | #80 |
| BAR-022 | #77 | #80 |
| BAR-023 | #52 | #54 |
| BAR-024 | #52 | #58 |
| BAR-025 | #72 | #75 |
| BAR-026 | #34 | #35 |
| BAR-027 | #34 | #123 |
| BAR-028 | #34 | #40 |
| BAR-029 | #90 | #95 |
| BAR-030 | #53 | #62 |
| BAR-031 | #53 | #68 |
| BAR-033 | #90 | #93 |
| BAR-034 | #90 | #124 |
| BAR-035 | #72 | #73 |
| BAR-103 | #56 | #65 |
| BAR-105 | #77 | #79 |
| BAR-109 | #56 | #65 |
| BAR-110 | #34, #56 | #39, #65 |
| BAR-112 | #83 | #86 |
| BAR-113 | #83 | #86, #87 |
| BAR-118 | #77 | #80 |
| BAR-119 | #77 | #81 |
| BAR-120 | #56 | #65 |
| BAR-130 | #56 | #64 |
| BAR-131 | #56 | #65 |
| BAR-134 | #56 | #65 |
| BAR-135 | #56 | #65 |
| BAR-136 | #83 | #86 |
| BAR-137 | #56 | #65 |
| BAR-141 | #56 | #65 |
| BAR-142 | #77 | #80 |
| BAR-143 | #56 | #64 |
| BAR-144 | #56 | #64, #66 |
| BAR-145 | #90 | #93 |
| BAR-146 | #56 | #67 |
| BAR-147 | #56, #77 | #67, #81 |
| BAR-148 | #44, #56 | #51, #66 |
| BAR-160 | #89 | #91 |
| BAR-161 | #89 | #91 |
| BAR-162 | #89 | #91 |
| BAR-163 | #43 | #46 |
| BAR-164 | #43 | #46 |
| BAR-165 | #56 | #66 |
| BAR-166 | #89 | #91 |
| BAR-168 | #89 | #91 |
| BAR-169 | #89 | #91 |
| BAR-171 | #34 | #37 |
| BAR-174 | #89 | #91 |
| BAR-175 | #89 | #91 |
| BAR-176 | #89 | #91 |
| BAR-177 | #89 | #91 |
| BAR-178 | #90 | #93 |
| BAR-179 | #89 | #92 |
| BAR-200 | #34 | #35 |
| BAR-201 | #34 | #42 |
| BAR-202 | #34 | #42 |
| BAR-204 | #34 | #42 |
| BAR-205 | #34 | #38 |
| BAR-209 | #34 | #37 |
| BAR-211 | #34 | #40, #41 |
| BAR-212 | #34 | #36, #42 |
| BAR-213 | #34 | #123 |
| BAR-214 | #77 | #82 |
| BAR-215 | #53 | #60 |
| BAR-216 | #53 | #60 |
| BAR-217 | #53 | #60, #70 |
| BAR-218 | #53 | #68 |
| BAR-219 | #53 | #60 |
| BAR-220 | #53 | #61 |
| BAR-221 | #53 | #61 |
| BAR-222 | #53 | #61 |
| BAR-223 | #53 | #60 |
| BAR-224 | #53 | #61 |
| BAR-225 | #34 | #36 |
| BAR-226 | #34 | #40 |
| BAR-229 | #34 | #41 |
| BAR-230 | #34 | #35 |
| BAR-231 | #83 | #84 |
| BAR-232 | #83 | #84 |
| BAR-233 | #83 | #85 |
| BAR-234 | #77 | #78 |
| BAR-235 | #83 | #87 |
| BAR-237 | #34 | #123 |
| BAR-238 | #34 | #37 |
| BAR-239 | #34 | #37 |
| BAR-240 | #34 | #37 |
| BAR-241 | #34 | #36 |
| BAR-242 | #34 | #36 |
| BAR-244 | #34 | #39 |
| BAR-245 | #34 | #39 |
| BAR-246 | #34 | #38 |
| BAR-247 | #34 | #38 |
| BAR-248 | #34 | #123 |
| BAR-249 | #77 | #79 |
| BAR-250 | #77 | #82 |
| BAR-254 | #77 | #81 |
| BAR-255 | #77 | #80 |
| BAR-256 | #52 | #54 |
| BAR-257 | #52 | #58 |
| BAR-258 | #72 | #75 |
| BAR-259 | #34 | #35, #40 |
| BAR-260 | #34 | #40 |
| BAR-261 | #34 | #40 |
| BAR-262 | #34 | #40, #41 |
| BAR-263 | #34 | #41 |
| BAR-265 | #53 | #62 |
| BAR-266 | #53 | #62 |
| BAR-267 | #34, #53 | #42, #62 |
| BAR-268 | #34, #53 | #35, #42, #63 |
| BAR-269 | #53 | #63 |
| BAR-270 | #53 | #62 |
| BAR-271 | #53 | #63 |
| BAR-272 | #53 | #63 |
| BAR-273 | #53 | #62 |
| BAR-274 | #53 | #62 |
| BAR-275 | #53 | #71 |
| BAR-276 | #53 | #68 |
| BAR-277 | #53 | #68 |
| BAR-278 | #53 | #68 |
| BAR-279 | #53 | #68 |
| BAR-280 | #53 | #69 |
| BAR-281 | #53 | #69 |
| BAR-282 | #53 | #69 |
| BAR-283 | #53 | #69 |
| BAR-284 | #53 | #69 |
| BAR-285 | #53 | #70 |
| BAR-286 | #53 | #63 |
| BAR-287 | #53 | #70 |
| BAR-288 | #53 | #70 |
| BAR-289 | #53 | #70 |
| BAR-290 | #53 | #69 |
| BAR-291 | #53 | #69 |
| BAR-292 | #53 | #69 |
| BAR-293 | #53 | #71 |
| BAR-294 | #53 | #71 |
| BAR-300 | #83 | #85 |
| BAR-302 | #43 | #47 |
| BAR-303 | #83 | #84 |
| BAR-304 | #83 | #85 |
| BAR-305 | #83 | #85, #86, #88 |
| BAR-306 | #83 | #86 |
| BAR-307 | #83 | #87 |
| BAR-308 | #83 | #86 |
| BAR-309 | #83 | #88 |
| BAR-310 | #43, #83 | #47, #86 |
| BAR-311 | #43, #83 | #47, #86 |
| BAR-312 | #43 | #46 |
| BAR-313 | #43 | #46 |
| BAR-314 | #43 | #45 |
| BAR-315 | #43 | #45 |
| BAR-316 | #43 | #46 |
| BAR-317 | #77 | #79 |
| BAR-318 | #77 | #82 |
| BAR-321 | #77, #83 | #78, #84 |
| BAR-322 | #77 | #78 |
| BAR-323 | #77 | #78 |
| BAR-324 | #77, #83 | #78, #88 |
| BAR-325 | #52, #77 | #59, #81 |
| BAR-326 | #77 | #81 |
| BAR-327 | #77 | #80 |
| BAR-328 | #52, #77 | #57, #80 |
| BAR-329 | #52, #77 | #59, #80 |
| BAR-330 | #52 | #58, #59 |
| BAR-331 | #72 | #75, #76 |
| BAR-332 | #72 | #75 |
| BAR-333 | #52, #72 | #57, #76 |
| BAR-334 | #52 | #54 |
| BAR-335 | #52, #72 | #54, #76 |
| BAR-336 | #72 | #73 |
| BAR-337 | #72 | #73 |
| BAR-400 | #56 | #64 |
| BAR-401 | #56 | #64 |
| BAR-402 | #56 | #64 |
| BAR-403 | #56 | #65 |
| BAR-404 | #56 | #65 |
| BAR-405 | #44, #56 | #51, #66 |
| BAR-406 | #56 | #67 |
| BAR-407 | #56, #77 | #67, #80 |
| BAR-408 | #56 | #67 |
| BAR-409 | #83 | #86 |
| BAR-411 | #56, #77 | #67, #81 |
| BAR-412 | #52, #56 | #58, #67 |
| BAR-420 | #44 | #48 |
| BAR-421 | #44 | #48 |
| BAR-422 | #44 | #51 |
| BAR-423 | #44 | #48 |
| BAR-424 | #44 | #49 |
| BAR-425 | #44 | #49 |
| BAR-426 | #44 | #49 |
| BAR-427 | #44 | #49 |
| BAR-428 | #44 | #50 |
| BAR-429 | #44 | #50 |
| BAR-430 | #44, #56 | #49, #67 |
| BAR-431 | #44 | #48 |
| BAR-432 | #44 | #49 |
| BAR-440 | #72 | #73 |
| BAR-441 | #72 | #73 |
| BAR-442 | #72 | #73 |
| BAR-443 | #72 | #74 |
| BAR-444 | #72 | #74 |
| BAR-445 | #72 | #73 |
| BAR-460 | #90 | #93 |
| BAR-461 | #90 | #93 |
| BAR-462 | #90 | #93 |
| BAR-463 | #90 | #94 |
| BAR-464 | #90 | #94 |
| BAR-465 | #90 | #94 |
| BAR-466 | #90 | #97 |
| BAR-467 | #90 | #97 |
| BAR-468 | #72 | #76 |
| BAR-480 | #90 | #98 |
| BAR-481 | #90 | #96 |
| BAR-482 | #90 | #124 |
| BAR-483 | #90 | #124 |
| BAR-484 | #90 | #124 |
| BAR-485 | #90 | #95 |
| BAR-486 | #90 | #124 |
| BAR-487 | #90 | #124 |

### A.4 Coverage diagnostics

- **Issues parsed from §4:** 60 rows across the 11 design epics (#56, #89, #83, #34, #43, #77, #72, #53,
  #44, #90, #52). Each issue appears under exactly one epic (no issue number appears twice).
- **Distinct ids mapped:** 276 `REQ-*`, 237 `BAR-*` — exactly the ids the backlog §4 trace cites. This is
  the backlog's trace coverage, not the full requirement set; `REQ-*` that no issue cites are absent by
  construction and are the join's gap check, not this spoke's.
- **Ids tracked under more than one epic (legitimate, all occurrences listed above):** 16 `REQ-*` —
  `REQ-DOM-117`, `REQ-DOM-118`, `REQ-ID-017/018/020/021/023/074`, `REQ-OPS-004/011/013/016`,
  `REQ-PROD-034`, `REQ-UX-033/092/093`; 19 `BAR-*` — `BAR-110/147/148/267/268/310/311/321/324/325/328/329/333/335/405/407/411/412/430`.
  These arise where distinct issues under different epics each enforce or depend on the same requirement
  or bar criterion (e.g. a persistence requirement cited by both the persistence epic #56 and the
  account-deletion/export issues under #77); the join carries every (epic, issue) pair.

---

## Part B — Identity verdicts

Each verdict names what was checked and what was found, so a cold reviewer could re-run it against the
same inputs and reach the same result. A failing or partial result is stated with what is missing and
whether it is fixable; nothing is silently reconciled.

### B.1 `ISSUE_TRACES` — **PASS** (for the design-requirement issue set; one scoped exception recorded)

*Statement asserted (verbatim):* "Every filed issue's acceptance criteria cite ≥1 REQ-* or BAR-*; every
issue sits under exactly one epic; each epic is one coherent landable code goal with stated dependencies."

**Checked, clause by clause, over the backlog §4 trace map (60 issue rows):**

1. **Citation (≥1 REQ-* or BAR-*).** 56 of the 60 rows cite ≥1 `REQ-*`, and every gating design-requirement
   issue also routes to ≥1 `BAR-*` through §4 (the A.2/A.3 map is the inversion). Issue **#55** (Block an
   account) cites `REQ-ID-083/084` and so meets the ≥1-`REQ` clause; it carries no `BAR-*` because it is
   designed-but-deferred / non-gating (recorded in backlog §6). **Exception:** the four folded follow-ups
   **#23, #24, #25, #27** (under EPIC #89) cite neither a `REQ-*` nor a `BAR-*`. These are pre-existing
   infrastructure / repository-hygiene follow-ups adopted from the board (the schema's
   `existing_open_followups`), explicitly non-gating, folded under #89 and tracing to
   `operational-readiness.md`'s `existing_followups` section rather than to a requirement.
2. **Exactly one epic per issue.** Verified mechanically: the 60 issue numbers each appear under exactly
   one `### EPIC` heading in §4; none appears under two. (An individual `REQ-*`/`BAR-*` may be cited by
   issues under different epics — see A.4 — but that is id-reuse, not an issue belonging to two epics.)
3. **Each epic one coherent landable goal with stated dependencies.** Backlog §2 gives each of the 11
   epics a single title (one landable code goal) and an explicit `Depends on (epics)` column (the wave-0
   roots #56 and #89 depend on none); §3's wave graph is stated acyclic, and the dependency edges there
   agree with §2.

**Verdict.** PASS for the design-requirement issue set (clauses 2 and 3 hold for all 60 issues; clause 1
holds for every requirement-bearing issue, 56 of 60). The sole shortfall against a literal "every filed
issue" reading is the four non-gating folded follow-ups #23/#24/#25/#27, which carry no REQ/BAR citation
by their nature as adopted board follow-ups. **Fixability: trivial and non-gating** — either tag these
four as repository-hygiene / non-requirement items explicitly out of the trace obligation, or add the
`REQ-OPS` / `existing_followups` anchor they map to; neither touches the release bar. Surfaced here for
`SUBTASK_assemble` to rule on whether the four folded follow-ups are in the identity's scope.

### B.2 `GAP_HAS_ISSUE` (design/backlog half) — **PASS**; live-measurement half **deferred (out of scope)**

*Statement asserted (verbatim):* "Every gap found in the live-product measurement maps to ≥1 filed
issue/epic." This spoke asserts only the **design/backlog half**: every gap the backlog itself records or
claims maps to ≥1 filed issue/epic.

**Checked (backlog §6, completeness-and-gap analysis).** §6 records exactly two gaps of the current design
against its own surface sweep, and both are filed:

| Gap recorded in §6 | Filed as | Epic | Traces to (per §4) |
|--------------------|----------|------|--------------------|
| Onboarding (post-sign-up first run) | **#123** | #34 | `REQ-PROD-032`, `REQ-UX-065/066`; `BAR-027/213/237/248` |
| Status / availability surface | **#124** | #90 | `REQ-PROD-040`, `REQ-OPS-085/086/088/092/093`; `BAR-034/482/483/484/486/487` |

Both filed gaps sit under exactly one epic and carry a REQ and BAR trace (consistent with A.2/A.3). The
remaining §6 rows are either covered surfaces (each named with its covering issue) or recorded
out-of-scope-with-reason (Notifications and Discovery: deferred non-gating; Billing: out of scope for this
product kind — no tenancy/billing; Block/mute: designed-but-deferred, with issue #55 on the board). None of
those is an un-filed gap.

**Verdict.** PASS for the design/backlog half: both gaps the backlog records are filed issues under one
epic with a REQ/BAR trace. **Explicitly deferred:** the live-measurement half — gaps found by exercising
the live product (at `c805525`) and mapping each to an issue/epic — is owned by the sibling
`SUBTASK_live_measurement` and is **not** evaluated here. The full `GAP_HAS_ISSUE` verdict is the join's to
complete once the live-measurement gaps are known.

### B.3 `GITHUB_HYGIENE` — **PASS** (on the recorded artifacts and the owning tasks' attestations)

*Statement asserted (verbatim):* "Nothing posted to GitHub contains host/system/taskflow detail or an
attribution trailer." Scope of the GitHub-posted artifacts for this spoke: PR `#122`'s body and commit
message (per the design-PR record), and the filed epics/issues plus the single consolidated re-anchoring
index posted to parent epic **#2** (per the backlog §5).

**Checked.**

1. **PR #122 body and commit (design-PR record).** The record attests the PR body "carries no
   host/system/taskflow detail and no attribution trailer (re-scanned clean)" and the commit message
   "carries no attribution trailer." The PR is named only by repository identity: `Nousix-LLC/nswe-demo#122`,
   the public pull URL, base/head branch names (`main` ← `work/design-chirp-r1`), and commit SHAs
   (`b4b65f1`, branched at `276138f`).
2. **Filed epics/issues and the #2 index comment (backlog §5, §7).** The backlog attests these name things
   by repository identity only — `owner/repo#N`, repo-relative `design/<file>.md`, `REQ/BAR/EPIC`/issue
   ids, PR `#122`, commit `c805525` — with no host, cluster, filesystem, taskflow, or run detail and no
   attribution trailer.
3. **Own scan of the two records for leaks.** Every identifier that appears in either completed input is a
   repository-identity form (PR/issue/epic number, commit SHA, branch name, repo-relative design path,
   REQ/BAR/EPIC id). Neither record carries an IP or host address, a cluster endpoint, a filesystem or
   workspace path, a DAG/run/agent id, or a `Co-Authored-By` / "Generated with" attribution trailer.

**Verdict.** PASS on the design/backlog-side evidence (the two completed records and the owning tasks'
re-scan attestations). **Limitation:** this is an assertion against the recorded artifacts, not a fresh
re-scan of the live posted text on GitHub — that live verification was not performed (the posted text is
attested clean by the tasks that posted it, and a live re-scan is outside this spoke's completed-inputs,
read-only scope). The only residual is a divergence between the posted text and these records, which is
not observable from the inputs available here.

### B.4 `ONE_OWNER_PER_FILE` — **PASS**

*Statement asserted (verbatim):* "Each design/*.md has exactly one owning task; none unowned, none
double-written." Checked by reconciling PR #122's assembled file map against `design_artifact_map.yaml`
(and the DAG-root manifest's ownership block).

| `design/*.md` | Owner per `design_artifact_map.yaml` | Owner per PR #122 file map | Agree |
|---------------|--------------------------------------|----------------------------|-------|
| `design/README.md` | `SUBTASK_design_pr` | `SUBTASK_design_pr` (authored in the PR task) | ✓ |
| `design/product-requirements.md` | `SUBTASK_product_requirements` | `SUBTASK_product_requirements` | ✓ |
| `design/domain-application-design.md` | `SUBTASK_domain_app_design` | `SUBTASK_domain_app_design` | ✓ |
| `design/experience-design.md` | `SUBTASK_experience_design` | `SUBTASK_experience_design` | ✓ |
| `design/identity-security.md` | `SUBTASK_identity_trust` | `SUBTASK_identity_trust` | ✓ |
| `design/operational-readiness.md` | `SUBTASK_operational_readiness` | `SUBTASK_operational_readiness` | ✓ |
| `design/release-bar.md` | `SUBTASK_release_bar` | `SUBTASK_release_bar` | ✓ |

**Found.** All seven files in the artifact map are present in the PR map, each with exactly one owner, and
the two maps agree on every owner. The PR record states the six concern files were copied byte-identical
from their single owning task's output and `design/README.md` was authored solely in the PR task — so
none is unowned and none is double-written. **One reconciled detail (not a conflict):**
`design/operational-readiness.md`'s *produced-at* source is the operational concern's synthesis-child
output (the operational concern decomposed into its own subtree), rather than the subtree-root `outputs/`
path the artifact map lists; the **owning task is unchanged** (`SUBTASK_operational_readiness`), and the PR
record explains the sub-path. Ownership is single and consistent.

**Verdict.** PASS — one owner per `design/*.md`, PR map and artifact map in agreement, none unowned, none
double-written.

---

## Summary

| Deliverable | Result |
|-------------|--------|
| `REQ/BAR → (epic, issue_numbers)` map | Built from backlog §4 (276 `REQ-*`, 237 `BAR-*`), ids verbatim, keyed for the `req_id` / `bar_id` join |
| `ISSUE_TRACES` | **PASS** (design-requirement issues); scoped exception recorded — 4 non-gating folded follow-ups (#23/#24/#25/#27) cite no REQ/BAR, trivially fixable |
| `GAP_HAS_ISSUE` (design/backlog half) | **PASS** — both recorded gaps filed (#123 under #34; #124 under #90); live-measurement half deferred to the sibling |
| `GITHUB_HYGIENE` | **PASS** on recorded artifacts + attestations; live posted-text re-scan out of scope (noted) |
| `ONE_OWNER_PER_FILE` | **PASS** — 7 `design/*.md`, one owner each, PR map ⟷ artifact map agree |

Scope note: this spoke owns the `epic`/`issue_numbers` columns and these four identities only. The
design-side skeleton columns, the `REQ → bar_ids` map, `CONCERN_COVERAGE`/`SURFACE_COVERAGE`,
`BAR_TESTABLE`, the cross-source `BAR_COVERS_GATING_REQS`, and the live-measurement half of `GAP_HAS_ISSUE`
belong to sibling spokes and the synthesis child. The `design` methodology loader was unavailable
(`agent_domain_unset`); work proceeded on the brief, hub, and inherited contracts, with the limitation
recorded.
