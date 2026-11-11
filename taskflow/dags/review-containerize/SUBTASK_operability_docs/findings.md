# findings.md — SUBTASK_operability_docs

## Header

- **Spoke**: `SUBTASK_operability_docs`
- **Concerns owned**: Concern 4 (operability — HEALTHCHECK, one-knob port, config, logging, out-of-box serve); Concern 6 **documentation slice** (clarity AND docs-match-real-behavior of `deploy/README.md` + the `README.md` "Running chirp in a container" section).
- **Diff reviewed**: PR #22 head commit `bc0c3c0d6380c9edd1b9433addc7fdcbffb55751` of `Nousix-LLC/nswe-demo` (`gh pr diff 22`).
- **Basis**: diff read-only; build/run facts relied on from `taskflow/dags/containerize/SYNTHESIS.md` (machine gate) — not re-run.

---

## Per-concern dispositions

### Concern 4 — Operability: `PASS-WITH-NOTES`

The operability surface is correct and well-constructed; the machine gate corroborates every runtime
claim.

- **HEALTHCHECK genuinely exercises `/healthz`.** `Dockerfile:111-112` declares
  `HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 CMD ["/usr/local/bin/healthcheck"]`
  in **exec form** — the only correct form for a distroless runtime with no shell (a shell-form `CMD`
  would fail with "no such file"). The probe (`deploy/docker/healthcheck.rs:31-50`) issues one real
  `GET /healthz` over loopback and maps HTTP 200→exit 0, else→exit 1, which is exactly the signal
  Docker's `HEALTHCHECK` consumes. Machine gate: `HEALTHCHECK` **healthy**, failing-streak 0, probe
  exit 0.
- **One-knob port derivation is real and correctly implemented.** The server reads `CHIRP_BIND_ADDR`;
  the probe derives its port from the *same* variable (`healthcheck.rs:probe_port()` — segment after
  the last `:`, all-digit validated, default `8080`) and connects to `127.0.0.1:<that port>`. There is
  no second port knob to drift. The documented port-change recipe (`deploy/README.md §Configuration`:
  `-p 9000:9000 -e CHIRP_BIND_ADDR=0.0.0.0:9000`) therefore moves both server and probe together — the
  claim "set **one** knob … the healthcheck derives its port from the same variable" is accurate.
- **Config is externalized and documented.** `Dockerfile:95-97` sets `CHIRP_BIND_ADDR=0.0.0.0:8080`,
  `CHIRP_STATIC_DIR=/srv/chirp`, `RUST_LOG=info,chirp_server=info,tower_http=info`; all three are
  documented with defaults + purpose in `deploy/README.md §Configuration`. Names/defaults match the
  machine gate's config vars of record exactly.
- **Logging to stdout/stderr.** `RUST_LOG` env-filter drives `tracing` to stdout/stderr for
  `docker logs` (`Dockerfile:93-94` comment; machine gate captured the SIGTERM drain log line) —
  12-factor-compliant.
- **Out-of-box serve.** exec-form `ENTRYPOINT ["/usr/local/bin/chirp-server"]` (`Dockerfile:113`) makes
  the server PID 1 and receives SIGTERM directly. Machine gate: SPA `/`, client-route fallback,
  `/pkg/*.wasm` (`application/wasm`), `POST /api/users`→201 all served on the in-memory default, no
  external DB.

Only a single advisory nit (OPS-3), below. No `block`/`major`.

### Concern 6 (documentation slice) — docs clarity & docs-match-behavior: `PASS-WITH-NOTES`

The two documents are clear, well-structured, and — critically — **factually match the diff's real
behavior** on every operator-facing command, env var, port, and default I cross-checked:

- `README.md` quick section: `docker build -t chirp:local .`, `docker run --rm -p 8080:8080 chirp:local`,
  `curl … /healthz -> {"status":"ok",...}` — all match `Dockerfile` and the machine gate; relative links
  to `Dockerfile` / `deploy/README.md` resolve.
