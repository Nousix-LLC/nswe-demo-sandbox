# Task: Build-toolchain enablement (wasm)

## Task Specification
**Slug**: SUBTASK_wasm_toolchain
**Task Kind**: standard
**Status**: Pending

### Objective
Enable and **prove** the wasm build toolchain — `wasm32-unknown-unknown` target + **wasm-bindgen** —
by producing a real WebAssembly build of the existing `crates/chirp-frontend`, with exact toolchain
versions recorded, delivered as a reproducible setup/build script set plus an honest evidence record.

### Context
Part of infra-bootstrap (#10) — see `../_GLOBAL.md` and `../contracts/`. This is the build-toolchain
concern only; it is **independent** of the cluster and ArgoCD spokes (no dependency). Do NOT modify
`chirp-frontend` source — it is the proof target, used as-is.

**Dependencies**: none. **Dependents**: `SUBTASK_synthesis_gate`.

## Inputs
- `../_GLOBAL.md` — objective, environment facts (crucially: the repo uses **wasm-bindgen, not
  trunk**; the frontend `index.html` imports `./pkg/chirp.js`; the README describes building the
  example to `wasm32-unknown-unknown` then running `wasm-bindgen` to emit `pkg/chirp.js` +
  `pkg/chirp_bg.wasm`).
- `../contracts/_MANIFEST.yaml` + `../contracts/result_record.schema.md` — your owned paths and the
  `RESULT.md` schema (read-only).
- The `crates/chirp-frontend` crate in a repo checkout of `Nousix-LLC/nswe-demo` (its `Cargo.toml`,
  `index.html`, `examples/`, `README.md`) — the concrete build target.

## Scope / what to deliver
- A reproducible **wasm toolchain setup script** (`rustup target add wasm32-unknown-unknown`, ensure
  a `wasm-bindgen` CLI compatible with the crate's `wasm-bindgen` dependency version) and a **build
  proof script** that performs the real `chirp-frontend` wasm build along the path the repo already
  uses (build example for `wasm32-unknown-unknown`, then wasm-bindgen → `pkg/`), plus a short **wasm
  runbook fragment** (prereqs, run order, verification) and **pinned/recorded versions**.
- Stage repo-destined files under `staged/deploy/bootstrap/wasm/`. Write `RESULT.md` per schema. No
  git; the synthesis gate owns it.
- Own and record the **wasm** criterion in `RESULT.md` (`owns-criteria: [wasm]`); `Versions` MUST name
  `rustc`, `cargo`, `wasm-bindgen`, and the `wasm32-unknown-unknown` target.

### Honest-outcome rule
If the build cannot complete here (no network to add the target/install wasm-bindgen, toolchain
mismatch, etc.): deliver the reproducible scripts and mark the wasm criterion **BLOCKED** with the
exact failing command, observed error, env fact, and a concrete remediation. Never claim a build that
did not produce a real `.wasm` artifact.

## Success Criteria
- [ ] Staged setup + build scripts exist with prereqs/re-run headers.
- [ ] `RESULT.md`: `wasm` criterion PASS (evidence: the build command + observed output showing a
      produced `pkg/*_bg.wasm` / `pkg/*.js`) OR BLOCKED (blocker + remediation); versions recorded
      (rustc, cargo, wasm-bindgen, target); `confirmed-no-secrets: true`.
- [ ] `chirp-frontend` source unmodified; no cluster/ArgoCD work here.

## Suggested Methodology Files
Parent's Domain-Mapping reading (**Writing Rust / Frontend build tooling**; primary **Rust**,
supporting **Frontend**, **Operations**, **Core**). Load on-demand:
- `rust` — primary. `rust/Rust_Cargo_Ecosystem_Methodology.md` (targets, toolchain pinning, cargo
  build for a wasm target). Rationale: the `wasm32-unknown-unknown` build + version pinning.
- `frontend` — `frontend/Frontend_Build_Tooling_Methodology.md`. Rationale: the wasm-bindgen → `pkg/`
  SPA build path the crate uses.
- `operations` — `operations/DevTools_Build_Systems_Methodology.md`,
  `operations/BestPractices_Documentation_Methodology.md`. Rationale: reproducible build script + runbook + pinned versions.
- `core` — `core/BestPractices_Coding_Standards_Methodology.md` for the script hygiene.

*Parent's flags, not exclusive — you are the final judge of what you load.*

## Inherited Constraints
All of `../_GLOBAL.md §Subtree-Wide Constraints` bind you (infra-only; reproducible; honest reporting;
repo scope; stage-only, no git). Compose against `../contracts/` literally; request an additive
amendment rather than deviating.

## Out-of-Scope Methodologies
`kubernetes/*`, `gitops/*`, `kubernetes-security/*` (other spokes), `synthesis/*` (the gate),
containerization/* (#12). Do not touch cluster or ArgoCD concerns.
