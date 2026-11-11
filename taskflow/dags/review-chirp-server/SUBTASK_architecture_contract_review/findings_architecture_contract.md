# Findings — Architecture / Layering / Frozen-Contract Conformance (SUBTASK_architecture_contract_review)
- PR: #19 (chirp-server), head 714d50f, reviewing main...HEAD
- Lens: architecture-contract
- Acceptance criteria owned: AC1, AC2, AC3, AC4, AC5
- F1 sub-questions owned: F1_1, F1_3
- Overall lens disposition: findings-only-minor-or-nit

## Summary

Through the architecture / layering / frozen-`chirp-types`-contract lens the change is **clean of
blocking and major defects**. The full 9-route REST surface, `/healthz`, and the SPA fallback are
assembled in one composition root (`build_router`); persistence sits behind `Arc<dyn ChirpRepository>`
with an in-memory default and **no** database dependency in the build graph; the `ServerError →
ApiError/ErrorCode → HTTP status` mapping is complete and correct for all six contract rows; every DTO
is imported from `chirp-types` and never re-declared; and the F1 validation fix is live on the HTTP
surface. Three **minor** observations are recorded (an unmatched-`/api/*` fallthrough, a collapsed
service tier, and the F1_3 `details` fidelity limitation). None is blocking on this lens; the F1_3
acceptable-vs-blocking ruling is explicitly left to the gate.

---

## Findings

