# COMPLETE — SUBTASK_product_definition

## What was done

Defined **what chirp is** as a releasable product and **which product kind(s)** apply, as
the `product_definition_and_kind` section source plus a product-kind-lens scope draft.
Grounded in the repository `Nousix-LLC/nswe-demo` @ `c805525` (inspected directly): the
WASM SPA (`crates/chirp-frontend`), the axum REST backend and its live route surface
(`crates/chirp-server`), the shared wire contract (`crates/chirp-types`), the handle-only
session model, the in-memory store, and the container/GitOps deployment (`deploy/`).

## Output produced

- `outputs/product-definition.md` — repository-ready design prose carrying:
  1. **What chirp is** from the user's side (the post / read-timeline / follow / like loop),
     how it is shaped (SPA + REST, self-hosted container), and a factual account of the
     product's state at `c805525` (handle-only identity; in-memory store; absent
     account-lifecycle and supporting surfaces) — the gap the rest of the requirements close.
  2. **Product kind(s):** chirp is a hosted **consumer web application** (applicable kind),
     with the seven things that kind makes users assume without asking surfaced as prose
     needs. **SaaS, COTS, and OSS** are each recorded as not-applicable with a reason, plus
     the honest source-available/self-hostable nuance and a note that "closed demonstration"
     does not lower the release bar.
  3. **Product-kind-lens scope draft:** in-scope inclusions a releasable product of this kind
     must carry, and out-of-scope items each with a reason — for `SUBTASK_requirements` to
     consolidate into `in_scope_out_of_scope`.

## Contract composition

- Expressed needs in prose with **12 informal `need:` handles**; **minted no `REQ-PROD-*`
  ids** (`SUBTASK_requirements` is the sole minter).
- Composed against the read-only subtree contract (`../contracts/`) and parent contract
  (`../../contracts/`); redefined no inherited schema, section list, or id scheme.
- Supports the subtree identities `KIND_IMPLICATIONS` (each kind implication is a prose need
  or recorded out-of-scope with a reason) and `SCOPE_RECORDED` (out-of-scope items carry
  reasons); leaves their assertion to the synthesis gate.
- Repository-ready hygiene verified: no host/cluster/taskflow detail, no filesystem paths,
  no attribution trailers; everything named by repository identity.

## Note on execution environment

The `design` methodology loader was unreachable in this invocation (the reconstructed node
booted with an unbound agent domain, so the loader could not be resolved). Per the dispatch
assumptions for an environment with no interactive operator, the work proceeded on the
principal-product-designer competence that governs this role and was grounded in the
repository itself; the methodology bundles would have supplemented coverage frameworks only.
This is recorded here, not in any repository-bound content.

## Success criteria

- [x] chirp defined from the user's side, grounded in the product at `c805525`.
- [x] Applicable product kind(s) named, each with what it makes users assume without asking.
- [x] Product-kind-lens in/out-of-scope draft provided; out-of-scope items carry reasons.
- [x] Needs are prose / `need:` handles only — no `REQ-PROD-*` ids minted here.
- [x] Composes against `../contracts/` and `../../contracts/`; redefines no schema; hygiene holds.
