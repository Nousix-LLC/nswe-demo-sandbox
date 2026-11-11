# Findings — SUBTASK_workflow_correctness (concerns 1 + 2)

**Spoke**: `SUBTASK_workflow_correctness` · id prefix `WF-`
**Concerns covered**: 1 (CI workflow correctness) and 2 (reproducibility / pinning)
**PR**: #21 — "CI: GitHub Actions for the Rust/WASM workspace (#11)", `Nousix-LLC/nswe-demo`
**PR head reviewed**: `c8123376` (`c8123376ca1794c0b0466f41a1204bf3c3301b16`)
**Artifact under review**: `.github/workflows/ci.yml` (new file, 194 lines)
**Posture**: read-only review; relied on the already-folded machine-PASS (fmt/clippy/test/doc/wasm/actionlint green at head). Spot-checks performed: fetched `ci.yml` at head, `gh pr view`/`gh pr checks`, `Cargo.lock` wasm-bindgen version, YAML validity. `actionlint` not re-run locally (not installed; covered by the machine gate).

---

## Findings

| id | severity | concern | location | finding | rationale |
|----|----------|---------|----------|---------|-----------|
| WF-1 | minor | 2 | `ci.yml:33` (`RUST_TOOLCHAIN: "1.97"`); applied at L45/47, L58/60, L73/76, L87/89, L121/123 | Toolchain is pinned to the **series** `"1.97"`, not an exact patch. `dtolnay/rust-toolchain` resolves `"1.97"` to the latest `1.97.x` available at run time, so a future 1.97 point release would silently change the toolchain a "clean checkout" resolves to. | The env comment (L29) states the intent is that "a clean checkout reproduces the result"; a series pin leaves a (small) patch-level float against that intent. Drift impact is low — Rust point releases are rare and bugfix-only — so it does not block landing. Suggestion: pin `"1.97.0"` or add a committed `rust-toolchain.toml` for an exact, reproducible toolchain. |
| WF-2 | minor | 2 | `ci.yml:30-33` (toolchain-selection comment + `RUST_TOOLCHAIN`) | CI builds **only** on Rust 1.97 and therefore does not exercise or enforce the workspace manifest's declared MSRV of 1.82; per the inline comment the locked dependency graph no longer parses on 1.82 (e.g. `hyper-util 0.1.21`), so the stated MSRV is effectively unmet by the locked graph. | This is a real reproducibility/claim-accuracy drift: the declared MSRV is unverified and contradicted by the locked deps. It is **documented** in-file with a follow-up (L32 references a `SYNTHESIS.md` MSRV-vs-locked-deps follow-up), is pre-existing to the manifest rather than introduced by `ci.yml`, is not part of issue #11's acceptance criteria, and does not break this PR's (internally consistent, 1.97 + `--locked`) CI — hence minor, not blocking. Suggestion: reconcile the manifest `rust-version` with reality (raise MSRV, or restore 1.82-parseable locked deps) under the noted follow-up, or add an explicit MSRV-check job if 1.82 support is a real requirement. |

No `block` and no `major` findings. The two minor findings are advisory and do not change the verdict.

---

## Concern-coverage notes

