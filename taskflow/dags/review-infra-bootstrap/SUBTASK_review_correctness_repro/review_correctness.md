# Review — correctness / reproducibility / idiom lens (PR #20, infra-bootstrap)

**Lens:** `correctness` · **Spoke:** `SUBTASK_review_correctness_repro`
**Subject:** PR #20 (`Nousix-LLC/nswe-demo`, `work/infra-bootstrap` @ `016bd44`, Closes #10), the six
`deploy/bootstrap/` scripts + `versions.txt` (+ READMEs read for context).
**Owned concerns:** (1) script correctness / genuine verification, (2) reproducibility & idempotency,
(3) code quality & shell/k8s/GitOps idiom.
**Method:** read all six scripts, the four READMEs, `versions.txt`, the PR diff/body, and the code DAG's
folded `SYNTHESIS.md` (INPUT, not authority); validated the wasm script's claims against the live crate;
empirically probed two suspected defects (`k3d cluster list -o json` serialization on the pinned k3d
v5.9.0; sudo env-forwarding semantics). Review-only — no repo/branch/checkout modification performed.

---

## 1. Lens summary

Through the "does it work, re-runnably, idiomatically" lens this is **strong, honest, idiomatic
infra shell** with no blocking defect. All six scripts carry `set -euo pipefail`, pin their versions,
declare prerequisites + re-run behaviour in a header, and — critically — their verification is
**genuine**, not trivially-true green: every `verify-*`/`build-*` performs a real cluster/toolchain
observation and exits non-zero when the thing it checks is actually broken (confirmed by reading each
assertion, and by validating the wasm build path against the real crate: the `chirp` example exists,
`index.html` imports `./pkg/chirp.js`, and `Cargo.lock` pins `wasm-bindgen 0.2.129`, exactly as the
scripts assume/derive). The GitOps install is the standout — server-side-apply-with-force-conflicts is
the correct, well-justified idiom for ArgoCD's oversized CRDs, and its readiness proof is thorough. The
one finding that rises above cosmetic is a **major, latent reproducibility defect on the NATIVE install
path** (version pin silently dropped when the installer is invoked through `sudo`), which matters
because native is the production target of #10 and the path was not exercised on the k3d build host.
Everything else is minor/nit: verification proves *readiness* genuinely but does not *assert* the
pinned version for cluster/ArgoCD (it prints it), and a couple of idiom/robustness rough edges.

**Genuine-vs-trivially-true-green verdict per subsystem:**
- **Cluster** — `verify-cluster.sh` is **genuine** (real `kubectl wait --for=condition=Ready nodes
  --all` + CoreDNS Running check; fails closed). Install is genuine; native-mode pin defect is CORR-1.
- **GitOps** — `verify-argocd.sh` is **genuine** (per-workload `kubectl rollout status` + explicit
  non-Running pod scan + CRD-registration check; fails closed). Install genuine and idiomatic.
- **wasm** — `build-chirp-wasm.sh` is **genuine** (real `cargo build --target wasm32-unknown-unknown`
  + `wasm-bindgen` run, then asserts `pkg/chirp.js` + `pkg/chirp_bg.wasm` exist and the `.wasm` carries
  the `0061736d` magic header). Not a fabricated green.

---

## 2. Concern-by-concern assessment

### Concern 1 — Script correctness / genuine verification

**Disposition: clean on genuineness; one major latent defect on native-mode install correctness.**

Every verification step is a real observation that gates:
- `verify-cluster.sh:40` `kubectl wait --for=condition=Ready nodes --all --timeout` then `:55–60`
  CoreDNS Running (label `k8s-app=kube-dns` with a name-match fallback) → non-zero on failure.
- `verify-argocd.sh:41–50` per-Deployment/StatefulSet `kubectl rollout status … || fail`, `:56–58` an
  explicit `--field-selector=status.phase!=Running` scan, `:36–38` CRD registration — all fail-closed.
- `build-chirp-wasm.sh:72–88` a real build + bind + magic-header assertion; verified against the live
  crate that the example (`crates/chirp-frontend/examples/chirp.rs`) and import
  (`index.html:35 import init from "./pkg/chirp.js"`) exist, so the build path is real and correct.

The one genuine correctness defect is **CORR-1** (native-mode version pin dropped under `sudo`), a
latent reproducibility bug on the unexercised NATIVE path. The verify scripts would not catch it because
they print — but do not assert — the pinned version (**CORR-2**).

### Concern 2 — Reproducibility & idempotency

