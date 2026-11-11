## Verdict

FINDINGS

---

## Findings

### Finding 1: `public_timeline` doc comment claims ISO 8601; the server type is `i64`

- **Location**: `crates/chirp-frontend/src/api.rs`, line 217 at commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- **Principle at stake**: A public method's documentation must describe the wire contract it actually implements. When the doc says one format and the server enforces another, any new caller following the doc gets a 422.
- **Why it matters**: The method doc at line 217 reads "Query params: `before` (ISO 8601 cursor), `limit` (1-50, default 20)." The server's `PublicTimelineQuery.before` is `Option<i64>` (lines 151–155 of `crates/chirp-types/src/api.rs`), which serde deserializes from a decimal integer query string. If a caller reads the doc and passes an ISO 8601 string such as `"2024-01-15T10:30:00Z"`, the server returns a 422 — the string is not parseable as `i64`. Both current callers work correctly: `landing.rs` line 201 and `public_profile.rs` line 244 each extract an `i64` timestamp from the response and call `.to_string()`, producing a decimal integer string (e.g., `"1700000000000"`) that the server parses without error. The runtime type contract is consistent; the documentation is not.
- **Severity**: non-blocking
- **Satisfying condition**: The sentence at `crates/chirp-frontend/src/api.rs` line 217 must replace "before (ISO 8601 cursor)" with wording that matches the actual wire format, e.g., "before (Unix timestamp in milliseconds as a decimal integer string)." The same correction should be applied to the module-level pagination notes in `crates/chirp-frontend/src/landing.rs` line 19 and `crates/chirp-frontend/src/public_profile.rs` line 15, both of which describe the cursor as "ISO 8601" when the stored and transmitted value is an `i64` millisecond timestamp.

---

## Clean Account

- **Concern 4 — Spec deviation (`before` milliseconds vs ISO 8601)**: Checked `PublicTimelineQuery.before` in `crates/chirp-types/src/api.rs` lines 142–155 at the pinned commit: the type is `Option<i64>`, the deviation from the external ISO 8601 spec is acknowledged in the struct doc comment with a stated rationale (consistency with the domain `Timestamp` type). Traced both callers of `public_timeline` and `public_user_profile` in `crates/chirp-frontend/src/landing.rs` (line 201) and `crates/chirp-frontend/src/public_profile.rs` (line 244): both extract an `i64` timestamp from the most recent response item, convert with `.to_string()`, and pass the resulting decimal string. The server parses this as `i64` without error — no live type mismatch exists. The spec deviation is bounded: server documentation is accurate, callers are correct. The finding is the wrong format claim in the client method doc at `crates/chirp-frontend/src/api.rs` line 217, which would cause any new caller following the doc to pass an ISO 8601 string and receive a 422. → Finding 1 (non-blocking).
