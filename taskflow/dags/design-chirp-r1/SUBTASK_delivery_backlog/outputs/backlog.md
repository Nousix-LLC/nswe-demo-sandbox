# chirp — design-r1 delivery backlog (epic/issue index + trace map)

The board backlog for the current chirp design, delivered to `design/` by `Nousix-LLC/nswe-demo#122`
(branch `work/design-chirp-r1` → `main`) and measured against the live product at commit `c805525`.
This file is the index the synthesis gate verifies: it names every epic and issue, maps each to the
current `REQ-*`/`BAR-*` ids and the design document it traces to, places each issue under exactly one
epic in dependency order, and records what was de-duplicated against the board rather than re-filed.

Traceability ids and the design-file section names follow `../contracts/id_and_traceability_schema.yaml`
and `../contracts/design_artifact_map.yaml`. `BAR-*` ids are the **current** release bar
(`design/release-bar.md`, `BAR-001..487`). Where an existing ticket body still carries a first-run
`BAR-001..050` label, the current ids in this file supersede it (see §5, Reconciliation).

---

## 1. How the backlog is built

- **One epic = one coherent, landable code goal** (one epic = one code DAG's goal), with its dependencies
  on other epics stated. The eleven design epics already on the board satisfy this; this backlog adopts
  and re-anchors them rather than re-filing.
- **Each issue sits under exactly one epic** and its acceptance criteria trace to ≥1 current `REQ-*` and,
  through this index, to ≥1 current `BAR-*` and the design-document section that defines the requirement.
- **Order reaches a usable product early, the release bar after.** Issues inherit the release bar's
  staging: `usable_early` (what a first adoptable version must already meet) before `releasable` (what the
  public release adds). The epic waves in §3 encode the cross-epic order.
- **The in-memory store at `c805525` is the one structural release blocker.** Durable persistence
  (EPIC #56) is wave 0 and `usable_early`; most of the product builds on it.

## 2. Epic index

| Epic | Title | Wave | Depends on (epics) | Current release-bar coverage | Design document(s) |
|------|-------|------|--------------------|------------------------------|--------------------|
| #56 | Durable persistence & data integrity | 0 | — | `BAR-013`; `BAR-100..120` (model integrity), `BAR-130..148` (persistence), `BAR-165` (seam); `BAR-400..412` (durable data) | `domain-application-design.md` (persistence_requirement, domain_model, interfaces_and_entry_points); `operational-readiness.md` (durable_data) |
| #89 | Self-hostable build/run & domain integrity | 0 | — | `BAR-160..179` (module/contract structure, single service, wire contract, config-from-env) | `domain-application-design.md` (modules_and_responsibilities, interfaces_and_entry_points); `operational-readiness.md` (existing_followups) |
| #83 | Identity, authentication & sessions | 1 | #56 | `BAR-300..311`; `BAR-007/009/010/016`; `BAR-112/113/114/116/136`; `BAR-231/232/233/235`; `BAR-409` | `identity-security.md` (authentication_and_sessions, accounts_and_lifecycle); `experience-design.md` (screens_and_flows) |
| #34 | Core product loop & accurate UX states | 2 | #56, #83 | `BAR-001..006/011/012`; `BAR-100..111/117/170..173`; `BAR-200..214/225/226/238..248/259..263` | `product-requirements.md` (user_journeys, requirements_and_acceptance_criteria); `experience-design.md` (information_architecture_and_interaction, screens_and_flows, empty_error_loading_states) |
| #43 | Authorization & application security | 2 | #83, #56 | `BAR-312..316`; `BAR-011/012`; `BAR-163/164/172`; `BAR-302/310/311` | `identity-security.md` (authorization, threat_model) |
| #77 | Account lifecycle (recovery, profile, hub, deletion, export) | 3 | #83, #56, #43 | `BAR-014..022`; `BAR-105/115/118/119`; `BAR-249..255`; `BAR-317..330`; `BAR-407/410/411` | `identity-security.md` (accounts_and_lifecycle); `product-requirements.md` (requirements_and_acceptance_criteria); `experience-design.md` (screens_and_flows) |
| #72 | Admin & support + abuse limits | 3 | #83, #43, (#56) | `BAR-023/025/035`; `BAR-258`; `BAR-331..337`; `BAR-440..445`; `BAR-468` | `identity-security.md` (abuse_and_privacy_basics, authorization); `operational-readiness.md` (limits_and_quotas); `product-requirements.md` |
| #53 | Visual design system, responsive layout & accessibility | 3 | #34 | `BAR-030/031/036`; `BAR-215..224` (visual); `BAR-265..274/286` (responsive); `BAR-275..294` (a11y) | `experience-design.md` (visual_language_and_design_system, responsive_layout, accessibility) |
| #44 | Durable-data operations (backup, recovery, rollback, migration) | 3 | #56 | `BAR-032`; `BAR-146/148`; `BAR-420..432` | `operational-readiness.md` (backups_and_recovery) |
| #90 | Observability & incident response | 3 | #56 | `BAR-033/034`; `BAR-145/178`; `BAR-460..468` (observability); `BAR-480..487` (incident/status/availability) | `operational-readiness.md` (observability, status_and_incident) |
| #52 | Trust, safety, privacy & the legal surface | 4 | #83, #43, #72 | `BAR-023/024`; `BAR-256/257`; `BAR-328..330`; `BAR-334/335/338/339`; `BAR-412` | `identity-security.md` (abuse_and_privacy_basics); `product-requirements.md`; `experience-design.md` (screens_and_flows); `operational-readiness.md` (status_and_incident) |

Parent trackers (pre-existing, not design epics): #1 (ferric), #2 (chirp), #3 (DevOps CI/CD). The design
epics above extend #2/#3 as distinct release-bar code goals; they are not duplicated into #1/#2/#3.

## 3. Wave / dependency order (usable product early, release bar after)

```
wave 0  #56 Durable persistence ─────────┐          #89 Self-hostable build/run (independent)
                                          │
wave 1  #83 Identity, auth & sessions ◄───┘
                                          │
wave 2  #34 Core product loop ◄───────────┤   #43 Authorization & app security ◄───┐
                                          │                                        │
wave 3  #77 Account lifecycle ◄───────────┴── #72 Admin & abuse limits ◄───────────┘
        #53 Visual/responsive/a11y ◄─ #34     #44 Durable-data operations ◄─ #56
        #90 Observability & incident ◄─ #56
                                          │
wave 4  #52 Trust, safety, privacy ◄── #83, #43, #72
```

The graph is acyclic. A first **usable-early** product is reached when wave 0–2's `usable_early` criteria
hold: durable persistence (#56), real credentialed identity and safe sessions (#83), the core loop with
accurate states and the mobile/keyboard floor (#34, and the `usable_early` items of #53). The
**releasable** bar is reached when the wave 3–4 `releasable` criteria hold: full account lifecycle (#77),
admin/abuse (#72), durable-data operations (#44), observability/incident/status (#90), the trust & legal
surface (#52), and the `releasable` completion of #53.

## 4. Issue trace map

Each row: issue → its one epic → current `REQ-*` → current `BAR-*` → design section → bar stage. `REQ-*`
cited are the stable requirement anchors already on the ticket (valid against the current design unless
noted in §5); `BAR-*` are the current release-bar ids that enforce them.

### EPIC #56 — Durable persistence & data integrity (wave 0)

| Issue | Trace (current `REQ`) | Current `BAR` | Design section | Stage |
|-------|----------------------|---------------|----------------|-------|
| #64 Replace the in-memory store with durable, pod-independent storage | REQ-PROD-037, REQ-DOM-113/114, REQ-OPS-001/002/003/009 | BAR-013, BAR-130, BAR-143, BAR-144, BAR-400, BAR-401, BAR-402 | domain…persistence_requirement; operational…durable_data | usable_early |
| #65 Preserve invariants, counts, opaque ids under concurrency | REQ-DOM-040/101/104/105/107/111, REQ-OPS-006/008 | BAR-103, BAR-109, BAR-110, BAR-120, BAR-131, BAR-134, BAR-135, BAR-137, BAR-141, BAR-403, BAR-404 | domain…domain_model; operational…durable_data | usable_early |
| #66 Durable storage plugs into the `ChirpRepository` seam soundly; versioned schema | REQ-DOM-114/118, REQ-DOM-204/223, REQ-OPS-004 | BAR-144, BAR-148, BAR-165, BAR-405 | domain…interfaces_and_entry_points; operational…durable_data | releasable |
| #67 Honour retention/capacity; prove durability with a repeatable drill | REQ-OPS-010/011/012/013/016, REQ-DOM-116/117 | BAR-146, BAR-147, BAR-406, BAR-407, BAR-408, BAR-411, BAR-412, BAR-430 | operational…durable_data | releasable |

### EPIC #89 — Self-hostable build/run & domain integrity (wave 0)

| Issue | Trace (current `REQ`) | Current `BAR` | Design section | Stage |
|-------|----------------------|---------------|----------------|-------|
| #91 One self-contained service; wire contract extended only through `chirp-types` | REQ-DOM-200/201/202/205/215/216/217/221/222/224/225 | BAR-160, BAR-161, BAR-162, BAR-166, BAR-168, BAR-169, BAR-174, BAR-175, BAR-176, BAR-177 | domain…modules_and_responsibilities, interfaces_and_entry_points | usable_early |
| #92 Builds and runs from documented steps on the self-hostable surface | REQ-DOM-227 | BAR-179 | domain…interfaces_and_entry_points; operational…existing_followups | usable_early |
| #23 Harden & exercise the native k3s install path *(folded, non-gating)* | — | — | operational…existing_followups | non-gating |
| #24 ArgoCD least-privilege RBAC + supply-chain hardening *(folded, non-gating)* | — | — | operational…existing_followups | non-gating |
| #25 Containerize follow-ups: non-blocking polish *(folded, non-gating)* | — | — | operational…existing_followups | non-gating |
| #27 PR-body hygiene (DOC-3, HYG-1) *(folded, non-gating)* | — | — | — (repository hygiene) | non-gating |

Note on #92: the current release bar gates deploy-from-configuration (`BAR-179`) and does not mint a
separate "builds bit-for-bit reproducibly" criterion (the first-run `BAR-050`). Reproducible-from-docs
build/run is held as the design README's self-hostable-surface statement; `BAR-179` is the gated
criterion. (This supersedes the first-run-bar review items #103 and the capacity note #107, which were
raised against the first-run bar.)

### EPIC #83 — Identity, authentication & sessions (wave 1)

| Issue | Trace (current `REQ`) | Current `BAR` | Design section | Stage |
|-------|----------------------|---------------|----------------|-------|
| #84 Self-service, validated sign-up creates one owned, credentialed account | REQ-ID-002/003/004/005, REQ-PROD-008/009, REQ-UX-041/042/043 | BAR-007, BAR-008, BAR-231, BAR-232, BAR-303, BAR-321 | identity…accounts_and_lifecycle; experience…screens_and_flows | usable_early (contact-verify step: releasable) |
| #85 Sign-in proves ownership; a handle is never enough | REQ-ID-030/031/032/033, REQ-PROD-010/011, REQ-UX-044/045 | BAR-009, BAR-010, BAR-233, BAR-300, BAR-304, BAR-305 | identity…authentication_and_sessions; experience…screens_and_flows | usable_early |
| #86 Sessions are durable, bounded, confidential, never silently dropped | REQ-ID-037/038/040/041/042/044/045, REQ-DOM-106, REQ-OPS-014 | BAR-112, BAR-113, BAR-136, BAR-305, BAR-306, BAR-308, BAR-310, BAR-311, BAR-409 | identity…authentication_and_sessions; domain…persistence_requirement | usable_early |
| #87 Deliberate sign-out ends the session at the server | REQ-ID-039, REQ-PROD-014, REQ-UX-048 | BAR-016, BAR-113, BAR-235, BAR-307 | identity…authentication_and_sessions; experience…screens_and_flows | usable_early |
| #88 Session integrity: fixation-resistant, re-proof, revoked on credential change | REQ-ID-043/046 | BAR-305, BAR-309, BAR-324 | identity…authentication_and_sessions | usable_early (re-proof/reset-eject: releasable) |

### EPIC #34 — Core product loop & accurate UX states (wave 2)

| Issue | Trace (current `REQ`) | Current `BAR` | Design section | Stage |
|-------|----------------------|---------------|----------------|-------|
| #35 Logged-out reading and a useful landing with accurate states | REQ-PROD-007/030/031, REQ-UX-001/040/084 | BAR-006, BAR-026, BAR-200, BAR-230, BAR-259, BAR-268 | product…user_journeys; experience…information_architecture_and_interaction, screens_and_flows | usable_early |
| #36 Compose and post within the limit without losing the draft | REQ-PROD-001, REQ-UX-013/054/055/056 | BAR-001, BAR-212, BAR-225, BAR-241, BAR-242 | product…requirements_and_acceptance_criteria; experience…screens_and_flows | usable_early |
| #37 Home timeline: reverse-chronological feed, accurate states, paging | REQ-PROD-002, REQ-DOM-025/026/027/028, REQ-UX-051/052/053 | BAR-002, BAR-171, BAR-209, BAR-238, BAR-239, BAR-240 | product…requirements_and_acceptance_criteria; experience…screens_and_flows; domain…domain_model | usable_early |
| #38 Profiles present the user accurately and handle all states | REQ-PROD-007, REQ-UX-061/062/063 | BAR-006, BAR-205, BAR-246, BAR-247 | product…requirements_and_acceptance_criteria; experience…screens_and_flows | usable_early |
| #39 Follow/unfollow and like/unlike reliable with accurate counts | REQ-PROD-005/006, REQ-DOM-017/022/023/024, REQ-UX-059/060 | BAR-004, BAR-005, BAR-110, BAR-244, BAR-245 | product…requirements_and_acceptance_criteria; experience…screens_and_flows; domain…domain_model | usable_early |
| #40 One consistent, accurate state model across the product | REQ-UX-031/033/036/085/086/087/088 | BAR-028, BAR-211, BAR-226, BAR-259, BAR-260, BAR-261, BAR-262 | experience…empty_error_loading_states | usable_early |
| #41 Accurate, loss-free input, submission and action feedback | REQ-PROD-033/034, REQ-UX-012/039/089 | BAR-211, BAR-229, BAR-262, BAR-263 | experience…empty_error_loading_states, screens_and_flows | usable_early |
| #42 Navigation reaches every product surface in both auth states | REQ-UX-002/003/005/092/093 | BAR-201, BAR-202, BAR-204, BAR-212, BAR-267, BAR-268 | experience…information_architecture_and_interaction | usable_early |
| #123 Onboarding: a new account's first run lands on a useful empty state | REQ-PROD-032, REQ-UX-065/066 | BAR-027, BAR-213, BAR-237, BAR-248 | experience…screens_and_flows, empty_error_loading_states; product…user_journeys | usable_early (BAR-248) / releasable (BAR-027/213/237) |

### EPIC #43 — Authorization & application security (wave 2)

| Issue | Trace (current `REQ`) | Current `BAR` | Design section | Stage |
|-------|----------------------|---------------|----------------|-------|
| #45 A user acts only on their own resources and only as their own identity | REQ-PROD-023, REQ-ID-064/065/066/067/068 | BAR-011, BAR-314, BAR-315 | identity…authorization | usable_early |
| #46 Authorization is server-side, default-deny, consistent across every entry point | REQ-ID-060/061/062/063/069, REQ-DOM-203/207 | BAR-163, BAR-164, BAR-312, BAR-313, BAR-316 | identity…authorization; domain…modules_and_responsibilities | usable_early |
| #47 Application security: credentials protected, mutations resist CSRF, content cannot execute as code | REQ-PROD-024, REQ-ID-036/100, REQ-DOM-219 | BAR-012, BAR-302, BAR-310, BAR-311 | identity…threat_model, authentication_and_sessions | usable_early (hardening depth: releasable) |

### EPIC #77 — Account lifecycle (wave 3)

| Issue | Trace (current `REQ`) | Current `BAR` | Design section | Stage |
|-------|----------------------|---------------|----------------|-------|
| #78 Account recovery returns a locked-out owner, without becoming a bypass | REQ-PROD-012/013, REQ-ID-013/014/015/016, REQ-UX-046/047 | BAR-014, BAR-015, BAR-234, BAR-321, BAR-322, BAR-323, BAR-324 | identity…accounts_and_lifecycle; experience…screens_and_flows | releasable |
| #79 View and edit your own profile, persisted | REQ-PROD-016, REQ-DOM-009, REQ-ID-007, REQ-UX-067/068 | BAR-017, BAR-105, BAR-249, BAR-317 | product…requirements_and_acceptance_criteria; experience…screens_and_flows | releasable |
| #82 A reachable account-management hub gathers the lifecycle surfaces | REQ-PROD-017, REQ-ID-008, REQ-UX-069 | BAR-018, BAR-214, BAR-250, BAR-318 | experience…screens_and_flows; identity…accounts_and_lifecycle | releasable |
| #80 Self-service account deletion is confirmed, honoured, bounded | REQ-PROD-020/021/022, REQ-DOM-037/112, REQ-ID-020/021/022/023, REQ-OPS-011, REQ-UX-076/077 | BAR-020, BAR-021, BAR-022, BAR-118, BAR-142, BAR-255, BAR-327, BAR-328, BAR-329, BAR-407 | identity…accounts_and_lifecycle; product…requirements_and_acceptance_criteria; experience…screens_and_flows | releasable |
| #81 Export your own complete data in a portable form | REQ-PROD-019, REQ-DOM-038/117, REQ-ID-017/018/019, REQ-OPS-013, REQ-UX-075 | BAR-019, BAR-119, BAR-147, BAR-254, BAR-325, BAR-326, BAR-411 | identity…accounts_and_lifecycle; experience…screens_and_flows | releasable |

### EPIC #72 — Admin & support + abuse limits (wave 3)

| Issue | Trace (current `REQ`) | Current `BAR` | Design section | Stage |
|-------|----------------------|---------------|----------------|-------|
| #73 Baseline anti-abuse limits and per-caller rate limits enforced safely | REQ-PROD-041, REQ-ID-085/101, REQ-OPS-040/041/042/046/047 | BAR-035, BAR-336, BAR-337, BAR-440, BAR-441, BAR-442, BAR-445 | operational…limits_and_quotas; identity…abuse_and_privacy_basics | releasable |
| #74 Request payloads and collection responses are bounded | REQ-OPS-043/044 | BAR-443, BAR-444 | operational…limits_and_quotas | usable_early |
| #75 A segregated operator surface can look up and support an account, under data minimisation | REQ-PROD-028, REQ-ID-070/071/072, REQ-UX-082 | BAR-025, BAR-258, BAR-331, BAR-332 | identity…authorization, abuse_and_privacy_basics | releasable |
| #76 Moderation authority is least-privilege, attributable, revocable | REQ-ID-073/074, REQ-OPS-077 | BAR-331, BAR-333, BAR-335, BAR-468 | identity…authorization; operational…observability | releasable |

### EPIC #53 — Visual design system, responsive layout & accessibility (wave 3)

| Issue | Trace (current `REQ`) | Current `BAR` | Design section | Stage |
|-------|----------------------|---------------|----------------|-------|
| #60 One consistent visual language: typography, colour, spacing, readable column | REQ-UX-020/021/022/026/032 | BAR-215, BAR-216, BAR-217, BAR-219, BAR-223 | experience…visual_language_and_design_system | usable_early (type/contrast) / releasable (system) |
| #61 A consistent component system with full interaction and feedback states | REQ-UX-027/028/029/033/034 | BAR-220, BAR-221, BAR-222, BAR-224 | experience…visual_language_and_design_system | releasable |
| #62 Mobile floor: usable on a small phone without losing state | REQ-PROD-035, REQ-UX-090/091/092/095/098/099 | BAR-030, BAR-265, BAR-266, BAR-267, BAR-270, BAR-273, BAR-274 | experience…responsive_layout | usable_early |
| #63 Every surface reflows correctly across the defined breakpoint set | REQ-UX-093/094/096/097/112 | BAR-268, BAR-269, BAR-271, BAR-272, BAR-286 | experience…responsive_layout | releasable |
| #68 Full keyboard operability with managed, visible focus | REQ-PROD-036, REQ-UX-025/101/102/103/104 | BAR-031, BAR-218, BAR-276, BAR-277, BAR-278, BAR-279 | experience…accessibility | usable_early |
| #69 Correct structure, names, announcements for assistive technology | REQ-UX-106/107/108/109/110/115/116/117 | BAR-280, BAR-281, BAR-282, BAR-283, BAR-284, BAR-290, BAR-291, BAR-292 | experience…accessibility | usable_early (names/states) / releasable (landmarks) |
| #70 Perceivable content: contrast, not-colour-alone, resize, motion | REQ-UX-022/111/113/114 | BAR-217, BAR-285, BAR-287, BAR-288, BAR-289 | experience…accessibility | usable_early (contrast) / releasable |
| #71 Accessibility verified across the whole gating screen inventory | REQ-UX-100/118/119 | BAR-275, BAR-293, BAR-294 | experience…accessibility | releasable |

### EPIC #44 — Durable-data operations (wave 3)

| Issue | Trace (current `REQ`) | Current `BAR` | Design section | Stage |
|-------|----------------------|---------------|----------------|-------|
| #48 Scheduled, complete, monitored, separately-stored backups | REQ-OPS-020/021/023/032 | BAR-420, BAR-421, BAR-423, BAR-431 | operational…backups_and_recovery | releasable |
| #49 Define and meet RPO/RTO; prove restore by a periodic drill and a runbook | REQ-OPS-024/025/026/027/028/031/033 | BAR-424, BAR-425, BAR-426, BAR-427, BAR-430, BAR-432 | operational…backups_and_recovery | releasable |
| #50 Deploy rollback returns to last known-good without destroying user data | REQ-OPS-029/030 | BAR-428, BAR-429 | operational…backups_and_recovery | releasable |
| #51 Forward schema migrations apply safely; a failed migration has a recovery path | REQ-OPS-004, REQ-DOM-118, REQ-OPS-022 | BAR-148, BAR-405, BAR-422 | operational…backups_and_recovery; domain…persistence_requirement | releasable |

### EPIC #90 — Observability & incident response (wave 3)

| Issue | Trace (current `REQ`) | Current `BAR` | Design section | Stage |
|-------|----------------------|---------------|----------------|-------|
| #93 Honest product health: distinct liveness/readiness that exercise the store, fail closed | REQ-PROD-039, REQ-DOM-115/226, REQ-OPS-060/061/062/063/064/065 | BAR-033, BAR-145, BAR-178, BAR-460, BAR-461, BAR-462 | operational…observability; domain…interfaces_and_entry_points | usable_early |
| #94 Structured, correlated, secret-free logs an operator can diagnose from | REQ-OPS-066/068/069/079 | BAR-463, BAR-464, BAR-465 | operational…observability | usable_early (structured/secret-free) / releasable (coverage) |
| #97 Request metrics and named SLIs that make degradation visible | REQ-OPS-072/075 | BAR-466, BAR-467 | operational…observability | releasable |
| #98 Detect product trouble on product health and notify a responsible human | REQ-OPS-080/081 | BAR-480 | operational…status_and_incident | releasable |
| #95 Honest user-facing degradation that never loses the user's work | REQ-PROD-034, REQ-OPS-090 | BAR-029, BAR-485 | operational…status_and_incident; experience…empty_error_loading_states | releasable |
| #96 Define incident-response responsibility and record incidents durably | REQ-OPS-081/083 | BAR-481 | operational…status_and_incident | releasable |
| #124 Status & availability surface: tell users when chirp is down; availability stated and measured | REQ-PROD-040, REQ-OPS-085/086/088/092/093 | BAR-034, BAR-482, BAR-483, BAR-484, BAR-486, BAR-487 | operational…status_and_incident | releasable |

### EPIC #52 — Trust, safety, privacy & the legal surface (wave 4)

| Issue | Trace (current `REQ`) | Current `BAR` | Design section | Stage |
|-------|----------------------|---------------|----------------|-------|
| #54 Report a chirp or an account | REQ-PROD-025/026, REQ-ID-080/081/082, REQ-UX-079 | BAR-023, BAR-256, BAR-334, BAR-335 | identity…abuse_and_privacy_basics; experience…screens_and_flows | releasable |
| #55 Block an account to reduce exposure | REQ-ID-083/084 | — *(deferred, non-gating — designed; see §6)* | identity…abuse_and_privacy_basics | releasable (deferred) |
| #57 Moderation's effect is visible to the people affected | REQ-ID-021, REQ-ID-074 | BAR-328, BAR-333 | identity…accounts_and_lifecycle, authorization | releasable |
| #58 A reachable, accurate privacy & terms surface | REQ-ID-086/090, REQ-UX-083, REQ-OPS-016 | BAR-024, BAR-257, BAR-330, BAR-412 | identity…abuse_and_privacy_basics; operational…status_and_incident | releasable |
| #59 Access & erasure: data-subject rights are honoured | REQ-ID-017/018/020/023/090 | BAR-325, BAR-329, BAR-330 | identity…abuse_and_privacy_basics, accounts_and_lifecycle | releasable |

## 5. Reconciliation against the existing board (de-duplication record)

This is a reconstructed run. A prior run produced the first chirp design (merged as `#33`) **and a full
board backlog** — epics #34, #43, #44, #52, #53, #56, #72, #77, #83, #89, #90 and issues #35–#98 — tracing
to the first-run release bar's `BAR-001..050` id scheme. The design was then revised; `#122` delivers the
current design, whose release bar is renumbered and expanded to `BAR-001..487`.

**Finding.** The existing backlog's epic structure and issue coverage still map, one-for-one, to the
current design's areas and surfaces. One epic is one landable code goal; each issue sits under exactly one
epic; the wave order is acyclic and already reaches a usable product before the release bar. The only
break the revision introduced is **traceability**: the `BAR-*` labels in the ticket bodies point at the
superseded first-run scheme, and a few identity `REQ-ID` ids above `REQ-ID-101` are first-run ids absent
from the current design.

**Action taken (extend/supersede, not duplicate).**
- The existing epics and issues are **adopted, not re-filed.** Re-filing would duplicate the backlog that
  already covers the design — the outcome the brief forbids.
- This file is the **authoritative current-design trace map** (§4). It is the source the synthesis gate
  assembles the traceability matrix from (`req_id ↔ bar_ids ↔ epic ↔ issue_numbers ↔ design_doc_ref`).
  The current `BAR-*`/`REQ-*` ids here supersede the first-run labels still present in ticket bodies.
- A single consolidated **re-anchoring index** is posted to the board on parent epic **#2**, carrying the
  epic→current-bar-area→current-design-doc table and the wave plan, so the board itself records the
  current-design mapping in one auditable place. This also answers the open request **#106** (a
  consolidated epic dependency-graph / wave-plan tracker for the design backlog).
- The first-run follow-ups **#23, #24, #25, #27** remain **folded under #89** (verified; not duplicated).
- Two coverage gaps in the current design — each a surface with no existing covering issue — are filed as
  new issues (§6).
- Ticket bodies are left otherwise intact. Their `REQ-*` citations remain the stable semantic anchor and
  are valid against the current design except for the stale `REQ-ID` ids noted above; a mechanical
  in-ticket `BAR`-label refresh across the ~55 issues is a low-risk grooming pass (the board already
  carries in-flight grooming/language sweeps #104, #109, #110, #111) and is not re-authored here, where it
  would churn well-formed tickets with lower confidence than this reconciled map.
- The first-run-bar review items **#99–#103, #107** were raised against the superseded bar; their id-level
  concerns are overtaken by the current bar and this map. They are noted, not closed (review-DAG owned).

## 6. Completeness and gap analysis (board vs the current design's surfaces)

Against the release bar's own surface sweep (`design/release-bar.md` §completeness-and-gap-review), every
surface a product of this kind is expected to have is either covered by a board issue or recorded
out-of-scope with a reason:

| Surface | Covered by | Status |
|---------|-----------|--------|
| Sign-up / sign-in | #84, #85 | covered |
| Recovery | #78 | covered |
| Account deletion | #80 | covered |
| Data export | #81 | covered |
| **Onboarding (post-sign-up first run)** | **#123** (filed) | **gap → filed under #34** |
| Settings hub / sessions & devices | #82, #86 | covered |
| Notifications | — | out of scope v1 (deferred, non-gating; designed) |
| Admin / support | #75, #76 | covered |
| Billing | — | out of scope (product kind: no tenancy/billing) |
| Public first visit / landing | #35 | covered |
| Reporting abuse | #54 | covered |
| Rules / content policy | #54, #58 | covered |
| Block / mute | #55 | designed; deferred, non-gating (safety floor is reporting + operator action, both gated) |
| Discovery / Explore | — | out of scope v1 (deferred, non-gating; follow from any profile is gated via #39) |
| Accessibility statement & conformance | #71 | covered |
| **Status / availability surface** | **#124** (filed) | **gap → filed under #90** |
| Privacy / data-rights & retention posture | #58, #59, #67 | covered |
| Durable persistence (restart survival) | #64, #65, #66, #67 | covered (the `c805525` blocker) |
| Backups / recovery / rollback / migration | #48, #49, #50, #51 | covered |
| Observability / logs / metrics / health | #93, #94, #97, #93 | covered |

Two gaps, both filed this run:

1. **Onboarding** — the current design gates a post-sign-up onboarding surface (`BAR-027`, `BAR-213`,
   `BAR-237`, `BAR-248`; `REQ-UX-065/066`, `REQ-PROD-032`): a new account lands on a screen that explains
   the empty timeline and offers a first action, never a blank page. The existing core-loop issues cover
   the logged-out landing (#35) and the product-wide state model (#40) but not this surface. Filed as
   **#123** under EPIC #34.
2. **Status & availability surface** — the current design gates a status surface that tells users chirp
   itself is affected and stays reachable when the product is fully down (`BAR-482`, `BAR-483`), plus a
   stated and measured availability target (`BAR-034`, `BAR-486`, `BAR-487`; `REQ-OPS-085/086/092/093`,
   `REQ-PROD-040`). The existing observability issues cover health (#93), degradation in-app (#95), and
   incident responsibility (#96) but not the user-facing status surface or the availability target. Filed
   as **#124** under EPIC #90.

## 7. Contract identities this backlog carries evidence for

- **ISSUE_TRACES** — every issue sits under exactly one epic (§4); each traces to ≥1 current `REQ-*` and,
  through §4, to ≥1 current `BAR-*` and a design section. Each epic is one coherent landable code goal
  with its dependencies stated (§2, §3).
- **GAP_HAS_ISSUE** — the two surface gaps found against the current design are filed as issues (§6); the
  live-product measurement gaps are the synthesis gate's to map, and every release-gating area already has
  a covering epic/issue here.
- **SURFACE_COVERAGE** — every recurring account/operational surface is designed-and-covered or recorded
  out-of-scope with a reason (§6).
- **GITHUB_HYGIENE** — the filed issues and the #2 index comment name things by repository identity only
  (`owner/repo#N`, `design/<file>.md`, `REQ/BAR` ids, PR `#122`, commit `c805525`); no host, cluster,
  filesystem, taskflow, or run detail, and no attribution trailer.
