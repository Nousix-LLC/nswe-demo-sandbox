# _GLOBAL.md — SUBTASK_product_requirements (product-requirements subtree hub)

## Project Context

**Status**: Active

### Objective

Produce the chirp **product-requirements** design — the foundation every other design area traces to.
This subtree owns `design/product-requirements.md` (assembled at this workspace's
`outputs/product-requirements.md`) and the entire `REQ-PROD-*` requirement register. It states **what the
product must be, for whom, and why, and what "done" looks like from the user's side** — never how it is built.

This task spans three distinct concerns — (1) product definition & kind, (2) users/personas & their end-to-end
journeys, (3) the testable requirements & acceptance criteria that follow — plus a verification-gate synthesis
that assembles them into one coherent document. It is decomposed hub-and-spoke: two independent precursor
spokes (definition; users & journeys), one requirements spoke that depends on both, and one synthesis gate.

The authoritative task spec for this subtree is this directory's `_BRIEF.md` (the parent-authored brief). This
hub carries the shared context; `contracts/` (read-only) freezes the seam the children compose against.

### Scope

**In Scope:**
- The five required sections of `design/product-requirements.md` (per the inherited
  `../contracts/design_artifact_map.yaml`): `product_definition_and_kind`, `users_personas`, `user_journeys`,
  `requirements_and_acceptance_criteria`, `in_scope_out_of_scope`.
- The product kind(s) that apply to chirp (consumer web app / SaaS / COTS / OSS) and what each makes users
  assume without asking — carried into requirements or recorded out-of-scope with a reason.
- End-to-end journeys incl. **first visit, sign-up, sign-in, recovery, the core posting/reading/timeline/follow
  loops, daily use, and leaving (account deletion and taking their data out)**.
- The `REQ-PROD-*` register: every requirement testable by a stranger, each with its release-gating flag.
- An explicit in-scope / out-of-scope statement for a releasable product of this kind.

**Out of Scope:**
- Any implementation "how" (persistence engine, auth protocol internals, framework internals) — deferred to
  later code DAGs; stated here only as a requirement with a testable bar where it belongs to another area it is
  left to that area's `REQ-*`.
- Requirement areas owned by sibling design tasks: `REQ-DOM-*`, `REQ-UX-*`, `REQ-ID-*`, `REQ-OPS-*`, `BAR-*`.
  This subtree owns `REQ-PROD-*` only and does not redefine the inherited id/traceability or artifact-map schema.

### Success Criteria

- [ ] `design/product-requirements.md` carries all five required sections from `../contracts/design_artifact_map.yaml`.
- [ ] Product kind(s) named, with what each implies for a releasable product.
- [ ] Journeys walked end-to-end incl. first visit, daily use, and leaving (deletion / data export).
- [ ] Every `REQ-PROD-*` has acceptance criteria testable by someone who never met the author; release-gating flag set.
- [ ] In-scope / out-of-scope stated; any concern judged out-of-scope recorded with a reason.
- [ ] Composes against `../contracts/` (uses the inherited `REQ-PROD-*` scheme; does not redefine any schema).

---

## Constraints and Requirements

### Process Constraints
- **Design & requirements only** — defer every implementation "how" to later code DAGs.
- **Inherited contracts are read-only.** This subtree's `contracts/` EXTENDS the parent `../contracts/`
  (adds section ownership + the sole-REQ-PROD-minter rule + subtree identities); it MUST NOT override the
  inherited `REQ-<AREA>-NNN` scheme, the `each_requirement_has` fields, or the `product-requirements.md`
  required-section list.
- **Repository-ready hygiene** (binding on all content that reaches the repo): no host/cluster addresses, no
  filesystem/taskflow paths, no agent/DAG/run ids, no `SYNTHESIS.md` locations, no attribution trailers. Name
  things by repository identity (`owner/repo`, repo-relative path, issue/PR number, commit SHA).

### Inputs (shared by the subtree)

