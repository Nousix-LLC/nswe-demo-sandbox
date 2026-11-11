# _GLOBAL.md — SUBTASK_identity_trust (identity, security & trust subtree hub)

## Project Context

**Status**: Active

### Objective

Design the **identity, security & trust** surface a releasable, publicly-exposed chirp needs, stated **as
requirements** (`REQ-ID-*`) plus the **threat model** the surface implies, to the bar **real auth, not a stub;
sessions safe to expose publicly**. The single deliverable is `design/identity-security.md` (produced at
`SUBTASK_identity_trust/outputs/identity-security.md`), with the six required sections the parent contract fixes
and a `REQ-ID-*` register whose every entry is testable and traces to `REQ-PROD-*`.

This subtree writes **design, not product code**. Every topic with an engineering "how" (password hashing,
token formats, SSO protocol flows, session stores, rate-limiter internals) is stated here as a **requirement
with a testable bar** and the implementation "how" is deferred to later code DAGs in the `software` domain.

This node (`SUBTASK_identity_trust`) decomposed because its brief enumerates five distinct concerns that are a
clean hub-and-spoke fan-out: four parallel requirement clusters (accounts & lifecycle; authentication &
sessions; authorization; abuse & privacy) and a threat model that integrates all four as the synthesis. The
authoritative task spec is this directory's `_BRIEF.md`.

### Scope

**In Scope:**
- The five identity/security/trust concerns, each carried to testable `REQ-ID-*` requirements with release-gating
  flags: accounts & lifecycle, authentication & sessions, authorization, abuse & privacy basics, threat model.
- The account-lifecycle surfaces a releasable account-based product needs (sign-up that establishes a real
  credential; owner-only sign-in; verified-contact recovery; server-side sign-out; profile/settings; data export;
  account deletion with a defined, confirmed outcome) — designed as `REQ-ID-*`, each tracing to its `REQ-PROD-*`.
- The authority model (who may see/change what) and the privacy/data-rights basics for a public social product.
- A threat model that names the threats chirp's public surface implies and what the design answers for each.

**Out of Scope:**
- Implementing auth, sessions, credentials, or crypto — deferred to code DAGs (reach the `software` domain by
  prose where a "how" is tempting).
- Any `REQ-*` area other than `REQ-ID-*` (do not mint `REQ-PROD-*`, `REQ-DOM-*`, `REQ-UX-*`, `REQ-OPS-*`, `BAR-*`).
- Tenancy/organizations/billing and SSO-for-enterprise-tenants as a tenancy feature — chirp is a single public
  product of individual accounts (product-requirements Part 1/5). Whether **optional** social-login or MFA is in
  scope *for the bar* is a decision the authentication spoke must state with its reason, not assume.
- Any repo/cluster/namespace other than `Nousix-LLC/nswe-demo` (+ read-only use of the live deployment).

### Success Criteria

- [ ] Every required section of `design/identity-security.md` is present (accounts_and_lifecycle,
      authentication_and_sessions, authorization, abuse_and_privacy_basics, threat_model,
      requirements_and_acceptance_criteria) — per `../contracts/design_artifact_map.yaml`.
- [ ] Real authentication, sessions safe to expose publicly, and an authorization model are specified **as
      requirements, not stubs**; account lifecycle incl. recovery, deletion, and data export is covered.
- [ ] A threat model and the abuse/privacy basics are stated, the threat model derived from the other four areas.
- [ ] Every `REQ-ID-*` has a statement, testable acceptance criteria, a `release_gating` flag, a verification
      method from the schema vocabulary where it anchors a bar, and traces to ≥1 `REQ-PROD-*`.
- [ ] The `REQ-ID-*` id scheme and the parent traceability schema are **composed against, not redefined**.

---

## Constraints and Requirements

### Process Constraints
- **Scope**: `Nousix-LLC/nswe-demo` only — read-only use of the repo (`@ c805525`) and the live deployment to
  measure the current auth/session surface. Touch nothing else.
- **Requirements/threat-model only — no implementation.** Do not design password hashing, token formats, SSO
  protocol internals, session storage, or rate-limiter mechanics. State *what must be true from the user's /
  operator's / attacker's side* and defer the "how" to code DAGs by prose.
