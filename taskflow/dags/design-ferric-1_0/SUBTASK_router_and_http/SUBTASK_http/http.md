# Ferric 1.0 — HTTP/JSON client design (`REQ-HTTP-*`)

*Design area: the HTTP/JSON client an app author uses to talk to a REST backend. Owns the `REQ-HTTP-*`
register. One spoke of the router + HTTP/JSON client concern (`../_GLOBAL.md`); the router is the sibling
`REQ-RT-*`. Conforms to `../../contracts/id_and_traceability_schema.yaml`. Grounded in `Nousix-LLC/nswe-demo`
at `276138f`. This is design — what the client must do and the bar it is held to — not how the fetch path is
coded.*

---

## Overview

*(section: `overview`)*

Ferric's HTTP/JSON client is the capability an application author (persona A2) reaches for when a Ferric
single-page app needs to read from and write to a JSON/REST backend — the `chirp-frontend` talking to
`chirp-server` is the first real case. The author configures a client once (a base URL and the headers every
request carries, such as `Authorization`), then for each call picks a verb, a path, query parameters and a
typed request body, and `await`s a typed response. Request and response bodies are ordinary `serde` types, so
the author works in their own structs rather than in JSON strings. Every failure — a request that could not be
built, a network call that never reached the server, a non-2xx status, or a body that would not
(de)serialize — arrives as one matchable `Error`, so the calling code can branch on *why* a call failed.

The evaluating author (persona A1) weighs this client against `reqwest` and `gloo-net` when deciding whether
Ferric can carry a real data-backed app. The client is built on the browser Fetch API and keeps a lean
dependency set so the WASM bundle stays small; it does not depend on the `ferric` view crate, so it is usable
on its own and composes with the view framework and the async/resource layer (`REQ-ASYNC-*`) rather than
assuming them. This client realizes the HTTP half of the cross-cutting `REQ-FW-007` (client routing and an
HTTP/JSON client) and is one of the capabilities the `usable_early` floor depends on: an author cannot build a
real app without being able to fetch and post typed data with real error states.

The companion crate `ferric-http` already exists at the baseline with a frozen public surface and an
implemented, natively-tested core. This design ratifies that surface as the 1.0 baseline, states the testable
bar the client is held to, and names the small additions a credible 1.0 adds on top — each addition flagged
additive so no existing item is silently redefined (identity SI2 / parent I9).

---

## Relationship to the frozen `ferric-http` surface

*(section: `relationship_to_frozen`; realizes SI2 / parent I9 — every change below is additive)*

### What exists at the baseline (`276138f`), read from the crate

`ferric-http`'s public surface is its `prelude` plus the crate-root re-exports. Confirmed by reading
`crates/ferric-http/src/{lib,client,request,response,error}.rs` — not the summary alone. The frozen exported
items are:

| Exported item | What it is at the baseline |
|---|---|
| `Client` | Holds an optional base URL + default headers; `Clone`, `Default`, holds no connection state. Verb entries `get`/`post`/`put`/`delete(path)` and a generic `request(Method, path)`; each returns a `RequestBuilder`. `new()`, `builder()`, `base_url()`. |
| `ClientBuilder` | `base_url(impl Into<String>)`, `default_header(name, value)`, `build()`. |
| `Method` | Enum `Get`/`Post`/`Put`/`Delete`; `as_str()`, `Display`. **Not** `#[non_exhaustive]` at the baseline. |
| `RequestBuilder` | Fluent `header`, `query(&[(&str,&str)])`, `json<B: Serialize>(&B) -> Result<Self>`, `body_string`, `url() -> String`; terminals `send() -> Result<Response>` and `send_json<T: DeserializeOwned>() -> Result<T>`. |
| `Response` | Owned data: `status`, `status_text`, `url`, `ok`, `headers`, case-insensitive `header(name)`, `body`, `text`, `json<T>()`, `error_for_status()` — all synchronous. |
| `Error` | `#[non_exhaustive]` enum: `Builder(String)`, `Network(String)`, `Status { status, status_text, url, body }`, `Serialize(serde_json::Error)`, `Deserialize(serde_json::Error)`, `Body(String)`; `is_network()`, `is_status()`, `status() -> Option<u16>`, `Display`, `std::error::Error` with `source`. |
| `Result<T>` | `std::result::Result<T, Error>`. |

