# CONCERN_COVERAGE and SURFACE_COVERAGE — coverage inspection over the chirp design set

Repository: `Nousix-LLC/nswe-demo`. Design set under review: the five area designs plus the release
bar, as they will land in the repository at `design/*.md`, and the delivery backlog on the project board.
This spoke owns exactly two identities — `CONCERN_COVERAGE` and `SURFACE_COVERAGE` — and asserts no other.
It builds no matrix columns. It reads completed inputs only and reports findings; it edits nothing.

**Scope note (recorded limitation).** The `design` methodology loader was unavailable for this run
(`agent_domain_unset`), as it was for every sibling gate. This inspection applies the principal-product-
designer judgment and the relayed Release Definition guidance (CompletenessAndGapReview, ReleaseBar) by
prose. The limitation did not block the work: coverage is a look-up against the enumerated concern and
surface lists, and the evidence below is grounded in the design set, not in the loader.

**Method.** For each of the six brief concerns, and for each enumerated account/operational surface, the
disposition is one of: *covered/designed* (with the design file or release-bar judgment that holds it,
cited by repo-relative path, section, and `REQ-*`/`BAR-*` id), or *out of scope with a reason* (the
recorded reason). A concern or surface that is neither designed nor consciously scoped out would be a
`FAIL` with specifics. None was found.

---

## CONCERN_COVERAGE

**Statement (inherited, verbatim):** "Each of the six brief concerns is covered by a design file OR
recorded out-of-scope with a reason."

**Verdict: PASS.** All six brief concerns — the six bulleted "Concerns to cover" in the DAG root brief —
are covered by a design artifact. None is absent; none is out of scope (and so none required an
out-of-scope reason here).

| # | Brief concern | Disposition | Covering design artifact and evidence |
|---|---------------|-------------|----------------------------------------|
| 1 | Product scope & requirements | Covered | `design/product-requirements.md` — §1 Product definition & kind, §2 Users & personas, §3 End-to-end journeys (incl. J1 first visit through J10 self-host), §4 Requirements & acceptance criteria (`REQ-PROD-*`), §5 In scope / out of scope with reasons. |
| 2 | Domain & application design | Covered | `design/domain-application-design.md` — §Domain model, §Modules and responsibilities, §Persistence requirement (the in-memory store is named as the blocker; durable persistence required), §Interfaces and entry points; `REQ-DOM-*` (domain 001–049, persistence 100–149, modules/interfaces 200–249). |
| 3 | User experience & visual design | Covered | `design/experience-design.md` — §Information architecture and interaction model, §Screens and flows (screen inventory, landing, sign-up/in/out, home timeline, profiles), §Empty, loading, and error states, §Visual language and design system (design tokens), §Responsive layout, §Accessibility; `REQ-UX-*`. |
| 4 | Identity, security & trust | Covered | `design/identity-security.md` — §Accounts and lifecycle, §Authentication and sessions, §Authorization, §Abuse and privacy basics, §Threat model; `REQ-ID-*`. |
| 5 | Operational readiness for release | Covered | `design/operational-readiness.md` — §durable_data, §backups_and_recovery (cadence, retention, RPO/RTO, restore drills), §limits_and_quotas, §observability (incl. operator/administrative audit trail), §status_and_incident; `REQ-OPS-*`. Existing follow-ups #23/#24/#25 folded in, not duplicated. |
| 6 | The plan (epics & work-items) | Covered | The delivery backlog on the project board — epic index, wave/dependency order (waves 0–4: durable persistence and self-hostable build first, release-bar concerns after), and the `REQ/BAR → (epic, issue)` trace map (EPIC #56, #89, #83, #34, #43, #77, #72, #53, #44, #90, #52). Delivery staging is also stated in `design/release-bar.md` §MVP-vs-releasable scoping. |

**Findings.** Each concern maps to exactly one primary design artifact, with no concern unowned and no
concern left to synthesis to discover. Concern 6 (the plan) is the one concern whose artifact is the
project board rather than a `design/*.md` file; this is by design — the brief names the plan as "epics and
work-items … on the project board" — and the board's epic index, wave order, and trace map carry it, with
the release bar's scoping section stating the same usable-early-then-releasable ordering. No concern is
absent and none is consciously out of scope, so no `FAIL` and no out-of-scope reason applies.

---

## SURFACE_COVERAGE

**Statement (inherited, verbatim):** "Every recurring account/operational surface (sign-up/in/recovery,
account deletion, data export, onboarding, settings, notifications, admin/support, billing) is designed OR
recorded out-of-scope with a reason."

**Verdict: PASS.** All ten enumerated surfaces have an explicit disposition. Eight are designed and gated;
two (notifications, billing) are recorded out of scope with a stated reason. The release bar's
Completeness-and-gap review (`design/release-bar.md` §Completeness and gap review → Account and operational
surfaces) is the authoritative sweep where each surface's in/out-of-scope judgment and `BAR-*` refs are
recorded; the area designs below are where each in-scope surface is actually designed.

