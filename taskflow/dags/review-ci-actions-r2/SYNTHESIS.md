# SYNTHESIS — Landing verdict: PR #21 "CI: GitHub Actions for the Rust/WASM workspace (#11)"

**Repo**: `Nousix-LLC/nswe-demo` · **PR**: #21 → base `main`
**Reviewed head**: `c8123376` (`c8123376ca1794c0b0466f41a1204bf3c3301b16`) — the head this review DAG examined
**Gate**: `SUBTASK_synthesis` (concern 6 + fold) · all four spokes COMPLETED and conformant
**Produced**: verification gate over 4 review spokes; this file is both the gate's terminal record and the fold record that resolves the SUSPENDED parent DAG.

---

## ⬛ VERDICT

> ### Reviewed head `c8123376`: **REQUEST-CHANGES**
> 1 `major` finding (IMG-1); 0 `block`. Per the contract verdict rule
> (`APPROVE` iff `block==0 AND major==0`), one `major` forces `REQUEST-CHANGES`.
>
> ### Landed code (PR already MERGED at `716817bc` / merge commit `ada3aa97`): **APPROVE-equivalent — the one required change was made before merge.**
> The sole blocker (IMG-1) was resolved by commit `716817bc` on the branch prior to merge; the merged code carries **0 block / 0 major**. **No further action is required against what landed.** Residual items are all advisory (`minor`/`nit`), several already addressed, the rest tracked under issue #24.

**Why two verdicts:** the gate's mandated deliverable is the verdict on the head it reviewed (`c8123376`) → **REQUEST-CHANGES**. But between dispatch and this gate running, PR #21 was **already merged** (2026-10-08, by `mattsmcknight`) at a branch head one commit beyond the reviewed head, and that commit explicitly implements IMG-1's required change. Reporting only the `c8123376` verdict would be accurate but misleading about the live state; reporting only "merged/approved" would silently drop the finding. Both are stated. See **Post-review merge reconciliation** below. This is reported, not plugged.

---

## Severity counts (reviewed head `c8123376`)

| Severity | Count | Finding ids |
|----------|-------|-------------|
| `block`  | **0** | — |
| `major`  | **1** | IMG-1 |
| `minor`  | **5** | WF-1, WF-2, SEC-1, IMG-2, DOC-1 |
| `nit`    | **4** | SEC-2, IMG-3, IMG-4, DOC-2 |
| **total**| **10**| |

Aggregation and the verdict-rule application were computed deterministically (`calculations/aggregate.py`): `block=0, major=1 → REQUEST-CHANGES`; duplicate-location check → none; six-concern coverage → each covered exactly once.

### All findings (id · severity · concern · location · finding)