The pure logic (URL base/path joining, RFC-3986 query percent-encoding, the `Response` accessors, serde
round-trips, and error mapping/`Display`) is implemented and covered by native `cargo test`; the Fetch call
in `RequestBuilder::send` is implemented against `web-sys` and exercised by a browser-gated `wasm-bindgen-test`
smoke test. The surface is therefore a real, usable baseline, not a `todo!()` shell. Earlier framing of the
companion crates as "`todo!()` skeletons" is correct for some leaves elsewhere but not for `ferric-http`'s
core, which this design treats as the ratified `usable_early` client.

### What the 1.0 adds, each additive

The 1.0 keeps every item above usable and unchanged (`REQ-HTTP-013` below), and adds only:

1. **Broader method coverage (`REQ-HTTP-009`).** Add `Method::Patch` and a `Client::patch(path)` verb entry.
   Because `Method` is not `#[non_exhaustive]` at the baseline, adding a variant would break a downstream
   exhaustive `match`; the additive-safe move is to mark `Method` `#[non_exhaustive]` as part of 1.0, then add
   `Patch` under it. The baseline variants and `as_str()`/`Display` are unchanged; the `#[non_exhaustive]`
   attribute is a new, semver-recorded surface fact, not a redefinition of an existing variant.
2. **Per-request timeout / cancellation (`REQ-HTTP-010`).** Add a `RequestBuilder::timeout(..)` (and/or an
   abort handle) and a new matchable `Error` variant for a timed-out/aborted request. The `Error` enum is
   already `#[non_exhaustive]` at the baseline, so a new variant is additive by construction. No existing
   variant changes.

No existing exported item is removed or redefined. If a future need forces a true break, it is signalled by
semver and recorded in the changelog (`REQ-REL-*`, read-only here), never applied silently — this is the
acceptance condition of `REQ-FW-009` restated for this crate.

---

## Requirements register (`REQ-HTTP-*`)

*(section: `requirements_register`. Each item: statement (what, not how), rationale (peer evidence where it
bears), acceptance criteria checkable by a stranger via a `verification_method` from the parent schema —
`automated_test` / `example_build` / `doc_inspection` — a `stage`, and `release_gating`. Cross-references to
other registers are read-only. SI1: only `REQ-HTTP-*` ids are defined here.)*

### A. Request building

#### REQ-HTTP-001 — One configured, shareable client
- **Statement:** An author configures a single `Client` with an optional base URL and a set of default headers
  and shares it across the whole app; the client is cheap to clone and carries no connection state of its own.
