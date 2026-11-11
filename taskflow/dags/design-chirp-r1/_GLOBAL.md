# _GLOBAL.md — design-chirp-r1 (product design subtree hub)

## Project Context

**Status**: Active

### Objective

Establish what `chirp` (`Nousix-LLC/nswe-demo`) must be to be a **releasable** Twitter-style product, as the
engagement's **first product design**: set a concrete, testable **release bar**; produce the design in the
repository as one reviewable PR on branch `work/design-chirp-r1`; turn the design into a traceable board backlog
(epics + issues with acceptance criteria); and **measure the live product** (deployed at commit `c805525`)
against the bar in the DAG's root `SYNTHESIS.md`.

This subtree designs **what the product must be and what "releasable" means for it** — requirements, journeys,
surfaces, acceptance criteria, the bar. It writes **design and tickets, not product code**. Every topic with an
engineering "how" (durable persistence, SSO, backups, rate limiting, sessions) is stated here as a **design
requirement with a testable bar**, and the implementation "how" is deferred to later code DAGs.

The authoritative task spec is this directory's `_BRIEF.md` (read it). This hub carries the shared context,
the task tree, and the contract every child composes against.

### Scope

**In Scope:**
- The six design concerns (product scope & requirements; domain & application design; UX & visual design;
  identity/security/trust; operational readiness; the plan) each carried to a **testable bar**.
- The recurring account-lifecycle & operational surfaces a releasable account-based product needs
  (sign-up / sign-in / recovery, account lifecycle incl. deletion & data export, onboarding, settings,
  notifications, admin/support, billing *if warranted*) — designed, or explicitly recorded as out-of-scope
  with rationale. Absence is the defect this subtree exists to prevent.
- The design PR into `main`; the board backlog; the root `SYNTHESIS.md` measurement + fold.

**Out of Scope:**
- Writing product code or implementing any ticket (later code DAGs, one epic at a time).
- Any repo/cluster/namespace other than `Nousix-LLC/nswe-demo` (+ read-only use of the live deployment).
- Teaching *how* to build any requirement (that is the `software` domain's / code DAGs' job).

### Success Criteria

- [ ] Release bar is concrete and testable — a later gap review, code DAG, or PR review can hold the product
      to it criterion by criterion. "It deploys / is reachable / CI is green / a working skeleton" is NOT a bar.
- [ ] The design covers every applicable concern; any concern judged out-of-scope is recorded with its reason.
- [ ] One design PR on `work/design-chirp-r1` into `main` carries the requirements, the bar, and the design
      artifacts, written for the repository's readers.
- [ ] A board backlog of epics + issues whose acceptance criteria **trace to the design**, de-duplicated
      against the existing board, each issue placed under its epic in dependency order (one epic = one coherent
      code goal).
- [ ] Root `SYNTHESIS.md` states the bar, indexes the issues by epic, and gives a **measured** account of where
      the live product at `c805525` stands against the bar (met / missing / which epic-issue covers each gap).

---

## Constraints and Requirements

### Process Constraints
- **Scope**: `Nousix-LLC/nswe-demo` only — its code, branches, PRs, issues, labels, milestones, Project, and
  Actions — plus **read-only** use of the live deployment to measure the product. Touch nothing else.
- **Design branch**: `work/design-chirp-r1`; open exactly **one** PR into `main`. Never force-push `main`;
  never rewrite merged history.
