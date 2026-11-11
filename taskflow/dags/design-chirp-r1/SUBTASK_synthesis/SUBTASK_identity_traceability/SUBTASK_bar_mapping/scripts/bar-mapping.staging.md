# chirp — BAR→REQ mapping, `REQ → bar_ids`, and the `BAR_TESTABLE` identity

This maps each release-bar criterion (`BAR-*`) to the requirements (`REQ-*`) it enforces, inverts that into the `REQ → bar_ids` map the traceability matrix needs, and records a `PASS`/`FAIL` verdict for the `BAR_TESTABLE` identity with the evidence behind it. It reads the release bar for `Nousix-LLC/nswe-demo` (`design/release-bar.md`, measured at commit `c805525`) and nothing else; it does not touch the design docs, the backlog, the live product, or the bar itself. A finding is reported here, not fixed in place.

The `verification_method` and `stage` values are checked against the inherited schema (`design/`-level `id_and_traceability_schema.yaml`): the closed verification vocabulary is `manual_user_check`, `automated_test`, `inspection`, `operational_check`, and the stage is one of `usable_early` or `releasable`. A value outside those is reported as a `BAR_TESTABLE` failure, not normalised to the nearest legal value.

**Note on the methodology surface.** The `design` methodology loader was unavailable for this run (`agent_domain_unset`); this spoke proceeded under the principal-product-designer persona and the relayed release-definition guidance, as the subtree hub directs. The limitation changes nothing mechanical here: the mapping and the identity are read straight from the bar and the inherited schema.

## Summary

- **`BAR-*` criteria found: 278.** (The bar's own area table totals 278; the subtree hub's working estimate of 279 was one high. The actual count parsed from the register is **278**.)
- **Stage split:** 148 `usable_early`, 130 `releasable`.
- **Distinct `REQ-*` referenced by at least one `BAR-*`: 343.** These are the keys of the `REQ → bar_ids` map below.
- **`BAR_TESTABLE`: PASS.** Every criterion names a verification method from the closed vocabulary and references at least one `REQ-*`; evidence and any offenders are in the verdict section at the end.

**Per-area cross-check** — the parsed stage counts per area, set beside the bar's own published area table. They agree exactly, which is the evidence that every criterion in the register was captured with its stage (no criterion silently dropped or mis-staged).

| Area | `usable_early` | `releasable` | Total |
|------|---------------:|-------------:|------:|
| Product | 14 | 21 | 35 |
| Domain & application | 50 | 10 | 60 |
| Experience | 51 | 43 | 94 |
| Identity, security & trust | 18 | 22 | 40 |
| Operational readiness | 15 | 34 | 49 |
| **All areas** | **148** | **130** | **278** |

**Verification-method distribution** (how the bar says each condition is checked):

| `verification_method` | Count |
|-----------------------|------:|
| `manual_user_check` | 139 |
| `automated_test` | 36 |
| `inspection` | 35 |
| `operational_check` | 68 |

---

## 1. Per-`BAR-*` table

