# COMPLETE — SUBTASK_wasm_toolchain (infra-bootstrap #10)

## What was done
Enabled and **proved** the `chirp-frontend` WebAssembly build toolchain, and delivered a reproducible
setup + build-proof script set, a runbook fragment, pinned versions, and an evidence record.

- Verified `wasm32-unknown-unknown` is installed; installed a version-matched `wasm-bindgen` CLI
  (**0.2.129**, exactly matching the `wasm-bindgen` crate resolved in `Cargo.lock`).
- Ran the real repo-documented build path against `crates/chirp-frontend` (source untouched):
  `cargo build --example chirp --target wasm32-unknown-unknown` → `wasm-bindgen --target web`,
  producing `pkg/chirp.js` (28,259 B, default `init` export) + `pkg/chirp_bg.wasm` (1,639,651 B,
  valid WASM MVP, magic `0061736d`).
- Proved the **staged scripts themselves** reproduce the artifact end-to-end (setup = idempotent
  no-op on re-run; build = green PASS).

## Outputs (owned paths per contracts/_MANIFEST.yaml)
- `staged/deploy/bootstrap/wasm/setup-wasm-toolchain.sh`
- `staged/deploy/bootstrap/wasm/build-chirp-wasm.sh`
- `staged/deploy/bootstrap/wasm/README.md`  (wasm runbook fragment)
- `staged/deploy/bootstrap/wasm/versions.txt`
- `RESULT.md`  (evidence record; owns-criteria: [wasm]; verdict PASS)

## Criterion
- **wasm: PASS** — target present, version-matched CLI installed, real build produced a runnable
  `pkg/` bundle; versions (rustc, cargo, wasm-bindgen, wasm32 target) recorded.

## Contract identities fed to the synthesis gate
- I1 coverage: owns `wasm`, verdict PASS. · I2 no-secrets: confirmed true, scan clean. ·
  I3 reproducible: scripts carry prereq/re-run headers, runbook states run order + verification. ·
  I4 versions: rustc/cargo/wasm-bindgen/target recorded. · I5 honest: PASS carries command+observed
  evidence. · I6 infra-only: no Dockerfile / app Deployment / ArgoCD Application produced.

## Boundaries honored
`chirp-frontend` source unmodified (git status clean); no git performed (staging only — the synthesis
gate owns git/PR); no cluster or ArgoCD work; composed against `contracts/` literally (no deviation,
no amendment needed).

## Notes for the synthesis gate
No infra `checkout/` existed yet, so the toolchain was proven against a faithful existing
`nswe-demo` working tree at commit `b5f7e62` (carries the same crate + `Cargo.lock` wasm-bindgen
0.2.129 pin). Staged scripts are repo-root-relative and will run against whatever checkout the gate
commits them into. See `RESULT.md §Environment / honesty notes`.
