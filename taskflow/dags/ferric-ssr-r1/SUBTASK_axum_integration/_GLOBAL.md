# _GLOBAL.md — ferric-ssr-r1-axum-integration

Atomic task. See parent hub: `../\_GLOBAL.md`.

This task implements the Axum server integration portion of Issue #226 (BAR-006): a document
assembly helper and route handler in `crates/chirp-server` that calls `render_to_string` and
composes with the existing `build_router`. It runs on branch `work/ferric-ssr-r1-axum`
(based on `work/ferric-ssr-r1` after the skeleton has committed).

The server-render and client-hydrate spokes run concurrently with this task. This spoke does
not depend on those spokes completing first — it depends only on the skeleton, which
establishes the `render_to_string` stub in `crates/ferric`. The Axum handler can call the
stub signature; the synthesis gate verifies the full end-to-end once all spokes land.

Contracts inherited read-only from `../contracts/`.
