## Review verdict: **APPROVE**

Principal-level human-review-equivalent read of `crates/ferric-http` (PR #15, `Closes #6`), on top of the already-green machine gate. I reviewed the full per-file diff vs `main` (1,356 additive lines), issue #6's acceptance criteria, and applied the `code-review`, `rust` (error handling, trait/API design), and `core` methodologies. No block- or major-severity findings. The crate is clean, well-documented, well-tested, and ergonomically sound.

### What's strong (specific praise)
- **Error taxonomy is exactly right.** `Error` distinguishes `Builder`/`Network`/`Status`/`Serialize`/`Deserialize`/`Body`; `#[non_exhaustive]` future-proofs the public enum; `source()` preserves the underlying `serde_json::Error` for the (de)serialization variants. `send()` returns the `Response` for *any* completed exchange (non-2xx is **not** an error — caller inspects), while `send_json()`/`error_for_status()` are safe-by-default (non-2xx → `Error::Status`). This is the correct, reqwest-like split and it is explicitly documented.
- **Testability by construction.** URL resolution + RFC-3986 percent-encoding are pure free functions, and `Response` is plain owned data, so `json`/`text`/`error_for_status` are synchronous — the whole logic surface is covered by native `cargo test` with the browser only on `send()`.
- **Percent-encoding is correct.** Unreserved set `A–Za–z0–9-_.~` passes through; everything else is `%XX` uppercase hex, byte-wise over UTF-8 (`é` → `%C3%A9`, space → `%20`). Tested.
- **No panics on fallible paths.** Every `unwrap`/`expect`/`panic!` is confined to `#[cfg(test)]` modules; zero on production paths. No `unsafe`. JS-boundary failures all map to typed `Error` variants.
- **Clean workspace integration.** Slots into `members = ["crates/*"]` with zero root-manifest edit; inherits `[workspace.lints]` (`missing_docs = warn`, clippy `all = warn`) under `-D warnings`, so rustdoc-on-public-items is machine-enforced.

### Non-blocking findings (minor / nit / suggestion)
| # | Severity | Location | Finding |
|---|----------|----------|---------|
| 1 | suggestion | `request.rs:109-115` (`header`) | Headers only ever *append* (Fetch combines same-named headers). A per-request `Authorization` layered over a `default_header("Authorization", …)` yields two combined values, not a replacement. Fine and documented for now; consider a `replace`-style setter or dedup-on-build before the chirp-server auth client is built on this. |
| 2 | suggestion | `request.rs` (`Method`) / `client.rs` | Scope for #6 is get/post/put/delete and is met. The later SPA/chirp REST client will likely want `PATCH`, and cookie-auth will want a `credentials`/`mode`/`redirect` `RequestInit` knob and a timeout/`AbortController`. Out of scope here — flagging for the consumer milestone, not this PR. |
| 3 | nit | `request.rs:334` (`read_body`) | `value.as_string().unwrap_or_default()` silently maps a non-string/null body to `""`; an empty body then surfaces via `send_json()` as a `Deserialize` error rather than a distinct "empty body" signal. Acceptable — the error is still typed and matchable. |
| 4 | nit | `request.rs:257-260` (`is_absolute`) | Allocates via `to_ascii_lowercase()` per request and treats protocol-relative `//host/path` as relative. Negligible; a prefix `eq_ignore_ascii_case` check would avoid the allocation. |
| 5 | nit | `request.rs:275-288` (`append_query`) | A `#fragment` in the path would place the appended query after the fragment. Pathological for a JSON API client; noting for completeness. |

### Acceptance criteria (issue #6)
All 7 substantively met: (1) member crate, no root edit ✅; (2) fetch-based async typed JSON verbs over web-sys/js-sys/wasm-bindgen-futures + serde ✅; (3) error taxonomy + ergonomic `Result`, no unwrap/panic on fallible paths ✅; (4) headers/query/base-URL + JSON content-type default ✅; (5) compiles for `wasm32-unknown-unknown` ✅; (6) native tests + documented `wasm-bindgen-test` ✅; (7) fmt/clippy `-D warnings` clean, rustdoc on public items, README usage + architecture ✅.

Recommend **merge**. The findings above are forward-looking notes, not merge blockers.