- **No attribution trailers** on any commit or PR body (the engagement forbids them; see #27 / HYG-1).
- **Not a prototype exemption**: unless the repo or engagement explicitly reduces it, the bar is a
  **releasable product**.

### Hygiene (binding on everything posted to GitHub)
Everything posted to GitHub (design doc, PR, issues, epics, comments) is written for the repository's readers
and carries **no** host/system detail: no host or cluster addresses, no filesystem or taskflow paths, no
agent/DAG/run ids, no `SYNTHESIS.md` locations, no attribution footers. Name things by repository identity
(`owner/repo`, repo-relative path, issue/PR number, commit SHA). Provenance is a link a reader can open.

### GitHub / live-deployment access (environment facts — NOT product content)
- GitHub operations use the `gh` CLI and git against `Nousix-LLC/nswe-demo` (default branch `main`,
  current HEAD `c805525`). A task needing a git working tree clones the repo into **its own workspace**
  (`gh repo clone Nousix-LLC/nswe-demo`); tasks do not share a working tree.
- The live deployment is reached per the repository/host environment facts (see the project `CLAUDE.md` host
  notes available in the environment). These facts are for running checks only and MUST NOT appear in any
  GitHub artifact.

---

## Input Specifications

| Source | Identity | Role |
|--------|----------|------|
| Repository | `Nousix-LLC/nswe-demo` @ `c805525` | The product being designed; crates `ferric`, `chirp-types`, `chirp-server` (axum REST, **in-memory repo, no external DB**, serves the SPA), `chirp-frontend` (SPA on ferric); `deploy/` (k8s + ArgoCD); `.github/` (CI). |
| Live deployment | ArgoCD app `chirp`, Synced+Healthy @ `c805525`, `/healthz`→200 | Exercise as a user to measure the product against the bar (read-only). |
| Engagement aim | `TASK.md` (repo root) | Production-quality framework + Twitter-style clone, built/tested/CD/reachable. This is the *aim*, **not** a bar — translating it into a concrete bar is the subtree's job. |
| Current board | open #27, #25, #24, #23 (non-release-gating hardening/polish follow-ups); EPIC trackers #1 ferric, #2 chirp, #3 devops | De-duplicate against these; fold #23/#24/#25 in where they belong rather than duplicating. No existing design/, docs/, or release bar. |

---

## Subtree Methodology Posture

The Phase-B application boot file is the **`design` domain loader/index**. Each child's `_BRIEF.md` names the
design bundle ID(s) its concern maps to (per the loader's Domain Mapping); the **executing** child loads full
bundle content on demand — a decomposing child propagates IDs, it does not pre-load bodies. Bundle assignments
per child are in the Task Summary below and in each brief.

**Synthesis is a verification gate, not a prose summary.** `SUBTASK_synthesis` (Task Kind: `synthesis`)
reconciles the siblings' combined output, asserts the contract identities below **with recorded evidence**,
measures the live product against the bar, and — where it finds a fixable design/backlog gap — **remediates by
decomposing a remediation subtree**, never by a silent plug or a quiet pass. The method for *how* to run a
decomposition and a synthesis gate is engineering practice in the `software` domain's `decomposition` /
`synthesis` bundles, reached by prose; this design subtree does not duplicate it.

---

## Task Structure

### Overview

```
design-chirp-r1/
├── _GLOBAL.md                          (this hub)
├── contracts/                          (READ-ONLY for descendants)
│   ├── _MANIFEST.yaml                  (kind, ownership, identities, derived artifacts)
│   ├── design_artifact_map.yaml        (repo design/ file layout + owner + required sections per file)
│   └── id_and_traceability_schema.yaml (REQ/BAR/EPIC id scheme + traceability matrix + verification methods)
├── SUBTASK_product_requirements/_BRIEF.md
├── SUBTASK_domain_app_design/_BRIEF.md
├── SUBTASK_experience_design/_BRIEF.md
├── SUBTASK_identity_trust/_BRIEF.md
├── SUBTASK_operational_readiness/_BRIEF.md
├── SUBTASK_release_bar/_BRIEF.md
├── SUBTASK_design_pr/_BRIEF.md
├── SUBTASK_delivery_backlog/_BRIEF.md
└── SUBTASK_synthesis/_BRIEF.md
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_product_requirements` | none | Define the product and its kind, the users/personas and their journeys, and the testable product requirements & acceptance criteria that the rest of the design traces to. Bundles: Product Strategy (primary); Release Definition, Product Surfaces (support). Owns `REQ-PROD-*`. | `outputs/product-requirements.md` |
| `SUBTASK_domain_app_design` | `SUBTASK_product_requirements` | Design the application/domain **as requirements and structure** the product must have: domain model, modules & responsibilities, the **durable-persistence requirement** (the in-memory store is a release blocker), interfaces, entry points, where state lives — held to ferric/chirp-types/chirp-server contracts, concrete enough to build against; implementation how deferred. Bundles: Product Strategy, Release Definition. Owns `REQ-DOM-*`. | `outputs/domain-application-design.md` |
| `SUBTASK_experience_design` | `SUBTASK_product_requirements` | Design how the product looks and behaves: information architecture & interaction, the screens & flows (incl. sign-up/in, the posting/timeline loops, onboarding, settings, empty/error/loading states), a visual language & design system, responsive layout, and accessibility. Bundles: Experience Design (primary); Product Strategy, Identity and Trust (support). Owns `REQ-UX-*`. | `outputs/experience-design.md` |
| `SUBTASK_identity_trust` | `SUBTASK_product_requirements` | Design identity, security & trust **as requirements**: accounts & their full lifecycle (sign-up/in/recovery, deletion, data export), real authentication & safe sessions, authorization (what each user may see/change), abuse/privacy basics, and the threat model this surface implies. Bundles: Identity and Trust (primary); Product Strategy, Release Definition, Product Surfaces (support). Owns `REQ-ID-*`. | `outputs/identity-security.md` |
| `SUBTASK_operational_readiness` | `SUBTASK_product_requirements`, `SUBTASK_domain_app_design` | Design what must be true in production beyond "it runs", as release requirements: durable data, backups & recovery path, limits/quotas, observability, status/incident — consuming the persistence model from domain design. Fold existing follow-ups #23/#24/#25 in where they belong. Bundle: Release Readiness (primary); Release Definition, Product Strategy, Identity and Trust (support). Owns `REQ-OPS-*`. | `outputs/operational-readiness.md` |
| `SUBTASK_release_bar` | `SUBTASK_product_requirements`, `SUBTASK_domain_app_design`, `SUBTASK_experience_design`, `SUBTASK_identity_trust`, `SUBTASK_operational_readiness` | Consolidate the per-area requirements into (a) an MVP-vs-releasable scoping and (b) the concrete, testable **release bar** (`BAR-*`), and run a **completeness & gap review** (Product Surfaces) over the whole design to catch missing surfaces and record in/out-of-scope judgments. Bundle: Release Definition (primary); Release Readiness, Product Strategy, Identity and Trust, Product Surfaces (support). Owns `BAR-*`. | `outputs/release-bar.md` |
| `SUBTASK_design_pr` | `SUBTASK_product_requirements`, `SUBTASK_domain_app_design`, `SUBTASK_experience_design`, `SUBTASK_identity_trust`, `SUBTASK_operational_readiness`, `SUBTASK_release_bar` | Assemble the completed design-area outputs + the release bar into the repository `design/` tree per `design_artifact_map.yaml`, on branch `work/design-chirp-r1`, and open **one** PR into `main` written for the repo's readers. Owns the `design/` index/README and the PR; owns no section content. | `outputs/design-pr.md` (records PR # / branch / file map) |
| `SUBTASK_delivery_backlog` | `SUBTASK_design_pr`, `SUBTASK_release_bar` | Turn the design + bar into a board backlog: epics (one epic = one coherent, landable code goal, deps stated) and issues with acceptance criteria that **trace** to `REQ-*`/`BAR-*` and to the design doc in the repo, de-duplicated against the existing board, each issue under its epic in dependency order reaching a usable product early and the bar after. Owns `EPIC-*`/issue placement. Bundle: Delivery (primary); Product Strategy, Release Definition (support). | `outputs/backlog.md` (issue/epic index + trace map) |
| `SUBTASK_synthesis` | `SUBTASK_design_pr`, `SUBTASK_delivery_backlog`, `SUBTASK_release_bar`, `SUBTASK_product_requirements`, `SUBTASK_domain_app_design`, `SUBTASK_experience_design`, `SUBTASK_identity_trust`, `SUBTASK_operational_readiness` | **Verification gate + fold.** Assert the contract identities with recorded evidence (coverage, traceability, one-owner-per-file, every gap→issue, hygiene); **measure the live product** at `c805525` against the bar as a user; author the root `SYNTHESIS.md` stating the bar, indexing issues by epic, and giving the measured standing. Remediate fixable gaps by decomposing a remediation subtree (no silent plugs). Bundle: Release Definition (CompletenessAndGapReview, ReleaseBar); synthesis-gate method from `software`/`synthesis` by prose. | `SYNTHESIS.md` (at this subtree root — the fold record) |

### Dependency Graph (human-readable; the table above is authoritative)

```
product_requirements ─┬─> domain_app_design ─────┐
                       ├─> experience_design ─────┤
                       ├─> identity_trust ────────┤
                       └─> domain_app_design ──> operational_readiness
                                                   │
      (product_requirements + all four concerns) ──┴─> release_bar
                                                          │
            (all concerns + release_bar) ──> design_pr ──┼─> delivery_backlog
                                                          │        │
                                              (design_pr + delivery_backlog + release_bar + all) ──> synthesis
```

---

## Contract

The two co-designed outputs of this decomposition are the task tree above and the contract below. The children
are parts of one product design; they share a real seam — a single coherent design document, one identifier
scheme that makes requirements, bar criteria, and tickets traceable to one another, and the coverage/trace
invariants the synthesis gate asserts. That seam is frozen **before any child runs**.

**Contract location**: `contracts/` (read-only for every descendant)
**Contract kind**: `yaml_schema` (requirement/traceability schema + design-artifact ownership map)

### Structural Declarations
- `contracts/design_artifact_map.yaml` — the repo `design/` file layout, the **one owning task per file**, and
  the required sections each file must contain.
- `contracts/id_and_traceability_schema.yaml` — the `REQ-<AREA>-NNN` / `BAR-NNN` / epic-and-issue identifier
  conventions, the area→owner assignment, the traceability-matrix columns, and the verification-method
  vocabulary each `BAR-*` must use.

### Ownership (one producer per artifact)

| Artifact | Owning subtask |
|----------|----------------|
| `design/product-requirements.md` + `REQ-PROD-*` | `SUBTASK_product_requirements` |
| `design/domain-application-design.md` + `REQ-DOM-*` | `SUBTASK_domain_app_design` |
| `design/experience-design.md` + `REQ-UX-*` | `SUBTASK_experience_design` |
| `design/identity-security.md` + `REQ-ID-*` | `SUBTASK_identity_trust` |
| `design/operational-readiness.md` + `REQ-OPS-*` | `SUBTASK_operational_readiness` |
| `design/release-bar.md` + `BAR-*` | `SUBTASK_release_bar` |
| `design/README.md` (index) + the PR | `SUBTASK_design_pr` |
| epics + issues (board) + trace map | `SUBTASK_delivery_backlog` |
| `SYNTHESIS.md` + the live-product measurement | `SUBTASK_synthesis` |

### Identities (asserted by `SUBTASK_synthesis` with recorded evidence; no silent plugs)
1. Each `design/*.md` file has exactly one owning task (no file written by two tasks; none unowned).
2. Each of the six brief concerns is either covered by a design file **or** explicitly recorded out-of-scope
   with a stated reason.
3. Every **release-gating** `REQ-*` is covered by ≥1 `BAR-*`.
4. Every `BAR-*` is testable — it names a verification method from the schema vocabulary and references ≥1 `REQ-*`.
5. Every filed issue's acceptance criteria cite ≥1 `REQ-*` or `BAR-*`; every issue sits under exactly one epic;
   each epic is one coherent, landable code goal with its dependencies stated.
6. Every gap found in the live-product measurement maps to ≥1 filed issue/epic.
7. Every recurring account/operational surface (sign-up/in/recovery, account deletion, data export, onboarding,
   settings, notifications, admin/support, billing) is either designed or recorded out-of-scope with a reason.
8. Nothing posted to GitHub contains host/system/taskflow detail or an attribution trailer (hygiene).

### Derived Artifacts
- **Traceability matrix** (`REQ-* ↔ BAR-* ↔ epic/issue`) — assembled and checked by `SUBTASK_synthesis` from
  the owned columns the bar and backlog produce.
- **`design/README.md`** — the design index, generated by `SUBTASK_design_pr` from `design_artifact_map.yaml`.

### Thin-Seam Note
The seam here is not thin: a shared document, a shared ID scheme, and cross-artifact traceability are a rich
contract. Children MUST compose against `contracts/` and MUST NOT redefine the ID scheme or the file map.
