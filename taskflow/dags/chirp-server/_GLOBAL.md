# chirp-server — axum REST API + persistence + static/SPA serving (subtree hub)

## Project Context

**Status**: Active (decomposed; awaiting subtree resolution)

This subtree delivers **work-item #8** of the `Nousix-LLC/nswe-demo` engagement: the
`crates/chirp-server` crate — the **axum REST API backend** for the `chirp` Twitter-style app.
It composes against the **already-landed shared contract crate `crates/chirp-types`** (#7, on
`main` at squash commit `2e32aed`): the server imports `chirp-types` domain entities + API DTOs
directly and MUST NOT re-declare the wire contract. Delivered as a PR into `main` on branch
`work/chirp-server`, body `Closes #8`.

### Objective

Produce a clean, layered, well-documented axum server — REST endpoints over the `chirp-types`
DTOs, persistence behind a repository trait (in-memory default), static-asset + SPA serving, a
health endpoint, structured logging, and end-to-end API integration tests — and deliver it as a
reviewed PR with a verification verdict.

### Scope

**In scope:**
- A new workspace member crate `crates/chirp-server` (axum; native binary + library split), slotting
  into the virtual workspace.
- A **repository trait** abstracting persistence, with an **in-memory implementation** as the default
  backing (the server boots and `cargo test` runs with NO database).
- REST endpoints for the core surface: timeline (list), post a chirp, create user, login/session,
  user profiles, follow/unfollow, like/unlike — using `chirp-types` request/response DTOs.
- Typed server errors mapped to HTTP status + the `ApiError`/`ErrorCode` wire contract.
- Static-file serving (a `static/`/`dist/` dir) + SPA fallback route, and a health endpoint (`GET /healthz`).
- Structured logging (`tracing`).
- End-to-end API integration tests (spin the router against the in-memory repo; assert status + DTO round-trips + error paths).
- Quality: `cargo build --workspace` clean, `cargo test` passes, `cargo fmt --check` clean,
  `cargo clippy --all-targets -- -D warnings` clean, rustdoc on public items, a `README.md`.
- Delivery: branch `work/chirp-server`, PR into `main`, body ending `Closes #8`.