- **Rationale:** A SPA against one backend sets the base URL and the auth header once, not on every call.
  `reqwest::Client` is the shareable, clone-cheap connection holder authors expect; `gloo-net` has no client
  object at all, so base URL and headers are repeated per request — a gap this client closes. Ferric's client
  owns no connection (the browser's Fetch layer does), so sharing is just cloning a string and a small vector.
- **Acceptance criteria:** A native `cargo test` builds a client with `ClientBuilder::base_url(..)` and two
  `default_header(..)` calls and asserts (a) the resolved URL of an issued request includes the base URL and
  (b) the default headers are present on the produced `RequestBuilder`; a second test asserts a cloned client
  resolves identically to its source.
- **verification_method:** automated_test · **stage:** usable_early · **release_gating:** true
- **References:** REQ-FW-007, REQ-FW-009. *Satisfied by the frozen surface; carried forward additively.*

#### REQ-HTTP-002 — Fluent per-request construction
- **Statement:** For each request an author selects a method (a verb helper, or `Method` via the generic
  `request` entry), a path, appends query parameters, adds headers, and optionally sets a body, through a
  chainable `RequestBuilder` — without assembling a URL or header string by hand.
- **Rationale:** Builder ergonomics are the shared idiom of `reqwest` and `gloo-net`; hand-built URLs and
  header lists are where missing encoding and duplicated `?` separators hide. Keeping construction fluent and
  inspectable moves those bugs into tests rather than into runtime 400s.
- **Acceptance criteria:** A native `cargo test` asserts that two successive `.query(..)` calls accumulate and
  produce the exact resolved URL, that `.header(..)` values are observable on the builder, and that `.url()`
  returns the fully resolved URL *without* performing the request.
- **verification_method:** automated_test · **stage:** usable_early · **release_gating:** true
- **References:** REQ-FW-007. *Satisfied by the frozen surface; carried forward additively.*

#### REQ-HTTP-003 — Correct URL resolution and RFC-3986 query encoding, pure and native-testable
- **Statement:** Base and path join with exactly one `/` separator; an absolute request path (`http(s)://…`)
  overrides the base; query keys and values are percent-encoded per RFC 3986; and this resolution logic is
  pure, so it is testable without a browser.
- **Rationale:** URL correctness is a frequent, silent source of backend errors, and a WASM client that needs
  a headless browser to test its URL building is hard to trust. Making resolution a pure function the native
  test suite covers is how the client earns that trust cheaply.
- **Acceptance criteria:** `cargo test -p ferric-http` passes resolution cases covering base+`/path` and
  base+`path`, both trailing-slash variants, absolute-path override of the base, empty-path-returns-base, the
  `?`-vs-`&` separator choice when the path already carries a query, and `%XX` uppercase encoding including a
  multi-byte UTF-8 value (`é` → `%C3%A9`).
- **verification_method:** automated_test · **stage:** usable_early · **release_gating:** true
- **References:** REQ-FW-007. *Satisfied by the frozen surface; carried forward additively.*

### B. Typed JSON fetch

#### REQ-HTTP-004 — Typed JSON request body with a defaulted Content-Type
- **Statement:** An author sets a request body by passing any `serde::Serialize` value; the client serializes
  it to JSON and defaults `Content-Type: application/json` unless the author set a Content-Type explicitly.
- **Rationale:** Typed request bodies are the reason to use a JSON client rather than raw Fetch; `reqwest`'s
  `.json()` is the model. Defaulting Content-Type without clobbering an author-set value removes a common
  cause of a backend 415.
- **Acceptance criteria:** A native test asserts `.json(&T)` encodes the expected JSON string and adds exactly
  one `Content-Type: application/json`; a second test with a prior explicit `Content-Type` asserts that value
  is preserved and not duplicated; a serialization failure is returned as `Error::Serialize` (a `Result`),
  never a panic.
- **verification_method:** automated_test · **stage:** usable_early · **release_gating:** true
- **References:** REQ-FW-007. *Satisfied by the frozen surface; carried forward additively.*

#### REQ-HTTP-005 — Safe-by-default typed round-trip, with a raw escape hatch
- **Statement:** `send_json::<T>()` performs the request and returns a deserialized `T`, treating a non-2xx
  status as an error; a lower-level `send()` returns the raw `Response` so an author who wants to read a
  non-2xx body, or stream their own handling, can.
- **Rationale:** The dominant case — typed in, typed out, error on failure — should be the shortest path, with
  an explicit escape hatch for the rest. This two-path design is what separates a considered client from
  `gloo-net`'s thinner single surface, where status handling is left to the caller every time.
- **Acceptance criteria:** A headless `wasm-bindgen-test` performs a typed round-trip against an echo/stub
  endpoint and asserts the deserialized value; it then asserts `send()` on a 404 returns a `Response` without
  erroring while `send_json()` on the same request yields `Error::Status`. Where no browser runner is
  available, the native suite covers the `Response` → `error_for_status` → `json` composition that `send_json`
  is defined as, so the behavior is gated by `cargo test` even without a browser.
- **verification_method:** automated_test · **stage:** usable_early · **release_gating:** true
- **References:** REQ-FW-007. *Satisfied by the frozen surface; carried forward additively.*

#### REQ-HTTP-006 — Response as owned, synchronously-inspectable data
- **Statement:** A completed `Response` exposes the status code, status text, final URL (after redirects),
  headers with case-insensitive lookup, and the body as owned data, with synchronous `json::<T>()`, `text()`,
  `ok()`, and `error_for_status()`.
- **Rationale:** Reading the body eagerly and owning it makes every accessor synchronous and native-testable;
  `reqwest`'s response bodies are async, and Ferric trades that for testability and a simpler surface suited to
  the browser, where the body is already in memory after the Fetch resolves.
- **Acceptance criteria:** Native tests assert `ok()` across the 2xx boundary (199/200/204/299/300), a
  case-insensitive header lookup, a `json()` round-trip plus `Error::Deserialize` on a malformed body, and
  `error_for_status()` mapping a 404 to `Error::Status` carrying the code, URL, and body.
- **verification_method:** automated_test · **stage:** usable_early · **release_gating:** true
- **References:** REQ-FW-007. *Satisfied by the frozen surface; carried forward additively.*

### C. Error model

#### REQ-HTTP-007 — One matchable error type over every failure mode
- **Statement:** Every fallible operation returns `Result<T, Error>`, where `Error` distinguishes request-build
  failure, network failure (no response received), a non-2xx status (carrying code, status text, final URL, and
  body), request-body serialization failure, response-body deserialization failure, and body-read failure; no
  fallible path panics.
- **Rationale:** An app branches on *why* a call failed — retry a network blip, show a 404 to the user, log a
  500 — so the failure modes must be distinct and matchable. A single opaque error forces string-matching on
  messages. `reqwest`'s `Error` with its `is_*` predicates and `status()` accessor is the model this follows,
  kept lean (no `thiserror`) to hold the dependency footprint.
- **Acceptance criteria:** A native test constructs each variant and asserts a single-line `Display`, the
  `is_network()` / `is_status()` / `status()` classifiers, and that the serialize/deserialize variants expose
  their `serde_json::Error` through `std::error::Error::source`. A `doc_inspection` of the public surface
  confirms every fallible method returns `Result` (no `unwrap`/`expect`/panic on the fallible path).
- **verification_method:** automated_test · **stage:** usable_early · **release_gating:** true
- **References:** REQ-FW-007.

#### REQ-HTTP-008 — Non-2xx is an error on the safe path
- **Statement:** On the typed path a non-2xx response is surfaced as `Error::Status` carrying the status code,
  status text, final URL, and body — not returned as though it were a successful value.
- **Rationale:** Deserializing a 500's error body as if it were the expected `T`, or returning it as success,
  is the classic JSON-client bug. The `REQ-FW-007` acceptance bar names "handles a non-2xx status as an error"
  explicitly, and this requirement is where that bar is met for the client half.
- **Acceptance criteria:** A test asserts `send_json()` and `error_for_status()` on a 404 and on a 500 each
  yield `Error::Status` with the correct code and the response body preserved, while `send()` on the same
  requests returns the `Response` unchanged for the caller to inspect.
- **verification_method:** automated_test · **stage:** usable_early · **release_gating:** true
- **References:** REQ-FW-007.

### D. Additions a credible 1.0 adds (flagged additive — SI2)

#### REQ-HTTP-009 — Broader HTTP method coverage, added additively
- **Statement:** Beyond GET/POST/PUT/DELETE the client can issue PATCH, via a `Method::Patch` variant and a
  `Client::patch(path)` verb entry; the `Method` enum is carried forward so that adding methods does not break
  exhaustive matches in downstream code.
- **Rationale:** PATCH is standard REST for a partial update, and a backend like `chirp-server` uses it; a 1.0
  client that cannot PATCH pushes authors to the generic `request` entry or a workaround. Adding a variant to a
  plain enum is a breaking change, so the additive-safe path is to mark `Method` `#[non_exhaustive]` as part of
  1.0 and add `Patch` under it — a surface change recorded by semver, not a redefinition of an existing
  variant.
- **Acceptance criteria:** `Method::Patch` exists, `client.patch(path)` issues a request whose method token is
  `PATCH`, and `Method` is `#[non_exhaustive]`; a `trybuild`/build check confirms code written against the
  baseline variants still compiles; a `doc_inspection` confirms the changelog records the `#[non_exhaustive]`
  addition as the semver-signalled surface change.
- **verification_method:** automated_test · **stage:** one_oh · **release_gating:** true
- **References:** REQ-FW-009; REQ-REL-* (semver/changelog, read-only). *Additive over the frozen `Method`.*

#### REQ-HTTP-010 — Per-request timeout and cancellation
- **Statement:** An author can bound a request with a timeout and/or cancel it through an abort handle, so a
  hung or slow backend does not hang the app; a timed-out or aborted request surfaces as a distinct, matchable
  `Error`.
- **Rationale:** A real app cannot wait forever on a request. The Fetch API provides `AbortController` /
  `AbortSignal` for exactly this, and `reqwest` exposes `.timeout()`; the frozen surface has neither today. The
  addition is a `RequestBuilder::timeout(..)` (and/or an abort handle) plus a new `Error` variant — and because
  `Error` is already `#[non_exhaustive]`, the new variant is additive by construction. It uses `web-sys`'s
  existing `AbortController`, so it adds no new crate dependency (`REQ-HTTP-012`).
- **Acceptance criteria:** A headless `wasm-bindgen-test` issues a request against a never-responding stub with
  a short timeout and asserts the call resolves to the timeout/abort error within the bound rather than hanging;
  the new error variant is matchable and documented. (On a native build, the timeout plumbing that does not
  touch Fetch is unit-tested where it is pure.)
- **verification_method:** automated_test · **stage:** one_oh · **release_gating:** true
- **References:** REQ-FW-009, REQ-FW-013. *Additive: new `RequestBuilder::timeout`/abort handle + a new
  `#[non_exhaustive]` `Error` variant.*

### E. Composition and footprint

#### REQ-HTTP-011 — Composes with the view framework and async layer; no view dependency
- **Statement:** The client is usable from Ferric's async resource/suspense layer — a shared `Client` driven
  inside an async loader that renders loading, loaded, empty, and error states — and does not depend on the
  `ferric` view crate, so it is usable on its own and composes without conflicting assumptions.
- **Rationale:** `REQ-FW-008` requires the pieces to compose into one real app; the HTTP client is consumed by
  the async/resource layer (`REQ-ASYNC-*`), which means it must be `Clone`/shareable and view-agnostic. The
  crate already declares no `ferric` dependency, which keeps it reusable and testable on its own.
- **Acceptance criteria:** `cargo tree -p ferric-http` shows no dependency on the `ferric` view crate; a stated
  example (or the `chirp-frontend` reference app) drives a `send_json()` from inside an async resource and
  renders distinct loading/loaded/error states from the result.
- **verification_method:** example_build · **stage:** usable_early · **release_gating:** true
- **References:** REQ-FW-007, REQ-FW-008; REQ-ASYNC-* (resource/suspense, read-only).

#### REQ-HTTP-012 — Lean, documented dependency footprint
- **Statement:** The client's dependency set stays limited to the WASM-binding essentials (`web-sys`, `js-sys`,
  `wasm-bindgen`, `wasm-bindgen-futures`) plus `serde` and `serde_json`, with no heavy general-purpose HTTP
  runtime; the set and its bundle-size impact are documented.
