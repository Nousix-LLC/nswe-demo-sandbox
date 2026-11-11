# SYNTHESIS — ci-actions (work-item #11): GitHub Actions CI for the Rust/WASM workspace

**Verdict: PASS.** CI is stood up, the workspace at the PR head passes every check the workflow
defines (verified both locally and in the real GitHub Actions runner), and the two deferred
#8-review minors are folded in. Delivered as commits on `work/ci-actions` and **PR #21 into `main`
(`Closes #11`)**. This item did **not** merge the PR or push to `main` — the overseer lands after a
review DAG (P1).

- **Repo:** `Nousix-LLC/nswe-demo` · **Base:** `main @ fcfc7a2` · **Branch:** `work/ci-actions`
- **PR:** https://github.com/Nousix-LLC/nswe-demo/pull/21 (OPEN, not merged)
- **Head commit:** `c812337`
- **Decompose evaluation:** `Atomic` (one responsibility — stand up and validate the CI pipeline —
  delivered as one commit series / one PR over one mutable git working tree; no clean parallel
  ownership partition to decompose into).

---

## Deliverable: `.github/workflows/ci.yml`

Validates every pull request and every push to `main`; `workflow_dispatch` for manual runs. Six jobs
with stable names (the first five are PR + `main` required-check-ready; `image` is `main`-push-only).

| Job | Command / purpose | Required-check candidate |
|-----|-------------------|--------------------------|
| `fmt` | `cargo fmt --all --check` | yes |
| `clippy` | `cargo clippy --workspace --all-targets --locked -- -D warnings` (promotes the workspace `missing_docs`/`unsafe_code`/`clippy::all` warns to errors) | yes |
| `test` | `cargo test --workspace --locked` | yes |
| `wasm` | `chirp-frontend` `wasm32-unknown-unknown` build + example + `wasm-bindgen --target web` → `pkg/chirp.js` + `pkg/chirp_bg.wasm` | yes |
| `doc` | `cargo doc --workspace --no-deps --locked` under `RUSTDOCFLAGS=-D warnings` | yes |
| `image` | **`main` push only** — build & push `ghcr.io/nousix-llc/chirp-server` to GHCR | no (does not run on PRs) |

### Checks run — results (acceptance #6)

Verified at head `c812337`, **locally** and in the **real runner** (Actions run `37581289276`):

| Check | Local | GitHub runner |
|-------|-------|---------------|
| `fmt` | pass | **pass** (14s) |
| `clippy -D warnings` | pass | **pass** (35s) |
| `test --workspace` (14 suites / 207 tests) | pass | **pass** (48s) |
| `doc -D warnings` | pass | **pass** (43s) |
| `wasm` build + bindgen | pass | **pass** (2m19s) |
| `actionlint` on `ci.yml` | clean | — |