- **One owning file, one id area.** This subtree owns exactly `design/identity-security.md` and the `REQ-ID-*`
  area. Id ranges are partitioned across children by `contracts/req_id_partition.yaml` so children never collide.

### Repository-ready hygiene (binding on the deliverable `identity-security.md`)
The deliverable is written for the repository's readers and carries **no** host/system/taskflow detail: no host
or cluster addresses, no filesystem or taskflow paths, no agent/DAG/run ids, no `SYNTHESIS.md` locations, no
attribution footers. Name things by repository identity (`owner/repo`, repo-relative path, commit SHA). These
workspace files (`_GLOBAL.md`, briefs, `contracts/`) are internal and may reference workspace paths; the **output
document must not**.

### Writing voice (binding on all prose in the deliverable)
Plain, human, checkable. No moral/character adjective on a thing that cannot hold character ("honest" metric,
"genuine" durability); no narrated candor ("to be honest", "let's be clear"); name both halves of any contrast or
drop it; no slot-fill templates ("a [X] step toward [Y]", "in today's [world]", "at its core"); keep real counts,
don't pad to triads; drop hollow filler (*seamless*, *robust*, *comprehensive*, *leverage*, *utilize*, *in order
to*, stacked *Moreover/Furthermore/Additionally*). Judge by cluster and density, not single words. Each child runs
this pass over its partial; the synthesis runs it over the assembled document before finalizing.

---

## Input Specifications

| Source | Identity / path | Role |
|--------|-----------------|------|
| This subtree hub | `SUBTASK_identity_trust/_GLOBAL.md` | Shared context/constraints (this file) |
| This subtree contract | `SUBTASK_identity_trust/contracts/` (read-only) | `REQ-ID-*` range partition, section→owner map, partial-output format, identities |
| Parent contract | `taskflow/dags/design-chirp-r1/contracts/` (read-only) | `REQ-ID-*` format, `release_gating`, verification-method vocabulary, traceability schema, design-artifact map — **compose against, do not redefine** |
| Product requirements | `taskflow/dags/design-chirp-r1/SUBTASK_product_requirements/outputs/product-requirements.md` | `REQ-PROD-*` register, personas, journeys — the user-side needs identity must answer and the trace targets |
| Repository | `Nousix-LLC/nswe-demo` @ `c805525` | Current auth/session surface: handle-only sign-in, server-issued session token, in-memory store (nothing durable), no recovery/sign-out/settings/deletion/export |
| Live deployment | ArgoCD app `chirp` (read-only) | Exercise the current identity surface to ground "state today" observations |

### The two findings the identity design must close (from product-requirements)
- **Handle-only authentication (critical).** Signing in = typing a handle; the server opens a session for it. No
  password, no credential, no verification — anyone who knows a handle can sign in as that account. Breaks the
  core premise *this person said this*. (`REQ-PROD-008`, `REQ-PROD-010`, `REQ-PROD-011`.)
- **No session hygiene.** No server-side sign-out/invalidation, no expiry story, no recovery, no account
  settings, no deletion, no export. (`REQ-PROD-012`–`022`, `REQ-PROD-024`.) The in-memory store losing sessions
  on restart is a `REQ-DOM-*`/`REQ-OPS-*` concern but shapes the session-durability requirement here.

---

## Methodology

Bundle IDs (from the brief's Domain Mapping): **Identity and Trust** (primary — accounts & authentication incl.
SSO/MFA, authorization & multi-tenancy, privacy/data-rights & compliance); **Product Strategy**, **Release
Definition**, **Product Surfaces** (supporting). Each executing child names the bundle ID(s) its concern maps to;
the child loads full bundle content on demand. (Note: in this reconstructed node the methodology surface is
unbound; children apply the principal-product-designer posture and the named bundle IDs.)

---

## Task Structure

### Overview