- **Rationale:** In WASM every dependency is downloaded bytes before the app runs, and `REQ-FW-013` names
  leanness as a differentiator Ferric competes on. A full-stack native client such as `reqwest` pulls a large
  `hyper`/`tokio` dependency tree ill-suited to a lean WASM bundle; a Fetch-based client exists precisely to
  avoid that. The `serde`/`serde_json`/`wasm-bindgen-futures` additions are the narrowly-scoped,
  per-crate-justified exceptions `REQ-FW-013` anticipates.
- **Acceptance criteria:** A reviewer confirms the crate's `Cargo.toml` dependency set matches the stated list,
  and a check confirms no transitively-heavy runtime (for example `tokio` or `hyper`) is pulled on the
  `wasm32-unknown-unknown` target; the footprint is recorded and its bundle-size contribution is reflected in
  the performance numbers (`REQ-PERF-*`, read-only).
- **verification_method:** doc_inspection · **stage:** one_oh · **release_gating:** true
- **References:** REQ-FW-013; REQ-PERF-* (bundle-size measurement, read-only).

#### REQ-HTTP-013 — Frozen surface carried forward additively
- **Statement:** The `ferric-http` public `prelude` present at the baseline stays usable at 1.0; every change
  is additive (new items only), and no previously exported item is removed or redefined without a
  semver-signalled, changelog-recorded break.
