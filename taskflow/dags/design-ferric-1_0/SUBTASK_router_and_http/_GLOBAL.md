# _GLOBAL.md — SUBTASK_router_and_http (router + HTTP/JSON client subtree hub)

## Project Context

**Status**: Active

This subtree is one concern of the Ferric 1.0 framework design (parent hub: `../_GLOBAL.md`). Its job is to
design **two capabilities a real Rust/WASM app needs** — a **router** and an **HTTP/JSON client** — each to a
testable bar, reconciled additively with the crates that already exist (`ferric-router` = board issue #5,
`ferric-http` = board issue #6), and to fold those two board issues into the 1.0 plan rather than duplicate
them. The combined deliverable is one document, `router-and-http.md`, placed once at
`design/ferric/router-and-http.md` in the repository.

### Why this concern was decomposed

The assigned concern designs **two distinct capabilities**, not one. A router (route table, path params,
nested routes, in-app links, History-API navigation, a reactive outlet) and an HTTP/JSON client (typed fetch,
request building, error model) are separate system components: separate frozen crates (`ferric-router` /
`ferric-http`), separate id registers (`REQ-RT-*` / `REQ-HTTP-*`), separate board issues (#5 / #6), and
disjoint peer evidence (leptos_router / Dioxus router vs `reqwest` / `gloo-net`). A routing specialist and a
network-client specialist could design these in parallel with no shared structural seam. The kernel's
Scope-Based trigger and Distinct Concerns Test fire on that enumeration, so the concern is split into two
parallel design spokes plus one synthesis gate that composes them into the single deliverable and verifies the
seam.

### Objective

Deliver `design/ferric/router-and-http.md`: a router design owning the `REQ-RT-*` register and an HTTP/JSON
client design owning the `REQ-HTTP-*` register, each with testable acceptance criteria, each additive over its
crate's frozen `prelude` surface, each stating explicitly how its board issue (#5 / #6) is superseded or
extended by the 1.0 design — composed into one document and verified against the identities below.

### Scope

**In Scope:**
- **Router (`REQ-RT-*`, absorbs #5):** route table and matching, path parameters, **nested routes**, in-app
  links and History-API navigation, the reactive outlet that re-renders on path change; the relationship to the
  frozen `ferric-router` surface (`Params`, `RoutePattern`, `Router`, `navigate`, `current_path`, `link`) and
  exactly what the 1.0 adds (e.g. nested routing if not yet present).
- **HTTP/JSON client (`REQ-HTTP-*`, absorbs #6):** typed JSON fetch (serde), request building, the error model
  (including non-2xx handling); the relationship to the frozen `ferric-http` surface (`Client` / `ClientBuilder`,
  `RequestBuilder`, `Response`, `Error` / `Result`) and exactly what the 1.0 adds.
- **The fold of #5 and #6:** each child states how its board issue is superseded/extended, feeding parent
  identity I7 so `file_backlog` edits #5/#6 rather than filing duplicates.
- Honest, named peer comparison (routers: leptos_router, Dioxus router; HTTP: `reqwest`, `gloo-net`).

**Out of Scope:**
- Implementation. This is **design (what, not how)**: requirements, architecture, and a testable bar; not the
  matcher algorithm, the fetch wrapper internals, or any code. Implementation is deferred to later code DAGs.
- Any other area's register. `REQ-RT-*` / `REQ-HTTP-*` only; all cross-references to `REQ-FW-*`, `REQ-API-*`,
  `REQ-ASYNC-*`, etc. are read-only.
- Silent redefinition of the frozen `prelude` surfaces (identity I9). Any change is called out as additive.

### Success Criteria

- [ ] Nested routing, route params, in-app links/navigation, and typed JSON fetch are each specified with
      testable `REQ-RT-*` / `REQ-HTTP-*` acceptance criteria conforming to the contract schema.
- [ ] The design is additive over the frozen `ferric-router` / `ferric-http` `prelude` surfaces (I9); any change
      to an existing surface is flagged additive, never a silent redefinition.
- [ ] The fold of #5 and #6 is explicit (what each becomes under the 1.0 plan), feeding parent identity I7.
- [ ] Peer routers / HTTP clients compared by name.
- [ ] The combined deliverable `router-and-http.md` lands exactly once at `design/ferric/router-and-http.md`
      (parent identity I8).

---

## Constraints and Requirements

### Process Constraints
- **Repository scope**: `Nousix-LLC/nswe-demo` only. Nothing posted to GitHub carries host, cluster, SSH, path,
  or environment detail; name only repository identities (`owner/repo`, issue/PR numbers, commits).
- **Design, not code**: every requirement reads as something a stranger could check against the framework; no
  internal implementation is chosen.

### Quality Requirements
- **Evidence over memory.** Peer comparisons cite frameworks by name; "common practice" claims rest on
  something actually read. Cite peers by name, never by host path.
- **Writing voice.** Plain, checkable prose. No machine-writing tells (no "honest" on things that cannot hold a
  character, no narrated candor, no unpaired contrasts, no slot-fill templates, no padded triads, no hollow
  intensifiers). Run the avoid-ai-writing pass over every narrative deliverable before finalizing.

### Methodology
- No methodology is named here. Each child **selects and loads its own** methodology for its concern (API /
  library design, web routing design, HTTP-client / networking API design, requirements engineering) and
  applies it. (At the time this subtree was authored the engine's methodology loader was returning
  `agent_domain_unset`; if a child meets the same condition it proceeds on its brief and the design persona,
  and records the assumption — it does not block on methodology.)

---

## Input Specifications

| Source | Location | Purpose |
|--------|----------|---------|
| This subtree hub | `_GLOBAL.md` (this file) | Shared context + constraints for the two spokes and the gate. |
| This subtree's contract | `contracts/_MANIFEST.yaml` | Sub-register ownership + the identities the gate asserts. |
| Parent contract | `../contracts/` | The `REQ-<AREA>-*` / `BAR-FERRIC-*` schema, verification-method and stage vocab, artifact map. READ-ONLY. |
| 1.0 requirements frame | `../SUBTASK_scope_and_requirements/scope-and-requirements.md` | `REQ-FW-007` (routing + HTTP), `REQ-FW-009` (frozen surfaces additive), the `usable_early`/`one_oh` staging, personas and journeys to specialize. |
| Router scaffold (#5) | `crates/ferric-router/` in `Nousix-LLC/nswe-demo` @ `276138f` (frozen `prelude`, README) | What exists to extend additively — do not duplicate. Read the real crate. |
| HTTP scaffold (#6) | `crates/ferric-http/` in `Nousix-LLC/nswe-demo` @ `276138f` (frozen `prelude`, README) | What exists to extend additively — do not duplicate. Read the real crate. |
| Board issues | #5 `ferric-router`, #6 `ferric-http`, under epic #1 | The issues to fold; read their current scope on the board. |
| Peer precedent | leptos_router, Dioxus router (routing); `reqwest`, `gloo-net` (fetch) | Named, honest comparison. |

The frozen surfaces, stated by the parent for grounding: `ferric-router` exposes `Params`, `RoutePattern`,
`Router`, `navigate`, `current_path`, `link`; `ferric-http` exposes `Client` / `ClientBuilder`,
`RequestBuilder`, `Response`, `Error` / `Result`. Each spoke reads the real crate to confirm the exact surface.

---

## Task Structure

### Overview

```
_GLOBAL.md (this hub)
├── contracts/                      (sub-contract — READ-ONLY for descendants)
│   └── _MANIFEST.yaml
├── SUBTASK_router/                 (spoke — owns REQ-RT-*, folds #5)
│   └── _BRIEF.md                   → router.md
├── SUBTASK_http/                   (spoke — owns REQ-HTTP-*, folds #6)
│   └── _BRIEF.md                   → http.md
└── SUBTASK_synthesis/              (synthesis gate — composes + verifies)
    └── _BRIEF.md                   → router-and-http.md (the deliverable) + SYNTHESIS.md (fold)
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_router` | none | Router design: route table, path params, nested routes, in-app links + History-API navigation, reactive outlet; relationship to the frozen `ferric-router` surface and what the 1.0 adds; the fold of #5; named peer comparison (leptos_router, Dioxus router). Owns `REQ-RT-*`. | `router.md` |
| `SUBTASK_http` | none | HTTP/JSON client design: typed JSON fetch (serde), request building, error model incl. non-2xx; relationship to the frozen `ferric-http` surface and what the 1.0 adds; the fold of #6; named peer comparison (`reqwest`, `gloo-net`). Owns `REQ-HTTP-*`. | `http.md` |
| `SUBTASK_synthesis` | `SUBTASK_router`, `SUBTASK_http` | Verify the identities below over both spoke outputs (no silent plugs), then compose the two into the single deliverable `router-and-http.md` at the parent workspace and fold this subtree. | `router-and-http.md`, `SYNTHESIS.md` |

### Dependency Graph

```
SUBTASK_router ──┐
                 ├── SUBTASK_synthesis
SUBTASK_http  ───┘
```

---

## Contract

The sub-contract lives in `contracts/` (read-only for descendants). It is thin because the seam is thin: the
two spokes share one id/traceability scheme (already fixed by the parent contract), a consistent per-doc
section layout so the gate can compose them mechanically, and the identities the gate asserts. It **extends**
the parent contract (it partitions this subtree's two namespaces between the two spokes and adds composition
identities); it does not override anything the parent declared.

**Contract location**: `contracts/` · **Contract kind**: `yaml_schema` (manifest of ownership + identities)

### Ownership (within this subtree)

| Child | Owns | Output file |
|---|---|---|
| `SUBTASK_router` | `REQ-RT-*` register | `router.md` (its workspace) |
| `SUBTASK_http` | `REQ-HTTP-*` register | `http.md` (its workspace) |
| `SUBTASK_synthesis` | the composed deliverable + the fold | `router-and-http.md` (parent workspace), `SYNTHESIS.md` (parent workspace) |

### Identities (the synthesis gate asserts these; no silent plugs)

- [ ] **SI1 — disjoint sub-registers.** `SUBTASK_router` writes only `REQ-RT-*`; `SUBTASK_http` writes only
      `REQ-HTTP-*`. The two namespaces do not overlap. (Realizes parent I1 within this subtree.)
- [ ] **SI2 — additive over frozen surfaces.** Each spoke's design is additive over its crate's frozen
      `prelude`; any change to an existing exported item is called out as additive, never a silent
      redefinition. (Realizes parent I9.)
- [ ] **SI3 — fold recorded, not duplicated.** `router.md` states how board issue #5 is superseded/extended;
      `http.md` states how #6 is superseded/extended. (Feeds parent I7.)
- [ ] **SI4 — composed once.** The gate composes both registers into one `router-and-http.md` that lands exactly
      once at `design/ferric/router-and-http.md`; neither spoke's content is dropped or double-placed. (Realizes
      parent I8.)
- [ ] **SI5 — realizes REQ-FW-007.** The combined `REQ-RT-*` / `REQ-HTTP-*` registers cover the cross-cutting
      `REQ-FW-007` surface: client routing with params, nested routes, and in-app links, plus a typed JSON
      request/response that handles a non-2xx status as an error.
- [ ] **SI6 — testable criteria.** Every `REQ-RT-*` / `REQ-HTTP-*` has ≥1 acceptance criterion a stranger could
      check, using a `verification_method` from the parent schema (`automated_test` / `example_build` /
      `doc_inspection` for this area).

### Derived artifacts
- The two spoke docs (`router.md`, `http.md`) are the source the gate composes into `router-and-http.md`.
- `router-and-http.md` is the artifact `SUBTASK_design_pr` places at `design/ferric/router-and-http.md`.

---

## Output Specifications

| Deliverable | Location | Description |
|-------------|----------|-------------|
| `router.md` | `SUBTASK_router/` | Router design + `REQ-RT-*` register + #5 fold. |
| `http.md` | `SUBTASK_http/` | HTTP/JSON client design + `REQ-HTTP-*` register + #6 fold. |
| `router-and-http.md` | this subtree root (parent workspace) | The composed deliverable; repo target `design/ferric/router-and-http.md`. |
| `SYNTHESIS.md` | this subtree root (parent workspace) | The fold record: identity verdicts + how the two were composed. |
