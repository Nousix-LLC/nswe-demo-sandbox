# SYNTHESIS — SUBTASK_router_and_http (router + HTTP/JSON client)

**Gate:** `SUBTASK_rt_http_synthesis` (workspace `SUBTASK_synthesis/`) · **Status:** completed ·
**Evaluation:** Atomic
**Fold target:** `SUBTASK_router_and_http` (`SUSPENDED → COMPLETED`) · **Seam:** this file.

This is the fold record for the router + HTTP/JSON client subtree. It records the per-identity verdicts the gate
asserted over the two completed spoke outputs and how those outputs were composed into the single deliverable
`router-and-http.md` at this workspace. No failing identity was patched over; every verdict below is evidenced
from the spoke files.

## Inputs read

| Input | Path | State |
|---|---|---|
| Sub-contract (identities + `doc_layout`) | `contracts/_MANIFEST.yaml` | read |
| Router spoke output (`REQ-RT-*`) | `SUBTASK_router/router.md` | COMPLETED |
| HTTP/JSON client spoke output (`REQ-HTTP-*`) | `SUBTASK_http/http.md` | COMPLETED |
| Parent id/traceability schema | `../contracts/id_and_traceability_schema.yaml` | read (READ-ONLY) |
| Parent artifact map | `../contracts/design_artifact_map.yaml` | read (READ-ONLY) |
| Subtree hub | `_GLOBAL.md` | read |

## Identity verdicts (SI1–SI6)

