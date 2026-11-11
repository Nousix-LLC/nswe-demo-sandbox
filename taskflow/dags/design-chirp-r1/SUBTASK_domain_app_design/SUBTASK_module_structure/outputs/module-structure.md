<!--
This file carries two sections of design/domain-application-design.md:
`modules_and_responsibilities` and `interfaces_and_entry_points`.
SUBTASK_dad_synthesis assembles it, with the sibling parts, into the consolidated design file and
folds every REQ-DOM-* below into that file's requirements_and_acceptance_criteria register.
Owns: those two sections and REQ-DOM-200..249.
Held to the crates at Nousix-LLC/nswe-demo @ c805525: ferric (+ ferric-http, ferric-router),
chirp-types, chirp-server, chirp-frontend. Entities are referenced only by the canonical names the
domain model (REQ-DOM-001..049) fixes.
-->

# Modules and responsibilities

## What this section fixes

This section states *how chirp's running system divides into parts, what each part is responsible
for, and the contracts at the seams between them* — as requirements and structure, not as code. It
is held to the four crates that already exist at commit `c805525`, so the design refines the running
product rather than proposing a parallel one. Where an engineering *how* is implied — which HTTP
framework, how WebAssembly is bundled, how a datastore is wired — the requirement is stated and the
decision is left to the `software` domain's later code work.

The division is described from the outside: what each part owes the others, and what crosses each
seam, so that a reader can tell whether a given change belongs in the shared types, the server, or
the frontend, and so the parts compose into one product. Entities are named only by the canonical
vocabulary the domain model establishes (Account/User, Handle, Chirp, Reply, Follow, Like, Timeline,
Session); this section assigns responsibility over those entities, it does not redefine them.

### The parts at a glance

chirp is four crates in one repository, in two layers:

- **`ferric`** — the in-house client-side UI framework (reactive signals and a virtual DOM), with
  **`ferric-router`** (client-side routing) and **`ferric-http`** (a browser HTTP client) beside
  it. `ferric` is the engagement's *other* deliverable; chirp is the product that exercises it.
  `ferric` carries **no** chirp domain knowledge.
- **`chirp-types`** — the single source of truth for every type that crosses the wire: the
  identifiers, the domain entities and their validated value objects, and the request/response
  shapes, pagination envelope, and error contract. Pure data and validation — no I/O, no framework,
  no async — so both a native server and a WebAssembly frontend import it unchanged.
- **`chirp-server`** — the backend: a REST service that implements the API over the shared types,
  enforces the domain invariants, owns the persistence seam and the data behind it, serves the
  single-page app, and exposes the health endpoint.
- **`chirp-frontend`** — the single-page web application the person uses: it presents the screens,
  holds the signed-in Session in reactive state, and talks to the backend through the shared
  contract. It holds **no** durable state of its own.

---

## The requirements (`REQ-DOM-200..224`)

Each requirement carries an `id`, a `statement` (what must be true of the structure), an
`acceptance_criteria` a person who never met the author can check — by inspecting the named crate in
the shared contract, or by exercising the running product — a `release_gating` flag (`true` when a
releasable product depends on it), and `traces_to` the product requirement it serves where one
applies.

### The module decomposition

#### REQ-DOM-200 — The product is exactly these four crates, in two layers
- **statement**: chirp is partitioned into a client-side framework layer (`ferric`, with `ferric-http` and `ferric-router`) and a product layer of three crates — `chirp-types` (shared wire contract), `chirp-server` (REST backend), and `chirp-frontend` (the single-page app) — with no fifth product crate silently carrying responsibility. Every responsibility in this design is assigned to exactly one of these parts.
- **acceptance_criteria**: Inspect the repository's `crates/` directory at `c805525`; it contains `ferric`, `ferric-http`, `ferric-router`, `chirp-types`, `chirp-server`, and `chirp-frontend`, and no product responsibility in this design is left unassigned or assigned to two parts.
- **release_gating**: true

#### REQ-DOM-201 — `ferric` is the framework, and carries no chirp domain knowledge
- **statement**: `ferric` (with `ferric-router` and `ferric-http`) provides the client-side UI framework — reactive state, a virtual DOM, client-side routing, and a browser HTTP client — and nothing in it names a chirp entity or encodes a chirp rule; chirp builds *on* `ferric`, and `ferric` could serve a different product unchanged.
- **acceptance_criteria**: Inspect `crates/ferric`, `crates/ferric-router`, and `crates/ferric-http`; none references an Account, Chirp, Follow, Like, Timeline, or Session, nor depends on `chirp-types`. The dependency direction is one-way: `chirp-frontend` depends on the `ferric` crates, never the reverse.
- **release_gating**: true

