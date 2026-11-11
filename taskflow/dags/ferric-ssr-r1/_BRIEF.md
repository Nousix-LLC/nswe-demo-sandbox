# _BRIEF.md — ferric-ssr-r1 code DAG (persona swe-coder)

## Objective

Implement the scope-limited SSR and hydration foundation for Ferric, covering server-side HTML rendering with per-request reactive isolation, client hydration without re-render, hydration mismatch detection, and the Axum server integration path.

This goal covers issues #223 (BAR-003), #224 (BAR-004), and #226 (BAR-006) from epic #133 (Server-Side Rendering and Hydration). The state carry and async resource resume work (BAR-005 / #225) is **explicitly out of scope**: it is blocked on issue #130 (async resource primitive) and will be a follow-up.

## Issues and acceptance criteria

### #223 — Server-side HTML rendering and per-request scope isolation (BAR-003)

Acceptance criteria:
- `render_to_string` function that takes a Ferric component tree and produces an HTML string.
- The ferric crate (or a new `ferric-ssr` sub-crate under `crates/ferric`) compiles natively off-wasm; no browser APIs (`web_sys`, `wasm_bindgen`) are referenced in the server-render path.
- Text-boundary markers in the output are unambiguous and can be matched by the hydration walk.
- HTML escaping holds for all injection-risky characters (at minimum `<`, `>`, `&`, `"`, `'`).
- Each call to `render_to_string` runs in its own reactive context; no signal subscription leaks across concurrent render calls. Testable by rendering two requests concurrently with different seeded state and verifying outputs are independent.
- The surface is additive: existing code that uses `mount` and the frozen `ferric` prelude compiles and behaves without modification.
- Requirement references: REQ-SSR-001, REQ-SSR-002, REQ-SSR-003, REQ-SSR-010, REQ-SSR-012.

### #224 — Client hydration without re-render — must-have (BAR-004)

Acceptance criteria:
- `hydrate` entry point that adopts a server-rendered DOM subtree.
- Zero structural mutations during hydration under the hydration root: no DOM nodes created, replaced, moved, or removed during the adopt pass. This is the gating observable bar. Must be verifiable by `MutationObserver` or by node-identity comparison in a headless `wasm-bindgen-test`.
- Existing `Click` and `Input` event handlers wire onto adopted elements during hydration.
- Reactive effects are established on adopted elements; subsequent signal updates patch via the existing keyed-patch path.
- Requirement references: REQ-SSR-004, REQ-SSR-005.

### #226 — Hydration mismatch detection and Axum server integration (BAR-006)

Acceptance criteria:
- The hydration walk detects tag/text divergence at any path in the tree.
- In dev builds (cfg(debug_assertions)), a diagnostic names the mismatch path with the expected tag/text and what was found — actionable for the developer.
- A mismatched subtree is recovered by client-rendering that subtree; the rest of the already-adopted document is not disturbed.
- `render_to_string` and a document assembly helper are callable from an Axum handler (in `crates/chirp-server` or a new adjacent crate), composing with the existing `build_router` surface.
- Usage is documented (in an example or inline doc comment).
- Requirement references: REQ-SSR-009, REQ-SSR-011.

## Inputs

- **Repository**: `Nousix-LLC/nswe-demo` at commit `945fade38abd6b053268501f3801734756f02502` on `main`.
- **Design specs** (merged via PR #128, on `main`):
  - `design/ferric/ssr-hydration.md` — authoritative source for the SSR architecture and requirements register `REQ-SSR-*`.
  - `design/ferric/scope-and-requirements.md` — the requirements register.
- **Current ferric crate surface** (`crates/ferric`): `signal`, `vdom`, `component`, `dom`, the frozen `ferric` prelude including `mount`.
- **Axum server** (`crates/chirp-server`): existing `build_router` and server infrastructure.
- **Authoring model** (landed in PR #188, commit `aa2468771`, on `main`): `view!` macro, component system, context.
- **Client-side router** (landed in PR #203, commit `d8230fea`, on `main`).
- **HTTP client** (landed in PR #210, commit `945fade3`, on `main`): fetch/JSON HTTP client.

## Declared output

- Commits on branch `work/ferric-ssr-r1`.
- One PR closing issues #223, #224, #226 (BAR-003, BAR-004, BAR-006), with the following note in the PR description: "BAR-005 / #225 (state carry + async resource resume) is a follow-up issue dependent on #130 and is NOT part of this goal."
- Root `SYNTHESIS.md` accounting for each issue (#223, #224, #226): met, or not and why.

## Concerns to cover

- **Server render correctness**: `render_to_string` produces valid, well-formed HTML; text-boundary markers are unambiguous and unambiguously parseable; HTML escaping holds for all injection-risky characters; the view layer builds natively off-wasm with no browser APIs; `REQ-SSR-001`, `REQ-SSR-002`, `REQ-SSR-003`, `REQ-SSR-010`, `REQ-SSR-012`.

- **Per-request isolation**: each server render runs in its own reactive context; no signal subscription leaks across requests; the isolation is confirmed by a concurrent-render test with different seeded state; `REQ-SSR-003`.

- **Hydration without re-render**: `hydrate` adopts the server DOM with zero structural mutations under the hydration root; the gating bar is zero create/replace/move/remove, verifiable by `MutationObserver` or node-identity in a headless `wasm-bindgen-test`; `REQ-SSR-004`, `REQ-SSR-005`.

- **Event wiring on adopt**: existing `Click` and `Input` handlers wire onto adopted elements; subsequent signal updates patch via the existing keyed-patch path; `REQ-SSR-005`.

- **Mismatch detection and recovery**: the hydration walk detects tag/text divergence at any path; dev-build diagnostic names path + expected/found; mismatched subtree is recovered by client-rendering; the rest of the document remains adopted; `REQ-SSR-009`.

- **Axum integration**: `render_to_string` and a document assembly helper callable from an Axum handler; composing with `chirp-server`'s existing `build_router`; documented usage; `REQ-SSR-011`.

- **Additive surface**: `mount` and the frozen prelude are unchanged; `hydrate` and `render_to_string` are new surface; existing apps compile and run without modification; `REQ-SSR-012`.

- **Test coverage**: server-render path covered by native tests (not wasm); hydration path covered by headless `wasm-bindgen-test`; mismatch detection covered by a headless test with a deliberately mismatched DOM; Axum integration covered by an example or integration test.

## Constraints

- Branch: `work/ferric-ssr-r1`. Do not force-push to `main`.
- Scope: `crates/ferric` and `crates/chirp-server` only; do not touch other crates except additive entries in `Cargo.toml`/workspace.
- BAR-005 (#225) is out of scope: do not attempt async resource serialisation or state island implementation.
- The frozen `ferric` prelude surface (including `mount`, `Signal`, `create_effect`, router, HTTP client) must remain unchanged; all additions are additive.
- Whatever the PR posts to GitHub is written for the repository's readers: outcome, what changed, how it was verified, and the issues it closes — no host paths or taskflow internals.