All 278 criteria in id order, each with its stage, verification method, and the `REQ-*` ids it enforces (verbatim from the bar's `_Enforces …_` clause — the authoritative reference, not anything a design file claims about itself). A criterion that enforces several requirements lists them comma-separated.

| `bar_id` | `stage` | `verification_method` | Referenced `REQ-*` |
|----------|---------|-----------------------|--------------------|
| BAR-001 | usable_early | automated_test | REQ-PROD-001 |
| BAR-002 | usable_early | automated_test | REQ-PROD-002 |
| BAR-003 | usable_early | automated_test | REQ-PROD-003 |
| BAR-004 | usable_early | automated_test | REQ-PROD-005 |
| BAR-005 | usable_early | automated_test | REQ-PROD-006 |
| BAR-006 | usable_early | automated_test | REQ-PROD-007 |
| BAR-007 | usable_early | automated_test | REQ-PROD-008 |
| BAR-008 | usable_early | automated_test | REQ-PROD-009 |
| BAR-009 | usable_early | automated_test | REQ-PROD-010 |
| BAR-010 | usable_early | automated_test | REQ-PROD-011 |
| BAR-011 | usable_early | automated_test | REQ-PROD-023 |
| BAR-012 | usable_early | automated_test | REQ-PROD-024 |
| BAR-013 | usable_early | operational_check | REQ-PROD-037 |
| BAR-014 | releasable | manual_user_check | REQ-PROD-012 |
| BAR-015 | releasable | manual_user_check | REQ-PROD-013 |
| BAR-016 | usable_early | automated_test | REQ-PROD-014 |
| BAR-017 | releasable | automated_test | REQ-PROD-016 |
| BAR-018 | releasable | manual_user_check | REQ-PROD-017 |
| BAR-019 | releasable | manual_user_check | REQ-PROD-019 |
| BAR-020 | releasable | automated_test | REQ-PROD-020 |
| BAR-021 | releasable | inspection | REQ-PROD-021 |
| BAR-022 | releasable | manual_user_check | REQ-PROD-022 |
| BAR-023 | releasable | manual_user_check | REQ-PROD-025 |
| BAR-024 | releasable | inspection | REQ-PROD-026 |
| BAR-025 | releasable | manual_user_check | REQ-PROD-028 |
| BAR-026 | releasable | manual_user_check | REQ-PROD-030 |
| BAR-027 | releasable | manual_user_check | REQ-PROD-032 |
| BAR-028 | releasable | manual_user_check | REQ-PROD-033 |
| BAR-029 | releasable | manual_user_check | REQ-PROD-034 |
| BAR-030 | releasable | manual_user_check | REQ-PROD-035 |
| BAR-031 | releasable | manual_user_check | REQ-PROD-036 |
| BAR-032 | releasable | operational_check | REQ-PROD-038 |
| BAR-033 | releasable | operational_check | REQ-PROD-039 |
| BAR-034 | releasable | operational_check | REQ-PROD-040 |
| BAR-035 | releasable | operational_check | REQ-PROD-041 |
| BAR-100 | usable_early | manual_user_check | REQ-DOM-001, REQ-DOM-004, REQ-DOM-005 |
| BAR-101 | usable_early | manual_user_check | REQ-DOM-002, REQ-DOM-003 |
| BAR-102 | usable_early | manual_user_check | REQ-DOM-006 |
| BAR-103 | usable_early | automated_test | REQ-DOM-007 |
| BAR-104 | usable_early | manual_user_check | REQ-DOM-008, REQ-DOM-039 |
| BAR-105 | usable_early | manual_user_check | REQ-DOM-009 |
| BAR-106 | usable_early | manual_user_check | REQ-DOM-011, REQ-DOM-012, REQ-DOM-013, REQ-DOM-014 |
| BAR-107 | usable_early | manual_user_check | REQ-DOM-015 |
| BAR-108 | usable_early | manual_user_check | REQ-DOM-017, REQ-DOM-018, REQ-DOM-019, REQ-DOM-020 |
| BAR-109 | usable_early | manual_user_check | REQ-DOM-021 |
| BAR-110 | usable_early | manual_user_check | REQ-DOM-022, REQ-DOM-023, REQ-DOM-024 |
| BAR-111 | usable_early | manual_user_check | REQ-DOM-025, REQ-DOM-026, REQ-DOM-027, REQ-DOM-028 |
| BAR-112 | usable_early | manual_user_check | REQ-DOM-029, REQ-DOM-032 |
| BAR-113 | usable_early | manual_user_check | REQ-DOM-030, REQ-DOM-031 |
| BAR-114 | usable_early | manual_user_check | REQ-DOM-033 |
| BAR-115 | releasable | manual_user_check | REQ-DOM-034 |
| BAR-116 | usable_early | manual_user_check | REQ-DOM-035 |
| BAR-117 | usable_early | manual_user_check | REQ-DOM-036 |
| BAR-118 | releasable | manual_user_check | REQ-DOM-037 |
| BAR-119 | releasable | manual_user_check | REQ-DOM-038 |
| BAR-120 | usable_early | inspection | REQ-DOM-040 |
| BAR-130 | usable_early | operational_check | REQ-DOM-100 |
| BAR-131 | usable_early | operational_check | REQ-DOM-101 |
| BAR-132 | usable_early | operational_check | REQ-DOM-102 |
| BAR-133 | usable_early | operational_check | REQ-DOM-103 |
| BAR-134 | usable_early | operational_check | REQ-DOM-104 |
| BAR-135 | usable_early | operational_check | REQ-DOM-105 |
| BAR-136 | usable_early | operational_check | REQ-DOM-106 |
| BAR-137 | usable_early | operational_check | REQ-DOM-107 |
| BAR-138 | usable_early | operational_check | REQ-DOM-108 |
| BAR-139 | usable_early | operational_check | REQ-DOM-109 |
| BAR-140 | releasable | operational_check | REQ-DOM-110 |
| BAR-141 | usable_early | operational_check | REQ-DOM-111 |
| BAR-142 | releasable | operational_check | REQ-DOM-112 |
| BAR-143 | usable_early | operational_check | REQ-DOM-113 |
| BAR-144 | usable_early | operational_check | REQ-DOM-114 |
| BAR-145 | usable_early | operational_check | REQ-DOM-115 |
| BAR-146 | releasable | operational_check | REQ-DOM-116 |
| BAR-147 | releasable | operational_check | REQ-DOM-117 |
| BAR-148 | releasable | operational_check | REQ-DOM-118 |
| BAR-160 | usable_early | inspection | REQ-DOM-200, REQ-DOM-208 |
| BAR-161 | usable_early | inspection | REQ-DOM-201 |
| BAR-162 | usable_early | inspection | REQ-DOM-202 |
| BAR-163 | usable_early | manual_user_check | REQ-DOM-203 |
| BAR-164 | usable_early | automated_test | REQ-DOM-207 |
| BAR-165 | usable_early | inspection | REQ-DOM-204, REQ-DOM-223 |
| BAR-166 | usable_early | manual_user_check | REQ-DOM-205 |
| BAR-167 | usable_early | inspection | REQ-DOM-206 |
| BAR-168 | usable_early | inspection | REQ-DOM-215 |
| BAR-169 | usable_early | manual_user_check | REQ-DOM-216 |
| BAR-170 | usable_early | manual_user_check | REQ-DOM-217 |
| BAR-171 | usable_early | manual_user_check | REQ-DOM-218 |
| BAR-172 | usable_early | manual_user_check | REQ-DOM-219 |
| BAR-173 | usable_early | manual_user_check | REQ-DOM-220 |
| BAR-174 | usable_early | inspection | REQ-DOM-221 |
| BAR-175 | releasable | inspection | REQ-DOM-222 |
| BAR-176 | usable_early | manual_user_check | REQ-DOM-224 |
| BAR-177 | usable_early | manual_user_check | REQ-DOM-225 |
| BAR-178 | releasable | operational_check | REQ-DOM-226 |
| BAR-179 | usable_early | inspection | REQ-DOM-227 |
| BAR-200 | usable_early | manual_user_check | REQ-UX-001 |
| BAR-201 | usable_early | manual_user_check | REQ-UX-002 |
| BAR-202 | usable_early | manual_user_check | REQ-UX-003 |
| BAR-203 | releasable | inspection | REQ-UX-004 |
| BAR-204 | usable_early | manual_user_check | REQ-UX-005 |
| BAR-205 | usable_early | automated_test | REQ-UX-006 |
| BAR-206 | releasable | manual_user_check | REQ-UX-007 |
| BAR-207 | releasable | manual_user_check | REQ-UX-008 |
| BAR-208 | releasable | manual_user_check | REQ-UX-009 |
| BAR-209 | usable_early | manual_user_check | REQ-UX-010 |
| BAR-210 | releasable | manual_user_check | REQ-UX-011 |
| BAR-211 | usable_early | manual_user_check | REQ-UX-012 |
| BAR-212 | usable_early | manual_user_check | REQ-UX-013 |
| BAR-213 | usable_early | manual_user_check | REQ-UX-014, REQ-UX-016 |
| BAR-214 | releasable | manual_user_check | REQ-UX-017, REQ-UX-018 |
| BAR-215 | releasable | manual_user_check | REQ-UX-020 |
| BAR-216 | usable_early | manual_user_check | REQ-UX-021 |
| BAR-217 | usable_early | manual_user_check | REQ-UX-022 |
| BAR-218 | usable_early | manual_user_check | REQ-UX-025 |
| BAR-219 | releasable | manual_user_check | REQ-UX-026 |
| BAR-220 | releasable | manual_user_check | REQ-UX-027 |
| BAR-221 | releasable | manual_user_check | REQ-UX-028 |
| BAR-222 | releasable | manual_user_check | REQ-UX-029 |
| BAR-223 | usable_early | manual_user_check | REQ-UX-032 |
| BAR-224 | releasable | manual_user_check | REQ-UX-033, REQ-UX-034 |
| BAR-225 | usable_early | manual_user_check | REQ-UX-035 |
| BAR-226 | usable_early | manual_user_check | REQ-UX-031, REQ-UX-036 |
| BAR-227 | usable_early | manual_user_check | REQ-UX-037 |
| BAR-228 | usable_early | manual_user_check | REQ-UX-038 |
| BAR-229 | usable_early | manual_user_check | REQ-UX-039 |
| BAR-230 | usable_early | manual_user_check | REQ-UX-040, REQ-PROD-030, REQ-PROD-031 |
| BAR-231 | usable_early | manual_user_check | REQ-UX-041, REQ-UX-043, REQ-PROD-008, REQ-PROD-012, REQ-PROD-031 |
| BAR-232 | usable_early | automated_test | REQ-UX-042, REQ-PROD-009 |
| BAR-233 | usable_early | automated_test | REQ-UX-044, REQ-UX-045, REQ-PROD-010, REQ-PROD-011 |
| BAR-234 | releasable | automated_test | REQ-UX-046, REQ-UX-047, REQ-PROD-013, REQ-PROD-012 |
| BAR-235 | usable_early | automated_test | REQ-UX-048, REQ-PROD-014 |
| BAR-236 | releasable | manual_user_check | REQ-UX-049, REQ-PROD-033, REQ-PROD-034 |
| BAR-237 | releasable | automated_test | REQ-UX-050, REQ-PROD-032, REQ-PROD-014 |
| BAR-238 | usable_early | manual_user_check | REQ-UX-051, REQ-PROD-002 |
| BAR-239 | releasable | manual_user_check | REQ-UX-052, REQ-PROD-002 |
| BAR-240 | releasable | manual_user_check | REQ-UX-053, REQ-PROD-002 |
| BAR-241 | usable_early | automated_test | REQ-UX-054, REQ-UX-055, REQ-PROD-001 |
| BAR-242 | releasable | manual_user_check | REQ-UX-056, REQ-PROD-001, REQ-PROD-003 |
| BAR-243 | usable_early | manual_user_check | REQ-UX-058, REQ-PROD-003 |
| BAR-244 | usable_early | manual_user_check | REQ-UX-059, REQ-PROD-005 |
| BAR-245 | usable_early | manual_user_check | REQ-UX-060, REQ-PROD-006 |
| BAR-246 | usable_early | manual_user_check | REQ-UX-061, REQ-UX-062, REQ-PROD-007 |
| BAR-247 | releasable | manual_user_check | REQ-UX-063, REQ-PROD-007, REQ-PROD-006 |
| BAR-248 | usable_early | manual_user_check | REQ-UX-065, REQ-UX-066, REQ-PROD-032, REQ-PROD-033 |
| BAR-249 | releasable | manual_user_check | REQ-UX-067, REQ-UX-068, REQ-PROD-016, REQ-PROD-033, REQ-PROD-034 |
| BAR-250 | releasable | manual_user_check | REQ-UX-069, REQ-PROD-017 |
| BAR-251 | releasable | manual_user_check | REQ-UX-070, REQ-PROD-012, REQ-PROD-017 |
| BAR-252 | releasable | operational_check | REQ-UX-073, REQ-PROD-017, REQ-PROD-014 |
| BAR-253 | usable_early | operational_check | REQ-UX-074, REQ-PROD-014 |
| BAR-254 | releasable | manual_user_check | REQ-UX-075, REQ-PROD-019 |
| BAR-255 | releasable | operational_check | REQ-UX-076, REQ-UX-077, REQ-PROD-020, REQ-PROD-021, REQ-PROD-022 |
| BAR-256 | releasable | manual_user_check | REQ-UX-079, REQ-PROD-025, REQ-PROD-026 |
| BAR-257 | releasable | manual_user_check | REQ-UX-083, REQ-PROD-026 |
| BAR-258 | releasable | manual_user_check | REQ-UX-082, REQ-PROD-028, REQ-PROD-013 |
| BAR-259 | usable_early | manual_user_check | REQ-UX-084, REQ-PROD-033 |
| BAR-260 | usable_early | manual_user_check | REQ-UX-085, REQ-UX-086, REQ-PROD-033, REQ-PROD-034 |
| BAR-261 | usable_early | manual_user_check | REQ-UX-087, REQ-PROD-033 |
| BAR-262 | usable_early | manual_user_check | REQ-UX-088, REQ-PROD-033 |
| BAR-263 | releasable | manual_user_check | REQ-UX-089, REQ-PROD-034 |
| BAR-265 | usable_early | manual_user_check | REQ-UX-090 |
| BAR-266 | usable_early | automated_test | REQ-UX-091 |
| BAR-267 | usable_early | manual_user_check | REQ-UX-092 |
| BAR-268 | usable_early | manual_user_check | REQ-UX-093 |
| BAR-269 | releasable | manual_user_check | REQ-UX-094 |
| BAR-270 | usable_early | manual_user_check | REQ-UX-095 |
| BAR-271 | releasable | manual_user_check | REQ-UX-096 |
| BAR-272 | releasable | manual_user_check | REQ-UX-097 |
| BAR-273 | usable_early | automated_test | REQ-UX-098 |
| BAR-274 | usable_early | manual_user_check | REQ-UX-099 |
| BAR-275 | releasable | inspection | REQ-UX-100, REQ-PROD-036 |
| BAR-276 | usable_early | manual_user_check | REQ-UX-101 |
| BAR-277 | usable_early | manual_user_check | REQ-UX-102, REQ-UX-025 |
| BAR-278 | usable_early | manual_user_check | REQ-UX-103 |
| BAR-279 | releasable | manual_user_check | REQ-UX-104 |
| BAR-280 | usable_early | manual_user_check | REQ-UX-106 |
| BAR-281 | releasable | manual_user_check | REQ-UX-107 |
| BAR-282 | releasable | manual_user_check | REQ-UX-108 |
| BAR-283 | releasable | manual_user_check | REQ-UX-109 |
| BAR-284 | usable_early | manual_user_check | REQ-UX-110, REQ-UX-028 |
| BAR-285 | usable_early | automated_test | REQ-UX-111, REQ-UX-022 |
| BAR-286 | releasable | manual_user_check | REQ-UX-112 |
| BAR-287 | usable_early | manual_user_check | REQ-UX-113, REQ-UX-022 |
| BAR-288 | releasable | manual_user_check | REQ-UX-113 |
| BAR-289 | releasable | manual_user_check | REQ-UX-114, REQ-UX-029 |
| BAR-290 | releasable | manual_user_check | REQ-UX-115 |
| BAR-291 | usable_early | manual_user_check | REQ-UX-116, REQ-UX-032 |
| BAR-292 | usable_early | manual_user_check | REQ-UX-117, REQ-UX-008 |
| BAR-293 | releasable | inspection | REQ-UX-118 |
| BAR-294 | releasable | inspection | REQ-UX-119 |
| BAR-300 | usable_early | manual_user_check | REQ-ID-002, REQ-ID-030, REQ-ID-031, REQ-ID-032 |
| BAR-301 | usable_early | automated_test | REQ-ID-034, REQ-ID-035 |
| BAR-302 | usable_early | inspection | REQ-ID-036 |
| BAR-303 | usable_early | manual_user_check | REQ-ID-003 |
| BAR-304 | usable_early | manual_user_check | REQ-ID-033 |
| BAR-305 | usable_early | automated_test | REQ-ID-037, REQ-ID-040 |
| BAR-306 | usable_early | operational_check | REQ-ID-038, REQ-ID-044 |
| BAR-307 | usable_early | operational_check | REQ-ID-039 |
| BAR-308 | releasable | operational_check | REQ-ID-045 |
| BAR-309 | usable_early | automated_test | REQ-ID-043 |
| BAR-310 | usable_early | inspection | REQ-ID-041, REQ-ID-042 |
| BAR-311 | usable_early | inspection | REQ-ID-100 |
| BAR-312 | usable_early | automated_test | REQ-ID-060 |
| BAR-313 | usable_early | automated_test | REQ-ID-001, REQ-ID-061, REQ-ID-062, REQ-ID-063 |
| BAR-314 | usable_early | automated_test | REQ-ID-064, REQ-ID-065, REQ-ID-068 |
| BAR-315 | usable_early | automated_test | REQ-ID-066, REQ-ID-067 |
| BAR-316 | usable_early | manual_user_check | REQ-ID-069 |
| BAR-317 | usable_early | manual_user_check | REQ-ID-007 |
| BAR-318 | releasable | manual_user_check | REQ-ID-008 |
| BAR-319 | releasable | manual_user_check | REQ-ID-009 |
| BAR-320 | releasable | operational_check | REQ-ID-010 |
| BAR-321 | releasable | manual_user_check | REQ-ID-004, REQ-ID-005 |
| BAR-322 | releasable | manual_user_check | REQ-ID-013, REQ-ID-014 |
| BAR-323 | releasable | manual_user_check | REQ-ID-015 |
| BAR-324 | releasable | operational_check | REQ-ID-016, REQ-ID-046 |
| BAR-325 | releasable | manual_user_check | REQ-ID-017, REQ-ID-018 |
| BAR-326 | releasable | inspection | REQ-ID-019 |
| BAR-327 | releasable | manual_user_check | REQ-ID-020, REQ-ID-022 |
| BAR-328 | releasable | manual_user_check | REQ-ID-021 |
| BAR-329 | releasable | operational_check | REQ-ID-023, REQ-ID-024, REQ-ID-088 |
| BAR-330 | releasable | manual_user_check | REQ-ID-090 |
| BAR-331 | releasable | inspection | REQ-ID-070, REQ-ID-071 |
| BAR-332 | releasable | inspection | REQ-ID-072 |
| BAR-333 | releasable | operational_check | REQ-ID-073, REQ-ID-074 |
| BAR-334 | releasable | manual_user_check | REQ-ID-080, REQ-ID-081 |
| BAR-335 | releasable | operational_check | REQ-ID-082 |
| BAR-336 | releasable | operational_check | REQ-ID-085 |
| BAR-337 | releasable | operational_check | REQ-ID-101 |
| BAR-338 | usable_early | manual_user_check | REQ-ID-087 |
| BAR-339 | releasable | inspection | REQ-ID-086 |
| BAR-400 | usable_early | operational_check | REQ-OPS-002, REQ-OPS-009 |
| BAR-401 | usable_early | operational_check | REQ-OPS-001, REQ-OPS-003 |
| BAR-402 | usable_early | operational_check | REQ-OPS-005 |
| BAR-403 | usable_early | operational_check | REQ-OPS-006 |
| BAR-404 | usable_early | operational_check | REQ-OPS-008 |
| BAR-405 | releasable | operational_check | REQ-OPS-004 |
| BAR-406 | usable_early | manual_user_check | REQ-OPS-010 |
| BAR-407 | releasable | operational_check | REQ-OPS-011 |
| BAR-408 | releasable | inspection | REQ-OPS-012 |
| BAR-409 | usable_early | operational_check | REQ-OPS-014 |
| BAR-410 | usable_early | operational_check | REQ-OPS-015 |
| BAR-411 | releasable | manual_user_check | REQ-OPS-013 |
| BAR-412 | releasable | inspection | REQ-OPS-016 |
| BAR-420 | releasable | operational_check | REQ-OPS-020 |
| BAR-421 | releasable | inspection | REQ-OPS-021 |
| BAR-422 | releasable | operational_check | REQ-OPS-022 |
| BAR-423 | releasable | inspection | REQ-OPS-023 |
| BAR-424 | releasable | inspection | REQ-OPS-024, REQ-OPS-025 |
| BAR-425 | releasable | inspection | REQ-OPS-026 |
| BAR-426 | releasable | operational_check | REQ-OPS-027, REQ-OPS-007 |
| BAR-427 | releasable | operational_check | REQ-OPS-028 |
| BAR-428 | releasable | operational_check | REQ-OPS-029 |
| BAR-429 | releasable | operational_check | REQ-OPS-030 |
| BAR-430 | releasable | operational_check | REQ-OPS-031 |
| BAR-431 | releasable | operational_check | REQ-OPS-032 |
| BAR-432 | releasable | inspection | REQ-OPS-033 |
| BAR-440 | releasable | operational_check | REQ-OPS-040, REQ-OPS-046 |
| BAR-441 | releasable | operational_check | REQ-OPS-041 |
| BAR-442 | releasable | operational_check | REQ-OPS-042 |
| BAR-443 | usable_early | automated_test | REQ-OPS-043 |
| BAR-444 | usable_early | automated_test | REQ-OPS-044 |
| BAR-445 | releasable | operational_check | REQ-OPS-045 |
| BAR-460 | usable_early | operational_check | REQ-OPS-060, REQ-OPS-061, REQ-OPS-064, REQ-OPS-065 |
| BAR-461 | usable_early | operational_check | REQ-OPS-062 |
| BAR-462 | usable_early | manual_user_check | REQ-OPS-063 |
| BAR-463 | usable_early | inspection | REQ-OPS-066 |
| BAR-464 | releasable | operational_check | REQ-OPS-068 |
| BAR-465 | usable_early | inspection | REQ-OPS-069, REQ-OPS-079 |
| BAR-466 | releasable | operational_check | REQ-OPS-072 |
| BAR-467 | releasable | operational_check | REQ-OPS-075 |
| BAR-468 | releasable | operational_check | REQ-OPS-077 |
| BAR-480 | releasable | operational_check | REQ-OPS-080, REQ-OPS-081 |
| BAR-481 | releasable | inspection | REQ-OPS-083 |
| BAR-482 | releasable | manual_user_check | REQ-OPS-085 |
| BAR-483 | releasable | operational_check | REQ-OPS-086 |
| BAR-484 | releasable | inspection | REQ-OPS-088 |
| BAR-485 | releasable | manual_user_check | REQ-OPS-090 |
| BAR-486 | releasable | inspection | REQ-OPS-092 |
| BAR-487 | releasable | operational_check | REQ-OPS-093 |

---

## 2. Inverted `REQ → bar_ids` map

One entry per `REQ-*` that at least one `BAR-*` enforces — 343 requirements — built by inverting the `_Enforces …_` clauses above. This is the `bar_ids` column the synthesis child joins onto each matrix row by `req_id`. A release-gating `REQ-*` that does **not** appear as a key here has no `BAR-*` enforcing it; detecting that is the cross-source `BAR_COVERS_GATING_REQS` identity, owned by the synthesis child, which consumes this map — it is out of scope for this spoke, which owns only the mapping and `BAR_TESTABLE`.

| `req_id` | `bar_ids` |
|----------|-----------|
| REQ-DOM-001 | BAR-100 |
| REQ-DOM-002 | BAR-101 |
| REQ-DOM-003 | BAR-101 |
| REQ-DOM-004 | BAR-100 |
| REQ-DOM-005 | BAR-100 |
| REQ-DOM-006 | BAR-102 |
| REQ-DOM-007 | BAR-103 |
| REQ-DOM-008 | BAR-104 |
| REQ-DOM-009 | BAR-105 |
| REQ-DOM-011 | BAR-106 |
| REQ-DOM-012 | BAR-106 |
| REQ-DOM-013 | BAR-106 |
| REQ-DOM-014 | BAR-106 |
| REQ-DOM-015 | BAR-107 |
| REQ-DOM-017 | BAR-108 |
| REQ-DOM-018 | BAR-108 |
| REQ-DOM-019 | BAR-108 |
| REQ-DOM-020 | BAR-108 |
| REQ-DOM-021 | BAR-109 |
| REQ-DOM-022 | BAR-110 |
| REQ-DOM-023 | BAR-110 |
| REQ-DOM-024 | BAR-110 |
| REQ-DOM-025 | BAR-111 |
| REQ-DOM-026 | BAR-111 |
| REQ-DOM-027 | BAR-111 |
| REQ-DOM-028 | BAR-111 |
| REQ-DOM-029 | BAR-112 |
| REQ-DOM-030 | BAR-113 |
| REQ-DOM-031 | BAR-113 |
| REQ-DOM-032 | BAR-112 |
| REQ-DOM-033 | BAR-114 |
| REQ-DOM-034 | BAR-115 |
| REQ-DOM-035 | BAR-116 |
| REQ-DOM-036 | BAR-117 |
| REQ-DOM-037 | BAR-118 |
| REQ-DOM-038 | BAR-119 |
| REQ-DOM-039 | BAR-104 |
| REQ-DOM-040 | BAR-120 |
| REQ-DOM-100 | BAR-130 |
| REQ-DOM-101 | BAR-131 |
| REQ-DOM-102 | BAR-132 |
| REQ-DOM-103 | BAR-133 |
| REQ-DOM-104 | BAR-134 |
| REQ-DOM-105 | BAR-135 |
| REQ-DOM-106 | BAR-136 |
| REQ-DOM-107 | BAR-137 |
| REQ-DOM-108 | BAR-138 |
| REQ-DOM-109 | BAR-139 |
| REQ-DOM-110 | BAR-140 |
| REQ-DOM-111 | BAR-141 |
| REQ-DOM-112 | BAR-142 |
| REQ-DOM-113 | BAR-143 |
| REQ-DOM-114 | BAR-144 |
| REQ-DOM-115 | BAR-145 |
| REQ-DOM-116 | BAR-146 |
| REQ-DOM-117 | BAR-147 |
| REQ-DOM-118 | BAR-148 |
| REQ-DOM-200 | BAR-160 |
| REQ-DOM-201 | BAR-161 |
| REQ-DOM-202 | BAR-162 |
| REQ-DOM-203 | BAR-163 |
| REQ-DOM-204 | BAR-165 |
| REQ-DOM-205 | BAR-166 |
| REQ-DOM-206 | BAR-167 |
| REQ-DOM-207 | BAR-164 |
| REQ-DOM-208 | BAR-160 |
| REQ-DOM-215 | BAR-168 |
| REQ-DOM-216 | BAR-169 |
| REQ-DOM-217 | BAR-170 |
| REQ-DOM-218 | BAR-171 |
| REQ-DOM-219 | BAR-172 |
| REQ-DOM-220 | BAR-173 |
| REQ-DOM-221 | BAR-174 |
| REQ-DOM-222 | BAR-175 |
| REQ-DOM-223 | BAR-165 |
| REQ-DOM-224 | BAR-176 |
| REQ-DOM-225 | BAR-177 |
| REQ-DOM-226 | BAR-178 |
| REQ-DOM-227 | BAR-179 |
| REQ-ID-001 | BAR-313 |
| REQ-ID-002 | BAR-300 |
| REQ-ID-003 | BAR-303 |
| REQ-ID-004 | BAR-321 |
| REQ-ID-005 | BAR-321 |
| REQ-ID-007 | BAR-317 |
| REQ-ID-008 | BAR-318 |
| REQ-ID-009 | BAR-319 |
| REQ-ID-010 | BAR-320 |
| REQ-ID-013 | BAR-322 |
| REQ-ID-014 | BAR-322 |
| REQ-ID-015 | BAR-323 |
| REQ-ID-016 | BAR-324 |
| REQ-ID-017 | BAR-325 |
| REQ-ID-018 | BAR-325 |
| REQ-ID-019 | BAR-326 |
| REQ-ID-020 | BAR-327 |
| REQ-ID-021 | BAR-328 |
| REQ-ID-022 | BAR-327 |
| REQ-ID-023 | BAR-329 |
| REQ-ID-024 | BAR-329 |
| REQ-ID-030 | BAR-300 |
| REQ-ID-031 | BAR-300 |
| REQ-ID-032 | BAR-300 |
| REQ-ID-033 | BAR-304 |
| REQ-ID-034 | BAR-301 |
| REQ-ID-035 | BAR-301 |
| REQ-ID-036 | BAR-302 |
| REQ-ID-037 | BAR-305 |
| REQ-ID-038 | BAR-306 |
| REQ-ID-039 | BAR-307 |
| REQ-ID-040 | BAR-305 |
| REQ-ID-041 | BAR-310 |
| REQ-ID-042 | BAR-310 |
| REQ-ID-043 | BAR-309 |
| REQ-ID-044 | BAR-306 |
| REQ-ID-045 | BAR-308 |
| REQ-ID-046 | BAR-324 |
| REQ-ID-060 | BAR-312 |
| REQ-ID-061 | BAR-313 |
| REQ-ID-062 | BAR-313 |
| REQ-ID-063 | BAR-313 |
| REQ-ID-064 | BAR-314 |
| REQ-ID-065 | BAR-314 |
| REQ-ID-066 | BAR-315 |
| REQ-ID-067 | BAR-315 |
| REQ-ID-068 | BAR-314 |
| REQ-ID-069 | BAR-316 |
| REQ-ID-070 | BAR-331 |
| REQ-ID-071 | BAR-331 |
| REQ-ID-072 | BAR-332 |
| REQ-ID-073 | BAR-333 |
| REQ-ID-074 | BAR-333 |
| REQ-ID-080 | BAR-334 |
| REQ-ID-081 | BAR-334 |
| REQ-ID-082 | BAR-335 |
| REQ-ID-085 | BAR-336 |
| REQ-ID-086 | BAR-339 |
| REQ-ID-087 | BAR-338 |
| REQ-ID-088 | BAR-329 |
| REQ-ID-090 | BAR-330 |
| REQ-ID-100 | BAR-311 |
| REQ-ID-101 | BAR-337 |
| REQ-OPS-001 | BAR-401 |
| REQ-OPS-002 | BAR-400 |
| REQ-OPS-003 | BAR-401 |
| REQ-OPS-004 | BAR-405 |
| REQ-OPS-005 | BAR-402 |
| REQ-OPS-006 | BAR-403 |
| REQ-OPS-007 | BAR-426 |
| REQ-OPS-008 | BAR-404 |
| REQ-OPS-009 | BAR-400 |
| REQ-OPS-010 | BAR-406 |
| REQ-OPS-011 | BAR-407 |
| REQ-OPS-012 | BAR-408 |
| REQ-OPS-013 | BAR-411 |
| REQ-OPS-014 | BAR-409 |
| REQ-OPS-015 | BAR-410 |
| REQ-OPS-016 | BAR-412 |
| REQ-OPS-020 | BAR-420 |
| REQ-OPS-021 | BAR-421 |
| REQ-OPS-022 | BAR-422 |
| REQ-OPS-023 | BAR-423 |
| REQ-OPS-024 | BAR-424 |
| REQ-OPS-025 | BAR-424 |
| REQ-OPS-026 | BAR-425 |
| REQ-OPS-027 | BAR-426 |
| REQ-OPS-028 | BAR-427 |
| REQ-OPS-029 | BAR-428 |
| REQ-OPS-030 | BAR-429 |
| REQ-OPS-031 | BAR-430 |
| REQ-OPS-032 | BAR-431 |
| REQ-OPS-033 | BAR-432 |
| REQ-OPS-040 | BAR-440 |
| REQ-OPS-041 | BAR-441 |
| REQ-OPS-042 | BAR-442 |
| REQ-OPS-043 | BAR-443 |
| REQ-OPS-044 | BAR-444 |
| REQ-OPS-045 | BAR-445 |
| REQ-OPS-046 | BAR-440 |
| REQ-OPS-060 | BAR-460 |
| REQ-OPS-061 | BAR-460 |
| REQ-OPS-062 | BAR-461 |
| REQ-OPS-063 | BAR-462 |
| REQ-OPS-064 | BAR-460 |
| REQ-OPS-065 | BAR-460 |
| REQ-OPS-066 | BAR-463 |
| REQ-OPS-068 | BAR-464 |
| REQ-OPS-069 | BAR-465 |
| REQ-OPS-072 | BAR-466 |
| REQ-OPS-075 | BAR-467 |
| REQ-OPS-077 | BAR-468 |
| REQ-OPS-079 | BAR-465 |
| REQ-OPS-080 | BAR-480 |
| REQ-OPS-081 | BAR-480 |
| REQ-OPS-083 | BAR-481 |
| REQ-OPS-085 | BAR-482 |
| REQ-OPS-086 | BAR-483 |
| REQ-OPS-088 | BAR-484 |
| REQ-OPS-090 | BAR-485 |
| REQ-OPS-092 | BAR-486 |
| REQ-OPS-093 | BAR-487 |
| REQ-PROD-001 | BAR-001, BAR-241, BAR-242 |
| REQ-PROD-002 | BAR-002, BAR-238, BAR-239, BAR-240 |
| REQ-PROD-003 | BAR-003, BAR-242, BAR-243 |
| REQ-PROD-005 | BAR-004, BAR-244 |
| REQ-PROD-006 | BAR-005, BAR-245, BAR-247 |
| REQ-PROD-007 | BAR-006, BAR-246, BAR-247 |
| REQ-PROD-008 | BAR-007, BAR-231 |
| REQ-PROD-009 | BAR-008, BAR-232 |
| REQ-PROD-010 | BAR-009, BAR-233 |
| REQ-PROD-011 | BAR-010, BAR-233 |
| REQ-PROD-012 | BAR-014, BAR-231, BAR-234, BAR-251 |
| REQ-PROD-013 | BAR-015, BAR-234, BAR-258 |
| REQ-PROD-014 | BAR-016, BAR-235, BAR-237, BAR-252, BAR-253 |
| REQ-PROD-016 | BAR-017, BAR-249 |
| REQ-PROD-017 | BAR-018, BAR-250, BAR-251, BAR-252 |
| REQ-PROD-019 | BAR-019, BAR-254 |
| REQ-PROD-020 | BAR-020, BAR-255 |
| REQ-PROD-021 | BAR-021, BAR-255 |
| REQ-PROD-022 | BAR-022, BAR-255 |
| REQ-PROD-023 | BAR-011 |
| REQ-PROD-024 | BAR-012 |
| REQ-PROD-025 | BAR-023, BAR-256 |
| REQ-PROD-026 | BAR-024, BAR-256, BAR-257 |
| REQ-PROD-028 | BAR-025, BAR-258 |
| REQ-PROD-030 | BAR-026, BAR-230 |
| REQ-PROD-031 | BAR-230, BAR-231 |
| REQ-PROD-032 | BAR-027, BAR-237, BAR-248 |
| REQ-PROD-033 | BAR-028, BAR-236, BAR-248, BAR-249, BAR-259, BAR-260, BAR-261, BAR-262 |
| REQ-PROD-034 | BAR-029, BAR-236, BAR-249, BAR-260, BAR-263 |
| REQ-PROD-035 | BAR-030 |
| REQ-PROD-036 | BAR-031, BAR-275 |
| REQ-PROD-037 | BAR-013 |
| REQ-PROD-038 | BAR-032 |
| REQ-PROD-039 | BAR-033 |
| REQ-PROD-040 | BAR-034 |
| REQ-PROD-041 | BAR-035 |
| REQ-UX-001 | BAR-200 |
| REQ-UX-002 | BAR-201 |
| REQ-UX-003 | BAR-202 |
| REQ-UX-004 | BAR-203 |
| REQ-UX-005 | BAR-204 |
| REQ-UX-006 | BAR-205 |
| REQ-UX-007 | BAR-206 |
| REQ-UX-008 | BAR-207, BAR-292 |
| REQ-UX-009 | BAR-208 |
| REQ-UX-010 | BAR-209 |
| REQ-UX-011 | BAR-210 |
| REQ-UX-012 | BAR-211 |
| REQ-UX-013 | BAR-212 |
| REQ-UX-014 | BAR-213 |
| REQ-UX-016 | BAR-213 |
| REQ-UX-017 | BAR-214 |
| REQ-UX-018 | BAR-214 |
| REQ-UX-020 | BAR-215 |
| REQ-UX-021 | BAR-216 |
| REQ-UX-022 | BAR-217, BAR-285, BAR-287 |
| REQ-UX-025 | BAR-218, BAR-277 |
| REQ-UX-026 | BAR-219 |
| REQ-UX-027 | BAR-220 |
| REQ-UX-028 | BAR-221, BAR-284 |
| REQ-UX-029 | BAR-222, BAR-289 |
| REQ-UX-031 | BAR-226 |
| REQ-UX-032 | BAR-223, BAR-291 |
| REQ-UX-033 | BAR-224 |
| REQ-UX-034 | BAR-224 |
| REQ-UX-035 | BAR-225 |
| REQ-UX-036 | BAR-226 |
| REQ-UX-037 | BAR-227 |
| REQ-UX-038 | BAR-228 |
| REQ-UX-039 | BAR-229 |
| REQ-UX-040 | BAR-230 |
| REQ-UX-041 | BAR-231 |
| REQ-UX-042 | BAR-232 |
| REQ-UX-043 | BAR-231 |
| REQ-UX-044 | BAR-233 |
| REQ-UX-045 | BAR-233 |
| REQ-UX-046 | BAR-234 |
| REQ-UX-047 | BAR-234 |
| REQ-UX-048 | BAR-235 |
| REQ-UX-049 | BAR-236 |
| REQ-UX-050 | BAR-237 |
| REQ-UX-051 | BAR-238 |
| REQ-UX-052 | BAR-239 |
| REQ-UX-053 | BAR-240 |
| REQ-UX-054 | BAR-241 |
| REQ-UX-055 | BAR-241 |
| REQ-UX-056 | BAR-242 |
| REQ-UX-058 | BAR-243 |
| REQ-UX-059 | BAR-244 |
| REQ-UX-060 | BAR-245 |
| REQ-UX-061 | BAR-246 |
| REQ-UX-062 | BAR-246 |
| REQ-UX-063 | BAR-247 |
| REQ-UX-065 | BAR-248 |
| REQ-UX-066 | BAR-248 |
| REQ-UX-067 | BAR-249 |
| REQ-UX-068 | BAR-249 |
| REQ-UX-069 | BAR-250 |
| REQ-UX-070 | BAR-251 |
| REQ-UX-073 | BAR-252 |
| REQ-UX-074 | BAR-253 |
| REQ-UX-075 | BAR-254 |
| REQ-UX-076 | BAR-255 |
| REQ-UX-077 | BAR-255 |
| REQ-UX-079 | BAR-256 |
| REQ-UX-082 | BAR-258 |
| REQ-UX-083 | BAR-257 |
| REQ-UX-084 | BAR-259 |
| REQ-UX-085 | BAR-260 |
| REQ-UX-086 | BAR-260 |
| REQ-UX-087 | BAR-261 |
| REQ-UX-088 | BAR-262 |
| REQ-UX-089 | BAR-263 |
| REQ-UX-090 | BAR-265 |
| REQ-UX-091 | BAR-266 |
| REQ-UX-092 | BAR-267 |
| REQ-UX-093 | BAR-268 |
| REQ-UX-094 | BAR-269 |
| REQ-UX-095 | BAR-270 |
| REQ-UX-096 | BAR-271 |
| REQ-UX-097 | BAR-272 |
| REQ-UX-098 | BAR-273 |
| REQ-UX-099 | BAR-274 |
| REQ-UX-100 | BAR-275 |
| REQ-UX-101 | BAR-276 |
| REQ-UX-102 | BAR-277 |
| REQ-UX-103 | BAR-278 |
| REQ-UX-104 | BAR-279 |
| REQ-UX-106 | BAR-280 |
| REQ-UX-107 | BAR-281 |
| REQ-UX-108 | BAR-282 |
| REQ-UX-109 | BAR-283 |
| REQ-UX-110 | BAR-284 |
| REQ-UX-111 | BAR-285 |
| REQ-UX-112 | BAR-286 |
| REQ-UX-113 | BAR-287, BAR-288 |
| REQ-UX-114 | BAR-289 |
| REQ-UX-115 | BAR-290 |
| REQ-UX-116 | BAR-291 |
| REQ-UX-117 | BAR-292 |
| REQ-UX-118 | BAR-293 |
| REQ-UX-119 | BAR-294 |

---

## 3. `BAR_TESTABLE` verdict

**Identity:** *Every `BAR-*` names a verification method from the schema vocabulary and references ≥1 `REQ-*`.* (Stated verbatim from the DAG-root contract manifest.)

**Verdict: PASS.**

**Evidence.** Across all 278 criteria parsed from `design/release-bar.md`:

- Every criterion's `verification_method` is one of the closed vocabulary (`manual_user_check`, `automated_test`, `inspection`, `operational_check`) — **0** criteria carry a method outside it.
- Every criterion references at least one `REQ-*` in its `_Enforces …_` clause — **0** criteria reference no requirement.
- As a parse-integrity check (so a `FAIL` cannot hide behind a line this spoke failed to read): every `BAR-*` line matched the expected `**BAR-NNN** (\`stage\` · \`method\`) — … _Enforces …_` shape, every criterion carried a trailing `_Enforces …_` clause, and no `bar_id` appeared twice — **0** parse problems.
- Every criterion's `stage` is one of `usable_early` / `releasable` — **0** out-of-vocabulary stages.

A cold reviewer can reproduce this by parsing the same `_Enforces …_` clauses and checking each method against the four-value vocabulary; the per-`BAR-*` table above is that parse in full.

---

### Handoff to the synthesis join

- **Owned and delivered here:** the `REQ → bar_ids` map (section 2) and the `BAR_TESTABLE` verdict (section 3).
- **Not owned here (do not infer from this file):** the matrix design-side columns (`req_id`, `release_gating`, `design_doc_ref`), the `epic`/`issue_numbers` columns, the `live_status` column, and the cross-source `BAR_COVERS_GATING_REQS` identity. Those belong to the sibling spokes and the synthesis child.
- **Key for the join:** `req_id`, verbatim. Each listed `REQ-*` key here attaches its `bar_ids` to the matching matrix row.
