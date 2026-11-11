# app.rs Quality Notes

Reviewed at commit `75c1eef` (branch `work/ferric-ssr-r1`, PR #228).
File: `crates/chirp-frontend/src/app.rs`.

---

## cfg-gate idiom

**Severity**: Pass
**Evidence**: `app.rs:154–161`

`#[cfg(target_arch = "wasm32")]` is applied at the statement level, which is the
correct scope: `ferric::hydrate` does not exist on non-wasm32 targets, so a
compile-time gate is required (a runtime `cfg!()` branch would not suppress the
missing-symbol error). The two guards — `#[cfg(target_arch = "wasm32")]` and
`#[cfg(not(target_arch = "wasm32"))]` — are mutually exclusive and exhaustive with
no gap between them. `ferric::hydrate` is called fully-qualified, so no conditional
import is needed. The pattern is idiomatic statement-level cfg for conditional
wasm32 behavior.

---

## Conditional dispatch logic

**Severity**: Warning
**Evidence**: `app.rs:155`

`has_child_nodes()` returns `true` for any child node — element nodes, whitespace
text nodes, and HTML comments. If the server's HTML template wraps SSR content with
surrounding whitespace inside `#app` (e.g., `<div id="app">\n  {content}\n</div>`),
a fresh page load with no SSR content could arrive with whitespace text-node
children and incorrectly trigger `ferric::hydrate` on an empty VNode tree.

`Element::first_element_child()` counts only element children — it excludes text and
comment nodes — and matches the actual intent of "SSR markup is present". The check
at line 155 should be verified against the server's HTML template (in
`chirp-server/src/ssr.rs`) to confirm that `#app` cannot contain incidental text
nodes on a non-SSR page load, or the guard should be changed to
`root.first_element_child().is_some()`.

---

## Error handling

**Severity**: Warning
**Evidence**: `app.rs:156`

`ferric::hydrate(root, app)` on line 156 discards its return value. If `hydrate`
returns a `Result` without a `#[must_use]` annotation, a mismatch between the
server-rendered DOM and the client VNode tree fails silently — the DOM is left in a
partially-patched state with no log entry. The adjacent `mount(root, app)` calls on
lines 158 and 161 share this gap, so the PR is consistent with the surrounding code,
but hydration failures differ in kind: `mount` on a non-empty root replaces the
content cleanly, while a hydration mismatch corrupts the existing DOM in place.

Verify `ferric::hydrate`'s return type and whether the library signals mismatch
through a returned error, a panic, or a side-channel. If it returns `Result`, either
annotate it `#[must_use]` in the library or handle the error at the call site.

---

## Docstring accuracy

**Severity**: Warning
**Evidence**: `app.rs:8`, `app.rs:103–104`

The module-level docstring on line 8 describes the module as one that "mounts the
application into `#app` (falling back to `<body>`)". The `start()` function
docstring on lines 103–104 says the function will "mount the app into `#app`
(falling back to `<body>`)". Neither mentions that on wasm32 targets `start()` now
conditionally hydrates server-rendered content rather than always mounting.

A reader consulting either docstring would not know hydration occurs. Both should be
updated to describe the conditional behavior: hydrate when SSR markup is present in
the mount root on wasm32; mount fresh otherwise; always mount on non-wasm32.

---

## Readability

**Severity**: Pass
**Evidence**: `app.rs:150–161`

The inline comment at lines 150–153 names both paths (hydrate vs mount), gives the
condition that determines which runs, and explains why a compile-time cfg gate is
used rather than a runtime branch. The two sequential `#[cfg]`-gated statements form
an exhaustive pair that Rust readers familiar with cfg attributes will follow without
ambiguity. Variable names `root` and `app` carry through unchanged from the
surrounding code. The structure is clear for the target audience.

---

## Fresh Non-Blockers (if any)

- `app.rs:156`: `ferric::hydrate` is called fully-qualified while `mount` arrives
  via `use ferric::prelude::*`. This is a minor style inconsistency — `hydrate` may
  not be re-exported from the prelude, so the full path may be the only option; no
  action needed unless `hydrate` is added to the prelude in a later revision.