| Surface | Disposition | Designed where (area design) + bar judgment / reason |
|---------|-------------|--------------------------------------------------------|
| Sign-up | Designed · in scope | `design/identity-security.md` §Accounts and lifecycle → Sign-up (`REQ-ID-002/004/006`, secret est. at sign-up `REQ-ID-030`); `design/experience-design.md` §Screens and flows → Sign up `/signup` (`REQ-UX-041/043`). Bar: in scope — `BAR-007`, `BAR-008`, `BAR-231`, `BAR-232`, `BAR-303`, `BAR-321`. |
| Sign-in | Designed · in scope | `design/identity-security.md` §Authentication and sessions (`REQ-ID-031/032/035/037`); `design/experience-design.md` → Sign in `/signin` (`REQ-UX-044/045`). Bar: in scope — `BAR-009`, `BAR-010`, `BAR-233`, `BAR-300`, `BAR-304`, `BAR-305`. |
| Recovery | Designed · in scope (releasable) | `design/identity-security.md` §Accounts and lifecycle → Recovery (`REQ-ID-013..016`: self-service, gated on proven contact control, resists non-owners, ends prior sessions); `design/experience-design.md` recovery flow (`REQ-UX-047`, interlinked with sign-in `REQ-UX-015`). Bar: in scope — `BAR-015`, `BAR-234`, `BAR-321`–`BAR-324`. |
| Account deletion | Designed · in scope (releasable) | `design/identity-security.md` §Leaving: export and deletion (`REQ-ID-020..024`: self-service, confirmed, defined outcome for content/handle, private data erased, sessions ended); `design/experience-design.md` → Delete account `/settings/delete`. Bar: in scope — `BAR-020`–`BAR-022`, `BAR-118`, `BAR-255`, `BAR-327`–`BAR-329`, `BAR-407`. |
| Data export | Designed · in scope (releasable) | `design/identity-security.md` export (`REQ-ID-017..019`: portable form, scoped to requester, excludes secrets); `design/experience-design.md` → Export your data `/settings/export`. Bar: in scope — `BAR-019`, `BAR-119`, `BAR-147`, `BAR-254`, `BAR-325`, `BAR-326`, `BAR-411`. |
| Onboarding | Designed · in scope | `design/experience-design.md` §Account lifecycle → Onboarding `/welcome` (`REQ-UX-014`: fresh sign-up lands on onboarding, never a blank page). Bar: in scope — `BAR-027`, `BAR-213`, `BAR-237`, `BAR-248`. |
| Settings | Designed · in scope | `design/identity-security.md` §Managing the account (account settings surface `REQ-ID-008`, sessions/devices `REQ-ID-010`); `design/experience-design.md` → Settings hub `/settings` and sub-sections (profile, account & contact, sessions & devices, export, delete) (`REQ-UX-017`). Bar: in scope — `BAR-017`, `BAR-018`, `BAR-214`, `BAR-249`–`BAR-252`, `BAR-317`–`BAR-320`. |
| Notifications | Out of scope for v1 — designed, deferred, with reason | A baseline notifications story IS designed: `design/experience-design.md` → Notification preferences `/settings/notifications` and §Safety, notifications, and public-explanatory surfaces → Notifications; `REQ-UX-019/072/078`, `REQ-ID-011`. Reason recorded in `design/release-bar.md` sweep: every area marks it non-gating, so the release does not gate on it; it is a stated near-term fast-follow, and the settings notification-preferences row ships only where notifications ship. Absence at release is a decision, not an oversight. |
| Admin / support | Designed · in scope (releasable) | Operator surface: `design/operational-readiness.md` §observability → Operator and administrative audit trail, plus `design/identity-security.md` (least-privilege operator that cannot impersonate users or read credentials). User-facing help & support: `design/experience-design.md` §Safety, notifications, and public-explanatory surfaces. Bar: in scope — `BAR-025`, `BAR-258`, `BAR-331`–`BAR-333`, `BAR-335`, `BAR-468`. |
| Billing | Out of scope — by product kind, with reason | `design/release-bar.md` sweep records the reason: chirp is a single public consumer product of individual accounts where no money changes hands; tenancy, team/seat management, org-admin, and billing are an explicit non-goal (`need: no-tenancy-or-billing`). There is no billing surface to design, so none is gated. Corroborated by `design/product-requirements.md` §5 Out of scope. |

**Findings.**
- Every enumerated surface resolves to an explicit judgment; none is simply absent. The eight in-scope
  surfaces are each designed in an area design and held by at least one `BAR-*`; the two out-of-scope
  surfaces each carry a stated reason in the bar's sweep.
- The two out-of-scope surfaces are of two different kinds, and both are sound: **billing** is out by
  product kind (no money changes hands — a structural non-goal, nothing to design), while **notifications**
  is designed and deferred (a conscious v1 scoping decision resting on every area marking it non-gating,
  recorded as a near-term fast-follow). Neither is a hole.
- The bar's sweep also records judgments for additional product-kind surfaces beyond the enumerated ten
  (landing/first visit, reporting abuse, rules/content policy, block/mute [deferred], discovery/Explore
  [deferred], sessions & devices, accessibility statement, status/incident, privacy/data-rights). These
  are outside this identity's enumerated set but confirm the sweep was deliberate and complete; they are
  noted, not asserted here.

---

## Summary

| Identity | Verdict | Basis |
|----------|---------|-------|
| `CONCERN_COVERAGE` | **PASS** | All six brief concerns covered by a design artifact (five area design files + the board backlog / bar scoping for the plan). None absent; none out of scope. |
| `SURFACE_COVERAGE` | **PASS** | All ten enumerated surfaces have explicit dispositions: eight designed and gated; notifications and billing out of scope, each with a stated reason. No surface is absent. |

No `FAIL`, no absent concern or surface, and no silent "covered" treatment. Nothing above required editing
the designs or the bar; every disposition is a read against completed, immutable inputs.
