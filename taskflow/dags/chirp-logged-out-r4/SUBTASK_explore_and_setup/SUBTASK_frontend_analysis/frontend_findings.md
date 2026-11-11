# chirp-frontend Structure Findings

## Router Setup

- **Router registration file**: `crates/chirp-frontend/src/app.rs`
- **How routes are registered**: The `start()` function in `app.rs` constructs a `ferric_router::Router` using a builder chain, adding routes via `.route(path, handler_fn)`, a fallback via `.fallback(handler_fn)`, then calling `.mount_history()` to activate History-API–based client-side routing:

  ```rust
  let router = Router::new()
      .route("/", move |_params| timeline_view(&timeline_ctx))
      .route("/compose", move |_params| compose_view(&compose_ctx))
      .route("/user/:id", move |params| profile_view(&profile_ctx, params))
      .fallback(|_params| not_found_view())
      .mount_history();
  ```

  Each handler closure captures a clone of `AppContext` (called `*_ctx`). The closure receives a `params` map for dynamic segments (e.g. `:id`).

- **Where new routes need to be added**: Inside the `start()` function in `app.rs`, by inserting additional `.route(...)` calls before `.fallback(...)`. The corresponding `AppContext` clone for the new view must also be created in `start()` before the router chain.

---

## Existing Routes

- **Sign-in route path**: **not found** — there is no dedicated `/login`, `/sign-in`, or `/signin` route.
  - *Note*: A login form DOES exist inline at `/compose` (`crates/chirp-frontend/src/compose.rs`). When no session is present, `compose_view` renders a handle-entry login form instead of the compose textarea. There is no standalone sign-in page.
- **Sign-up route path**: **not found** — there is no `/register`, `/sign-up`, or `/signup` route, and no registration/create-account form anywhere in the base codebase.
- **Home/landing route**: `/` → `timeline_view` (`crates/chirp-frontend/src/timeline.rs`)
  - Currently calls `ctx.client().timeline(...)` which requires an authenticated session (passes a `Bearer` token). There is no public/unauthenticated timeline at the base commit.
- **Other notable routes**:
  - `/compose` → `compose_view` (`crates/chirp-frontend/src/compose.rs`) — dual-state: login form (logged out) or compose form (logged in)
  - `/user/:id` → `profile_view` (`crates/chirp-frontend/src/profile.rs`) — user profile view
  - `(fallback)` → `not_found_view` (`crates/chirp-frontend/src/app.rs`) — 404 inline

---

## Component Module Layout

- **Directory convention**: Flat, feature-based modules — all source files are siblings directly under `crates/chirp-frontend/src/`. No `components/`, `pages/`, or `views/` subdirectory hierarchy. The convention is one file per feature view or cross-cutting concern.

- **Module inventory** (all 6 modules declared in `lib.rs`):
  | Module | File | Role |
  |--------|------|------|
  | `app` | `src/app.rs` | Composition root: router setup, `AppContext` struct, `start()` entry point, nav bar |
  | `api` | `src/api.rs` | `ApiClient` — the single HTTP client wrapper for all backend calls |
  | `error` | `src/error.rs` | `AppError` — unified error type every view branches on |
  | `timeline` | `src/timeline.rs` | Timeline view (`/`) — chirp list with pagination |
  | `compose` | `src/compose.rs` | Compose + login view (`/compose`) |
  | `profile` | `src/profile.rs` | User profile view (`/user/:id`) |

- **Naming convention**:
  - Module files: lowercase `snake_case` (e.g. `timeline.rs`, `compose.rs`)
  - Entry point function: `<module>_view(ctx: &AppContext) -> VNode` (e.g. `timeline_view`, `compose_view`)
  - Internal helpers: lowercase `snake_case` functions within the same file
  - Cross-cutting types shared across modules: defined in `app.rs` (`AppContext`, `Session`) or `error.rs` (`AppError`)

- **Where new components should live**: Create a new `src/<feature>.rs` file (e.g. `src/sign_in.rs`, `src/sign_up.rs`) and declare it in `src/lib.rs` as `pub mod sign_in;`. Follow the `<feature>_view(ctx: &AppContext) -> VNode` signature for the route entry point. Register the route in `app.rs`'s `start()` function.

