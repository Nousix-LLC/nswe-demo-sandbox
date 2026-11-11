# COMPLETE — SUBTASK_http (Ferric 1.0 HTTP/JSON client design)

## Status
Completed. Declared output `http.md` authored at this task's workspace.

## What was done
Designed the Ferric 1.0 HTTP/JSON client to a testable bar, following the sub-contract's `doc_layout`
(overview → relationship-to-frozen-surface → `REQ-HTTP-*` register → peer comparison → #6 fold) and conforming
to `../../contracts/id_and_traceability_schema.yaml`.

- **Register `REQ-HTTP-001`–`REQ-HTTP-013`** covering the three facets of the one capability — request building
  (001–003), typed JSON fetch (004–006), the error model incl. non-2xx (007–008) — plus the two additive 1.0
  additions (009 broader methods, 010 timeout/cancellation), composition + footprint + additivity (011–013).
  Each item has a what-not-how statement, peer-grounded rationale, ≥1 stranger-checkable acceptance criterion
  with a parent-schema `verification_method` (`automated_test` / `example_build` / `doc_inspection`), a `stage`
  (`usable_early` / `one_oh`), and `release_gating: true`.
- **Additive over the frozen surface (SI2 / parent I9):** the exact frozen `prelude`
  (`Client`/`ClientBuilder`, `RequestBuilder`, `Response`, `Error`/`Result`, `Method`) read from the real crate
  and ratified as the 1.0 baseline; the only changes are additions, each flagged — `Method::Patch` under a new
  `#[non_exhaustive]`, a `RequestBuilder::timeout`/abort handle, and a new (already-`#[non_exhaustive]`) `Error`
  variant. `REQ-HTTP-013` states the additive carry-forward as a requirement.
- **#6 fold (SI3 / feeds parent I7):** board issue #6 is CLOSED and landed the `usable_early` core; the 1.0
  work extends it. Recorded that the release plan/backlog should cite #6 as the scaffold the 1.0 epic
  supersedes/extends (via `supersedes`) rather than file a duplicate.
- **Peer comparison:** `reqwest` and `gloo-net` compared by name on transport, client object, typed bodies,
  safe-by-default status, error model, timeout, and WASM weight.

## Grounding
Read `crates/ferric-http/src/{lib,client,request,response,error}.rs` and `Cargo.toml`/`README.md` in
`Nousix-LLC/nswe-demo` @ `276138f` directly (not the parent summary), plus board issue #6 and epic #1. A
grounding correction is recorded in `http.md`: `ferric-http`'s core is implemented and natively tested at the
baseline, not a `todo!()` shell — the design ratifies and sets the bar over that real surface.

## Identities honored
SI1 (only `REQ-HTTP-*` ids written; cross-refs read-only), SI2 (additive over frozen), SI3 (#6 fold),
SI5 (realizes the HTTP half of `REQ-FW-007`, incl. non-2xx-as-error), SI6 (every REQ has a checkable AC with a
schema `verification_method`). SI4 (composed once) is the synthesis gate's to assert.

## Constraints honored
Design not implementation (surface/requirement/bar, not fetch internals); repository-only naming (no
host/cluster/SSH/path detail); lean footprint (`REQ-HTTP-012`, no heavy runtime); writing-voice rules applied
with a by-hand avoid-ai-writing pass (one narrated-candor tell removed; no character adjectives on
character-less nouns, no slot-fill templates, no padded triads, no hollow intensifiers).

## Assumption recorded
The engine methodology loader was unavailable this invocation (`engine_load_methodology` /
`engine_methodology_glob` returned `agent_domain_unset`, empty `agent_id`). Per the brief's and the subtree
hub's explicit instruction, I proceeded on the brief, the inherited contracts, the requirements frame, and the
design persona (HTTP-client / networking API design + requirements engineering applied from the persona), and
did not block on methodology.

## Output
- `http.md` — the HTTP/JSON client design + `REQ-HTTP-*` register + #6 fold (this task's workspace). Source for
  the synthesis gate's `router-and-http.md`.
