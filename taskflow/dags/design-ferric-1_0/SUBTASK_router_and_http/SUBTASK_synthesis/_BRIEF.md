# Task: Ferric 1.0 — router + HTTP synthesis gate (compose + verify, then fold)

## Task Specification
**Slug**: SUBTASK_synthesis
**Task Kind**: synthesis
**Status**: Pending

### Objective
Verify the router and HTTP/JSON client designs against this subtree's contract identities, then compose them
into the single deliverable `router-and-http.md` at the parent workspace and fold this subtree back into its
parent.

### Context
This is the synthesis gate for the router + HTTP/JSON client concern (subtree hub: `../_GLOBAL.md`). Its two
spokes — `SUBTASK_router` (owns `REQ-RT-*`, output `router.md`) and `SUBTASK_http` (owns `REQ-HTTP-*`, output
`http.md`) — have completed. This gate reads both, asserts the identities in `../contracts/_MANIFEST.yaml`
mechanically (no silent plugs: a failed identity is reported as a structured signal, not patched over), and
composes the two registers into one document that conforms to the per-doc section layout. The combined document
is this concern's contribution to the Ferric 1.0 design PR; it must land exactly once at
`design/ferric/router-and-http.md` (parent identity I8).

**Dependencies**: `SUBTASK_router`, `SUBTASK_http`.

### Scope to cover
- **Assert the identities** in `../contracts/_MANIFEST.yaml` over the two spoke outputs: SI1 (disjoint
  registers — no `REQ-RT-*`/`REQ-HTTP-*` overlap), SI2 (additive over frozen surfaces; additions flagged),
  SI3 (#5 and #6 folds both present), SI4 (both registers composed, none dropped/double-placed), SI5 (the
  combined registers realize `REQ-FW-007`: params, nested routes, links, typed JSON fetch, non-2xx as error),
  SI6 (every REQ has ≥1 stranger-checkable acceptance criterion with a schema `verification_method`). Report
  each verdict; if one fails, surface it rather than reconcile it silently.
- **Compose** `router.md` and `http.md` into `router-and-http.md` at the parent workspace, preserving both full
  registers and both #5/#6 fold statements, with a short combined overview framing the two capabilities as the
  app-integration surface (routing + backend data) of Ferric 1.0. Repo target `design/ferric/router-and-http.md`.
- **Fold** this subtree into its parent per the kernel's synthesis-fold contract.

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | The composed-deliverable spec and success criteria. |
| Sub-contract | `../contracts/_MANIFEST.yaml` | The identities to assert and the `doc_layout` to compose to. |
| Router design | `../SUBTASK_router/router.md` | The `REQ-RT-*` register + #5 fold to compose in. |
| HTTP design | `../SUBTASK_http/http.md` | The `REQ-HTTP-*` register + #6 fold to compose in. |
| Parent contract | `../../contracts/id_and_traceability_schema.yaml`, `../../contracts/design_artifact_map.yaml` | The id schema the registers conform to; the artifact map placing `router-and-http.md` at its repo path. READ-ONLY. |

### Declared output
- `router-and-http.md` at the **parent** workspace (`../`) — the composed deliverable; repo target
  `design/ferric/router-and-http.md`.
- `SYNTHESIS.md` at the **parent** workspace (`../`) — the fold record: the per-identity verdicts (SI1–SI6) and
  how the two spoke outputs were composed. This is both this task's terminal record and the record the fold
  consumes.

### Success criteria
- [ ] Every identity SI1–SI6 is evaluated with an explicit pass/fail verdict recorded in `SYNTHESIS.md`; no
      failing identity is silently patched.
- [ ] `router-and-http.md` contains both the full `REQ-RT-*` and `REQ-HTTP-*` registers and both #5/#6 fold
      statements, conforming to the parent id schema, placed exactly once at the parent workspace for the repo
      path `design/ferric/router-and-http.md`.
- [ ] The subtree is folded into its parent (the parent task `SUBTASK_router_and_http` reaches COMPLETED via the
      fold).

### Constraints
- Mechanical gate, not a rewrite: compose the spokes' content and verify; do not re-author their requirements or
  add new `REQ-*` ids. Design, not implementation.
- Repository `Nousix-LLC/nswe-demo` only; nothing on GitHub carries host/cluster/SSH/path/environment detail.
- Honor the writing-voice rules on the composed overview and the fold record (plain, checkable prose; no
  machine-writing tells; run the avoid-ai-writing pass before finalizing).
