# Findings — SUBTASK_rustcode_sigterm

- **Spoke**: `SUBTASK_rustcode_sigterm`
- **Concerns owned**: Concern 5 (SIGTERM handling in `crates/chirp-server/src/main.rs`: correctness, unix-gating, no regression, scope fit) + the concern-6 slice *"Rust idiom of the SIGTERM change AND the std-only probe (`deploy/docker/healthcheck.rs`)"*.
- **Diff reviewed**: PR #22 head commit `bc0c3c0d6380c9edd1b9433addc7fdcbffb55751` of `Nousix-LLC/nswe-demo`.

## Per-concern dispositions

### Concern 5 — SIGTERM handling correctness, unix-gating, no-regression, scope-fit: `PASS-WITH-NOTES`

The change rewrites the private `async fn shutdown_signal()` (wired into `axum::serve(listener, app).with_graceful_shutdown(shutdown_signal())`) to await **either** SIGINT or SIGTERM via `tokio::select!`, where previously it awaited only `tokio::signal::ctrl_c()`.

- **Correct.** The `terminate` future uses the idiomatic `tokio::signal::unix::{signal, SignalKind}` API — `signal(SignalKind::terminate())` then `term.recv().await` — matching the Tokio graceful-shutdown pattern. When either signal arrives, `shutdown_signal()` resolves and axum stops accepting and drains in-flight requests (`main.rs:88–96`). This is exactly what makes a container drain and exit 0 on `docker stop`/Kubernetes stop rather than being SIGKILL'd (exit 137).
- **Unix-gated correctly.** The real `terminate` is `#[cfg(unix)]`; `#[cfg(not(unix))] let terminate = std::future::pending::<()>();` keeps non-unix compiling, where only SIGINT can drive shutdown (correct — Windows has no SIGTERM). Confirmed compiling + `clippy -D warnings` clean by the machine gate.
- **No spurious-shutdown trap.** A failed SIGTERM-handler install logs the error and then `std::future::pending::<()>().await` — it defers to the SIGINT branch rather than firing a false shutdown. This is the right call (`main.rs:80–84`).
- **No API/transport/behavior change.** `shutdown_signal()` is a private `async fn` with unchanged signature; no routes, DTOs, or transport touched. The only behavior delta is the expanded shutdown-trigger set — precisely the clean-shutdown change intended.
- **No regression.** Machine gate (`taskflow/dags/containerize/SYNTHESIS.md`) records `cargo fmt`/`clippy -D warnings`/`cargo test -p chirp-server` (20 passed) clean *after* this change, and `docker stop` → exit 0 in ~0.3 s with the expected drain log. The SIGINT path is preserved.
- **Minimal / in-scope.** This is the minimal repo change required to run cleanly in a container — it does not reach for `tokio-util` `CancellationToken`/`TaskTracker` scaffolding (unnecessary here, since axum's `with_graceful_shutdown` already performs the drain). It is justified and belongs in work-item #12's scope; it is not scope creep.

One nit (RUST-1) on a pre-existing, documented asymmetry in the SIGINT branch; see table. No `block`/`major`/`minor`.

### Concern 6 (Rust-idiom slice) — SIGTERM change + `deploy/docker/healthcheck.rs`: `PASS-WITH-NOTES`

- **SIGTERM change idiom.** Clean and idiomatic: two lazy `async` blocks resolved under `tokio::select!`; `std::future::pending::<()>()` used correctly both for the non-unix branch and the failed-install defer; the `#[cfg(unix)]`/`#[cfg(not(unix))]` `let terminate` bindings both yield a `Future<Output = ()>`. The doc comment is accurate and complete.
- **`healthcheck.rs` idiom (Rust quality only).** Std-only as intended — only `std::*` imports, no crates, so it compiles with bare `rustc` and never touches the workspace manifest. `probe_port()` is a clean `Option` combinator chain (`rsplit(':').next()` → non-empty + all-ASCII-digit filter → `unwrap_or_else("8080")`). `healthy()` sets connect/read/write timeouts (important — a probe must not hang), uses HTTP/1.0 + `Connection: close` so `read_to_end` terminates without `Content-Length` parsing, and maps the status line to `io::Result<bool>`; `main()` maps `Ok(true)` → exit 0, everything else → exit 1. No `unsafe`, no FFI. `clippy -D warnings` clean per the machine gate.

One nit (RUST-2) on `probe_port` returning `String` rather than a parsed `u16`; see table. No `block`/`major`/`minor`.

> Scope note: the probe's *operational* behavior (port-knob matching, docs, out-of-box health) is owned by `SUBTASK_operability_docs` and is cross-referenced here, not re-filed.

## Findings

| Finding ID | Concern | Severity | Location | Evidence | Remediation |
|---|---|---|---|---|---|
| RUST-1 | 5 | nit | `crates/chirp-server/src/main.rs:73–77` (the `interrupt` block) | On a *failed* `ctrl_c()` install the `interrupt` block logs the error and then resolves, which completes the `select!` and triggers an immediate graceful shutdown — asymmetric with the SIGTERM branch, which defers via `pending()`. This is **pre-existing** behavior (the prior `shutdown_signal()` also returned on `ctrl_c` error) and is explicitly documented in the doc comment ("SIGINT: immediately"). It fires only in the degenerate case where the SIGINT handler cannot be installed, which effectively never happens on supported platforms. | Optional: for symmetry, treat a SIGINT-install failure the same as SIGTERM's (`pending()` and defer) so neither install failure can cause a spurious shutdown. Non-blocking; defensible as-is. |
| RUST-2 | 6 | nit | `deploy/docker/healthcheck.rs:22–29` (`probe_port`) | `probe_port` returns `String`, re-interpolated into `format!("127.0.0.1:{}")` and then `.parse::<SocketAddr>()`. The all-digits filter makes the subsequent parse safe, so this is correct; parsing to `u16` up front would be marginally stronger typing. | Optional: return `u16` (`.and_then(|s| s.parse().ok())`) and build the `SocketAddr` from `(Ipv4Addr::LOCALHOST, port)`. Purely stylistic; current form is fine. |

_No `block`, `major`, or `minor` findings. The SIGTERM change is correct, unix-gated, regression-free, and minimal; the std-only probe is clean idiomatic Rust._
