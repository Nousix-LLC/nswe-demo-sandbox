# _BRIEF.md — DAG: ferric-http-r1 (swe-coder)

**Goal**: Implement the Ferric 1.0 HTTP/JSON Client (`ferric-http` crate), closing epic **#132** and sub-issue **#148** (usable_early scope). Issue #149 (one_oh: PATCH, timeout, lean footprint) is NOT in scope — it depends on #148 and #159 (OPEN).

**Branch**: `work/ferric-http-r1`  
**Base**: `main` (current HEAD `f481a5eebddb1322d60d18b349c5190aa7318493`)

**Issues to close**: #132 (epic — if all usable_early work done), #148

**Acceptance criteria — #148** (HTTP methods, JSON bodies, error handling):
- `Client` accepts a base URL at configuration time
- `RequestBuilder` chains URL resolution per RFC 3986: GET, POST, PUT, DELETE methods
- Typed `body::<T>()` serializes `T` to JSON (Content-Type: application/json)
- Typed `send::<T>()` deserializes response body as `T`
- Matchable `Error` enum covering: network failure, non-2xx status, deserialization failure
- Non-2xx responses surface as `Err` by default
- Request headers can be set per-request
- All `ferric-http` prelude surfaces present at the #6 baseline are present at 1.0 without removal or redefinition
- Stated HTTP client examples compile
- **Traces to**: REQ-HTTP-001 through REQ-HTTP-008, REQ-HTTP-011, REQ-HTTP-013; BAR-FERRIC-017

**Design references** (on main):
- `design/ferric/router-and-http.md` §http-client (Part 2)
- `design/ferric/scope-and-requirements.md`

**What is already in the codebase** (#6 baseline on main):
- `crates/ferric-http/` exists from the scaffold in #6; review existing code before adding
- Do NOT remove or redefine any existing prelude surfaces

**Machine gate**: all 6 CI jobs must PASS (fmt, clippy, test, wasm, doc, image)

**Declared output**: branch `work/ferric-http-r1`, PR closing #132 and #148, root `SYNTHESIS.md` with machine gate verdict.