**Concern 1 — CI workflow correctness: CLEAN (no findings).** Examined, and confirmed correct:
- **Stated commands run.** Verified line-by-line against issue #11: `fmt` → `cargo fmt --all --check` (L50); `clippy` → `cargo clippy --workspace --all-targets --locked -- -D warnings` (L66); `test` → `cargo test --workspace --locked` (L79); `wasm` → builds `chirp-frontend` + example to `wasm32-unknown-unknown`, generates `wasm-bindgen` output, asserts `pkg/chirp.js` + `pkg/chirp_bg.wasm` exist (L99–109); `doc` → `cargo doc --workspace --no-deps --locked` with `RUSTDOCFLAGS: "-D warnings"` (L117–127). All match the stated intent.
- **Triggers correct.** `pull_request`→`[main]`, `push`→`[main]`, plus `workflow_dispatch` (L10–15) — satisfies issue #11's "runs on PR + push to `main`". YAML validity confirmed; jobs parse as `fmt, clippy, test, wasm, doc, image`.
- **Required-check-stable job names.** Each job sets an explicit `name:` equal to its id (L40/53/69/82/112), so the five check names are stable identifiers suitable to select in branch protection. The `image` job is correctly **not** a PR required check — it is gated `if: github.event_name == 'push' && github.ref == 'refs/heads/main'` and `needs: [fmt,clippy,test,wasm,doc]` (L133–134), and the live PR run shows it `skipping` (neutral), so it will not hang PR merges. (Branch protection should select the five job names, not a top-level "CI" context — advisory, not a file defect.)
- **Matrix/caching sound.** No build matrix is used (single `ubuntu-latest`, single toolchain) — acceptable and simpler for this workspace; not a defect. Caching uses `Swatinem/rust-cache@v2` on the four compiling jobs (clippy L62, test L77, wasm L91, doc L125) and correctly omits it from `fmt` (which only runs `rustfmt`, no compilation). Concurrency group (L24–26) cancels superseded non-`main` runs and never cancels `main` — sound. `CARGO_INCREMENTAL: "0"` (L36) is correct for cold CI builds.
- **`--locked` consistency.** Present on every dependency-resolving cargo invocation (clippy, test, both wasm `cargo build`s, the `cargo install` of wasm-bindgen-cli, and doc). Its absence on `cargo fmt` (L50) and on the non-cargo `wasm-bindgen` CLI call (L105–107) is correct — neither resolves the dependency graph.
- Live evidence: `gh pr checks 21` shows fmt/clippy/test/wasm/doc = pass, image = skipping, consistent with the folded machine-PASS at head.

**Concern 2 — reproducibility / pinning: 2 minor findings (WF-1, WF-2); core pinning is sound.** Examined:
- **wasm-bindgen-cli ⇄ lockfile match VERIFIED.** `cargo install --locked wasm-bindgen-cli --version 0.2.129` (L94–95) exactly matches `wasm-bindgen 0.2.129` in `Cargo.lock` at head (`version = "0.2.129"`, checksum `9bb54f33…`). No version skew — the hard-runtime-error risk the inline comment (L92–93) warns about does not exist at this head. This is the most important reproducibility assertion for the wasm job and it holds.
- **`--locked` cargo** throughout → the dependency graph is resolved from `Cargo.lock`, not re-solved; reproducible.
- **`Swatinem/rust-cache@v2` cache-key correctness: sound.** rust-cache@v2 keys by default on the `Cargo.lock` hash plus the rustc version (and job/workspace), i.e. exactly the "keys on `Cargo.lock` + rustc" the brief asks for. Cache-poisoning / stale-cache correctness risk is negligible here: with `--locked` and a pinned toolchain, a stale or mismatched cache cannot cause a divergent build output — cargo validates the locked graph and rustc identity is part of the key. No drift finding against the cache.
- **Drift risks flagged explicitly** (per the brief's mandate): toolchain series-float (WF-1) and MSRV-not-enforced (WF-2) above. No other version-float, cache-correctness, or lockfile-skew risk found.

---

## Cross-references (interaction notes; verdicts left to the owning spokes)

- **Action pinning by tag/branch vs commit SHA** — `dtolnay/rust-toolchain@1.97`, `Swatinem/rust-cache@v2`, `actions/checkout@v4`, and the `docker/*@vN` actions are pinned by mutable tags/branches rather than immutable commit SHAs. This is a **supply-chain** concern owned by `SUBTASK_supply_chain_security` (concern 3, issue #24); noted here only because it is adjacent to WF-1's reproducibility float — not adjudicated here.
- **`image` job internals** — build context, image name/tag derivation, GHCR auth, and the "Dockerfile-missing skip" logic are owned by `SUBTASK_image_job` (concern 4). I assessed the `image` job only insofar as it affects overall workflow correctness and PR required-check stability (correct: excluded from PR checks); I did not adjudicate its build/publish correctness.

---

## Spoke roll-up

**block: 0 · major: 0 · minor: 2 (WF-1, WF-2) · nit: 0**

Local conclusion for this spoke: concerns 1 and 2 are both satisfied. The CI workflow is correct and reproducible at head `c8123376`; the two minor findings are advisory drift notes and do not force `REQUEST-CHANGES`. On this spoke's scope alone, nothing blocks landing.