| Source | Identity | Role |
|--------|----------|------|
| Parent hub | `../_GLOBAL.md` | Engagement context, release-bar intent, GitHub/live-deployment facts |
| Parent contract | `../contracts/` (read-only) | `REQ-PROD-*` id scheme; required sections; traceability vocabulary |
| Subtree contract | `contracts/` (read-only) | Section ownership, sole-REQ-PROD-minter rule, subtree identities |
| Repository | `Nousix-LLC/nswe-demo` @ `c805525` | The product as it exists: crates `ferric`, `chirp-types`, `chirp-server` (axum REST, in-memory repo, serves the SPA), `chirp-frontend` (SPA); `deploy/`; `.github/`. Executing children clone it into their own workspace. |
| Engagement aim | `TASK.md` (repo root) | Production-quality Rust/WASM framework + Twitter-style clone — the *aim* to translate into product requirements |

---

## Subtree Methodology Posture

The Phase-B application boot file is the **`design` domain loader/index**. Each child `_BRIEF.md` names the
design bundle ID(s) its concern maps to (per the loader's Domain Mapping); the **executing** child loads full
bundle content on demand. This hub does not pre-load bundle bodies.

**Synthesis is a verification gate, not a prose summary.** `SUBTASK_pr_synthesis` (Task Kind: `synthesis`)
reconciles the three fragments into the single `product-requirements.md`, asserts the subtree identities below
**with recorded evidence**, and — where it finds a fixable gap (a missing required section, an untestable or
unflagged requirement, a journey with no requirement) — **remediates by decomposing a remediation subtree**,
never by a silent plug or a quiet pass. The method for *how* to run a decomposition / synthesis gate is
engineering practice in the `software` domain's `decomposition` / `synthesis` bundles, reached by prose.

---

## Task Structure

### Overview

```
SUBTASK_product_requirements/
├── _GLOBAL.md                              (this hub)
├── contracts/                              (READ-ONLY for descendants; EXTENDS ../contracts/)
│   ├── _MANIFEST.yaml                      (kind, section ownership, subtree identities, derived artifacts)
│   └── section_ownership_map.yaml          (which fragment owns which required section + the REQ-PROD register)
├── SUBTASK_product_definition/_BRIEF.md
├── SUBTASK_users_and_journeys/_BRIEF.md
├── SUBTASK_requirements/_BRIEF.md
├── SUBTASK_pr_synthesis/_BRIEF.md
└── outputs/product-requirements.md         (assembled by SUBTASK_synthesis — this subtree's deliverable)
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_product_definition` | none | Define what chirp is as a releasable product and which product kind(s) apply (consumer web / SaaS / COTS / OSS), with what each kind makes users assume without asking. Owns the `product_definition_and_kind` section source and a product-kind-lens scope draft. Bundles: Product Strategy (primary); Release Definition, Product Surfaces (support). | `outputs/product-definition.md` |
| `SUBTASK_users_and_journeys` | none | Characterize chirp's users/personas and walk their end-to-end journeys (first visit, sign-up/in/recovery, the posting/reading/timeline/follow loops, daily use, and leaving incl. deletion & data export), surfacing journey-derived needs in prose. Owns the `users_personas` and `user_journeys` section sources. Bundles: Product Strategy (primary); Experience Design, Product Surfaces, Identity and Trust (support). | `outputs/users-and-journeys.md` |
| `SUBTASK_requirements` | `SUBTASK_product_definition`, `SUBTASK_users_and_journeys` | Formalize every need from the two upstream fragments into the testable `REQ-PROD-*` register (sole minter) — each with a stranger-checkable acceptance criterion and a release-gating flag — and write the consolidated `in_scope_out_of_scope` statement. Owns `requirements_and_acceptance_criteria` and `in_scope_out_of_scope`. Bundles: Product Strategy (primary); Release Definition, Delivery (support). | `outputs/requirements.md` |
| `SUBTASK_pr_synthesis` | `SUBTASK_product_definition`, `SUBTASK_users_and_journeys`, `SUBTASK_requirements` | **Verification gate + fold.** Assemble the three fragments into the single `product-requirements.md` with all five required sections; assert the subtree identities with recorded evidence; remediate fixable gaps by decomposing (no silent plug). Author the fold record and fold this subtree. | `../outputs/product-requirements.md` + `SYNTHESIS.md` (at this subtree root) |

### Dependency Graph (human-readable; the table above is authoritative)

```
SUBTASK_product_definition ──┐
                             ├──> SUBTASK_requirements ──> SUBTASK_pr_synthesis
SUBTASK_users_and_journeys ──┘                              (also depends on both precursors)
```

---

## Contract

The two co-designed outputs of this decomposition are the task tree above and the contract in `contracts/`.
The children are parts of ONE document (`product-requirements.md`) and inherit this task's identity; they share
a real seam — one document with five fixed sections, one `REQ-PROD-*` register minted by a single owner, and the
coverage/traceability invariants the synthesis gate asserts. That seam is frozen **before any child runs**.

**Contract location**: `contracts/` (read-only for every descendant)
**Contract kind**: `yaml_schema` (section-ownership map + subtree identities, extending the inherited parent contract)

### Inherited Contracts

| Ancestor contract | Path | What it binds here |
|---|---|---|
| ID & traceability schema | `../contracts/id_and_traceability_schema.yaml` | `REQ-PROD-*` format, `each_requirement_has` fields, `release_gating`. MUST NOT redefine. |
| Design artifact map | `../contracts/design_artifact_map.yaml` | `product-requirements.md` required-section list + ownership. MUST NOT redefine. |

### Structural Declarations (this level)
- `contracts/_MANIFEST.yaml` — kind, per-fragment section ownership, subtree identities, derived artifacts.
- `contracts/section_ownership_map.yaml` — which fragment owns which required section, and the rule that
  `SUBTASK_requirements` is the SOLE minter of `REQ-PROD-*` ids.

### Ownership (one producer per artifact)

| Artifact | Owning subtask |
|----------|----------------|
| `product_definition_and_kind` section source + product-kind scope draft | `SUBTASK_product_definition` |
| `users_personas` + `user_journeys` section sources | `SUBTASK_users_and_journeys` |
| `requirements_and_acceptance_criteria` + `in_scope_out_of_scope` sections + all `REQ-PROD-*` | `SUBTASK_requirements` |
| assembled `outputs/product-requirements.md` + `SYNTHESIS.md` | `SUBTASK_pr_synthesis` |

### Identities (asserted by `SUBTASK_pr_synthesis` with recorded evidence; no silent plugs)
1. **SECTION_COVERAGE** — the assembled `product-requirements.md` contains all five required sections from
   `../contracts/design_artifact_map.yaml`, each sourced from its owning fragment.
2. **REQ_SINGLE_OWNER** — every `REQ-PROD-*` id is minted by `SUBTASK_requirements` alone; no other fragment
   defines a `REQ-PROD-*` id.
3. **REQ_WELL_FORMED** — every `REQ-PROD-*` carries `id`, `statement`, `acceptance_criteria` (testable by a
   stranger), and `release_gating` (true|false), per the inherited `each_requirement_has`.
4. **JOURNEY_TO_REQ** — every end-to-end journey (incl. first visit, daily use, and leaving: account deletion
   and data export) traces to ≥1 `REQ-PROD-*`.
5. **KIND_IMPLICATIONS** — the applicable product kind(s) are named with what each implies, and each implication
   is either reflected in a `REQ-PROD-*` or recorded out-of-scope with a reason.
6. **SCOPE_RECORDED** — `in_scope_out_of_scope` is present; any concern judged out-of-scope carries a reason.
7. **HYGIENE** — no host/system/taskflow detail and no attribution trailer appears in any content bound for the
   repo (inherits parent `GITHUB_HYGIENE`).

### Derived Artifacts
- **Assembled `product-requirements.md`** — composed by `SUBTASK_synthesis` from the three fragment outputs per
  the section-ownership map; this subtree's single deliverable.

### Thin-Seam Note
The seam is not thin: a shared document with fixed sections, a single-owner requirement register, and
journey→requirement traceability are a rich contract. Children MUST compose against `contracts/` and MUST NOT
redefine the inherited id scheme, section list, or artifact map.