**Disposition: strong, with one major (CORR-1) and two minor (CORR-2, CORR-3) caveats.**

- **Shell discipline:** all six scripts begin `set -euo pipefail` (verified in each). Variables are
  quoted throughout; failure propagates (no `|| true` swallowing on load-bearing steps — the few
  `|| true` uses are deliberately on diagnostic/`echo` paths, e.g. `verify-cluster.sh:42,49`).
  `curl -sfL … | sh` is `-f`-guarded and under `set -o pipefail`, so a failed manifest/installer
  download propagates rather than piping a truncated script to the shell — a correctness strength many
  piped installers get wrong. (`-S` omission is a nit, CORR-5.)
- **Pinning:** k3s `v1.35.5+k3s1` + k3d image `rancher/k3s:v1.35.5-k3s1`; ArgoCD `v3.5.4`; wasm-bindgen
  derived from `Cargo.lock` (robust against crate bumps) and asserted CLI==crate. Versions recorded in
  `versions.txt`. The native-mode path, however, silently loses its pin under sudo (**CORR-1**).
- **Idempotency idioms (all correct):** ArgoCD namespace via `kubectl create … --dry-run=client -o yaml
  | kubectl apply -f -` (`install-argocd.sh:59`); manifest via `apply --server-side --force-conflicts`
  (converge, not duplicate); k3d create-if-missing with `K3S_FORCE_RECREATE` escape hatch; wasm
  `rustup target add` no-op + CLI install skipped when version already matches. The k3d existence probe
  works on the pinned k3d but is brittle idiom (**CORR-3**).

### Concern 3 — Code quality & shell/k8s/GitOps idiom

**Disposition: clean / idiomatic and maintainable; a few nits only.**

Readable at 2am: consistent `log()` helpers, clear section banners, headers stating purpose/prereqs/
re-run/exit-codes, helpful failure diagnostics that point at the remediating runbook. k8s/GitOps idiom
is correct and current (server-side apply for large CRDs with an explicit WHY comment; ClusterIP +
port-forward default; `rollout status` as the readiness primitive). No needless complexity; no clever
one-liners that obscure intent. The rough edges are all nit-level: a JSON-via-`grep` existence check
with a cleaner alternative (CORR-3, also a reproducibility concern), a stdout-vs-stderr logging
inconsistency across the suite (CORR-7), a dead/wrong-token guard string in the wasm bundle check
(CORR-4), and the `curl` `-S` nit (CORR-5).

---

## 3. Findings

- [CORR-1] severity=major concern=reproducibility_idempotency lens=correctness
  location=`cluster/install-k3s.sh:61–65` (`install_native`)
  acceptance_criteria_touched=[AC1_cluster, AC4_runbook]
  statement: In NATIVE mode on a non-root host, the pinned k3s version is silently dropped, so the
  installer resolves to `latest`/stable instead of `v1.35.5+k3s1`. The command expands to
  `INSTALL_K3S_VERSION="$K3S_VERSION" sudo sh -s - server …` — the `VAR=val` prefix sets the variable in
  **sudo's own** environment, and default sudoers `env_reset` does not forward it to the `sh` that sudo
  then runs. The cluster still comes up, but at an unpinned version — a silent reproducibility break on
  the production (native) path that #10 actually targets. (When run as real root, `sh_pfx=""` and the
  var is passed directly, so the bug is specific to the non-root + passwordless-sudo native sub-path.)
  evidence: `install-k3s.sh:61` `local sh_pfx=""; [ "$(id -u)" = "0" ] || sh_pfx="sudo"` then `:63–65`
  `curl -sfL https://get.k3s.io | INSTALL_K3S_VERSION="$K3S_VERSION" $sh_pfx sh -s - server …`. sudoers(5)
  `env_reset` is the default and strips non-`env_keep` variables; confirmed by reasoning (no passwordless
  sudo on the review host to demo live). The native path was not exercised on the k3d build host, so the
  defect is latent — the code DAG gate only ran k3d. `verify-cluster.sh` would not catch it (CORR-2).
  remediation: pass the version **inside** the privileged shell rather than as a prefix to `sudo`, e.g.
  `curl -sfL https://get.k3s.io | $sh_pfx env INSTALL_K3S_VERSION="$K3S_VERSION" sh -s - server
  --write-kubeconfig-mode 0644` (use `env` so it also works when `sh_pfx` is empty), or
  `sudo --preserve-env=INSTALL_K3S_VERSION`. Leave the land-blocking-vs-follow-up call to the gate; it is
  a real defect on a supported path but on code the PR transparently documents as unexercised here.