### ARCH-01  — Unknown `/api/*` paths fall through to the SPA `index.html` (200 HTML) instead of a JSON 404 `ApiError`
- **Severity**: minor
- **AC / F1 ref**: AC1
- **Location**: `crates/chirp-server/src/api/router.rs:57`, `:77` (`fallback_service(spa)`); design acknowledged in the module docs `router.rs:17-22`
- **Observation**: The router mounts the 9 API routes, then `.fallback_service(spa)` serves the static
  dir with an `index.html` fallback for *every* unmatched path. Because the API is namespaced under
  `/api/…` but shares one fallback with the SPA, a mistyped or unknown API path (e.g.
  `GET /api/typo`, or a wrong method on a known path) does not produce a `404 NOT_FOUND`/`ApiError` —
  it returns **200 OK with the SPA `index.html`**. The module docs state this is intentional
  ("an unknown `/api/…` path still falls through to the SPA fallback … which is the conventional SPA
  behavior"). Genuine resource 404s (unknown user/chirp id) still come correctly from the handlers.
- **Why it matters**: contract/maintainability. For the *API* path space this is an API-design wart: a
  JSON client that hits a wrong `/api` route receives `text/html` with a success status, which decodes
  as neither the success DTO nor the `ApiError` wire contract — a confusing failure mode versus a clean
  `404 { code: NOT_FOUND }`. It does not violate AC1 (all required routes are present and correctly
  mounted) and is bounded to the error path of *unknown* routes, hence minor, not blocking.
- **Recommendation**: scope the static/SPA fallback to the non-`/api` path space (e.g. mount the SPA
  under its own fallback and give the `/api` namespace a nested router whose own fallback returns a
  `ServerError::NotFound` → `404 ApiError`), so unmatched `/api/*` yields the wire error contract. Do
  NOT make the change here — it is for the remediation DAG if the gate elects to act.

### ARCH-02  — No distinct service tier; domain logic lives in the repository implementor ("fat repository")
- **Severity**: minor
- **AC / F1 ref**: AC2
- **Location**: `crates/chirp-server/src/api/handlers.rs:64-203` (handlers call `state.repo.*` directly);
  invariants enforced in `crates/chirp-server/src/repository/in_memory.rs:263-375` (self-follow forbid,
  idempotency, counts, timeline scoping)
- **Observation**: AC2 names a `transport → service → repository` separation. In the code there are two
  layers, not three: each handler is a thin transport adapter that `.await`s exactly one
  `ChirpRepository` method, and all business/domain logic (self-follow `Forbidden`, follow/like
  idempotency, denormalized-count maintenance, home-timeline scoping, conflict detection) lives inside
  the `InMemoryRepository` implementor. There is no intermediate service type; the repository trait is
  effectively service + persistence combined.
- **Why it matters**: maintainability / design. The literal three-tier phrasing in AC2 is not met — the
  "service" tier is nominal. For a demo-scale, single-backing app this is a defensible, common
  simplification (the logic is still cleanly encapsulated behind one replaceable trait, and the testable
  core of AC2 — persistence behind `ChirpRepository`, `Arc<dyn>` seam, in-memory default, no DB — is
  fully satisfied). The risk surfaces only if a second backing (SQLite) is added and the invariant logic
  would then need to be duplicated per-implementor rather than shared in a service above the store.
- **Why not major**: it carries no correctness or contract cost, violates no testable AC clause, and the
  code DAG's wiring/contract checks already PASS. It is a structural-taste deviation from the literal
  wording, appropriately tracked rather than blocking.
- **Recommendation**: if a persistent backing is ever added, lift the cross-backing invariant logic
  (self-follow guard, idempotent count maintenance, timeline assembly) into a service layer over the
  repository so each `ChirpRepository` impl is pure storage. Track as a design note for the CI
  work-items; no action required to land #19.

### ARCH-03  — F1_3: `InvalidBody` validation `details` carries a single generic `field: "body"` rather than the offending field
- **Severity**: minor
- **AC / F1 ref**: F1_3, AC3, AC5
- **Location**: `crates/chirp-server/src/error.rs:139-142` (`InvalidBody` → `FieldError { field: "body", … }`),
  `error.rs:156-160` (`From<JsonRejection>`); contrast the domain path `error.rs:135-138` +
  `validation_field()` `error.rs:164-170` which *does* recover the field
- **Observation**: Two validation sub-paths exist. A domain `ServerError::Validation(ValidationError)`
  lifts the real offending field (`"username"`, `"text"`) into `details`. A transport-boundary
  `ServerError::InvalidBody` (from an axum `JsonRejection`, which is where a `chirp-types`
  `#[serde(try_from = "String")]` value-object failure surfaces during body decode) emits a single
  generic `FieldError { field: "body", message: <rejection text> }`, because the structured field name
  is not recoverable from `JsonRejection` without `serde_path_to_error`. The frozen contract's
  `error_mapping` note requires: *"Populate details (Vec<FieldError>) for validation failures."*
- **Contract-satisfaction reading**: **Satisfies — acceptable trade-off (not blocking on this lens).**
  The contract requires `details` to be a *populated* `Vec<FieldError>` for validation failures; the
  `InvalidBody` path produces exactly that — a non-empty `Vec<FieldError>` with a valid `field` +
  `message`, rendered as the `ApiError` wire shape with `VALIDATION_ERROR`/400 (verified by
  `tests/api.rs::errors::invalid_dto_field_is_rejected_as_400_validation_error`, which asserts
  `!error.details.is_empty()`). The contract does not stipulate that `field` must name the structurally
  precise offending key; the wire *shape* and the `code`/`message`/`details`-present obligation are all
  honored. The limitation is a **fidelity** one: field-level attribution degrades to a generic `"body"`
  marker for the serde-boundary case only. It weakens the *usefulness* of `details` for that one path,
  not the *conformance* of the wire contract.
- **Why it matters**: contract fidelity. A frontend binding per-field errors gets precise attribution
  for domain-constructed validation errors but only a `"body"`-level message for malformed-body
  rejections. Low impact for this demo surface; could matter for form UX later.
- **Gate note**: per the contract (`identities.details_ruling_is_gate_decision`) the final
  acceptable-vs-blocking ruling is the gate's. This lens's contract-conformance analysis: **acceptable /
  minor** — it satisfies "populate details (Vec<FieldError>)" and preserves the wire shape; it does not
  rise to a blocking weakening of the frozen contract.
- **Recommendation**: if precise field attribution for body rejections is later desired, decode via
  `serde_path_to_error` (or a typed two-step decode) so the offending JSON path becomes the `FieldError.field`.
  Optional enhancement; not required to land. Do NOT change here.

---

## Verdict ledger (owned items)

| AC / F1 id | Verdict | Evidence (file:line / route / diff ref) | Finding id (if any) |
|------------|---------|------------------------------------------|---------------------|
| AC1 | conforms (minor note) | All 9 `/api` endpoints mounted in the single `build_router` root — `router.rs:63-75`: `POST /api/users`, `GET /api/users/{id}`, `POST /api/sessions`, `POST /api/chirps`, `GET /api/timeline`, `PUT`+`DELETE /api/users/{id}/follow`, `PUT`+`DELETE /api/chirps/{id}/like`; plus `GET /healthz` (`router.rs:61`, handler `:88`) and the static-file service with SPA `index.html` fallback (`router.rs:55-57`, `:77`). Reverse-chron + cursor + limit-clamp timeline confirmed under AC2/repo semantics. | ARCH-01 (minor) |
| AC2 | conforms (minor note) | `AppState { repo: Arc<dyn ChirpRepository> }` (`state.rs:26-32`); in-memory default `InMemoryRepository` (`in_memory.rs:72-91`); **no DB dependency** — `sqlx`/`sqlite` appear only in doc comments + manifest prose, never in `[dependencies]` (`Cargo.toml` grep: 0 dep hits); whole suite boots DB-free via `build_router(AppState::new(Arc::new(InMemoryRepository::new())))` (`tests/api.rs:180-182`). Repo semantics assessed below. | ARCH-02 (minor) |
| AC3 | conforms | `ServerError::code()` maps every variant → `ErrorCode` (`error.rs:109-118`); `impl IntoResponse` maps all six `ErrorCode`s → status, exhaustive match (`error.rs:191-211`): `VALIDATION_ERROR`→400, `UNAUTHORIZED`→401, `FORBIDDEN`→403, `NOT_FOUND`→404, `CONFLICT`→409, `INTERNAL`→500; `Internal` logs + returns a generic body (no server-detail leak, `error.rs:203-206`). `ApiError`/`ErrorCode`/`FieldError` imported from `chirp_types::api` (`error.rs:38`). End-to-end rows exercised in `tests/api.rs::errors` (409/404/401/403/400). | — |
| AC4 | conforms | `TraceLayer::new_for_http()` on the whole stack (`router.rs:79`); global subscriber installed in the binary only (`main.rs:28`, `:51-57`); `lib.rs` re-exports `build_router`, `AppState`, `AuthUser`, `ValidatedJson`, `ChirpRepository`, `InMemoryRepository` (`lib.rs:41-43`); integration tests drive the real app against the in-memory repo through that surface (`tests/api.rs:200`, `:180-182`). | — |
| AC5 | conforms | No DTO redefinition: server-crate `struct`/`enum` defs are only `ServerError` (`error.rs:51`), `Store`/`InMemoryRepository` (`in_memory.rs:47,73`), `AppState` (`state.rs:26`), `AuthUser` (`auth.rs:45`), `ValidatedJson` (`json.rs:46`) — none a contract type. All DTOs imported from `chirp_types::{api,domain,ids}` (`handlers.rs:48-53`, `repository/mod.rs:47-52`). Wire shape by composition: base `/api` (`router.rs:63-75`); camelCase from `chirp-types` `#[serde(rename_all="camelCase")]` (`api.rs`, `domain.rs`); `Authorization: Bearer` parsed case-insensitively (`auth.rs:65-92`); `ErrorCode` SCREAMING_SNAKE_CASE from `chirp-types` (`api.rs:168-183`). No local contract re-declaration ⇒ no `block`. | — |
| F1_1 | conforms | Fix is live, not dead code: the three body handlers extract via `ValidatedJson<T>` — `create_user` (`handlers.rs:66`), `login` (`handlers.rs:100`), `create_chirp` (`handlers.rs:117`); `ValidatedJson::Rejection = ServerError` (`json.rs:53`) and `ServerError: IntoResponse` (`error.rs:191`) route the failure as `VALIDATION_ERROR`/400 via `From<JsonRejection>` (`error.rs:156-160`); routes mounted in `build_router` (`router.rs:63-66`). Live-path corroborated end-to-end by the passing `tests/api.rs:514` 400-assertion. No orphaned items. | — |
| F1_3 | satisfies (acceptable / minor — gate rules) | `InvalidBody` populates a non-empty `details: Vec<FieldError>` with a generic `field:"body"` (`error.rs:139-142`); contract requires `details` *populated* for validation failures (`chirp-server/contracts/_MANIFEST.yaml:80`); wire shape (`ApiError{code,message,details}`) honored; the generic `body` field is a fidelity limitation for the serde-boundary path only (field name not recoverable from `JsonRejection` without `serde_path_to_error`). Final acceptable-vs-blocking ruling deferred to the gate per `identities.details_ruling_is_gate_decision`. | ARCH-03 (minor) |

### In-memory repository semantics (AC2 sub-assessment)

| Behavior | Verdict | Evidence |
|----------|---------|----------|
| Timeline reverse-chronological | conforms | Ordered by `id` descending (`in_memory.rs:246`, `std::cmp::Reverse(chirp.id.get())`); monotonic-id-as-time rationale documented (`in_memory.rs:19-24`); verified `tests/api.rs:273-301`, `in_memory.rs:539-562`. |
| Cursor pagination | conforms | Opaque cursor = last item's id; only chirps with `id < cursor` returned (`in_memory.rs:228,243`); `next_cursor` `Some` iff more remain via take-one-extra (`in_memory.rs:249-258`); malformed cursor fails safe to first page (`in_memory.rs:226-228`); verified `tests/api.rs:546-602`. |
| Limit clamp | conforms | `limit.unwrap_or(DEFAULT=20).clamp(1, MAX=100)` (`in_memory.rs:221-224`, `repository/mod.rs:57-61`); oversize clamps without error (`tests/api.rs:604-617`, `in_memory.rs:604-616`). |
| Home-timeline scope (self + followees) | conforms | `is_visible = author == viewer || followees.contains(author)` (`in_memory.rs:231-237`); verified `in_memory.rs:539-562`. |
| Follow/unfollow idempotency + count consistency | conforms | Counts move only on genuine `HashSet` insert/remove (`in_memory.rs:283-290`, `:314-321`); `saturating_sub` guards underflow (`:316-320`); verified `in_memory.rs:629-680`. |
| Like/unlike idempotency | conforms | At-most-one `(user,chirp)` via `HashSet`; count moves only on real state change; `saturating_sub` floor (`in_memory.rs:340-344`, `:363-367`); verified `in_memory.rs:682-721`. |
| Conflict / 409 on duplicate handle | conforms | `username_to_id.contains_key` → `ServerError::Conflict` (`in_memory.rs:108-113`); verified `tests/api.rs:397-407`. |
| No-DB / no panic on store ops | conforms | Single `Mutex<Store>`, no `.await` across the guard (`in_memory.rs:9-17,86-91`); poisoned lock → `Internal` not panic (`:86-90`); pre-epoch clock degrades to 0 not panic (`:95-101`). (Panic/`unsafe` discipline is the Rust spoke's AC6; noted here only as it bears on the seam.) |

---

## Notes for the gate

- **Block/major open on this lens?** No. No frozen-contract violation (no DTO redefinition, no wrong
  wire shape, no missing/incorrect status mapping, no route absent). Disposition is
  minor/nit-only: ARCH-01, ARCH-02, ARCH-03 are all `minor` and non-blocking.
- **F1_3 is the one item requiring an explicit gate ruling.** This lens reads it as *satisfies /
  acceptable* (populates `details`, preserves the wire shape; fidelity-only limitation on the serde
  boundary). The contract assigns the final acceptable-vs-blocking call to the gate.
- **Discipline observed:** review-only. No source edited, no push/rebase/relock, `main` untouched, no
  `gh pr review` posted. Evidence gathered by read-only file inspection + read-only `grep`/`git` over
  the `714d50f` checkout. The `Cargo.lock` CONFLICTING/DIRTY mergeability was NOT assessed (out of scope
  per the hub).