### SI1 — disjoint sub-registers — PASS
`router.md` defines `REQ-RT-001`…`REQ-RT-009` and no other id; `http.md` defines `REQ-HTTP-001`…`REQ-HTTP-013`
and no other id. Every mention of a foreign register in either file (`REQ-FW-*`, `REQ-ASYNC-*`, and each spoke's
mention of the other's ids) is marked read-only. The `RT` and `HTTP` prefixes do not overlap. Realizes parent I1
within this subtree.

### SI2 — additive over frozen surfaces — PASS
- Router: a dedicated relationship-to-frozen section carries forward `Params`, `RoutePattern`, `Router`,
  `navigate`, `current_path`, and `link` with unchanged signatures, and flags each 1.0 addition as additive —
  nested routes (`REQ-RT-005`), replace-navigation (`REQ-RT-003`), active-link (`REQ-RT-007`), per-level nested
  fallback (`REQ-RT-006`) — with `REQ-RT-008` stating the additive-only condition as a testable requirement.
- HTTP: the frozen `ferric-http` `prelude` (`Client`/`ClientBuilder`, `Method`, `RequestBuilder`, `Response`,
  `Error`/`Result`) is ratified and carried forward, with only two additions, each flagged: `Method::Patch`
  under a newly-`#[non_exhaustive]` `Method` (`REQ-HTTP-009`) and a `RequestBuilder::timeout`/abort plus a new
  `Error` variant (`REQ-HTTP-010`, additive by construction since `Error` is already `#[non_exhaustive]`);
  `REQ-HTTP-013` states the carry-forward.
- Both correctly treat the one subtle case — marking an enum `#[non_exhaustive]` — as a semver-recorded surface
  fact rather than a redefinition of an existing variant. No frozen item is removed or silently redefined.
Realizes parent I9.

### SI3 — fold recorded, not duplicated — PASS
`router.md` §"Board fold — issue #5" records #5 as CLOSED/delivered baseline, maps the shipped capabilities to
the carried-forward `REQ-RT-*` ids, scopes the new work to the additive capabilities, and instructs the release
plan to file new work under epic #1 with `supersedes: #5` rather than duplicate. `http.md` §"Board fold —
issue #6" records #6 as CLOSED/landed the usable_early core, scopes the additive 1.0 work to `REQ-HTTP-009`/`010`,
and instructs the backlog to cite #6 in `supersedes` rather than open a duplicate. Feeds parent I7.

### SI4 — composed once — PASS (realized by this gate)
Both full registers and both board-fold sections are composed into one `router-and-http.md` at this workspace,
under a combined overview framing routing + backend data as the app-integration surface. Nothing was dropped:
every `REQ-RT-001`…`009` and `REQ-HTTP-001`…`013` entry, both register summaries, both peer comparisons, and
both folds are present. Nothing was double-placed: the document lands exactly once here, and
`design_artifact_map.yaml` assigns a single repo path `design/ferric/router-and-http.md` (owner
`SUBTASK_router_and_http`) for `SUBTASK_design_pr` to place it. Realizes parent I8.

### SI5 — realizes REQ-FW-007 — PASS
The combined registers cover every element of the cross-cutting `REQ-FW-007` surface:

| `REQ-FW-007` element | Covered by |
|---|---|
| Client routing with route parameters | `REQ-RT-001` |
| Nested routes | `REQ-RT-005` |
| In-app links | `REQ-RT-004` (+ navigation `REQ-RT-002`, `REQ-RT-003`) |
| Typed JSON request/response | `REQ-HTTP-004`, `REQ-HTTP-005`, `REQ-HTTP-006` |
| Non-2xx status treated as an error | `REQ-HTTP-008` (+ `REQ-HTTP-005`) |

### SI6 — testable criteria — PASS (with one recorded nuance)
Every release-gating requirement carries at least one stranger-checkable acceptance criterion naming a
parent-schema `verification_method` (`automated_test` / `example_build` / `doc_inspection`):
- Router `REQ-RT-001`–`REQ-RT-008` (all `release_gating: true`): each has ≥1 such criterion.
- HTTP `REQ-HTTP-001`–`REQ-HTTP-013` (all `release_gating: true`): each has ≥1 such criterion.

Nuance: `REQ-RT-009` (query/search params) carries no acceptance criterion. It is a `stage: post_one_oh`,
`release_gating: false` deferral, which the parent schema's trace rule ("no out-of-1.0 item is enforced by any
`BAR-FERRIC-*`") legitimately leaves un-gated. SI6 binds release-gating requirements; this deferral is outside
its scope, so SI6 holds. Recorded here so the absence is explicit, not a gap.

## How the two were composed

The deliverable follows the sub-contract `doc_layout`. A short combined overview opens it, framing the router and
the HTTP/JSON client as the two halves of the app-integration surface and stating that both specialize
`REQ-FW-007` and are held to `REQ-FW-009`. The two spoke bodies follow whole, under `## Part 1 — Client-side
router` and `## Part 2 — HTTP/JSON client`, each preserving its `doc_layout` sections (overview,
relationship-to-frozen, requirements register, peer comparison, board fold). A combined register summary and a
`REQ-FW-007` coverage map close the body. This was a mechanical compose-and-verify: no requirement was
re-authored, no `REQ-*` id was added or renamed, and no spoke content was altered in substance (spoke heading
levels were demoted to nest under the two parts).

## Deliverable placed

- `router-and-http.md` at this workspace (`SUBTASK_router_and_http/`) — the composed deliverable; repo target
  `design/ferric/router-and-http.md`, placed by `SUBTASK_design_pr` per `design_artifact_map.yaml`.
- `SYNTHESIS.md` at this workspace (this file) — the fold record and the seam `engine_resume_suspended` consumes.

## Fold

With all six identities passing and the deliverable composed and placed, this gate folds the subtree: the parent
`SUBTASK_router_and_http` moves `SUSPENDED → COMPLETED` via `engine_resume_suspended` with this `SYNTHESIS.md` as
the seam. The two spoke outputs and this deliverable are its resolved result.

## Assumption recorded

The engine methodology loader returned `agent_domain_unset` throughout this invocation, as the subtree hub
anticipated and as both spokes recorded. Composition and verification proceeded from the brief, the sub-contract
and parent contracts, the two spoke outputs, and the product-design persona, applying requirements-engineering
judgment. No methodology bundle was loadable; the gate did not block on it.

## Writing-voice pass

The combined overview and this record were checked by hand against the avoid-ai-writing P0/P1 patterns (the
methodology loader being unavailable): no character adjective on a character-less noun, no narrated candor, no
unpaired contrast, no slot-fill template, no padded triad, no hollow intensifier. The spoke bodies were carried
through as their authors wrote them, each having run its own pass.