- [CORR-2] severity=minor concern=script_correctness lens=correctness
  location=`cluster/verify-cluster.sh:49–50`, `gitops/verify-argocd.sh:60–62`
  acceptance_criteria_touched=[AC1_cluster, AC2_gitops, AC4_runbook]
  statement: Verification proves *readiness* genuinely but does not *assert* the pinned version. The
  cluster verifier prints the node `osImage` and the ArgoCD verifier prints the installed server image,
  but neither compares it to the pin (`v1.35.5+k3s1` / `v3.5.4`). A version-drifted install (e.g. the
  CORR-1 native-mode case, or an operator overriding `ARGOCD_VERSION`) would still report PASS.
  evidence: `verify-cluster.sh:49` `K3S_VER="$(kc get nodes -o jsonpath=…osImage…)"` then `:50`
  `echo "k3s server version (node osImage): ${K3S_VER:-unknown}"` — printed, never asserted;
  `verify-argocd.sh:60–62` logs `INSTALLED_IMAGE` with no equality check against `v3.5.4`.
  remediation: optional for a minor — if version-pin conformance is to be gated, add an assertion that
  the observed version/image contains the pinned tag and `fail`/exit non-zero otherwise. #10's AC says
  versions "recorded," which is satisfied; this raises the bar from recorded to proven.

- [CORR-3] severity=minor concern=code_quality_shell_k8s_gitops_idiom lens=correctness
  location=`cluster/install-k3s.sh:72`
  acceptance_criteria_touched=[AC1_cluster, AC4_runbook]
  statement: The k3d cluster-exists idempotency probe parses JSON with `grep` for the literal
  `"name":"<cluster>"`. It works on the pinned k3d (v5.9.0 emits compact, space-free JSON — verified),
  but it is brittle idiom: it silently depends on k3d's non-indented serialization, an undocumented
  implementation detail. If a future k3d pretty-prints (`"name": "nswe"`), the probe false-negatives,
  `k3d cluster create` then errors on the existing cluster, and `set -e` turns a re-run into a hard
  failure — i.e. idempotency would break on a k3d bump.
  evidence: `install-k3s.sh:72` `if k3d cluster list -o json 2>/dev/null | grep -q
  "\"name\":\"${CLUSTER_NAME}\""; then`. Empirically, `k3d version v5.9.0` `cluster list -o json` emits
  `[{"name":"nswe",…}]` (compact) and the grep matches exactly once (node names are `k3d-nswe-*`, so no
  false-positive) — so it is correct today, brittle tomorrow.
  remediation: use k3d's own existence query instead of grepping JSON, e.g.
  `if k3d cluster get "$CLUSTER_NAME" >/dev/null 2>&1; then` (exits non-zero when absent), which is
  serialization-independent and reads clearly.

- [CORR-4] severity=nit concern=code_quality_shell_k8s_gitops_idiom lens=correctness
  location=`wasm/build-chirp-wasm.sh:89`
  acceptance_criteria_touched=[AC3_wasm]
  statement: The post-build bundle sanity note greps for the wrong token. wasm-bindgen `--target web`
  emits `export default …` in `chirp.js`, not the string `as default`, so this guard will emit its
  "no default export" note even on a correct bundle. Non-fatal (it only `log`s; `||` guards it and it
  never exits), so it cannot cause a false failure — purely a misleading diagnostic.
  evidence: `build-chirp-wasm.sh:89` `grep -q "as default" "$JS" || log "note: $JS has no 'as default'
  export line …"`; the crate's `index.html:35` uses a **default import** `import init from
  "./pkg/chirp.js"`, which wasm-bindgen satisfies with `export default`.
  remediation: optional for a nit — grep for `export default` (or drop the cosmetic check), e.g.
  `grep -q "export default" "$JS" || log "note: …"`.

- [CORR-5] severity=nit concern=code_quality_shell_k8s_gitops_idiom lens=correctness
  location=`cluster/install-k3s.sh:63`
  acceptance_criteria_touched=[AC1_cluster]
  statement: The piped installer uses `curl -sfL`; `-s` without `-S` suppresses curl's own error text,
  so a download failure is silent (the non-zero exit still propagates correctly under `-f` + pipefail,
  so correctness is preserved — only the diagnostic is lost).
  evidence: `install-k3s.sh:63` `curl -sfL https://get.k3s.io | …`.
  remediation: optional — `curl -fsSL` is the conventional flag set (keep errors visible while hiding
  progress). Same applies cosmetically to any other `-sfL` usage.

