# Task Complete: Frontend Route Survey

**Task**: SUBTASK_explore-survey-frontend  
**Status**: completed

## Summary

Surveyed `crates/chirp-frontend/` at `main` / `cb1ced3` and produced `frontend-survey.md` covering all seven required sections:

1. **Crate Structure** — file layout, Cargo.toml dependencies (ferric, ferric-router, ferric-http, chirp-types), WASM build target
2. **Router Configuration** — `app.rs::start()`, configuration-based Ferric router with `.mount_history()`, no router-level auth guards
3. **Route Inventory** — full table: `/` (unauthenticated timeline), `/compose` (conditional: login form or compose form), `/user/:id` (unauthenticated profile + action hints), fallback 404
4. **Home/Landing Route Assessment** — `/` renders content unconditionally; no auth gate; no login CTA or landing copy for logged-out visitors
5. **User Profile Route Assessment** — `/user/:id` exists, is fully visible to logged-out visitors; follow/like actions degrade to informational hints; numeric `:id` not linked from timeline
6. **Component Inventory** — AppContext, Session, ApiClient, AppError, all three route views, and all reusable UI primitives
7. **Gaps** — login route absent, nav bar session-unaware, no profile links from timeline, no signup flow, no session persistence

## Output

- `frontend-survey.md` — written at this workspace