#### REQ-DOM-202 — `chirp-types` is the single source of truth for everything that crosses the wire
- **statement**: Every type that passes between the frontend and the backend — identifiers, the domain entities and their validated value objects, the request and response shapes, the pagination envelope, the Session token, and the error contract — is defined once in `chirp-types`; neither side defines a parallel shape for data that crosses the seam. `chirp-types` is pure data and validation: it performs no I/O, embeds no framework, and is not async, so both the native backend and the WebAssembly frontend compile against the identical definitions.
- **acceptance_criteria**: Inspect `crates/chirp-types`; its `ids`, `domain`, and `api` modules carry the identifiers, entities/value objects, and request/response DTOs respectively, and both `chirp-server` and `chirp-frontend` depend on it. `chirp-types` has no I/O, framework, or async dependency. No DTO that crosses the wire is defined anywhere but `chirp-types`.
- **release_gating**: true

#### REQ-DOM-203 — `chirp-server` owns the REST backend and enforces the domain invariants
- **statement**: `chirp-server` implements the REST API over the shared types and is the authority for the domain invariants the model fixes — a Chirp's author exists, Follow is not self-directed and is idempotent, a Like is at most one per (Account, Chirp) and idempotent, server-maintained counts stay consistent with their edges, and a Timeline is newest-first and bounded. It maps each failure to a machine-readable category the transport layer turns into a status; a client cannot cause the server to persist a state that violates an invariant.
- **acceptance_criteria**: Through the running product, attempt actions that would violate an invariant (follow yourself; like a chirp twice; post a chirp as a nonexistent Account); each is refused with a categorized error and no violating state is stored. Inspect `crates/chirp-server`; the `ChirpRepository` boundary documents these invariants as obligations on every implementation.
- **release_gating**: true

#### REQ-DOM-204 — `chirp-server` owns the persistence seam and the data behind it
- **statement**: All of chirp's durable state lives behind one boundary owned by `chirp-server` — the `ChirpRepository` seam — and no other part reaches around it to the store. Which store backs the seam is an engineering choice deferred to the `software` domain and the persistence requirement; the structural requirement is that exactly one replaceable boundary owns durable state.
- **acceptance_criteria**: Inspect `crates/chirp-server/src/repository`; a single `ChirpRepository` boundary mediates every durable operation, with the store behind it chosen by configuration. No handler or frontend code reads or writes the store except through this boundary. (Which store and its durability guarantees are the sibling persistence requirement, REQ-DOM-100..149.)
- **release_gating**: true
- **traces_to**: REQ-PROD-037

#### REQ-DOM-205 — `chirp-server` serves the single-page app and the health endpoint
- **statement**: The same `chirp-server` process that serves the API also serves the frontend's static assets and exposes the health endpoint, so chirp is one running service and not a pair that must be deployed and reconciled separately.
- **acceptance_criteria**: Start the service and, from one address, both call the API and load the single-page app; query the health endpoint at that same address. No second process or second deployable is required to serve the app.
- **release_gating**: true
- **traces_to**: REQ-PROD-040

#### REQ-DOM-206 — `chirp-frontend` presents the product and holds only session state
- **statement**: `chirp-frontend` is the single-page web application: it renders the screens and the persistent navigation, holds the signed-in Session (the authenticated Account and its bearer token) in reactive state, and issues requests and decodes responses through the shared contract. It holds no durable state — every Account, Chirp, Follow, Like, and Timeline it shows is the backend's, fetched through the API — so clearing the browser loses nothing but the local Session.
- **acceptance_criteria**: Inspect `crates/chirp-frontend`; the only state it owns across views is the current Session, and all entity data is fetched through its typed API client rather than stored locally. Reloading the app in the browser re-fetches state from the backend; no entity data persists only in the client.
- **release_gating**: true

#### REQ-DOM-207 — Domain rules are enforced on the server, not trusted from the client
- **statement**: The frontend may validate inputs for a fast, kind experience (for example the Handle and Chirp-text rules), but every domain invariant is re-checked and enforced by `chirp-server`; the product never depends on the client to uphold a rule, because a request can reach the API without the frontend.
- **acceptance_criteria**: Bypassing the frontend, submit to the API a Chirp over the length limit, a self-Follow, and a Chirp attributed to a nonexistent Account; each is refused by the server regardless of any client-side checking.
- **release_gating**: true
- **traces_to**: REQ-PROD-023

