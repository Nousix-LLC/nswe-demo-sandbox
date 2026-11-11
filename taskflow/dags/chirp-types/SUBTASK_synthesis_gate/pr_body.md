## chirp-types — shared domain model + client↔server API contract (#7)

Adds `crates/chirp-types`, the single source of truth for every type that crosses the wire between
`chirp-server` (#8) and `chirp-frontend` (#9). Pure data + validation + `serde` derives — no I/O,
no framework, no async, no server/wasm deps — so both a native server and a wasm frontend import it
unchanged.

### Design

- **`ids`** — opaque, type-safe id newtypes `UserId`/`ChirpId` (`#[serde(transparent)]` → bare JSON
  numbers) via a local `opaque_id!` macro, plus `Timestamp` (epoch-millis, UTC, as a JSON number).
  `u64` newtypes over UUIDs keep the contract dependency-light and let the representation change
  later without breaking field names.
- **`domain`** — entities `User`, `Chirp` (optional `replyTo` for threads), `Follow`, `Like`, and
  the `Timeline` aggregate; validated value objects `Username` (1..=15, ASCII alnum/underscore) and
  `ChirpText` (1..=280, counted by Unicode scalar). Value objects use `#[serde(try_from = "String")]`
  so **invalid values are rejected on deserialize**, not merely in constructors. Documented
  invariants: `follower_id != followee_id`; one like per (user, chirp); denormalized counts are
  read-only to clients.
- **`api`** — request/response DTOs (login, create-user, create-chirp, timeline query,
  follow/unfollow, like/unlike), a generic `Page<T>` pagination envelope, and the wire error
  contract `ApiError` / `ErrorCode` (`SCREAMING_SNAKE_CASE`). Responses reuse entity types where a
  response *is* the entity; dedicated DTOs only where the wire shape differs.

### Wire conventions (explicit + stable)

camelCase object fields pinned by `#[serde(rename_all = "camelCase")]` (renaming a Rust field does
not change JSON); transparent opaque wrappers; validation-on-deserialize for value objects;
`SCREAMING_SNAKE_CASE` error codes; timestamps as epoch-millis JSON numbers.

### Dependencies

`serde` (derive) is the only runtime dependency; `serde_json` is a **dev-dependency** (round-trip
tests only — consumers pick their own wire format). Centralized in `[workspace.dependencies]` so
#8/#9 share one version. No `uuid`/time crate; no server/wasm deps.

### Verification (authoritative gate run on the clone)

| Check | Result |
|-------|--------|
| `cargo build --workspace` | ✅ pass |
| `cargo test -p chirp-types` | ✅ pass — 18 unit tests + 1 doctest, 0 failed |
| `cargo fmt --check` | ✅ clean |
| `cargo clippy --all-targets -- -D warnings` | ✅ clean (0 warnings) |

Diff is scoped to the new crate plus two centralized `[workspace.dependencies]` lines and the
lockfile; no other crate (including `ferric`) is touched.

Closes #7