- `deploy/README.md`: build-stage table (both base images, digest-pinned; `wasm-bindgen-cli@0.2.129`
  matching `ARG WASM_BINDGEN_VERSION=0.2.129`), the `/healthz` JSON body
  (`{"status":"ok","service":"chirp-server","version":"0.1.0"}` — **byte-identical** to the machine gate),
  the HEALTHCHECK parameters ("every 30s, 5s timeout, 5s start-period, 3 retries" — exact match to
  `Dockerfile:111`), the config table (all three vars + defaults match `Dockerfile:95-97`), the
  one-knob port recipe, and `docker inspect … .State.Health.Status`.
- No documented flag/env/port is unsupported by the image, and no honored var is left undocumented —
  i.e. the brief's named failure mode ("a doc that claims a flag or env var the image does not honor")
  does **not** occur here.

Two concrete-but-minor doc inaccuracies remain (OPS-1, OPS-2). Neither misstates operator-facing
runtime behavior, so per the severity discipline (I4) neither is a `block`/`major`.

---

## Findings

| Finding ID | Concern | Severity | Location | Evidence | Remediation |
|---|---|---|---|---|---|
| OPS-1 | 6 (docs) | `minor` | `deploy/README.md §Healthcheck` and `deploy/docker/healthcheck.rs:3` (module doc) | Both say the probe is "compiled with `rustc -O`", but the Dockerfile actually builds it with `rustc -C opt-level=z -C strip=symbols deploy/docker/healthcheck.rs` (`Dockerfile:67`). `-O` is `opt-level=2`; the real flags optimize for **size** and strip symbols. A concrete doc↔build mismatch (internal build detail, not an operator-facing command). | Change "compiled with `rustc -O`" to "compiled with `rustc -C opt-level=z -C strip=symbols`" (or neutrally "size-optimized with `rustc`") in both the `deploy/README.md §Healthcheck` text and the `healthcheck.rs` module comment so the prose tracks `Dockerfile:67`. |
| OPS-2 | 6 (docs) | `minor` | `deploy/README.md §Image characteristics` (final line) | The doc defers the image size entirely: "The measured image size and build/run evidence are recorded in the work-item's `SYNTHESIS.md`." That `SYNTHESIS.md` is a taskflow artifact, not shipped in the repo, so a reader of the repo docs cannot see the documented size. The work-item criterion ("size … documented") is satisfied only by an out-of-repo file. | State the measured figure inline, e.g. add to §Image characteristics: "**Size:** ≈42 MB (`linux/amd64`)." Keep the `SYNTHESIS.md` reference as supporting detail, but put the number where a repo reader will find it. |
| OPS-3 | 4 | `nit` | `deploy/docker/healthcheck.rs:36-38` (`probe_port` / socket) | The probe always connects to `127.0.0.1:<port>` regardless of the **host** portion of `CHIRP_BIND_ADDR`. With the image default `0.0.0.0:8080` (and any bind that includes loopback) this is correct and is the standard loopback-healthcheck idiom; it would only fail if the server were bound to a specific non-loopback interface that excludes `127.0.0.1`. Noted as a robustness observation, **not** a defect — the shipped default behaves correctly (machine gate: healthy). | Optional: one sentence in `deploy/README.md §Healthcheck` noting the probe assumes the server is reachable on loopback (true for the `0.0.0.0` default). No code change warranted for the shipped configuration. |

---

## Cross-references (not re-filed — owned by siblings per contract I2)

- The **Rust idiom/correctness** of `healthcheck.rs` and the `main.rs` SIGTERM change → `SUBTASK_rustcode_sigterm`. (OPS-1 is filed as a *documentation* finding, not a Rust-idiom finding; OPS-3 is an *operability behavior* observation, not a style critique.)
- **Image size / layer composition / build reproducibility** as engineering concerns → `SUBTASK_dockerfile_build`. (OPS-2 is a *documentation* finding — the size is not stated in the repo docs — not a size/repro judgment.)
- **Security posture** of the hardened-run block and distroless/non-root → `SUBTASK_security_supplychain`. I checked `deploy/README.md §Hardened run` only for doc accuracy; its security merits are that spoke's call.

## Read-only attestation

No file was edited, staged, committed, pushed, or merged; `main` and `work/containerize` untouched;
all diff access was read-only `gh`. Nothing was posted to GitHub (I5 honored). The container build was
**not** re-run (machine gate relied upon).
