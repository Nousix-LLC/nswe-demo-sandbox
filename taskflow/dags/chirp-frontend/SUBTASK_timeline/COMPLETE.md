# COMPLETE — SUBTASK_timeline (timeline view)

## What was done
Replaced the scaffold stub with the real `timeline_view(ctx: &AppContext) -> VNode` in
`crates/chirp-frontend/src/timeline.rs`: the `/` route loads a `Page<Chirp>` through the frozen
`ApiClient` seam and renders a keyed, reactive chirp list with loading / error / empty states and
cursor-based "load more".

## Declared output (owned, written)
- `checkout/crates/chirp-frontend/src/timeline.rs`
  (abs: `/home/user/nousix-runtime/nswe-demo/taskflow/dags/chirp-frontend/checkout/crates/chirp-frontend/src/timeline.rs`)

No other file was touched. No git commands were run (Group-1 discipline: the synthesis gate owns all git).

## How it composes with the parent
- Realizes the frozen `contracts/app_api.rs` signature `timeline_view(&AppContext) -> VNode`
  verbatim; the scaffold's route table binds `/` to it unchanged.
- Composes against the **frozen** `ApiClient` seam only (`ctx.client().timeline(&TimelineQuery)`),
  i.e. the scaffold stub is the L1 mock it compiled against; the real `src/api.rs`
  (SUBTASK_api_client) drops in behind the same signature at the gate.
- Uses `chirp-types` DTOs directly (`Chirp`, `Page<Chirp>`, `Cursor`, `TimelineQuery`,
  `ChirpId`/`UserId`/`Timestamp` via accessors) — no DTO redefined.
- Surfaces failures only as `AppError` UI state via `AppError::user_message()` — never panics.

## Behavior delivered (success criteria)
- Reactive keyed list: each chirp is a `<li>` keyed by `ChirpId`, so `ferric`'s keyed diff
  reconciles by identity across loads and pagination.
- States: full-screen loading; first-load error (banner + Retry); empty ("No chirps yet.");
  loaded list with a footer that is one of inline-error+Try-again / "Loading more…" / "Load more" /
  end-of-timeline, selected from the model.
- Pagination: "load more" issues a `next_cursor` continuation and appends the page; the button
  disappears when `next_cursor` is `None`.
- Async bridge: `wasm_bindgen_futures::spawn_local` runs `ctx.client().timeline(..)` and folds the
  outcome back into the view state on completion (fetch → state → re-render).

## Key design decision (important for the synthesis gate)
`ferric` is a **coarse** re-render framework: `mount` wraps the whole render in one effect and the
route view is re-invoked on every re-render, and a signal created *inside* a running effect is
**disposed when that effect re-runs** (documented in `ferric-router`'s `router.rs`). So the literal
"create local `loading`/`data`/`error` signals inside the view" shape is unsound — the signals
would reset on the first async-driven re-render (and reading a disposed handle would panic).

The sound equivalent used here **mirrors `ferric-router`'s own `thread_local` current-path
precedent**:
- the view's data lives in a module `thread_local!` `TimelineModel` (plain data → never disposed,
  survives every re-render); and
- reactivity is driven by a tiny re-render **trigger** `Signal<u32>` that each render recreates and
  reads (subscribing the live mount effect) and that async completions / handlers bump. Because the
  trigger is recreated every render, the stored handle is always the live one while the route is
  mounted; a completion that fires after navigating away is dropped by a route guard rather than
  setting a disposed handle.

This keeps the frozen seam **adequate** — no amendment was needed. `app.rs`/`Cargo.toml` were not
modified (`wasm-bindgen-futures` was already present).

## Verification (run in `checkout/`)
- `rustfmt --edition 2021 --check …/timeline.rs` → clean.
- `cargo clippy -p chirp-frontend --all-targets -- -D warnings` → clean.
- `cargo test -p chirp-frontend` → 41 passed (11 new timeline tests: query building, all state
  reducers, and the view tree for loading/loaded-keyed/empty/initial-error/last-page states).
- `cargo build -p chirp-frontend` (native) and `cargo build -p chirp-frontend --target
  wasm32-unknown-unknown` → both succeed on the combined tree.
- No `unwrap`/`expect`/`panic!`/`todo!`/`unimplemented!`/`unsafe` anywhere in the module (runtime
  or tests); the one public item (`timeline_view`) is documented.
