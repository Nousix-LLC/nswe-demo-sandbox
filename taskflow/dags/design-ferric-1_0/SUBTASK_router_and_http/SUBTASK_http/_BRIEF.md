# Task: Ferric 1.0 — HTTP/JSON client design (owns REQ-HTTP-*; folds board issue #6)

## Task Specification
**Slug**: SUBTASK_http
**Task Kind**: standard
**Status**: Pending

### Objective
Design the Ferric 1.0 **HTTP/JSON client** — the capability a Rust/WASM app author uses to talk to a JSON/REST
backend — to a testable bar, reconciled additively with the existing frozen `ferric-http` surface, and state
how board issue #6 is superseded/extended by this design.

### Context
This is one spoke of the router + HTTP/JSON client concern of the Ferric 1.0 framework design (subtree hub:
`../_GLOBAL.md`). You own the `REQ-HTTP-*` register and nothing else. The router is a sibling spoke
(`SUBTASK_router`, owns `REQ-RT-*`); a synthesis gate composes both into one deliverable. `ferric-http` exists
today as a walking-skeleton composition root with a **frozen public `prelude` surface** — the parent records it
as exposing `Client` / `ClientBuilder`, `RequestBuilder`, `Response`, `Error` / `Result`, with many leaf bodies
still `todo!()`. Read the real crate to confirm the exact surface. The 1.0 client design must build on that
frozen surface **additively** (identity SI2 / parent I9): extend it, never silently redefine or duplicate it.

**Dependencies**: none (sibling of `SUBTASK_router`; both read the same upstream inputs).

### Scope to cover
This is the HTTP/JSON client as one coherent capability, with these facets, each carried to a testable
`REQ-HTTP-*`:
- **typed JSON fetch** (serde-based request and response bodies) — the common case of posting and receiving
  typed data against a REST backend;
- **request building** (method, URL, headers, query, body) over the frozen `RequestBuilder` / `ClientBuilder`;
- the **error model**: how transport failures, non-2xx statuses, and deserialization failures surface to the
  author through `Error` / `Result` (treating a non-2xx status as an error is part of the `REQ-FW-007` bar);
- the **relationship to the frozen `ferric-http` surface**: what each existing `prelude` item is in the 1.0,
  and exactly what the 1.0 adds on top — every addition flagged as additive;
- the **fold of board issue #6**: what #6 becomes under the 1.0 plan (superseded or extended), so the release
  plan and backlog filing edit #6 rather than duplicate it.
Name these as the facets of one capability; your own evaluation decides whether they are one atomic design or
warrant their own sub-decomposition.

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints, the identities your output is held to. |
| Sub-contract | `../contracts/_MANIFEST.yaml` | Your register ownership (REQ-HTTP-*), the per-doc section layout, the identities. |
| Parent contract | `../../contracts/id_and_traceability_schema.yaml`, `../../contracts/_MANIFEST.yaml` | The REQ id schema, acceptance-criterion fields, `verification_method` and `stage` vocabularies. READ-ONLY. |
| 1.0 requirements frame | `../../SUBTASK_scope_and_requirements/scope-and-requirements.md` | `REQ-FW-007` (HTTP client), `REQ-FW-009` (frozen surfaces additive), `REQ-FW-013` (lean footprint — serde/wasm-bindgen-futures is the expected per-crate addition), personas A1/A2, journey JA2. Specialize these; do not re-mint `REQ-FW-*`. |
| HTTP scaffold (#6) | `crates/ferric-http/` in `Nousix-LLC/nswe-demo` @ `276138f` (frozen `prelude`, README) | The exact frozen surface to extend additively. Read it; do not trust the summary alone. |
| Board issue #6 | `ferric-http` under epic #1, board `NSWE Delivery` | Its current scope, so you can state the fold. |
| Peer HTTP clients | `reqwest`, `gloo-net` | Named, honest comparison of fetch/JSON-client models (typed bodies, builder ergonomics, error handling, WASM fetch). |

### Declared output
- `http.md` (this task's workspace) — the HTTP/JSON client design following the sub-contract's `doc_layout`:
  overview, relationship-to-frozen-surface (+ what 1.0 adds), the `REQ-HTTP-*` register with testable
  acceptance criteria, named peer comparison, and the #6 fold statement.

### Success criteria
- [ ] Typed JSON fetch, request building, and the error model (including non-2xx handling) are each specified
      with testable `REQ-HTTP-*` acceptance criteria conforming to
      `../../contracts/id_and_traceability_schema.yaml` (each criterion checkable by a stranger, using a
      `verification_method` from the schema).
- [ ] The design is additive over the frozen `ferric-http` `prelude`; any change to an existing item is flagged
      additive, never a silent redefinition (SI2 / I9).
- [ ] The #6 fold is explicit — what #6 becomes under the 1.0 plan (SI3 / feeds I7).
- [ ] `reqwest` and `gloo-net` are compared by name.
- [ ] You write only `REQ-HTTP-*` ids (SI1 / I1); cross-references to other registers are read-only.

### Constraints
- Design, not implementation (what, not how). State the user-facing requirement, the architecture, and the
  testable bar; do not choose the fetch wrapper internals or serialization code path.
- Repository `Nousix-LLC/nswe-demo` only; nothing on GitHub carries host/cluster/SSH/path/environment detail.
- Keep the dependency footprint defensible (`REQ-FW-013`): a narrowly-scoped `serde` / `wasm-bindgen-futures`
  addition is the expected example; do not introduce a heavy general-purpose runtime.
- Select and load your own methodology (HTTP-client / networking API design, requirements engineering) and
  apply it. If the engine's methodology loader is unavailable, proceed on this brief and the design persona and
  record the assumption. Honor the writing-voice rules (plain, checkable prose; no machine-writing tells; run
  the avoid-ai-writing pass before finalizing).