**Out of scope:** the frontend SPA (#9 — only the serving path is wired; a placeholder static dir is
acceptable), deploy/CI (#10–#13), any change to `main` or to crates other than slotting the new
member in, and any required running database for tests.

### Success Criteria

- [ ] `crates/chirp-server` slots into the workspace and `cargo build --workspace` succeeds on the stable host target.
- [ ] All listed REST endpoints implemented over `chirp-types` DTOs; typed errors → HTTP status + `ApiError`.
- [ ] Persistence behind a repository trait with an in-memory default; no DB required for `cargo test`.
- [ ] Static serving + SPA fallback wired; `GET /healthz` present; `tracing` structured logging present.
- [ ] Unit tests (repository) + integration tests (API end-to-end) pass; `fmt --check` and `clippy -D warnings` clean.
- [ ] `README.md` describes endpoints + how to run + the repository-choice rationale; rustdoc on public items.
- [ ] PR opened into `main` (`Closes #8`); `SYNTHESIS.md` at this workspace records a PASS/FAIL verdict with evidence + PR URL.

---

## Constraints and Requirements

- **Crate identity**: name `chirp-server` at `crates/chirp-server`; depends on `chirp-types` via a
  workspace **path dependency** for ALL wire types — single source of truth; never fork or re-declare the contract.
- **Edition 2021 / rust-version 1.82 / stable toolchain**; inherit workspace lints
  (`missing_docs=warn`, `unsafe_code=warn`, `clippy::all=warn`) via `[lints] workspace = true`, and
  additionally satisfy `clippy --all-targets -- -D warnings`.
- **Demo runs without external infra**: in-memory repository behind the trait is the default; SQLite/`sqlx`
  is an OPTIONAL, documented alternative backing only if a child chooses to add it — it MUST NOT become a
  test prerequisite.
- **Isolated clone**: ALL repo work happens in ONE shared clone at `checkout/` under this workspace
  (`/home/user/nousix-runtime/nswe-demo/taskflow/dags/chirp-server/checkout`). The first spoke creates it;
  later spokes operate on the same clone. Do NOT reuse any other process's clone.
- **Never** commit to or force-push `main`. Local commits on `work/chirp-server`; push the branch; open the PR only.
- **No commit-attribution trailers.**
- Match conventions already on `main` (read the root `Cargo.toml` and an existing crate before authoring).

---

## Input Specifications

| Source | Location | Purpose |
|--------|----------|---------|
| This hub | `_GLOBAL.md` | Shared context, constraints, contract pointer |
| Contract | `contracts/_MANIFEST.yaml` | Frozen shared conventions (clone path, branch, crate id, module layout), the repository-trait seam spec, the error-mapping table, and the gate's assertion set |
| Dependency contract | `crates/chirp-types` (on `main`) | The imported domain entities + API DTOs; the wire contract to compose against (do not re-declare) |
| Repo | `Nousix-LLC/nswe-demo` (clone to `checkout/`) | Base `main` with the landed virtual workspace + `crates/ferric` + `crates/ferric-router` + `crates/chirp-types` |

---

## Subtree Methodology Posture

- **Dominant task type**: *Writing new code* (an axum REST backend) → primary bundle **`rust`**; plus
  **`core`** (coding standards, error handling, commit practices) and **`architecture`** (the layering
  transport → service → repository; the repository-trait boundary; how static serving + SPA fallback compose).
  The integration-test leaf leans on **`testing`** (API integration tests; trait-against-impl testing;
  DTO round-trips). The terminal gate is a *Synthesizing/verifying a hub-and-spoke decomposition* task →
  **`synthesis`** (+ `code-review`).
- **Primary bundles in scope subtree-wide**: `rust`, `core`, `architecture` for implementation; `testing`
  for the test leaf; `synthesis`, `code-review` for the gate. Descendants may assume these without re-justifying.
- **Cross-cutting bindings**: the server is a layered system whose seam is the **repository trait** and whose
  error discipline is **typed-error → `ApiError`/`ErrorCode` → HTTP status**; both bind every leaf even though
  only one leaf owns each. `chirp-types` is the single source of truth for wire types — no leaf re-declares a DTO.
- **Suggestion, not prescription**: descendant agents retain final judgment over what they load, and each
  re-runs its OWN decompose-evaluation — a leaf whose own brief still spans multiple concerns MUST decompose further.

## Subtree-Wide Constraints

- Crate name/path, path-dependency on `chirp-types`, edition/rust-version, in-memory-default rule,
  isolated-clone path, branch name, never-touch-`main`, and no-attribution-trailers are fixed above and in
  `contracts/_MANIFEST.yaml`; descendants conform and do not re-litigate them.
- The clone is a **serially shared** artifact: the pipeline order (scaffold_and_repository → api_layer →
  integration_tests_and_docs → synthesis_gate) guarantees no two children write the clone concurrently.

---

## Task Structure

### Overview

```
_GLOBAL.md (this hub)
├── contracts/_MANIFEST.yaml                       (frozen conventions + repo-trait seam + error map + gate assertions)
├── SUBTASK_scaffold_and_repository/_BRIEF.md      (clone; scaffold crate; repository trait + in-memory impl + unit tests; commit)
├── SUBTASK_api_layer/_BRIEF.md                    (axum transport/service: handlers, router, state, error→HTTP, static+SPA, health, tracing, bin; commit)
├── SUBTASK_integration_tests_and_docs/_BRIEF.md   (end-to-end API integration tests + README + rustdoc polish; commit)
└── SUBTASK_synthesis_gate/_BRIEF.md               (verification gate; push + PR; SYNTHESIS.md verdict at this hub)
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_scaffold_and_repository` | none | Create the `checkout/` clone + `work/chirp-server` branch; scaffold `crates/chirp-server` (Cargo.toml, workspace member entry, lib/bin module layout, deps); define the `ChirpRepository` trait + the server error enum (per the contract seam spec); implement the in-memory repository with unit tests; build + test locally; commit. | `SUBTASK_scaffold_and_repository/IMPLEMENTATION_NOTES.md` (trait signature, error enum, module layout, clone/branch pointers, local build/test status) |
| `SUBTASK_api_layer` | `SUBTASK_scaffold_and_repository` | Build the axum transport/service layer against the committed repository trait: handlers for all endpoints over `chirp-types` DTOs, router + `AppState`, typed-error → `ApiError`/HTTP-status mapping (`IntoResponse`), static-file service + SPA fallback, `GET /healthz`, `tracing` setup, and the binary `main`. Build locally; commit. | `SUBTASK_api_layer/API_NOTES.md` (route table, state design, error-mapping, serving/fallback, run instructions, local build status) |
| `SUBTASK_integration_tests_and_docs` | `SUBTASK_api_layer` | Author end-to-end API integration tests (spin the router against the in-memory repo; assert status codes, DTO round-trips, and error paths across the acceptance surface) and the crate `README.md` + rustdoc polish on public items. Build + test locally; commit. | `SUBTASK_integration_tests_and_docs/TEST_NOTES.md` (test inventory, results, acceptance-criteria coverage map, README summary) |
| `SUBTASK_synthesis_gate` | `SUBTASK_scaffold_and_repository`, `SUBTASK_api_layer`, `SUBTASK_integration_tests_and_docs` | Verification gate: run authoritative `cargo build --workspace` / `cargo test` / `cargo fmt --check` / `cargo clippy --all-targets -- -D warnings`; run the four-check model (contract/wiring/dedup/review) over the combined output; push the branch; open the PR; record the PASS/FAIL verdict. On FAIL, schedule remediation as decomposed fix-tasks rather than green-washing. | `SYNTHESIS.md` (at THIS hub workspace — the fold location / observation seam) |

### Dependency Graph

```
SUBTASK_scaffold_and_repository ──► SUBTASK_api_layer ──► SUBTASK_integration_tests_and_docs ──► SUBTASK_synthesis_gate
```

---

## Contract

**Contract location**: `contracts/` (read-only for every descendant)
**Contract kind**: `yaml_schema` (a thin handoff/convention manifest + seam spec + assertion set)

The cross-sibling edges in this subtree are **serialized** by the dependency chain (each spoke reads the
real committed clone produced by its predecessor), so the repository trait and error type do not need to be
frozen as compilable Rust artifacts in `contracts/` — the consumer reads the real code. What the manifest
DOES freeze before any child runs are: (1) the *forced/stable* shared conventions (clone path, branch name,
crate path/name, workspace membership, module-layout skeleton); (2) the **repository-trait seam spec** — the
capability set the trait MUST cover so the api_layer composes without a gap; (3) the **error-mapping table**
(server-error variant ↔ `chirp-types::ErrorCode` ↔ HTTP status) so the transport layer maps consistently; and
(4) the gate's **assertion set** (build/test/fmt/clippy + wiring identities), each with a runnable command.
See `contracts/_MANIFEST.yaml`.

### Ownership (summary; authoritative in the manifest)

| Artifact | Owner |
|---|---|
| `checkout/` clone, `work/chirp-server` branch, `crates/chirp-server/Cargo.toml` + workspace member entry, repository trait + in-memory impl + its unit tests | `SUBTASK_scaffold_and_repository` |
| axum handlers, router, `AppState`, error `IntoResponse`, static+SPA serving, health, tracing, binary `main` | `SUBTASK_api_layer` |
| `tests/` integration tests, `crates/chirp-server/README.md`, rustdoc polish | `SUBTASK_integration_tests_and_docs` |
| The PR into `main` + `SYNTHESIS.md` verdict | `SUBTASK_synthesis_gate` |

### Identities (the gate asserts these; no silent plug)

- [ ] `cargo build --workspace` succeeds (the crate slots into the workspace).
- [ ] `cargo test` passes on the native host target (repository unit tests + API integration tests), with no DB running.
- [ ] `cargo fmt --check` clean.
- [ ] `cargo clippy --all-targets -- -D warnings` clean.
- [ ] Every REST endpoint in scope is routed and reachable; handlers call through the `ChirpRepository` trait (no bypassing).
- [ ] Wire types come from `chirp-types` (no DTO re-declared in `chirp-server`); errors surface as `ApiError`/`ErrorCode`.
- [ ] A PR into `main` exists with body ending `Closes #8`.

---

## Output Specifications

| Deliverable | Location | Description |
|-------------|----------|-------------|
| `chirp-server` crate | `checkout/crates/chirp-server/` (committed to `work/chirp-server`) | The axum REST API backend |
| Scaffold/repository handoff | `SUBTASK_scaffold_and_repository/IMPLEMENTATION_NOTES.md` | Trait + error enum + module layout + build status |
| API-layer handoff | `SUBTASK_api_layer/API_NOTES.md` | Routes, state, error mapping, serving, run instructions |
| Test/docs handoff | `SUBTASK_integration_tests_and_docs/TEST_NOTES.md` | Test inventory + results + acceptance coverage |
| Verdict / fold record | `SYNTHESIS.md` (this workspace) | Build/test/fmt/clippy verdict, four-check results, diff manifest, PR URL, PASS/FAIL |
