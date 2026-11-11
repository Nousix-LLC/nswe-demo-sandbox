## Review verdict: APPROVE — chirp-server (PR #19, head `714d50f`)

**Authoritative landing verdict lives in the review DAG's root `SYNTHESIS.md`** (observation seam). This
gh review posts as **COMMENTED** because of the self-review platform block — that is expected and does
not change the verdict below.

### Verdict: **APPROVE**
No open `block` or `major` finding across the four review lenses (Rust soundness, architecture/contract,
test adequacy, code-review quality). All open items are `minor`/`nit` — land-then-fix / tracked.

### Acceptance criteria: 8 / 8 conform
- **AC1** full REST surface (9 `/api` routes + `/healthz` + SPA fallback in one `build_router`) — conforms
- **AC2** layered transport→repository behind `Arc<dyn ChirpRepository>`, in-memory default, no DB — conforms
- **AC3** typed `ServerError → ApiError/ErrorCode → HTTP status`, all six rows, exhaustive `IntoResponse` — conforms
- **AC4** `tracing` + `lib.rs` exposes router/repo so integration tests drive the real app — conforms
- **AC5** DTOs imported from `chirp-types`, never redefined; wire shape by composition — conforms
- **AC6** no runtime panic / no `unsafe` on request paths (lock-poison→500, not panic) — conforms
- **AC7** fmt/clippy(`-D warnings`)/rustdoc(`missing_docs`)/README — conforms (README staleness is a tracked minor)
- **AC8** 44-test suite (24 unit + 20 integration, no DB) drives the real app, covers 400/401/403/404/409 + timeline clamp — conforms

### F1 remediation (validation → 400 `ApiError{VALIDATION_ERROR, details}`): **SOUND**
- **Live, not dead** (F1_1): the three body handlers extract via `ValidatedJson<T>`; `Rejection = ServerError` routes `From<JsonRejection>` → `VALIDATION_ERROR`/400; clippy `-D warnings` clean ⇒ no orphaned items.
- **Flipped test, no 422 pin** (F1_2): `tests/api.rs::errors::invalid_dto_field_is_rejected_as_400_validation_error` asserts 400 / `ErrorCode::ValidationError` / `!details.is_empty()`; no `422`/`UNPROCESSABLE_ENTITY` assertion anywhere (remaining `422` strings are doc/comment only). Mechanically re-corroborated.
- **No regression** (F1_4): 401/403/404/409 integration tests + timeline limit-clamp still green.
- **Rust soundness**: the `FromRequest` extractor + local-type `From<JsonRejection>` impl is sound and idiomatic (correct bounds, body-extractor-last ordering, no orphan abuse, no panic).

**`details`-limitation ruling (gate decision): ACCEPTABLE trade-off — not a blocking weakening of the wire contract.**
The `InvalidBody` (serde-boundary) path emits a single generic `FieldError{field:"body", message:…}` because the
offending field name is not structurally recoverable from axum's `JsonRejection` without `serde_path_to_error`.
This **satisfies** the contract's "populate `details` (`Vec<FieldError>`)" requirement: `details` is non-empty and
the full `ApiError{code,message,details}` wire shape is preserved; the contract does not require `field` to name
the precise offending key, and the domain-validation path *does* recover it. The gap is a confined **fidelity**
limitation on one sub-path, the minimal-dependency trade-off is documented in four places, and it is appropriately
`minor`, not `block`.

### F2 disposition: non-gating tracked debt
Rustdoc intra-doc-link warnings fire only under `RUSTDOCFLAGS=-D warnings` (exit 101: broken/private/redundant
links). `cargo doc -D warnings` is **not** in the authoritative gate set (build/test/fmt/clippy — all PASS cold),
and `missing_docs` **is** satisfied. Confirmed non-gating. **Recommend tracking as CI work-items #10–#13**, folded
together with the stale-README doc fix (CRQ-01).

### Open findings (all minor/nit, none blocking)
- **minor** ARCH-01 unknown `/api/*` falls through to SPA `index.html` (200 HTML) instead of JSON 404
- **minor** ARCH-02 nominal service tier (domain logic in the repository implementor) — defensible at this scale
- **minor** ARCH-03 F1 `details` generic `body` fidelity (ruled acceptable above)
- **minor** TEST-01 SPA-fallback route has no integration test
- **minor** CRQ-01 README still documents the old 422 "known gap" and omits the 400 row
- **minor** CRQ-02 F2 rustdoc-link debt (tracked, above)
- **nit** RUST-01 guarded-but-panic-capable `HashMap` indexing (not reachable today); RUST-02 `into_api_error(&self)` naming; RUST-03/CRQ-03 surplus `ValidatedJson` derives; TEST-02 500-row not integration-reachable (correct)

Note: the PR's CONFLICTING mergeability is a known `Cargo.lock` restale (out of review scope), cleared mechanically
before landing — not a code finding.
