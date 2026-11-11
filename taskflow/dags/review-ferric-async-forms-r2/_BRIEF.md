# _BRIEF.md — review-ferric-async-forms-r2 (swe-reviewer)

## Objective

Review PR #193 (`work/ferric-async-forms-r2` → `main`, repo Nousix-LLC/nswe-demo).  
This PR implements Ferric 1.0 Async Resources, Forms, and Events: issues #130 (EPIC), #143, #144, and #145.  
Post the review on PR #193. Produce a root `SYNTHESIS.md` with an APPROVE or REQUEST-CHANGES verdict and findings per concern.

---

## Target

- **PR**: https://github.com/Nousix-LLC/nswe-demo/pull/193  
- **Branch**: `work/ferric-async-forms-r2` → `main`, repo Nousix-LLC/nswe-demo  
- **Head SHA** (at review launch): all 6 CI PASS on run 41780600207  
- **Code DAG terminal record**: `taskflow/dags/ferric-async-forms-r2/COMPLETE.md`

### Issues closed by this PR and their acceptance criteria

**#130 (EPIC) — Async Resources and Suspense (REQ-ASYNC-001..016)**  
- REQ-ASYNC-001: `Resource<T>` type wrapping an async fetch, integrated with the reactive system (re-fetches on signal change)  
- REQ-ASYNC-002: `ResourceState<T>` enum (`Loading`, `Ready(T)`, `Error(String)`)  
- REQ-ASYNC-003: `resource()` constructor takes a signal-dependent async function and returns `Resource<T>`  
- REQ-ASYNC-004: initial fetch runs immediately on creation  
- REQ-ASYNC-005: resource re-fetches when any read signal changes (reactive dependency tracking)  
- REQ-ASYNC-006: `suspense()` renders a placeholder while any `Resource` in its subtree is loading  
- REQ-ASYNC-007: `suspense()` renders content when all resources are ready  
- REQ-ASYNC-008: errors are captured in `ResourceState::Error`; view! can pattern-match on them  
- REQ-ASYNC-009..016: resource lifecycle (cancel in-flight on re-fetch, teardown on drop, concurrent safety, etc.)

**#143 — DOM Event Handling (REQ-ASYNC-020..024)**  
- REQ-ASYNC-020: `on:click`, `on:input`, `on:change`, `on:submit`, `on:keydown`, `on:keyup`, `on:focus`, `on:blur` wired to DOM elements  
- REQ-ASYNC-021: custom events via `on:<name>` where name is not a static variant  
- REQ-ASYNC-022: event handler teardown on component unmount  
- REQ-ASYNC-023: `event.prevent_default()` and `event.stop_propagation()` callable from handlers  
- REQ-ASYNC-024: 47 static `EventKind` variants exported; `EventKind::Custom(String)` for all others

**#144 — Form Bindings (REQ-ASYNC-040..043)**  
- REQ-ASYNC-040: `bind:value` two-way binding on `<input>`, `<textarea>`, `<select>` driven by a `Signal<String>`  
- REQ-ASYNC-041: `FormField<T>` and `Bind<T>` types providing the two-way sync  
- REQ-ASYNC-042: binding updates the signal on user input and updates the DOM when the signal changes  
- REQ-ASYNC-043: binding teardown on unmount

**#145 — Further Async Concerns**  
Covers implementation quality, error propagation, and async hazards not captured by the above requirements.  
Acceptance: no data races, no memory leaks in async resource lifecycle, no panics in WASM on common async paths.

### Design reference

`design/ferric/async-forms-events.md` (Ferric 1.0 design, async/forms/events chapter) in Nousix-LLC/nswe-demo.

---

## Review concerns (each is distinct; address each separately with its goal and bar)

### 1. Correctness
Does the change implement REQ-ASYNC-001..024, REQ-ASYNC-040..043 correctly?

Specifically:
- Does `Resource<T>` re-fetch reactively when signals change, and does it cancel any in-flight fetch before starting a new one?
- Does `ResourceState` cover the full loading/ready/error lifecycle, with error captured rather than panicked?
- Does `suspense()` render the placeholder exactly while loading and switch to content on all-ready?
- Do the 47 static `EventKind` variants and `Custom(String)` match the design's event set?
- Are event handlers torn down on component unmount (no listener leak)?
- Does `Bind<T>` produce two-way sync: DOM→signal on input, signal→DOM on signal change?
- Are the edge cases handled: form field bound to an initially empty signal, custom event with an empty name, resource that errors then is re-fetched and succeeds, `suspense()` containing a resource that errors?
- Are there async hazards: resource lifecycle across concurrent fetches, signal/reactive invalidation during an in-flight fetch, WASM runtime panics on the async paths?

Bar: every requirement is met; no edge-case path silently diverges from the specified behavior.

### 2. Code quality and design
Are the abstractions well-drawn and the code clear to extend?