- [CORR-6] severity=nit concern=script_correctness lens=correctness
  location=`cluster/verify-cluster.sh:40`
  acceptance_criteria_touched=[AC1_cluster]
  statement: `kubectl wait --for=condition=Ready nodes --all` can be vacuously satisfied if zero nodes
  are registered (an empty resource set), so node-readiness alone is not a hard floor. In practice the
  risk is fully closed by the downstream CoreDNS-Running check (`:55–60`), which cannot pass with no
  running nodes — so the net verification remains genuine. Recorded for completeness.
  evidence: `verify-cluster.sh:40` the `--all` wait; `:55–60` the CoreDNS gate that backstops it.
  remediation: optional — if a strict floor is wanted, assert `kc get nodes` returns ≥1 node before the
  wait.

- [CORR-7] severity=nit concern=code_quality_shell_k8s_gitops_idiom lens=correctness
  location=`gitops/install-argocd.sh:43`, `gitops/verify-argocd.sh:27` vs `cluster/install-k3s.sh:38`,
  `wasm/setup-wasm-toolchain.sh:30`
  acceptance_criteria_touched=[]
  statement: Logging idiom is inconsistent across the suite: the cluster/wasm scripts log via
  `printf … >&2` (stderr, keeping stdout clean for captured output), while the gitops scripts log via
  `echo` to stdout. Harmless, but a uniform convention reads better and keeps machine-parseable stdout
  clean.
  evidence: `install-k3s.sh:38` `log() { printf '[install-k3s] %s\n' "$*" >&2; }` vs
  `install-argocd.sh:43` `log() { echo "[install-argocd] $*"; }`.
  remediation: optional for a nit — standardize log helpers on stderr across all six scripts.

### Clean / verified (evidenced, not silence)

- **Shell discipline:** `set -euo pipefail` present in all six scripts (install-k3s:29, verify-cluster:21,
  install-argocd:37, verify-argocd:18, setup-wasm:28, build-chirp-wasm:27).
- **Genuine verification:** all three `verify`/`build` subsystems perform real observations and fail
  closed (see §1 verdict and Concern 1 evidence) — no fabricated or trivially-true green found.
- **GitOps idiom:** `kubectl apply --server-side --force-conflicts` with an explicit, accurate WHY
  (the `applicationsets.argoproj.io` CRD exceeds the 262144-byte client-side annotation limit) —
  correct, current, upstream-recommended idiom (`install-argocd.sh:23–27,62`).
- **wasm pin integrity:** version derived from `Cargo.lock` and asserted CLI==crate==`0.2.129`, validated
  against the live lockfile and crate (`setup-wasm-toolchain.sh:65–92`, `build-chirp-wasm.sh:60–66`).

---

## 4. Acceptance-criteria bearing (for the gate's R2 assembly)

| AC | Findings from this lens that bear on it |
|----|------------------------------------------|
| AC1_cluster | CORR-1 (major), CORR-2 (minor), CORR-3 (minor), CORR-5 (nit), CORR-6 (nit) |
| AC2_gitops | CORR-2 (minor) |
| AC3_wasm | CORR-4 (nit); otherwise clean/genuine |
| AC4_runbook (idempotency/pinning clause) | CORR-1 (major), CORR-2 (minor), CORR-3 (minor) |

**This lens raises no `block` finding.** One `major` (CORR-1) — a real, latent reproducibility defect on
the native install path; the gate owns the land-blocking-vs-carry-as-follow-up decision per the
contract's `verdict_rule`. All other findings are minor/nit. The genuine-verification question central
to this lens is answered **affirmatively for all three subsystems**.

### Notes for the gate (out of this lens's ownership — flagged, not owned)

- The acceptability of the **k3d-vs-native substitution** is owned by `SUBTASK_review_honesty_scope_ops`;
  I do not adjudicate it. I only observe (within correctness scope) that the native path carries a latent
  pin defect (CORR-1) — relevant input to that adjudication, not a verdict on the substitution itself.
- No security/secrets judgment is made here (owned by `SUBTASK_review_security_rbac`); I note only, as a
  correctness strength, that `curl -f` + `pipefail` prevents a truncated piped installer from executing.
- **R7 (review-only):** this spoke read the scripts and probed `k3d`/`sudo` behaviour on the review host
  only; it performed no edit/stage/commit/push to the repo, branch, or checkout. The sole write is this
  findings document.
