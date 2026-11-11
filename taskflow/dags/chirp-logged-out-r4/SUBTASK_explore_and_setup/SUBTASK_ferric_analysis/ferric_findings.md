# Ferric Framework API Findings

## Resource / Async Data-Loading API

**Type name:** No `Resource<T, E>` type exists. Ferric has no built-in reactive async
data-loading wrapper (unlike Leptos/Solid's `create_resource`).

**Available async tooling:** `ferric-http` provides a plain async HTTP/JSON client over the
browser Fetch API (`crates/ferric-http/`). It is fully independent of the signal system —
it has no `Resource` state machine. Async futures must be bridged to signals manually via
`wasm_bindgen_futures::spawn_local`.

**Idiomatic pattern — manual signal + spawn_local:**

```rust
use ferric::prelude::*;
use ferric_http::Client;
use wasm_bindgen_futures::spawn_local;

// Represent three states with a single signal:
//   None           → loading (initial)
//   Some(Err(e))   → fetch failed
//   Some(Ok(posts))→ loaded with data
let state: Signal<Option<Result<Vec<Post>, String>>> = create_signal(None);

// Fire the fetch once (outside any reactive effect so it does not re-run on render).
let state_writer = state;
spawn_local(async move {
    let client = Client::builder().base_url("/api").build();
    match client.get("/timeline").send_json::<Vec<Post>>().await {
        Ok(posts) => state_writer.set(Some(Ok(posts))),
        Err(e)    => state_writer.set(Some(Err(e.to_string()))),
    }
});

// In a component closure — pattern-match the signal:
let timeline = move || -> VNode {
    match state.get() {
        None             => text("Loading…"),
        Some(Err(msg))   => text(format!("Error: {}", msg)),
        Some(Ok(posts))  => {
            if posts.is_empty() {
                text("No posts yet.")
            } else {
                // render list ...
            }
        }
    }
};
```

**Loading state representation:** `None` (the signal's initial value)  
**Error state representation:** `Some(Err(e))`  
**Loaded state representation:** `Some(Ok(data))`  

**Source:** No dedicated file — `Signal` is in `crates/ferric/src/signal.rs`;
`ferric-http` client is in `crates/ferric-http/src/`.

---

## Router API

**Source:** `crates/ferric-router/src/router.rs`, `crates/ferric-router/src/matcher.rs`,
`crates/ferric-router/src/link.rs`; prelude in `crates/ferric-router/src/lib.rs`.

**Import:**
```rust
use ferric_router::prelude::*;  // Router, navigate, navigate_replace, current_path, Params, RoutePattern, link
```

### Route definition

Routes are registered with the fluent builder method `.route(pattern, view_fn)`.  
The view function signature is `Fn(&Params) -> VNode + 'static`.

```rust
.route("/", |_params| text("home"))
.route("/user/:id", |params| {
    let id = params.get("id").unwrap_or("unknown");
    text(format!("user {}", id))
})
```

### Route parameter syntax

Named parameters use `:name` segments: `/user/:id`, `/api/v1/post/:slug`.  
Matching is **exact over segments** — no wildcards, no optional segments.  
Parameters are extracted into `Params` and read with `.get("name") -> Option<&str>`.

### Route mounting / composition

```rust
let router = Router::new()
    .route("/", |_| home_view())
    .route("/about", |_| about_view())
    .route("/user/:id", user_view)
    .fallback(|_| not_found_view())
    .mount_history();          // seeds path from window.location; installs popstate listener

let outlet = router.outlet(); // consumes Router into impl Component

mount(root, app);              // ferric::dom::mount wires the outlet component into the DOM
```

`.mount_history()` — seeds the reactive current-path signal from `window.location.pathname`
and installs a `popstate` listener (back/forward). Call once at startup.

`.outlet()` — consumes the router into a `Component` that re-renders whenever the current
path changes (it reads the current-path `Signal` inside the render effect).

### Nested routes

```rust
Router::new()
    .route("/", |_| home_view())
    .nest(
        "/settings",
        |_params, child_outlet| {
            VElement::new("section")
                .child(text("Settings nav"))
                .child(child_outlet.render())  // renders matched child route
                .into()
        },
        |child_router| {
            child_router
                .route("/", |_| settings_index_view())
                .route("/profile", |_| settings_profile_view())
                .fallback(|_| not_found_view())
        },
    )
```

Child routes are matched against the **remaining path** after the prefix; `/settings/profile`
→ prefix `/settings` matched → child path `/profile` matched.

### Programmatic navigation

```rust
navigate("/path");         // pushState — back-button works
navigate_replace("/path"); // replaceState — no back entry (redirects, login flows)
current_path()             // read reactive current path; subscribes the calling effect
```

### In-app links

```rust
link("/about", "About")   // returns VNode: <span role="link" data-to="/about">About</span>
                           // adds aria-current="page" when to == current_path()
```

Links are `<span>` (not `<a href>`) because ferric click handlers are zero-argument `Fn()`
and cannot call `event.preventDefault()`. A `data-to` attribute records the destination for
styling and accessibility tools.

---

## SSR and Hydration

**Source:** `crates/ferric/src/ssr.rs` (always compiled); `crates/ferric/src/hydrate.rs`
(`#[cfg(target_arch = "wasm32")]` only).

### SSR available: **yes**

### SSR invocation

```rust
use ferric::render_to_string;

// On the server (native host, no wasm):
let html: String = render_to_string(|| my_component());
```

`render_to_string<F: FnOnce() -> VNode>(f: F) -> String`

- Runs `f` inside a fresh `ReactiveScope` (disposed before return, so no signal leaks)
- HTML-escapes `< > & " '` in text nodes and attribute values
- Wraps `VNode::Text` in comment sentinels `<!--$t-->…<!--/$t-->` so the hydration pass can
  identify text boundaries
- Void elements self-close (`<br />`, `<input />`, `<img />`)
- Event handlers are silently dropped (they are wired at hydration time, not in HTML)

### Hydration API

```rust
use ferric::hydrate; // wasm32 only

// On the client (wasm32), after the HTML has been injected by the server:
hydrate(root_element, || my_component());
```

`pub fn hydrate<F: Fn() -> VNode + 'static>(root: web_sys::Element, f: F)`

Three-phase protocol:
1. **Adopt pass** — walk the existing DOM against the VNode tree; wire event handlers in-place;
   skip `<!--$t-->`/`<!--/$t-->` comment sentinel nodes
2. **Sentinel cleanup** — strip the TEXT_OPEN and TEXT_CLOSE comment nodes from the DOM
3. **Reactive loop** — install a `create_effect` whose re-runs call `vdom::diff` + `apply_patches`
   on signal changes

Mismatch recovery: replace the mismatched DOM node with a client-rendered equivalent and emit
`console.warn` in debug builds.

### Recommendation: use SSR for the public home/timeline route?

**Decision: NO — do not use SSR for the public timeline in the first iteration.**

**Rationale:**

1. **Framework readiness.** The SSR and hydration modules are marked as "walking skeleton"
   compositions (see `lib.rs`). The placeholders and `todo!()` stubs indicate the full
   implementation is in-progress. Using SSR before the framework layer is proven stable
   adds a risk multiplier to a new feature.

2. **Operational complexity.** SSR requires a native-compiled server-side rendering step
   integrated into the Axum server (or a separate render service). The current deployment
   is a single binary Axum server compiled for wasm-free use; adding `render_to_string` to
   the request path means the same binary must call into ferric's native build, introducing
   a cross-compilation requirement and a failure mode in the hot request path.

3. **Hydration mismatch risk.** The mismatch recovery path logs a `console.warn` and replaces
   mismatched nodes. For a public timeline whose data is fetched asynchronously (no Resource
   type, no server-side fetch), the SSR pass would render a loading skeleton and the client
   would render real data — an intentional mismatch on every request. This defeats SSR's
   primary benefit (meaningful first paint) while paying its full cost.

4. **SEO/performance trade-off.** The public timeline is real-time and user-generated; the
   first meaningful interaction is a feed of posts, not static content. CSR with an immediate
   loading skeleton is acceptable. If SEO becomes a priority later, SSR can be added
   incrementally (the API is stable and the hydration contract is clear).

5. **Path forward.** Register a plain CSR route with ferric-router. Use `spawn_local` +
   `Signal<Option<Result<Vec<Post>, E>>>` for async data loading. Add SSR as a later
   optimization only if SEO or first-contentful-paint metrics justify it.

---

## Signal / State Patterns

**Signal type:** `Signal<T>` — `Copy` generational key; `.get()` (clone + subscribe),
`.with(f)` (borrow + subscribe), `.set(value)`, `.update(f)`.

### Pattern for managing loading / error / loaded / empty states

The idiomatic pattern is a **single-signal state machine** using `Option<Result<T, E>>`:

| Signal value     | UI state     |
|-----------------|--------------|
| `None`          | Loading      |
| `Some(Err(e))`  | Error        |
| `Some(Ok([]))` | Empty list   |
| `Some(Ok(xs))` | Populated list |

```rust
let posts: Signal<Option<Result<Vec<Post>, String>>> = create_signal(None);

let timeline = move || -> VNode {
    match posts.get() {
        None => VElement::new("div").attr("class", "loading").child(text("Loading…")).into(),
        Some(Err(msg)) => {
            VElement::new("div")
                .attr("class", "error")
                .child(text(format!("Failed to load: {}", msg)))
                .into()
        }
        Some(Ok(list)) if list.is_empty() => {
            VElement::new("div")
                .attr("class", "empty")
                .child(text("No posts yet. Be the first to chirp!"))
                .into()
        }
        Some(Ok(list)) => {
            let items: Vec<VNode> = list.iter().map(|p| post_item(p)).collect();
            let mut ul = VElement::new("ul").attr("class", "timeline");
            for item in items {
                ul = ul.child(item);
            }
            // End-of-list sentinel (pagination / infinite scroll):
            // append a "load more" button or "you're all caught up" text as the last child
            ul.child(text("— end —")).into()
        }
    }
};
```

### Derived / computed state with Memo

```rust
let post_count: Memo<usize> = create_memo(move || {
    posts.get().and_then(|r| r.ok()).map(|v| v.len()).unwrap_or(0)
});
```

### Effects for side effects on state change

```rust
create_effect(move || {
    // Runs once immediately, then re-runs whenever `posts` is read-subscribed here.
    if let Some(Err(msg)) = posts.get() {
        // e.g. log to console
        web_sys::console::error_1(&msg.into());
    }
});
```

### Context API (share state across component tree)

```rust
// At the root:
provide_context(posts);           // provide_context<T: Clone + 'static>(value: T)

// In any descendant:
let posts = expect_context::<Signal<Option<Result<Vec<Post>, String>>>>();
```

---

## Module / File Locations

| API | File path |
|-----|-----------|
| Resource API | **Not implemented** — no `Resource<T, E>` type in ferric or ferric-http |
| `ferric-http` async HTTP client | `crates/ferric-http/src/lib.rs`, `src/client.rs`, `src/request.rs`, `src/response.rs`, `src/error.rs` |
| `Signal`, `Memo`, `create_signal`, `create_effect`, `create_memo`, context API | `crates/ferric/src/signal.rs` |
| `Component` trait, `Children`, `Slot`, `SlotFn` | `crates/ferric/src/component.rs` |
| `VNode`, `VElement`, `EventKind` | `crates/ferric/src/vdom.rs` (re-exported from `crates/ferric/src/lib.rs`) |
| SSR API (`render_to_string`) | `crates/ferric/src/ssr.rs` |
| Hydration API (`hydrate`) | `crates/ferric/src/hydrate.rs` (wasm32 only) |
| Router API (`Router`, `navigate`, `navigate_replace`, `current_path`) | `crates/ferric-router/src/router.rs` |
| Route matching (`RoutePattern`, `Params`) | `crates/ferric-router/src/matcher.rs` |
| In-app link (`link`, `Link`) | `crates/ferric-router/src/link.rs` |
| Ferric prelude | `crates/ferric/src/lib.rs` (`ferric::prelude::*`) |
| Ferric-router prelude | `crates/ferric-router/src/lib.rs` (`ferric_router::prelude::*`) |
| Full router example | `crates/ferric-router/examples/app.rs` |