- **Rationale:** `chirp-frontend` and any example are written against the baseline `prelude`; silently
  redefining it during the 1.0 work would break consumers. This is `REQ-FW-009` restated for this crate and the
  condition identity SI2 asserts over this spoke.
- **Acceptance criteria:** A program written against the baseline `prelude` (`Client`, `ClientBuilder`, `Error`,
  `Method`, `RequestBuilder`, `Response`, `Result`) still compiles against the 1.0 crate; the only surface
  differences a `doc_inspection` finds are additions (the `Method::Patch` variant and `#[non_exhaustive]`, the
  timeout/abort method, the new `Error` variant), each recorded in the changelog.
- **verification_method:** automated_test · **stage:** usable_early · **release_gating:** true
- **References:** REQ-FW-009; REQ-REL-* (compatibility policy, read-only).

### Register summary

| Facet | Requirements | Stage |
|---|---|---|
| Request building | REQ-HTTP-001, 002, 003 | usable_early |
| Typed JSON fetch | REQ-HTTP-004, 005, 006 | usable_early |
| Error model | REQ-HTTP-007, 008 | usable_early |
| 1.0 additions (flagged additive) | REQ-HTTP-009, 010 | one_oh |
| Composition & footprint | REQ-HTTP-011 (usable_early), 012 (one_oh), 013 (usable_early) | mixed |