Total pipeline ≈ 2m20s (parallel) — well under the <10-minute fast-feedback target. The workflow
**self-validated on its own introduction PR (#21)**.

### Concerns covered (per the brief)
- **CI correctness & reproducibility** — valid YAML (`actionlint` clean; acceptance #1); toolchain
  pinned to `1.97`, actions pinned (`dtolnay/rust-toolchain@1.97`, `Swatinem/rust-cache@v2`,
  `docker/*@v3/v5/v6`, `actions/checkout@v4`), `wasm-bindgen-cli` pinned to the **locked `0.2.129`**
  (a crate↔CLI version skew is a hard error), `--locked` cargo so a clean checkout reproduces.
- **Build-graph & caching** — `Swatinem/rust-cache@v2` caches `~/.cargo` + `target/`, keyed on
  `Cargo.lock` + rustc (does not mask staleness); `wasm32-unknown-unknown` installed only in the
  `wasm` job. No matrix (single-target workspace — a matrix would add cost without coverage).
- **Security / least-privilege** — top-level `permissions: contents: read`; only `image` adds
  `packages: write`. GHCR auth is the built-in `GITHUB_TOKEN` (no PATs / long-lived secrets); GHCR
  login + push scoped to `main` pushes. Actions pinned.
- **Required-check friendliness & ergonomics** — stable job names; PR-vs-`main` triggering avoids
  redundant feature-branch runs; `concurrency` cancels superseded non-`main` runs for fast feedback.
- **Documentation accuracy** — the two folded minors (below).
- **Rust/CI idiom** — current `dtolnay` + `Swatinem` + `docker/*` action stack.

---

## Folded #8-review minors

### CRQ-02 / F2 — rustdoc intra-doc-link debt (resolved; it is the `doc` gate's enforcement)
`cargo doc --workspace --no-deps` under `RUSTDOCFLAGS=-D warnings` reported **79** intra-doc-link
errors across `ferric`, `ferric-router`, `ferric-http`, `chirp-frontend`, `chirp-server`. All
resolved so the gate is green **without weakening the check** (commit `c2a60d2`). Four categories:
- **29 redundant explicit link targets** — `` [`X`](path) `` → `` [`X`] `` (the bare label already
  resolves to the same item). Applied per-file to the flagged occurrences only.
- **5 public-doc→private-item links** — `Runtime`, `ReactiveScope`, `Store`, `static_dir`,
  `api_base_url` rendered as plain code spans.
- **2 ambiguous links** — `axum::serve` disambiguated to the function; `async_trait` de-linked (this
  rustdoc rejects the `attribute@` disambiguator).
- **~43 unresolved forward-references** — the `chirp-frontend` walking-skeleton module docs reference
  items a later feature spoke adds (`ApiClient`, `AppContext`, `ComposeState`, …), plus the server
  binary `main` (not in the lib doc graph). Rendered as plain code spans (a broken link → a readable
  code span is strictly an improvement; no behavior change).

All changes are doc comments (`///` / `//!`) only — a mechanical audit of the staged diff confirmed
**zero application-logic lines changed**.

### CRQ-01 — README validation-error status 422 → 400 (resolved)
`crates/chirp-server/README.md` omitted the `VALIDATION_ERROR` row and carried a **stale** "known
gap" note claiming DTO-validation failures surface as HTTP **422**. Finding **F1 is already fixed in
code** (commit `714d50f`): the `ValidatedJson` extractor maps deserialization/validation failures to
`ServerError::Validation` → `VALIDATION_ERROR` → **400** (`ErrorCode::ValidationError => BAD_REQUEST`,
`crates/chirp-server/src/error.rs:194`). A literal "422→400" digit swap would have made the sentence
self-contradictory, so — per the brief's goal "docs match the server's real behavior" — I added the
missing **400** `VALIDATION_ERROR` table row and rewrote the note to state the resolved behavior
(commit `763b0e4`).

---

## #12 (containerize) ordering — handled honestly (gate this before relying on the image)

The `image` job needs the **multi-stage `Dockerfile` that work-item #12 has NOT yet landed**. Rather
than fabricate a build, the job:
1. runs **only** on `github.event_name == 'push' && github.ref == 'refs/heads/main'` (never on PRs);
2. first detects `./Dockerfile`; if absent it emits a `::notice::` ("awaiting #12") and the job
   **succeeds while building nothing**; the GHCR login / metadata / buildx / build-push steps are all
   gated on `steps.dockerfile.outputs.present == 'true'`.

**Consequence for the overseer:** on `main` today the `image` job is green-but-no-op. Once #12 adds
`./Dockerfile` (repo root, `context: .`, `file: ./Dockerfile` — the paths this job assumes), the job
builds and pushes `ghcr.io/nousix-llc/chirp-server` automatically on the next `main` push, **with no
edit to `ci.yml`**. If #12 places the Dockerfile elsewhere, update `file:`/`context:` accordingly.
Do not adopt `image` as a required check until #12 has landed (it would be a no-op gate; and it never
runs on PRs regardless).

---

## Repo-admin / follow-up actions (outside this item's write scope)

1. **Branch protection** — adopt `fmt`, `clippy`, `test`, `wasm`, `doc` as **required status checks**
   on `main` (Settings → Branches, or a ruleset). The jobs are named stably for this; configuring it
   is a repo-admin action, not a workflow change.
2. **GHCR package visibility** — the first `main` build (post-#12) creates the
   `ghcr.io/nousix-llc/chirp-server` package; set its visibility (public/private) and link it to the
   repo in the org's packages settings.
3. **MSRV vs. locked deps (pre-existing, flagged — not fixed here).** The root manifest declares
   `rust-version = "1.82"`, but the locked dependency graph no longer parses on 1.82 (e.g.
   `hyper-util 0.1.21`). CI therefore pins `1.97`, not the declared MSRV. Resolve separately by
   either bumping the declared `rust-version` to a floor that the locked graph supports or pinning
   deps down — and, if MSRV is a real guarantee, add a dedicated MSRV job. Out of scope for #11
   (it is a dependency/manifest concern, not CI setup).

---

## Process note — decompose evaluation & a runtime size signal

Evaluated `Atomic` at dispatch: the six named "concerns" are review lenses on one artifact (`ci.yml`),
and the folded minors are in-service doc corrections, all landing as one commit series on one branch
over one mutable git tree — no clean parallel ownership partition. During execution the rustdoc debt
proved larger than estimated (**79** errors vs. an initial read of ~28 concentrated in one crate).
Per TASK_DECOMPOSITION_FRAMEWORK §Pushing Through, this is a **size misestimate on a genuinely
single-responsibility sub-task** ("resolve the doc-link debt" — one kind of change, one kind of
output), not a responsibility misclassification — so I pushed through (recorded here as the framework
asks), fixing the debt with one deterministic, idempotent, per-file-scoped script rather than 79
hand-edits. Total ≈ one coherent pass, well within the atomic tool-call envelope.

## Scope boundary (non-goals honored)
Did **not** containerize the app (#12) or author deploy manifests / the ArgoCD Application (#13). Did
**not** change application behavior beyond CRQ-01 (one doc row) and CRQ-02 (doc comments). Did **not**
merge PR #21 or push to `main`.

## Commits on `work/ci-actions`
- `c2a60d2` docs: resolve rustdoc intra-doc-link debt for the -D warnings gate (CRQ-02)
- `763b0e4` docs(chirp-server): correct validation-error status to 400 in the API table (CRQ-01)
- `c812337` ci: add GitHub Actions workflow for the Rust/WASM workspace (#11) — `Closes #11`
