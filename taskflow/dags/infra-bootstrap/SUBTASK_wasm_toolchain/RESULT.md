# RESULT — wasm build toolchain (issue #10)

## Spoke
- subtask: SUBTASK_wasm_toolchain
- owns-criteria: [wasm]

## Versions
- rustc: 1.97.1 (8bab26f4f 2026-07-14)
- cargo: 1.97.1 (c980f4866 2026-06-30)
- rustup: 1.29.0 (28d1352db 2026-03-05)
- wasm-bindgen: 0.2.129            # CLI; installed version-matched to the crate
- wasm-bindgen (crate, Cargo.lock): 0.2.129
- wasm32-unknown-unknown: installed (rustup target)
- workspace MSRV (rust-version): 1.82
- (informational, from Cargo.lock) wasm-bindgen-futures: 0.4.79; js-sys: 0.3.106; web-sys: 0.3.106

## Criteria

### wasm  — verdict: PASS
- what: `wasm32-unknown-unknown` target + a `wasm-bindgen` CLI present, and a real
  `crates/chirp-frontend` WebAssembly build succeeds producing a runnable `pkg/` bundle, with
  exact toolchain versions recorded.
- evidence:
  - command: `rustup target list --installed | grep -x wasm32-unknown-unknown`
    observed: |
      wasm32-unknown-unknown
      (target already present on the proving host.)
  - command: `cargo install wasm-bindgen-cli --version 0.2.129 --locked`
    observed: |
      Compiling wasm-bindgen-cli v0.2.129
       Finished `release` profile [optimized] target(s) in 1m 31s
        Installing /home/user/.cargo/bin/wasm-bindgen
       Installed package `wasm-bindgen-cli v0.2.129` (executables `wasm-bindgen`, ...)
      $ wasm-bindgen --version  ->  wasm-bindgen 0.2.129
      (CLI version 0.2.129 exactly matches the resolved wasm-bindgen crate — required for binding.)
  - command: `cargo build -p chirp-frontend --example chirp --target wasm32-unknown-unknown`
    observed: |
      Compiling chirp-types / ferric-http / chirp-frontend ...
       Finished `dev` profile [unoptimized + debuginfo] target(s)
      produced: target/wasm32-unknown-unknown/debug/examples/chirp.wasm (14,376,389 bytes)
  - command: `wasm-bindgen --target web --no-typescript --out-dir <pkg> target/wasm32-unknown-unknown/debug/examples/chirp.wasm`
    observed: |
      exit 0; produced:
        pkg/chirp.js        (28,259 bytes) — ES module; `export { initSync, __wbg_init as default }`,
                             the default `init` that crates/chirp-frontend/index.html imports.
        pkg/chirp_bg.wasm   (1,639,651 bytes) — `file` reports: WebAssembly (wasm) binary module
                             version 0x1 (MVP); magic header 0061736d verified.
  - command: `OUT_DIR=/tmp/wasm_proof_pkg2 bash deploy/bootstrap/wasm/build-chirp-wasm.sh` (staged script, end-to-end)
    observed: |
      [build-wasm] toolchain: rustc 1.97.1 | cargo 1.97.1 | wasm-bindgen 0.2.129 (matches crate)
      [build-wasm] PASS: produced chirp.js (28259 bytes) + chirp_bg.wasm (1639651 bytes); wasm magic OK.
      (The staged scripts — not just hand-run commands — reproduce the artifact; setup-… ran idempotent no-op.)

## Staged files
- deploy/bootstrap/wasm/setup-wasm-toolchain.sh: adds the wasm32 target and installs a
  `wasm-bindgen` CLI whose version is derived from Cargo.lock to match the crate exactly.
  Idempotent: no-op when target present and CLI version already matches. Has a prereq/re-run header.
- deploy/bootstrap/wasm/build-chirp-wasm.sh: builds the `chirp` example for wasm32 then runs
  wasm-bindgen to emit `pkg/`, and verifies `pkg/chirp.js` + `pkg/chirp_bg.wasm` (asserts wasm magic).
  Re-runnable; `OUT_DIR` overridable; does not modify chirp-frontend source. Prereq/re-run header present.
- deploy/bootstrap/wasm/README.md: wasm runbook fragment — prereqs, run order, verification, blocker
  remediation. (To be folded into the unified deploy/bootstrap/README.md by the synthesis gate.)
- deploy/bootstrap/wasm/versions.txt: the pinned/recorded toolchain versions above.

## Secrets check
- confirmed-no-secrets: true
- notes: Staged files are build scripts + docs only; no kubeconfig, token, password, or key is
  present (secret-pattern scan over the staged tree returned zero matches). The toolchain build
  touches no credentials.

## Environment / honesty notes
- `crates/chirp-frontend` source was NOT modified; the build produces only cache (`target/`) and
  generated binding (`pkg/`) artifacts. For the proof-dir runs, `pkg/` was emitted to a scratch
  `OUT_DIR` so nothing was written into the crate directory.
- No infra-bootstrap `checkout/` worktree exists yet (the synthesis gate establishes it off
  `origin/main`). The toolchain was therefore proven against a faithful existing working-tree
  checkout of `Nousix-LLC/nswe-demo` at commit `b5f7e62` (`chirp-frontend: implement the SPA feature
  modules (#9)`), which carries the same `crates/chirp-frontend` crate and the workspace `Cargo.lock`
  pinning `wasm-bindgen = 0.2.129`. The toolchain capability (target + version-matched CLI + a real
  wasm build to a runnable pkg/) is what the `wasm` criterion asserts and is independent of which
  commit the proof target sits at; the staged scripts are repo-root-relative and run against whatever
  checkout the synthesis gate commits them into.
- No cluster or ArgoCD work was performed here (out of this spoke's scope).
