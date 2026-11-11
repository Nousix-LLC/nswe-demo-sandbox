# COMPLETE — SUBTASK_docs_and_dx

**Task:** Ferric 1.0 — documentation & developer-experience bar (concern 6). Owns `REQ-DX-*`.
**Evaluation:** Atomic (one design responsibility: the DX bar as one `REQ-DX-*` register + plan; the three
named sub-areas are sections of one onboarding arc, below the atomic-peer granularity set by
`SUBTASK_scope_and_requirements`).

## What was produced

`docs-and-dx.md` (this workspace; repo target `design/ferric/docs-and-dx.md`) — the docs/DX plan and the
`REQ-DX-001`–`REQ-DX-010` register. It designs **what documentation and tooling must exist and how "a new user
can get to a working app" is checked**, not the prose of the guide/tutorial/API docs (that is downstream build
work).

### Coverage of the brief's three distinct concerns
- **Learning path** — guide (`REQ-DX-001`), tutorial with compiling end state (`REQ-DX-002`), examples set
  across the capability span incl. SSR+hydrate (`REQ-DX-004`), evaluator README/landing (`REQ-DX-009`).
- **API docs** — rendered rustdoc on docs.rs for the public prelude surface (`REQ-DX-003`), diagnostics docs
  (`REQ-DX-008`), docs-kept-in-sync / CI (`REQ-DX-010`).
- **The cargo-generate starter** — CSR + SSR starter (`REQ-DX-005`), the integrating "new user → working app"
  acceptance path (`REQ-DX-006`), build/toolchain docs client + SSR (`REQ-DX-007`).

Surfaces added beyond the brief's named three (a starting list is a floor): README/landing for A1, diagnostics
documentation, and docs-don't-rot CI.

## Success criteria
- [x] Guide / tutorial / API-docs / examples / starter each specified with testable `REQ-DX-*` acceptance
      criteria, each carrying a `verification_method` from the contract vocabulary (`example_build`,
      `doc_inspection`, `automated_test`), `stage`, and `release_gating`.
- [x] The "new user → working app" path is concrete and checkable — `REQ-DX-006`, a scripted 4-step path
      verified by `example_build` + `doc_inspection`.
- [x] Peer DX compared by name (Leptos, Dioxus, Yew) — §6 table plus §2/§4, grounded in each framework's
      documented public tooling (Leptos Book + `start-trunk`/`cargo leptos new`; Dioxus `dx new`; Yew/Trunk;
      `cargo-generate`; docs.rs).

## Contract conformance
- **I1 (disjoint registers):** only `REQ-DX-*` ids are minted; every `REQ-FW-*`, `REQ-API-*`, `REQ-SSR-*`,
  `REQ-RT-*`, `REQ-HTTP-*`, `REQ-PERF-*`, `REQ-REL-*` reference is read-only.
- **I2/I3 (trace):** every `REQ-DX-*` cites ≥1 upstream `REQ-FW-*`, so the gating criteria the release bar
  consolidates trace to a framework-level need.
- **I5 (out-of-1.0 recorded):** the DX-adjacent deferral (hot reload/HMR) is left as `REQ-FW-017` (owned by
  scope) and referenced by no `BAR-FERRIC-*`; no `REQ-DX-*` is `post_one_oh`.
- Conforms to `../contracts/id_and_traceability_schema.yaml` and `../contracts/_MANIFEST.yaml`.

## How it composes with the parent
Feeds `SUBTASK_release_bar` (the `one_oh` gating `REQ-DX-*` for the consolidated `BAR-FERRIC-*`),
`SUBTASK_release_plan` (a docs/DX epic tracing to this register), and `SUBTASK_design_pr` (placed at
`design/ferric/docs-and-dx.md`).

## Notes
- Grounded at `Nousix-LLC/nswe-demo` @ `276138f`: three crate READMEs + `counter.rs` + router `app.rs` exist;
  no guide, tutorial, rendered API site, or starter — every `REQ-DX-*` closes a stated gap.
- The methodology surface returned `agent_domain_unset` at boot (not bound for this invocation); per the hub
  ("each child selects its own methodology; the hub names none"), the DX/library-design judgment was applied
  from the principal-product-designer role overlay. Peer-tooling claims were grounded by web search, not memory.
- avoid-ai-writing pass run over the narrative deliverable (patterns.md P0/P1 by hand; the skill was not
  available in this node); the one character-adjective tell ("truthful" on a README) was fixed to "accurate".