#### REQ-DOM-208 — Responsibility over each entity is assigned to exactly one part
- **statement**: For every entity in the canonical vocabulary, `chirp-types` carries its wire *shape*, `chirp-server` owns its *lifecycle and persistence* (creating it, enforcing its invariants, storing it), and `chirp-frontend` only *presents* it; no entity's lifecycle is owned by two parts, and none is owned by the frontend.
- **acceptance_criteria**: For each of Account, Chirp, Follow, Like, Timeline, and Session, trace where its shape is defined (`chirp-types`), where it is created and validated (`chirp-server`, behind `ChirpRepository`), and where it is shown (`chirp-frontend`); each role resolves to exactly one crate and the frontend owns no lifecycle.
- **release_gating**: true

---

# Interfaces and entry points

## What this section fixes

This section states the **seams between the parts** and the **entry points into the product** as
requirements and structure, from the outside: what the REST API must offer the single-page app as a
contract (not route-by-route code), what the shared types boundary must carry so the server and
frontend agree, how the persistence seam is shaped so a durable store drops in, how the frontend is
delivered, and the entry points a person or an operator reaches. Every engineering *how* — the exact
HTTP framework, URL strings, the serialization library, the datastore wiring, the WebAssembly build
— is deferred to the `software` domain. Entities are named only by the canonical vocabulary.

Three seams hold the product together, and they are the backbone of this section:

1. **The REST contract** — the typed request/response surface the frontend calls and the server
   implements, with `chirp-types` as its single source of truth.
2. **The persistence seam** — the one boundary (`ChirpRepository`) through which all durable state
   flows, so the store is replaceable.
