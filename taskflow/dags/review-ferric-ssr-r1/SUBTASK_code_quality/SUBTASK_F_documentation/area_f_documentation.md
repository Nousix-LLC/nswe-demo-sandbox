# Area F: Documentation — PR #228

**Status**: FINDING (NON-BLOCKER)

---

## What Was Checked

**`ferric::render_to_string`** (`crates/ferric/src/ssr.rs:124–138`)
Examined the `///` doc comment on the function. It covers purpose (render a component closure to an HTML string), reactive-scope isolation (fresh `ReactiveScope`, dropped before return), HTML escaping, text-sentinel wrapping (`TEXT_OPEN_MARKER` / `TEXT_CLOSE_MARKER`), and compile target (native/non-wasm only). No `# Examples` section, but the prose and type signature (`F: FnOnce() -> VNode`) together give a first-time caller sufficient context to invoke the function correctly.

**`ferric::hydrate`** (`crates/ferric/src/hydrate.rs:35–40`)
Examined the `///` doc comment on the function and the module-level `//!` comment. The module doc explains the three-phase protocol (adopt pass, sentinel cleanup, reactive effects) in detail. The function doc covers what `hydrate` does and states that `f` must match the closure used for the SSR render. Examined for a usage example and for the documented caveats enumerated in the brief.

**`ferric::ssr::TEXT_OPEN_MARKER` / `TEXT_CLOSE_MARKER`** (`crates/ferric/src/ssr.rs:21–35`)
Examined both `pub const` doc comments for the marker-format stability caveat named in the brief.

**`chirp-server::ssr::assemble_document`** (`crates/chirp-server/src/ssr.rs:65–117`)
Examined doc comment for coverage, example quality, and prose clarity. Not a `ferric` pub item; checked as adjacent user-facing prose the PR ships.

**`chirp-server::ssr::ssr_handler`** (`crates/chirp-server/src/ssr.rs:119–174`)
Same examination.

**PR description prose**
Checked for inflated language, machine-writing tells (moral/character adjectives on non-agentic nouns, narrated candor, slot-fill templates, padding filler), and factual accuracy.

---

## Evidence

**Finding 1 — `hydrate`: no timing caveat, no usage example**

`crates/ferric/src/hydrate.rs:35–40` — the entire function doc comment:

```
/// Adopt a server-rendered DOM subtree rooted at `root`, wire event handlers, and establish
/// a reactive effect that keeps the DOM up-to-date when signals change.
///
/// `f` must be the same component closure used for the server-side `render_to_string` call
/// that produced the HTML now under `root`.
```

Nothing states when this function must be called relative to DOM state. If a user calls `hydrate` before the SSR HTML exists in the DOM (e.g., invoking it synchronously before the page has fully loaded), `root.first_child()` returns `None` and mismatch recovery silently client-renders the entire subtree — no error, only a `console.warn` in debug builds (`crates/ferric/src/hydrate.rs:261–272`). The SSR benefit is discarded without any visible indication. No `# Examples` section shows how to wire the call correctly (obtain the `#app` element, call `hydrate` from the WASM entry point after the DOM is ready).

**Finding 2 — `TEXT_OPEN_MARKER` / `TEXT_CLOSE_MARKER`: no version-stability note**

`crates/ferric/src/ssr.rs:21–28` and `crates/ferric/src/ssr.rs:30–35` — both constants' doc comments instruct callers to "use this exact literal — never define a local copy." Correct advice for today, but neither comment states whether the marker *format* itself (`<!--$t-->` / `<!--/$t-->`) is stable across ferric versions. A user who pre-renders and caches server HTML then upgrades ferric would experience silent hydration failure if the marker format changes — the cached HTML carries old markers, the upgraded hydration client expects new ones, and the mismatch recovery path silently client-renders without error.

---

## Finding

**`hydrate` is underdocumented for a first-time user of this surface (NON-BLOCKER).**

The function doc gives the protocol overview (at the module level) and the `f`-must-match requirement (at the function level), but omits the most mistake-prone part of the calling contract: `hydrate` must be called only after the SSR HTML is already in the DOM under `root`. When called before that point, the code silently degrades to a full client-render via mismatch recovery — correct enough to not break the app, but wrong enough to defeat the SSR purpose. A debug `console.warn` is the only signal. Neither the function doc nor the module doc names this requirement or provides an example showing the correct call-site pattern.

What a sufficient doc comment would add:
1. A `# Calling Contract` or `# When to Call` note stating the function must be invoked after the SSR HTML is in the DOM (e.g., from a `#[wasm_bindgen(start)]` function or equivalent, after the browser has parsed the server-rendered document).
2. A `# Examples` section showing how to obtain the mount element and call `hydrate`, mirroring the pattern in `chirp_server::ssr`'s module doc.

**Marker-format stability is undocumented (NON-BLOCKER).**

`TEXT_OPEN_MARKER` and `TEXT_CLOSE_MARKER` are `pub const` values on a `pub mod ssr` — first-class public API. Their doc comments correctly tell consumers to import the constants rather than copy the literals. What they do not say is whether the marker format is stable across ferric versions. For a framework where server HTML may be cached (CDN, static export, pre-render pipeline), a version bump that changes the marker format would silently break hydration in production without any compile-time or link-time error. Adding a `# Stability` note — even a provisional one (e.g., "the marker format is not yet considered stable; pin your ferric dependency to a minor version if you cache server-rendered HTML") — would let users make informed decisions about upgrade cadence.

**What was clean:** `render_to_string` has adequate prose coverage for a first-time caller (type signature plus scope-isolation and escaping notes). `assemble_document` and `ssr_handler` in `chirp-server::ssr` are well-documented with examples, parameter descriptions, and a `# Panics` note. The PR description prose is factual and plain; no clustered machine-writing tells.