Specifically:
- Is the split between `async_resource.rs`, `form.rs`, `dom.rs`, and `vdom.rs` clean, with each owning one responsibility?
- Are `Resource<T>`, `Bind<T>`, `FormField<T>`, and `suspense()` coherent, minimally coupled abstractions?
- Is naming clear and consistent with the rest of `crates/ferric` (signals, component model, vdom)?
- Are functions sized appropriately, with no large catch-all routines?
- Is error handling idiomatic: errors surfaced in return types or `ResourceState`, not panicked?
- Does the change leave `crates/ferric` easier to extend (the next epic can add HTTP client on top of `Resource<T>` without fighting the async resource design)?

Bar: a reviewer reading a fresh copy of the crate can follow each abstraction without surprise.

### 3. Test coverage and depth
Do the tests exercise each acceptance criterion and the edge and error paths?

Specifically:
- Do native tests cover each `ResourceState` variant, the reactive re-fetch trigger, the cancel-on-re-fetch path, and the error path?
- Do WASM tests (3 noted in the COMPLETE.md) exercise the WASM-specific behavior (DOM event dispatch, actual form binding round-trip)?
- Do the 18 `form.rs` native tests and the 20 `async_resource.rs` native tests assert real behavior (state transitions, signal updates) rather than passing vacuously (e.g. constructing a struct and asserting `true`)?
- Are the error paths tested: resource that errors, re-fetch after error, binding to a signal that changes before DOM is mounted?
- Is teardown tested: unmounting a component with a bound form field or a loaded resource, and verifying the listener/resource was cleaned up?

Bar: every acceptance criterion has at least one test; every error path has at least one test; no test passes vacuously.

### 4. Security
Does the change introduce any security exposure?

Specifically:
- Is custom event data (from `EventKind::Custom(String)` and `on:input`) handled safely, without interpreting user-supplied strings as code or as privileged identifiers?
- Does the web-sys/wasm-bindgen bridge handle untrusted DOM values safely (no `unwrap` on arbitrary JS values without fallback)?
- Are there any host-specific or internal-infrastructure details committed in the diff (absolute host paths, tailnet `100.x` or LAN IPs, internal server URLs, host runtime or taskflow directory paths)?
- Does the change pull in any new dependencies beyond `wasm-bindgen-futures` that require scrutiny?

Bar: no exposed trust boundary, no committed infrastructure detail, no unsafe data flow from untrusted DOM input to privileged state.

### 5. Rust idioms
Is the code sound, with correct lifetimes and idiomatic async/WASM patterns?

Specifically:
- Are lifetimes explicit where needed (closures capturing signals, async blocks capturing resource state)?
- Is `unsafe` present, and if so, is it justified and minimal?
- Are the WASM async patterns idiomatic (`wasm_bindgen_futures::spawn_local`, `Closure::wrap`, etc.)?
- Is the `EventKind` enum's removal of `Copy + Ord` (noted in COMPLETE.md) sound? Do any downstream usages require those traits?
- Are there clippy-worthy patterns (redundant clones, unnecessary `Box<dyn …>`, avoidable `unwrap`s)?

Bar: no soundness issues; idiomatic WASM async; no gratuitous deviations from Rust conventions.

### 6. API/contract stability
Does the public API align with what `chirp-frontend` and future ferric epics would depend on?

Specifically:
- Are `Resource<T>`, `ResourceState<T>`, `Bind<T>`, `FormField<T>`, and `suspense()` correctly re-exported through the `ferric::prelude`?
- Does the API match the design's declared public surface (`design/ferric/async-forms-events.md`)?
- Does the `EventKind` expansion (2 → 47 + `Custom(String)`) preserve backward compatibility with existing usages in `crates/ferric` and `crates/chirp-frontend`?
- Are the new types sealed or extensible in the right ways — `ResourceState` is exhaustive (match on it), `EventKind::Custom` is open (any string)?
- Does the removal of `Copy + Ord` from `EventKind` break any existing uses in the codebase?

Bar: `chirp-frontend` can depend on these types without change; no silent breaking changes to existing API surface.

---

## Declared output

1. **Posted review** on PR #193 (https://github.com/Nousix-LLC/nswe-demo/pull/193) with the verdict (APPROVE or REQUEST-CHANGES) and findings per concern. If the platform blocks posting as a formal approval (same account), post as a comment carrying the verdict and all findings. Every finding points at a file and line in the repository; no host paths or taskflow internals.

2. **Root `SYNTHESIS.md`** at `taskflow/dags/review-ferric-async-forms-r2/SYNTHESIS.md` with:
   - Overall verdict: APPROVE or REQUEST-CHANGES
   - Per-concern summary: what was checked, what was found, severity (blocker / non-blocker / clean), and blocker status
   - For each blocker: the specific behavior or criterion it fails, with file/line reference where possible
   - For each non-blocker: a one-line description suitable for filing as a backlog issue

3. **Non-blocking findings filed as backlog issues** on Nousix-LLC/nswe-demo (one issue per finding or grouped where closely related), linked to PR #193. Filed findings are listed in `SYNTHESIS.md`.

---

## Constraints

- Repo scope: Nousix-LLC/nswe-demo only. No findings, issues, or posts to any other repository.
- No host paths, tailnet IPs, internal server URLs, or taskflow directory paths in anything posted to GitHub.
- Read and judge; do not edit the repository or the PR diff.
