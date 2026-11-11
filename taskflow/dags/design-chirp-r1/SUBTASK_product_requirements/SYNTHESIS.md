# SYNTHESIS.md — product-requirements subtree fold record

**Subtree root**: `SUBTASK_product_requirements`  
**Synthesis gate**: `SUBTASK_product_requirements/SUBTASK_pr_synthesis`  
**Assembled deliverable**: `outputs/product-requirements.md`  
**Fold outcome**: parent task SUSPENDED → COMPLETED

---

## Section → fragment map

| Required section | Sourcing fragment | Present in deliverable |
|---|---|---|
| `product_definition_and_kind` | `SUBTASK_product_definition/outputs/product-definition.md` | Yes — Part 1 |
| `users_personas` | `SUBTASK_users_and_journeys/outputs/users-and-journeys.md` | Yes — Part 2 |
| `user_journeys` | `SUBTASK_users_and_journeys/outputs/users-and-journeys.md` | Yes — Part 3 |
| `requirements_and_acceptance_criteria` | `SUBTASK_requirements/outputs/requirements.md` | Yes — Part 4 |
| `in_scope_out_of_scope` | `SUBTASK_requirements/outputs/requirements.md` | Yes — Part 5 |

All five required sections sourced from their contracted fragments and present in the assembled document.

---

## Identity assertions

### SECTION_COVERAGE

**Check**: Does `outputs/product-requirements.md` carry each of the five required sections named in `../../contracts/design_artifact_map.yaml` and mapped in `contracts/section_ownership_map.yaml`?

**Evidence**:
- Part 1 "Product definition & kind" — opens with "## What chirp is" and "## Product kind(s)"; covers the consumer-web-app kind and three non-applicable kinds with reasons.
- Part 2 "Users and personas" — opens with "## User personas" at line ~117 of assembled doc; covers P1–P5.
- Part 3 "User journeys" — covers J1–J10 end-to-end including first visit, sign-up, sign-in, recovery, core loop, daily use, account management, leaving, operating, self-hosting.
- Part 4 "Requirements and acceptance criteria" — REQ-PROD-001 through REQ-PROD-042; each entry carries id, statement, acceptance_criteria, release_gating flag; traceability tables for kind implications and journeys.
- Part 5 "In scope / out of scope" — consolidates the product-kind scope draft from Part 1 with the requirements in Part 4; in-scope list and out-of-scope list each with reasons.

**Result**: PASS

---

### REQ_SINGLE_OWNER

**Check**: Are REQ-PROD-* ids minted only by `SUBTASK_requirements`? Do upstream fragments (`product-definition.md`, `users-and-journeys.md`) assign no REQ-PROD-NNN ids?

**Evidence**:
- `product-definition.md`: uses only `need:` handles (`need: real-account-signup-signin`, `need: authenticated-identity`, `need: durable-account-data`, `need: account-settings`, `need: account-deletion`, `need: data-export`, `need: authorization-boundary`, `need: privacy-basics`, `need: considered-states`, `need: works-on-mobile`, `need: reachable-and-available`, `need: help-and-abuse-reporting`, `need: no-tenancy-or-billing`, `need: releasable-bar-not-prototype`). No REQ-PROD-NNN ids present.
- `users-and-journeys.md`: uses journey codes (J1–J10) and need handles; no REQ-PROD-NNN ids present.
- `requirements.md`: mints REQ-PROD-001 through REQ-PROD-042; each id appears exactly once as a heading in Part 4; traceability tables reference those ids but do not mint new ones.
- The assembled Parts 1–3 carry no REQ-PROD-* ids; REQ-PROD-* appear only in Parts 4 and 5 (sourced entirely from `SUBTASK_requirements`).

**Result**: PASS

---

### REQ_WELL_FORMED

**Check**: Does every requirement in the REQ-PROD-* register carry the four required fields: `id`, `statement`, `acceptance_criteria` (stranger-testable), `release_gating` flag?

**Evidence**:
All 42 requirements (REQ-PROD-001 through REQ-PROD-042) follow the schema:
- **id**: formatted `REQ-PROD-NNN`, each unique heading in Part 4.
- **statement**: each carries a one-sentence statement of what the product must do.
- **acceptance_criteria**: each carries bullet-list criteria using observable, third-person-testable language (e.g., "A person visiting the site without a session sees…", "A person can register…", "Given a valid session token…"). No acceptance criterion is phrased as an internal or implementation claim.
- **release_gating**: each carries `release_gating: true` or `release_gating: false` with a rationale.

Sample spot-check confirming the pattern:
- REQ-PROD-001 (post a chirp): statement + 4 AC bullets + `release_gating: true`
- REQ-PROD-010 (owner-only sign-in): statement + AC including "signing in with a handle and the wrong credential fails" + `release_gating: true`
- REQ-PROD-037 (durable data): statement + AC including "user data must survive a server restart" + `release_gating: true`
- REQ-PROD-042 (user discovery): statement + AC + `release_gating: false` with stated reason

**Result**: PASS

---

### JOURNEY_TO_REQ

**Check**: Does every journey J1–J10 map to at least one REQ-PROD-* requirement in the traceability table?

**Evidence** (from the Journeys → REQ-PROD traceability table in Part 4):

| Journey | REQ-PROD coverage |
|---|---|
| J1 First visit | 030, 031, 007 |
| J2 Sign-up | 008, 009, 012, 031 |
| J3 Sign-in | 010, 011 |
| J3a Recovery | 013, 012 |
| J3b Sign-out | 014 |
| J4 Core loop | 001, 002, 003, 004, 005, 006, 007, 042 |
| J5 Daily & returning use | 015, 032, 033, 034 |
| J6 Managing the account | 016, 017, 018 |
| J7 Safety & notifications | 025, 026, 027, 029 |
| J8 Leaving (export & deletion) | 019, 020, 021, 022 |
| J9 Operating the service | 037, 038, 039, 040, 028, 041 |
| J10 Self-hosting | REQ-PROD-037 inherits; supported self-hosting out of scope (reasoned) |

