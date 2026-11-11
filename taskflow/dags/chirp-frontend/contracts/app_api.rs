// contracts/app_api.rs — FROZEN in-crate public signatures for `chirp-frontend` (#9).
//
// READ-ONLY. This is the seam the decomposition freezes. SUBTASK_scaffold realizes
// these signatures verbatim in `src/` (as the compiling walking skeleton); the feature
// spokes import them from `crate::...` and fill in the bodies. Signatures are
// signature-identical between the scaffold stub and the real impl, so feature spokes
// compile against the stub and recompose against the real impl at the gate.
//
// Types from `chirp_types::prelude::*` are the wire contract — used directly, never
// redefined. `ferric`/`ferric-router` types come from their preludes. This file fixes
// the SHAPE; bodies/behaviour are the owning spoke's (see each _BRIEF.md). It is a
// specification artifact, not a compiled module.

use chirp_types::prelude::*;                 // DTOs — the wire contract (do not redefine)
use ferric::prelude::*;                       // Signal, VNode, mount, ...
use ferric_router::prelude::Params;           // route params for profile_view

// ---------------------------------------------------------------------------------
// error.rs  (owner: SUBTASK_scaffold)
// ---------------------------------------------------------------------------------

/// The single error type the UI branches on. Every `ferric_http::Error` and every
/// decodable server `ApiError` funnels through here so views render coherent states.
pub enum AppError {
    /// A non-2xx response whose JSON body decoded to the server's wire error contract.
    Api(ApiError),
    /// `fetch` failed before a response arrived (offline/DNS/CORS). Human-readable text.
    Network(String),
    /// Any other transport/encoding failure (builder/body/(de)serialize, or a non-2xx
    /// whose body was not a decodable `ApiError`). Human-readable text.
    Transport(String),
}

impl AppError {
    /// Map a `ferric_http::Error` into an `AppError`, decoding a `chirp_types::ApiError`
    /// out of a non-2xx `Error::Status { body }` when the body is a valid error document.
    pub fn from_http(err: ferric_http::Error) -> Self { unimplemented!("scaffold realizes; see error.rs") }
    /// A short, user-facing message suitable for an error banner.
    pub fn user_message(&self) -> String { unimplemented!() }
    /// The machine-readable category when this is a decoded server error.
    pub fn code(&self) -> Option<ErrorCode> { unimplemented!() }
}

// ---------------------------------------------------------------------------------
// app.rs  (owner: SUBTASK_scaffold) — composition root + shared reactive state
// ---------------------------------------------------------------------------------

/// The authenticated session: the current user and their bearer token. `None` session
/// means "logged out". Set by the compose/login flow; read by any view that needs auth.
#[derive(Clone)]
pub struct Session {
    pub user: User,
    pub token: SessionToken,
}

/// Shared, cheaply-cloneable application context handed to every route view. Holds the
/// configurable API base URL and the reactive session signal. `Signal` is `Copy`, so
/// `AppContext` is `Clone`.
#[derive(Clone)]
pub struct AppContext {
    /// Base URL the ApiClient targets (default `/api`; see rest_endpoints.md). Configurable.
    pub base_url: String,
    /// Reactive current session; writing it (login/logout) re-renders dependent views.
    pub session: Signal<Option<Session>>,
}

impl AppContext {
    /// Build a context with a base URL and an empty (logged-out) session signal.
    pub fn new(base_url: impl Into<String>) -> Self { unimplemented!() }
    /// An `ApiClient` configured for the current session (adds the bearer token, if any).
    pub fn client(&self) -> ApiClient { unimplemented!() }
}

/// Wasm entry (thin; owner: SUBTASK_scaffold). Builds the `AppContext`, the `Router`
/// route table (`/`->timeline_view, `/compose`->compose_view, `/user/:id`->profile_view,
/// plus a fallback), the persistent nav, and `mount`s the root into `#app`/`<body>`.
/// MAY use `expect()` for mount-point acquisition (documented), mirroring the examples.
pub fn start() { unimplemented!("scaffold realizes the composition root") }