All `REQ-HTTP-*` are `release_gating: true` (none is a post-1.0 deferral). Every item carries ≥1 acceptance
criterion checkable by a stranger via a parent-schema `verification_method` (SI6). REQ-HTTP-001–008 and 013 are
met by the frozen surface the baseline already landed; REQ-HTTP-009 and 010 are the additive 1.0 work.

---

## Peer comparison

*(section: `peer_comparison` — named comparison against `reqwest` and `gloo-net`, on typed bodies, builder
ergonomics, error handling, and WASM Fetch fit)*

| Dimension | `reqwest` | `gloo-net` | Ferric `ferric-http` |
|---|---|---|---|
| Transport | Native `hyper`/`tokio` stack; a separate `wasm` backend wraps Fetch | Browser Fetch only | Browser Fetch only (`web-sys`) |
| Client object | `Client` holds connection pool + config, clone-cheap, shareable | No client object — base URL/headers repeated per call | `Client` holds base URL + default headers, clone-cheap, no connection state |
| Typed bodies | `.json()` request and response via `serde` | `.json()` request and response via `serde` | `.json(&T)` request, `send_json::<T>()` response via `serde` |
| Safe-by-default status | `error_for_status()` is opt-in; `send` returns any status | Caller checks status each time | `send_json()` treats non-2xx as `Error::Status`; `send()` is the raw escape hatch |
| Error model | Rich `Error` with `is_*` predicates and `status()` | Thinner; a single error over Fetch/serde failures | One `#[non_exhaustive]` `Error` splitting builder / network / status / (de)serialize / body, with `is_*` + `status()` |
| Timeout / cancel | `.timeout()`, abort | Via raw `AbortController` | Added at 1.0 (`REQ-HTTP-010`); not at baseline |
| WASM bundle weight | Heavier — the fuller stack is more than a lean WASM target wants | Light | Light (binding essentials + `serde`) |