---

## API Call Pattern

- **HTTP client**: Custom `ApiClient` struct in `crates/chirp-frontend/src/api.rs`, wrapping `ferric_http::Client`. Not `reqwest`, not raw `web-sys` fetch.

- **Base URL source**: Compile-time constant with optional env-var override:
  ```rust
  const DEFAULT_API_BASE_URL: &str = "/api";
  // resolved at build time via:
  option_env!("CHIRP_API_BASE_URL").unwrap_or(DEFAULT_API_BASE_URL)
  ```
  At runtime the base URL is stored in `AppContext.base_url: String` and passed into `ApiClient` on each call.

- **Request construction pattern**:
  ```rust
  // ApiClient builds a fresh ferric_http::Client per call, injecting the Bearer token when present
  fn http_client(&self) -> Client {
      let mut builder = Client::builder().base_url(self.base_url.clone());
      if let Some(token) = &self.token {
          builder = builder.default_header("Authorization", &format!("Bearer {}", token.0));
      }
      builder.build()
  }

  // GET example (unauthenticated query)
  self.http_client().get("/path").send_json().await

  // POST example (with request body)
  self.http_client().post("/path").json(body).send_json().await

  // DELETE example
  self.http_client().delete("/path").send_empty().await
  ```
  All paths are relative to `base_url` (e.g. `"/sessions"`, `"/users"`, `"/chirps"`).

- **Auth mechanism**: The `ApiClient` is initialized from an `AppContext` that holds a `Signal<Option<Session>>`. When a session is present, `ApiClient::new(ctx)` extracts `ctx.session.get().map(|s| s.token)` and passes `Bearer <token>` as a default header.

- **Error handling approach**: All `ferric_http::Error` values are converted into `AppError` (defined in `src/error.rs`) either via the `From<HttpError>` impl (`?` operator) or `AppError::from_http(err)`. `AppError` has three variants:
  - `AppError::Api(ApiError)` — non-2xx with a decodable server error body
  - `AppError::Network(String)` — fetch failed before a response (offline/DNS/CORS)
  - `AppError::Transport(String)` — any other transport/encoding failure
  Views call `err.user_message()` to get a human-readable banner string.

- **Existing API methods** (all in `src/api.rs`):
  | Method | HTTP | Path | Auth required |
  |--------|------|------|---------------|
  | `login` | POST | `/sessions` | No |
  | `create_user` | POST | `/users` | No |
  | `timeline` | GET | `/timeline` | Yes (Bearer) |
  | `create_chirp` | POST | `/chirps` | Yes |
  | `get_user` | GET | `/users/{id}` | No |
  | `set_follow` | PUT/DELETE | `/users/{id}/follow` | Yes |
  | `set_like` | PUT/DELETE | `/chirps/{id}/like` | Yes |

  **Gap**: No `public_timeline` method exists. The design spec requires a public timeline for logged-out visitors; a new `ApiClient` method will be needed (likely `GET /timeline` without auth, or a separate `/public_timeline` endpoint per whatever the server exposes).

---

## Files to Modify / Create

- **Router file**: `crates/chirp-frontend/src/app.rs` — add new route registrations inside `start()`. Also contains the nav bar; new nav links (e.g. Sign In, Sign Up) need to be added to the nav `VElement` in `start()`.
- **Module declarations**: `crates/chirp-frontend/src/lib.rs` — add `pub mod <new_module>;` for each new view file.
- **API client**: `crates/chirp-frontend/src/api.rs` — add `public_timeline` method (and potentially `create_account` / `sign_up` if the backend exposes a registration endpoint separate from `POST /users`).
- **Recommended new component files**:
  - `crates/chirp-frontend/src/sign_in.rs` — dedicated sign-in page (if a standalone `/sign-in` route is needed beyond the inline login in `/compose`)
  - `crates/chirp-frontend/src/sign_up.rs` — sign-up / registration page at `/sign-up`
  - `crates/chirp-frontend/src/landing.rs` — public landing/home page (if `/` should show a different view for logged-out visitors rather than redirecting)
  - Alternatively: augment `timeline.rs` to branch on `ctx.session` and render a public timeline or CTA when logged out (avoids a new file for the `/` route case)