| id | sev | concern | location | finding (one line) | required_change |
|----|-----|---------|----------|--------------------|-----------------|
| **IMG-1** | **major** | 4 | `ci.yml` `image` job vs `Dockerfile:FROM rust:1.88` (`main@61f924a`) | Image build uses Rust **1.88**, decoupled from & older than CI's validated **1.97**; the `image` job ran **only on `push`→`main`**, so the Dockerfile build was never gated pre-merge → a toolchain-drift publish break would surface only post-merge on `main`. | Gate the Dockerfile build before merge (run `image` on PRs with `push:false`) and/or drive the Dockerfile Rust version from a single source shared with `RUST_TOOLCHAIN`. **← done in `716817bc`.** |
| WF-1 | minor | 2 | `ci.yml:33` + apply sites | Toolchain pinned to series `"1.97"`, not an exact patch → small patch-level float vs the "clean checkout reproduces" intent. | — (advisory; pin `1.97.0` or add `rust-toolchain.toml`) |
| WF-2 | minor | 2 | `ci.yml:30-33` | CI builds only on 1.97; declared MSRV 1.82 is unenforced and contradicted by the locked graph (pre-existing manifest/lock drift, not introduced here, not in #11's criteria). | — (advisory; reconcile manifest `rust-version` or add an MSRV job) |
| SEC-1 | minor | 3 | `ci.yml` all `uses:` steps | Every third-party action tag/branch-pinned, not SHA-pinned (tag-move supply-chain class); highest-impact slice is the write-scoped `docker/*` actions. Deferred to the owned hardening track **#24**. | — (advisory; SHA-pin under #24, `docker/*` first; add Dependabot) |
| IMG-2 | minor | 4 | `ci.yml` `image` Dockerfile-detect step + guards | With `./Dockerfile` now on `main`, the `[ -f Dockerfile ]` detect + `present=='true'` guards are dead code with a silent-skip-on-removal hazard (would report green while publishing nothing). | — (advisory; drop detection, build unconditionally) **← done in `716817bc`.** |
| DOC-1 | minor | 5 | PR #21 (21 non-CI files) | CI-titled PR also folds ~79 rustdoc link fixes + a README correction; mixed-concern reviewability cost — strongly mitigated (the doc fixes are the debt the new `-D warnings` doc gate would catch, so folding is correct scope). | — (advisory; name the folded work in the PR description) |
| SEC-2 | nit | 3 | `ci.yml` `image` build-push | Published image carries no provenance/attestation/SBOM. | — (optional; #24) |
| IMG-3 | nit | 4 | `ci.yml` `image` `if:` + `workflow_dispatch` | `image` job required `event_name=='push'` → a manual `workflow_dispatch` never (re)built/published the image. | — (awareness) |
| IMG-4 | nit | 4 | `ci.yml` `image` build-push step | Pushed image digest (`outputs.digest`) not surfaced for provenance/traceability. | — (optional) **← done in `716817bc`.** |
| DOC-2 | nit | 5 | `chirp-server/README.md:342-346` | Prose names `ServerError::Validation`; the body-extraction path produces the sibling `ServerError::InvalidBody` — cosmetic only (both map to 400 `VALIDATION_ERROR`, so the asserted user contract is correct). | — (optional; name `InvalidBody`) |

---

## Gate checks (all four run)

**1 — Contract / conformance: PASS.** All four `findings.md` exist and conform to `contracts/findings_schema.md`: every severity ∈ {`block`,`major`,`minor`,`nit`}; every finding carries a `location` and `rationale`; the one `major` (IMG-1) carries a `required_change`; every spoke states it reviewed head `c8123376`. No missing or non-conformant findings file; nothing fabricated.

**2 — Coverage / wiring: PASS.** Each of the six brief concerns is covered by exactly one spoke scope — 1+2 → `workflow_correctness`, 3 → `supply_chain_security`, 4 → `image_job`, 5 → `folded_minors`, 6 → this gate. No concern dropped; none double-owned.

**3 — Duplication: PASS (no merges needed).** No two spokes raised a finding about the same `location`. `workflow_correctness` explicitly *cross-referenced* action-pinning (owned by SEC-1) and image-job internals (owned by IMG-*) without raising competing findings, so counts are not inflated. WF-2 (manifest MSRV 1.82 unenforced) and IMG-1 (Dockerfile 1.88 vs CI 1.97) share the toolchain-pinning *theme* but are distinct findings at distinct locations/artifacts — both correctly retained.

**4 — Review / verdict: PASS.** Roll-ups aggregated (`calculations/aggregate.py`), verdict rule applied → `REQUEST-CHANGES` on the reviewed head, driven solely by IMG-1. Verdict is supported by the findings.

**Remediation:** none required from this gate — no spoke failed, no findings file was missing/non-conformant, no concern was uncovered. The only `major` was already remediated in the landed code (below), so no `engine_amend_plan` injection is warranted; a full re-review of the merged head would be disproportionate to a single, directly-inspected one-commit delta. Recorded as a reconciliation caveat per the brief.

---

## Acceptance-criteria mapping — issue #11 (reviewed head `c8123376`)

| # | Criterion | Verdict | Evidence |
|---|-----------|---------|----------|
| 1 | `ci.yml` runs on PR **and** push to `main` | **PASS** | `on: pull_request:[main]`, `push:[main]`, `workflow_dispatch` (WF concern-1) |
| 2 | `cargo fmt --check` | **PASS** | `cargo fmt --all --check` (ci.yml:50) |
| 3 | `cargo clippy -D warnings` | **PASS** | `cargo clippy --workspace --all-targets --locked -- -D warnings` (ci.yml:66) |
| 4 | `cargo test` | **PASS** | `cargo test --workspace --locked` (ci.yml:79) |
| 5 | build the WASM frontend | **PASS** | wasm job builds `chirp-frontend` → `wasm32-unknown-unknown`, runs `wasm-bindgen`, asserts `pkg/*`; `wasm-bindgen-cli 0.2.129` matches `Cargo.lock` (WF concern-2, verified) |
| 6 | on `main`, build + push chirp-server image to GHCR | **PASS (criterion met) — carried the IMG-1 `major`** | `image` job builds `./Dockerfile`, pushes `ghcr.io/nousix-llc/chirp-server` (long-SHA + `latest`) via `GITHUB_TOKEN`; build context/name/tag/auth all correct (IMG). Criterion is *met as written*; IMG-1 is a robustness defect (toolchain drift + no pre-merge gate), not an unmet criterion. |
| 7 | cache cargo/target | **PASS** | `Swatinem/rust-cache@v2` on the four compiling jobs; key = `Cargo.lock`+rustc; sound with `--locked` (WF) |
| 8 | required-check friendly | **PASS** | stable per-job `name:`s; `image` correctly excluded from PR checks (skipped on PR) (WF) |
| 9 | delivered as a PR into `main` | **PASS** | PR #21, base `main` |

**All nine acceptance criteria are satisfied as written at `c8123376`.** The `REQUEST-CHANGES` verdict is driven by the IMG-1 `major` (a robustness/drift defect on criterion 6's mechanics), not by any unmet criterion.

---

## Post-review merge reconciliation (live state — reported, not plugged)

Confirmed read-only via `gh` at gate time:

- PR #21 state: **MERGED** — `mergedAt` `2026-10-08T16:04:03Z`, `mergedBy` `mattsmcknight`, **merge commit `ada3aa97`**.
- PR branch head: **`716817bc`** — **one commit ahead** of the reviewed head `c8123376` (`compare c8123376...716817bc` → `ahead_by=1`, only `.github/workflows/ci.yml` changed, +38/−30).
- That commit: **`716817bc` "ci: gate the chirp-server image build on pull requests (IMG-1)"** — message cites this review's finding id.

Diff inspection of `716817bc` (verified, not assumed):

- **IMG-1 (major) → RESOLVED.** The `image` job's `if: event_name=='push' && ref=='main'` gate was removed; the job now runs on **both** PRs and `main` pushes, **build-only on PRs** (`push: ${{ env.PUBLISH }}`, `PUBLISH` true only on push→`main`). The Dockerfile build is now gated by the same required checks pre-merge, closing the "drift discovered only post-merge" window IMG-1 described. (IMG-1 offered this as one of its two acceptable required changes — "run the image build on PRs with `push:false`" — so the finding is cleared. The two Rust pins remain nominally decoupled, but the risk is now caught pre-merge; tracking a single-source-of-truth toolchain as an optional follow-up is reasonable but not required.)
- **IMG-2 (minor) → RESOLVED.** The `Detect Dockerfile` step and all `present=='true'` guards were removed; the build runs unconditionally, so a missing/broken Dockerfile now fails loudly instead of silently green-skipping.
- **IMG-4 (nit) → RESOLVED.** A "Summarize published image" step surfaces `steps.build.outputs.digest` for provenance/traceability.

**Net:** against the landed code, `block=0, major=0` → the review's blocker was satisfied before merge. The folded doc changes (DOC-1/DOC-2) were already in the reviewed head and are unchanged in the landed code (advisory). Remaining advisories: WF-1/WF-2 (toolchain series-pin + MSRV-vs-lock reconciliation), SEC-1/SEC-2 (SHA-pin third-party actions + image provenance — **issue #24**), IMG-3 (manual-dispatch publish path). None blocks, and nothing was landed in contradiction of this review.

---

## Overseer guidance

1. **Landing is already done** — PR #21 merged at `ada3aa97`. This verdict is therefore **retrospective**; treat it as confirmation that the one required change (IMG-1) was correctly made before merge, not as a gate on a pending merge.
2. **If a current-head sign-off is wanted**, the authoritative statement is: the merged code (`716817bc`→`ada3aa97`) is **APPROVE-equivalent** — 0 block, 0 major, IMG-1/IMG-2/IMG-4 resolved.
3. **Follow-ups to track (non-blocking):** issue **#24** for SHA-pinning third-party actions (prioritize the write-scoped `docker/*`) and image provenance/SBOM; WF-2's manifest-MSRV-vs-locked-deps reconciliation; optionally unify the Dockerfile/CI Rust toolchain to a single source of truth.
4. Per constraint: no GitHub review was posted (self-review is platform-blocked and non-authoritative); **this `SYNTHESIS.md` body is the authoritative verdict**.

---

### Head confirmation
Reviewed head **`c8123376`** confirmed as the head all four spokes examined. Live PR head is `716817bc` (merged via `ada3aa97`); the divergence is fully reconciled above.