3. **The delivery seam** — how the single-page app is served, and the entry points (the app URL,
   the in-app routes, the health endpoint, the service's configuration) a person or operator meets.

---

## The requirements (`REQ-DOM-215..239`)

Same fields as above: `id`, `statement`, testable `acceptance_criteria`, `release_gating`, and
`traces_to` where a product requirement applies.

### The REST contract (the frontend↔server seam)

#### REQ-DOM-215 — There is exactly one typed client↔server contract, and `chirp-types` is it
- **statement**: The frontend and the server communicate through a single REST contract whose request and response types are the `chirp-types` definitions; the two sides build requests and decode responses from the same definitions, so they cannot drift. There is no second, hand-maintained copy of any wire shape on either side.
- **acceptance_criteria**: Inspect `crates/chirp-types/src/api.rs`; it defines the request/response DTOs, the pagination envelope (`Page` with an opaque `Cursor`), the `SessionToken`, and the error contract. Confirm `chirp-server` accepts and returns these types and `chirp-frontend` sends and decodes them, with no parallel DTO defined in either crate.
- **release_gating**: true

#### REQ-DOM-216 — The API is namespaced and same-origin with the app
- **statement**: The REST surface lives under a reserved path prefix so it never collides with the app's own client-side routes, and the frontend reaches it on the same origin that served the app, so no cross-origin configuration is part of the product's normal operation.
- **acceptance_criteria**: Load the app and observe its API calls; they target the reserved API prefix on the same origin as the page. A path that is not an API path resolves to the single-page app, not to an API handler.
- **release_gating**: true

#### REQ-DOM-217 — The contract covers the core-loop operations the app depends on
- **statement**: The REST contract offers, as a surface the frontend can rely on, the operations the core loop needs: create an Account, fetch an Account's public profile, open a Session, post a Chirp (including a Reply), read a Timeline, follow and unfollow an Account, and like and unlike a Chirp. The design fixes the *operations and their types*, not their exact URLs.
- **acceptance_criteria**: Against the running product, exercise each operation end to end from the app and confirm it is served. Inspect `chirp-types::api`; each operation has a defined request and response type. (The live surface at `c805525` already provides these; inspect the server's router to confirm each is mounted.)
- **release_gating**: true
- **traces_to**: REQ-PROD-001, REQ-PROD-002, REQ-PROD-005, REQ-PROD-006, REQ-PROD-007

#### REQ-DOM-218 — Timeline reads cross the contract as bounded pages behind an opaque cursor
- **statement**: A Timeline is returned over the contract one bounded page at a time, each page carrying an opaque continuation cursor when more Chirps remain; the server enforces a maximum page size, so a client cannot force the contract to return every Chirp in one response.
- **acceptance_criteria**: Request a Timeline over the API; a bounded page returns with a continuation cursor when more remain, and passing the cursor returns the next, older page. A requested size above the server's maximum is clamped. Inspect `chirp-types::api`; the page envelope carries the items and an optional next cursor, and the cursor is opaque.
- **release_gating**: true
- **traces_to**: REQ-PROD-002

#### REQ-DOM-219 — Authentication crosses the contract as an opaque bearer Session token; private data never does
- **statement**: A signed-in request proves itself by presenting the Session as an opaque bearer token the server issued; the token's internals are not part of the contract. Only an Account's public profile fields (Handle, display name, bio, follower/following counts) and public Chirps cross the contract outward — an Account's credential, verified contact, and Session data never appear in any response.
- **acceptance_criteria**: Sign in, obtain a token, and present it on an authenticated request; the request acts as that Account. Inspect responses for another Account's profile and any public response; only public fields appear, and no credential, contact, or Session data is ever returned. Inspect `chirp-types::api`; the Session token is a transparent string wrapper with no interpreted structure.
- **release_gating**: true
- **traces_to**: REQ-PROD-010, REQ-PROD-024

#### REQ-DOM-220 — Errors cross the contract as a typed, machine-readable category
- **statement**: A failed request returns a typed error carrying a machine-readable category (for example validation, not-found, conflict, unauthorized, forbidden), not an ad-hoc string, so the frontend can present it meaningfully and distinguish, for example, a taken Handle from a malformed one.
- **acceptance_criteria**: Provoke a validation failure, a conflict (a duplicate Handle), and an unauthorized request; each returns a response carrying a distinct, machine-readable category the frontend can branch on. Inspect `chirp-types::api`; the error contract defines a closed set of categories.
- **release_gating**: true
- **traces_to**: REQ-PROD-009, REQ-PROD-011

#### REQ-DOM-221 — The contract's wire conventions are stable and grow additively
- **statement**: The contract's serialization conventions are fixed and load-bearing — JSON field names are stable regardless of internal renames, opaque identifiers and tokens serialize as their bare value, validated value objects (the Handle, the Chirp text) reject invalid input on the way in, and error categories are machine-readable constants — and the contract's public surface grows only by addition, never by changing or removing an existing shape.
- **acceptance_criteria**: Inspect `crates/chirp-types`; field naming, the transparent identifier/token wrappers, the validate-on-deserialize value objects, and the machine-readable error codes are present as conventions. A change that renamed or removed an existing wire field (rather than adding one) would be a breaking change to this contract and is out of bounds.
- **release_gating**: true

#### REQ-DOM-222 — New product surfaces extend the one contract, not a second API
- **statement**: The release requires surfaces the live API at `c805525` does not yet carry — among them ending a Session (sign-out), editing a profile, account settings, recovery, data export, account deletion, reporting and blocking/muting, notifications, a supported operator/administrative surface, and a way to find Accounts to follow. Each is added by extending the one `chirp-types` contract and the one namespaced API, additively; the product does not grow a second, parallel API. Which of these surfaces exist, and their detailed behavior, are owned by the product, identity, experience, and operational-readiness designs and the `software` domain; the structural requirement here is that they attach to the single existing contract.
- **acceptance_criteria**: For each new surface the release adopts, confirm its request/response types are defined in `chirp-types` and its operations are mounted under the one namespaced API alongside the existing ones — not in a separate contract or service. (The set of surfaces and their behavior trace to the product and area designs named; this requirement checks only that they extend the one contract.)
- **release_gating**: true
- **traces_to**: REQ-PROD-008, REQ-PROD-014, REQ-PROD-016, REQ-PROD-017, REQ-PROD-019, REQ-PROD-020, REQ-PROD-028

### The persistence seam (the server↔store boundary)

#### REQ-DOM-223 — All durable state flows through one replaceable boundary, and a durable store is a drop-in
- **statement**: Every durable operation the server performs on an Account, Chirp, Follow, Like, Session, or Timeline passes through the single `ChirpRepository` boundary; replacing the in-memory backing at `c805525` with a durable store is introducing a new implementation of that one boundary, touching no request handler and no frontend code. The capability set the boundary exposes is the whole of what the product needs from durable state, so a durable implementation has a closed, known surface to satisfy.
- **acceptance_criteria**: Inspect `crates/chirp-server/src/repository`; the `ChirpRepository` boundary enumerates exactly the durable operations the product uses, the default in-memory backing implements it, and the handlers depend on the boundary rather than on a concrete store. A durable store added as a second implementation requires no change to any handler. (The durability guarantees themselves — what survives a restart — are the sibling persistence requirement, REQ-DOM-100..149.)
- **release_gating**: true
- **traces_to**: REQ-PROD-037

### Delivery and entry points

#### REQ-DOM-224 — The app is served as static assets with a single-page fallback, and owns its client-side routing
- **statement**: `chirp-server` serves the frontend as static assets from a configured root, and any request path that is neither an API path nor a real asset resolves to the app's entry document, so the single-page app owns its own client-side routing and a deep link to an in-app route loads the app rather than failing.
- **acceptance_criteria**: Request an in-app route directly (not the app root) with no prior navigation; the app loads and resolves that route client-side. Request an unknown asset path; the app's entry document is returned rather than a server error. The static root is configurable for deployment.
- **release_gating**: true
- **traces_to**: REQ-PROD-035

#### REQ-DOM-225 — The product has one user entry point: a single web address
- **statement**: A person reaches chirp at one web address that serves the single-page app; there is nothing to install and no second place to go. The in-app routes reached from that entry are the Timeline view, the compose-and-sign-in view, and a profile view (`c805525`), and this route set must grow to reach the release's new surfaces (sign-up, sign-in, recovery, settings, deletion, and the rest) rather than adding a separate app.
- **acceptance_criteria**: Open the single web address with no account; the app loads and offers a path onward. From the app, reach the Timeline, compose/sign-in, and a profile. Confirm there is no separate installed client. (The specific screens and their flows are the experience design's, REQ-UX-*; this requirement fixes that there is one web entry and the app owns the route set.)
- **release_gating**: true
- **traces_to**: REQ-PROD-030, REQ-PROD-040

#### REQ-DOM-226 — The product exposes a health/readiness entry point for the operator
- **statement**: The service exposes an unauthenticated health endpoint an operator can query without a Session. Today it reports process liveness only; the release requires that it report *readiness* — that the service can actually serve users, including that its durable store is reachable — so an orchestrator can tell "serving" from "merely running."
- **acceptance_criteria**: Query the health endpoint with no Session; it responds. With the durable store made unavailable, the readiness signal reports not-ready; with the service able to serve users, it reports ready. (The detailed observability and the readiness semantics are the operational-readiness design's, REQ-OPS-*; the `how` is deferred to the `software` domain.)
- **release_gating**: true
- **traces_to**: REQ-PROD-039

#### REQ-DOM-227 — The service's runtime entry points are configured, not hard-coded, and it ships as one artifact
- **statement**: An operator reaches the service through configuration rather than code changes: the network address it binds and the static-asset root it serves are set from the environment, and chirp ships as one self-contained artifact that serves both the API and the app and is operated as a hosted service. No part of the product requires editing source to deploy it to a new environment.
- **acceptance_criteria**: Inspect the server binary's configuration; the bind address and static root are read from the environment with sensible defaults. Deploy the one artifact to a fresh environment by setting configuration only — without editing source — and confirm it serves both the API and the app at its address.
- **release_gating**: true
- **traces_to**: REQ-PROD-040

<!--
Range note: this part owns REQ-DOM-200..249 and uses 200..208 (modules_and_responsibilities) and
215..227 (interfaces_and_entry_points). The gaps (209..214, 228..249) are reserved, not padding; a
later amendment to the module/interface design takes ids from there without disturbing the domain
model (001..049) or persistence (100..149) ranges.
-->

---

## Traceability

Every `REQ-DOM-*` above that refines a product requirement cites it in `traces_to`. The map below is
the checkable summary, folded into the consolidated traceability matrix.

| REQ-DOM | Section | Traces to REQ-PROD | release_gating |
|---|---|---|---|
| 200 | modules | — | true |
| 201 | modules | — | true |
| 202 | modules | — | true |
| 203 | modules | — | true |
| 204 | modules | 037 | true |
| 205 | modules | 040 | true |
| 206 | modules | — | true |
| 207 | modules | 023 | true |
| 208 | modules | — | true |
| 215 | interfaces | — | true |
| 216 | interfaces | — | true |
| 217 | interfaces | 001, 002, 005, 006, 007 | true |
| 218 | interfaces | 002 | true |
| 219 | interfaces | 010, 024 | true |
| 220 | interfaces | 009, 011 | true |
| 221 | interfaces | — | true |
| 222 | interfaces | 008, 014, 016, 017, 019, 020, 028 | true |
| 223 | persistence seam | 037 | true |
| 224 | entry points | 035 | true |
| 225 | entry points | 030, 040 | true |
| 226 | entry points | 039 | true |
| 227 | entry points | 040 | true |

**How this builds on the model and feeds the rest of the design.** This structure assigns ownership
over every entity the domain model (`REQ-DOM-001..049`) names, lands the persistence seam that the
persistence requirement (`REQ-DOM-100..149`) fills with durability guarantees, and names the three
seams — the one REST contract, the one `ChirpRepository` boundary, and the one delivery/entry model —
that the `software` domain's later code DAGs build against. Each requirement states *what must be
true* of the structure and defers every engineering *how* by prose to that later work.