// ---------------------------------------------------------------------------------
// api.rs  (owner: SUBTASK_api_client) — typed REST client over ferric-http + chirp-types
// ---------------------------------------------------------------------------------

/// Typed async REST client. Wraps `ferric_http::Client`, (de)serializes `chirp_types`
/// DTOs, attaches the bearer token when present, and maps every failure to `AppError`
/// (decoding a server `ApiError` from a non-2xx body). Cheap to clone.
///
/// Each method's REST method+path and DTOs are frozen in `rest_endpoints.md`.
pub struct ApiClient { /* ferric_http::Client + optional SessionToken (owner-designed) */ }

impl ApiClient {
    /// New client for `base_url` with no token (logged out).
    pub fn new(base_url: impl Into<String>) -> Self { unimplemented!() }
    /// Same client carrying a bearer token added to each request's `Authorization` header.
    pub fn with_token(self, token: SessionToken) -> Self { unimplemented!() }

    /// `POST /sessions`  — LoginRequest -> AuthResponse
    pub async fn login(&self, req: &LoginRequest) -> Result<AuthResponse, AppError> { unimplemented!() }
    /// `POST /users`     — CreateUserRequest -> User
    pub async fn create_user(&self, req: &CreateUserRequest) -> Result<User, AppError> { unimplemented!() }
    /// `POST /chirps`    — CreateChirpRequest -> Chirp
    pub async fn create_chirp(&self, req: &CreateChirpRequest) -> Result<Chirp, AppError> { unimplemented!() }
    /// `GET  /timeline`  — TimelineQuery (query string) -> Page<Chirp>
    pub async fn timeline(&self, query: &TimelineQuery) -> Result<Page<Chirp>, AppError> { unimplemented!() }
    /// `GET  /users/{id}` — -> User
    pub async fn get_user(&self, id: UserId) -> Result<User, AppError> { unimplemented!() }
    /// `PUT`/`DELETE /users/{id}/follow` (by `follow`) -> FollowResponse
    pub async fn set_follow(&self, id: UserId, follow: bool) -> Result<FollowResponse, AppError> { unimplemented!() }
    /// `PUT`/`DELETE /chirps/{id}/like` (by `like`) -> LikeResponse
    pub async fn set_like(&self, id: ChirpId, like: bool) -> Result<LikeResponse, AppError> { unimplemented!() }
}

// ---------------------------------------------------------------------------------
// Route views — frozen signatures (owners: the three feature spokes). The scaffold's
// route table binds each to its path; each spoke fills in its module behind the seam.
// Async data loads are driven by `wasm_bindgen_futures::spawn_local`, which updates
// `ferric` signals on completion (fetch -> signal -> reactive re-render). Each view owns
// local loading/data/error signals and renders loading/error/empty/content states.
// ---------------------------------------------------------------------------------

/// `/` — timeline. Loads `Page<Chirp>` via `ctx.client().timeline(..)`, renders a keyed
/// list (by `ChirpId`), with loading/error/empty states and cursor pagination.
/// (owner: SUBTASK_timeline, src/timeline.rs)
pub fn timeline_view(ctx: &AppContext) -> VNode { unimplemented!() }

/// `/compose` — login + compose. Handle-based login sets `ctx.session`; a validated
/// (`ChirpText`) compose form calls `create_chirp`, surfacing validation/API/network
/// errors. (owner: SUBTASK_compose, src/compose.rs)
pub fn compose_view(ctx: &AppContext) -> VNode { unimplemented!() }

/// `/user/:id` — profile. Reads `params.get("id")`, loads the `User`, shows profile +
/// counts, and offers follow/unfollow (`set_follow`) and like (`set_like`) actions with
/// reactive count updates. (owner: SUBTASK_profile, src/profile.rs)
pub fn profile_view(ctx: &AppContext, params: &Params) -> VNode { unimplemented!() }
