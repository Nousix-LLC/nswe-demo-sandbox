# COMPLETE — SUBTASK_router (Ferric 1.0 router design)

**Status:** completed · **Evaluation:** Atomic · **Output:** `router.md`

## What was produced

`router.md` — the Ferric 1.0 client-side router design, following the sub-contract `doc_layout` (overview,
relationship-to-frozen-surface + what 1.0 adds, the `REQ-RT-*` register with testable acceptance criteria, named
peer comparison, and the board-issue-#5 fold). It owns the `REQ-RT-*` register and nothing else.

## How the work was done

1. Booted the kernel (Phase A boot-load set, Phase B methodology loader — unavailable, `agent_domain_unset`,
   assumption recorded — Phase C `_BRIEF.md`; `_GLOBAL.md` path not relayed, cleanly skipped).
2. Evaluated decompose/atomic against the TDF triggers: one component, one methodology, one register, one
   perspective; facets share one API vocabulary and one id space → every trigger clears, both concern tests pass
   → `Atomic`.
3. Read the inputs the brief named: the sub-contract manifest, the parent id/traceability schema, the
   requirements frame (`scope-and-requirements.md`), and the real frozen crate
   (`crates/ferric-router/src/{lib,matcher,router,link}.rs` + `contracts/ferric_router_api.rs` at `276138f`).
   Confirmed board issue #5 is CLOSED (baseline shipped). Verified peer-router behavior (`leptos_router`, Dioxus)
   from current public docs.
4. Wrote `router.md`; ran the avoid-ai-writing P0/P1 pass by hand (loader unavailable) and fixed one tell
   ("honest cost" → "cost ... is concrete").

## Success criteria (from `_BRIEF.md`)

- [x] Route params, nested routes, and in-app links/navigation each specified with testable `REQ-RT-*`
      acceptance criteria conforming to `id_and_traceability_schema.yaml` (each criterion stranger-checkable,
      each naming a `verification_method`: automated_test / example_build / doc_inspection). — `REQ-RT-001/005/003/004`.
- [x] Additive over the frozen `ferric-router` prelude; every change flagged additive, no silent redefinition
      (SI2 / I9). — dedicated relationship section + `REQ-RT-008`; additions: nested routes (005), replace-nav
      (003), active-link (007), nested fallback (006).
- [x] The #5 fold is explicit — #5 CLOSED/delivered baseline, 1.0 extends it; new work-items under epic #1
      reference #5 as superseded, `supersedes: #5` (SI3 / feeds I7).
- [x] `leptos_router` and Dioxus router compared by name.
- [x] Only `REQ-RT-*` ids written (SI1 / I1); all `REQ-FW-*` / `REQ-ASYNC-*` / `REQ-HTTP-*` references read-only.

## Notes for the synthesis gate

- Register: `REQ-RT-001`–`REQ-RT-008` are 1.0 gating; `REQ-RT-009` (query/search params) is a recorded post-1.0
  deferral (`release_gating: false`, referenced by no BAR).
- Design-not-implementation held throughout: the matcher algorithm, internal data structures, and the exact
  shape of the additive replace-navigation API are left to the implementing code DAG.
- Repository references carry no host/cluster/SSH/path/environment detail.