Where Ferric sits: it takes `gloo-net`'s leanness and Fetch basis and adds the client-level
ergonomics an author expects from `reqwest` — a configured, shareable `Client` with base URL and default
headers, a typed round-trip that errors on non-2xx by default, and a structured error — without `reqwest`'s
dependency weight. Against `reqwest` it is deliberately smaller: no connection pooling to own (the browser owns
it), synchronous owned-body responses instead of async bodies, and (until `REQ-HTTP-010` lands) no timeout.
Against `gloo-net` it adds the pieces a real app otherwise re-implements by hand: client configuration, the
safe-by-default status path, and a matchable error taxonomy. The one capability both peers have that the
baseline lacks — a request timeout — is the `REQ-HTTP-010` addition, so the 1.0 client is not behind either
peer on the dimensions an app author weighs.

---

## Board fold — issue #6 (`ferric-http`)

*(section: `board_fold`; realizes SI3, feeds parent I7 — record the fold, do not duplicate)*

**Issue #6 — "ferric-http: fetch-based HTTP/JSON client"** (epic #1, milestone M1, labels `framework` /
`type:feature`) is **CLOSED**. Its scope was "a small async HTTP client over the Fetch API: typed JSON
get/post/put/delete with serde, error handling, request/response helpers; tested; fmt/clippy clean; delivered
as a PR into `main`." The PR landed the `ferric-http` crate at the frozen `prelude` surface documented above,
with the pure logic implemented and natively tested and a browser smoke test for the Fetch path.

**The fold: #6 is extended, not duplicated.** #6 delivered the `usable_early` core of this client — it is the
scaffold that `REQ-HTTP-001`–`REQ-HTTP-008` and `REQ-HTTP-013` describe and that those criteria are already met
by. The 1.0 design does not re-file that work; it builds on it. The additive 1.0 work is `REQ-HTTP-009`
(PATCH + `#[non_exhaustive] Method`) and `REQ-HTTP-010` (timeout/cancellation), plus ratifying the testable bar
across the whole register.

Because #6 is closed, the release plan should record the fold as follows (the plan is owned by
`SUBTASK_release_plan`; backlog edits by `SUBTASK_file_backlog` — both read-only to this spoke):

- The 1.0 HTTP epic/work-items **supersede/extend #6** and cite it as the scaffold they complete, with their
  acceptance criteria tracing to `REQ-HTTP-009` / `REQ-HTTP-010` and this design section (per the epic
  `supersedes` field and identity I7).
- `file_backlog` should **link the new work-items to the closed #6** (reference it in the epic's `supersedes`)
  rather than opening a duplicate "HTTP client" issue — the capability already has a home on the board; the 1.0
  work is the additive completion of it.

---

## Metadata

- **Owning task:** `SUBTASK_http` (owns the `REQ-HTTP-*` register; identity SI1).
- **Output:** `http.md` (this file); composed by `SUBTASK_synthesis` into `router-and-http.md` at
  `design/ferric/router-and-http.md` (SI4 / parent I8).
- **Conforms to:** `../../contracts/id_and_traceability_schema.yaml` (REQ fields, stage vocabulary,
  `verification_method`, `release_gating`); `../contracts/_MANIFEST.yaml` (`doc_layout`, ownership, identities
  SI1–SI6).
- **Grounding:** `Nousix-LLC/nswe-demo` @ `276138f` — `crates/ferric-http/src/*` read directly; board issue #6
  and epic #1 read from the `NSWE Delivery` board.
- **Register:** `REQ-HTTP-001`–`REQ-HTTP-013`, all `release_gating: true`; `usable_early` (001–008, 011, 013)
  or `one_oh` (009, 010, 012). Only `REQ-HTTP-*` ids are defined here; all other-register references are
  read-only.
- **Realizes:** the HTTP half of `REQ-FW-007`; honors `REQ-FW-009` (additive over frozen surface) and
  `REQ-FW-013` (lean footprint).