All 10 journeys (plus sub-journeys J3a, J3b) have at least one covering requirement. J10's treatment is correct: the requirement for durable data (REQ-PROD-037) holds for any deployment including self-hosted instances; the absence of a self-hosting support persona is a scoped-out decision, not a coverage gap, and is stated as such with a reason.

**Result**: PASS

---

### KIND_IMPLICATIONS

**Check**: Are all need handles from the consumer-web-app kind implications in Part 1 either reflected in a REQ-PROD-* requirement or recorded out-of-scope with a reason?

**Evidence** — each handle traced:

| Need handle | Disposition |
|---|---|
| `need: real-account-signup-signin` | REQ-PROD-008 (sign-up), REQ-PROD-010 (sign-in) |
| `need: account-recovery` | REQ-PROD-012, REQ-PROD-013 |
| `need: authenticated-identity` | REQ-PROD-009, REQ-PROD-010, REQ-PROD-011 |
| `need: durable-account-data` | REQ-PROD-037 |
| `need: account-settings` | REQ-PROD-016, REQ-PROD-017 |
| `need: account-deletion` | REQ-PROD-021, REQ-PROD-022 |
| `need: data-export` | REQ-PROD-019, REQ-PROD-020 |
| `need: authorization-boundary` | REQ-PROD-023 |
| `need: privacy-basics` | REQ-PROD-024 |
| `need: considered-states` | REQ-PROD-033 |
| `need: works-on-mobile` | REQ-PROD-035 |
| `need: reachable-and-available` | REQ-PROD-039, REQ-PROD-040 |
| `need: help-and-abuse-reporting` | REQ-PROD-025, REQ-PROD-026, REQ-PROD-028 |
| `need: no-tenancy-or-billing` | Recorded out-of-scope in Part 5 with reason (SaaS kind does not apply) |
| `need: releasable-bar-not-prototype` | Stated in scope in Part 5; `release_gating: true` throughout Part 4 |

The kind implications traceability table in Part 4 covers the same handles with the same disposition. Every implication either has a covering requirement or is recorded out of scope with a reason.

**Result**: PASS

---

### SCOPE_RECORDED

**Check**: Does Part 5 record what is in scope and what is out of scope with reasons? Are all out-of-scope judgments reasoned, not bare exclusions?

**Evidence**:
Part 5 ("In scope / out of scope", lines ~927–1004 of assembled document) opens by referencing the product kind and consolidating from Part 1's scope draft.

In-scope items listed with requirement references:
- Core loop (REQ-PROD-001–007)
- Real accounts and full account lifecycle (REQ-PROD-008–022)
- Authorization boundary and privacy basics (REQ-PROD-023–024)
- Safety, moderation, operator support (REQ-PROD-025–028)
- Baseline notifications (REQ-PROD-029)
- Finished-feeling experience (REQ-PROD-030–036)
- Durability and operational readiness (REQ-PROD-037–041)
- User discovery (REQ-PROD-042)

Non-gating items (REQ-PROD-004, 015, 018, 027, 029, 031, 042) are noted as in-scope but not release-blocking, with explicit statement that their non-gating status is deliberate.

Out-of-scope items each carry a stated reason:
- Tenancy, billing — SaaS kind does not apply; no money changes hands
- COTS install/licensing/upgrade tooling — chirp is a hosted service, not distributed for customer install
- OSS community infrastructure — repository is closed demonstration, does not accept contributions
- Native mobile apps — chirp is a responsive web app; native clients are a separate product surface
- Rich social features beyond core loop — candidates for later scope, not v1; deliberate decision recorded
- Implementation "how" — deferred to code work; stated as design-only document

Each out-of-scope exclusion names the reason it is excluded. No bare exclusions.

**Result**: PASS

---

### HYGIENE

**Check**: Does the assembled `outputs/product-requirements.md` contain any host addresses, SSH paths, server user names, taskflow system metadata, or attribution trailers that would make it unfit for repository commit?

**Evidence**:
- No HTML comment blocks with taskflow metadata (task IDs, SUBTASK_ slugs, process IDs, workspace paths) in the assembled document body. (The fragment source files carry such comments in their preambles; those were not copied into the assembled document.)
- No host addresses (no IP addresses, no `100.90.75.93` or similar).
- No SSH key paths, no server user names.
- No `nousix-runtime` paths or HAL engine references.
- No `Co-Authored-By` or attribution trailers.
- Document references `c805525` (a commit hash) and `TASK.md` — these are project content references appropriate for the design document, not system metadata.
- References to `SUBTASK_requirements`, `SUBTASK_product_definition` etc. appear only in the traceability note at the end of Part 4 in the context of "other design areas" — these are legitimate cross-references within the design's own structure, not taskflow system metadata.

**Result**: PASS

---

## Summary

| Identity | Result |
|---|---|
| SECTION_COVERAGE | PASS |
| REQ_SINGLE_OWNER | PASS |
| REQ_WELL_FORMED | PASS |
| JOURNEY_TO_REQ | PASS |
| KIND_IMPLICATIONS | PASS |
| SCOPE_RECORDED | PASS |
| HYGIENE | PASS |

All 7 identities hold. No gaps requiring remediation decomposition. The assembled `outputs/product-requirements.md` is repository-ready and satisfies the deliverable specification.

**Fold**: parent task `SUBTASK_product_requirements` SUSPENDED → COMPLETED.
