# Concern Findings — Router + HTTP/JSON Client

## concern_name

Router + HTTP/JSON Client (`REQ-RT-*` · `REQ-HTTP-*`)

## document_validated

`design/ferric/router-and-http.md` on branch `work/design-ferric-1_0`

## req_ids_found

### REQ-RT-* (defined in Part 1)

- REQ-RT-001 — Declarative route table with path parameters
- REQ-RT-002 — Reactive outlet that re-renders on path change
- REQ-RT-003 — History-API navigation: push, replace, back/forward, reactive current path
- REQ-RT-004 — In-app links that navigate client-side
- REQ-RT-005 — Nested routes with a nested outlet
- REQ-RT-006 — No-match (fallback) handling at each routing level
- REQ-RT-007 — Active-route awareness for links
- REQ-RT-008 — Composition over the frozen surface, additive-only
- REQ-RT-009 — Query/search-string parameters (recorded post-1.0 deferral)

### REQ-HTTP-* (defined in Part 2)

- REQ-HTTP-001 — One configured, shareable client
- REQ-HTTP-002 — Fluent per-request construction
- REQ-HTTP-003 — Correct URL resolution and RFC-3986 query encoding
- REQ-HTTP-004 — Typed JSON request body with a defaulted Content-Type
- REQ-HTTP-005 — Safe-by-default typed round-trip, with a raw escape hatch
- REQ-HTTP-006 — Response as owned, synchronously-inspectable data
- REQ-HTTP-007 — One matchable error type over every failure mode
- REQ-HTTP-008 — Non-2xx is an error on the safe path
- REQ-HTTP-009 — Broader HTTP method coverage, added additively
- REQ-HTTP-010 — Per-request timeout and cancellation
- REQ-HTTP-011 — Composes with the view framework and async layer; no view dependency
- REQ-HTTP-012 — Lean, documented dependency footprint
- REQ-HTTP-013 — Frozen surface carried forward additively

## status

needs-fix

## specific_issues

### Issue 1

- **type**: completeness
- **description**: The explicit REQ-FW-007 traceability table present in the prior-art draft (`## How the two parts realize REQ-FW-007`, prior-art lines 739–751) is absent from the branch version. The branch Overview describes the coverage in narrative form ("Together they cover the cross-cutting `REQ-FW-007` surface…"), and individual requirements carry read-only `REQ-FW-007` references, but there is no consolidated table mapping each REQ-FW-007 element (client routing with route parameters, nested routes, in-app links, typed JSON request/response, non-2xx as an error) to its covering requirement(s). The table existed in the prior-art as a designed coherence check and is the evidence that `REQ-FW-007` is fully covered by the combined registers.
- **severity**: minor

### Issue 2

- **type**: coherence
- **description**: The branch version Metadata section contains the line "**Identities asserted (SI1–SI6):** all PASS — see `SYNTHESIS.md` at this workspace for verdicts." `SYNTHESIS.md` is an internal taskflow authoring artifact (the fold record) rather than a file that belongs in or alongside the design deliverable. The prior-art does not carry this reference. A design document that cites an internal process file as the evidence source for its own identity verdicts creates a dangling dependency for any reader or reviewer who picks up the document without access to the taskflow workspace.
- **severity**: minor

### Validation criteria — all pass

The following criteria from the task brief were assessed and pass:

1. **Additive over issues #5/#6 — PASS.** The branch version states both issues CLOSED, maps the shipped capabilities to `REQ-RT-*` / `REQ-HTTP-*` carried-forward ids, and scopes all new work as explicitly additive. No duplication or contradiction with the frozen surfaces.

2. **Reconciles prior-art drafts without dropping content — PASS (minor note at Issue 1).** All requirements, peer comparisons, board folds, and relationship-to-frozen sections from the prior-art are present in the branch version. The only missing element is the standalone REQ-FW-007 coverage table (Issue 1 above).

3. **Nested routes addressed with testable requirements — PASS.** REQ-RT-005 carries three acceptance criteria with explicit `verification_method` values: `automated_test` (two-level config, `cargo test`), `example_build` (persistent parent layout example), `doc_inspection` (guide documents nested outlet).

4. **Route parameters addressed — PASS.** REQ-RT-001 covers declarative route table with named `:param` segments; acceptance criteria include a native `cargo test` for parameter extraction and an `example_build`.

5. **Active-link state addressed — PASS.** REQ-RT-007 covers active-route awareness; acceptance criteria include `automated_test` (active marker present/absent), `example_build` (visible marking), and `doc_inspection` (styling guide).

6. **Typed JSON request/response addressed — PASS.** REQ-HTTP-004 (typed request body via `serde::Serialize`), REQ-HTTP-005 (safe-by-default typed round-trip via `send_json`), and REQ-HTTP-006 (owned synchronously-inspectable response) collectively cover this surface, each with `automated_test` acceptance criteria.

7. **Per-request timeouts addressed — PASS.** REQ-HTTP-010 covers timeout and cancellation via `RequestBuilder::timeout` and/or an abort handle; acceptance criterion is a headless `wasm-bindgen-test` against a never-responding stub.

8. **REQ-RT-* and REQ-HTTP-* prefixes used correctly — PASS.** Part 1 defines only `REQ-RT-001`–`REQ-RT-009`; Part 2 defines only `REQ-HTTP-001`–`REQ-HTTP-013`. Every cross-reference to the other register (and to `REQ-FW-*`, `REQ-ASYNC-*`, `REQ-PERF-*`, `REQ-REL-*`) is marked read-only within the section that cites it. No prefix mixing.

## gaps

### GAP-040

- **id**: GAP-040
- **description**: The REQ-FW-007 explicit coverage map table is absent from the branch version. The prior-art draft included a dedicated section (`## How the two parts realize REQ-FW-007`) with a table mapping each element of the cross-cutting requirement to its covering `REQ-RT-*` / `REQ-HTTP-*` id(s). The branch version addresses this only in the Overview paragraph. Without the table, a reviewer checking that the combined registers fully discharge `REQ-FW-007` must reconstruct the mapping by hand.
- **severity**: minor
- **action_required**: Add a `## How the two parts realize REQ-FW-007` section (or equivalent coverage map) to the branch version, mapping each REQ-FW-007 element to its covering requirement(s). This can be placed at the end of the document before or within the Metadata section. The prior-art table at lines 739–751 is the correct model.

### GAP-041

- **id**: GAP-041
- **description**: The Metadata section references `SYNTHESIS.md` as the source for identity verdicts ("**Identities asserted (SI1–SI6):** all PASS — see `SYNTHESIS.md` at this workspace for verdicts."). `SYNTHESIS.md` is the taskflow fold record from the authoring DAG, not a deliverable or companion file to the design document. The prior-art version does not carry this reference. Readers and reviewers who encounter the design document outside the taskflow workspace cannot follow this reference.
- **severity**: minor
- **action_required**: Either remove the `SYNTHESIS.md` reference and record the identity verdicts inline in the Metadata section (matching the style of the prior-art version), or reword to omit the external-artifact reference while preserving the provenance note.