```
SUBTASK_identity_trust/
├── _GLOBAL.md                               (this hub)
├── contracts/                               (READ-ONLY for descendants)
│   ├── _MANIFEST.yaml                       (kind, ownership, identities, derived artifacts)
│   └── req_id_partition.yaml                (REQ-ID range partition + section→owner map + partial format)
├── SUBTASK_accounts_lifecycle/_BRIEF.md
├── SUBTASK_auth_sessions/_BRIEF.md
├── SUBTASK_authorization/_BRIEF.md
├── SUBTASK_abuse_privacy/_BRIEF.md
└── SUBTASK_synthesis/_BRIEF.md              (Task Kind: synthesis — threat model + assembly + verification)
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_accounts_lifecycle` | none | The account object and its full lifecycle **as requirements**: sign-up that establishes a real credential, verified-contact recovery, profile edit, account-settings surface, data export, account deletion with a defined+confirmed outcome, handle-change policy. REQ-ID range 001–029. Section: `accounts_and_lifecycle`. | `outputs/accounts-lifecycle.md` |
| `SUBTASK_auth_sessions` | none | Real authentication and publicly-safe sessions **as requirements**: what "real auth" must mean, credential strength expectations (stated, not crypto-how), session issuance/expiry/invalidation/sign-out safe on the public internet, stay-signed-in on a trusted device, and an explicit in/out-of-scope decision on MFA and social-login with reasons. REQ-ID range 030–059. Section: `authentication_and_sessions`. | `outputs/auth-sessions.md` |
| `SUBTASK_authorization` | none | The authority model **as requirements**: a person acts only as themselves and changes only their own account/content; the public-vs-private field boundary; the authority model for the supported operator/admin/support actions (who may do what, under what authorization). REQ-ID range 060–079. Section: `authorization`. | `outputs/authorization.md` |
| `SUBTASK_abuse_privacy` | none | Abuse-resistance and privacy/data-rights basics **as requirements**: reporting, stated rules/terms, block/mute, rate/volume limits as a first line against abuse (coordinate with `REQ-OPS-*`, do not mint it), data minimization, private-field protection, retention/erasure on deletion, lawful-basis/data-rights baseline proportionate to a public microblog. REQ-ID range 080–099. Section: `abuse_and_privacy_basics`. | `outputs/abuse-privacy.md` |
| `SUBTASK_synthesis` | `SUBTASK_accounts_lifecycle`, `SUBTASK_auth_sessions`, `SUBTASK_authorization`, `SUBTASK_abuse_privacy` | **Synthesis gate + assembly.** Read the four partials; author the `threat_model` section (STRIDE-style over chirp's public surface, derived from the four areas) incl. any threat-driven `REQ-ID-*` (range 100–119); assemble the single `identity-security.md` with all six required sections and the consolidated `requirements_and_acceptance_criteria` register; verify the contract identities with recorded evidence (unique ids in range, every REQ-ID testable + gating + traces to ≥1 REQ-PROD, coverage of all REQ-PROD identity needs, no schema redefinition, repo hygiene, writing-voice pass); remediate gaps by decomposing, never silent-plug. | `outputs/identity-security.md`, `SYNTHESIS.md` |

### Dependency Graph (human-readable; the table above is authoritative)

```
SUBTASK_accounts_lifecycle ─┐
SUBTASK_auth_sessions ──────┤
SUBTASK_authorization ──────┼──> SUBTASK_synthesis ──> (folds SUBTASK_identity_trust: outputs/identity-security.md)
SUBTASK_abuse_privacy ──────┘
```

The four spokes carry **no dependency edge on `SUBTASK_product_requirements`** (it is already COMPLETED; the
forward-only amendment rule forbids depending on completed work). They read its output directly as a declared
input file, which already exists.

---

## Contract

**Contract location**: `contracts/` (read-only for every descendant)
**Contract kind**: `yaml_schema` (extends the parent `yaml_schema`; additive only, never overriding)

### Inherited Contracts

| Ancestor contract | Path | What it binds here |
|---|---|---|
| design-chirp-r1 root | `taskflow/dags/design-chirp-r1/contracts/id_and_traceability_schema.yaml` | `REQ-<AREA>-NNN` format; `ID` area owner = this subtree; each requirement's required fields; `BAR-*`/verification-method vocabulary; traceability-matrix columns |
| design-chirp-r1 root | `taskflow/dags/design-chirp-r1/contracts/design_artifact_map.yaml` | `design/identity-security.md` owner + its six required sections |
| design-chirp-r1 root | `taskflow/dags/design-chirp-r1/contracts/_MANIFEST.yaml` | one-owner-per-file, concern-coverage, surface-coverage identities |

This subtree **extends** these (partitions the `REQ-ID` number space across children, fixes the partial-output
format and the final-file owner, adds subtree identities). It **MUST NOT** redefine the id format, the required
fields, the verification vocabulary, or the design-artifact map.

### Structural Declarations
- `contracts/req_id_partition.yaml` — per-child `REQ-ID-NNN` number range, the section each child owns in the
  final document, and the markdown partial-output format each spoke writes.

### Ownership (one producer per artifact)

| Artifact | Owning subtask |
|---|---|
| `SUBTASK_accounts_lifecycle/outputs/accounts-lifecycle.md` (+ `REQ-ID-001..029`, section `accounts_and_lifecycle`) | `SUBTASK_accounts_lifecycle` |
| `SUBTASK_auth_sessions/outputs/auth-sessions.md` (+ `REQ-ID-030..059`, section `authentication_and_sessions`) | `SUBTASK_auth_sessions` |
| `SUBTASK_authorization/outputs/authorization.md` (+ `REQ-ID-060..079`, section `authorization`) | `SUBTASK_authorization` |
| `SUBTASK_abuse_privacy/outputs/abuse-privacy.md` (+ `REQ-ID-080..099`, section `abuse_and_privacy_basics`) | `SUBTASK_abuse_privacy` |
| `outputs/identity-security.md` (assembled, six sections, consolidated register) + `threat_model` section + `REQ-ID-100..119` + `SYNTHESIS.md` | `SUBTASK_synthesis` |

### Identities (asserted by `SUBTASK_synthesis` with recorded evidence; no silent plugs)
1. Every `REQ-ID-*` is unique and sits within its owning child's declared range.
2. Every `REQ-ID-*` has a statement, testable `acceptance_criteria`, a `release_gating` flag, and traces to ≥1
   `REQ-PROD-*` that exists in the product-requirements register.
3. Each `REQ-ID-*` that a `BAR-*` would gate names a verification method from the parent schema vocabulary.
4. The assembled `identity-security.md` contains all six required sections from `design_artifact_map.yaml`.
5. Every `REQ-PROD-*` identity/security need (008–014, 016–024, 025–028 identity aspects) is answered by ≥1
   `REQ-ID-*` **or** explicitly recorded as carried by a sibling area (e.g. `REQ-OPS-*` for limits) with a reason.
6. The threat model names the threats chirp's public surface implies and, for each, what the design answers.
7. The id scheme and traceability schema are not redefined; this subtree's additions are additive only.
8. The deliverable carries no host/system/taskflow detail and no attribution trailer (repo hygiene).

### Derived Artifacts
- **Consolidated `REQ-ID-*` register** — assembled by `SUBTASK_synthesis` from the four spoke partials + its own
  threat-derived requirements, as the `requirements_and_acceptance_criteria` section.
- **REQ-ID ↔ REQ-PROD trace list** — produced by `SUBTASK_synthesis` for the parent synthesis to fold into the
  design-wide traceability matrix.

### Thin-Seam Note
The seam here is **not** thin: a single shared deliverable, a partitioned id space, a threat model that depends on
all four areas, and cross-area traceability. The contract is correspondingly real. Children MUST compose against
`contracts/` and MUST NOT redefine the id scheme, the required fields, or the section map.

---

## Output Specifications

| Deliverable | Format | Location | Producer |
|-------------|--------|----------|----------|
| `identity-security.md` (the design-area deliverable: six sections + consolidated `REQ-ID-*` register) | Markdown, repository-ready | `SUBTASK_identity_trust/outputs/identity-security.md` | `SUBTASK_synthesis` |
| Four section partials | Markdown | each spoke's `outputs/` | the four spokes |
| `SYNTHESIS.md` (fold record + identity evidence + trace list) | Markdown | `SUBTASK_identity_trust/SYNTHESIS.md` | `SUBTASK_synthesis` |
